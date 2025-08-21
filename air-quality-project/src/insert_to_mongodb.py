import json
from pymongo import MongoClient # type: ignore

# Mongo connection (local default)
client = MongoClient("mongodb://localhost:27017/")

# Choose DB and collection
db = client["airquality"]
collection = db["pm25_raw"]

# Load your raw JSON file
with open("data/raw/pm25_daily_full.json", "r") as f:
    records = [json.loads(line) for line in f]

# Insert into MongoDB
result = collection.insert_many(records)

print(f"Inserted {len(result.inserted_ids)} records into MongoDB collection 'pm25_raw'")
