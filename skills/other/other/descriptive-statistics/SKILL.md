---
name: descriptive-statistics
description: Summarizing and visualizing data through measures of center, spread, shape, and position. Covers mean, median, mode, range, IQR, variance, standard deviation, percentiles, z-scores, five-number summaries, and graphical displays (histograms, box plots, stem-and-leaf, dot plots, scatter plots). Emphasizes choosing the right summary for the data's shape and scale. Use when summarizing datasets, choosing visualizations, computing summary statistics, or interpreting distributions.
type: skill
category: statistics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/statistics/descriptive-statistics/SKILL.md
superseded_by: null
---
# Descriptive Statistics

Descriptive statistics distills raw data into interpretable summaries. Before any inference, modeling, or prediction, a dataset must be described: its center, its spread, its shape, and its notable features. This skill covers the full toolkit of numerical summaries and graphical displays that turn observations into understanding.

**Agent affinity:** pearson (measures of association), gosset (small-sample summaries), george (pedagogy)

**Concept IDs:** stat-descriptive-statistics, stat-data-visualization

## Measures of Center

The center of a distribution answers "where is the typical value?"

| Measure | Definition | Best for | Sensitive to |
|---|---|---|---|
| Mean | Sum of values divided by count | Symmetric distributions | Outliers, skew |
| Median | Middle value when sorted | Skewed distributions, ordinal data | Nothing -- robust |
| Mode | Most frequent value | Categorical data, multimodal distributions | Ties, bin width |
| Trimmed mean | Mean after removing k% from each tail | Distributions with mild outliers | Choice of trim percentage |

**Decision rule.** Use the mean when the distribution is roughly symmetric with no extreme outliers. Use the median when the distribution is skewed or contains outliers. Use the mode for categorical data or when identifying the most common category matters more than a numeric center.

**When they diverge.** If mean and median differ substantially, the distribution is skewed. Mean > median indicates right skew (pulled by high values); mean < median indicates left skew. The distance between them is a rough skew indicator.

## Measures of Spread

Spread answers "how variable are the values?"

| Measure | Definition | Best for | Properties |
|---|---|---|---|
| Range | Max minus min | Quick sense of total spread | Extremely sensitive to outliers |
| IQR | Q3 minus Q1 | Robust measure alongside median | Ignores tails entirely |
| Variance | Average squared deviation from the mean | Theoretical work, ANOVA | In squared units |
| Standard deviation | Square root of variance | General-purpose spread | Same units as data |
| MAD | Median absolute deviation from the median | Robust alternative to SD | Resistant to outliers |
| Coefficient of variation | SD divided by mean, as percentage | Comparing spread across different scales | Undefined if mean = 0 |

