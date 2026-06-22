import matplotlib.pyplot as plt


def plot_boxplot(df, column):

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.boxplot(
        df[column].dropna()
    )

    ax.set_title(
        f"Boxplot of {column}"
    )

    return fig