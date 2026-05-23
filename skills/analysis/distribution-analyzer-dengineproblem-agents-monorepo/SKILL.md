---
name: distribution-analyzer
description: Эксперт анализа распределений. Используй для statistical distributions, data analysis и hypothesis testing.
---

# Distribution Analyzer Expert

Эксперт по анализу статистических распределений.

## Core Principles

### Exploratory Data Analysis
- Начинайте с визуализации (histograms, Q-Q plots)
- Descriptive statistics (mean, median, std, skewness, kurtosis)
- Выявление outliers и аномалий

### Multiple Testing
- Kolmogorov-Smirnov test
- Anderson-Darling test
- Shapiro-Wilk test
- Chi-square goodness-of-fit

### Model Selection
- AIC/BIC criteria
- Cross-validation
- Residual analysis

## Distribution Families

### Continuous Distributions

```yaml
Normal (Gaussian):
  Use cases: Natural phenomena, measurement errors
  Parameters: μ (mean), σ (std)
  When: Symmetric, additive processes
  Test: Shapiro-Wilk

Log-Normal:
  Use cases: Income, stock prices, file sizes
  Parameters: μ, σ (of log)
  When: Multiplicative processes, positive skew
  Test: Transform and test normality

Exponential:
  Use cases: Time between events, failure times
  Parameters: λ (rate)
  When: Memoryless processes
  Test: K-S test

Gamma:
  Use cases: Wait times, insurance claims
  Parameters: α (shape), β (rate)
  When: Sum of exponential events

Weibull:
  Use cases: Reliability, survival analysis
  Parameters: λ (scale), k (shape)
  When: Failure time modeling

Beta:
  Use cases: Proportions, probabilities
  Parameters: α, β
  When: Bounded [0,1] data

Pareto:
  Use cases: Wealth, city sizes
  Parameters: α (shape), xm (scale)
  When: Power law, heavy tail

Student's t:
  Use cases: Small samples, heavy tails
  Parameters: ν (degrees of freedom)
  When: Normal-like but heavier tails
```

### Discrete Distributions

```yaml
Poisson:
  Use cases: Event counts, rare events
  Parameters: λ (rate)
  When: Events in fixed interval

Binomial:
  Use cases: Success/failure trials
  Parameters: n (trials), p (probability)
  When: Fixed number of independent trials

Negative Binomial:
  Use cases: Overdispersed counts
  Parameters: r, p
  When: Variance > Mean

Geometric:
  Use cases: Number of trials until success
  Parameters: p (probability)
  When: Waiting for first success
```

## Distribution Analyzer Class

