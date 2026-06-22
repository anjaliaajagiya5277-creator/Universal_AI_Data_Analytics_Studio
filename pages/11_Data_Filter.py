import streamlit as st
import pandas as pd

# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="Data Filter",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Data Filter & Search")

# ---------------------------------
# Check Dataset
# ---------------------------------

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"].copy()

filtered_df = df.copy()

# ---------------------------------
# Filter by Categorical Columns
# ---------------------------------

st.subheader("🔤 Categorical Filters")

categorical_cols = filtered_df.select_dtypes(
    exclude="number"
).columns.tolist()

for col in categorical_cols:

    values = filtered_df[col].dropna().unique().tolist()

    selected = st.multiselect(
        f"{col}",
        values
    )

    if selected:
        filtered_df = filtered_df[
            filtered_df[col].isin(selected)
        ]

st.divider()

# ---------------------------------
# Filter by Numeric Columns
# ---------------------------------

st.subheader("🔢 Numeric Filters")

numeric_cols = filtered_df.select_dtypes(
    include="number"
).columns.tolist()

for col in numeric_cols:

    min_val = float(filtered_df[col].min())
    max_val = float(filtered_df[col].max())

    low, high = st.slider(
        col,
        min_val,
        max_val,
        (min_val, max_val)
    )

    filtered_df = filtered_df[
        (filtered_df[col] >= low) &
        (filtered_df[col] <= high)
    ]

st.divider()

# ---------------------------------
# Search Text
# ---------------------------------

st.subheader("🔎 Search")

search = st.text_input(
    "Search value"
)

if search:

    mask = pd.Series(
        False,
        index=filtered_df.index
    )

    for col in filtered_df.columns:

        mask |= filtered_df[col].astype(str).str.contains(
            search,
            case=False,
            na=False
        )

    filtered_df = filtered_df[mask]

st.divider()

# ---------------------------------
# Metrics
# ---------------------------------

st.subheader("📊 Filter Summary")

c1, c2 = st.columns(2)

c1.metric(
    "Original Rows",
    len(df)
)

c2.metric(
    "Filtered Rows",
    len(filtered_df)
)

st.divider()

# ---------------------------------
# Display Data
# ---------------------------------

st.subheader("👀 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.divider()

# ---------------------------------
# Download
# ---------------------------------

csv = filtered_df.to_csv(
    index=False
)

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_dataset.csv",
    mime="text/csv"
)

st.success(
    "Filtering completed successfully."
)