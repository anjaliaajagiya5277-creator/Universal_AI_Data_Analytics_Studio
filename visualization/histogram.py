import matplotlib.pyplot as plt


def plot_histogram(df, column):

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        df[column].dropna(),
        bins=20
    )

    ax.set_title(f"Histogram of {column}")
    ax.set_xlabel(column)
    ax.set_ylabel("Frequency")

    return fig