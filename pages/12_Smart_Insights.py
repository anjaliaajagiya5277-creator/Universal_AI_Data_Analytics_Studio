import streamlit as st
import pandas as pd

# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="Smart Insights",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Smart Dataset Insights")

# --------------------------------
# Check Dataset
# --------------------------------

if "df" not in st.session_state:
    st.warning("Please upload a dataset first.")
    st.stop()

df = st.session_state["df"]

# --------------------------------
# Basic Metrics
# --------------------------------

st.subheader("📊 Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", df.shape[0])
col2.metric("Columns", df.shape[1])
col3.metric("Missing Values", df.isnull().sum().sum())
col4.metric("Duplicate Rows", df.duplicated().sum())

st.divider()

# --------------------------------
# Numeric Columns
# --------------------------------

numeric_cols = df.select_dtypes(
    include="number"
).columns.tolist()

categorical_cols = df.select_dtypes(
    exclude="number"
).columns.tolist()

# --------------------------------
# Numeric Insights
# --------------------------------

st.subheader("🔢 Numeric Insights")

if numeric_cols:

    for col in numeric_cols:

        st.write(f"### {col}")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Mean",
            round(df[col].mean(),2)
        )

        c2.metric(
            "Median",
            round(df[col].median(),2)
        )

        c3.metric(
            "Maximum",
            round(df[col].max(),2)
        )

else:

    st.info("No numeric columns.")

st.divider()

# --------------------------------
# Categorical Insights
# --------------------------------

st.subheader("🔤 Categorical Insights")

if categorical_cols:

    for col in categorical_cols:

        mode = df[col].mode()

        top = mode[0] if not mode.empty else "N/A"

        st.write(
            f"{col} : Most Frequent Value → {top}"
        )

else:

    st.info("No categorical columns.")

st.divider()

# --------------------------------
# Correlation Insights
# --------------------------------

if len(numeric_cols) >= 2:

    st.subheader("🔗 Correlation Insights")

    corr = df[numeric_cols].corr()

    pairs = []

    for i in corr.columns:
        for j in corr.columns:

            if i != j:

                pairs.append({
                    "Column 1": i,
                    "Column 2": j,
                    "Correlation":
                    round(corr.loc[i,j],2)
                })

    pair_df = pd.DataFrame(pairs)

    pair_df = pair_df[
        abs(pair_df["Correlation"]) > 0.7
    ]

    pair_df = pair_df.drop_duplicates()

    if len(pair_df)==0:

        st.write(
            "No strong correlations."
        )

    else:

        st.dataframe(
            pair_df,
            use_container_width=True
        )

st.divider()

# --------------------------------
# Missing Value Insights
# --------------------------------

st.subheader("❓ Missing Value Insights")

missing = df.isnull().sum()

for col in df.columns:

    if missing[col] == 0:

        st.write(
            f"✅ {col} has no missing values."
        )

    else:

        st.write(
            f"⚠ {col} has {missing[col]} missing values."
        )

st.divider()

# --------------------------------
# Duplicate Insights
# --------------------------------

st.subheader("🔁 Duplicate Insights")

duplicates = df.duplicated().sum()

if duplicates == 0:

    st.success(
        "No duplicate rows."
    )

else:

    st.warning(
        f"{duplicates} duplicate rows found."
    )

st.divider()

# --------------------------------
# Final Dataset Health
# --------------------------------

st.subheader("🏥 Dataset Health Score")

score = 100

score -= min(
    df.isnull().sum().sum(),
    50
)

score -= min(
    duplicates,
    50
)

score = max(score,0)

st.metric(
    "Health Score",
    f"{score}/100"
)

if score > 80:

    st.success(
        "Dataset quality is excellent."
    )

elif score > 60:

    st.info(
        "Dataset quality is good."
    )

else:

    st.warning(
        "Dataset needs additional cleaning."
    )