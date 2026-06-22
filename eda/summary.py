import pandas as pd


def dataset_summary(df):

    summary = {}

    summary["Rows"] = df.shape[0]
    summary["Columns"] = df.shape[1]

    summary["Numerical Columns"] = len(
        df.select_dtypes(include="number").columns
    )

    summary["Categorical Columns"] = len(
        df.select_dtypes(exclude="number").columns
    )

    summary["Memory Usage (KB)"] = round(
        df.memory_usage(deep=True).sum() / 1024,
        2
    )

    return summary


def get_datatypes(df):

    return pd.DataFrame({

        "Column": df.columns,

        "Data Type": df.dtypes.astype(str)

    })


def get_statistics(df):

    return df.describe(include="all").transpose()