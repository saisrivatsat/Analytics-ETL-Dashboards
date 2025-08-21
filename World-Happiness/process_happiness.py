import pandas as pd
import os

# Load raw data
INPUT_CSV = "world-happiness-report.csv"
df = pd.read_csv(INPUT_CSV)

# Initial inspection
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())

# Clean & Save
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Drop duplicates / missing values
df = df.dropna(subset=["country_name", "year", "life_ladder"])

# Save cleaned version
os.makedirs("data/cleaned", exist_ok=True)
df.to_csv("data/cleaned/cleaned_happiness.csv", index=False)

# Summary after cleaning
print("Cleaned data saved.")
print("Shape after cleaning:", df.shape)
print("Columns after cleaning:", df.columns.tolist())
print(df.head())
print("Unique countries:", df["country_name"].nunique())
print("Unique years:", df["year"].nunique())
print("Unique life ladder values:", df["life_ladder"].nunique())

# Optional fields (only print if they exist)
if "region" in df.columns:
    print("Unique regions:", df["region"].nunique())
if "subregion" in df.columns:
    print("Unique subregions:", df["subregion"].nunique())

print("Sample Happiness Scores:", df["life_ladder"].unique()[:10])
