import pandas as pd
import psycopg2 # type: ignore

# Load cleaned CSV
df = pd.read_csv("data/cleaned/cleaned_happiness.csv")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="happinessdb",
    user="saisrivatsat",
    host="localhost",
    port=5433
)
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS happiness_data (
        country_name TEXT,
        year INT,
        life_ladder FLOAT,
        log_gdp_per_capita FLOAT,
        social_support FLOAT,
        healthy_life_expectancy_at_birth FLOAT,
        freedom_to_make_life_choices FLOAT,
        generosity FLOAT,
        perceptions_of_corruption FLOAT,
        positive_affect FLOAT,
        negative_affect FLOAT
    )
""")

# Insert data row-by-row
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO happiness_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# Commit and close
conn.commit()
cur.close()
conn.close()

print("Happiness data loaded into PostgreSQL.")
