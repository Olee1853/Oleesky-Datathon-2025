import streamlit as st
import pandas as pd
import joblib
import os
import base64

# Load model
MODEL_FILE = "risk_model.pkl"
if not os.path.exists(MODEL_FILE):
    st.error(f"Model '{MODEL_FILE}' not found. Run train_model.py first.")
    st.stop()
model = joblib.load(MODEL_FILE)

# Map categorical variables
consciousness_map = {"A": 0, "V": 1, "P": 2, "U": 3}

# Function to set background
def set_background_local(image_file):
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
        }}
        .form-container {{
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            margin-top: -40px;
        }}
        .section-header {{
            color: #023e8a;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .stButton>button {{
            background-color: #0077b6;
            color: white;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background_local("ocean.jpg")

st.markdown('<h1 style="color:#0077b6;text-align:center;">🏥 Health Risk Checker</h1>', unsafe_allow_html=True)

# Form container
st.markdown('<div class="form-container">', unsafe_allow_html=True)

with st.form("risk_form"):
    st.markdown('<div class="section-header">Patient Vitals</div>', unsafe_allow_html=True)
    
    respiratory_rate = st.number_input("Respiratory Rate", min_value=0.0, step=0.1)
    oxygen_saturation = st.number_input("Oxygen Saturation (%)", min_value=0.0, max_value=100.0, step=0.1)
    
    # Use select_slider instead of selectbox for fully white appearance
    o2_scale = st.select_slider("O2 Scale", options=[1,2], value=1)
    systolic_bp = st.number_input("Systolic BP", min_value=0.0, step=0.1)
    heart_rate = st.number_input("Heart Rate", min_value=0.0, step=0.1)
    temperature = st.number_input("Temperature (°C)", min_value=25.0, max_value=45.0, step=0.1)
    consciousness = st.select_slider("Consciousness", options=["A","V","P","U"], value="A")
    on_oxygen = st.select_slider("On Oxygen", options=[0,1], value=0)
    
    submitted = st.form_submit_button("Check Risk")

st.markdown('</div>', unsafe_allow_html=True)

# Prediction
if submitted:
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
