"""
preprocess.py
--------------
Step 3 of the pipeline: Text preprocessing.
Cleans raw SMS text before it is fed into the classifier.
"""

import re


def clean_text(text: str) -> str:
    """Lowercase, strip URLs/punctuation/extra whitespace from an SMS message."""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\.\S+", " url ", text)   # normalise links
    text = re.sub(r"[^a-z0-9\s]", " ", text)             # remove punctuation
    text = re.sub(r"\s+", " ", text).strip()              # collapse whitespace
    return text


if __name__ == "__main__":
    sample = "URGENT!! Verify your PIN now: bit.ly/verify-ew"
    print(clean_text(sample))
