---
name: conducting-meta-analyses
description: Performs meta-analysis with heterogeneity assessment, forest plot generation, and GRADE evidence grading. Use when conducting meta-analyses, assessing heterogeneity, or grading evidence quality.
tags:
  - process
  - clinical-research
metadata:
  author: casemark
  practice_areas:
    - Clinical Research
    - Biostatistics
    - Regulatory Affairs
  document_types:
    - Process Documentation
  skill_modes:
    - Process Management
---

# Conducting Meta-Analyses

## Why This Skill Exists

Meta-analysis quantitatively synthesizes results across multiple studies to produce pooled effect estimates with greater precision than any individual trial. It is the statistical engine behind systematic reviews, health technology assessments, and regulatory benefit-risk evaluations. Poorly conducted meta-analyses — using inappropriate pooling models, ignoring heterogeneity, or failing to assess publication bias — produce misleading conclusions that can harm patients and distort policy. This skill implements Cochrane Handbook methodology, PRISMA reporting standards, and GRADE evidence assessment for defensible quantitative synthesis.

---

## Checkpoint A — Intake and Scoping

### Required Intake Questions
1. Is this meta-analysis part of a registered systematic review (PROSPERO ID)?
2. What is the clinical question in PICOS format?
3. What is the primary effect measure (risk ratio, odds ratio, hazard ratio, mean difference, standardized mean difference)?
4. Are individual participant data (IPD) available, or is this an aggregate-data meta-analysis?
5. How many studies are expected to be included (impacts model choice and publication-bias assessment)?
6. Are subgroup analyses or meta-regression pre-specified?
7. Is a network meta-analysis (NMA) required for indirect comparisons?
8. What software will be used (R metafor/meta, Stata metan, RevMan, CMA)?
9. Is a GRADE Summary of Findings table required?
10. What is the intended audience (regulatory, HTA, journal publication, clinical guideline)?

### Required Source Documents
- Completed data extraction forms from the systematic review
- Risk-of-bias assessments for all included studies
- Pre-specified analysis plan (from the systematic review protocol)
- Existing meta-analyses on the same topic (for comparison and gap analysis)

---

## Step 1 — Select the Effect Measure

Choose the appropriate summary statistic based on outcome type:

### Binary Outcomes
- **Risk Ratio (RR)**: Preferred when baseline risk is stable across studies; interpretable as relative risk
- **Odds Ratio (OR)**: Required for case-control studies; approximates RR when event rates are low (<10%)
- **Risk Difference (RD)**: Absolute measure; useful for NNT calculation; but often heterogeneous across baseline risks

### Continuous Outcomes
- **Mean Difference (MD)**: When all studies use the same measurement scale
- **Standardized Mean Difference (SMD)**: When studies use different scales measuring the same construct (Cohen's d or Hedges' g with small-sample correction)

### Time-to-Event Outcomes
- **Hazard Ratio (HR)**: Preferred; requires either reported HRs or IPD reconstruction from KM curves using validated methods (Tierney et al., BMJ 2007)

### Count/Rate Data
- **Rate Ratio**: Events per person-time; use when follow-up durations differ substantially

Document the rationale for effect-measure selection in the methods section.

---

## Step 2 — Choose the Statistical Model

### Fixed-Effect Model
- Assumes all studies estimate the same true effect (common-effect assumption)
- Appropriate only when studies are clinically and methodologically homogeneous
- Weights studies by inverse variance (larger studies contribute more)
- Methods: Mantel-Haenszel (binary), inverse variance (continuous), Peto (rare events with balanced arms)

### Random-Effects Model
- Assumes study-level true effects vary around a mean (distributional assumption)
- Appropriate when heterogeneity is expected or observed
- Incorporates between-study variance (tau²) into weights
- Methods: DerSimonian-Laird (simple but biased tau² estimate), REML (restricted maximum likelihood — preferred), Paule-Mandel, Knapp-Hartung adjustment for CI calculation (recommended when <20 studies)

### Model Selection Decision
- Default to random-effects in most clinical contexts (heterogeneity is nearly always present)
- Present fixed-effect as sensitivity analysis
- When tau² estimate is zero, random-effects reduces to fixed-effect

---

## Step 3 — Assess and Quantify Heterogeneity

Heterogeneity assessment is mandatory, not optional:

1. **Cochran's Q test**: Chi-squared test for heterogeneity; low power with few studies (p < 0.10 threshold)
2. **I² statistic**: Proportion of variability due to between-study differences; 0-40% = low, 30-60% = moderate, 50-90% = substantial, 75-100% = considerable (Cochrane thresholds are overlapping deliberately)
3. **Tau² (τ²)**: Absolute between-study variance; more informative than I² for clinical interpretation
4. **Prediction interval**: Range within which the true effect in a new study would likely fall; far more informative than the confidence interval of the pooled estimate for clinical decision-making
5. **Visual inspection**: Examine forest plot for non-overlapping CIs, outliers, and directional inconsistency

When substantial heterogeneity exists, do not simply report the pooled estimate — explore and explain it.

---

## Step 4 — Explore Sources of Heterogeneity

When I² > 40% or clinical heterogeneity is suspected:

### Subgroup Analysis
- Pre-specified clinical or methodological moderators (dose, population, risk of bias, study design)
- Formal test for subgroup differences (interaction test, not separate subgroup p-values)
- Minimum 2-3 studies per subgroup for meaningful analysis

