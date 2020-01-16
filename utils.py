## Utilities for running the simulations

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


#https://stackoverflow.com/questions/29129095/save-additional-attributes-in-pandas-dataframe
def h5store(path, df, **kwargs):
    """Store simulation data with given metadata (e.g. density, no. of iterations etc.). Based on https://stackoverflow.com/questions/29129095/save-additional-attributes-in-pandas-dataframe.

    Arguments:
        path {str} -- The path to write to
        df {dict} -- Metadata
    """
    store = pd.HDFStore(path)
    store.put('data', df)
    store.get_storer('data').attrs.metadata = kwargs
    store.close()

def h5load(path):
    """Read simulation data with metadata (e.g. density, no. of iterations etc.). Based on https://stackoverflow.com/questions/29129095/save-additional-attributes-in-pandas-dataframe.

    Arguments:
        path {str} -- The path to read from

    Returns:
        (data, metadata) -- The simulation data and metadata
    """
    with pd.HDFStore(path) as store:
        data = store['data']
        metadata = store.get_storer('data').attrs.metadata
        return data, metadata
