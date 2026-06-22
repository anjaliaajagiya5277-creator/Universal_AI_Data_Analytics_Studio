import pandas as pd


def duplicate_rows(df):

    total_duplicates = df.duplicated().sum()

    duplicate_data = df[df.duplicated()]

    return total_duplicates, duplicate_data