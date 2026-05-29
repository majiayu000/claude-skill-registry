---
name: quantitative-management
description: Use when establishing measurement programs, analyzing metrics with statistical process control, setting baselines, or implementing CMMI Level 4 quantitative management - prevents vanity metrics and measurement theater
---

# Quantitative Management

## Purpose & Context

Implements CMMI **MA** (Measurement & Analysis), **QPM** (Quantitative Project Management), and **OPP** (Organizational Process Performance) through data-driven decision making, statistical process control, and predictive analytics.

**Core Principle**: Measure what matters, use data to drive decisions, distinguish signal from noise.

**Avoid**: Measurement theater (tracking without action), vanity metrics (looks good but no value), gaming metrics (optimizing numbers vs processes).

---

## When to Use This Skill

**Triggers**:
- "What should we measure?"
- "How do I know if this variation is a problem?"
- "How do I establish process baselines?"
- "What's the difference between Level 2, 3, and 4 measurement?"
- "How do I use DORA metrics?"
- "How do I implement statistical process control?"
- "How do I use metrics for project decisions?"

**Use this when**:
- Establishing a measurement program
- Moving from Level 2 → 3 → 4
- Implementing DORA metrics
- Analyzing process performance
- Detecting process instability
- Predicting project outcomes
- Making data-driven decisions

**Do NOT use for**:
- Platform-specific metric collection → See `platform-integration` skill
- One-time reporting → Just write the report
- Metrics mandated by compliance → See `governance-and-risk` skill

---

## Quick Reference: Finding What You Need

| You Want To... | Reference Sheet | Key Content |
|----------------|-----------------|-------------|
| **Plan what to measure** | measurement-planning.md | GQM methodology, cost/value analysis, anti-patterns |
| **Choose metrics** | key-metrics-by-domain.md | Quality, velocity, stability, deployment metrics |
| **Implement DORA** | dora-metrics.md | 4 DORA metrics, collection automation, baselines |
| **Analyze variation** | statistical-analysis.md | Control charts, SPC, trend detection |
| **Establish baselines** | process-baselines.md | Historical data analysis, baseline maintenance |
| **Make data-driven decisions** | quantitative-management.md | QPM, prediction models, Level 4 practices |
| **Scale L2→L3→L4** | level-scaling.md | Maturity progression, requirements by level |

---

## Maturity Level Guidance

### Level 2 (Managed): Basic Tracking

**Focus**: Capture data for visibility

**Measurements**:
- Counts (defects found, tests run, deployments)
- Dates (when tasks completed, releases shipped)
- Simple averages (average lead time, average velocity)

**Tools**: Spreadsheets, basic dashboards, manual collection acceptable

**Example**: Track number of bugs found per sprint, average time to close bugs

**Limitation**: No statistical analysis, no baselines, reactive only

### Level 3 (Defined): Organizational Baselines & Trends

**Focus**: Establish norms, detect trends

**Measurements**:
- Organizational baselines (typical velocity, typical defect density)
- Trend analysis (improving or degrading?)
- Comparative analysis (this project vs org average)

**Tools**: Analytics platforms, automated collection, historical databases

**Example**: Know that your organization typically delivers 30 story points/sprint ± 10, and current project is trending 25 (slightly below average)

**Advancement over L2**: Baselines provide context, trends show direction

### Level 4 (Quantitatively Managed): Statistical Process Control

**Focus**: Predict outcomes, control variation

**Measurements**:
- Statistical process control (control charts, control limits)
- Prediction models (effort estimation, defect prediction)
- Process performance objectives (quantitative targets)
- Variance analysis (special cause vs common cause)

**Tools**: Statistical packages (R, Python), control chart software, Monte Carlo simulation

**Example**: Use control charts to detect when defect rate exceeds upper control limit (special cause), trigger root cause analysis. Use regression model to predict project completion date with 90% confidence interval.

**Advancement over L3**: Predictive, not just reactive; distinguishes noise from signal

---

## Measurement Anti-Patterns

| Anti-Pattern | Symptom | Better Approach |
|--------------|---------|-----------------|
| **Measurement Theater** | Tracking many metrics, no action taken | Use GQM to link metrics to decisions |
| **Vanity Metrics** | Numbers look impressive but don't drive improvement | Focus on actionable metrics with clear business value |
| **Gaming Metrics** | Teams optimize numbers instead of processes | Measure outcomes, not activities; use multiple metrics |
| **Lagging-Only** | Only measure results after the fact | Balance lagging with leading indicators |
| **Analysis Paralysis** | Too many metrics, can't make decisions | Focus on critical few (3-5 key metrics) |
| **Flying Blind** | No metrics, decisions based on opinion | Start with Level 2 basics, build up |
| **Over-Precision** | Measuring to 3 decimal places when ±20% is noise | Match precision to decision granularity |

---

## Integration with Other CMMI Process Areas

**REQM (Requirements Management)**:
- Metric: Requirements volatility (changes per sprint)
- Metric: Requirements traceability coverage (% with tests)
- Use baseline to detect abnormal churn

**CM (Configuration Management)**:
- Metric: Branch protection compliance
- Metric: Baseline stability (changes after freeze)
- Use SPC to detect configuration drift

