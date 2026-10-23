"""Both estimators use exactly the same observations in each replicate."""
import numpy as np

def estimate(x):
    x = np.asarray(x)
    if x.ndim != 2 or x.shape[1] < 2:
        raise ValueError("Expected a matrix with >= 2 observations per row")
    return {"mean": np.mean(x, axis=1), "median": np.median(x, axis=1)}
