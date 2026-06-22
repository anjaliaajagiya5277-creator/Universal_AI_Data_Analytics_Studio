import pandas as pd


def missing_values(df):

    missing = pd.DataFrame({

        "Column": df.columns,

        "Missing Values": df.isnull().sum(),

        "Percentage": round(
            (df.isnull().sum() / len(df)) * 100,
            2
        )

    })

    return missing