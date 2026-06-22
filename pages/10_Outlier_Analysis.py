import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(
    page_title="Outlier Analysis",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Outlier Analysis")

# ---------------------------------
# Check Dataset
# ---------------------------------

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# ---------------------------------
# Numeric Columns
# ---------------------------------

numeric_cols = df.select_dtypes(
    include="number"
).columns.tolist()

if len(numeric_cols) == 0:
    st.warning("No numeric columns available.")
    st.stop()

# ---------------------------------
# Column Selection
# ---------------------------------

column = st.selectbox(
    "Select Numeric Column",
    numeric_cols
)

st.divider()

# ---------------------------------
# Statistics
# ---------------------------------

st.subheader("📊 Column Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Mean",
    round(df[column].mean(),2)
)

col2.metric(
    "Median",
    round(df[column].median(),2)
)

col3.metric(
    "Standard Deviation",
    round(df[column].std(),2)
)

st.divider()

# ---------------------------------
# IQR Method
# ---------------------------------

Q1 = df[column].quantile(0.25)
Q3 = df[column].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[
    (df[column] < lower) |
    (df[column] > upper)
]

# ---------------------------------
# Metrics
# ---------------------------------

st.subheader("📈 Outlier Summary")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Values",
    len(df)
)

c2.metric(
    "Outliers",
    len(outliers)
)

c3.metric(
    "Outlier %",
    round(
        len(outliers)/len(df)*100,
        2
    )
)

st.divider()

# ---------------------------------
# Bounds
# ---------------------------------

st.subheader("📏 IQR Bounds")

st.write(f"Lower Bound : {lower:.2f}")
st.write(f"Upper Bound : {upper:.2f}")

st.divider()

# ---------------------------------
# Outlier Rows
# ---------------------------------

st.subheader("🚨 Outlier Records")

if len(outliers)==0:

    st.success(
        "No outliers detected."
    )

else:

    st.dataframe(
        outliers,
        use_container_width=True
    )

st.divider()

# ---------------------------------
# Box Plot
# ---------------------------------

st.subheader("📦 Box Plot")

fig, ax = plt.subplots()

ax.boxplot(
    df[column].dropna()
)

ax.set_title(column)

st.pyplot(fig)

st.divider()

# ---------------------------------
# Remove Outliers
# ---------------------------------

st.subheader("🧹 Remove Outliers")

if st.button(
    "Remove Outliers"
):

    clean_df = df[
        (df[column] >= lower) &
        (df[column] <= upper)
    ]

    st.session_state["df"] = clean_df

    st.success(
        f"{len(df)-len(clean_df)} outliers removed."
    )

    st.dataframe(
        clean_df,
        use_container_width=True
    )