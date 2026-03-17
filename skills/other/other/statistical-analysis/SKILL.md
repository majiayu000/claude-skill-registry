---
name: statistical-analysis
description: Hypothesis testing, power analysis, ablation design, and multiple comparison corrections for ML experiment evaluation.
---

# Statistical Analysis for ML Experiments

## Test Selection

### Decision Table: Which Test to Use

| Scenario | Test | Assumptions | When to Use |
|----------|------|-------------|-------------|
| Compare 2 models, paired runs | Paired permutation test | None (non-parametric) | Default choice for ML |
| Compare 2 models, unpaired | Mann-Whitney U | Independent samples | Different datasets/splits |
| Compare 2 means, normal data | Paired t-test | Normality, paired | Large N (>30) runs |
| Compare >2 models | Friedman test | Paired, ordinal | Ranking across datasets |
| Post-hoc after Friedman | Nemenyi test | Same as Friedman | Pairwise model comparison |
| Compare proportions | McNemar's test | Paired binary | Classification correct/incorrect |
| Correlation of metrics | Spearman's rho | Monotonic relationship | Rank-based, robust to outliers |
| Effect of hyperparameters | ANOVA / Kruskal-Wallis | See specific test | Factorial ablation design |

### Decision Table: Confidence Interval Method

| Situation | Method | N Seeds |
|-----------|--------|---------|
| Metric approximately normal | t-interval | >= 5 |
| Unknown distribution | Bootstrap percentile | >= 10 |
| Small N, heavy tails | BCa bootstrap | >= 15 |
| Proportion (accuracy) | Wilson interval | Any |

## Bootstrap Confidence Intervals

```python
import numpy as np
from scipy import stats

def bootstrap_ci(
    data: np.ndarray,
    statistic=np.mean,
    n_bootstrap: int = 10_000,
    confidence: float = 0.95,
    method: str = "percentile",
    seed: int = 42,
) -> tuple[float, float, float]:
    """Compute bootstrap confidence interval.

    Args:
        data: 1D array of observations (e.g., accuracy per seed).
        statistic: Function to compute on each resample.
        method: 'percentile' or 'bca'.

    Returns:
        (point_estimate, lower, upper)
    """
    rng = np.random.default_rng(seed)
    observed = statistic(data)
    n = len(data)

    boot_stats = np.array([
        statistic(rng.choice(data, size=n, replace=True))
        for _ in range(n_bootstrap)
    ])

    alpha = 1 - confidence
    if method == "percentile":
        lower = np.percentile(boot_stats, 100 * alpha / 2)
        upper = np.percentile(boot_stats, 100 * (1 - alpha / 2))
    elif method == "bca":
        # Bias-correction
        z0 = stats.norm.ppf(np.mean(boot_stats < observed))
        # Acceleration (jackknife)
        jackknife = np.array([
            statistic(np.delete(data, i)) for i in range(n)
        ])
        jack_mean = jackknife.mean()
        acc = np.sum((jack_mean - jackknife) ** 3) / (
            6 * np.sum((jack_mean - jackknife) ** 2) ** 1.5
        )
        # Adjusted percentiles
        z_alpha = stats.norm.ppf(alpha / 2)
        z_1alpha = stats.norm.ppf(1 - alpha / 2)
        p_lower = stats.norm.cdf(z0 + (z0 + z_alpha) / (1 - acc * (z0 + z_alpha)))
        p_upper = stats.norm.cdf(z0 + (z0 + z_1alpha) / (1 - acc * (z0 + z_1alpha)))
        lower = np.percentile(boot_stats, 100 * p_lower)
        upper = np.percentile(boot_stats, 100 * p_upper)
    else:
        raise ValueError(f"Unknown method: {method}")

    return observed, lower, upper

# Usage
accuracies = np.array([92.1, 92.5, 91.8, 92.3, 92.0, 91.9, 92.4, 92.2, 92.6, 91.7])
point, lo, hi = bootstrap_ci(accuracies, method="bca")
print(f"Accuracy: {point:.2f} [{lo:.2f}, {hi:.2f}] (95% BCa CI)")
```

## Paired Permutation Test

```python
def paired_permutation_test(
    scores_a: np.ndarray,
    scores_b: np.ndarray,
    n_permutations: int = 100_000,
    seed: int = 42,
) -> tuple[float, float]:
    """Two-sided paired permutation test.

    Returns:
        (observed_diff, p_value) where diff = mean(a) - mean(b).
    """
    rng = np.random.default_rng(seed)
    diffs = scores_a - scores_b
    observed = np.mean(diffs)

    count = 0
    for _ in range(n_permutations):
        signs = rng.choice([-1, 1], size=len(diffs))
        perm_diff = np.mean(diffs * signs)
        if abs(perm_diff) >= abs(observed):
            count += 1

    p_value = count / n_permutations
    return observed, p_value

# Usage
model_a = np.array([92.1, 92.5, 91.8, 92.3, 92.0])
model_b = np.array([91.5, 91.8, 91.2, 91.9, 91.4])
diff, p = paired_permutation_test(model_a, model_b)
print(f"Mean diff: {diff:.2f}, p-value: {p:.4f}")
```

