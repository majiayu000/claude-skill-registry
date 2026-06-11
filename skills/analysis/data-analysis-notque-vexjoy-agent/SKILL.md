---
name: data-analysis
description: "Decision-first data analysis with statistical rigor gates."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
  - Task
context: fork
routing:
  triggers:
    - analyze data
    - data analysis
    - CSV
    - dataset
    - metrics
    - trend
    - cohort
    - A/B test
    - statistical
    - distribution
    - correlation
    - KPI
    - funnel
    - experiment results
    - "data insights"
    - "statistical analysis"
    - "CSV analysis"
    - "explore dataset"
  pairs_with:
    - workflow
    - codebase-analyzer
  complexity: medium
  category: analysis
---

# Data Analysis Skill

Every analysis begins with the decision being supported, works backward to the evidence required, and only then touches the data. This prevents the common failure mode where analysis produces impressive summaries that answer the wrong question. **Analysis without a decision is just arithmetic.**

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| extended pattern catalog: methodology, statistical, communication, process fixes | `preferred-patterns.md` | Loads detailed guidance from `preferred-patterns.md`. |
| writing analysis scripts: tool detection and metric computation code | `compute-examples.md` | Loads detailed guidance from `compute-examples.md`. |
| errors, error handling | `error-handling.md` | Loads detailed guidance from `error-handling.md`. |
| writing analysis-report.md per analysis type (A/B, trend, distribution) | `output-templates.md` | Loads detailed guidance from `output-templates.md`. |
| applying Phase 4 statistical gates: adequacy, fairness, correction, significance | `rigor-gates.md` | Loads detailed guidance from `rigor-gates.md`. |
| end-to-end phase walkthroughs on realistic inputs | `worked-examples.md` | Loads detailed guidance from `worked-examples.md`. |

## Instructions

### Phase 1: FRAME (Frame the decision before touching data)

**Goal**: Establish what decision this analysis supports and what evidence would change it.

Starting with data before establishing the decision context is the single most common analytical failure. The analyst finds interesting patterns and presents them, but the decision-maker cannot act because the patterns do not map to their options. Complete framing even when the user says they "just want numbers" -- numbers without decision context are not actionable.

**Step 1: Identify the decision**
- What specific decision does this analysis support?
- Who is the decision-maker?
- What are their options? (Option A vs. Option B vs. do nothing)
- What is the current default action if no analysis is performed?

If the user does not articulate a decision, ask: "What will you do differently based on this analysis?" If the answer is "nothing" or "I just want to see the data," switch to Exploratory Mode and label all output as exploratory. Exploratory Mode still applies rigor gates but makes no causal claims.

**Step 2: Define evidence requirements**
- What evidence would favor Option A over Option B?
- What is the minimum evidence threshold for changing the default action?
- Are there deal-breakers? (e.g., "If churn exceeds 5%, we switch vendors regardless of cost")

**Step 3: Save the frame artifact**

Save `analysis-frame.md` using the template from `references/output-templates.md` (Phase Artifact Templates § analysis-frame.md).

**GATE**: Decision identified, options enumerated, evidence requirements written to file. If the user cannot articulate a decision, explicitly switch to Exploratory Mode and document this in the frame. Proceed only when gate passes.

---

### Phase 2: DEFINE (Lock metrics before loading data)

**Goal**: Define exactly what will be measured, how, and over what population. Write definitions to file before any data is loaded.

Defining metrics after seeing data enables (consciously or not) choosing definitions that produce favorable results. Locking definitions first makes the analysis auditable. Verify every metric definition is exact -- a slight change in numerator or denominator can flip a conclusion.

**Step 1: Define metrics**

For each metric:
- **Name**: Clear, unambiguous label
- **Formula**: Exact computation (numerator/denominator for rates, aggregation method for summaries)
- **Population**: Who/what is included and excluded
- **Time window**: Start date, end date, granularity (daily/weekly/monthly)
- **Segments**: How data will be sliced (by region, cohort, plan tier, etc.)

**Step 2: Define comparison groups** (if applicable)

For each comparison:
- **Group A**: Definition and selection criteria
- **Group B**: Definition and selection criteria
- **Fairness check**: Are groups drawn from the same population and time window?

**Step 3: Define success criteria**
- What threshold constitutes a meaningful result?
- What is the minimum sample size per segment?
- Is this a one-tailed or two-tailed question?

**Step 4: Save definitions artifact**

Save `metric-definitions.md` using the template from `references/output-templates.md` (Phase Artifact Templates § metric-definitions.md).

**GATE**: All metrics defined with formulas and populations. Definitions saved to file. If this is a comparison analysis, fairness checks documented. Proceed only when gate passes.

**Immutability rule**: Once Phase 3 begins, these definitions are locked. If the data reveals that a definition is unworkable, return to Phase 2, update the definition, and document the change and its reason in the artifact. Document every adjustment -- silent definition changes are p-hacking by another name.

---

### Phase 3: EXTRACT (Load data. Assess quality. No interpretation.)

**Goal**: Load the data, profile its quality, and determine whether it is adequate for the planned analysis. Keep interpretation out of this phase.

Combining loading and interpretation causes confirmation bias. Extracting first forces you to confront data quality issues (missing values, unexpected distributions, date gaps) before they silently distort your conclusions.

**Step 1: Detect available tools**

See `references/compute-examples.md` for tool detection code. If pandas is unavailable, fall back to `csv.DictReader` + `statistics` module.

**Step 2: Load and inspect data**

