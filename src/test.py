# =====================================
# test.py
# =====================================

import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_auc_score, confusion_matrix

# -------------------------------
# Load saved test set
# -------------------------------
X_test = pd.read_csv("Data/processed/final/X_test.csv")
y_test = pd.read_csv("Data/processed/final/y_test.csv")

# -------------------------------
# Load LabelEncoders and transform categorical columns
# -------------------------------
categorical_columns = [
    "gender",
    "dietary_habits",
    "family_history_of_mental_illness",
    "have_you_ever_had_suicidal_thoughts",
]

for col in categorical_columns:
    le = joblib.load(f"models/Final/encoders/{col}_encoder.pkl")
    X_test[col + "_encoded"] = le.transform(X_test[col])

X_test.drop(columns=categorical_columns, inplace=True)

# -------------------------------
# Function to evaluate model
# -------------------------------
def evaluate_model(y_true, y_pred, y_proba=None):
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred),
    }
    if y_proba is not None:
        metrics["roc_auc"] = roc_auc_score(y_true, y_proba)
    return metrics

# -------------------------------
# Evaluate saved models
# -------------------------------
model_files = {
    "Phase 2 - Balanced": "models/Final/model_balanced.pkl",
    "Phase 3 - High Recall": "models/Final/model_highrecall.pkl",
}

for name, path in model_files.items():
    model = joblib.load(path)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
    metrics = evaluate_model(y_test, y_pred, y_proba)

    print(f"\n📊 {name} Performance:")
    for metric_name, value in metrics.items():
        print(f"  {metric_name}: {value:.4f}")
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"  Confusion Matrix:\n{cm}")
