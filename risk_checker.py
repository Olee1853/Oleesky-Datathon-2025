import joblib

# Simple numeric input (no bounds)
def get_number(prompt, integer=False):
    while True:
        try:
            value = float(input(prompt))
            if integer:
                value = int(value)
            return value
        except ValueError:
            print("❌ Error: Please enter a valid number.\n")

# For inputs with fixed allowed values
def get_choice(prompt, choices):
    choices_display = "/".join(choices)
    while True:
        value = input(f"{prompt} ({choices_display}): ").strip().upper()
        if value not in choices:
            print(f"❌ Error: Must be one of: {choices_display}. Please try again.\n")
        else:
            return value


def main():
    model = joblib.load("risk_model.pkl")

    print("\n--- Patient Risk Checker ---\n")

    # No bounds on these:
    Respiratory_Rate = get_number("Enter Respiratory Rate: ")
    Oxygen_Saturation = get_number("Enter Oxygen Saturation %: ")
    Systolic_BP = get_number("Enter Systolic Blood Pressure: ")
    Heart_Rate = get_number("Enter Heart Rate: ")
    Temperature = get_number("Enter Temperature (°F): ")

    # ONLY THESE HAVE BOUNDS:

    # O2 Scale must be 1 or 2
    O2_Scale = get_choice("Enter O2 Scale", ["1", "2"])
    O2_Scale = int(O2_Scale)

    # Consciousness must be A, V, P, or U
    Consciousness = get_choice("Enter Consciousness", ["A", "V", "P", "U"])

    # On Oxygen must be 0 or 1
    On_Oxygen = get_choice("Is the patient on oxygen?", ["0", "1"])
    On_Oxygen = int(On_Oxygen)

    # Encode consciousness
    consciousness_map = {"A": 0, "V": 1, "P": 2, "U": 3}
    Consciousness_Code = consciousness_map[Consciousness]

    # Prepare input
    X = [[
        Respiratory_Rate,
        Oxygen_Saturation,
        O2_Scale,
        Systolic_BP,
        Heart_Rate,
        Temperature,
        Consciousness_Code,
        On_Oxygen
    ]]

    predicted_risk = model.predict(X)[0]

    print("\n--- Prediction Complete ---")
    print(f"Predicted Risk Level: {predicted_risk}\n")


if __name__ == "__main__":
    main()
