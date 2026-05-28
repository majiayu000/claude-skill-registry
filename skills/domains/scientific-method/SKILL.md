---
name: scientific-method
description: Research methodology for hypothesis testing, evidence evaluation, and verification standards in geoscience research. Use when designing experiments, formulating hypotheses, or evaluating evidence quality.
triggers:
  - formulate hypothesis
  - test hypothesis
  - research design
  - evidence evaluation
  - verify finding
  - scientific method
location: user
---

# Scientific Method for Geoscience Research

## When to Use This Skill

Invoke when:
- Formulating or testing hypotheses
- Designing validation experiments
- Evaluating strength of evidence
- Deciding if a finding is confirmed vs preliminary
- Setting up controls and reproducibility checks

## Core Principles

### 1. Evidence Hierarchy

Apply this hierarchy when evaluating claims:

| Level | Description | Example |
|-------|-------------|---------|
| **Tier 1** | Multi-proxy validation | δ18O + Mg/Ca + δ13C all show signal |
| **Tier 2** | Two independent lines | δ18O + historical documentation |
| **Tier 3** | Single proxy | Only δ18O shows anomaly |

### 2. Verification Standards

**Minimum for confident claims:**
- One source = coincidence (interesting but unverified)
- Two sources = clue (worth investigating)
- Three sources = verified (minimum for publication)

### 3. Hypothesis Formulation

Good hypotheses are:
- **Falsifiable**: Define what evidence would disprove it
- **Specific**: Include testable predictions with measurable outcomes
- **Bounded**: State assumptions and limitations upfront

**Template:**
```
HYPOTHESIS: [Claim]
PREDICTION: If true, we should observe [specific outcome]
FALSIFICATION: If we observe [contrary evidence], hypothesis is rejected
ASSUMPTIONS: [List key assumptions]
```

### 4. Controls and Reproducibility

For each analysis, identify:
- **Positive controls**: Known events that SHOULD be detected
- **Negative controls**: Periods that SHOULD NOT show signal
- **Blind tests**: Analyze data without knowing expected result first

### 5. Uncertainty Language

Use precise language:

| Term | Meaning | When to Use |
|------|---------|-------------|
| "proposed" | Unconfirmed hypothesis | Single line of evidence |
| "likely" | Probable (2+ sources) | Two independent confirmations |
| "confirmed" | Multi-proxy validated | Three+ independent lines |
| "suggests" | Indicates direction | Preliminary interpretation |
| "consistent with" | Doesn't contradict | Supportive but not proof |

**NEVER use**: "100%", "definitely", "certainly", "must be", "proves"

### 6. Red Flags

Stop and reconsider if:
- [ ] Finding seems too clean/perfect
- [ ] No alternative explanations considered
- [ ] Post-hoc selection of "successful" cases
- [ ] Confirmation bias (looking for expected result)
- [ ] Circular reasoning (using conclusion as premise)

### 7. Breakthrough Skepticism

When you think you've made a major discovery:
1. **Pause** - Don't immediately declare success
2. **Check arithmetic** - Verify calculations independently
3. **Seek alternatives** - What else could explain this?
4. **Consult literature** - Has this been tried before?
5. **Sleep on it** - Fresh eyes often find flaws

## Workflow for New Hypothesis

```
1. STATE the hypothesis clearly
2. DEFINE falsification criteria
3. IDENTIFY positive/negative controls
4. GATHER data (ideally blind to expected result)
5. ANALYZE using pre-defined methods
6. EVALUATE against falsification criteria
7. DOCUMENT regardless of outcome
8. REPORT uncertainty honestly
```

## Example: Testing Earthquake Detection

**Hypothesis**: Speleothem δ18O detects M6+ earthquakes within 50 km

**Prediction**: Known historical earthquakes should show z > 2.0 anomalies within ±10 years of event

**Falsification**: If >50% of known earthquakes show no anomaly, hypothesis is rejected

**Positive controls**: 1896 Independence M6.3 (48 km from Crystal Cave)

**Negative controls**: Periods with no documented seismicity

**Test result**: 6/6 positive controls detected → Tier 2 evidence (small n, needs replication)
