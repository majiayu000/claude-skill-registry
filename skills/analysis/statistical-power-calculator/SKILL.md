---
name: statistical-power-calculator
description: Use when asked to calculate statistical power, determine sample size, or plan experiments for hypothesis testing.
---

# Statistical Power Calculator

Calculate statistical power and determine required sample sizes for hypothesis testing and experimental design.

## Purpose

Experiment planning for:
- Clinical trial design
- A/B test planning
- Research study sizing
- Survey sample size determination
- Power analysis and validation

## Features

- **Power Calculation**: Calculate statistical power for tests
- **Sample Size**: Determine required sample size for desired power
- **Effect Size**: Estimate detectable effect size
- **Multiple Tests**: t-test, proportion test, ANOVA, chi-square
- **Visualizations**: Power curves, sample size charts
- **Reports**: Detailed analysis reports with recommendations

## Quick Start

```python
from statistical_power_calculator import PowerCalculator

# Calculate required sample size
calc = PowerCalculator()
result = calc.sample_size_ttest(
    effect_size=0.5,
    alpha=0.05,
    power=0.8
)
print(f"Required n per group: {result.n_per_group}")

# Calculate power
power = calc.power_ttest(n_per_group=100, effect_size=0.5, alpha=0.05)
```

## CLI Usage

```bash
# Calculate sample size for t-test
python statistical_power_calculator.py --test ttest --effect-size 0.5 --power 0.8

# Calculate power
python statistical_power_calculator.py --test ttest --n 100 --effect-size 0.5
```
