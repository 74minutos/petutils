import numpy as np
import scipy.optimize
import scipy.spatial


def emd(x, y, xy_dist):
    """
    Calculates earth movers' distance between two densities x and y

    Parameters
    ----------

    x : ndarray
        1 - dimensional array of weights
    y : ndarray
        1 - dimensional array of weights
    xy_dist : ndarray
        2 - dimensional array containing distances between x and y density coordinates

    Returns
    -------

    float
        earth movers' distance
    ndarray
        moves required to move x onto y

    This implementation doesn't exploit the sparsity in the A_eq matrix.

    TODO: there's something wrong with this implementation, it passes basic
    tests but fails sometimes with real data, need to debug.

    """

    assert np.allclose(x.sum(), y.sum())
    x_dim = x.shape[0]
    y_dim = y.shape[0]

    flat_dim = x_dim * y_dim

    A_eq = np.zeros((x_dim + y_dim, flat_dim))

    # rows must emit earth equal to x
    for i in range(x_dim):
        constraint = np.zeros(xy_dist.shape)
        constraint[i] = 1.0
        A_eq[i] = constraint.flatten()

    # columns must recieve earth equal to y
    for i in range(y_dim):
        constraint = np.zeros(xy_dist.shape)
        constraint[:, i] = 1.0
        A_eq[i + x_dim] = constraint.flatten()

    c = xy_dist.flatten()

    b_eq = np.hstack([x, y])
    bounds = [(0, None)]

    res = scipy.optimize.linprog(c=c, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

    assert res["success"]

    return res["fun"], res["x"].reshape(xy_dist.shape)


def sparse_emd(x, x_points, y, y_points, p=2):
    """
    Calculates earth movers' distance between two densities x and y.

    Parameters
    ----------

    x : ndarray
        1 - dimensional array of weights
    x_points : ndarray
        (x.shape[0], n) - shaped array of points
    y : ndarray
        1 - dimensional array of weights
    y_points : ndarray
        (y.shape[0], n) - shaped array of points
    p : int
        minkowski p-norm

    Returns
    -------

    float
        earth movers' distance
    ndarray
        moves required to move x onto y

    """

    xy_dist = scipy.spatial.distance_matrix(x_points, y_points, p)

    return emd(x, y, xy_dist)