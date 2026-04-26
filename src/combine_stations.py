import pandas as pd
import os

data_path = "../data/"

files = [
    "Manali.csv",
    "Velachery.csv",
    "Arumbakkam.csv"
]

dfs = []

for file in files:
    df = pd.read_csv(os.path.join(data_path, file), low_memory=False)

    # Clean column names
    df.columns = df.columns.str.strip()

    # Add Station column
    station_name = file.replace(".csv", "")
    df["Station"] = station_name

    # ✅ FIX: Ensure City column exists
    if "City" not in df.columns:
        df["City"] = "Chennai"

    dfs.append(df)

# Combine
df = pd.concat(dfs, ignore_index=True)

print("Combined shape:", df.shape)
print("Columns:", df.columns)

# ---------------- CLEANING ----------------

df["City"] = df["City"].astype(str).str.strip().str.title()

# Convert Datetime safely
if "Datetime" in df.columns:
    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")

# Convert numeric columns
cols = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]
for col in cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop invalid rows
df = df.dropna(subset=["Datetime"])

# Fill missing values
available_cols = [col for col in cols if col in df.columns]
df[available_cols] = df[available_cols].ffill()

# Remove duplicates
df = df.drop_duplicates()

# ---------------- SAVE ----------------

df.to_csv("../data/final_station_data.csv", index=False)

print("✅ Final dataset created!")
print("Stations:", df["Station"].unique())