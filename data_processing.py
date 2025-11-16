import pandas as pd
from sklearn.model_selection import train_test_split

def load_data(path):
    return pd.read_csv(path)

def make_train_test(df, target_col="Risk_Level", test_size=0.2, random_state=42):
    X = df.drop(columns=[target_col, "Patient_ID"])
    y = df[target_col]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)