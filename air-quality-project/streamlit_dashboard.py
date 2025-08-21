import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load data
BASE = Path(__file__).resolve().parent
df = pd.read_csv(BASE / "data" / "processed" / "pm25_geo_enriched.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.dropna(subset=["pm25", "city", "country"])

# Configure page
st.set_page_config(page_title="PM2.5 Dashboard", layout="wide")
st.title("🌍 Air Quality (PM2.5) Interactive Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")
country = st.sidebar.selectbox("Select Country", ["All"] + sorted(df["country"].dropna().unique()))
if country != "All":
    df = df[df["country"] == country]

city = st.sidebar.selectbox("Select City", ["All"] + sorted(df["city"].dropna().unique()))
if city != "All":
    df = df[df["city"] == city]

# Date range filter
min_date, max_date = df["date"].min(), df["date"].max()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])
df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

# Download button
csv = df.to_csv(index=False).encode("utf-8")
st.sidebar.download_button("📥 Download Filtered CSV", data=csv, file_name="filtered_pm25_data.csv", mime="text/csv")

# KPIs
st.markdown("### 📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg PM2.5", f"{df['pm25'].mean():.2f} µg/m³")
col2.metric("Max PM2.5", f"{df['pm25'].max():.2f} µg/m³")
col3.metric("Unique Cities", df["city"].nunique())

# 1. PM2.5 trend over time
st.subheader("📈 Daily PM2.5 Trend")
daily_avg = df.groupby("date")["pm25"].mean().reset_index()
fig_trend = px.line(daily_avg, x="date", y="pm25", labels={"pm25": "PM2.5 (µg/m³)"})
st.plotly_chart(fig_trend, use_container_width=True)

# 2. Top 10 cities by average PM2.5
st.subheader("🏙️ Top 10 Cities by Avg PM2.5")
top_cities = df.groupby("city")["pm25"].mean().sort_values(ascending=False).head(10).reset_index()
fig_top = px.bar(top_cities, x="pm25", y="city", orientation="h", labels={"pm25": "Avg PM2.5", "city": "City"})
st.plotly_chart(fig_top, use_container_width=True)

# 3. Geographic distribution
st.subheader("🗺️ Sensor Locations by PM2.5")
df["pm25_clipped"] = df["pm25"].clip(lower=1, upper=300)
map_df = df.dropna(subset=["latitude", "longitude"])
fig_map = px.scatter_mapbox(
    map_df,
    lat="latitude",
    lon="longitude",
    color="pm25",
    size="pm25_clipped",
    hover_name="city",
    hover_data=["country", "pm25"],
    color_continuous_scale="Reds",
    size_max=15,
    zoom=1,
    height=500,
)
fig_map.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 40, "l": 0, "b": 0})
st.plotly_chart(fig_map, use_container_width=True)

# 4. Monthly & weekday patterns
st.subheader("📅 PM2.5 Patterns by Time")
col1, col2 = st.columns(2)

with col1:
    df["month"] = df["date"].dt.month
    month_avg = df.groupby("month")["pm25"].mean().reset_index()
    fig_month = px.line(month_avg, x="month", y="pm25", markers=True, title="Monthly Avg PM2.5")
    st.plotly_chart(fig_month, use_container_width=True)

with col2:
    df["weekday"] = df["date"].dt.day_name()
    weekday_avg = df.groupby("weekday")["pm25"].mean().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]).reset_index()
    fig_week = px.bar(weekday_avg, x="weekday", y="pm25", title="Weekday Avg PM2.5")
    st.plotly_chart(fig_week, use_container_width=True)

st.success("All visualizations rendered successfully.")
