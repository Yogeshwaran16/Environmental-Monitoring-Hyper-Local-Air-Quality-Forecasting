import pandas as pd
import os

# ---------------- SETTINGS ----------------
data_folder = "../data"

files = [
    "City_wise_raw_data_1Day_2024_Vellore_1Day.csv",
    "City_wise_raw_data_1Day_2024_Salem_1Day.csv",
    "City_wise_raw_data_1Day_2024_Thoothukudi_1Day.csv",
    "City_wise_raw_data_1Day_2024_Chennai_1Day.csv",
    "City_wise_raw_data_1Day_2024_Tirupur_1Day.csv",
    "City_wise_raw_data_1Day_2024_Madurai_1Day.csv",
    "City_wise_raw_data_1Day_2024_Coimbatore_1Day.csv",
    "Raw_data_1Day_2025_site_288_Velachery_Res._Area_Chennai_CPCB_1Day.csv",
    "Raw_data_1Day_2025_site_5092_Manali_Village_Chennai_TNPCB_1Day.csv",
    "Raw_data_1Day_2025_site_5361_Arumbakkam_Chennai_TNPCB_1Day.csv"
]

dfs = []

# ---------------- READ FILES ----------------
for file in files:
    path = os.path.join(data_folder, file)
    print("Reading:", file)

    try:
        df = pd.read_csv(path, low_memory=False)

        # Clean column names
        df.columns = df.columns.str.strip()

        # ----------- FIX DATETIME COLUMN -----------
        possible_datetime_cols = ["Datetime", "Date", "date", "Timestamp", "From Date", "To Date"]

        found = None
        for col in possible_datetime_cols:
            if col in df.columns:
                found = col
                break

        if found:
            df.rename(columns={found: "Datetime"}, inplace=True)
            df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
        else:
            print("⚠️ No datetime column in:", file)

        # ----------- CITY -----------
        if "Chennai" in file:
            city_name = "Chennai"
        elif "Coimbatore" in file:
            city_name = "Coimbatore"
        elif "Madurai" in file:
            city_name = "Madurai"
        elif "Tirupur" in file:
            city_name = "Tirupur"
        elif "Thoothukudi" in file:
            city_name = "Thoothukudi"
        elif "Salem" in file:
            city_name = "Salem"
        elif "Vellore" in file:
            city_name = "Vellore"
        else:
            city_name = "Other"

        df["City"] = city_name

        # ----------- STATION -----------
        if "Velachery" in file:
            df["Station"] = "Velachery"
        elif "Manali" in file:
            df["Station"] = "Manali"
        elif "Arumbakkam" in file:
            df["Station"] = "Arumbakkam"
        else:
            df["Station"] = city_name + "_Center"

        # ----------- NUMERIC CLEANING -----------
        cols = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # Keep only valid rows
        if "Datetime" in df.columns:
            df = df.dropna(subset=["Datetime"])

        df = df.drop_duplicates()

        if not df.empty:
            dfs.append(df)
        else:
            print("⚠️ Empty file:", file)

    except Exception as e:
        print("❌ Error reading:", file)
        print(e)

# ---------------- COMBINE ----------------
if len(dfs) == 0:
    print("❌ No valid data loaded. Check files.")
    exit()

combined_df = pd.concat(dfs, ignore_index=True)

print("✅ Combined shape:", combined_df.shape)

# ----------- FINAL CLEANING -----------
cols = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]

for col in cols:
    if col in combined_df.columns:
        combined_df[col] = combined_df[col].fillna(method="ffill")

combined_df = combined_df.drop_duplicates()

# ---------------- SAVE ----------------
output_path = "../data/final_combined_data.csv"
combined_df.to_csv(output_path, index=False)

print("🎉 DONE!")
print("Saved file:", output_path)
print("Cities:", combined_df["City"].unique())
print("Stations:", combined_df["Station"].unique())