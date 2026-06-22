import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Upload Dataset",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Dataset")
st.write("Upload a CSV or Excel file to begin data cleaning and visualization.")

st.markdown("---")

# -----------------------------
# File Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

# -----------------------------
# Process File
# -----------------------------
if uploaded_file is not None:

    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        # Store dataset
        st.session_state["df"] = df

        st.success("✅ Dataset uploaded successfully!")

        st.markdown("---")

        # -----------------------------
        # Dataset Metrics
        # -----------------------------
        st.subheader("📊 Dataset Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())

        with col4:
            memory = round(df.memory_usage(deep=True).sum() / 1024, 2)
            st.metric("Memory (KB)", memory)

        st.markdown("---")

        # -----------------------------
        # Data Types
        # -----------------------------
        st.subheader("📋 Column Information")

        info_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        st.dataframe(
            info_df,
            use_container_width=True
        )

        st.markdown("---")

        # -----------------------------
        # Dataset Preview
        # -----------------------------
        st.subheader("👀 Dataset Preview")

        st.dataframe(
            df,
            use_container_width=True
        )
        st.markdown("---")

        # -----------------------------
        # Dataset Shape
        # -----------------------------
        st.subheader("📐 Dataset Shape")

        st.write(f"**Rows :** {df.shape[0]}")
        st.write(f"**Columns :** {df.shape[1]}")

        st.markdown("---")

        # -----------------------------
        # Missing Values
        # -----------------------------
        st.subheader("❓ Missing Values")

        missing_df = pd.DataFrame({
            "Column": df.columns,
            "Missing Values": df.isnull().sum().values
        })

        st.dataframe(
            missing_df,
            use_container_width=True
        )

        st.markdown("---")

        # -----------------------------
        # Duplicate Rows
        # -----------------------------
        st.subheader("🔁 Duplicate Rows")

        duplicates = df.duplicated().sum()

        st.write(f"Duplicate Rows : **{duplicates}**")

        st.markdown("---")

        # -----------------------------
        # Download Original Dataset
        # -----------------------------
        csv = df.to_csv(index=False)

        st.download_button(
            label="📥 Download Original Dataset",
            data=csv,
            file_name="original_dataset.csv",
            mime="text/csv"
        )

        st.success("👉 Dataset is ready for Data Cleaning.")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("📂 Please upload a dataset to continue.")