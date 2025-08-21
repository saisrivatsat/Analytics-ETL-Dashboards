# streamlit_dashboard.py  (router at repo root)

import os
from contextlib import contextmanager
import runpy
from pathlib import Path
import streamlit as st

# Page config (and prevent sub‑apps from resetting it)
st.set_page_config(page_title="Analytics Dashboards", layout="wide")
st.set_page_config = lambda *args, **kwargs: None  # no-op in child apps

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
