import streamlit as st
import pandas as pd
import joblib

# Load files
model = joblib.load("KNN_heart.pkl")
scaler = joblib.load("scaler.pkl")
expected_columns = joblib.load("columns.pkl")

# Title
st.title("❤️ Heart Disease Prediction System")
st.markdown("Enter patient details to predict heart disease risk.")

# Inputs
age = st.slider("Age", 18, 100, 40)

sex = st.selectbox("Sex", ["Male", "Female"])

chestpain = st.selectbox(
    "Chest Pain Type",
    ["ATA", "NAP", "TA", "ASY"]
)

resting_bp = st.slider(
    "Resting Blood Pressure",
    80, 200, 120
)

cholesterol = st.slider(
    "Cholesterol",
    100, 400, 200
)

fasting_bs = st.selectbox(
    "Fasting Blood Sugar > 120",
    [0, 1]
)

rest_ecg = st.selectbox(
    "Resting ECG",
    ["Normal", "ST", "LVH"]
)

max_hr = st.slider(
    "Maximum Heart Rate",
    60, 220, 150
)

exercise_angina = st.selectbox(
    "Exercise Angina",
    ["Y", "N"]
)

oldpeak = st.slider(
    "Oldpeak",
    0.0, 6.0, 1.0
)

slope = st.selectbox(
    "ST Slope",
    ["Up", "Flat", "Down"]
)

# Prediction button
if st.button("Predict"):

    # Input dictionary
    input_data = {
        'Age': age,
        'RestingBP': resting_bp,
        'Cholesterol': cholesterol,
        'FastingBS': fasting_bs,
        'MaxHR': max_hr,
        'Oldpeak': oldpeak,

        'Sex_M': 1 if sex == "Male" else 0,

        'ChestPainType_ATA': 1 if chestpain == "ATA" else 0,
        'ChestPainType_NAP': 1 if chestpain == "NAP" else 0,
        'ChestPainType_TA': 1 if chestpain == "TA" else 0,

        'RestingECG_Normal': 1 if rest_ecg == "Normal" else 0,
        'RestingECG_ST': 1 if rest_ecg == "ST" else 0,

        'ExerciseAngina_Y': 1 if exercise_angina == "Y" else 0,

        'ST_Slope_Flat': 1 if slope == "Flat" else 0,
        'ST_Slope_Up': 1 if slope == "Up" else 0,
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Ensure all columns exist
    input_df = input_df.reindex(columns=expected_columns, fill_value=0)

    # Scale data
    scaled_data = scaler.transform(input_df)

    # Prediction
    prediction = model.predict(scaled_data)[0]

    # Output
    if prediction == 1:
        st.error("⚠️ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")