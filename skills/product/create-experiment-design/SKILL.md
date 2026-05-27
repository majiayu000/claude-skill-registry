---
name: create-experiment-design
description: Design a rigorous A/B test or experiment when the user asks to create an experiment, design an A/B test, or validate a hypothesis
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[hypothesis or feature to test]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: experiment, ab-test, design
---

# Create Experiment Design

## Overview

Design A/B tests and experiments with scientific rigor. Includes a falsifiable hypothesis, pre-registered analysis plan, sample size calculation, guardrail metrics, and clear decision criteria to prevent p-hacking and HARKing.

## Workflow

1. **Read product context** — Scan `.chalk/docs/product/` for the product profile, relevant PRDs, and any existing experiment docs. Check for a metrics framework that defines standard metrics and their baseline values.

2. **Define the hypothesis** — Parse `$ARGUMENTS` and work with the user to formulate a hypothesis in the format: "If we [change], then [primary metric] will [direction] by [minimum detectable effect], because [rationale]." The hypothesis must be falsifiable.

3. **Select metrics** — Define:
   - **Primary metric**: The single metric that determines success or failure. Must be measurable within the experiment duration.
   - **Secondary metrics**: Additional metrics to monitor for deeper understanding. These do not determine the outcome.
   - **Guardrail metrics**: Metrics that must NOT degrade (e.g., error rate, page load time, support ticket volume). If a guardrail is breached, the experiment is stopped regardless of the primary metric.

4. **Calculate sample size** — Based on: baseline conversion rate, minimum detectable effect (MDE), statistical significance level (default: 95%), statistical power (default: 80%). State the required sample size per variant.

5. **Estimate duration** — Based on current traffic or user volume, estimate how many days or weeks the experiment needs to run to reach the required sample size. Flag if the duration is impractically long and suggest adjusting the MDE.

6. **Design the variants** — Describe the control and treatment(s). Each variant must differ in exactly one variable to isolate causation. If multiple changes are bundled, note the confounding risk.

7. **Pre-register the analysis plan** — Document before the experiment starts: statistical test to use (e.g., chi-squared, t-test, Mann-Whitney), one-tailed vs. two-tailed, how to handle multiple comparisons (Bonferroni correction), and when to check results (no peeking before reaching sample size).

8. **Define decision criteria** — State explicitly: what outcome leads to ship, iterate, or kill. Include the scenario where the result is inconclusive (effect size smaller than MDE).

9. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. Use `highest + 1`.

10. **Write the experiment doc** — Save to `.chalk/docs/product/<n>_experiment_<name>.md`.

## Output

- **File**: `.chalk/docs/product/<n>_experiment_<name>.md`
- **Format**: Markdown with clearly labeled sections
- **Key sections**: Hypothesis, Primary Metric, Secondary Metrics, Guardrail Metrics, Sample Size Calculation, Duration Estimate, Variant Descriptions, Analysis Plan (pre-registered), Decision Criteria, Risks and Mitigations

## Anti-patterns

- **No pre-registered analysis plan** — Choosing the statistical test after seeing the data is p-hacking. The analysis plan must be written before the experiment starts.
- **Peeking at results** — Checking results daily and stopping when p < 0.05 inflates false positive rates dramatically. Commit to the sample size and do not check early without a sequential testing correction.
- **Too many metrics** — Testing 20 metrics guarantees at least one will be "significant" by chance. One primary metric determines the outcome. Everything else is exploratory.
- **Bundling changes** — Testing a new UI, new copy, and new pricing simultaneously makes it impossible to know which change drove the result. Isolate variables.
- **Missing guardrails** — An experiment that increases conversion by 5% but doubles error rates is not a success. Always define guardrail metrics.
- **Ignoring practical significance** — A statistically significant 0.1% improvement may not be worth the engineering cost. Define the minimum effect size that justifies shipping.
