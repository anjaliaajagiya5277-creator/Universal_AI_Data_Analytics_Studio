import streamlit as st
import pandas as pd
from io import BytesIO

# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Export Data",
    page_icon="📥",
    layout="wide"
)

st.title("📥 Export Clean Dataset")

# ----------------------------
# Check Dataset
# ----------------------------

if "df" not in st.session_state:
    st.warning("Please upload and clean a dataset first.")
    st.stop()

df = st.session_state["df"]

# ----------------------------
# Dataset Summary
# ----------------------------

st.subheader("📊 Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows", df.shape[0])

with col2:
    st.metric("Columns", df.shape[1])

with col3:
    st.metric("Missing Values", df.isnull().sum().sum())

with col4:
    st.metric("Duplicate Rows", df.duplicated().sum())

st.divider()

# ----------------------------
# Preview
# ----------------------------

st.subheader("👀 Dataset Preview")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# ----------------------------
# Download CSV
# ----------------------------

st.subheader("📄 Download CSV")

csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="clean_dataset.csv",
    mime="text/csv"
)

st.divider()

# ----------------------------
# Download Excel
# ----------------------------

st.subheader("📊 Download Excel")

buffer = BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df.to_excel(
        writer,
        index=False,
        sheet_name="Clean_Data"
    )

excel_data = buffer.getvalue()

st.download_button(
    label="Download Excel",
    data=excel_data,
    file_name="clean_dataset.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ----------------------------
# Generate Summary Report
# ----------------------------

st.subheader("📝 Dataset Report")

report = f"""
DATASET REPORT

Rows: {df.shape[0]}
Columns: {df.shape[1]}

Missing Values:
{df.isnull().sum().to_string()}

Duplicate Rows:
{df.duplicated().sum()}

Data Types:
{df.dtypes.to_string()}
"""

st.text(report)

st.download_button(
    label="Download Report",
    data=report,
    file_name="dataset_report.txt",
    mime="text/plain"
)

st.success(
    "Dataset ready for export."
)