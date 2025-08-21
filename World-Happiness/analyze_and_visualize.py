import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load cleaned dataset
df = pd.read_csv("data/cleaned/cleaned_happiness.csv")

# Create outputs folder
os.makedirs("outputs", exist_ok=True)

# 1. Top 10 happiest countries by latest year available
latest_year = df["year"].max()
top10 = df[df["year"] == latest_year].sort_values("life_ladder", ascending=False).head(10)
plt.figure(figsize=(10, 6))
ax = sns.barplot(x="life_ladder", y="country_name", data=top10, hue="country_name", dodge=False, legend=False, palette="viridis")
for i, v in enumerate(top10["life_ladder"]):
    ax.text(v + 0.05, i, f"{v:.2f}", va="center")
plt.title(f"Top 10 Happiest Countries in {int(latest_year)}")
plt.xlabel("Happiness Score (Life Ladder)")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("outputs/top10_happiest_countries.png")
plt.close()

# 2. Country vs average happiness (all years)
country_avg = df.groupby("country_name")["life_ladder"].mean().sort_values(ascending=False).head(15)
plt.figure(figsize=(12, 6))
ax = sns.barplot(
    x=country_avg.values,
    y=country_avg.index,
    hue=country_avg.index,      
    palette="coolwarm",
    dodge=False,
    legend=False
)

for i, v in enumerate(country_avg.values):
    ax.text(v + 0.05, i, f"{v:.2f}", va="center")
plt.title("Average Happiness Score (Top 15 Countries)")
plt.xlabel("Average Happiness")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("outputs/country_vs_happiness.png")
plt.close()

# 3. Trend of happiness globally over years
year_avg = df.groupby("year")["life_ladder"].mean().reset_index()
plt.figure(figsize=(10, 5))
sns.lineplot(x="year", y="life_ladder", data=year_avg, marker='o')
for i in range(len(year_avg)):
    plt.text(year_avg["year"][i], year_avg["life_ladder"][i] + 0.02, f"{year_avg['life_ladder'][i]:.2f}", ha='center')
plt.title("Global Average Happiness Score Over Years")
plt.ylabel("Life Ladder Score")
plt.xlabel("Year")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/yearwise_happiness.png")
plt.close()

# 4. Correlation heatmap
plt.figure(figsize=(10, 8))
numeric_cols = df.select_dtypes(include=["float64", "int64"]).drop(columns=["year"])
sns.heatmap(numeric_cols.corr(), annot=True, cmap="Blues", fmt=".2f")
plt.title("Correlation Matrix of Happiness Indicators")
plt.tight_layout()
plt.savefig("outputs/correlation_matrix.png")
plt.close()

# 5. Happiness by GDP
plt.figure(figsize=(10, 6))
sns.scatterplot(x="log_gdp_per_capita", y="life_ladder", data=df, alpha=0.6)
plt.title("Happiness vs GDP per Capita")
plt.xlabel("Log GDP per Capita")
plt.ylabel("Happiness Score (Life Ladder)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/happiness_vs_gdp.png")
plt.close()

# 6. Happiness by social support
plt.figure(figsize=(10, 6))
sns.scatterplot(x="social_support", y="life_ladder", data=df, alpha=0.6)
plt.title("Happiness vs Social Support")
plt.xlabel("Social Support")
plt.ylabel("Happiness Score (Life Ladder)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/happiness_vs_social_support.png")
plt.close()

# 7. Happiness by healthy life expectancy
plt.figure(figsize=(10, 6))
sns.scatterplot(x="healthy_life_expectancy_at_birth", y="life_ladder", data=df, alpha=0.6)
plt.title("Happiness vs Healthy Life Expectancy")
plt.xlabel("Healthy Life Expectancy")
plt.ylabel("Happiness Score (Life Ladder)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/happiness_vs_healthy_life_expectancy.png")
plt.close()

# 8. Happiness by freedom to make life choices
plt.figure(figsize=(10, 6))
sns.scatterplot(x="freedom_to_make_life_choices", y="life_ladder", data=df, alpha=0.6)
plt.title("Happiness vs Freedom to Make Life Choices")
plt.xlabel("Freedom to Make Life Choices")
plt.ylabel("Happiness Score (Life Ladder)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/happiness_vs_freedom.png")
plt.close()

# 9. Happiness by generosity
plt.figure(figsize=(10, 6))
sns.scatterplot(x="generosity", y="life_ladder", data=df, alpha=0.6)
plt.title("Happiness vs Generosity")
plt.xlabel("Generosity")
plt.ylabel("Happiness Score (Life Ladder)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/happiness_vs_generosity.png")
plt.close()

# 10. Happiness by perceptions of corruption
plt.figure(figsize=(10, 6))
sns.scatterplot(x="perceptions_of_corruption", y="life_ladder", data=df, alpha=0.6)
plt.title("Happiness vs Perceptions of Corruption")
plt.xlabel("Perceptions of Corruption")
plt.ylabel("Happiness Score (Life Ladder)")
plt.grid(True)
plt.tight_layout()
plt.savefig("outputs/happiness_vs_corruption.png")
plt.close()

print("All visualizations generated and saved in 'outputs/' folder.")
