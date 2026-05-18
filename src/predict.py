import joblib
import sys
from pathlib import Path
import pandas as pd
from features import extract_features

_models_dir = Path(__file__).parent.parent / "models"
models = {
    "Random Forest": joblib.load(_models_dir / "PhiUSIIL_model_forest.pkl"),
    "Gradient Boosting": joblib.load(_models_dir / "PhiUSIIL_model_gb.pkl"),
    "Decision Tree": joblib.load(_models_dir / "PhiUSIIL_model_tree.pkl"),
}

url = sys.argv[1]
features = pd.DataFrame([extract_features(url)])

for name, model in models.items():
    result = model.predict(features)[0]
    prob = model.predict_proba(features)[0]
    label = "BENIGN" if result == 1 else "PHISHING"
    print(f"{name}: {label} (confidence: {max(prob):.1%})")