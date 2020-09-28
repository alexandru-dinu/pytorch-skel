import numpy as np


def get_batches(xs: np.ndarray, bs: int) -> list:
    ys = []
    n = xs.shape[0]

    for k in range(n // bs):
        split = xs[(k*bs):(k+1)*bs]
        ys.append(split)

    if n % bs != 0:
        split = xs[n - n%bs:]
        ys.append(split)

    return ys