import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import joblib
import os

# Load data
df = pd.read_csv("Data/processed/final/clean_data.csv")

# Separate features and target
X = df.drop("depression", axis=1)
y = df["depression"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

os.makedirs("Data/processed/final", exist_ok=True)
X_test.to_csv("Data/processed/final/X_test.csv", index=False)
y_test.to_csv("Data/processed/final/y_test.csv", index=False)

# Impute CGPA
mean_cgpa = X_train["cgpa"].mean()
X_train["cgpa"] = X_train["cgpa"].fillna(mean_cgpa)
X_test["cgpa"] = X_test["cgpa"].fillna(mean_cgpa)

# Encode categorical variables
categorical_columns = [
    "gender",
    "dietary_habits",
    "family_history_of_mental_illness",
    "have_you_ever_had_suicidal_thoughts",
]

label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    X_train[col + "_encoded"] = le.fit_transform(X_train[col])
    X_test[col + "_encoded"] = le.transform(X_test[col])
    label_encoders[col] = le

X_train.drop(columns=categorical_columns, inplace=True)
X_test.drop(columns=categorical_columns, inplace=True)

# Save preprocessing artifacts
os.makedirs("models/final/artifacts", exist_ok=True)
joblib.dump(mean_cgpa, "models/final/artifacts/mean_cgpa.pkl")

final_features = X_train.columns.tolist()
joblib.dump(final_features, "models/final/artifacts/final_features.pkl")

# Define model parameters
phase2_params = {
    "objective": "binary:logistic",
    "eval_metric": ["auc", "logloss"],
    "random_state": 42,
    "max_depth": 3,
    "min_child_weight": 10,
    "max_delta_step": 3,
    "learning_rate": 0.05,
    "n_estimators": 200,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0,
    "gamma": 0.5
}

# Train and save balanced model
phase2_model = XGBClassifier(**phase2_params)
phase2_model.fit(X_train, y_train)
joblib.dump(phase2_model, "models/final/model_balanced.pkl")

# Define high-recall parameters
phase3_params = {
    **phase2_params,
    "subsample": 0.9,
    "colsample_bytree": 0.6,
    "scale_pos_weight": 3.0,
}

# Train and save high-recall model
phase3_model = XGBClassifier(**phase3_params)
phase3_model.fit(X_train, y_train)
joblib.dump(phase3_model, "models/final/model_highrecall.pkl")

# Save encoders
os.makedirs("models/final/encoders", exist_ok=True)
for col, le in label_encoders.items():
    joblib.dump(le, f"models/final/encoders/{col}_encoder.pkl")