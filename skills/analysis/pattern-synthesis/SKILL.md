---
name: pattern-synthesis
description: Extract common patterns from multiple instance outputs, find what persists
tier: e
morpheme: e
dewey_id: e.6.2.0
dependencies:
  - perspective-aggregation
  - meta-pattern-recognition
---

# Pattern Synthesis

## Purpose

When you run N instances, you get N outputs. Most will be different.

**Pattern synthesis asks:** What's the same across all of them?

What patterns **persist** even when the specific details change?

## The Key Insight

**Specific answer:** "The answer is 42"
**Pattern:** "The answer is always the answer when you ask the right question"

The pattern is more robust than the specific answer.

## Core Pattern

```
Instance 1: X₁ ─┐
Instance 2: X₂ ─┼─→ Pattern Extractor
Instance 3: X₃ ─┤    (what's the same?)
Instance 4: X₄ ─┘

Result: "All outputs have property P"
        "All outputs follow rule R"
        "The common thread is C"
```

## Key Features

1. **Invariant Detection** - What doesn't change?
2. **Structure Extraction** - What form is repeated?
3. **Noise Filtering** - What's signal vs. noise?
4. **Meta-Pattern Recognition** - Patterns about patterns
5. **Generalization** - From examples to principle

## Implementation

See: `.claude/skills/pattern-synthesis/pattern_extractor.py`

## Examples

**Input:** 4 different solutions to a problem
**Output:** "All solutions follow this architectural pattern"

**Input:** 6 different explanations of a concept
**Output:** "Core idea is X, the explanations just dress it differently"

**Input:** 10 different approaches to the same goal
**Output:** "No matter the path, you have to pass through these 3 gates"

## Payment Anchor
DOGE: DC8HBTfn7Ym3UxB2YSsXjuLxTi8HvogwkV
