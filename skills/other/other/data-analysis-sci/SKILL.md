---
name: data-analysis-sci
description: Data collection, analysis, and interpretation for scientific inquiry. Covers measurement and units, data recording and organization, descriptive and inferential statistics, graphical representation, error analysis, drawing valid conclusions from evidence, and recognizing the limits of data. Use when collecting, analyzing, visualizing, or interpreting scientific data at any level.
type: skill
category: science
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/science/data-analysis-sci/SKILL.md
superseded_by: null
---
# Data Analysis for Science

Data analysis is where observations become evidence. Raw measurements are not conclusions -- they are the raw material from which conclusions are carefully extracted. This skill covers the full pipeline from recording measurements to drawing valid conclusions, with emphasis on honest reporting, appropriate statistical reasoning, and the discipline of knowing where the data end and interpretation begins.

**Agent affinity:** wu (precision and error analysis), mcclintock (data interpretation)

**Concept IDs:** sci-measurement-units, sci-data-tables-graphs, sci-error-analysis, sci-evidence-conclusions

## The Analysis Pipeline

| Stage | What happens | Key question |
|---|---|---|
| 1. Measurement | Quantitative observation with instruments | What is being measured, with what tool, to what precision? |
| 2. Recording | Data captured in organized form | Are the data recorded systematically and in real time? |
| 3. Description | Summary statistics and visualization | What do the data look like? |
| 4. Inference | Statistical tests | Are observed patterns real or noise? |
| 5. Conclusion | Interpretation and limitation | What can the data tell us, and what can they not? |

## Stage 1 -- Measurement

### SI Units and Dimensional Consistency

All scientific measurements use SI units (International System of Units) or units derived from them:

| Quantity | SI unit | Symbol |
|---|---|---|
| Length | meter | m |
| Mass | kilogram | kg |
| Time | second | s |
| Temperature | kelvin | K |
| Amount | mole | mol |
| Electric current | ampere | A |
| Luminous intensity | candela | cd |

**Dimensional analysis** catches errors by checking that units are consistent across an equation. If you are calculating a speed and your answer has units of kg/m, something is wrong.

### Significant Figures

The number of significant figures in a measurement reflects the precision of the instrument:

- A ruler marked in millimeters gives measurements to 3-4 significant figures (e.g., 12.3 cm).
- A digital balance reading 4.5678 g gives 5 significant figures.
- Calculations cannot increase precision. The result has the same number of significant figures as the least precise input.

**The false precision trap:** Reporting a calculated result as "3.141592654 grams" when the original measurement was "3.1 grams" creates an illusion of precision that does not exist. Wu's significant figures audit catches this.

### Accuracy vs. Precision

**Accuracy:** How close a measurement is to the true value. A scale that consistently reads 0.5 g too high is precise but inaccurate.

**Precision:** How close repeated measurements are to each other. A scale that reads 4.2, 4.3, 4.1, 4.2, 4.2 is precise. If the true value is 4.2, it is also accurate. If the true value is 5.0, it is precise but not accurate.

Both matter. Precision without accuracy is systematically wrong. Accuracy without precision is unreliable.

## Stage 2 -- Recording

### Data Tables

Data should be recorded in structured tables at the time of measurement, not reconstructed from memory afterward.

**Table conventions:**
- Independent variable in the left column
- Dependent variable(s) in subsequent columns
- Units in column headers, not in individual cells
- One measurement per row
- Include a column for notes/observations (qualitative data captured alongside quantitative)

**Example:**

| Light wavelength (nm) | Plant height day 14 (cm) | Notes |
|---|---|---|
| 450 (blue) | 8.2 | Slight yellowing on leaf tips |
| 450 (blue) | 7.9 | |
| 450 (blue) | 8.5 | |
| 650 (red) | 12.1 | |
| 650 (red) | 11.8 | |
| 650 (red) | 12.4 | Tallest plant in tray |

### Data Integrity

- **Record in real time.** Do not fill in data tables from memory.
- **Record anomalies.** If a measurement looks odd, record it and flag it. Do not silently discard it.
- **Use ink, not pencil** (or digital timestamps). The record should show what was measured, not what was expected.
- **Preserve raw data.** Processed data (means, ratios) are derived from raw data. If the raw data are lost, reanalysis is impossible.

## Stage 3 -- Description

### Descriptive Statistics

| Statistic | What it tells you | When to use |
|---|---|---|
| Mean (average) | Central tendency | Symmetric distributions |
| Median | Central tendency, robust to outliers | Skewed distributions or when outliers are present |
| Standard deviation (SD) | Spread of individual measurements | Describing variability in raw data |
| Standard error of the mean (SEM) | Precision of the estimated mean | Comparing group means |
| Range | Total spread (min to max) | Quick sense of variability |
| Interquartile range (IQR) | Middle 50% spread | Robust alternative to SD for skewed data |

