# streamlit_dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load cleaned data
BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "cleaned" / "cleaned_unemployment.csv")
df["year"] = df["year"].astype(int)

# Streamlit page setup
st.set_page_config(page_title="Global Unemployment Dashboard", layout="wide")
st.title("📉 Global Unemployment Dashboard (2014–2024)")

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")

# Country filter
countries = ["All"] + sorted(df["country_name"].unique())
selected_country = st.sidebar.selectbox("Country", countries)
if selected_country != "All":
    df = df[df["country_name"] == selected_country]

# Gender filter
genders = ["All"] + sorted(df["sex"].unique())
selected_gender = st.sidebar.selectbox("Gender", genders)
if selected_gender != "All":
    df = df[df["sex"] == selected_gender]

# Age Group filter
age_groups = ["All"] + sorted(df["age_group"].unique())
selected_age = st.sidebar.selectbox("Age Group", age_groups)
if selected_age != "All":
    df = df[df["age_group"] == selected_age]

# Year filter
years = ["All"] + sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Year", years)
if selected_year != "All":
    df = df[df["year"] == selected_year]

# Download filtered data
st.sidebar.download_button(
    "📥 Download CSV", data=df.to_csv(index=False), file_name="filtered_unemployment.csv"
)

# Key Metrics
st.subheader("📊 Key Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg Unemployment Rate", f"{df['unemployment_rate'].mean():.2f}%")
col2.metric("Max Unemployment Rate", f"{df['unemployment_rate'].max():.2f}%")
col3.metric("Countries in View", df["country_name"].nunique())

# Line Chart - Global Trend
st.subheader("📈 Global Unemployment Trend Over Time")
yearly_avg = df.groupby("year")["unemployment_rate"].mean().reset_index()
fig1 = px.line(yearly_avg, x="year", y="unemployment_rate", markers=True,
               labels={"unemployment_rate": "Unemployment Rate (%)"},
               title="Global Average Unemployment (2014–2024)")
st.plotly_chart(fig1, use_container_width=True)

# Bar Chart - Top 10 Countries by Avg Rate
st.subheader("🌍 Top 10 Countries by Average Unemployment Rate")
top10 = (
    df.groupby("country_name")["unemployment_rate"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig2 = px.bar(top10, x="unemployment_rate", y="country_name", orientation="h",
              labels={"unemployment_rate": "Avg Unemployment Rate", "country_name": "Country"},
              title="Top 10 Countries (2014–2024)", color="unemployment_rate", color_continuous_scale="Reds")
st.plotly_chart(fig2, use_container_width=True)

# Line Chart - Gender Comparison
st.subheader("👩‍🦰👨 Unemployment by Gender Over Time")
gender_trend = df.groupby(["year", "sex"])["unemployment_rate"].mean().reset_index()
fig3 = px.line(gender_trend, x="year", y="unemployment_rate", color="sex", markers=True,
               labels={"unemployment_rate": "Unemployment Rate (%)"}, title="Gender-wise Trends")
st.plotly_chart(fig3, use_container_width=True)

# Bar Chart - By Age Group
st.subheader("📊 Unemployment by Age Group")
age_avg = df.groupby("age_group")["unemployment_rate"].mean().reset_index()
fig4 = px.bar(age_avg, x="unemployment_rate", y="age_group", orientation="h",
              labels={"unemployment_rate": "Avg Rate", "age_group": "Age Group"},
              title="Average Unemployment by Age Group", color="unemployment_rate", color_continuous_scale="Blues")
st.plotly_chart(fig4, use_container_width=True)

st.success("Dashboard rendered successfully.")
