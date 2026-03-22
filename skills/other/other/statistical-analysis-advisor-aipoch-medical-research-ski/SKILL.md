---
name: statistical-analysis-advisor
description: Recommend appropriate statistical tests (T-test, ANOVA, Mann-Whitney, etc.) based on data type, distribution, sample size, and research design.
license: MIT
skill-author: AIPOCH
---
# Statistical Analysis Advisor

Intelligent statistical test recommendation engine that guides users through selecting the right statistical methods for their data and research design.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py
```

## When to Use

- Choosing between parametric and non-parametric tests
- Selecting the right test for 2-group vs multi-group comparisons
- Checking statistical assumptions before analysis
- Power analysis and sample size planning

## Usage

```python
from scripts.main import StatisticalAdvisor

advisor = StatisticalAdvisor()

recommendation = advisor.recommend_test(
    data_type="continuous",
    groups=2,
    independent=True,
    distribution="normal"
)
```

## Input Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `data_type` | str | "continuous", "categorical", "ordinal" |
| `groups` | int | Number of groups/comparison levels |
| `independent` | bool | Independent or paired/related samples |
| `distribution` | str | "normal", "non-normal", "unknown" |
| `sample_size` | int | Current or planned sample size |

## Capabilities

1. **Test Selection** — T-test, ANOVA, Chi-square, Mann-Whitney, Kruskal-Wallis, Fisher's exact, and more
2. **Assumption Checking** — Normality (Shapiro-Wilk, K-S), homogeneity of variance (Levene's, Bartlett's), independence
3. **Power Analysis** — Effect size (Cohen's d, eta-squared, Cramér's V), sample size calculations, post-hoc power

## Workflow

1. Confirm objective, required inputs, and constraints before proceeding.
2. Validate request matches documented scope; stop early if unsupported assumptions are needed.
3. Run `scripts/main.py` with available inputs, or use the documented reasoning path.
4. Return structured result separating assumptions, deliverables, risks, and unresolved items.
5. On execution failure or incomplete inputs, switch to fallback path and state exactly what blocked completion.

## Fallback Template

If `scripts/main.py` cannot run (missing inputs, environment error), respond with:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : <stated goal>
Blocked by     : <exact missing input or error>
Partial result : <what can still be assessed manually>
Next step      : <minimum action to unblock>
───────────────────────────────────────
```

## Limitations

- Provides recommendations only — does not perform actual data analysis
- Cannot access raw data directly
- Complex multivariate designs may require specialized biostatistician consultation
- Bayesian alternatives not covered comprehensively

**Warning:** Statistical recommendations have significant implications for research validity. All recommendations must be verified by a qualified statistician before use in published research.

## Output Requirements

Every response must make these explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state exactly which fields are missing and request only the minimum additional information.
- If the task goes outside documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what can still be completed safely, and provide the manual fallback above.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Input Validation

This skill accepts: descriptions of research designs, data types, group structures, and sample sizes for statistical test selection and power analysis.

If the request does not involve statistical method selection — for example, asking to run a full statistical analysis on raw data, perform machine learning modeling, or interpret clinical trial results — do not proceed. Instead respond:

> "statistical-analysis-advisor is designed to recommend appropriate statistical methods based on your research design. Your request appears to be outside this scope. Please describe your data type, number of groups, and research question, or use a more appropriate tool for your task."

## Response Template

Use this fixed structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

For simple requests, compress the structure but keep assumptions and limits explicit when they affect correctness.

## References

- [Statistical Tests Guide](references/statistical_tests_guide.md)
- [Assumption Tests](references/assumption_tests.md)
- [Power Analysis Guide](references/power_analysis_guide.md)

## Prerequisites

```bash
pip install -r requirements.txt
```
