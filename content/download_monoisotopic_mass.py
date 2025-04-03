# donload_monoisotopic_mass.py

import streamlit as st
import pandas as pd
import pyopenms as oms
import zipfile
import io
import os
from pathlib import Path
import streamlit as st

from src.common.common import page_setup

page_setup(page="main")
# Apply Custom CSS for Table Styling
st.markdown(
    """
    <style>
    /* Table Styling */
    table {
        width: 100%;
        border-collapse: collapse;
    }
    
    /* Table Header */
    thead th {
        background-color: #4CAF50 !important; /* Green Header */
        color: white !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 10px;
    }

    /* Table Rows */
    tbody td {
        text-align: center !important;
        padding: 8px;
        border-bottom: 1px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Function to get amino acid information
def get_amino_acid_info(sequence: str):
    try:
        seq = oms.AASequence.fromString(sequence)
        amino_acids = [{"Amino Acid": aa.getName(), "Monoisotopic Mass": round(aa.getMonoWeight(), 4)} for aa in seq]
        return pd.DataFrame(amino_acids)
    except Exception as e:
        return str(e)

# 
# def download_page():
#     st.title("⬇️ Download Monoisotopic Mass Data")
    
#     if "sequence" in st.session_state:
#         sequence = st.session_state["sequence"]
#         charge = st.session_state["charge"]
#         mz= st.session_state["mz"]
#         # Create a dataframe with the sequence and charge and mz value



#         amino_acid_df = get_amino_acid_info(sequence)
        
#         if isinstance(amino_acid_df, pd.DataFrame):
#             csv_data = amino_acid_df.to_csv(index=False).encode('utf-8')
#             st.dataframe(amino_acid_df, use_container_width=True)
#             st.download_button("📥 Download CSV", data=csv_data, file_name="amino_acid_masses.csv", mime='text/csv')
#         else:
#             st.error("⚠ Error processing sequence.")
#     else:
#         st.warning("⚠ No sequence provided. Return to main page.")
#         st.page_link("peptide_mz_calculator.py", label="🔙 Go Back")


def download_page():
    st.title("⬇️ Download Monoisotopic Mass Data")
    sequence = st.session_state["sequence"]
    charge = st.session_state["charge"]
    mz = st.session_state["mz"]
    print("Values: ", sequence, charge, mz)
    
    if sequence and charge and mz:

        # Get the amino acid information for the sequence
        amino_acid_df = get_amino_acid_info(sequence)

        if isinstance(amino_acid_df, pd.DataFrame):
            # Create the first dataset for amino acid masses
            amino_acid_csv = amino_acid_df.to_csv(index=False).encode('utf-8')
            
            # Display preview of the amino acid dataset
            st.subheader("Amino Acid Masses Preview")
            # st.dataframe(amino_acid_df, use_container_width=True)
            st.table(amino_acid_df)  # Replaces st.dataframe()

            # Create the second dataset for sequence, charge state, and m/z ratio
            sequence_data = {
                "Sequence": [sequence],
                "Charge State": [charge],
                "m/z Ratio": [mz]
            }
            sequence_df = pd.DataFrame(sequence_data)
            sequence_csv = sequence_df.to_csv(index=False).encode('utf-8')

            # Display preview of the second dataset
            st.subheader("Sequence, Charge, and m/z Data Preview")
            # st.dataframe(sequence_df, use_container_width=True)
            st.table(sequence_df)  # Replaces st.dataframe()

            # Create a ZIP file in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr("amino_acid_masses.csv", amino_acid_csv)
                zip_file.writestr("sequence_charge_mz.csv", sequence_csv)

            # Make sure the ZIP buffer is at the beginning before saving or sending it for download
            zip_buffer.seek(0)

            # Add a download button for the ZIP file
            st.subheader("Download Results as ZIP")
            st.download_button(
                label="📥 Download Results (ZIP)",
                data=zip_buffer,
                file_name="peptide_masses_data.zip",
                mime="application/zip"
            )

        else:
            st.error("⚠ No sequence provided. Return to main page.")
    else:
        st.warning("⚠ Missing or invalid data in session state. Please go back and provide input.")
# Run the page
download_page()
