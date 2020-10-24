import matplotlib.pyplot as plt
import numpy as np


def stem_hist(xs: np.ndarray, show_now=True, linefmt='C0-', markerfmt='C0o') -> None:
    x, f = np.unique(xs, return_counts=True)
    f = f / f.sum()

    plt.stem(x, f, use_line_collection=True, linefmt=linefmt, markerfmt=markerfmt)
    q = max(1, x.size // 10)
    plt.xticks(x[::q])

    if show_now:
        plt.show()