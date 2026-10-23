"""Symmetric location models; all have population mean and median equal to mu."""
import numpy as np

DISTRIBUTIONS = ("normal", "student_t3", "contaminated_normal")

def generate(rng, distribution, n, replicates, mu=0.0):
    if distribution not in DISTRIBUTIONS:
        raise ValueError(f"Unknown distribution: {distribution}")
    if n < 2 or replicates < 1:
        raise ValueError("Require n >= 2 and replicates >= 1")
    shape = (replicates, n)
    if distribution == "normal":
        x = rng.normal(size=shape)
    elif distribution == "student_t3":
        x = rng.standard_t(df=3, size=shape) / np.sqrt(3)
    else:
        # Same population variance (1) as the other models.
        scale = np.where(rng.random(shape) < 0.05, 10.0, 1.0)
        x = rng.normal(size=shape) * scale / np.sqrt(5.95)
    return x + mu
