# Phishing Link Classifier

Detecting phishing URLs with classic ML models currently trained on the [PhiUSIIL phishing URL dataset](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset).

## Limitations

The current models are not suitable for real world usage.

- Links using HTTP are automatically labeled phishing.
- Links with path are automatically labeled phishing.
- Plain URLs like `https://google.com` get flagged because `dot_count < 2`.
- The feature set is intentionally small (9 lexical features) and does not look at page content, WHOIS, DNS, or reputation signals.

I documented these more in ("/notebook/phishing-link-classifier.ipynb")["/notebook/phishing-link-classifier.ipynb"]

## Project layout

- `src/features.py` — extracts URL features (HTTPS, IP host, host length, digit/dot/hyphen counts, path depth, query presence, Shannon entropy).
- `src/predict.py` — CLI that loads the trained models and classifies a single URL.
- `notebook/phishing-link-classifier.ipynb` — full training and evaluation walkthrough.
- `models/` — pickled trained models (`model_tree.pkl`, `model_forest.pkl`, `model_gb.pkl`).

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install pandas scikit-learn ucimlrepo joblib seaborn matplotlib
```

## Usage

Classify a URL from the command line:

```bash
python src/predict.py "https://example.com/login"
```

Each model prints its prediction (`BENIGN` / `PHISHING`) and confidence.

To retrain, run the notebook end-to-end.
