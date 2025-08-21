import pandas as pd
import psycopg2 # type: ignore

# Load cleaned data
df = pd.read_csv("data/cleaned/cleaned_unemployment.csv")

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="unemploymentdb",
    user="saisrivatsat", 
    host="localhost",
    port=5433
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS unemployment_data (
    country_name TEXT,
    indicator_name TEXT,
    sex TEXT,
    age_group TEXT,
    age_categories TEXT,
    year INT,
    unemployment_rate FLOAT
)
""")

# Insert records
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO unemployment_data (
            country_name, indicator_name, sex, age_group, age_categories, year, unemployment_rate
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

conn.commit()
cur.close()
conn.close()
print("Unemployment data loaded into PostgreSQL.")

