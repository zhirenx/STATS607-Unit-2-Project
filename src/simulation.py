"""Run with python -m src.simulation from the project root."""
import csv
import json
import logging
from pathlib import Path
import numpy as np
from .dgps import generate, DISTRIBUTIONS
from .methods import estimate

ROOT = Path(__file__).resolve().parents[1]

def run(config, output):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["distribution", "n", "replicate", "method", "estimate"])
        for distribution in config["distributions"]:
            d_index = DISTRIBUTIONS.index(distribution)
            for n in config["sample_sizes"]:
                # Condition-specific streams do not depend on loop order or batch size.
                rng = np.random.default_rng(np.random.SeedSequence([config["seed"], d_index, n]))
                # Each replicate has its own stream, ensuring batch-size invariance.
                seeds = rng.integers(0, 2**63, size=config["replicates"], dtype=np.int64)
                for start in range(0, config["replicates"], config["batch_size"]):
                    stop = min(start + config["batch_size"], config["replicates"])
                    x = np.concatenate([generate(np.random.default_rng(int(s)), distribution, n, 1,
                                                config["location"]) for s in seeds[start:stop]])
                    values = estimate(x)
                    for j in range(stop-start):
                        for method, estimates in values.items():
                            writer.writerow([distribution, n, start+j, method, repr(float(estimates[j]))])
                logging.info("Completed %s, n=%s (%s replicates)", distribution, n, config["replicates"])
    # Snapshot exact configuration alongside unsummarized estimates.
    output.with_suffix(".config.json").write_text(json.dumps(config, indent=2)+"\n")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    run(json.loads((ROOT / "config.json").read_text()), ROOT / "results/raw/estimates.csv")
