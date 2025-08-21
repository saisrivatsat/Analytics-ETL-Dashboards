import os
import runpy
from contextlib import contextmanager

import streamlit as st

st.set_page_config(page_title="Analytics Dashboards", layout="wide")
# Prevent sub-dashboards from resetting page config
st.set_page_config = lambda *args, **kwargs: None

@contextmanager
def run_from(path: str):
    """Temporarily change directory to run a Streamlit script."""
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)

st.sidebar.title("Dashboards")
dashboard = st.sidebar.radio(
    "Select a dashboard",
    (
        "Air Quality",
        "World Happiness",
        "Global Unemployment",
    ),
)

if dashboard == "Air Quality":
    with run_from("air-quality-project"):
        runpy.run_path("streamlit_dashboard.py", run_name="__main__")
elif dashboard == "World Happiness":
    with run_from("World-Happiness"):
        runpy.run_path("streamlit_dashboard.py", run_name="__main__")
else:
    with run_from("Global-Unemployment"):
        runpy.run_path("streamlit_dashboard.py", run_name="__main__")
