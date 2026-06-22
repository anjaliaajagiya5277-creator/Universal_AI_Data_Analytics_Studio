import streamlit as st
import pandas as pd

# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(
    page_title="Final Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Final Analytics Dashboard")

# ---------------------------------
# Dataset Check
# ---------------------------------

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# ---------------------------------
# KPI Section
# ---------------------------------

st.subheader("📈 Key Metrics")

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric(
    "Rows",
    df.shape[0]
)

col2.metric(
    "Columns",
    df.shape[1]
)

col3.metric(
    "Missing",
    df.isnull().sum().sum()
)

col4.metric(
    "Duplicates",
    df.duplicated().sum()
)

memory = round(
    df.memory_usage(deep=True).sum()/1024,
    2
)

col5.metric(
    "Memory KB",
    memory
)

st.divider()

# ---------------------------------
# Column Summary
# ---------------------------------

numeric = df.select_dtypes(
    include="number"
).columns.tolist()

categorical = df.select_dtypes(
    exclude="number"
).columns.tolist()

st.subheader("📋 Column Summary")

c1,c2 = st.columns(2)

c1.metric(
    "Numeric Columns",
    len(numeric)
)

c2.metric(
    "Categorical Columns",
    len(categorical)
)

st.divider()

# ---------------------------------
# Missing Summary
# ---------------------------------

st.subheader("❓ Missing Value Summary")

missing_df = pd.DataFrame({

    "Column":df.columns,

    "Missing":df.isnull().sum().values

})

st.dataframe(
    missing_df,
    use_container_width=True
)

st.divider()

# ---------------------------------
# Duplicate Summary
# ---------------------------------

st.subheader("🔁 Duplicate Summary")

duplicates = df.duplicated().sum()

if duplicates==0:

    st.success(
        "No duplicate rows."
    )

else:

    st.warning(
        f"{duplicates} duplicate rows found."
    )

st.divider()

# ---------------------------------
# Top Categories
# ---------------------------------

if len(categorical)>0:

    st.subheader(
        "🔤 Top Category Values"
    )

    for col in categorical:

        mode = df[col].mode()

        value = mode[0] if not mode.empty else "N/A"

        st.write(
            f"{col} : {value}"
        )

st.divider()

# ---------------------------------
# Correlation Matrix
# ---------------------------------

if len(numeric)>=2:

    st.subheader(
        "🔗 Correlation Matrix"
    )

    corr = df[numeric].corr()

    st.dataframe(
        corr,
        use_container_width=True
    )

st.divider()

# ---------------------------------
# Dataset Health
# ---------------------------------

st.subheader(
    "🏥 Dataset Health"
)

score = 100

score -= min(
    df.isnull().sum().sum(),
    50
)

score -= min(
    duplicates,
    50
)

score = max(
    score,
    0
)

st.metric(
    "Health Score",
    f"{score}/100"
)

if score>80:

    st.success(
        "Excellent dataset quality."
    )

elif score>60:

    st.info(
        "Good dataset quality."
    )

else:

    st.warning(
        "Dataset requires cleaning."
    )

st.divider()

# ---------------------------------
# Dataset Preview
# ---------------------------------

st.subheader(
    "👀 Dataset Preview"
)

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# ---------------------------------
# Final Summary
# ---------------------------------

st.subheader(
    "📄 Executive Summary"
)

st.info(
    f"""
Dataset contains {df.shape[0]} rows and {df.shape[1]} columns.

Missing Values : {df.isnull().sum().sum()}

Duplicate Rows : {duplicates}

Numeric Columns : {len(numeric)}

Categorical Columns : {len(categorical)}

Dataset Health Score : {score}/100
"""
)