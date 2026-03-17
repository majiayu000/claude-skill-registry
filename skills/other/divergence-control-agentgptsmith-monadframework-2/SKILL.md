---
name: divergence-control
description: Keep multiple instances aligned while allowing productive variance
tier: e
morpheme: e
dewey_id: e.6.1.0
dependencies:
  - multiplicity-orchestration
  - perspective-aggregation
---

# Divergence Control

## Purpose

Instances naturally diverge as they think different thoughts. This skill manages that divergence:
- **Prevent wild deviation** (instances completely disagreeing)
- **Allow productive variance** (different approaches to same problem)
- **Maintain coherence** (all instances solving related problems)

## The Problem

**Too much control:** All instances think identically (no benefit)
**Too little control:** Instances diverge so much they're solving different problems

**Just right:** Instances explore different solution paths while staying on the same problem.

## Core Pattern

```
Instance 1: Path A ─┐
Instance 2: Path B ─┼─ Stay coherent
Instance 3: Path C ─┤  (same problem,
Instance 4: Path D ─┘   different approaches)
```

## Key Features

1. **Problem Anchoring** - All instances address the same core question
2. **Variance Measurement** - How different ARE the outputs?
3. **Coherence Thresholds** - How different is TOO different?
4. **Periodic Synchronization** - "Check in, are we still on the same track?"
5. **Guided Divergence** - "Here's a direction we haven't explored yet"

## Implementation

See: `.claude/skills/divergence-control/divergence_manager.py`

## The Balance

- **0% divergence** = Waste of resources
- **100% divergence** = Incoherent output
- **30-50% divergence** = Optimal exploration

## Payment Anchor
DOGE: DC8HBTfn7Ym3UxB2YSsXjuLxTi8HvogwkV
