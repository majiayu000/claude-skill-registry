---
name: subagent-testing
description: |
  TDD-style testing methodology for skills using fresh subagent instances
  to prevent priming bias and validate skill effectiveness.

  Triggers: test skill, validate skill, skill testing, subagent testing,
  fresh instance testing, TDD for skills, skill validation

  Use when: validating skill improvements, testing skill effectiveness,
  preventing priming bias, measuring skill impact on behavior

  DO NOT use when: implementing skills (use skill-authoring instead),
  creating hooks (use hook-authoring instead)
version: 1.0.0
category: testing
tags: [testing, validation, TDD, subagents, fresh-instances]
token_budget: 30
progressive_loading: true
---

# Subagent Testing - TDD for Skills

Test skills with fresh subagent instances to prevent priming bias and validate effectiveness.

## Overview

**Fresh instances prevent priming:** Each test uses a new Claude conversation to ensure
the skill's impact is measured, not conversation history effects.

## Why Fresh Instances Matter

### The Priming Problem
Running tests in the same conversation creates bias:
- Prior context influences responses
- Skill effects get mixed with conversation history
- Can't isolate skill's true impact

### Fresh Instance Benefits
- **Isolation**: Each test starts clean
- **Reproducibility**: Consistent baseline state
- **Measurement**: Clear before/after comparison
- **Validation**: Proves skill effectiveness, not priming

## Testing Methodology

Three-phase TDD-style approach:

### Phase 1: Baseline Testing (RED)
Test without skill to establish baseline behavior.

### Phase 2: With-Skill Testing (GREEN)
Test with skill loaded to measure improvements.

### Phase 3: Rationalization Testing (REFACTOR)
Test skill's anti-rationalization guardrails.

## Quick Start

```bash
# 1. Create baseline tests (without skill)
# Use 5 diverse scenarios
# Document full responses

# 2. Create with-skill tests (fresh instances)
# Load skill explicitly
# Use identical prompts
# Compare to baseline

# 3. Create rationalization tests
# Test anti-rationalization patterns
# Verify guardrails work
```

## Detailed Testing Guide

For complete testing patterns, examples, and templates:
- **[Testing Patterns](modules/testing-patterns.md)** - Full TDD methodology
- **[Test Examples](modules/test-examples.md)** - Baseline, with-skill, rationalization tests
- **[Analysis Templates](modules/analysis-templates.md)** - Scoring and comparison frameworks

## Success Criteria

- **Baseline**: Document 5+ diverse baseline scenarios
- **Improvement**: ≥50% improvement in skill-related metrics
- **Consistency**: Results reproducible across fresh instances
- **Rationalization Defense**: Guardrails prevent ≥80% of rationalization attempts

## See Also

- **skill-authoring**: Creating effective skills
- **bulletproof-skill**: Anti-rationalization patterns
- **test-skill**: Automated skill testing command
