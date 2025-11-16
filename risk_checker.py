# risk_checker.py

import joblib
import pandas as pd
import os

MODEL_FILE = "risk_model.pkl"

# === Load trained model safely ===
if not os.path.exists(MODEL_FILE):
    print(f"Error: Model file '{MODEL_FILE}' not found. Run train_model.py first.")
    exit(1)

model = joblib.load(MODEL_FILE)

# === Mapping for categorical variables ===
consciousness_map = {"A": 0, "V": 1, "P": 2, "U": 3}

# === Helper function for validated input ===
def get_input(prompt, valid_values=None, val_type=float):
    while True:
        val = input(prompt)
        try:
            val_casted = val_type(val)
            if valid_values is not None and val_casted not in valid_values:
                print(f"Invalid input! Must be one of {valid_values}.")
            else:
                return val_casted
        except ValueError:
            print(f"Invalid input! Must be of type {val_type.__name__}.")

# === Main function ===
def main():
    print("=== HealthSense ===")
    
    # Numeric vitals
    respiratory_rate = get_input("Respiratory Rate: ", val_type=float)
    oxygen_saturation = get_input("Oxygen Saturation: ", val_type=float)
    o2_scale = get_input("O2 Scale (1 or 2): ", valid_values=[1, 2], val_type=int)
    systolic_bp = get_input("Systolic BP: ", val_type=float)
    heart_rate = get_input("Heart Rate: ", val_type=float)
    temperature = get_input("Temperature: ", val_type=float)
    
    # Categorical vitals
    while True:
        consciousness = input("Consciousness (A, V, P, U): ").upper()
        if consciousness in consciousness_map:
            consciousness_encoded = consciousness_map[consciousness]
            break
        else:
            print("Invalid input! Must be one of A, V, P, U.")
    
    on_oxygen = get_input("On Oxygen (0 = No, 1 = Yes): ", valid_values=[0, 1], val_type=int)
    
    # Prepare DataFrame for prediction
    input_data = pd.DataFrame([{
        "Respiratory_Rate": respiratory_rate,
        "Oxygen_Saturation": oxygen_saturation,
        "O2_Scale": o2_scale,
        "Systolic_BP": systolic_bp,
        "Heart_Rate": heart_rate,
        "Temperature": temperature,
        "Consciousness": consciousness_encoded,
        "On_Oxygen": on_oxygen
    }])
    
    # Predict risk level
    risk_prediction = model.predict(input_data)[0]
    
    print(f"\nPredicted Risk Level: {risk_prediction}")

if __name__ == "__main__":
    main()
