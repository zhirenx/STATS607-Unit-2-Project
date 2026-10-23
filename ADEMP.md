# ADEMP: Mean versus median under heavy tails

**Selection:** Option B, original simulation. Instructor consultation is required by the assignment; approval is not asserted here. No external dataset or paper reproduction is used.

## Aims
When estimating a symmetric population's location, how much efficiency does the sample median lose under normality, and how much does it gain under heavy tails or symmetric outliers? Hypotheses: the mean has lower MSE under normality; the median has lower MSE in the two heavy-tail conditions. A secondary aim is to verify the exact result MSE(sample mean) = 1/n for unit-variance iid observations.

## Data-generating mechanisms
Each replicate contains n independent observations X = mu + Z, with mu = 0. All three distributions have mean 0, median 0, and variance 1 before the location shift:

- Normal: Z ~ N(0,1).
- Student t: Z = T/sqrt(3), T ~ t with 3 degrees of freedom (Var(T) = 3).
- Contaminated normal: draw B ~ Bernoulli(0.05) and G ~ N(0,1) independently; Z = G(1 + 9B)/sqrt(5.95). Its variance is (0.95 + 0.05 × 100)/5.95 = 1. Outliers are symmetric and stochastic; exactly 5% in each sample is not imposed.

### Complete design matrix

| Distribution | n | Replicates | Methods |
|---|---:|---:|---|
| Normal | 20 | 10,000 | Mean, median |
| Normal | 100 | 10,000 | Mean, median |
| Normal | 500 | 10,000 | Mean, median |
| Student t3 / sqrt(3) | 20 | 10,000 | Mean, median |
| Student t3 / sqrt(3) | 100 | 10,000 | Mean, median |
| Student t3 / sqrt(3) | 500 | 10,000 | Mean, median |
| Contaminated normal / sqrt(5.95) | 20 | 10,000 | Mean, median |
| Contaminated normal / sqrt(5.95) | 100 | 10,000 | Mean, median |
| Contaminated normal / sqrt(5.95) | 500 | 10,000 | Mean, median |

Total: 90,000 independently generated datasets and 180,000 estimates. Sample sizes represent small, moderate, and larger samples. Unit variance isolates distribution shape from overall scale. The heavy-tail conditions have a denser center as a consequence of this normalization.

## Estimand
The common location mu = E(X) = population median(X) = 0. Symmetry ensures that the methods target the same quantity. This would generally fail for asymmetric distributions.

## Methods
The arithmetic sample mean and sample median (average of the two central order statistics for even n), implemented by NumPy. Both methods use the same dataset in each replicate, without tuning or distribution-specific information. No method receives the known location as an input.

## Performance measures
With errors e_r = estimate_r - mu, calculate bias = average(e), sample variance with denominator R-1, MSE = average(e²), and RMSE = sqrt(MSE). Bias MCSE is sample SD(e)/sqrt(R); MSE MCSE is sample SD(e²)/sqrt(R). Descriptive 95% Monte Carlo error bars are estimate ± 1.96 MCSE. These describe simulation uncertainty, not confidence intervals for a population parameter from a single dataset.

Compare methods using MSE(median)/MSE(mean) and paired differences d_r = e_median,r² - e_mean,r². Compute the MCSE of the average difference using SD(d)/sqrt(R), preserving the pairing. For t3 data, fourth moments do not exist, so the squared errors of the mean have infinite variance. Its empirical MSE MCSE and paired difference intervals are exploratory and have no standard finite-variance CLT guarantee. The finite MSE itself remains well defined. No coverage, hypothesis-testing power, or Type I error claims are made.

## Reproduction
Use `config.json` (master seed 5042026, 10,000 replicates, batch size 500). Each condition uses NumPy SeedSequence([master seed, fixed distribution index, n]); distribution indices are normal=0, student_t3=1, contaminated_normal=2. A condition generator draws R replicate seeds, each used to initialize a separate default_rng. Replicate streams and results are invariant to batch size and condition iteration order. Each dataset is generated once and shared across methods. Raw replicate estimates and a configuration snapshot are saved before analysis; full observation arrays are not cached. See README for exact commands and environment versions.
