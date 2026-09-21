"""
app.py
------
Step 6 of the pipeline: Logging-and-interface component.

A simple Streamlit web app that:
1. Accepts a pasted SMS message
2. Classifies it as suspicious/legitimate (trained model)
3. Detects social-engineering tactics (rule-based)
4. Displays a plain-language warning + explanation
5. Logs every check to log.csv

Run with:
    streamlit run app.py
"""

import streamlit as st
import joblib
import pandas as pd
from datetime import datetime
import os

from preprocess import clean_text
from tactic_rules import detect_tactics

MODEL_PATH = "model.joblib"
VECTORISER_PATH = "vectoriser.joblib"
LOG_PATH = "log.csv"

st.set_page_config(page_title="SMS Scam Detector", page_icon="📱")

st.title("📱 SMS Smishing Detector")
st.caption(
    "Paste an SMS message below to check whether it shows signs of a "
    "mobile-money phishing (smishing) scam."
)

# --- Load model (trained separately via train_model.py) ---
if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORISER_PATH)):
    st.error("Model not found. Please run `python train_model.py` first.")
    st.stop()

model = joblib.load(MODEL_PATH)
vectoriser = joblib.load(VECTORISER_PATH)

# --- User input ---
message = st.text_area("Paste the SMS message here:", height=100)
check_button = st.button("Check Message")

if check_button and message.strip():
    cleaned = clean_text(message)

    # Classification component
    vec = vectoriser.transform([cleaned])
    prediction = model.predict(vec)[0]
    confidence = model.predict_proba(vec).max()

    # Tactic-detection component
    tactics = detect_tactics(cleaned)

    # --- Display result ---
    if prediction == "suspicious":
        st.error(f"⚠️ This message looks SUSPICIOUS ({confidence:.0%} confidence)")
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
    else:
        st.success(f"✅ This message looks LEGITIMATE ({confidence:.0%} confidence)")

    # --- Logging component ---
    log_entry = pd.DataFrame([{
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "message": message,
        "prediction": prediction,
        "confidence": round(float(confidence), 2),
        "tactics_detected": "; ".join(tactics) if tactics else "None",
    }])
    log_entry.to_csv(
        LOG_PATH, mode="a", header=not os.path.exists(LOG_PATH), index=False
    )

elif check_button:
    st.warning("Please paste a message first.")

# --- Show log for demonstration/testing sessions ---
with st.expander("View log of checked messages"):
    if os.path.exists(LOG_PATH):
        st.dataframe(pd.read_csv(LOG_PATH))
    else:
        st.write("No messages checked yet.")
