import matplotlib.pyplot as plt


def plot_heatmap(df):

    numeric_df = df.select_dtypes(include="number")

    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(10, 6))

    image = ax.imshow(corr)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(
        corr.columns,
        rotation=90
    )

    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)

    plt.colorbar(image)

    ax.set_title("Correlation Heatmap")

    return fig