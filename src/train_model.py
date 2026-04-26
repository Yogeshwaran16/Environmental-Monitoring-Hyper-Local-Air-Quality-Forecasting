import streamlit as st
import pandas as pd
import joblib
import pydeck as pdk

st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

st.title("🌫️ Hyperlocal Air Quality Dashboard")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("../data/final_combined_data.csv")
    df.columns = df.columns.str.strip()

    # Rename columns
    rename_map = {
        "PM2.5 (µg/m³)": "PM2.5",
        "PM10 (µg/m³)": "PM10",
        "NO2 (µg/m³)": "NO2",
        "SO2 (µg/m³)": "SO2",
        "CO (mg/m³)": "CO",
        "Ozone (µg/m³)": "O3"
    }
    df = df.rename(columns=rename_map)

    # Datetime
    if "Datetime" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")

    return df

df = load_data()

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load("../models/model.pkl")

model = load_model()

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

city = st.sidebar.selectbox("Select City", sorted(df["City"].dropna().unique()))

stations = df[df["City"] == city]["Station"].dropna().unique()
station = st.sidebar.selectbox("Select Station", sorted(stations))

filtered_df = df[(df["City"] == city) & (df["Station"] == station)]

# ---------------- SORT ----------------
filtered_df = filtered_df.sort_values("Datetime")

# ---------------- GRAPH ----------------
st.subheader("📈 PM2.5 Trend")

if "PM2.5" in filtered_df.columns:
    chart_df = filtered_df.set_index("Datetime")[["PM2.5"]].tail(100)
    st.line_chart(chart_df)
else:
    st.warning("PM2.5 data not available")

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

try:
    latest = filtered_df.iloc[-1]

    features = {
        "PM10": latest.get("PM10", 0),
        "NO2": latest.get("NO2", 0),
        "CO": latest.get("CO", 0),
        "SO2": latest.get("SO2", 0),
        "O3": latest.get("O3", 0),
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

# ---------------- MAP COORDINATES ----------------
station_coords = {
    "Manali": [13.1665, 80.2660],
    "Velachery": [12.9750, 80.2200],
    "Arumbakkam": [13.0700, 80.2100],
    "Chennai_Center": [13.0827, 80.2707],
    "Coimbatore_Center": [11.0168, 76.9558],
    "Madurai_Main": [9.9252, 78.1198],
    "Tirupur_Industrial": [11.1085, 77.3411],
    "Thoothukudi_Port": [8.7642, 78.1348],
    "Salem_Town": [11.6643, 78.1460],
    "Vellore_Center": [12.9165, 79.1325]
}

df["lat"] = df["Station"].map(lambda x: station_coords.get(x, [None, None])[0])
df["lon"] = df["Station"].map(lambda x: station_coords.get(x, [None, None])[1])

# ---------------- MAP DATA ----------------
map_df = df.dropna(subset=["lat", "lon"]).copy()
map_df = map_df.sort_values("Datetime").groupby("Station").tail(1)

# ---------------- MAP ----------------
st.subheader("🗺️ Live Pollution Map")

if not map_df.empty:

    map_df["pm25"] = map_df["PM2.5"].fillna(0)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position='[lon, lat]',
        get_color='[pm25 * 2, 100, 255 - pm25]',
        get_radius=5000,
    )

    view_state = pdk.ViewState(
        latitude=13.0827,
        longitude=80.2707,
        zoom=6,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
    ))

else:
    st.warning("No map data available")