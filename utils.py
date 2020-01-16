### utils.py
# Various utilities for running the simulations.
###

from numpy.random import RandomState
import pandas as pd

DEBUG = False

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def random_row(M, num_rows=1):
    """Returns one or more rows randomly from a matrix M.

    Arguments:
        M {np.array} -- A 2D numpy array.

    Keyword Arguments:
        num_rows {int} -- The number of rows to select (default: {1}).

    Returns:
        np.array -- A 2D numpy array containing the selected rows.
    """
    return M[RandomState().choice(M.shape[0], num_rows, replace=False)]
