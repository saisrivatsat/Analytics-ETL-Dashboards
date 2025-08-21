import os
from contextlib import contextmanager
import runpy
from pathlib import Path
import streamlit as st

# --- Page Config (title + logo) ---
st.set_page_config(
    page_title="ETL Analytics Dashboards",
    page_icon="📊",  
    layout="wide"
)

# Prevent sub-apps from resetting page config
st.set_page_config = lambda *args, **kwargs: None  

BASE = Path(__file__).resolve().parent

@contextmanager
def run_from(subdir: str):
    """Temporarily cd into a subfolder so relative paths (data/, outputs/) work."""
    prev = os.getcwd()
    os.chdir(BASE / subdir)
    try:
        yield
    finally:
        os.chdir(prev)

st.title("ETL Analytics Dashboards")
st.sidebar.title("Dashboards")
choice = st.sidebar.radio(
    "Select a dashboard",
    ("Air Quality", "World Happiness", "Global Unemployment"),
    key="dashboard_selector",
)

if choice == "Air Quality":
    with run_from("air-quality-project"):
        runpy.run_path("streamlit_dashboard.py", run_name="__main__")
elif choice == "World Happiness":
    with run_from("World-Happiness"):
        runpy.run_path("streamlit_dashboard.py", run_name="__main__")
else:
    with run_from("Global-Unemployment"):
        runpy.run_path("streamlit_dashboard.py", run_name="__main__")
