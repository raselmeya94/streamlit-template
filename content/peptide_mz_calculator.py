# peptide_mz_calculator.py

import streamlit as st
import pyopenms as oms
from pathlib import Path
import streamlit as st

from src.common.common import page_setup

page_setup(page="main")

# Function to calculate m/z ratio
def calculate_mz(sequence: str, charge_state: int):
    try:
        seq = oms.AASequence.fromString(sequence)
        mz = seq.getMZ(charge_state)
        return round(mz, 4)
    except Exception as e:
        return str(e)

# Streamlit UI for Peptide m/z Calculator

# def peptide_mz_calculator():
#     st.title("🧬 Peptide m/z Calculator")
    
#     sequence = st.text_input("🔢 Enter Peptide Sequence", "", help="Use uppercase letters (A-Z)")
#     charge = st.slider("🔋 Select Charge State", min_value=1, max_value=10, step=1)
    
#     if sequence:
#         if not sequence.isalpha():
#             st.error("❌ Sequence must contain only letters (A-Z)")
#         elif len(sequence) < 2:
#             st.warning("⚠ Sequence must have at least 2 characters.")
#         else:
#             mz = calculate_mz(sequence, charge)
#             st.success(f"✅ Calculated m/z ratio:: **{mz}**")
            
#             st.session_state["sequence"] = sequence

def peptide_mz_calculator():
    st.title("🧬 Peptide m/z Calculator")
    
    # Initialize session state if not already set
    if "sequence" not in st.session_state:
        st.session_state["sequence"] = None
    if "charge" not in st.session_state:
        st.session_state["charge"] = None
    if "mz" not in st.session_state:
        st.session_state["mz"] = None

    # Input fields with session state
    sequence = st.text_input(
        "🔢 Enter Peptide Sequence", 
        value=st.session_state["sequence"],  # Persist input
        help="Use uppercase letters (A-Z)"
    )
    
    charge = st.slider(
        "🔋 Select Charge State", 
        min_value=1, 
        max_value=10, 
        step=1, 
        value=st.session_state["charge"]  # Persist slider value
    )
    
    if sequence:
        if not sequence.isalpha():
            st.error("❌ Sequence must contain only letters (A-Z)")
        elif len(sequence) < 2:
            st.warning("⚠ Sequence must have at least 2 characters.")
        else:
            mz = calculate_mz(sequence, charge)
            st.success(f"✅ Calculated m/z ratio: **{mz}**")

            # Update session state on input change
            st.session_state["sequence"] = sequence
            st.session_state["charge"] = charge
            st.session_state["mz"] = mz


# Run the page

peptide_mz_calculator()
