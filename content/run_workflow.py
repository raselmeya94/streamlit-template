import streamlit as st
from pathlib import Path
import streamlit as st

from src.common.common import page_setup

page_setup(page="main")
# Run workflow interface
def run_workflow():
    st.title("⚙️ Run Workflow")
    st.write("""
        This page allows you to run various workflows on peptide sequences, 
        including mass calculations and further analysis.
    """)

# Run the page
run_workflow()
