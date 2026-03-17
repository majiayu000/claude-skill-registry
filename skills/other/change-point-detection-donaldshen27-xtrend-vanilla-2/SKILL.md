---
name: change-point-detection
description: Use when segmenting time-series into regimes, detecting structural breaks, or constructing context sets for few-shot learning. Covers GP-CPD algorithms, Matérn kernels, likelihood ratio tests, regime identification, market state transitions, volatility regime changes, and trend reversals in financial markets.
---

# Change-Point Detection for Financial Regimes

## Purpose

Comprehensive guide for detecting regime changes in financial time-series using Gaussian Process change-point detection (GP-CPD), essential for segmenting markets into stationary periods and improving trading strategies.

## When to Use

Activate this skill when:
- Segmenting time-series into distinct regimes
- Detecting structural breaks or market transitions
- Constructing context sets for few-shot learning
- Identifying momentum crashes or reversals
- Analyzing volatility regime changes
- Building regime-aware trading models

## Core Concepts

### 1. What is a Regime Change?

A **regime change** (or change-point) is a point in time where the statistical properties of a time-series shift significantly.

**Examples in Finance:**
- **2020 COVID-19**: Transition from bull market to extreme volatility
- **2008 Financial Crisis**: Shift to high correlation and volatility
- **2022 Russia-Ukraine**: Commodity market disruption
- **Rate Hiking Cycles**: Change in interest rate sensitivity

**Why Detect Them?**
- Momentum strategies suffer during regime transitions ("momentum crashes")
- Different regimes require different trading approaches
- Context sets with clean regime segments improve few-shot learning by 11.3%

### 2. Gaussian Process Basics

A **Gaussian Process** defines a distribution over functions:

```python
# GP is fully specified by mean and covariance functions
y ~ GP(μ(x), k(x, x'))

where:
- μ(x): mean function (often 0)
- k(x, x'): covariance (kernel) function
```

**Matérn 3/2 Kernel** (recommended for financial data):
```
k(r) = σ² * (1 + √3*r/ℓ) * exp(-√3*r/ℓ)

where:
- r = |x1 - x2|
- ℓ: length_scale (how quickly correlation decays)
- σ²: variance (overall scale)
```

**Properties:**
- Once differentiable (smoother than OU process)
- Not infinitely smooth (realistic for financial data)
- Better than RBF for capturing financial dynamics

