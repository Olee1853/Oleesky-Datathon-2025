# app.py

import streamlit as st
import pandas as pd
import joblib
import os

# === Load trained model safely ===
MODEL_FILE = os.path.join(os.path.dirname(__file__), "risk_model.pkl")

if not os.path.exists(MODEL_FILE):
    st.error(f"Model file '{MODEL_FILE}' not found. Run train_model.py first.")
    st.stop()

model = joblib.load(MODEL_FILE)

# === Mapping for categorical variables ===
consciousness_map = {"A": 0, "V": 1, "P": 2, "U": 3}

# === CSS for hospital theme ===
st.markdown(
    """
    <style>
    body {
        background-color: #f0f4f8;
    }
    .stApp {
        font-family: "Arial", sans-serif;
        color: #0c3c60;
    }
    .title {
        color: #0077b6;
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        padding-bottom: 20px;
    }
    .section-header {
        color: #023e8a;
        font-size: 24px;
        font-weight: bold;
        padding-top: 15px;
    }
    .stButton>button {
        background-color: #0077b6;
        color: white;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# === Title ===
st.markdown('<div class="title">🏥 Hospital Health Risk Checker</div>', unsafe_allow_html=True)

# === Input Form ===
with st.form("risk_form"):
    st.markdown('<div class="section-header">Patient Vitals</div>', unsafe_allow_html=True)
    
    respiratory_rate = st.number_input("Respiratory Rate", min_value=0.0, step=0.1)
    oxygen_saturation = st.number_input("Oxygen Saturation (%)", min_value=0.0, max_value=100.0, step=0.1)
    o2_scale = st.selectbox("O2 Scale", options=[1, 2])
    systolic_bp = st.number_input("Systolic BP", min_value=0.0, step=0.1)
    heart_rate = st.number_input("Heart Rate", min_value=0.0, step=0.1)
    temperature = st.number_input("Temperature (°C)", min_value=25.0, max_value=45.0, step=0.1)
    consciousness = st.selectbox("Consciousness", options=["A", "V", "P", "U"])
    on_oxygen = st.selectbox("On Oxygen", options=[0, 1])
    
    submitted = st.form_submit_button("Check Risk")

# === Prediction ===
if submitted:
    # Encode categorical inputs
    consciousness_encoded = consciousness_map[consciousness]
    
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
    
    risk_prediction = model.predict(input_data)[0]
    
    st.markdown('<div class="section-header">Predicted Risk Level</div>', unsafe_allow_html=True)
    
    if risk_prediction.lower() == "high":
        st.error(f"⚠️ {risk_prediction}")
    elif risk_prediction.lower() == "medium":
        st.warning(f"⚠️ {risk_prediction}")
    else:
        st.success(f"✅ {risk_prediction}")
