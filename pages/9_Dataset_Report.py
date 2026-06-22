import streamlit as st
import pandas as pd

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="Dataset Report",
    page_icon="📑",
    layout="wide"
)

st.title("📑 Dataset Report")

# ----------------------------------
# Check Dataset
# ----------------------------------

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# ----------------------------------
# Basic Information
# ----------------------------------

st.header("📊 Basic Information")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())
col4.metric("Duplicate Rows", df.duplicated().sum())

st.divider()

# ----------------------------------
# Data Types
# ----------------------------------

st.header("📝 Data Types")

dtype_df = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str)
})

st.dataframe(
    dtype_df,
    use_container_width=True
)

st.divider()

# ----------------------------------
# Missing Values
# ----------------------------------

st.header("❓ Missing Values")

missing_df = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values,
    "Missing %":
    (df.isnull().sum()/len(df)*100).round(2)
})

st.dataframe(
    missing_df,
    use_container_width=True
)

st.divider()

# ----------------------------------
# Unique Values
# ----------------------------------

st.header("🔢 Unique Values")

unique_df = pd.DataFrame({
    "Column": df.columns,
    "Unique Values": df.nunique().values
})

st.dataframe(
    unique_df,
    use_container_width=True
)

st.divider()

# ----------------------------------
# Numeric Summary
# ----------------------------------

numeric = df.select_dtypes(include="number")

if not numeric.empty:

    st.header("📈 Statistical Summary")

    st.dataframe(
        numeric.describe().T,
        use_container_width=True
    )

st.divider()

# ----------------------------------
# Categorical Summary
# ----------------------------------

categorical = df.select_dtypes(exclude="number")

if not categorical.empty:

    st.header("🔤 Categorical Summary")

    cat_report = []

    for col in categorical.columns:

        cat_report.append({

            "Column": col,

            "Unique Values": df[col].nunique(),

            "Most Frequent":

            df[col].mode()[0]

            if not df[col].mode().empty

            else "N/A"

        })

    st.dataframe(
        pd.DataFrame(cat_report),
        use_container_width=True
    )

st.divider()

# ----------------------------------
# Dataset Health
# ----------------------------------

st.header("✅ Dataset Health")

health = []

if df.isnull().sum().sum() == 0:
    health.append("✅ No missing values.")
else:
    health.append("⚠ Missing values present.")

if df.duplicated().sum() == 0:
    health.append("✅ No duplicate rows.")
else:
    health.append("⚠ Duplicate rows present.")

if len(df.columns) > 0:
    health.append("✅ Dataset loaded successfully.")

for item in health:
    st.write(item)

st.divider()

# ----------------------------------
# Final Report
# ----------------------------------

st.header("📋 Final Summary")

st.success(
    f"""
Dataset contains {df.shape[0]} rows and
{df.shape[1]} columns.

Total Missing Values:
{df.isnull().sum().sum()}

Duplicate Rows:
{df.duplicated().sum()}

Dataset inspection completed successfully.
"""
)