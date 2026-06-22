import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Dataset Overview",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Dataset Overview")

# -----------------------------
# Check Dataset
# -----------------------------
if "df" not in st.session_state:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# -----------------------------
# Basic Information
# -----------------------------
st.subheader("📊 Basic Information")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())
col4.metric("Duplicate Rows", df.duplicated().sum())

st.divider()

# -----------------------------
# Dataset Shape
# -----------------------------
st.subheader("📐 Dataset Shape")

shape_df = pd.DataFrame({
    "Property": ["Rows", "Columns"],
    "Value": [df.shape[0], df.shape[1]]
})

st.dataframe(shape_df, use_container_width=True)

st.divider()

# -----------------------------
# Column Details
# -----------------------------
st.subheader("📋 Column Details")

info_df = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isnull().sum().values,
    "Unique Values": df.nunique().values
})

st.dataframe(info_df, use_container_width=True)

st.divider()

# -----------------------------
# Numeric and Categorical
# -----------------------------
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔢 Numeric Columns")
    if numeric_cols:
        st.write(numeric_cols)
    else:
        st.write("No numeric columns.")

with col2:
    st.subheader("🔤 Categorical Columns")
    if categorical_cols:
        st.write(categorical_cols)
    else:
        st.write("No categorical columns.")

st.divider()

# -----------------------------
# Statistical Summary
# -----------------------------
st.subheader("📈 Statistical Summary")

st.dataframe(
    df.describe(include="all").transpose(),
    use_container_width=True
)

st.divider()

# -----------------------------
# Dataset Preview
# -----------------------------
st.subheader("👀 Complete Dataset")

st.dataframe(
    df,
    use_container_width=True
)

st.success("✅ Dataset overview completed. Proceed to Data Cleaning.")