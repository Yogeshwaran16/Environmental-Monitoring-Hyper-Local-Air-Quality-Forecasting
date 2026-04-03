# Environmental-Monitoring-Hyper-Local-Air-Quality-Forecasting
Predict street-level air quality 6-24 hours ahead in Tamil Nadu's industrial corridors by fusing TNPCB CAAQMS data with weather, traffic, and industrial activity signals.

# 🌍 AirCast - PM2.5 Prediction System

## 📌 Overview
AirCast predicts PM2.5 levels using weather data and provides health alerts.

## 🚀 Features
- PM2.5 prediction using ML
- Health risk classification
- Interactive UI using Streamlit

## 🧠 Model
- Random Forest Regressor

## ▶️ Run Project

### Install dependencies
pip install -r requirements.txt

### Train model
cd src
python train_model.py

### Run app
cd ../app
streamlit run app.py

## 📊 Future Improvements
- Add real-time data
- Map visualization
- LSTM model
