"""
cloud_log.py
-------------
Persistent, shared logging for the SMS Smishing Detector.

Problem this solves: a log file written to local disk (log.csv) is NOT
permanent on Streamlit Community Cloud -- the app's filesystem resets
whenever the app restarts, redeploys, or goes to sleep. It is also not
properly "shared": if two people open the app in different sessions,
they would not reliably see each other's checks.

This module writes every checked message to a Firebase Realtime
Database over a simple REST API (no SDK, just `requests`), so:
  - logs persist permanently across restarts/redeploys
  - every visitor to the app sees the same, shared log
  - no server of your own needs to be kept running

If Firebase is not configured (e.g. running locally without secrets
set up yet), this module automatically falls back to a local log.csv
file so the app still works during development.

SETUP (see README.md for full step-by-step instructions):
  1. Create a free Firebase project and enable "Realtime Database".
  2. Copy your Database URL (looks like
     https://<project-id>-default-rtdb.<region>.firebasedatabase.app).
  3. In Streamlit Cloud: App settings -> Secrets, add:
         FIREBASE_DB_URL = "https://your-project-default-rtdb...app"
"""

import os
import requests
import pandas as pd
import streamlit as st

LOCAL_LOG_PATH = "log.csv"


def _get_db_url():
    """Read the Firebase Realtime Database URL from Streamlit secrets."""
    try:
        return st.secrets["FIREBASE_DB_URL"].rstrip("/")
    except Exception:
        return None


def is_cloud_logging_enabled() -> bool:
    return _get_db_url() is not None


def add_log_entry(entry: dict) -> bool:
    """Save one log entry (a dict) permanently. Returns True on success."""
    db_url = _get_db_url()
    if db_url:
        try:
            # POST appends a new, uniquely-keyed child under /logs in the
            # database -- this is Firebase's standard way of storing a
            # permanent, ever-growing list of records.
            resp = requests.post(f"{db_url}/logs.json", json=entry, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            st.warning(f"Could not save to cloud log, saving locally instead. ({e})")

    # Fallback: local CSV (not permanent on Streamlit Cloud, but keeps
    # the app usable during local development before Firebase is set up)
    df = pd.DataFrame([entry])
    df.to_csv(LOCAL_LOG_PATH, mode="a", header=not os.path.exists(LOCAL_LOG_PATH),
              index=False)
    return True


def get_all_logs() -> pd.DataFrame:
    """Return every logged check, shared across all users, newest first."""
    db_url = _get_db_url()
    if db_url:
        try:
            resp = requests.get(f"{db_url}/logs.json", timeout=10)
            data = resp.json()
            if not data:
                return pd.DataFrame()
            df = pd.DataFrame(list(data.values()))
            if "timestamp" in df.columns:
                df = df.sort_values("timestamp", ascending=False)
            return df.reset_index(drop=True)
        except Exception as e:
            st.warning(f"Could not load cloud log. ({e})")
            return pd.DataFrame()

    if os.path.exists(LOCAL_LOG_PATH):
        df = pd.read_csv(LOCAL_LOG_PATH)
        return df.sort_values("timestamp", ascending=False).reset_index(drop=True)
    return pd.DataFrame()
