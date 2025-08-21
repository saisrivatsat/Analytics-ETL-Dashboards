import pandas as pd
import os

# Paths
RAW_PATH = "data/raw/global_unemployment_data.csv"
CLEANED_PATH = "data/cleaned/cleaned_unemployment.csv"

# Load raw data
df = pd.read_csv(RAW_PATH)

# Inspect initial structure
print("Initial shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())

# Strip whitespace and standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Melt year columns to convert wide → long format
year_cols = [str(year) for year in range(2014, 2025)]
df_long = df.melt(
    id_vars=["country_name", "indicator_name", "sex", "age_group", "age_categories"],
    value_vars=year_cols,
    var_name="year",
    value_name="unemployment_rate"
)

# Clean and format
df_long["year"] = df_long["year"].astype(int)
df_long["unemployment_rate"] = pd.to_numeric(df_long["unemployment_rate"], errors="coerce")

# Drop rows with missing unemployment rates
df_clean = df_long.dropna(subset=["unemployment_rate"])

# Save cleaned version
os.makedirs("data/cleaned", exist_ok=True)
df_clean.to_csv(CLEANED_PATH, index=False)

# Summary
print("Cleaned shape:", df_clean.shape)
print("Columns:", df_clean.columns.tolist())
print(df_clean.head())
print("Unique countries:", df_clean['country_name'].nunique())
print("Unique years:", df_clean['year'].nunique())
print("Unique indicators:", df_clean['indicator_name'].unique())
