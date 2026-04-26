import pandas as pd

# Load raw dataset (force read + skip bad lines)
df = pd.read_csv("../data/city_hour.csv", low_memory=False, on_bad_lines="skip")

print("Original shape:", df.shape)

# ---------------- CLEANING ----------------

# Clean column names
df.columns = df.columns.str.strip()

# Standardize City names
df["City"] = (
    df["City"]
    .astype(str)
    .str.strip()
    .str.title()
)

# Convert Datetime
df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")

# Convert numeric columns safely
cols = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]
for col in cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows with no city or time
df = df.dropna(subset=["City", "Datetime"])

# Fill missing pollution values (important!)
df[cols] = df[cols].fillna(method="ffill")

# Final cleanup
df = df.drop_duplicates()

print("Cleaned shape:", df.shape)
print("Cities:", df["City"].unique())

# ---------------- SAVE CLEAN DATA ----------------
df.to_csv("../data/clean_city_hour.csv", index=False)

print("✅ Clean dataset saved as clean_city_hour.csv")
import numpy as np

# Create fake stations based on city
def assign_station(city):
    if city == "Chennai":
        return np.random.choice(["Manali", "Velachery", "Arumbakkam"])
    elif city == "Coimbatore":
        return "Coimbatore_Center"
    elif city == "Madurai":
        return "Madurai_Main"
    elif city == "Tirupur":
        return "Tirupur_Industrial"
    elif city == "Thoothukudi":
        return "Thoothukudi_Port"
    elif city == "Salem":
        return "Salem_Town"
    elif city == "Vellore":
        return "Vellore_Center"
    else:
        return "Other"

df["Station"] = df["City"].apply(assign_station)
import numpy as np

# ---------------- ADD CHENNAI STATIONS ----------------

def assign_chennai_station(row):
    if row["City"] == "Chennai":
        return np.random.choice(["Manali", "Velachery", "Arumbakkam"])
    return None

df["Station"] = df.apply(assign_chennai_station, axis=1)

# Fill other cities with default station names
df["Station"] = df["Station"].fillna(df["City"] + "_Center")
df.to_csv("../data/Arumbakkam.csv", index=False)
df.to_csv("../data/Manali.csv", index=False)
df.to_csv("../data/Velachery.csv", index=False)




print("✅ Chennai station dataset created!")
print(df["Station"].unique())