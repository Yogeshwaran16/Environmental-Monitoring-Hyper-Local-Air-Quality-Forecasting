import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

st.title("🌫️ Air Quality Dashboard")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("../data/final_combined_data.csv")

# Clean columns
df.columns = df.columns.str.strip()

# Rename columns (important)
df = df.rename(columns={
    "PM2.5 (µg/m³)": "PM2.5",
    "PM10 (µg/m³)": "PM10",
    "NO2 (µg/m³)": "NO2",
    "SO2 (µg/m³)": "SO2",
    "CO (mg/m³)": "CO",
    "Ozone (µg/m³)": "O3"
})

# Convert datetime
df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")

# Clean text
df["City"] = df["City"].astype(str).str.strip()
df["Station"] = df["Station"].astype(str).str.strip()

# ---------------- LOAD MODEL ----------------
model = joblib.load("../models/model.pkl")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

city = st.sidebar.selectbox(
    "Select City",
    sorted(df["City"].dropna().unique())
)

stations = df[df["City"] == city]["Station"].dropna().unique()

station = st.sidebar.selectbox(
    "Select Station",
    sorted(stations)
)

filtered_df = df[
    (df["City"] == city) &
    (df["Station"] == station)
]

# ---------------- AQI CATEGORY ----------------
def get_aqi_category(pm25):
    if pm25 <= 30:
        return "🟢 Good"
    elif pm25 <= 60:
        return "🟡 Satisfactory"
    elif pm25 <= 90:
        return "🟠 Moderate"
    elif pm25 <= 120:
        return "🔴 Poor"
    elif pm25 <= 250:
        return "🟣 Very Poor"
    else:
        return "⚫ Severe"

# ---------------- PREDICTION ----------------
st.subheader("🔮 Air Quality Prediction")

if not filtered_df.empty:
    try:
        latest = filtered_df.sort_values("Datetime").iloc[-1]

        features = {
            "PM10": latest["PM10"],
            "NO2": latest["NO2"],
            "CO": latest["CO"],
            "SO2": latest["SO2"],
            "O3": latest["O3"],
            "hour": latest["Datetime"].hour,
            "day": latest["Datetime"].day,
            "month": latest["Datetime"].month,
        }

        X = pd.DataFrame([features])

        pred = model.predict(X)[0]

        category = get_aqi_category(pred)

        st.metric("Predicted PM2.5", f"{pred:.2f} µg/m³")

        if pred <= 30:
            st.success(category)
        elif pred <= 90:
            st.warning(category)
        else:
            st.error(category)

    except Exception as e:
        st.error(f"Prediction error: {e}")
else:
    st.warning("No data available")

# ---------------- MAP ----------------
st.subheader("🗺️ Station Location")

station_coords = {
    "Manali": [13.1665, 80.2660],
    "Velachery": [12.9750, 80.2200],
    "Arumbakkam": [13.0700, 80.2100]
}

coords = station_coords.get(station)

if coords:
    map_df = pd.DataFrame({"lat": [coords[0]], "lon": [coords[1]]})
    st.map(map_df)
else:
    st.warning("No location data for this station")