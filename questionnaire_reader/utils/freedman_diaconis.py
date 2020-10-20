import numpy as np
from scipy import stats


def freedman_diaconis(data) -> int:
    """
    Use Freedman Diaconis rule to compute optimal number of histogram bins.


    Parameters
    ----------
    data: np.ndarray
        One-dimensional array.
    """

    data = np.asarray(data, dtype=np.float_)
    IQR = stats.iqr(data, rng=(25, 75), scale=1.0, nan_policy="omit")
    N = data.size
    bw = (2 * IQR) / np.power(N, 1 / 3)
    datmin, datmax = data.min(), data.max()
    datrng = datmax - datmin
    return int((datrng / bw) + 1)
