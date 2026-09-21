"""
train_model.py
----------------
Step 4 of the pipeline: Train the classification component.

Trains a Naive Bayes classifier (TF-IDF features) to label an SMS
as 'suspicious' or 'legitimate', then saves the model + vectoriser
to disk so the Streamlit app can load them instantly.

Run this whenever you update data/sms_dataset.csv:
    python train_model.py
"""

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

from preprocess import clean_text

DATA_PATH = "data/sms_dataset.csv"
MODEL_PATH = "model.joblib"
VECTORISER_PATH = "vectoriser.joblib"


def main():
    # 1. Load and clean the dataset
    df = pd.read_csv(DATA_PATH)
    df["clean_message"] = df["message"].apply(clean_text)

    X = df["clean_message"]
    y = df["label"]

    # 2. Split into train/test (small dataset -> keep test set small too)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # 3. TF-IDF feature extraction
    vectoriser = TfidfVectorizer()
    X_train_vec = vectoriser.fit_transform(X_train)
    X_test_vec = vectoriser.transform(X_test)

    # 4. Train the classifier
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    # 5. Evaluate (these are the figures to report in Chapter 4)
    y_pred = model.predict(X_test_vec)
    print("=== Technical Evaluation Results ===")
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.2f}")
    print(f"Precision: {precision_score(y_test, y_pred, pos_label='suspicious'):.2f}")
    print(f"Recall   : {recall_score(y_test, y_pred, pos_label='suspicious'):.2f}")
    print(f"F1-score : {f1_score(y_test, y_pred, pos_label='suspicious'):.2f}")
    print("Confusion matrix (rows=actual, cols=predicted):")
    print(confusion_matrix(y_test, y_pred, labels=["suspicious", "legitimate"]))

    # 6. Save model + vectoriser for the Streamlit app to reuse
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectoriser, VECTORISER_PATH)
    print(f"\nSaved '{MODEL_PATH}' and '{VECTORISER_PATH}'.")


if __name__ == "__main__":
    main()
