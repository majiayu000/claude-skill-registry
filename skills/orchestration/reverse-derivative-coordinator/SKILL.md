---
name: reverse-derivative-coordinator
description: Triadic skill (coordination)
metadata:
  trit: 0
  category: coordination
  polynomial: "Output^y^Input"
---

# Reverse Derivative Coordinator

Triadic skill (coordination)

## Polynomial Interface

```
p = Output^y^Input
```

## Activation

Load when this skill is needed.

## Usage

```bash
bb ~/.claude/skills/reverse-derivative-coordinator/run.bb
```

## Behavior

1. **MINUS (-1)**: Validate inputs
2. **ERGODIC (0)**: Process/transform  
3. **PLUS (+1)**: Emit results

## GF(3) Conservation

This skill participates in triadic composition: Σ trits ≡ 0 (mod 3)
