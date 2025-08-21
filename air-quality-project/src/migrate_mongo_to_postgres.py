import psycopg2 # type: ignore
from pymongo import MongoClient # type: ignore

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["airquality"]
mongo_collection = mongo_db["pm25_raw"]

# PostgreSQL connection
pg_conn = psycopg2.connect(
    dbname="airqualitydb",
    user="saisrivatsat",  
    host="localhost",
    port=5433
)
pg_cursor = pg_conn.cursor()

# Fetch documents from MongoDB
documents = mongo_collection.find()

insert_query = """
INSERT INTO pm25_data (date, pm25, sensor_id, city, country)
VALUES (%s, %s, %s, %s, %s)
"""

count = 0
for doc in documents:
    try:
        pg_cursor.execute(insert_query, (
            doc.get("date"),
            doc.get("pm25"),
            doc.get("sensor_id"),
            doc.get("city"),
            doc.get("country")
        ))
        count += 1
    except Exception as e:
        print(f"Skipping document due to error: {e}")

# Commit & close
pg_conn.commit()
pg_cursor.close()
pg_conn.close()
print(f"Migrated {count} records from MongoDB to PostgreSQL.")
