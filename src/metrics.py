"""Monte Carlo errors quantify uncertainty across independent replicates."""
import numpy as np

def summarize(estimates, truth):
    errors = np.asarray(estimates, dtype=float) - truth
    r = len(errors)
    if r < 2 or not np.all(np.isfinite(errors)):
        raise ValueError("Need at least two finite estimates")
    squared = errors ** 2
    return {"replicates": r, "bias": float(errors.mean()),
            "bias_mcse": float(errors.std(ddof=1)/np.sqrt(r)),
            "variance": float(errors.var(ddof=1)),
            "mse": float(squared.mean()),
            "mse_mcse": float(squared.std(ddof=1)/np.sqrt(r)),
            "rmse": float(np.sqrt(squared.mean()))}
