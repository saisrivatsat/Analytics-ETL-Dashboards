import requests
import pandas as pd
import os
from dotenv import load_dotenv # type: ignore
import time

# Load the API key
load_dotenv()
API_KEY = os.getenv("OPENAQ_API_KEY")

headers = {
    "X-API-Key": API_KEY
}

# 1. Get list of sensors that measure PM2.5
def get_pm25_sensors(limit=50):
    url = "https://api.openaq.org/v3/parameters/2/latest"
    params = {"limit": limit}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch sensor list: {response.text}")
    results = response.json().get("results", [])
    # API responses use the key `sensorId` to identify each sensor.
    # The previous implementation looked for `sensorsId`, which never
    # exists and resulted in an empty sensor list.  Fetch the correct key
    # and guard against missing values.
    return [r["sensorId"] for r in results if r.get("sensorId") is not None]

# 2. Get daily average values for a given sensor ID
def get_daily_values(sensor_id, limit=365):
    url = f"https://api.openaq.org/v3/sensors/{sensor_id}/days"
    params = {"limit": limit}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Sensor {sensor_id} failed: {response.status_code}")
        return []
    return response.json().get("results", [])

# 3. Loop through sensors and collect data
def fetch_all_pm25_daily(sensor_limit=50, days_limit=365):
    sensors = get_pm25_sensors(sensor_limit)
    all_data = []
    for i, sensor_id in enumerate(sensors):
        print(f"Fetching sensor {i+1}/{len(sensors)} (ID: {sensor_id})...")
        daily_data = get_daily_values(sensor_id, days_limit)
        for entry in daily_data:
            entry["sensor_id"] = sensor_id  # keep track of sensor
        all_data.extend(daily_data)
        time.sleep(0.5)  # avoid hammering API
    return pd.json_normalize(all_data)

if __name__ == "__main__":
    df = fetch_all_pm25_daily(sensor_limit=50, days_limit=365)
    print(f"\nTotal records fetched: {len(df)}")

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/pm25_daily_full.csv", index=False)
    df.to_json("data/raw/pm25_daily_full.json", orient="records", lines=True)
    print("Data saved to data/raw/pm25_daily_full.csv and .json")
