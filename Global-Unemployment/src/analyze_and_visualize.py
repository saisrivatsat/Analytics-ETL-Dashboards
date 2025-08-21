import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned data
df = pd.read_csv("data/cleaned/cleaned_unemployment.csv")

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Convert year to int
df["year"] = df["year"].astype(int)

# Set global styles
sns.set(style="whitegrid")
plt.rcParams.update({"figure.autolayout": True})

# 1. Global Average Unemployment Over Time
plt.figure(figsize=(10, 5))
global_trend = df.groupby("year")["unemployment_rate"].mean().reset_index()
sns.lineplot(x="year", y="unemployment_rate", data=global_trend, marker='o')
plt.title("Global Average Unemployment Rate (2014–2024)")
plt.ylabel("Unemployment Rate (%)")
plt.xlabel("Year")
plt.grid(True)
plt.savefig("outputs/global_unemployment_trend.png")
plt.close()

# 2. Top 10 Countries with Highest Average Unemployment
plt.figure(figsize=(12, 6))
top_countries = df.groupby("country_name")["unemployment_rate"].mean().sort_values(ascending=False).head(10)
ax = sns.barplot(x=top_countries.values, y=top_countries.index, color="tomato")  # Use a solid color
ax.bar_label(ax.containers[0], fmt="%.1f", padding=3)
plt.title("Top 10 Countries with Highest Avg Unemployment (2014–2024)")
plt.xlabel("Average Unemployment Rate (%)")
plt.ylabel("Country")
plt.savefig("outputs/top10_unemployment_countries.png")
plt.close()


# 3. Unemployment by Gender Over Time
plt.figure(figsize=(10, 5))
gender_trend = df.groupby(["year", "sex"])["unemployment_rate"].mean().reset_index()
sns.lineplot(data=gender_trend, x="year", y="unemployment_rate", hue="sex", marker="o")
plt.title("Unemployment Trends by Gender (2014–2024)")
plt.ylabel("Unemployment Rate (%)")
plt.xlabel("Year")
plt.grid(True)
plt.savefig("outputs/unemployment_by_gender.png")
plt.close()

# 4. Unemployment by Age Group
plt.figure(figsize=(12, 6))
age_group_avg = df.groupby("age_group")["unemployment_rate"].mean().sort_values(ascending=False)
ax = sns.barplot(x=age_group_avg.values, y=age_group_avg.index, color="skyblue")  # consistent color
ax.bar_label(ax.containers[0], fmt="%.1f", padding=3)
plt.title("Average Unemployment Rate by Age Group (2014–2024)")
plt.xlabel("Average Unemployment Rate (%)")
plt.ylabel("Age Group")
plt.savefig("outputs/unemployment_by_age_group.png")
plt.close()

# 5. Country with Highest Unemployment Over Years
highest_country = df.groupby(["country_name", "year"])["unemployment_rate"].mean().reset_index()
top_country = highest_country.groupby("country_name")["unemployment_rate"].mean().idxmax()
trend_top_country = highest_country[highest_country["country_name"] == top_country]

plt.figure(figsize=(10, 5))
sns.lineplot(data=trend_top_country, x="year", y="unemployment_rate", marker="o")
plt.title(f"Unemployment Trend in {top_country} (2014–2024)")
plt.ylabel("Unemployment Rate (%)")
plt.xlabel("Year")
plt.grid(True)
plt.savefig("outputs/unemployment_trend_top_country.png")
plt.close()

print("All visualizations saved in the 'outputs/' folder.")

# 6. Correlation Heatmap
plt.figure(figsize=(10, 8))
numeric_cols = df.select_dtypes(include=["float64", "int64"])
correlation_matrix = numeric_cols.corr()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Matrix of Numeric Unemployment Data")
plt.tight_layout()
plt.savefig("outputs/correlation_matrix_unemployment.png")
plt.close()

# 7. Unemployment Rate Distribution
plt.figure(figsize=(10, 5))
sns.histplot(df["unemployment_rate"], bins=30, kde=True, color="blue")
plt.axvline(df["unemployment_rate"].mean(), color='red', linestyle='--')
plt.text(df["unemployment_rate"].mean() + 0.5, 50, f"Mean: {df['unemployment_rate'].mean():.2f}", color="red")
plt.title("Distribution of Unemployment Rates")
plt.xlabel("Unemployment Rate (%)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("outputs/unemployment_distribution.png")
plt.close()