Profile the dataset:
- Row count, column names and inferred types
- Missing value count per column (absolute and percentage)
- Date range (if temporal data)
- Unique value counts for categorical columns
- Basic distribution stats for numeric columns (min, max, mean, median, stdev)

**Step 3: Assess data quality**

Apply the Sample Adequacy gate (see `references/rigor-gates.md` Gate 1). Check actual numbers against these minimums:

| Check | Minimum | Action if Failed |
|-------|---------|------------------|
| Row count vs. population | Report sample fraction | State "N of M" and warn if <5% coverage |
| Time window completeness | No gaps >10% of window | Identify gaps, adjust window or note limitation |
| Segment minimums | 30+ observations per segment | Merge small segments or exclude with disclosure |
| Missing value rate | <20% per critical column | Impute with disclosure or exclude column |

**Step 4: Save quality report**

Save `data-quality-report.md` using the template from `references/output-templates.md` (Phase Artifact Templates § data-quality-report.md).

**GATE**: Data loaded, quality report saved, all four adequacy checks assessed. If data quality fails, document which analyses are affected and whether remediation is possible. Proceed only when gate passes or failures are documented as limitations.

---

### Phase 4: ANALYZE (Compute metrics. Apply rigor gates.)

**Goal**: Compute metrics per the locked definitions from Phase 2, applying statistical rigor gates at every step. Report confidence intervals, not point estimates -- "3-7% lift" is useful; "5% lift" is misleading because it implies false precision.

**Step 1: Compute primary metrics**

Calculate each metric defined in Phase 2 using the exact formula specified. See `references/compute-examples.md` for stdlib and pandas computation patterns including Wilson score confidence intervals.

**Step 2: Apply Comparison Fairness gate** (if comparing groups)

Before interpreting any group comparison, verify (see `references/rigor-gates.md` Gate 2):
- Same time window for all groups
- Same population definition for all groups
- Known confounders identified and documented
- Survivorship bias checked

**Step 3: Apply Multiple Testing Correction** (if testing multiple hypotheses)

See `references/rigor-gates.md` Gate 3 and `references/compute-examples.md` for the correction table. Report all segments tested -- if you test 10 segments, one will likely show significance by chance.

**Step 4: Apply Practical Significance gate**

See `references/rigor-gates.md` Gate 4:
- Report effect size alongside statistical significance
- Report confidence intervals, not just point estimates
- Assess whether the effect exceeds the minimum actionable threshold from Phase 2
- Provide base rate context: "from 2.1% to 2.3%" not just "+10% lift"

**Step 5: Save analysis results**

Save `analysis-results.md` using the template from `references/output-templates.md` (Phase Artifact Templates § analysis-results.md).

**GATE**: All defined metrics computed. Rigor gates applied and results documented. Violations either remediated or recorded as limitations. Proceed only when gate passes.

---

### Phase 5: CONCLUDE (Lead with insights. Return to the decision.)

**Goal**: Translate analytical results into a decision-oriented report. Lead with what the data says about the decision, not how you computed it -- the decision-maker reads Phase 5; the auditor reads Phases 2-4. Methodology belongs in the appendix.

**Step 1: State the headline finding**

One sentence that directly addresses the decision from Phase 1:
- "The data supports Option A: churn in the test group is 2.3% lower (95% CI: 1.1-3.5%) than control, exceeding the 1% threshold for switching."
- "The data is inconclusive: while conversion improved by 0.8%, the confidence interval (-0.2% to 1.8%) includes zero."
- "The data supports neither option: both segments show identical retention within measurement error."

**Step 2: Present supporting evidence**

Summarize the key metrics that support the headline, in order of importance:
1. Primary metric with confidence interval
2. Secondary metrics that reinforce or qualify
3. Segment breakdowns if they reveal important variation

**Step 3: State limitations explicitly**

If confidence intervals are wide, that IS the finding (the data is insufficient to support a decision), not a formatting problem to hide by reporting only the point estimate.

**Step 4: Return to the decision**

Explicitly map findings back to the decision frame:
- Does the evidence meet the minimum threshold from Phase 1?
- Are there deal-breakers triggered?
- What is the recommended action, with stated confidence?
- What additional data would increase confidence?

**Step 5: Save final report**

Save `analysis-report.md` using the template from `references/output-templates.md` (Phase Artifact Templates § analysis-report.md).

**GATE**: Report saved with headline finding, limitations, and explicit recommendation tied back to the decision. All artifact files referenced. Analysis complete.

---

## Reference Loading

| Signal | Load |
|--------|------|
| Phase 3 or 4 -- computing metrics, applying gates | `references/rigor-gates.md` |
| Phase 3 or 4 -- Python code for tool detection, CI computation | `references/compute-examples.md` |
| Any phase -- saving an artifact file | `references/output-templates.md` |
| Working examples of the full 5-phase flow | `references/worked-examples.md` |
| Data parse failure, segment size issue, definition revision | `references/error-handling.md` |
| Failure mode recognition (p-hacking, survivorship bias, etc.) | `references/preferred-patterns.md` |

---

## References

- **Rigor Gates**: `references/rigor-gates.md` - Detailed statistical gate documentation with examples
- **Output Templates**: `references/output-templates.md` - Phase artifact templates and analysis type templates (A/B test, trend, distribution, cohort)
- **Compute Examples**: `references/compute-examples.md` - Python computation patterns for extraction and analysis
- **Worked Examples**: `references/worked-examples.md` - Three end-to-end examples (A/B test, trend, distribution)
- **Error Handling**: `references/error-handling.md` - Error recovery procedures and blocker criteria
- **Failure modes**: `references/preferred-patterns.md` - Extended pattern catalog with code examples