**VER/VAL (Verification/Validation)**:
- Metric: Test coverage, defect density, escape rate
- Metric: Code review effectiveness
- Use control charts for quality gates

**RSKM (Risk Management)**:
- Metric: Risk exposure (probability × impact)
- Metric: Risk burndown (risks closed over time)
- Use trends to predict risk realization

**DAR (Decision Analysis & Resolution)**:
- Use measurement data as input to DAR
- Track decision quality (outcomes vs predictions)

**Cross-references**:
- `requirements-lifecycle` - Metrics for requirement quality
- `design-and-build` - Metrics for development process
- `governance-and-risk` - Risk and compliance metrics
- `platform-integration` - Metric collection automation

---

## Getting Started (Quick Start Scenarios)

### Scenario 1: First-Time Measurement Program (Level 2)

**Goal**: Start tracking basic metrics for visibility

1. Read `./measurement-planning.md` - Learn GQM methodology
2. Pick 3-5 metrics using GQM (don't start with 20+)
3. Set up manual or automated collection
4. Track for 4-8 weeks (establish baseline data)
5. Review monthly, adjust what you track

**Example metrics for first program**:
- Deployment frequency (how often we ship)
- Lead time for changes (commit to production)
- Defect escape rate (bugs found in production)

### Scenario 2: Implementing DORA Metrics (Level 2→3)

**Goal**: Industry-standard DevOps metrics

1. Read `./dora-metrics.md` - Understand the 4 metrics
2. Read `./measurement-planning.md` - Ensure DORA aligns with goals
3. Automate collection (see platform-integration skill for GitHub/Azure DevOps)
4. Establish baselines (4 weeks minimum)
5. Set quarterly improvement goals
6. Review weekly/monthly

### Scenario 3: Statistical Process Control (Level 3→4)

**Goal**: Detect process instability automatically

1. Read `./statistical-analysis.md` - Learn control charts
2. Establish process baselines (Level 3 requirement)
3. Calculate control limits (mean ± 2-3 standard deviations)
4. Plot data on control charts
5. Investigate points outside control limits (special cause)
6. Update baselines quarterly

**Example**: Defect escape rate control chart with UCL=15%, LCL=2%, current value 18% → investigate

### Scenario 4: Data-Driven Project Management (Level 4)

**Goal**: Use quantitative data for project decisions

1. Read `./quantitative-management.md` - Learn QPM practices
2. Read `./process-baselines.md` - Understand baseline usage
3. Set process performance objectives (e.g., defect density < X)
4. Use prediction models for estimates (see statistical-analysis.md)
5. Monitor against objectives using SPC
6. Adjust process when out of control

---

## Common Questions

**Q: How many metrics should I track?**
A: Level 2: 3-5 basic metrics. Level 3: 5-10 organizational baselines. Level 4: 3-5 with statistical control. **Focus beats breadth.**

**Q: How long to establish a baseline?**
A: Minimum 4 weeks for initial baseline. Prefer 12 weeks (1 quarter) for statistical validity. Update quarterly or when process changes.

**Q: What's the difference between MA and QPM?**
A: **MA** (Level 2+): Measurement & Analysis - defining, collecting, analyzing metrics. **QPM** (Level 4): Using statistical process control and prediction models to manage projects quantitatively.

**Q: Do I need Level 3 before Level 4?**
A: Yes. Level 4 requires organizational baselines (Level 3). Can't do statistical process control without knowing what "normal" looks like.

**Q: Leading vs lagging indicators - what's the difference?**
A: **Lagging**: Measure results after the fact (defects found, deployment time). **Leading**: Predict future outcomes (code review coverage, test coverage). You need both. See `./key-metrics-by-domain.md` for examples.

**Q: How do I avoid measurement theater?**
A: Use GQM methodology (see `./measurement-planning.md`). Every metric must answer a question that drives a decision. If you can't explain the decision, don't track the metric.

**Q: When should I use control charts?**
A: When you have 20+ data points and want to distinguish normal variation from abnormal (special cause). See `./statistical-analysis.md` for guidance.

---

## Reference Sheets

1. **measurement-planning.md** - GQM methodology, cost/value analysis, measurement repository design
2. **key-metrics-by-domain.md** - Quality, velocity, stability, deployment metrics with selection guidance
3. **dora-metrics.md** - Deployment Frequency, Lead Time, CFR, MTTR implementation
4. **statistical-analysis.md** - Control charts, trend detection, confidence intervals, SPC
5. **process-baselines.md** - Baseline establishment, maintenance, usage for estimation
6. **quantitative-management.md** - QPM practices, prediction models, process performance objectives
7. **level-scaling.md** - Level 2→3→4 progression with concrete requirements

---

## Related Practices

- `../requirements-lifecycle/SKILL.md` - Requirements management metrics
- `../design-and-build/SKILL.md` - Development process metrics
- `../governance-and-risk/SKILL.md` - Risk and compliance metrics
- `../platform-integration/SKILL.md` - Metric collection automation in GitHub/Azure DevOps

---

**Last Updated**: 2026-01-25
