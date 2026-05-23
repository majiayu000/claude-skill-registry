---
name: statistics
description: Geostatistics, uncertainty quantification, and time series analysis for paleoseismic research. Use for z-score analysis, Monte Carlo dating uncertainty, spatial clustering, and recurrence statistics.
triggers:
  - statistical analysis
  - uncertainty
  - geostatistics
  - monte carlo
  - z-score
  - recurrence interval
  - spatial analysis
location: user
---

# Statistics for Geoscience Research

## When to Use This Skill

Invoke when:
- Calculating z-scores or anomaly detection
- Quantifying dating uncertainty
- Analyzing spatial clustering of events
- Computing recurrence intervals
- Performing Monte Carlo simulations
- Assessing statistical significance

## Core Methods

### 1. Z-Score Analysis

Standard approach for anomaly detection in geochemical time series:

```
z = (x - μ) / σ

where:
  x = observed value
  μ = mean of reference period
  σ = standard deviation of reference period
```

**Interpretation thresholds**:
| z-score | Interpretation | Action |
|---------|---------------|--------|
| |z| < 2.0 | Within normal variation | No anomaly |
| |z| ≥ 2.0 | Significant anomaly | Investigate |
| |z| ≥ 2.5 | Strong anomaly | Likely real signal |
| |z| ≥ 3.0 | Extreme anomaly | High confidence |

**Best practices**:
- Use rolling window for mean/std (50-100 data points)
- Exclude the test point from reference calculation
- Report both positive and negative z-scores
- Consider autocorrelation in time series

### 2. Dating Uncertainty

**U-Th dating** (typical for speleothems):
- Precision: ±50-100 years for Holocene
- Report as: `1285 ± 85 yr (U-Th: 1237-1322 CE)`

**Radiocarbon dating**:
- Raw dates in 14C years BP
- Calibrate using IntCal20/SHCal20
- Report 2σ range: `830 ± 50 14C yr BP (cal. 720-940 CE)`

**Monte Carlo uncertainty propagation**:
```python
# Pseudocode for age-depth model uncertainty
for i in range(10000):
    ages_sample = sample_from_age_distributions(age_points)
    model = fit_age_depth_model(ages_sample, depths)
    interpolated_ages[i] = model.interpolate(target_depth)

uncertainty = np.percentile(interpolated_ages, [2.5, 97.5])
```

### 3. Recurrence Interval Statistics

For earthquake recurrence from event dates:

```
intervals = [t[i+1] - t[i] for i in range(len(events)-1)]
mean_recurrence = mean(intervals)
std_recurrence = std(intervals)
COV = std / mean  # Coefficient of variation
```

**Interpretation**:
- COV < 0.5: Quasi-periodic behavior
- COV ~ 1.0: Random (Poisson) process
- COV > 1.0: Clustered behavior

**MCP Tool**: `calc_recurrence` computes these statistics

### 4. Spatial Clustering Analysis

**Orphan earthquake detection**:
Identify seismicity far from mapped faults using nearest-neighbor distance.

```python
# For each earthquake, calculate distance to nearest fault
distances = [min_distance_to_fault(eq) for eq in earthquakes]

# Earthquakes > 50 km from any fault are "orphans"
orphans = [eq for eq, d in zip(earthquakes, distances) if d > 50]
```

**Kernel density estimation**:
- Use for seismicity hotspot mapping
- Bandwidth selection: Scott's rule or cross-validation

### 5. Significance Testing

**When comparing distributions**:
- Kolmogorov-Smirnov test: Compare CDFs
- Mann-Whitney U: Non-parametric comparison of medians
- Permutation tests: Distribution-free significance

**Correlation analysis**:
- Pearson r: Linear relationship (assumes normality)
- Spearman ρ: Monotonic relationship (rank-based)
- Cross-correlation: Time-lagged relationships

**P-value interpretation**:
| p-value | Interpretation |
|---------|---------------|
| p > 0.10 | Not significant |
| 0.05 < p ≤ 0.10 | Marginally significant |
| 0.01 < p ≤ 0.05 | Significant |
| p ≤ 0.01 | Highly significant |

**Warning**: With small samples (n < 20), be cautious about p-values.

### 6. Time Series Analysis

**Detrending**:
1. Remove long-term trend (linear, polynomial, or LOESS)
2. Calculate residuals for anomaly detection
3. Avoid over-fitting the trend

**Autocorrelation**:
- Check lag-1 autocorrelation before independence tests
- Effective sample size: n_eff = n × (1 - ρ) / (1 + ρ)

**Change point detection**:
- PELT algorithm for multiple change points
- Bayesian change point detection for uncertainty

## Available MCP Calculation Tools

| Tool | Function |
|------|----------|
| `calc_recurrence` | Recurrence interval from event dates |
| `calc_pga` | Peak Ground Acceleration (attenuation) |
| `calc_energy` | Seismic energy density (Wang & Manga) |
| `calc_distance` | Great-circle distance |

## Common Pitfalls

1. **Multiple comparisons**: Testing many anomalies inflates false positive rate. Apply Bonferroni correction or FDR.

2. **Small sample size**: With n < 10 events, statistical power is low. Report effect sizes, not just p-values.

3. **Circular logic**: Don't use detected anomalies to define the reference period.

4. **Ignoring uncertainty**: Always propagate dating errors through calculations.

5. **Cherry-picking**: Report ALL tests performed, not just significant ones.

## Reporting Standards

Always report:
- Sample size (n)
- Central tendency AND spread (mean ± std, or median + IQR)
- Uncertainty ranges (95% CI or 2σ)
- Effect size, not just significance
- Method used for calculation