### Meta-Regression
- Requires ≥10 studies (rule of thumb: 10 studies per covariate)
- Random-effects meta-regression with Knapp-Hartung modification
- Report R² (proportion of between-study variance explained)
- Caution: ecological fallacy — study-level associations do not imply patient-level relationships

### Sensitivity Analyses
- Leave-one-out analysis (recompute removing each study sequentially)
- Restrict to low risk-of-bias studies
- Restrict to studies with adequate allocation concealment
- Compare fixed vs. random effects
- Compare effect measures (RR vs. OR)

---

## Step 5 — Assess Publication Bias

Required when ≥10 studies are included in the meta-analysis:

1. **Funnel plot**: Scatter plot of effect estimates vs. standard error; asymmetry suggests bias
2. **Egger's test**: Regression test for funnel-plot asymmetry (continuous outcomes)
3. **Peters' test**: Alternative for binary outcomes (Egger's test is biased for ORs)
4. **Trim-and-fill**: Imputes missing studies and recalculates the pooled estimate (provides sensitivity estimate)
5. **Contour-enhanced funnel plot**: Adds significance contours to distinguish publication bias from other asymmetry causes
6. **Selection models** (Copas, Vevea-Hedges): More sophisticated modeling of publication-selection process

Report the results of bias assessment even if no evidence of bias is found.

---

## Step 6 — Generate Forest Plots and Visualizations

Produce publication-quality figures:

### Forest Plot Requirements
- Individual study estimates with 95% CIs as horizontal lines/boxes
- Box size proportional to study weight
- Diamond for pooled estimate (width = 95% CI)
- Vertical line at null effect (RR=1 or MD=0)
- Numeric columns: study author/year, n per arm, effect estimate, CI, weight
- I² and Q-test results displayed below the plot
- Prediction interval overlaid on the diamond (when using random effects)

### Additional Plots
- Funnel plot (with or without contour enhancement)
- L'Abbe plot (for binary outcomes — event rates in treatment vs. control)
- Galbraith/radial plot (to identify outliers)
- Cumulative meta-analysis (chronological accumulation of evidence)
- Influence plot (leave-one-out results)

---

## Step 7 — Apply GRADE and Generate Summary of Findings

Rate the certainty of evidence for each outcome using GRADE:

| Domain | Downgrade Criteria |
|--------|--------------------|
| Risk of bias | Majority of evidence at high/unclear risk in key domains |
| Inconsistency | I² >60%, unexplained; prediction interval crosses null |
| Indirectness | Population, intervention, or outcome differs from target question |
| Imprecision | CI crosses clinical decision threshold; OIS not met |
| Publication bias | Significant asymmetry; missing studies suspected |

Upgrade criteria (for observational studies): large magnitude of effect, dose-response gradient, all plausible confounders would reduce effect.

Final rating: High, Moderate, Low, or Very Low certainty.

Present in a GRADE Summary of Findings (SoF) table with: outcome, number of studies/participants, effect estimate (95% CI), certainty rating, and plain-language interpretation.

---

## Checkpoint B — Analysis Review

1. [ ] Effect measure is appropriate for the outcome type and study designs
2. [ ] Statistical model (fixed/random) is justified and sensitivity analysis includes the alternative
3. [ ] Heterogeneity is quantified (I², tau², prediction interval) and explored
4. [ ] Subgroup analyses and meta-regression are pre-specified in the protocol
5. [ ] Publication-bias assessment is performed (for ≥10 studies)
6. [ ] Forest plots include all required elements (weights, CIs, pooled estimate, heterogeneity statistics)
7. [ ] GRADE assessment is completed for all critical outcomes
8. [ ] Sensitivity analyses are performed and reported
9. [ ] Results are interpreted in context of heterogeneity and certainty
10. [ ] Software, packages, and version numbers are documented

---

## Quality Audit

- [ ] Data extraction values entering the meta-analysis match the systematic review extraction forms
- [ ] Effect direction is consistent across all studies (verify coding of events/non-events)
- [ ] Zero-event studies are handled appropriately (continuity correction or exact methods, not excluded)
- [ ] Small-study effects are explored beyond simple funnel plots
- [ ] Prediction intervals are reported alongside confidence intervals for random-effects models
- [ ] Network meta-analysis (if conducted) assesses transitivity and coherence
- [ ] All analyses are reproducible from documented code/commands
- [ ] All [VERIFY] flags have been resolved or escalated

---

## Guidelines

1. Never pool clinically heterogeneous studies just because statistical heterogeneity is low — clinical judgment precedes statistical combination
2. Report prediction intervals for all random-effects meta-analyses — the pooled CI alone understates uncertainty
3. I² is not a measure of the amount of heterogeneity; it is the proportion of variability due to heterogeneity — interpret in context of tau²
4. Do not use fixed-effect models solely to obtain a smaller p-value when random-effects is more appropriate
5. Zero-event studies carry information and should not be silently excluded — use Peto method or exact methods
6. For rare events (<1% event rate), standard methods (Mantel-Haenszel, DerSimonian-Laird) may be unreliable — use exact methods or beta-binomial models
7. Subgroup analyses are hypothesis-generating unless pre-specified and powered — do not overinterpret
8. Cite the specific software, package, and version used (e.g., R 4.3, metafor 4.4-0)
9. Escalate to methodologist when I² >75%, when zero-event handling is complex, or when network meta-analysis shows incoherence
10. This skill produces statistical analyses — clinical interpretation of pooled effects requires domain-expert collaboration
