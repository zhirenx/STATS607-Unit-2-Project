# Simulation study: Mean versus median

An original (Option B) reproducible study of location estimation under normal, Student t3, and 5% contaminated normal sampling. Nine conditions, 10,000 replicates each, and two estimators.

## Setup and execution

From this directory, with Python 3.10+ and make:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
make all
make test
```

`make all` runs simulation, analysis, and figures in order. Estimated runtime: approximately 5–30 seconds on a recent laptop (hardware and initial font-cache setup affect timing). `make simulate` saves replicate estimates; `make analyze` runs simulation and summaries; `make figures` runs all three stages. These phony targets deliberately rerun prerequisites, avoiding stale results after configuration edits. To reuse existing raw results without simulation, use `python -m src.analyze` and `python -m src.figures`. `make clean` removes generated outputs, and `make all` rebuilds them. Tests use Python's built-in unittest and require no pytest installation.

## Findings

The median had 45–57% greater MSE than the mean under normality, but about 38–40% lower MSE under t3 sampling and 71–72% lower MSE under symmetric contamination. All distributions have unit variance; heavy-tail Monte Carlo error bars need caution because t3 lacks a fourth moment.

## Files

- `ADEMP.md`: full design, all nine conditions, exact DGPs, metrics, seeds, and uncertainty caveat.
- `ANALYSIS.md`: critical analysis based on the actual saved results.
- `config.json`: all experimental settings; default master seed 5042026.
- `src/`: modular generation, estimators, metrics, orchestration, analysis, plotting.
- `results/raw/estimates.csv`: 180,000 replicate-level estimates.
- `results/raw/estimates.config.json`: configuration used to generate the estimates.
- `results/raw/summary.csv`: bias, variance, MSE, RMSE, and Monte Carlo errors.
- `results/raw/comparisons.csv`: paired differences and MSE ratios.
- `results/figures/performance.png` and `.pdf`: publication figure with Monte Carlo uncertainty.
- `results/figures/diagnostic.png`: diagnostic sampling-distribution boxplots.
- `tests/`: six tests; `data/simulated/` is reserved for optional dataset caching.

Full observation arrays are generated in memory and discarded; raw estimator outputs are retained before summarization. Figures describe the default experiment; if changing the design or true location, update figure labels and captions accordingly.

## Verified environment

Python 3.14.0, NumPy 2.4.4, Matplotlib 3.10.8. `requirements-lock.txt` records these exact library versions. Six tests passed and the complete pipeline executed successfully in this environment. Small differences across library versions or platforms are possible.

## Submission

Repository: https://github.com/zhirenx/STATS607-Unit-2-Project

Submit the publicly accessible repository URL and upload `ANALYSIS.md` separately, together with `ADEMP.md` as requested. The assignment also requires instructor consultation on the Option B scope; that consultation is not asserted as completed. A ZIP archive can be an additional submission artifact if the course platform requests one, but does not replace the repository URL or separate analysis upload.
