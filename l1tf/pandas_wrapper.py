from statsmodels.robust.scale import mad
from cvxopt import matrix, spmatrix, sin, mul, div, normal, spdiag
import pandas as pd
from l1tf import _l1_tf
import numpy as np

def l1_tf(corr, delta):
    """
    :param corr: Corrupted signal, should be a numpy array / pandas Series
    :param delta: Strength of regularization

    :return: The filtered series
    """

    m = corr.min()
    M = corr.max()
    denom = M - m
    # if denom == 0, corr is constant
    t = (corr-m) / (1 if denom == 0 else denom)

    if isinstance(corr, np.ndarray):
        values = matrix(t)
    elif isinstance(corr, pd.Series):
        values = matrix(t.values[:])
    else:
        raise ValueError("Wrong type for corr")

    values = _l1_tf(values, delta)
    values = values * (M - m) + m
    return values


def remove_outliers(t, delta, mad_factor=3):
    """
    :param t: an instance of pd.Series
    :param delta: parameter for l1tf function
    """
    filtered_t = l1_tf(t, delta)

    diff = t.values - np.asarray(filtered_t).squeeze()
    t = t.copy()
    t[np.abs(diff - np.median(diff)) > mad_factor * mad(diff)] = np.nan

    t = t.fillna(method='ffill').fillna(method='bfill')
    return t


def strip_na(s):
    """
    :param s: an instance of pd.Series

    Removes the NaN from the extremes
    """
    m = s.min()
    lmask = s.fillna(method='ffill').fillna(m-1) == m-1
    rmask = s.fillna(method='bfill').fillna(m-1) == m-1
    mask = np.logical_or(lmask, rmask)
    return s[np.logical_not(mask)]

def df_l1_tf(df, delta=3, remove_outliers=False, mad_factor=3):
    """
    Applies the l1tf function to the whole dataframe optionally removing outliers

    :param df: A pandas Dataframe
    :param delta: The delta parameter of the l1tf function
    :param remove_outliers: Whether outliers should be removed
    :param mad_factor: Strength of the outlier detection technique
    """
    l1tf_d = {}
    if remove_outliers: wo_outliers_d = {}
    ks = df.keys()

    for i, k in enumerate(ks):
        if i % 50 == 0: print i, 'of', len(ks)
        t = strip_na(df[k])

        if remove_outliers:
            t = remove_outliers(t, delta, mad_factor)
            wo_outliers_d[k] = t
        filtered_t = l1_tf(t, delta)

        s = pd.Series(filtered_t, index=t.index, name=k)
        l1tf_d[k] = s

    if remove_outliers:
        return pd.DataFrame(l1tf_d), pd.DataFrame(wo_outliers_d)
    else:
        return pd.DataFrame(l1tf_d)


