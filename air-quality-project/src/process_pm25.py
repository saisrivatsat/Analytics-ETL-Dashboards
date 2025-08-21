import pandas as pd
import requests
from tqdm import tqdm
import time
import os

# Load raw CSV (replace this path if needed)
RAW_CSV_PATH = "data/raw/pm25_daily_full.csv"
OUTPUT_CSV_PATH = "data/processed/pm25_geo_enriched.csv"

# Step 1: Load and clean raw data
print("Loading and cleaning raw data...")
df = pd.read_csv(RAW_CSV_PATH)

# Drop rows with missing PM2.5 values or sensor_id
df_clean = df[["value", "sensor_id", "period.datetimeFrom.utc"]].dropna()
df_clean = df_clean.rename(columns={"value": "pm25", "period.datetimeFrom.utc": "date"})

# Ensure correct types
df_clean["date"] = pd.to_datetime(df_clean["date"])
df_clean["sensor_id"] = df_clean["sensor_id"].astype(int)

# Step 2: Fetch sensor coordinates
print("Fetching sensor coordinates...")
API_KEY = os.getenv("OPENAQ_API_KEY") 
headers = {"x-api-key": API_KEY}

unique_sensors = df_clean["sensor_id"].unique()
sensor_coords = {}

for sensor_id in tqdm(unique_sensors, desc="Coordinates"):
    url = f"https://api.openaq.org/v3/sensors/{sensor_id}"
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json().get("data", {})
            coords = data.get("coordinates", {})
            sensor_coords[sensor_id] = coords
        else:
            print(f"Sensor {sensor_id} failed: {res.status_code}")
    except Exception as e:
        print(f"Error fetching sensor {sensor_id}: {e}")
    time.sleep(0.2)  # to avoid rate-limiting

df_clean["latitude"] = df_clean["sensor_id"].map(lambda x: sensor_coords.get(x, {}).get("latitude"))
df_clean["longitude"] = df_clean["sensor_id"].map(lambda x: sensor_coords.get(x, {}).get("longitude"))

# Step 3: Reverse geocoding using Nominatim
def reverse_geocode(lat, lon):
    if pd.isna(lat) or pd.isna(lon):
        return None, None
    try:
        res = requests.get(
            f"https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json"},
            headers={"User-Agent": "air-quality-project"}
        )
        if res.status_code == 200:
            data = res.json()
            city = data.get("address", {}).get("city") or data.get("address", {}).get("town") or data.get("address", {}).get("village")
            country = data.get("address", {}).get("country")
            return city, country
    except Exception as e:
        print(f"Reverse geocode error: {e}")
    return None, None

print("Performing reverse geocoding...")
geo_data = df_clean[["latitude", "longitude"]].drop_duplicates()
geo_data["city"], geo_data["country"] = zip(*geo_data.apply(lambda row: reverse_geocode(row["latitude"], row["longitude"]), axis=1))

# Merge back enriched data
df_enriched = df_clean.merge(geo_data, on=["latitude", "longitude"], how="left")

# Step 4: Save final enriched data
print(f"Saving final enriched dataset to: {OUTPUT_CSV_PATH}")
df_enriched[["date", "pm25", "sensor_id", "city", "country"]].to_csv(OUTPUT_CSV_PATH, index=False)

print("Process completed.")