## Multiple Comparison Corrections

### When to Correct

| Scenario | Correct? | Method |
|----------|----------|--------|
| Single primary metric, 2 models | No | Single test suffices |
| 1 model vs 5 baselines | Yes | Holm-Bonferroni |
| 5 metrics, 1 comparison | Yes | Holm-Bonferroni |
| Exploratory ablation (many combos) | Yes | Benjamini-Hochberg (FDR) |
| Pre-registered single comparison | No | Pre-registration controls |

### Implementation

```python
from statsmodels.stats.multitest import multipletests

def correct_pvalues(
    p_values: list[float],
    method: str = "holm",  # 'bonferroni', 'holm', 'fdr_bh'
    alpha: float = 0.05,
) -> dict:
    """Apply multiple comparison correction.

    Methods:
        'bonferroni': Conservative. alpha/n per test.
        'holm': Step-down Bonferroni. Less conservative, controls FWER.
        'fdr_bh': Benjamini-Hochberg. Controls false discovery rate.
    """
    reject, corrected, _, _ = multipletests(p_values, alpha=alpha, method=method)
    return {
        "reject": reject.tolist(),
        "corrected_p": corrected.tolist(),
        "method": method,
    }

# Usage: comparing model against 4 baselines
raw_p = [0.01, 0.04, 0.03, 0.08]
result = correct_pvalues(raw_p, method="holm")
# result['reject'] -> [True, True, True, False]
# result['corrected_p'] -> [0.04, 0.08, 0.09, 0.08]
```

## Power Analysis

```python
from statsmodels.stats.power import TTestPower

def compute_required_seeds(
    effect_size: float,
    alpha: float = 0.05,
    power: float = 0.8,
) -> int:
    """How many seeds needed to detect a given effect size.

    effect_size: Cohen's d = (mean_a - mean_b) / pooled_std
        Small: 0.2, Medium: 0.5, Large: 0.8

    Typical ML scenario:
        If accuracy diff ~0.5% and std ~0.3%, d = 0.5/0.3 = 1.67 (large).
        If accuracy diff ~0.2% and std ~0.3%, d = 0.2/0.3 = 0.67 (medium).
    """
    analysis = TTestPower()
    n = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        alternative="two-sided",
    )
    return int(np.ceil(n))

# How many seeds to detect 0.5% accuracy diff with 0.3% std?
d = 0.5 / 0.3  # ~1.67
n_seeds = compute_required_seeds(d)
print(f"Need {n_seeds} seeds per model")  # ~5

# Smaller effect: 0.2% diff, 0.3% std
d_small = 0.2 / 0.3  # ~0.67
n_seeds_small = compute_required_seeds(d_small)
print(f"Need {n_seeds_small} seeds per model")  # ~20
```

## Ablation Study Design

### Reporting Ablation Results

| Component Removed | Accuracy | Delta | p-value |
|-------------------|----------|-------|---------|
| None (full model) | 92.3 +/- 0.3 | -- | -- |
| - Attention | 90.1 +/- 0.4 | -2.2 | 0.001 |
| - Residual | 91.8 +/- 0.3 | -0.5 | 0.032 |
| - Dropout | 92.1 +/- 0.3 | -0.2 | 0.241 |

## Gotchas and Anti-Patterns

### P-Hacking via Metric Selection
- Choosing the metric that gives significance after seeing results invalidates the test.
- **Fix**: Pre-register primary metric. Report all metrics regardless of significance.

### Underpowered Experiments
- 3 seeds is almost never enough. Most ML experiments need 5-20 seeds depending on variance.
- Running power analysis post-hoc to explain away non-significance is invalid.
- **Fix**: Run power analysis before experiments. Report effect sizes alongside p-values.

### Invalid Independence Assumptions
- Runs on overlapping data splits are not independent. K-fold results are correlated.
- Training with different seeds on the same data violates independence for unpaired tests.
- **Fix**: Use paired tests when runs share data. Use corrected variance estimators for k-fold.

### Misuse of T-Tests
- T-tests assume normality. With 3-5 seeds, you cannot verify this.
- T-tests on bounded metrics (accuracy in [0,1]) are technically wrong but often okay in practice for mid-range values.
- **Fix**: Default to non-parametric tests (permutation, Wilcoxon). Use t-tests only with N >= 30 or verified normality.

### Reporting Pitfalls
- "Statistically significant" without effect size is meaningless. A 0.01% improvement can be significant with enough runs.
- Confidence intervals are more informative than p-values. Always report both.
- Standard deviation vs standard error: SD measures spread of runs, SE measures uncertainty of the mean. Report SD for reproducibility, SE or CI for comparison.
