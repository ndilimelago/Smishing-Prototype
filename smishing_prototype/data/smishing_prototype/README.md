# SMS Smishing Detector — Prototype

A lightweight AI-based prototype that detects SMS phishing (smishing)
messages and logs the social-engineering tactics used, built to match
Chapter 3 of the thesis (Analysis → Design → Development → Test →
Deployment).

## Project structure

```
smishing_prototype/
├── .streamlit/
│   └── config.toml          # hides Share/Star/GitHub/Edit icons, sets theme
├── data/
│   └── sms_dataset.csv      # labelled SMS examples (suspicious/legitimate)
├── preprocess.py            # text cleaning (Step 3: preprocessing component)
├── tactic_rules.py          # rule-based tactic detection (Step 5)
├── train_model.py           # trains + evaluates the classifier (Step 4)
├── cloud_log.py             # permanent, shared logging + phishing cache
├── app.py                   # Streamlit web interface + logging (Step 6)
├── requirements.txt
└── README.md
```

## How to run it locally (step by step)

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
accuracy/precision/recall/F1-score, and saves `model.joblib` +
`vectoriser.joblib`.
```
python train_model.py
```

### 6. Launch the app
```
streamlit run app.py
```
Without Firebase configured (see below), the log is saved locally to
`log.csv` so the app still works while you're developing.

---

## Making the log permanent and shared by all users (Firebase setup)

By default, a log file saved to disk on Streamlit Community Cloud is
**not permanent** — it is wiped whenever the app restarts, redeploys,
or goes to sleep — and is not reliably shared across different users'
sessions. To fix this, `cloud_log.py` uses a free **Firebase Realtime
Database** as a permanent, shared log that every visitor to the app
reads from and writes to.

### Step 1 — Create a free Firebase project
1. Go to https://console.firebase.google.com and sign in with any
   Google account.
2. Click **Add project**, give it a name (e.g. `smishing-prototype`),
   and finish the setup wizard (you can skip Google Analytics).

### Step 2 — Enable the Realtime Database
1. In your new project's left sidebar, go to **Build → Realtime
   Database**.
2. Click **Create Database**, choose a location, and start in
   **test mode** (this allows the app to read/write without complex
   authentication — acceptable for this academic prototype since no
   real personal account data is stored, only SMS text samples).
3. Once created, copy the **Database URL** shown at the top — it looks
   like `https://smishing-prototype-default-rtdb.firebaseio.com`.

### Step 3 — Add the URL to Streamlit Cloud as a secret
1. Go to your app on https://share.streamlit.io, click the **⋮** menu
   → **Settings** → **Secrets**.
2. Add this line (with your real URL):
   ```
   FIREBASE_DB_URL = "https://smishing-prototype-default-rtdb.firebaseio.com"
   ```
3. Save. Streamlit Cloud will automatically restart your app with the
   secret available.

### Step 4 — (Local testing only, optional)
If you also want cloud logging while running locally, create a file
`.streamlit/secrets.toml` (do **not** commit this file to GitHub) with
the same line as above.

Once this is set up, every message any visitor checks is saved
permanently and shown to every other visitor in the "Shared Log of
Checked Messages" section at the bottom of the app — this is also what
powers the **known-phishing cache**: if someone checks a message that
was already reported as suspicious by anyone else, the app recognises
it instantly without needing to re-run the model.

---

## What changed to make this "professionally hosted"

- **Icons removed**: `.streamlit/config.toml` sets `toolbarMode =
  "minimal"`, which hides the Share, Star, GitHub, and "Edit on GitHub"
  icons Streamlit Cloud normally shows for apps linked to a public
  repo, plus the "Made with Streamlit" footer is hidden via `app.py`.
- **Permanent, shared log**: see the Firebase setup above — replaces
  the old per-session `log.csv`.
- **Known-phishing cache**: messages already confirmed suspicious by
  any user are instantly recognised on resubmission (`app.py`,
  `load_known_phishing_cache`), and the model/vectoriser are loaded
  once via `st.cache_resource` rather than on every click, for speed.
- **Already hosted and shareable**: the app is already live on
  Streamlit Community Cloud and reachable by anyone with the link —
  no one needs you personally online or running anything locally for
  others to use it.

## Growing this for your thesis

- **Add more data**: the more real/simulated SMS examples you add to
  `data/sms_dataset.csv`, the more reliable the classifier becomes.
- **Add more tactic keywords**: edit `TACTIC_KEYWORDS` in
  `tactic_rules.py` to catch more phrasing.
- **Re-train after every data change**: just re-run `train_model.py`,
  then re-upload `model.joblib` and `vectoriser.joblib` to GitHub.
- **For your Test phase**: have participants open the live link and
  paste in the prepared test messages; the shared log at the bottom of
  the app is your evidence trail for the evaluation sessions.
