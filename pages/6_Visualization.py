import streamlit as st
import pandas as pd

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dataset Dashboard")

# -------------------------
# Check Dataset
# -------------------------

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# -------------------------
# Basic Metrics
# -------------------------

st.subheader("📈 Dataset Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Rows",
    df.shape[0]
)

col2.metric(
    "Columns",
    df.shape[1]
)

col3.metric(
    "Missing Values",
    df.isnull().sum().sum()
)

col4.metric(
    "Duplicate Rows",
    df.duplicated().sum()
)

st.divider()

# -------------------------
# Data Types
# -------------------------

numeric_cols = df.select_dtypes(
    include="number"
).columns.tolist()

categorical_cols = df.select_dtypes(
    exclude="number"
).columns.tolist()

st.subheader("📋 Column Summary")

c1, c2 = st.columns(2)

with c1:

    st.metric(
        "Numeric Columns",
        len(numeric_cols)
    )

with c2:

    st.metric(
        "Categorical Columns",
        len(categorical_cols)
    )

st.divider()

# -------------------------
# Missing Values Table
# -------------------------

st.subheader("❓ Missing Values")

missing_df = pd.DataFrame({

    "Column": df.columns,

    "Missing Values": df.isnull().sum().values

})

st.dataframe(
    missing_df,
    use_container_width=True
)

st.divider()

# -------------------------
# Data Types Table
# -------------------------

st.subheader("📝 Column Information")

info_df = pd.DataFrame({

    "Column": df.columns,

    "Data Type": df.dtypes.astype(str),

    "Unique Values": df.nunique().values

})

st.dataframe(
    info_df,
    use_container_width=True
)

st.divider()

# -------------------------
# Correlation
# -------------------------

if len(numeric_cols) >= 2:

    st.subheader("🔗 Correlation Matrix")

    corr = df[numeric_cols].corr()

    st.dataframe(
        corr,
        use_container_width=True
    )

st.divider()

# -------------------------
# Dataset Health
# -------------------------

st.subheader("✅ Dataset Health Check")

health = []

if df.isnull().sum().sum() == 0:
    health.append("✅ No missing values")
else:
    health.append("⚠ Missing values present")

if df.duplicated().sum() == 0:
    health.append("✅ No duplicate rows")
else:
    health.append("⚠ Duplicate rows present")

if len(numeric_cols) > 0:
    health.append("✅ Numeric columns available")

if len(categorical_cols) > 0:
    health.append("✅ Categorical columns available")

for item in health:
    st.write(item)

st.divider()

# -------------------------
# Dataset Preview
# -------------------------

st.subheader("👀 Dataset Preview")

st.dataframe(
    df,
    use_container_width=True
)

st.success(
    "Dashboard generated successfully."
)