# SMS Smishing Detector — Prototype

A lightweight AI-based prototype that detects SMS phishing (smishing)
messages and logs the social-engineering tactics used, built to match
Chapter 3 of the thesis (Analysis → Design → Development → Test →
Deployment).

## Project structure

```
smishing_prototype/
├── data/
│   └── sms_dataset.csv     # labelled SMS examples (suspicious/legitimate)
├── preprocess.py           # text cleaning (Step 3: preprocessing component)
├── tactic_rules.py         # rule-based tactic detection (Step 5)
├── train_model.py          # trains + evaluates the classifier (Step 4)
├── app.py                  # Streamlit web interface + logging (Step 6)
├── requirements.txt
└── README.md
```

## How to run it (step by step)

### 1. Install Python
Download Python 3.10+ from https://www.python.org/downloads/ if you
don't have it. Confirm it's installed:
```
python --version
```

### 2. Open this folder in a terminal
```
cd smishing_prototype
```

### 3. (Recommended) Create a virtual environment
```
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 4. Install the required libraries
```
pip install -r requirements.txt
```

### 5. Train the model
This reads `data/sms_dataset.csv`, trains the classifier, prints
accuracy/precision/recall/F1-score (use these in Chapter 4), and saves
`model.joblib` + `vectoriser.joblib`.
```
python train_model.py
```

### 6. Launch the app
```
streamlit run app.py
```
This opens a browser tab where you can paste an SMS message and see
the result. Every check is logged to `log.csv` for your Test-phase
evaluation sessions.

## Growing this for your thesis

- **Add more data**: the more real/simulated SMS examples you add to
  `data/sms_dataset.csv` (more rows = better), the more reliable the
  classifier becomes. Aim for at least 100–200 labelled messages if you
  can, roughly balanced between suspicious and legitimate.
- **Add more tactic keywords**: edit `TACTIC_KEYWORDS` in
  `tactic_rules.py` to catch more phrasing.
- **Re-train after every data change**: just re-run `train_model.py`.
- **For your Test phase**: run `streamlit run app.py`, have your
  participants paste in the prepared test messages, and use the
  `log.csv` file + `view log of checked messages` expander as evidence
  during your evaluation sessions.
- **For deployment (Section 3.7.1)**: you can host this for free on
  [Streamlit Community Cloud](https://streamlit.io/cloud) by pushing
  this folder to a GitHub repo and connecting it — no server cost.
