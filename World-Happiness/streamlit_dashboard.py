# World-Happiness/streamlit_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load data
BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "cleaned" / "cleaned_happiness.csv")
df["year"] = df["year"].astype(int)

st.set_page_config(layout="wide")
st.title("😊 World Happiness Report Dashboard")

# Sidebar filters
st.sidebar.header("📌 Filter Data")

# Country filter
countries = ["All"] + sorted(df["country_name"].unique())
selected_country = st.sidebar.selectbox("Select Country", countries)
if selected_country != "All":
    df = df[df["country_name"] == selected_country]

# Year filter
years = ["All"] + sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)
if selected_year != "All":
    df = df[df["year"] == selected_year]

# Download filtered data
st.sidebar.markdown("💾 Download Filtered Dataset")
st.sidebar.download_button(
    "⬇️ Download CSV",
    df.to_csv(index=False),
    file_name="filtered_happiness.csv"
)

# Key Metrics
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg Happiness", f"{df['life_ladder'].mean():.2f} / 10")
col2.metric("Max GDP (log)", f"{df['log_gdp_per_capita'].max():.2f}")
col3.metric("Countries Included", df["country_name"].nunique())

# Global Happiness Trend
st.subheader("📈 Global Average Happiness Over Time")
if "year" in df.columns and selected_year == "All":
    trend_df = df.groupby("year")["life_ladder"].mean().reset_index()
    fig_trend = px.line(trend_df, x="year", y="life_ladder", markers=True,
                        labels={"life_ladder": "Average Happiness", "year": "Year"},
                        title="Global Happiness Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

# Top Happiest Countries (latest year in the filtered data)
st.subheader(f"🌍 Top 10 Happiest Countries ({df['year'].max()})")
top10 = df[df["year"] == df["year"].max()].sort_values("life_ladder", ascending=False).head(10)
fig_top10 = px.bar(top10, x="life_ladder", y="country_name", orientation="h",
                   title="Top 10 Countries", labels={"life_ladder": "Happiness Score"})
st.plotly_chart(fig_top10, use_container_width=True)

# Correlation Heatmap
st.subheader("🧠 Correlation Matrix of Happiness Indicators")
numeric_df = df.select_dtypes(include="number").drop(columns=["year"])
corr_matrix = numeric_df.corr()
fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", title="Correlation Heatmap")
st.plotly_chart(fig_corr, use_container_width=True)

# Factor Relationships
st.subheader("📌 Factors Correlated with Happiness")

factors = [
    "log_gdp_per_capita", "social_support", "healthy_life_expectancy_at_birth",
    "freedom_to_make_life_choices", "generosity", "perceptions_of_corruption"
]

for feature in factors:
    st.markdown(f"#### ➕ {feature.replace('_', ' ').title()}")
    fig = px.scatter(
        df, x=feature, y="life_ladder", trendline="ols",
        labels={"life_ladder": "Happiness Score", feature: feature.replace("_", " ").title()},
        title=f"Happiness vs {feature.replace('_', ' ').title()}"
    )
    st.plotly_chart(fig, use_container_width=True)

st.success("Dashboard loaded successfully.")
