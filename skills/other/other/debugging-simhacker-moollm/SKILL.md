---
name: debugging
description: Systematic bug investigation with hypothesis tracking
license: MIT
tier: 2
allowed-tools:
  - read_file
  - write_file
  - list_dir
  - search_replace
  - run_terminal_cmd
  - grep
related: [adventure, sniffable-python, scratchpad, research-notebook, sister-script, session-log, self-repair, play-learn-lift, constructionism]
tags: [moollm, development, investigation, hypothesis, testing]
inputs:
  symptom:
    type: string
    required: true
    description: "What's the observable problem?"
  context:
    type: string
    required: false
    description: "When/where does it happen?"
  expected:
    type: string
    required: false
    description: "What should happen instead?"
outputs:
  - DEBUG.yml
  - HYPOTHESES.md
  - TESTS.md
  - ROOT_CAUSE.md
templates:
  - DEBUG.yml.tmpl
---

# 🔧 Debugging Skill

> **"Hypothesize, test, learn, repeat."**

Debug problems methodically. Track hypotheses, test systematically, converge on root causes.

## Purpose

Debug problems methodically. Track hypotheses, document tests, record what you learn, and converge on root causes.

## When to Use

- Something isn't working as expected
- Mysterious behavior needs explanation
- Performance problems need diagnosis
- "Works on my machine" situations

## The Debugging Loop

```
OBSERVE → HYPOTHESIZE → TEST → LEARN → (repeat or) → FIX
```

### Terminal States

- `FIX` — Bug resolved
- `WONTFIX` — Intentional behavior
- `DEFER` — Not addressing now

## Protocol

### Observation Phase

Before guessing, gather facts:

```yaml
observation:
  symptom: "What's the observable problem?"
  context: "When does it happen?"
  expected: "What should happen instead?"
  
  evidence:
    - "Error message (exact text)"
    - "Logs showing the issue"
    - "Steps to reproduce"
    
  constraints:
    - "What we know for sure"
    - "What we've already ruled out"
```

### Hypothesis Tracking

```yaml
hypothesis:
  id: "hyp-001"
  claim: "The bug is caused by X"
  confidence: "high|medium|low"
  
  if_true:
    - "We would expect to see..."
    - "Changing X should fix it"
    
  test:
    action: "What to try"
    expected: "What we expect if hypothesis is correct"
    
  result:
    status: "confirmed|refuted|inconclusive"
    observation: "What actually happened"
    learned: "What this tells us"
```

### Test Documentation

```yaml
test:
  id: "test-001"
  hypothesis: "hyp-001"
  action: "What we did"
  
  before:
    state: "System state before test"
    
  after:
    state: "System state after test"
    
  result: "confirmed|refuted|inconclusive"
  learned: "What we now know"
```

## Schemas

### Observation Schema

| Field | Required | Purpose |
|-------|----------|---------|
| `symptom` | ✓ | Observable problem |
| `expected` | ✓ | What should happen |
| `error_message` | | Exact error text |
| `logs` | | Relevant log entries |
| `steps_to_reproduce` | | How to trigger |
| `constraints` | | Known facts |
| `ruled_out` | | Eliminated possibilities |

### Hypothesis Schema

| Field | Required | Purpose |
|-------|----------|---------|
| `id` | ✓ | Unique identifier |
| `claim` | ✓ | What you think is wrong |
| `test` | ✓ | How to validate |
| `confidence` | | high/medium/low |
| `if_true` | | Expected observations |
| `result` | | Test outcome |
| `learned` | | Insight gained |

### Test Schema

| Field | Required | Purpose |
|-------|----------|---------|
| `id` | ✓ | Unique identifier |
| `hypothesis` | ✓ | Which hypothesis |
| `action` | ✓ | What was tried |
| `result` | ✓ | confirmed/refuted/inconclusive |
| `before` | | State before |
| `after` | | State after |
| `learned` | | Insight |

## Core Files

| File | Purpose |
|------|---------|
| `DEBUG.yml` | Current debugging session |
| `HYPOTHESES.md` | All hypotheses and their status |
| `TESTS.md` | Test log |
| `ROOT_CAUSE.md` | Final analysis |

## Commands

| Command | Action |
|---------|--------|
| `DEBUG [symptom]` | Start debugging session |
| `OBSERVE [fact]` | Record observation |
| `HYPOTHESIZE [claim]` | Propose hypothesis |
| `TEST [action]` | Document test |
| `LEARN [insight]` | Record what you learned |
| `ROOT-CAUSE [explanation]` | Document root cause |

## The Scientific Method for Bugs

1. **Observe**: What exactly is happening?
2. **Question**: Why might this be happening?
3. **Hypothesize**: Form testable explanation
4. **Predict**: What would we see if hypothesis is true?
5. **Test**: Try to confirm or refute
6. **Analyze**: What did we learn?
7. **Iterate**: New hypothesis or fix

## Debugging Techniques

### Binary Search

Narrow down where the bug lives. Use when the bug is somewhere in a large space.

```yaml
technique: binary_search
steps:
  - "Find a known good state"
  - "Find a known bad state"
  - "Check the middle"
  - "Repeat until found"
```

### Rubber Duck

Explain the problem in detail. Use when stuck and need fresh perspective. Write detailed observation in DEBUG.yml — forces you to articulate assumptions.

### Minimal Reproduction

Simplify until bug is isolated. Use when complex system with unclear cause.

### Git Bisect

Find the commit that introduced bug. Use when bug is a regression.

### Print Debugging

Add logging to trace execution. Use when you need to understand flow.

## Working Set

Always include in context:
- `DEBUG.yml`
- `HYPOTHESES.md`

## Integration

| Direction | Skill | Relationship |
|-----------|-------|--------------|
| ← | [play-learn-lift](../play-learn-lift/) | Debugging IS learning |
| → | [session-log](../session-log/) | Log all debugging activities |
| → | [research-notebook](../research-notebook/) | Complex bugs need research |
| → | [honest-forget](../honest-forget/) | Compress debugging wisdom |
| ↔ | [adventure](../adventure/) | Debugging IS adventure |
| ↔ | [room](../room/) | Debug sessions are rooms |
| ↔ | [card](../card/) | Git Goblin 🧌, Index Owl 🦉 companions |