```python
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional

class DistributionAnalyzer:
    """Comprehensive distribution analysis toolkit."""

    DISTRIBUTIONS = {
        'norm': stats.norm,
        'lognorm': stats.lognorm,
        'expon': stats.expon,
        'gamma': stats.gamma,
        'weibull_min': stats.weibull_min,
        'beta': stats.beta,
        'pareto': stats.pareto,
        't': stats.t
    }

    def __init__(self, data: np.ndarray):
        self.data = np.array(data)
        self.n = len(data)
        self.results = {}

    def descriptive_stats(self) -> Dict:
        """Calculate descriptive statistics."""
        return {
            'n': self.n,
            'mean': np.mean(self.data),
            'median': np.median(self.data),
            'std': np.std(self.data),
            'var': np.var(self.data),
            'min': np.min(self.data),
            'max': np.max(self.data),
            'range': np.ptp(self.data),
            'skewness': stats.skew(self.data),
            'kurtosis': stats.kurtosis(self.data),
            'q25': np.percentile(self.data, 25),
            'q50': np.percentile(self.data, 50),
            'q75': np.percentile(self.data, 75),
            'iqr': stats.iqr(self.data)
        }

    def fit_distributions(self) -> Dict:
        """Fit multiple distributions and rank by goodness-of-fit."""
        results = {}

        for name, dist in self.DISTRIBUTIONS.items():
            try:
                # Fit distribution
                params = dist.fit(self.data)

                # Calculate log-likelihood
                log_likelihood = np.sum(dist.logpdf(self.data, *params))

                # Calculate AIC and BIC
                k = len(params)
                aic = 2 * k - 2 * log_likelihood
                bic = k * np.log(self.n) - 2 * log_likelihood

                # K-S test
                ks_stat, ks_pvalue = stats.kstest(self.data, name, params)

                results[name] = {
                    'params': params,
                    'log_likelihood': log_likelihood,
                    'aic': aic,
                    'bic': bic,
                    'ks_statistic': ks_stat,
                    'ks_pvalue': ks_pvalue
                }
            except Exception as e:
                results[name] = {'error': str(e)}

        # Rank by AIC
        valid_results = {k: v for k, v in results.items() if 'aic' in v}
        ranked = sorted(valid_results.items(), key=lambda x: x[1]['aic'])

        self.results = results
        return {
            'all': results,
            'best': ranked[0] if ranked else None,
            'ranking': [(name, res['aic']) for name, res in ranked]
        }

    def test_normality(self) -> Dict:
        """Comprehensive normality testing."""
        results = {}

        # Shapiro-Wilk (best for n < 5000)
        if self.n < 5000:
            stat, pvalue = stats.shapiro(self.data)
            results['shapiro_wilk'] = {
                'statistic': stat,
                'pvalue': pvalue,
                'is_normal': pvalue > 0.05
            }

        # D'Agostino-Pearson
        if self.n >= 20:
            stat, pvalue = stats.normaltest(self.data)
            results['dagostino_pearson'] = {
                'statistic': stat,
                'pvalue': pvalue,
                'is_normal': pvalue > 0.05
            }

        # Anderson-Darling
        result = stats.anderson(self.data, dist='norm')
        results['anderson_darling'] = {
            'statistic': result.statistic,
            'critical_values': dict(zip(
                [f'{cv}%' for cv in result.significance_level],
                result.critical_values
            )),
            'is_normal': result.statistic < result.critical_values[2]  # 5%
        }

        # Kolmogorov-Smirnov
        stat, pvalue = stats.kstest(
            self.data, 'norm',
            args=(np.mean(self.data), np.std(self.data))
        )
        results['kolmogorov_smirnov'] = {
            'statistic': stat,
            'pvalue': pvalue,
            'is_normal': pvalue > 0.05
        }

        return results

    def detect_outliers(self, method: str = 'iqr') -> Dict:
        """Detect outliers using various methods."""
        results = {'method': method}

        if method == 'iqr':
            q1, q3 = np.percentile(self.data, [25, 75])
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = self.data[(self.data < lower) | (self.data > upper)]
            results.update({
                'lower_bound': lower,
                'upper_bound': upper,
                'outliers': outliers,
                'n_outliers': len(outliers),
                'outlier_percentage': len(outliers) / self.n * 100
            })

        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(self.data))
            threshold = 3
            outliers = self.data[z_scores > threshold]
            results.update({
                'threshold': threshold,
                'outliers': outliers,
                'n_outliers': len(outliers),
                'outlier_percentage': len(outliers) / self.n * 100
            })

        elif method == 'mad':
            median = np.median(self.data)
            mad = np.median(np.abs(self.data - median))
            threshold = 3.5
            modified_z = 0.6745 * (self.data - median) / mad
            outliers = self.data[np.abs(modified_z) > threshold]
            results.update({
                'median': median,
                'mad': mad,
                'outliers': outliers,
                'n_outliers': len(outliers),
                'outlier_percentage': len(outliers) / self.n * 100
            })

        return results

    def plot_analysis(self, figsize: Tuple = (15, 10)):
        """Generate comprehensive diagnostic plots."""
        fig, axes = plt.subplots(2, 3, figsize=figsize)

        # Histogram with KDE
        axes[0, 0].hist(self.data, bins='auto', density=True, alpha=0.7)
        kde_x = np.linspace(self.data.min(), self.data.max(), 100)
        kde = stats.gaussian_kde(self.data)
        axes[0, 0].plot(kde_x, kde(kde_x), 'r-', lw=2)
        axes[0, 0].set_title('Histogram with KDE')

        # Q-Q Plot (Normal)
        stats.probplot(self.data, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title('Q-Q Plot (Normal)')

        # Box Plot
        axes[0, 2].boxplot(self.data, vert=True)
        axes[0, 2].set_title('Box Plot')

        # ECDF
        sorted_data = np.sort(self.data)
        ecdf = np.arange(1, self.n + 1) / self.n
        axes[1, 0].step(sorted_data, ecdf, where='post')
        axes[1, 0].set_title('Empirical CDF')

        # P-P Plot
        theoretical = stats.norm.cdf(sorted_data,
                                     loc=np.mean(self.data),
                                     scale=np.std(self.data))
        axes[1, 1].scatter(theoretical, ecdf, alpha=0.5)
        axes[1, 1].plot([0, 1], [0, 1], 'r--')
        axes[1, 1].set_title('P-P Plot (Normal)')

        # Violin Plot
        axes[1, 2].violinplot(self.data)
        axes[1, 2].set_title('Violin Plot')

        plt.tight_layout()
        return fig

    def bootstrap_ci(self, statistic: str = 'mean',
                     n_bootstrap: int = 10000,
                     confidence: float = 0.95) -> Dict:
        """Calculate bootstrap confidence intervals."""
        stat_func = {
            'mean': np.mean,
            'median': np.median,
            'std': np.std
        }[statistic]

        bootstrap_stats = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(self.data, size=self.n, replace=True)
            bootstrap_stats.append(stat_func(sample))

        alpha = 1 - confidence
        lower = np.percentile(bootstrap_stats, alpha / 2 * 100)
        upper = np.percentile(bootstrap_stats, (1 - alpha / 2) * 100)

        return {
            'statistic': statistic,
            'point_estimate': stat_func(self.data),
            'ci_lower': lower,
            'ci_upper': upper,
            'confidence': confidence,
            'standard_error': np.std(bootstrap_stats)
        }
```

