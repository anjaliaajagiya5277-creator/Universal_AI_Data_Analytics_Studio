import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Missing Value Analysis",
    page_icon="❓",
    layout="wide"
)

st.title("❓ Missing Value Analysis")

# -----------------------------
# Check Dataset
# -----------------------------
if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# -----------------------------
# Overall Missing Values
# -----------------------------
total_missing = df.isnull().sum().sum()

st.metric(
    "Total Missing Values",
    total_missing
)

st.divider()

# -----------------------------
# Column-wise Missing Values
# -----------------------------
st.subheader("📋 Missing Values by Column")

missing_df = pd.DataFrame({
    "Column": df.columns,
    "Missing Values": df.isnull().sum().values,
    "Missing Percentage":
    (
        df.isnull().sum()/len(df)*100
    ).round(2).values
})

st.dataframe(
    missing_df,
    use_container_width=True
)

st.divider()

# -----------------------------
# Columns with Missing Values
# -----------------------------
st.subheader("⚠ Columns Containing Missing Values")

missing_cols = missing_df[
    missing_df["Missing Values"] > 0
]

if len(missing_cols) == 0:

    st.success("No missing values found.")

else:

    st.dataframe(
        missing_cols,
        use_container_width=True
    )

st.divider()

# -----------------------------
# Numeric Columns
# -----------------------------
st.subheader("🔢 Numeric Columns")

numeric = df.select_dtypes(
    include="number"
).columns.tolist()

numeric_missing = []

for col in numeric:

    numeric_missing.append({
        "Column": col,
        "Missing Values": df[col].isnull().sum()
    })

numeric_df = pd.DataFrame(numeric_missing)

st.dataframe(
    numeric_df,
    use_container_width=True
)

st.divider()

# -----------------------------
# Categorical Columns
# -----------------------------
st.subheader("🔤 Categorical Columns")

categorical = df.select_dtypes(
    exclude="number"
).columns.tolist()

categorical_missing = []

for col in categorical:

    categorical_missing.append({
        "Column": col,
        "Missing Values": df[col].isnull().sum()
    })

categorical_df = pd.DataFrame(categorical_missing)

st.dataframe(
    categorical_df,
    use_container_width=True
)

st.divider()

# -----------------------------
# Summary
# -----------------------------
st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Columns with Missing Values",
        (missing_df["Missing Values"] > 0).sum()
    )

with col2:
    st.metric(
        "Complete Columns",
        (missing_df["Missing Values"] == 0).sum()
    )

with col3:
    st.metric(
        "Dataset Missing %",
        round(
            total_missing /
            (df.shape[0] * df.shape[1])
            * 100,
            2
        )
    )

st.success(
    "Analysis completed. Continue to Data Cleaning."
)