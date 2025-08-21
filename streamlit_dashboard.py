import runpy
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Analytics Dashboards", layout="wide", theme="light")
# Prevent sub-dashboards from resetting page config
st.set_page_config = lambda *args, **kwargs: None

BASE = Path(__file__).resolve().parent
DASHBOARD_PATHS = {
    "Air Quality": BASE / "air-quality-project" / "streamlit_dashboard.py",
    "World Happiness": BASE / "World-Happiness" / "streamlit_dashboard.py",
    "Global Unemployment": BASE / "Global-Unemployment" / "streamlit_dashboard.py",
}

st.title("Analytics Dashboards")
st.sidebar.title("Dashboards")
dashboard = st.sidebar.radio(
    "Select a dashboard",
    list(DASHBOARD_PATHS.keys()),
    key="dashboard_selector",
)

runpy.run_path(str(DASHBOARD_PATHS[dashboard]), run_name="__main__")
