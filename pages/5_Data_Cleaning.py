import streamlit as st
import pandas as pd

# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="Data Cleaning",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Data Cleaning")

# ---------------------------------
# Check Dataset
# ---------------------------------

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"].copy()

# ---------------------------------
# Dataset Summary
# ---------------------------------

st.subheader("📊 Current Dataset Status")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())
col4.metric("Duplicates", df.duplicated().sum())

st.divider()

# ---------------------------------
# Remove Duplicates
# ---------------------------------

st.subheader("🔁 Duplicate Removal")

if st.button("Remove Duplicate Rows"):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    st.session_state["df"] = df

    st.success(
        f"{before-after} duplicate rows removed."
    )

st.divider()

# ---------------------------------
# Fill Numeric Missing Values
# ---------------------------------

st.subheader("🔢 Numeric Missing Values")

numeric_cols = df.select_dtypes(
    include="number"
).columns.tolist()

if numeric_cols:

    if st.button("Fill Numeric Missing Values"):

        for col in numeric_cols:
            df[col] = df[col].fillna(
                df[col].mean()
            )

        st.session_state["df"] = df

        st.success(
            "Numeric missing values filled."
        )

else:

    st.info("No numeric columns found.")

st.divider()

# ---------------------------------
# Fill Categorical Missing Values
# ---------------------------------

st.subheader("🔤 Categorical Missing Values")

categorical_cols = df.select_dtypes(
    exclude="number"
).columns.tolist()

if categorical_cols:

    if st.button(
        "Fill Categorical Missing Values"
    ):

        for col in categorical_cols:

            if not df[col].mode().empty:

                df[col] = df[col].fillna(
                    df[col].mode()[0]
                )

        st.session_state["df"] = df

        st.success(
            "Categorical missing values filled."
        )

else:

    st.info(
        "No categorical columns found."
    )

st.divider()

# ---------------------------------
# Cleaned Dataset Summary
# ---------------------------------

clean_df = st.session_state["df"]

st.subheader("📈 Cleaned Dataset")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", clean_df.shape[0])
col2.metric("Columns", clean_df.shape[1])
col3.metric(
    "Missing Values",
    clean_df.isnull().sum().sum()
)
col4.metric(
    "Duplicates",
    clean_df.duplicated().sum()
)

st.divider()

# ---------------------------------
# Preview
# ---------------------------------

st.subheader("👀 Cleaned Dataset Preview")

st.dataframe(
    clean_df,
    use_container_width=True
)

st.divider()

# ---------------------------------
# Download
# ---------------------------------

csv = clean_df.to_csv(index=False)

st.download_button(
    label="📥 Download Clean Dataset",
    data=csv,
    file_name="clean_dataset.csv",
    mime="text/csv"
)

st.success(
    "Dataset cleaned and ready for visualization."
)