## Usage Examples

```python
# Example usage
import numpy as np

# Generate sample data
np.random.seed(42)
data = np.random.lognormal(mean=2, sigma=0.5, size=1000)

# Create analyzer
analyzer = DistributionAnalyzer(data)

# Descriptive statistics
print("Descriptive Stats:")
print(analyzer.descriptive_stats())

# Fit distributions
print("\nDistribution Fitting:")
fit_results = analyzer.fit_distributions()
print(f"Best fit: {fit_results['best'][0]}")
print(f"AIC: {fit_results['best'][1]['aic']:.2f}")

# Test normality
print("\nNormality Tests:")
norm_results = analyzer.test_normality()
for test, result in norm_results.items():
    print(f"{test}: p-value = {result.get('pvalue', 'N/A'):.4f}")

# Detect outliers
print("\nOutlier Detection:")
outliers = analyzer.detect_outliers(method='iqr')
print(f"Found {outliers['n_outliers']} outliers ({outliers['outlier_percentage']:.1f}%)")

# Bootstrap CI
print("\nBootstrap Confidence Interval:")
ci = analyzer.bootstrap_ci('mean', confidence=0.95)
print(f"Mean: {ci['point_estimate']:.2f} [{ci['ci_lower']:.2f}, {ci['ci_upper']:.2f}]")

# Generate plots
fig = analyzer.plot_analysis()
plt.savefig('distribution_analysis.png')
```

## Distribution Selection Guide

```yaml
Symmetric data:
  - Start with Normal
  - If heavy tails: Student's t
  - If lighter tails: Consider uniform

Right-skewed data:
  - Log-normal for multiplicative
  - Gamma for waiting times
  - Weibull for reliability
  - Exponential if memoryless

Left-skewed data:
  - Reflect and fit right-skewed
  - Beta with appropriate parameters

Bounded data [0, 1]:
  - Beta distribution
  - Truncated normal if near-normal

Count data:
  - Poisson if mean ≈ variance
  - Negative binomial if overdispersed
  - Binomial for fixed trials

Heavy tails:
  - Pareto for power law
  - Student's t
  - Cauchy (extreme)
```

## Common Pitfalls

```yaml
Visual inspection alone:
  Problem: Histograms can be misleading
  Solution: Use multiple tests and Q-Q plots

Ignoring sample size:
  Problem: Tests behave differently with n
  Solution: Shapiro-Wilk for small, K-S for large

Single test reliance:
  Problem: Each test has assumptions
  Solution: Use multiple complementary tests

Overfitting:
  Problem: Complex distribution fits noise
  Solution: AIC/BIC penalize parameters

Parameter uncertainty:
  Problem: Point estimates hide uncertainty
  Solution: Bootstrap confidence intervals
```

## Лучшие практики

1. **Visualize first** — всегда начинайте с графиков
2. **Multiple tests** — не полагайтесь на один тест
3. **Sample size awareness** — выбирайте тесты по размеру выборки
4. **Domain knowledge** — учитывайте физический смысл данных
5. **Report uncertainty** — давайте confidence intervals
6. **Validate** — cross-validation для model selection