See [IMPLEMENTATION.md](IMPLEMENTATION.md#gaussian-process-kernels) for kernel implementations.

### 3. Change-Point Kernel

The **Change-Point (CP) kernel** models a transition between two GPs:

```
k_CP(x1, x2) = σ(x1) * σ(x2) * k1(x1, x2)
             + (1-σ(x1)) * (1-σ(x2)) * k2(x1, x2)

where σ(x) = sigmoid((x - t_cp) / sigma) is transition function
```

**Key Insight:**
- If there's a change-point, CP kernel fits better than single Matérn kernel
- We can detect this by comparing marginal likelihoods!

See [IMPLEMENTATION.md](IMPLEMENTATION.md#change-point-kernel) for code.

### 4. GP-CPD Algorithm

Compare two models:
1. **Matérn (M)**: No change-point, single stationary GP
2. **Change-Point (C)**: Change-point exists at time t_cp

**Detection Steps:**
1. Fit GP with Matérn kernel → compute L_M
2. Fit GP with Change-Point kernel → compute L_C (optimize t_cp)
3. Compare: `severity = L_C / (L_M + L_C)`
4. If `severity ≥ threshold`, declare change-point

**Severity Interpretation:**
- `severity = 0.5`: No evidence for change-point (models equally good)
- `severity = 0.9`: Strong evidence for change-point
- `severity = 0.95`: Very strong evidence for change-point

See [IMPLEMENTATION.md](IMPLEMENTATION.md#gp-cpd-algorithm) for full algorithm.

### 5. Segmentation Algorithm

Recursively apply GP-CPD to segment entire time-series:

**Process:**
1. Start from end of series
2. Check lookback window for change-point
3. If detected and severity ≥ threshold:
   - Mark regime from change-point to current end
   - Move before change-point and repeat
4. If not detected:
   - Move back one time step
   - Enforce max regime length constraint
5. Continue until start of series

**Constraints:**
- `min_length`: Minimum regime length (typically 5 days)
- `max_length`: Maximum regime length (21 or 63 days)

See [IMPLEMENTATION.md](IMPLEMENTATION.md#segmentation-algorithm) for implementation.

### 6. Using CPD for Context Sets

Create high-quality context sets for few-shot learning:

**Strategy:**
1. Segment each asset's history with CPD
2. Sample random regime segments as context
3. Ensure all context is before target_time (causality)

**Performance Impact** (from X-Trend paper):
- Random context: Sharpe = 2.38
- CPD context: Sharpe = 2.70
- **Improvement: +11.3%**

**Why It Works:**
- Clean regime segments are more informative
- Avoids mixing multiple market states in one context
- Better pattern matching via cross-attention
- Reduces noise in transferred knowledge

See [IMPLEMENTATION.md](IMPLEMENTATION.md#context-set-construction) for code.

## Hyperparameter Selection

### Lookback Window

```python
lookback_window (ℓ_lbw):
- 21 days (1 month): Good balance of speed and robustness
- 63 days (3 months): More robust but slower detection
- Trade-off: Shorter = faster detection, Longer = less noise
```

### Severity Threshold

```python
threshold (ν):
- 0.90: Detect most regime changes (more sensitive)
- 0.95: Detect only strong regime changes (more specific)
- 0.99: Very conservative (few, strong changes only)

Recommendation:
- For max_length = 21: Use ν = 0.90
- For max_length = 63: Use ν = 0.95
```

### Segment Length Constraints

```python
min_length = 5:  # Minimum 5 days for meaningful regime
max_length = 21 or 63:
    - 21 (1-month): Shorter, more granular regimes
    - 63 (3-month): Longer, more stable regimes
```

## Practical Usage

### Basic CPD Detection

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern

class FinancialCPD:
    def __init__(self, lookback=21, threshold=0.9):
        self.lookback = lookback
        self.threshold = threshold

    def detect_changepoint(self, prices):
        """Detect change-point in price window."""
        gp_m, L_M = self.fit_matern_gp(prices)
        t_cp, L_C = self.fit_changepoint_gp(prices)

        severity = L_C / (L_M + L_C)

        if severity >= self.threshold:
            return t_cp, severity
        else:
            return None, severity

    def segment(self, prices, min_len=5, max_len=63):
        """Segment entire time-series into regimes."""
        # See IMPLEMENTATION.md for full code
```

See [IMPLEMENTATION.md](IMPLEMENTATION.md#practical-implementation) for complete implementation.

### Visualization

```python
def visualize_regimes(prices, regimes):
    """Plot time-series with colored regime segments."""
    # See IMPLEMENTATION.md for full visualization code
```

See [IMPLEMENTATION.md](IMPLEMENTATION.md#visualization) for plotting code.

## Common Use Cases

### Use Case 1: Momentum Crash Detection

Identify regime changes that cause momentum losses:
- Market reverses rapidly (change-point detected)
- Existing position is wrong direction

See [IMPLEMENTATION.md](IMPLEMENTATION.md#momentum-crash-detection) for implementation.

### Use Case 2: Adaptive Strategy Selection

Choose trading strategy based on current regime characteristics:
- Trending regimes → Momentum strategies
- Mean-reverting regimes → Contrarian strategies
- High-volatility regimes → Risk-off strategies

See [IMPLEMENTATION.md](IMPLEMENTATION.md#adaptive-strategy-selection) for code.

## Best Practices

### DO:

✅ **Use Matérn 3/2 kernel** for financial data (better than RBF or OU)
✅ **Set reasonable lookback** (21 days is good default)
✅ **Enforce min/max lengths** to avoid trivial or excessive regimes
✅ **Validate on multiple assets** to tune threshold
✅ **Move past change-point** to avoid corrupting next regime's representation
✅ **Use for context construction** in few-shot learning

### DON'T:

❌ **Don't use RBF kernel** - too smooth for financial data
❌ **Don't set lookback too small** - noisy detections
❌ **Don't set lookback too large** - delayed detection
❌ **Don't ignore severity** - it indicates confidence
❌ **Don't allow overlapping regimes** - each point in one regime only

## Performance Impact

Based on X-Trend paper results:

**Few-Shot Learning:**
- Random context: Sharpe = 2.38
- CPD context: Sharpe = 2.70
- **Improvement: +11.3%**

**Why It Works:**
- Clean regime segments are more informative
- Avoids mixing multiple market states in one context
- Better pattern matching via cross-attention
- Reduces noise in transferred knowledge

## Implementation Checklist

When implementing GP-CPD:

- [ ] Install scikit-learn for GP support
- [ ] Implement Matérn 3/2 kernel
- [ ] Implement change-point kernel or two-GP approximation
- [ ] Calculate marginal likelihoods for both models
- [ ] Implement severity calculation: `L_C / (L_M + L_C)`
- [ ] Set appropriate threshold (0.90-0.95)
- [ ] Implement segmentation with min/max length constraints
- [ ] Add visualization for regime validation
- [ ] Integrate with context set construction
- [ ] Test on multiple assets and time periods

## Related Skills

- `few-shot-learning-finance` - Using CPD for context construction
- `financial-time-series` - Returns and momentum factors to analyze
- `x-trend-architecture` - Attending over regime segments

## Reference Files

- [IMPLEMENTATION.md](IMPLEMENTATION.md) - Complete implementations including FinancialCPD class, kernels, segmentation, context construction, use cases, and visualization

## References

- GP Change-Point Models (Saatçi, Turner, Rasmussen 2010)
- Sequential Bayesian Prediction (Garnett et al. 2010)
- Slow Momentum with Fast Reversion (Wood, Roberts, Zohren 2022)
- X-Trend: Few-Shot Learning Patterns (Wood et al. 2024)

---

**Last Updated**: Based on X-Trend paper (March 2024)
**Skill Type**: Domain Knowledge + Implementation
**Line Count**: ~290 (under 500-line rule ✅)
