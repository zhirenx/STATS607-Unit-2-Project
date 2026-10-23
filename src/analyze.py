"""Summarize saved estimates, including paired method comparisons."""
import csv
import json
from collections import defaultdict
import numpy as np
from .simulation import ROOT
from .metrics import summarize

def load_raw():
    groups = defaultdict(list)
    with (ROOT / "results/raw/estimates.csv").open() as f:
        for row in csv.DictReader(f):
            groups[(row["distribution"], int(row["n"]), row["method"])].append(float(row["estimate"]))
    return {k: np.asarray(v) for k,v in groups.items()}

def write_csv(path, rows):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main():
    config = json.loads((ROOT / "results/raw/estimates.config.json").read_text())
    truth = config["location"]
    groups = load_raw()
    rows = []
    comparisons = []
    for (distribution,n,method), values in groups.items():
        rows.append(dict(distribution=distribution,n=n,method=method,**summarize(values,truth)))
    for distribution in config["distributions"]:
        for n in config["sample_sizes"]:
            a = (groups[(distribution,n,"mean")]-truth)**2
            b = (groups[(distribution,n,"median")]-truth)**2
            delta = b-a
            se = delta.std(ddof=1)/np.sqrt(len(delta))
            comparisons.append(dict(distribution=distribution,n=n,
                median_to_mean_mse_ratio=b.mean()/a.mean(),
                mse_difference=delta.mean(),difference_mcse=se,
                difference_ci_low=delta.mean()-1.96*se,difference_ci_high=delta.mean()+1.96*se))
    write_csv(ROOT / "results/raw/summary.csv",rows)
    write_csv(ROOT / "results/raw/comparisons.csv",comparisons)

if __name__ == "__main__":
    main()
