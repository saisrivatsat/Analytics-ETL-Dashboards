import pandas as pd
import psycopg2 # type: ignore

# Load enriched CSV
df = pd.read_csv("data/processed/pm25_geo_enriched.csv")

# Clean nulls if necessary
df = df.dropna(subset=["date", "pm25", "city", "country"])

# Connect to Postgres
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="airqualitydb",
    user="saisrivatsat"
)
cur = conn.cursor()

# Insert data
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO pm25_data (date, pm25, sensor_id, city, country) VALUES (%s, %s, %s, %s, %s)",
        (row["date"], row["pm25"], row["sensor_id"], row["city"], row["country"])
    )
conn.commit()
cur.close()
conn.close()
print("Enriched data inserted into PostgreSQL.")
