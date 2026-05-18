import joblib
import sys
from pathlib import Path
import pandas as pd
from features import extract_features

_models_dir = Path(__file__).parent.parent / "models"

_MODEL_SETS = {
    "PhiUSIIL": {
        "Random Forest": "PhiUSIIL_model_forest.pkl",
        "Gradient Boosting": "PhiUSIIL_model_gb.pkl",
        "Decision Tree": "PhiUSIIL_model_tree.pkl",
    },
    "URL-Phish": {
        "Random Forest": "URL-Phish_model_forest.pkl",
        #"Gradient Boosting": "URL-Phish_model_gb.pkl",
        #"Decision Tree": "URL-Phish_model_tree.pkl",
    },
}

if len(sys.argv) < 2:
    print(f"Usage: python predict.py <url> [{'|'.join(_MODEL_SETS)}]")
    sys.exit(1)

url = sys.argv[1]
model_set = sys.argv[2] if len(sys.argv) > 2 else "URL-Phish"
if model_set not in _MODEL_SETS:
    print(f"Unknown model set '{model_set}'. Choose from: {', '.join(_MODEL_SETS)}")
    sys.exit(1)

models = {name: joblib.load(_models_dir / fname) for name, fname in _MODEL_SETS[model_set].items()}

features_df = pd.DataFrame([extract_features(url)])
if "tld" in features_df.columns:
    features_df = pd.get_dummies(features_df, columns=["tld"])

print(f"Using model: {model_set}")
for name, model in models.items():
    X = features_df
    expected = getattr(model, "feature_names_in_", None)
    if expected is not None:
        X = X.reindex(columns=expected, fill_value=0)
    result = model.predict(X)[0]
    prob = model.predict_proba(X)[0]
    label = "BENIGN" if result == 1 else "PHISHING"
    print(f"{label} (confidence: {max(prob):.1%})")
