import streamlit as st
import pandas as pd
import joblib
import os
import base64

# === Load model safely ===
MODEL_FILE = os.path.join(os.path.dirname(__file__), "risk_model.pkl")
if not os.path.exists(MODEL_FILE):
    st.error(f"Model file '{MODEL_FILE}' not found. Run train_model.py first.")
    st.stop()

model = joblib.load(MODEL_FILE)

# === Mapping categorical variables ===
consciousness_map = {"A": 0, "V": 1, "P": 2, "U": 3}

# === Set local image as background ===
def set_background_local(image_file):
    """Set a local image as Streamlit background using base64."""
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            backdrop-filter: blur(5px);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use ocean.jpg as background
set_background_local("ocean.jpg")

# === Title ===
st.markdown('<h1 style="color:#0077b6;text-align:center;">🏥 Health Risk Checker</h1>', unsafe_allow_html=True)

# === Input Form ===
with st.form("risk_form"):
    respiratory_rate = st.number_input("Respiratory Rate", min_value=0.0, step=0.1)
    oxygen_saturation = st.number_input("Oxygen Saturation (%)", min_value=0.0, max_value=100.0, step=0.1)
    o2_scale = st.selectbox("O2 Scale", options=[1, 2])
    systolic_bp = st.number_input("Systolic BP", min_value=0.0, step=0.1)
    heart_rate = st.number_input("Heart Rate", min_value=0.0, step=0.1)
    temperature = st.number_input("Temperature (°C)", min_value=25.0, max_value=45.0, step=0.1)
    consciousness = st.selectbox("Consciousness", options=["A", "V", "P", "U"])
    o
