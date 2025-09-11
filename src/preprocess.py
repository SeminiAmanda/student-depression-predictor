# =====================================
# preprocess.py
# =====================================

# Load libraries
import pandas as pd
import numpy as np
import os

# Load the dataset
df = pd.read_csv("./Data/raw/student_depression_dataset.csv")

# Clean column names
df.columns = [col.strip().lower().replace(" ", "_").replace("/", "_").replace("?", "").rstrip("_") for col in df.columns]

# =====================================
# Drop unnecessary columns
# =====================================
df.drop(['id', 'work_pressure', 'job_satisfaction', 'profession', 'city'], axis=1, inplace=True)

# =====================================
# Column Type Categorization
# =====================================
num_cols = ['age', 'academic_pressure', 'cgpa', 'financial_stress',
            'study_satisfaction', 'work_study_hours']

nominal_cat_cols = ['gender', 'dietary_habits',
                    'have_you_ever_had_suicidal_thoughts',
                    'family_history_of_mental_illness']

ordinal_cols = ['degree', 'sleep_duration']

# Convert nominal categorical columns to 'category' dtype
for col in nominal_cat_cols:
    df[col] = df[col].astype('category')

# =====================================
# Handle missing or invalid values
# =====================================
# Convert to object before replacing to avoid FutureWarning
df['sleep_duration'] = df['sleep_duration'].astype(object).replace('Others', np.nan)
df['dietary_habits'] = df['dietary_habits'].astype(object).replace('Others', np.nan)
df['financial_stress'] = pd.to_numeric(df['financial_stress'].replace('?', np.nan), errors='coerce')

# Drop rows with any remaining missing values
df_cleaned = df.dropna().copy()  # copy to avoid SettingWithCopyWarning

# =====================================
# Ordinal Categorical Encoding
# =====================================
# Encode 'degree'
df_cleaned.loc[:, 'degree'] = df_cleaned['degree'].str.strip().str.strip("'\"")
degree_encoding = {
    'Others': 0,
    'Class 12': 1,
    'B.Com': 2, 'BBA': 2, 'BA': 2, 'BSc': 2, 'BCA': 2, 'B.Pharm': 2,
    'BE': 2, 'B.Tech': 2, 'B.Arch': 2, 'BHM': 2, 'LLB': 2, 'MBBS': 2, 'B.Ed': 2,
    'MHM': 3, 'MSc': 3, 'MA': 3, 'M.Ed': 3, 'M.Com': 3, 'MCA': 3,
    'M.Tech': 3, 'M.Pharm': 3, 'ME': 3, 'MD': 3, 'MBA': 3, 'LLM': 3,
    'PhD': 4
}
df_cleaned.loc[:, 'degree_encoded'] = df_cleaned['degree'].map(degree_encoding)

# Encode 'sleep_duration'
df_cleaned.loc[:, 'sleep_duration'] = df_cleaned['sleep_duration'].str.strip().str.strip("'\"")
sleep_duration_encoding = {
    'Less than 5 hours': 0,
    '5-6 hours': 1,
    '7-8 hours': 2,
    'More than 8 hours': 3
}
df_cleaned.loc[:, 'sleep_duration_encoded'] = df_cleaned['sleep_duration'].map(sleep_duration_encoding)

# Drop original ordinal columns
df_encoded = df_cleaned.drop(['degree', 'sleep_duration'], axis=1).copy()

# Add encoded columns to numerical features
num_cols.extend(['degree_encoded', 'sleep_duration_encoded'])

# =====================================
# CGPA Conversion
# =====================================
# Convert CGPA from 0–10 scale to 0–4 scale
df_encoded.loc[:, 'cgpa'] = df_encoded['cgpa'] * (4 / 10)
df_encoded.loc[:, 'cgpa'] = df_encoded['cgpa'].round(2)

# Replace 0 with NaN to mark as missing
# 🧠 Imputation of missing CGPA values will be done after splitting to avoid data leakage
df_encoded.loc[:, 'cgpa'] = df_encoded['cgpa'].replace(0, np.nan)

# =====================================
# Save cleaned data
# =====================================
output_dir = "Data/processed/final"
os.makedirs(output_dir, exist_ok=True)
df_encoded.to_csv(f"{output_dir}/clean_data.csv", index=False)

print(f"\n🍀 Cleaned data saved as {output_dir}/clean_data.csv")
print("Data shape:", df_encoded.shape)
