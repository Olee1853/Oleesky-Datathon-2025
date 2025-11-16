# train_model.py

import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# === Configuration ===
DATA_FILE = "Health_Risk_Dataset.csv"
TARGET_COL = "Risk_Level"

# Save model in the same folder as this script
MODEL_FILE = os.path.join(os.path.dirname(__file__), "risk_model.pkl")

# === Load and preprocess data ===
def load_data():
    df = pd.read_csv(DATA_FILE)
    
    # Drop Patient_ID
    if "Patient_ID" in df.columns:
        df = df.drop(columns=["Patient_ID"])
    
    # Encode categorical columns
    consciousness_map = {"A": 0, "V": 1, "P": 2, "U": 3}
    df['Consciousness'] = df['Consciousness'].map(consciousness_map)
    
    # Ensure On_Oxygen and O2_Scale are numeric
    df['On_Oxygen'] = df['On_Oxygen'].astype(int)
    df['O2_Scale'] = df['O2_Scale'].astype(int)
    
    return df

# === Split into train/test sets ===
def make_train_test(df, target_col):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    return X_train, X_test, y_train, y_test

# === Train the model ===
def train():
    df = load_data()
    X_train, X_test, y_train, y_test = make_train_test(df, target_col=TARGET_COL)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate accuracy
    acc = model.score(X_test, y_test)
    print(f"Model trained! Test accuracy: {acc:.2f}")
    
    # Save model
    joblib.dump(model, MODEL_FILE)
    print(f"Model saved to {MODEL_FILE}")

# === Run training ===
if __name__ == "__main__":
    train()
