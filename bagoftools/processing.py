import numpy as np


def batchify(xs: np.ndarray, bs: int, func: callable = None):
    """
    Batchify @xs. If @func is not None, then the emitted item is func(batch).
    """
    if not isinstance(bs, int) or not (1 <= bs <= len(xs)):
        raise ValueError(f'Batch size must be an int in [1, {xs.shape[0]}].')

    if not isinstance(xs, np.ndarray):
        xs = np.array(xs)

    if func is None:
        func = lambda x: x

    l = len(xs)
    for ndx in range(0, l, bs):
        yield func(xs[ndx:min(ndx + bs, l)])
