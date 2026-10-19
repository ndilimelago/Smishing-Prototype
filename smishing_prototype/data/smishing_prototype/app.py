"""
app.py
------
Step 6 of the pipeline: Logging-and-interface component.

A simple Streamlit web app that:
1. Accepts a pasted SMS message
2. First checks it against a cache of messages ALREADY known to be
   phishing (from the permanent, shared log) for an instant result
3. Otherwise classifies it using the trained model (suspicious/legitimate)
4. Detects social-engineering tactics (rule-based)
5. Displays a plain-language warning + explanation
6. Logs every check PERMANENTLY to a shared cloud log, viewable by
   every visitor to the app (see cloud_log.py)

Run with:
    streamlit run app.py
"""

import streamlit as st
import joblib
from datetime import datetime
import os

from preprocess import clean_text
from tactic_rules import detect_tactics
from cloud_log import add_log_entry, get_all_logs, is_cloud_logging_enabled

MODEL_PATH = "model.joblib"
VECTORISER_PATH = "vectoriser.joblib"

st.set_page_config(
    page_title="SMS Smishing Detector",
    page_icon="📱",
    layout="centered",
)

# Extra polish on top of .streamlit/config.toml's toolbarMode="minimal":
# also hide the "Made with Streamlit" footer for a cleaner, standalone look.
st.markdown(
    "<style>footer {visibility: hidden;}</style>",
    unsafe_allow_html=True,
)


# --- Load model once per server, not on every click (performance cache) ---
@st.cache_resource
def load_model():
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORISER_PATH)):
        return None, None
    return joblib.load(MODEL_PATH), joblib.load(VECTORISER_PATH)


# --- Build a fast lookup cache of messages already confirmed as phishing,
#     from the permanent shared log. Refreshes every 5 minutes so new
#     entries from other users eventually appear without a manual reload. ---
@st.cache_data(ttl=300)
def load_known_phishing_cache():
    logs = get_all_logs()
    if logs.empty:
        return set()
    known = logs[logs["prediction"] == "suspicious"]["message"].astype(str)
    return set(known.str.strip().str.lower())


st.title("📱 SMS Smishing Detector")
st.caption(
    "Paste an SMS message below to check whether it shows signs of an "
    "eWallet phishing (smishing) scam."
)

if not is_cloud_logging_enabled():
    st.info(
        "ℹ️ Running in local mode: the shared permanent log is not yet "
        "configured. See README.md to connect Firebase so every check is "
        "saved permanently and visible to all users.",
        icon="ℹ️",
    )

model, vectoriser = load_model()
if model is None:
    st.error("Model not found. Please run `python train_model.py` first.")
    st.stop()

known_phishing_cache = load_known_phishing_cache()

# --- User input ---
message = st.text_area("Paste the SMS message here:", height=100)
check_button = st.button("Check Message")

if check_button and message.strip():
    cleaned = clean_text(message)
    is_known = cleaned.strip() in known_phishing_cache

    if is_known:
        # Cache hit: this exact message was already reported as phishing
        # by a previous user, so we can skip re-running the model.
        prediction = "suspicious"
        confidence = 1.0
        tactics = detect_tactics(cleaned)
        st.error("⚠️ This message looks SUSPICIOUS (previously reported)")
        st.caption("This exact message was already flagged by another user "
                   "and found in the known-phishing cache.")
    else:
        # Classification component
        vec = vectoriser.transform([cleaned])
        prediction = model.predict(vec)[0]
        confidence = model.predict_proba(vec).max()
        tactics = detect_tactics(cleaned)

        if prediction == "suspicious":
            st.error(f"⚠️ This message looks SUSPICIOUS ({confidence:.0%} confidence)")
        else:
            st.success(f"✅ This message looks LEGITIMATE ({confidence:.0%} confidence)")

    if prediction == "suspicious":
        if tactics:
            st.write("**Tactics detected:**")
            for t in tactics:
                st.write(f"- {t}")
        else:
            st.write("No specific known tactic phrases were matched, but the "
                      "overall wording pattern resembled scam messages.")
        st.info(
            "Tip: Never share your PIN, password, or OTP with anyone. "
            "Contact your bank or mobile-money provider directly using a "
            "number you already trust, not one from this message."
        )

    # --- Logging component: permanent, shared with all users ---
    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "message": message,
        "prediction": prediction,
        "confidence": round(float(confidence), 2),
        "tactics_detected": "; ".join(tactics) if tactics else "None",
        "from_cache": is_known,
    }
    add_log_entry(log_entry)
    # Refresh the cache so this message is caught instantly if resubmitted
    load_known_phishing_cache.clear()

elif check_button:
    st.warning("Please paste a message first.")

# --- Shared, permanent log -- visible to every visitor, not just you ---
st.divider()
st.subheader("📋 Shared Log of Checked Messages")
st.caption("This log is permanent and shared across all users of this app.")
logs_df = get_all_logs()
if not logs_df.empty:
    st.dataframe(logs_df, use_container_width=True)
else:
    st.write("No messages checked yet.")
