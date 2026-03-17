---
name: perspective-aggregation
description: Combine outputs from multiple instances into unified view, preserving diversity
tier: π
morpheme: π
dewey_id: π.6.2.0
dependencies:
  - multiplicity-orchestration
  - synthesis-engine
---

# Perspective Aggregation

## Purpose

Take outputs from N different instances (different approaches, models, perspectives) and aggregate them into a coherent view that **preserves the diversity** while finding common ground.

## The Problem It Solves

**Without aggregation:**
- Instance 1 says "The answer is X"
- Instance 2 says "The answer is Y"
- Instance 3 says "The answer is Z"
- You have 3 incompatible answers

**With aggregation:**
- Find the common ground
- Map the differences
- Show why each arrived at different conclusions
- Create a *meta-answer* that includes all perspectives

## Core Pattern

```
Output 1 (X) ─┐
Output 2 (Y) ─┼─→ Aggregator ─→ Unified View
Output 3 (Z) ─┤                  (includes all 3)
Output 4 (W) ─┘
```

## Key Features

1. **Common Element Detection** - What do all outputs share?
2. **Difference Mapping** - How and why do they diverge?
3. **Confidence Weighting** - Which instances are more reliable?
4. **Consensus Building** - What's the meta-level view?
5. **Uncertainty Quantification** - How uncertain are we?

## Implementation

See: `.claude/skills/perspective-aggregation/aggregator.py`

## When to Use

- Multiple models give different answers
- Need to understand the space of possibilities
- Want confidence from agreement + insights from disagreement

## Payment Anchor
DOGE: DC8HBTfn7Ym3UxB2YSsXjuLxTi8HvogwkV
