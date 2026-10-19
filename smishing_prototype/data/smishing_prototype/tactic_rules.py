"""
tactic_rules.py
----------------
Step 5 of the pipeline: Rule-based social-engineering tactic detection.
This does NOT require training -- it is a simple keyword/phrase dictionary.
Easy to extend: just add more phrases under each tactic.
"""

TACTIC_KEYWORDS = {
    "Impersonation": [
        "bank windhoek", "fnb", "nampost", "mtc", "ewallet", "nampower",
        "this is your bank", "official", "customer service",
    ],
    "Urgency / Threat": [
        "urgent", "immediately", "now", "today", "last warning",
        "will be blocked", "will be suspended", "will be closed",
        "24hrs", "expire", "before it expires",
    ],
    "Request for Confidential Info": [
        "pin", "otp", "password", "account number", "id number",
        "verify your identity", "confirm your otp", "card pin",
    ],
    "Prize / Refund Lure": [
        "won", "congratulations", "selected", "cash prize", "refund",
        "claim", "reward",
    ],
    "Suspicious Link / Payment Request": [
        "click here", "click link", "bit.ly", ".tk", "pay a", "processing fee",
        "clearance fee", "pay-now",
    ],
}


def detect_tactics(cleaned_text: str) -> list[str]:
    """Return a list of social-engineering tactics found in the message."""
    found = []
    for tactic, phrases in TACTIC_KEYWORDS.items():
        if any(phrase in cleaned_text for phrase in phrases):
            found.append(tactic)
    return found


if __name__ == "__main__":
    from preprocess import clean_text

    msg = "URGENT: Your eWallet account has been suspended. Verify your PIN now at bit.ly/verify-ew"
    print(detect_tactics(clean_text(msg)))
