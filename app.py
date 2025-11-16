import streamlit as st
import joblib

st.set_page_config(
    page_title="Patient Risk Classifier",
    page_icon="🩺",
    layout="centered"
)

# Load model
model = joblib.load("risk_model.pkl")

# ====== CSS for hospital theme ======
hospital_css = """
<style>
body {
    background-color: #f2f8ff;
}
.main > div {
    background: #ffffff;
    padding: 25px 40px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
h1 {
    color: #004d99 !important;
    font-weight: 700 !important;
}
label {
    font-size: 17px !important;
    font-weight: 600 !important;
}
.stButton>button {
    background-color: #0077cc;
    color: white;
    border-radius: 8px;
    padding: 10px 22px;
    font-size: 17px;
}
.stButton>button:hover {
    background-color: #005fa3;
}
.result-box {
    padding: 20px;
    border-radius: 12px;
    font-size: 22px;
    font-weight: bold;
    text-align: center;
}
.low { background-color: #cfffd0; color: #006600; }
.med { background-color: #fff7c4; color: #806600; }
.high { background-color: #ffd0d0; color: #800000; }
</style>
"""

st.markdown(hospital_css, unsafe_allow_html=True)

# Title
st.title("🩺 Patient Risk Classification")
st.write("Enter the patient's vital signs to estimate clinical risk level.")

# ===== Input fields =====
Respiratory_Rate = st.number_input("Respiratory Rate", step=1.0)
Oxygen_Saturation = st.number_input("Oxygen Saturation (%)", step=1.0)
Systolic_BP = st.number_input("Systolic Blood Pressure", step=1.0)
Heart_Rate = st.number_input("Heart Rate", step=1.0)
Temperature = st.number_input("Temperature (°F)", step=0.1)

O2_Scale = st.selectbox("O2 Scale", [1, 2])
Consciousness = st.selectbox("Consciousness (AVPU scale)", ["A", "V", "P", "U"])
On_Oxygen = st.selectbox("On Oxygen?", [0, 1])

# Encode consciousness
consciousness_map = {"A": 0, "V": 1, "P": 2, "U": 3}
Consciousness_Code = consciousness_map[Consciousness]

# ===== Prediction =====
if st.button("Predict Risk Level"):
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

    risk = model.predict(X)[0]

    st.subheader("Predicted Risk Level")

    if risk == 0:
        st.markdown('<div class="result-box low">🟢 LOW RISK</div>', unsafe_allow_html=True)
    elif risk == 1:
        st.markdown('<div class="result-box med">🟡 MEDIUM RISK</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-box high">🔴 HIGH RISK</div>', unsafe_allow_html=True)
