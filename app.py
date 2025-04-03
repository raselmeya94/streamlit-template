import streamlit as st
from pathlib import Path
import json
# For some reason the windows version only works if this is imported here
import pyopenms

if "settings" not in st.session_state:
        with open("settings.json", "r") as f:
            st.session_state.settings = json.load(f)

if __name__ == '__main__':
    pages = {
        str(st.session_state.settings["app-name"]) : [
            st.Page(Path("content", "quickstart.py"), title="Quickstart", icon="👋"),
            st.Page(Path("content", "documentation.py"), title="Documentation", icon="📖"),
        ],
        "Peptide m/z Calculation": [
            st.Page(Path("content", "peptide_mz_calculator.py"), title="Calculator", icon="🧬"),
            st.Page(Path("content", "monoisotopic_mass.py"), title="Monoisotopic Mass", icon="🧪"),
            st.Page(Path("content", "run_workflow.py"), title="Run Workflow", icon="⚙️"),
            st.Page(Path("content", "download_monoisotopic_mass.py"), title="Download Results", icon="⬇️"),
            ],


        "TOPP Workflow Framework": [
            st.Page(Path("content", "topp_workflow_file_upload.py"), title="File Upload", icon="📁"),
            st.Page(Path("content", "topp_workflow_parameter.py"), title="Configure", icon="⚙️"),
            st.Page(Path("content", "topp_workflow_execution.py"), title="Run", icon="🚀"),
            st.Page(Path("content", "topp_workflow_results.py"), title="Results", icon="📊"),
        ],
        "pyOpenMS Workflow" : [
            st.Page(Path("content", "file_upload.py"), title="File Upload", icon="📂"),
            st.Page(Path("content", "raw_data_viewer.py"), title="View MS data", icon="👀"),
            st.Page(Path("content", "run_example_workflow.py"), title="Run Workflow", icon="⚙️"),
            st.Page(Path("content", "download_section.py"), title="Download Results", icon="⬇️"),
        ],
        
        "Others Topics": [
            st.Page(Path("content", "simple_workflow.py"), title="Simple Workflow", icon="⚙️"),
            st.Page(Path("content", "run_subprocess.py"), title="Run Subprocess", icon="🖥️"),
        ]
    }

    pg = st.navigation(pages)
    pg.run()

# import streamlit as st
# import pyopenms as oms
# import pandas as pd
# import plotly.express as px

# # Function to calculate m/z ratio
# def calculate_mz(sequence: str, charge_state: int):
#     try:
#         seq = oms.AASequence.fromString(sequence)
#         mz = seq.getMZ(charge_state)
#         return round(mz, 4)
#     except Exception as e:
#         return str(e)

# # Function to get amino acid information as a DataFrame
# def get_amino_acid_info(sequence: str):
#     try:
#         seq = oms.AASequence.fromString(sequence)
#         amino_acids = [{"Amino Acid": aa.getName(), "Monoisotopic Mass": round(aa.getMonoWeight(), 4)} for aa in seq]
#         df = pd.DataFrame(amino_acids)
#         return df
#     except Exception as e:
#         return str(e)

# # Function to generate an interactive plot with Plotly
# def plot_interactive_amino_acid_masses(df):
#     fig = px.scatter(df, x=df.index, y="Monoisotopic Mass", text="Amino Acid", size_max=12, color="Monoisotopic Mass",
#                      title="Amino Acid Mass Distribution", labels={"index": "Position in Sequence", "Monoisotopic Mass": "Mass"})
#     fig.update_traces(textposition='top center', marker=dict(size=12, opacity=0.8, line=dict(width=1, color="black")))
#     fig.update_layout(xaxis_title="Amino Acid Position", yaxis_title="Monoisotopic Mass (Da)")
#     return fig

# # Streamlit Web App UI
# def main():
#     # Set page configuration FIRST
#     st.set_page_config(page_title="Peptide m/z Calculator", page_icon="🧬", layout="wide")

#     st.title("🧬 Peptide m/z Calculator")
#     st.write("This tool calculates the mass-to-charge (m/z) ratio for a given peptide sequence and provides interactive visualizations.")

#     # User input for peptide sequence and charge state
#     col1, col2 = st.columns(2)
#     with col1:
#         sequence = st.text_input("🔢 Enter Peptide Sequence", "", help="Use uppercase letters for peptide sequence (A-Z).")
#     with col2:
#         charge = st.slider("🔋 Select Charge State", min_value=1, max_value=10, step=1, help="Charge state of the peptide (positive integer).")

#     # Validation
#     if sequence:
#         if not sequence.isalpha():
#             st.error("❌ Peptide sequence should only contain letters (A-Z). Please check your input.")
#         elif len(sequence) < 2:
#             st.warning("⚠ Peptide sequence should have at least 2 characters.")
#         else:
#             # Calculation
#             if charge:
#                 with st.spinner('⚡ Calculating...'):
#                     mz = calculate_mz(sequence, charge)
#                     st.success(f"✅ Calculated m/z ratio: **{mz}**")

#                     # Display amino acid composition in a table
#                     st.subheader("📊 Amino Acid Composition")
#                     amino_acid_df = get_amino_acid_info(sequence)
#                     if isinstance(amino_acid_df, pd.DataFrame):
#                         st.dataframe(amino_acid_df, use_container_width=True)

#                         # Interactive Plot
#                         st.subheader("📈 Interactive Amino Acid Mass Distribution")
#                         fig = plot_interactive_amino_acid_masses(amino_acid_df)
#                         st.plotly_chart(fig, use_container_width=True)

#                         # Download Report
#                         csv_data = amino_acid_df.to_csv(index=False).encode('utf-8')
#                         st.download_button("📥 Download CSV", data=csv_data, file_name="amino_acid_masses.csv", mime='text/csv')
#                     else:
#                         st.error("⚠ Error processing amino acid information.")
#             else:
#                 st.warning("⚠ Please select a charge state for the peptide.")
#     else:
#         st.warning("⚠ Please enter a valid peptide sequence to calculate m/z.")

#     # Sidebar information
#     st.sidebar.header("ℹ About")
#     st.sidebar.write("""
#         **🔬 Peptide m/z Calculator**  
#         - Calculates the mass-to-charge ratio (m/z) for peptides.  
#         - Provides **interactive visualization** of amino acid masses.  
#         - Supports **CSV downloads** for research.  
#         - Built using **PyOpenMS + Streamlit + Plotly**.  
#     """)

# # Run the app
# if __name__ == "__main__":
#     main()