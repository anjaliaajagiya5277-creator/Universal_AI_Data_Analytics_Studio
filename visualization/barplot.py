import matplotlib.pyplot as plt


def plot_bar(df, column):

    counts = df[column].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        counts.index.astype(str),
        counts.values
    )

    ax.set_title(
        f"Bar Plot of {column}"
    )

    ax.set_xlabel(column)
    ax.set_ylabel("Count")

    plt.xticks(rotation=45)

    return fig