import psycopg2  # type: ignore
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Output directory
os.makedirs("outputs", exist_ok=True)

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="airqualitydb",
    user="saisrivatsat",
    host="localhost",
    port=5433
)

# Load data
query = "SELECT * FROM pm25_data WHERE city IS NOT NULL;"
df = pd.read_sql(query, conn)
conn.close()
df["date"] = pd.to_datetime(df["date"])

# -------- 1. Daily Average PM2.5 Over Time --------
plt.figure(figsize=(12, 6))
daily_avg = df.groupby("date")["pm25"].mean()
daily_avg.plot()
max_day = daily_avg.idxmax()
max_val = daily_avg.max()
plt.annotate(f"Peak: {max_val:.2f}", xy=(max_day, max_val), xytext=(max_day, max_val + 100),
             arrowprops=dict(facecolor='black', arrowstyle="->"))
plt.title("Daily Average PM2.5")
plt.xlabel("Date")
plt.ylabel("PM2.5 (µg/m³)")
plt.tight_layout()
plt.savefig("outputs/daily_pm25_trend.png")
plt.close()

# -------- 2. Top 10 Cities with Highest Avg PM2.5 --------
plt.figure(figsize=(12, 6))
top_cities = df.groupby("city")["pm25"].mean().sort_values(ascending=False).head(10)
ax = sns.barplot(x=top_cities.values, y=top_cities.index, palette="Reds_r")
for i, v in enumerate(top_cities.values):
    ax.text(v + 2, i, f"{v:.1f}", color='black', va='center')
plt.title("Top 10 Cities by Avg PM2.5")
plt.xlabel("Avg PM2.5 (µg/m³)")
plt.tight_layout()
plt.savefig("outputs/top10_cities_pm25.png")
plt.close()

# -------- 3. Distribution of PM2.5 --------
plt.figure(figsize=(10, 5))
sns.histplot(df["pm25"], bins=30, kde=True, color="blue")
plt.axvline(df["pm25"].mean(), color='red', linestyle='--')
plt.text(df["pm25"].mean() + 10, 1000, f"Mean: {df['pm25'].mean():.2f}", color="red")
plt.title("Distribution of PM2.5 Levels")
plt.xlabel("PM2.5 (µg/m³)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("outputs/pm25_distribution.png")
plt.close()

# -------- 4. Avg PM2.5 by Country --------
plt.figure(figsize=(14, 6))
country_avg = df.groupby("country")["pm25"].mean().sort_values(ascending=False)
ax = sns.barplot(x=country_avg.index, y=country_avg.values, palette="Blues")
for i, v in enumerate(country_avg.values):
    ax.text(i, v + 2, f"{v:.1f}", color='black', ha='center')
plt.xticks(rotation=45, ha="right")
plt.title("Average PM2.5 by Country")
plt.ylabel("Avg PM2.5 (µg/m³)")
plt.tight_layout()
plt.savefig("outputs/country_pm25.png")
plt.close()

# -------- 5. Avg PM2.5 by Month --------
df["month"] = df["date"].dt.month
monthly_avg = df.groupby("month")["pm25"].mean()
plt.figure(figsize=(10, 5))
sns.lineplot(x=monthly_avg.index, y=monthly_avg.values, marker='o')
plt.title("Average PM2.5 by Month")
plt.xlabel("Month")
plt.ylabel("PM2.5 (µg/m³)")
plt.tight_layout()
plt.savefig("outputs/monthly_avg_pm25.png")
plt.close()

# -------- 6. Avg PM2.5 by Day of Week --------
df["weekday"] = df["date"].dt.day_name()
weekday_avg = df.groupby("weekday")["pm25"].mean()
ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_avg = weekday_avg.reindex(ordered_days)
plt.figure(figsize=(10, 5))
ax = sns.barplot(x=weekday_avg.index, y=weekday_avg.values, palette="coolwarm")
for i, v in enumerate(weekday_avg.values):
    ax.text(i, v + 1, f"{v:.1f}", ha='center')
plt.title("Average PM2.5 by Day of the Week")
plt.ylabel("PM2.5 (µg/m³)")
plt.tight_layout()
plt.savefig("outputs/weekday_avg_pm25.png")
plt.close()

# -------- 7. Avg PM2.5 by Year --------
df["year"] = df["date"].dt.year
yearly_avg = df.groupby("year")["pm25"].mean()
plt.figure(figsize=(10, 5))
sns.lineplot(x=yearly_avg.index, y=yearly_avg.values, marker='o')
plt.title("Average PM2.5 by Year")
plt.xlabel("Year")
plt.ylabel("PM2.5 (µg/m³)")
plt.tight_layout()
plt.savefig("outputs/yearly_avg_pm25.png")
plt.close()

print("All visualizations saved to `outputs/` folder.")
