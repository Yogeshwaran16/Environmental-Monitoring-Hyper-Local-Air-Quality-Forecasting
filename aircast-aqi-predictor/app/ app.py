import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("../src"))
from predict import predict_pm25

st.title("🌍 AirCast - AQI Predictor")

st.write("Predict PM2.5 and get health alerts")

temp = st.slider("Temperature (°C)", 10, 45, 25)
humidity = st.slider("Humidity (%)", 10, 100, 60)
wind = st.slider("Wind Speed (m/s)", 0, 10, 2)
hour = st.slider("Hour", 0, 23, 12)
day = st.slider("Day", 1, 31, 1)

if st.button("Predict"):
    pm25 = predict_pm25(temp, humidity, wind, hour, day)

    st.subheader(f"Predicted PM2.5: {pm25:.2f}")

    # Alert system
    if pm25 < 50:
        st.success("✅ Safe Air Quality")
    elif pm25 < 100:
        st.warning("⚠️ Moderate Air Quality")
    else:
        st.error("🚫 Unsafe Air Quality")
