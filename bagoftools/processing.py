import numpy as np


def map_batchwise(xs: np.ndarray, bs: int, func: callable) -> list:
    """
    Map a function over a batch of data and collect the results.
    """
    if not isinstance(xs, np.ndarray):
        xs = np.array(xs)

    if not isinstance(bs, int) or not (1 <= bs <= xs.shape[0]):
        raise ValueError(f'Batch size must be an int in [1, {xs.shape[0]}].')

    n = xs.shape[0]
    ys = []

    for k in range(n // bs):
        ys.append(func(xs[(k * bs):(k + 1) * bs]))

    if n % bs != 0:
        ys.append(func(xs[n - n % bs:]))

    return ys


def get_batches(xs: np.ndarray, bs: int) -> list:
    """
    Split input array in batches of given size.
    """
    return map_batchwise(xs, bs, func=lambda x: x)
