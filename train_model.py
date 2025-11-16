import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from data_processing import load_data, make_train_test

TARGET_COL = "Risk_Level"

def train():
    df = load_data("Health_Risk_Dataset.csv")

    X_train, X_test, y_train, y_test = make_train_test(df, target=TARGET_COL)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, "risk_model.pkl")
    print("Model saved successfully as risk_model.pkl!")

if __name__ == "__main__":
    train()