**Sample vs. population.** Variance uses n in the denominator for a population and n-1 (Bessel's correction) for a sample. The n-1 correction produces an unbiased estimator of the population variance. Standard deviation inherits this distinction.

**Choosing a spread measure.** Pair the spread measure with the center measure: mean pairs with SD; median pairs with IQR or MAD. Mixing (e.g., reporting median and SD) obscures the summary because the measures respond to different features of the distribution.

## Shape

Shape describes the overall pattern of the distribution beyond center and spread.

### Symmetry and skewness

- **Symmetric:** Mean equals median. The distribution is a mirror image around the center. Examples: normal distribution, uniform distribution.
- **Right-skewed (positive skew):** Long right tail. Mean > median. Examples: income, home prices, reaction times.
- **Left-skewed (negative skew):** Long left tail. Mean < median. Examples: exam scores when most students do well, age at retirement.

### Kurtosis

Kurtosis measures the heaviness of the tails relative to the normal distribution.

- **Mesokurtic (kurtosis = 3):** Normal-like tails. Baseline.
- **Leptokurtic (kurtosis > 3):** Heavier tails than normal. More extreme values. Examples: financial returns, t-distributions with few degrees of freedom.
- **Platykurtic (kurtosis < 3):** Lighter tails than normal. Fewer extreme values. Examples: uniform distribution.

**Excess kurtosis** subtracts 3, so the normal distribution has excess kurtosis 0. Many software packages report excess kurtosis by default.

### Modality

- **Unimodal:** One peak. Most common shape.
- **Bimodal:** Two peaks. Often signals two subpopulations (e.g., heights of adults when sex is not separated).
- **Multimodal:** Three or more peaks. Investigate subgroups.

## Position Measures

Position answers "where does this observation fall within the distribution?"

### Percentiles and quartiles

The pth percentile is the value below which p% of the data falls.

- **Q1 (25th percentile):** One quarter of data below.
- **Q2 (50th percentile):** The median.
- **Q3 (75th percentile):** Three quarters of data below.

**Five-number summary:** Min, Q1, Median, Q3, Max. The backbone of the box plot.

### Z-scores

The z-score of an observation x is: z = (x - mean) / SD.

A z-score of +2 means the observation is 2 standard deviations above the mean. Z-scores allow comparison across different scales ("she scored 2.3 SDs above the mean on the verbal section, 1.8 SDs above on the math section").

**Chebyshev's inequality.** For any distribution, at least (1 - 1/k^2) of observations fall within k standard deviations of the mean. For k=2: at least 75%. For k=3: at least 89%.

**Empirical rule (68-95-99.7).** For approximately normal distributions: 68% within 1 SD, 95% within 2 SD, 99.7% within 3 SD.

## Graphical Displays

### Choosing the right graph

| Graph | Data type | Shows | Use when |
|---|---|---|---|
| Histogram | Quantitative | Distribution shape, center, spread | Exploring a single quantitative variable |
| Box plot | Quantitative | Five-number summary, outliers | Comparing distributions across groups |
| Dot plot | Quantitative (small n) | Individual values | Small datasets where every point matters |
| Stem-and-leaf | Quantitative (small n) | Shape + exact values | Quick classroom display |
| Bar chart | Categorical | Frequencies or proportions | Comparing category counts |
| Scatter plot | Two quantitative | Association pattern | Exploring bivariate relationships |
| Time series plot | Quantitative over time | Trends, seasonality, cycles | Temporal data |

### Histogram construction

1. Choose the number of bins. Sturges' rule: k = 1 + 3.322 * log10(n). Scott's rule: bin width = 3.49 * SD * n^(-1/3). Freedman-Diaconis: bin width = 2 * IQR * n^(-1/3).
2. Bins must be equal width, non-overlapping, and exhaustive.
3. The y-axis is frequency (count) or relative frequency (proportion). Density (relative frequency / bin width) is required when bin widths differ.

### Box plot construction

1. Draw a box from Q1 to Q3.
2. Draw a line at the median.
3. Compute fences: lower = Q1 - 1.5*IQR, upper = Q3 + 1.5*IQR.
4. Whiskers extend to the most extreme data points within the fences.
5. Observations beyond the fences are plotted individually as outliers.

**Modified box plots** use the same fences. Some implementations also mark "far outliers" beyond Q1 - 3*IQR and Q3 + 3*IQR.

## Bivariate Description

### Scatter plots and association

A scatter plot places two quantitative variables on the x and y axes. The pattern reveals:

- **Direction:** Positive (both increase together) or negative (one increases as the other decreases) or none.
- **Form:** Linear, curved, clustered, or no clear pattern.
- **Strength:** How tightly points cluster around the pattern.
- **Unusual features:** Outliers, gaps, subgroups.

### Correlation coefficient (Pearson's r)

r = (sum of (x_i - x_bar)(y_i - y_bar)) / ((n-1) * s_x * s_y)

Properties: -1 <= r <= 1. r = 1 means perfect positive linear association. r = -1 means perfect negative linear association. r = 0 means no linear association (but nonlinear association may still exist).

**Critical warnings about r:**
- r measures only linear association. A perfect parabola has r = 0.
- r is sensitive to outliers. One extreme point can inflate or deflate r dramatically.
- r does not imply causation.
- r is unitless -- it does not depend on the scale of measurement.
- Always plot the data before computing r. Anscombe's Quartet (four datasets with identical r but wildly different scatter plots) demonstrates why.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Reporting mean for skewed data | Mean is pulled by the tail, misrepresents typical value | Use median (or report both with a note about skew) |
| Interpreting correlation as causation | Association is not causation | State the association; identify confounders; reserve causal language for experiments |
| Ignoring outliers | Outliers can drive means, SDs, and correlations | Identify outliers, investigate their source, report with and without |
| Using a pie chart for many categories | Unreadable beyond ~5 categories | Use a bar chart |
| Choosing bins to force a shape | Histogram appearance depends heavily on bin count | Use a principled rule (Sturges, Scott, Freedman-Diaconis) |

## Cross-References

- **pearson agent:** Correlation coefficients, measures of association. The historical inventor of the Pearson r.
- **gosset agent:** Small-sample descriptive summaries and the care required when n is small.
- **george agent:** Teaching descriptive statistics through simulation and active learning.
- **probability-theory skill:** Theoretical distributions that descriptive statistics empirically approximates.
- **regression-modeling skill:** Bivariate description extends into regression when prediction is the goal.
- **statistical-computing skill:** Computational tools for calculating these summaries at scale.

## References

- Tukey, J. W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- Anscombe, F. J. (1973). "Graphs in statistical analysis." *The American Statistician*, 27(1), 17-21.
- Freedman, D., Pisani, R., & Purves, R. (2007). *Statistics*. 4th edition. W.W. Norton.
- Moore, D. S., McCabe, G. P., & Craig, B. A. (2021). *Introduction to the Practice of Statistics*. 10th edition. W.H. Freeman.
