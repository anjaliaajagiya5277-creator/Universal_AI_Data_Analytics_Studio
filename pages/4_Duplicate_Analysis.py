import streamlit as st
import pandas as pd

# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Duplicate Analysis",
    page_icon="🔁",
    layout="wide"
)

st.title("🔁 Duplicate Analysis")

# --------------------------------
# Check Dataset
# --------------------------------

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# --------------------------------
# Duplicate Count
# --------------------------------

duplicate_count = df.duplicated().sum()

st.metric(
    "Duplicate Rows",
    duplicate_count
)

st.divider()

# --------------------------------
# Duplicate Percentage
# --------------------------------

duplicate_percentage = round(
    (duplicate_count / len(df)) * 100,
    2
)

st.metric(
    "Duplicate Percentage",
    f"{duplicate_percentage}%"
)

st.divider()

# --------------------------------
# Duplicate Records
# --------------------------------

st.subheader("📋 Duplicate Records")

duplicates = df[df.duplicated()]

if duplicates.empty:
    st.success("✅ No duplicate rows found.")
else:
    st.dataframe(
        duplicates,
        use_container_width=True
    )

st.divider()

# --------------------------------
# Unique vs Duplicate
# --------------------------------

st.subheader("📊 Dataset Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Rows",
        len(df)
    )

with col2:
    st.metric(
        "Unique Rows",
        len(df) - duplicate_count
    )

with col3:
    st.metric(
        "Duplicate Rows",
        duplicate_count
    )

st.divider()

# --------------------------------
# Duplicate Columns Check
# --------------------------------

st.subheader("📌 Duplicate Information")

duplicate_columns = []

for col in df.columns:

    count = df[col].duplicated().sum()

    duplicate_columns.append({
        "Column": col,
        "Repeated Values": count
    })

duplicate_df = pd.DataFrame(
    duplicate_columns
)

st.dataframe(
    duplicate_df,
    use_container_width=True
)

st.divider()

# --------------------------------
# Summary Message
# --------------------------------

if duplicate_count == 0:

    st.success(
        "Dataset contains no duplicate rows."
    )

else:

    st.warning(
        f"Dataset contains {duplicate_count} duplicate rows."
    )

st.info(
    "Proceed to the Data Cleaning page to remove duplicate rows."
)