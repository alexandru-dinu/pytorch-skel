import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def stem_hist(xs: np.ndarray, show_now=True, linefmt='C0-', markerfmt='C0o') -> None:
    if not np.isclose(xs, np.round(xs)).all():
        raise ValueError("To be used only with discrete data.")

    x, f = np.unique(xs, return_counts=True)
    f = f / f.sum()

    plt.stem(x, f, use_line_collection=True, linefmt=linefmt, markerfmt=markerfmt)
    q = max(1, x.size // 10)
    plt.xticks(x[::q])

    if show_now:
        plt.show()


def heatmap(xs: np.ndarray, show_now=True, **kwargs) -> None:
    plt.figure(figsize=kwargs.get('figsize', (6, 6)))
    sns.heatmap(xs, cmap=kwargs.get('cmap', 'jet'))

    if show_now:
        plt.show()