**SD vs. SEM:** SD describes how variable the individual data points are. SEM describes how precisely the mean is estimated. SEM = SD / sqrt(n). As sample size increases, SEM shrinks (the mean estimate gets more precise) but SD does not (individual variability is unchanged). Use SD when describing the data. Use SEM when comparing group means.

### Graphical Representation

| Graph type | Best for | Example |
|---|---|---|
| Bar chart | Comparing means across discrete categories | Mean plant height by light color |
| Scatter plot | Showing relationship between two continuous variables | Height vs. temperature |
| Line graph | Showing change over time or continuous IV | Growth rate over 14 days |
| Histogram | Showing distribution of a single variable | Distribution of test scores |
| Box plot | Comparing distributions across groups | Height distribution by treatment |

**Error bars:** Every bar chart or line graph comparing group means should include error bars. Use SEM or 95% confidence intervals (report which one). Error bars without a label are meaningless.

**The cardinal rule of graphs:** A graph should be interpretable without reading the surrounding text. This requires: descriptive title, labeled axes with units, legend if multiple series, and error bars if applicable.

## Stage 4 -- Inference

### The Logic of Statistical Testing

Statistical inference answers: "Is the observed pattern likely to be real, or could it be explained by random chance?"

The framework:

1. State the null hypothesis (H0): there is no effect / no difference.
2. State the alternative hypothesis (H1): there is an effect / a difference.
3. Choose a significance level (alpha, typically 0.05).
4. Calculate a test statistic from the data.
5. Determine the p-value: the probability of observing data at least as extreme as the actual data, assuming H0 is true.
6. If p < alpha, reject H0. If p >= alpha, fail to reject H0.

**What "fail to reject H0" means:** It does NOT mean H0 is true. It means the data are insufficient to distinguish from H0. Absence of evidence is not evidence of absence.

### Common Tests

| Test | Use when | Example |
|---|---|---|
| t-test (independent) | Comparing means of 2 independent groups | Treatment vs. control |
| t-test (paired) | Comparing means of 2 related measurements | Before vs. after in same subjects |
| ANOVA | Comparing means of 3+ groups | Three light wavelengths |
| Chi-square | Testing association between categorical variables | Is survival related to treatment group? |
| Correlation (Pearson) | Measuring linear association between 2 continuous variables | Height vs. weight |
| Linear regression | Modeling the relationship between variables | Predicting growth rate from temperature |

### Effect Size

Statistical significance tells you whether an effect is real. Effect size tells you whether it matters. Report both.

**Cohen's d** for comparing two means: d = (mean1 - mean2) / pooled SD. Conventions: d = 0.2 (small), d = 0.5 (medium), d = 0.8 (large).

**r-squared** for regression: the proportion of variance in the DV explained by the IV. r^2 = 0.01 (1% explained, trivial), r^2 = 0.25 (25%, moderate), r^2 = 0.64 (64%, large).

## Stage 5 -- Conclusion

### Drawing Valid Conclusions

A valid conclusion:

1. **States what the data support.** "Plants grown under blue light were significantly shorter than those grown under red light (t(28) = 4.2, p < 0.001, d = 1.1)."
2. **Quantifies the evidence.** Effect size and confidence interval, not just the p-value.
3. **Acknowledges limitations.** "This study tested only two wavelengths. Intermediate wavelengths were not tested."
4. **Distinguishes correlation from causation.** Controlled experiments can support causal claims. Observational studies can establish correlation and temporal precedence but not causation.
5. **Identifies what the data do NOT show.** "The data do not address whether these effects persist beyond 14 days."

### The Absence of Evidence Clause

When an experiment finds no significant effect, the correct conclusion is NOT "there is no effect." The correct conclusion is: "The experiment did not detect an effect. This may mean there is no effect, or the effect may be too small to detect with this sample size (power = X), or the measurement may lack sufficient precision."

## Cross-References

- **wu agent:** Primary agent for precision measurement and error analysis. Draws on this skill for statistical methodology.
- **mcclintock agent:** Data interpretation in the context of experimental design.
- **feynman-s agent:** Evaluates whether data analysis methods are appropriate for the claims being made.
- **scientific-method skill:** The overarching inquiry cycle within which data analysis is one stage.
- **experimental-design-sci skill:** The design that determines what data are collected.

## References

- Moore, D. S., McCabe, G. P., & Craig, B. A. (2017). *Introduction to the Practice of Statistics*. 9th edition. W.H. Freeman.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information*. 2nd edition. Graphics Press.
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*. 2nd edition. Lawrence Erlbaum.
- Wasserstein, R. L., & Lazar, N. A. (2016). "The ASA Statement on p-Values." *The American Statistician*, 70(2), 129-133.
- Cumming, G. (2012). *Understanding the New Statistics*. Routledge.
