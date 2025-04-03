# # monoisotopic_mass.py

# import streamlit as st
# import pyopenms as oms
# import pandas as pd
# import plotly.express as px

# # Apply Custom CSS
# st.markdown(
#     """
#     <style>
#     /* Table Header Styling */
#     thead th {
#         background-color: #4CAF50 !important; /* Green Background */
#         color: white !important; /* White Text */
#         font-weight: bold !important; /* Bold Header */
#         text-align: center !important;
#     }

#     /* Table Body Styling */
#     tbody td {
#         text-align: center !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Function to get amino acid information
# def get_amino_acid_info(sequence: str):
#     try:
#         seq = oms.AASequence.fromString(sequence)
#         amino_acids = [{"Amino Acid": aa.getName(), "Monoisotopic Mass": round(aa.getMonoWeight(), 4)} for aa in seq]
#         return pd.DataFrame(amino_acids)
#     except Exception as e:
#         return str(e)

# # Function to plot amino acid mass distribution
# def plot_amino_acid_masses(df):
#     fig = px.scatter(df, x=df.index, y="Monoisotopic Mass", text="Amino Acid", color="Monoisotopic Mass")
#     fig.update_traces(textposition='top center')
#     fig.update_layout(xaxis_title="Position", yaxis_title="Monoisotopic Mass (Da)")
#     return fig

# # Monoisotopic Mass Page
# def monoisotopic_mass_page():
#     st.title("📊 Monoisotopic Mass Distribution")
    
#     if "sequence" in st.session_state:
#         sequence = st.session_state["sequence"]
#         amino_acid_df = get_amino_acid_info(sequence)
        
#         if isinstance(amino_acid_df, pd.DataFrame):
#             st.dataframe(amino_acid_df, use_container_width=True)

#             st.subheader("📈 Interactive Amino Acid Mass Distribution")
#             fig = plot_amino_acid_masses(amino_acid_df)
#             st.plotly_chart(fig)
#         else:
#             st.error("⚠ Error processing sequence.")
#     else:
#         st.warning("⚠ No sequence provided. Return to main page.")
#         st.page_link("peptide_mz_calculator.py", label="🔙 Go Back")

# # Run the page
# monoisotopic_mass_page()

import streamlit as st
import pyopenms as oms
import pandas as pd
import plotly.express as px
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

# Function to plot amino acid mass distribution
# def plot_amino_acid_masses(df):
#     fig = px.scatter(df, x=df.index, y="Monoisotopic Mass", text="Amino Acid", color="Monoisotopic Mass")
#     fig.update_traces(textposition='top center')
#     fig.update_layout(xaxis_title="Position", yaxis_title="Monoisotopic Mass (Da)")
#     return fig
def plot_amino_acid_masses(df):
    min_mass = df["Monoisotopic Mass"].min()
    y_min = 0 if min_mass < 10 else min_mass - 10  # Ensure y-axis starts properly

    fig = px.scatter(df, x=df.index, y="Monoisotopic Mass", text="Amino Acid", color="Monoisotopic Mass")
    fig.update_traces(textposition='top center')
    fig.update_layout(
        xaxis_title="Position",
        yaxis_title="Monoisotopic Mass (Da)",
        yaxis=dict(range=[y_min, df["Monoisotopic Mass"].max() + 5], autorange=False)  # Extend y-axis slightly
    )
    return fig

# Monoisotopic Mass Page
def monoisotopic_mass_page():
    st.title("📊 Monoisotopic Mass Distribution")
    sequence = st.session_state["sequence"]
    
    if sequence:
        amino_acid_df = get_amino_acid_info(sequence)
        
        if isinstance(amino_acid_df, pd.DataFrame):
            # Display Styled Table
            st.markdown("### 🧬 Amino Acid Composition")
            st.table(amino_acid_df)  # Replaces st.dataframe()
            
            st.subheader("📈 Interactive Amino Acid Mass Distribution")
            fig = plot_amino_acid_masses(amino_acid_df)
            st.plotly_chart(fig)
        else:
            st.error("⚠ Error processing sequence.")
    else:
        st.warning("⚠ No sequence provided. Return to main page.")

# Run the page
monoisotopic_mass_page()
