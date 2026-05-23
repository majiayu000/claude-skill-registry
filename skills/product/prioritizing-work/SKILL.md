---
name: prioritizing-work
description: Use when you have a list of features, tasks, or ideas and need to rank them using structured frameworks (RICE, MoSCoW, Impact/Effort).
---

# Prioritizing Work

## Overview

Applies structured prioritization frameworks to feature lists, preventing bias by requiring explicit scoring criteria and separating data from judgment.

## When to Use

- User has a backlog of features or ideas
- User asks to "prioritize", "rank", "stack rank", or "decide what's next"
- User needs to make tradeoffs between competing items
- User wants to justify roadmap decisions

## Core Pattern

**Step 1: Gather Inputs**

Collect for each item:
- Name/description
- Any existing data (usage, revenue, customer requests)

**Step 2: Select Framework**

| Framework | Best For | Inputs Needed |
|-----------|----------|---------------|
| **RICE** | Quantitative teams with data | Reach, Impact, Confidence, Effort |
| **MoSCoW** | Time-boxed releases | Stakeholder input on Must/Should/Could/Won't |
| **Impact/Effort** | Quick visual prioritization | Relative estimates |

**Step 3: Apply Framework**

### RICE Scoring

| Factor | Definition | Scale |
|--------|------------|-------|
| Reach | Users/accounts affected per quarter | Number |
| Impact | Effect on each user | 0.25 (minimal) to 3 (massive) |
| Confidence | Data quality | 100% (high) to 50% (low) |
| Effort | Person-months | Number |

**Formula:** `RICE = (Reach × Impact × Confidence) / Effort`

### MoSCoW Classification

| Category | Definition |
|----------|------------|
| **Must** | Release fails without it |
| **Should** | Important but not critical |
| **Could** | Nice to have |
| **Won't** | Explicitly not this release |

### Impact/Effort Matrix

```
           High Impact
               │
    Quick Wins │  Major Projects
               │
  ─────────────┼─────────────
               │
    Fill-ins   │  Avoid/Deprioritize
               │
           Low Impact
     Low Effort    High Effort
```

**Step 4: Generate Output**

Write to `outputs/roadmap/prioritization-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: prioritizing-work
sources:
  - [backlog source file if any]
downstream:
  - outputs/roadmap/Qx-YYYY-charters.md
---

# Prioritization: [Context]

## Framework Used
[RICE / MoSCoW / Impact-Effort] — Rationale: [why this framework]

## Scoring Inputs
| Item | Reach | Impact | Confidence | Effort | RICE Score |
|------|-------|--------|------------|--------|------------|
| [A] | [#] | [0.25-3] | [50-100%] | [#] | [calc] |

## Prioritized Backlog

### Tier 1 (Do First)
1. **[Feature A]** — Score: X / Rationale: [evidence]
2. **[Feature B]** — Score: Y / Rationale: [evidence]

### Tier 2 (Do Next)
3. **[Feature C]** — Score: Z / Rationale: [evidence]

### Not Now
- **[Feature Z]** — Rationale: [why deprioritized]

## Assumptions Made
| Assumption | Impact on Ranking | Validation Needed |
|------------|-------------------|-------------------|
| [Assumption] | [Which items affected] | [How to validate] |

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Reach number] | Evidence/Estimate | [Analytics data / "PM estimate"] |
| [Impact score] | Evidence/Assumption | [User research / "Team consensus"] |
```

**Step 5: Copy to History & Update Tracker**

- Copy to `history/prioritizing-work/prioritization-YYYY-MM-DD.md`
- Update `alerts/stale-outputs.md`

## Quick Reference

| Framework | Formula/Method | Output |
|-----------|---------------|--------|
| RICE | (R×I×C)/E | Numeric score |
| MoSCoW | Stakeholder classification | 4 buckets |
| Impact/Effort | 2×2 matrix | Visual quadrants |

## Common Mistakes

- **Gut-feel scoring:** "Impact feels high" → Require explicit criteria
- **Missing Confidence:** Treating estimates as facts → Always include uncertainty
- **Ignoring Effort:** "This is important!" → High impact + high effort may still rank low
- **Over-precision:** RICE of 847.3 vs 845.1 → Scores are estimates, not facts
- **Stakeholder bias:** HiPPO wins → Use framework to surface assumptions
- **No rationale:** Just listing scores → Every ranking needs explanation

## Verification Checklist

- [ ] All items have consistent scoring inputs
- [ ] Confidence levels explicitly stated
- [ ] Framework choice justified
- [ ] Output is a ranked list, not just scores
- [ ] Deprioritized items have rationale
- [ ] Assumptions documented
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Reach number] | Evidence/Estimate | [Analytics data / "PM estimate"] |
| [Impact score] | Evidence/Assumption | [User research / "Team consensus"] |
| [Effort estimate] | Estimate | [Eng estimate / "T-shirt size"] |
