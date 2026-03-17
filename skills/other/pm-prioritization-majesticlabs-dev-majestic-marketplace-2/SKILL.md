---
name: pm-prioritization
description: Feature prioritization frameworks - RICE scoring, ICE scoring, and Opportunity Solution Trees.
triggers:
  - rice scoring
  - ice scoring
  - feature prioritization
  - opportunity solution tree
  - prioritize features
  - ost
---

# Feature Prioritization

Frameworks for prioritizing features and opportunities.

## RICE Scoring

```
RICE Score = (Reach × Impact × Confidence) / Effort
```

| Factor | Definition | Scale |
|--------|------------|-------|
| **Reach** | Users affected per quarter | Actual number |
| **Impact** | Effect on users | 3=Massive, 2=High, 1=Medium, 0.5=Low, 0.25=Minimal |
| **Confidence** | How sure are you? | 100%=High, 80%=Medium, 50%=Low |
| **Effort** | Person-months to ship | Actual estimate |

**RICE Table:**

```markdown
| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| [Feature A] | 5000 | 2 | 80% | 2 | 4000 |
| [Feature B] | 1000 | 3 | 50% | 1 | 1500 |
```

## ICE Scoring (Simpler)

```
ICE Score = Impact × Confidence × Ease
```

| Factor | Scale |
|--------|-------|
| **Impact** | 1-10 (potential value) |
| **Confidence** | 1-10 (certainty of impact) |
| **Ease** | 1-10 (implementation simplicity) |

**ICE Table:**

```markdown
| Feature | Impact | Confidence | Ease | ICE Score |
|---------|--------|------------|------|-----------|
| [Feature A] | 8 | 7 | 5 | 280 |
| [Feature B] | 6 | 9 | 8 | 432 |
```

## Opportunity Solution Tree

**Structure:**

```
Outcome (measurable business goal)
├── Opportunity 1 (unmet customer need)
│   ├── Solution 1a
│   │   └── Experiment: [test]
│   └── Solution 1b
│       └── Experiment: [test]
├── Opportunity 2 (another need)
│   └── Solution 2a
│       └── Experiment: [test]
└── Opportunity 3
    └── ...
```

**OST Template:**

```markdown
## Outcome
**Goal:** [Measurable objective]
**Current:** [Baseline metric]
**Target:** [Target metric]
**Timeline:** [By when]

## Opportunity Map

### Opportunity 1: [Customer need/pain point]
**Evidence:** [Interview quotes, data]
**Size:** [How many users affected]

**Solutions considered:**
1. **[Solution A]**
   - Effort: [S/M/L]
   - Experiment: [How to test cheaply]
   - Success metric: [What to measure]

2. **[Solution B]**
   - Effort: [S/M/L]
   - Experiment: [How to test cheaply]
   - Success metric: [What to measure]

**Selected:** [Which and why]
```

## When to Use Each

| Framework | Best For | Limitations |
|-----------|----------|-------------|
| RICE | Large teams, many features | Requires reach data |
| ICE | Quick decisions, small teams | More subjective |
| OST | Strategy alignment | Requires outcome clarity |

## Prioritization Anti-Patterns

- **HiPPO** (Highest Paid Person's Opinion) → Use data
- **Squeaky wheel** (loudest customer wins) → Weight by segment size
- **Pet projects** (internal favorites) → Require evidence
- **Sunk cost** (we started, must finish) → Re-evaluate regularly
