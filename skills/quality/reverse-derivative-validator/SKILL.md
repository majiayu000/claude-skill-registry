---
name: reverse-derivative-validator
description: Triadic skill (validation)
metadata:
  trit: -1
  category: validation
  polynomial: "Output^y^Input"
---

# Reverse Derivative Validator

Triadic skill (validation)

## Polynomial Interface

```
p = Output^y^Input
```

## Activation

Load when this skill is needed.

## Usage

```bash
bb ~/.claude/skills/reverse-derivative-validator/run.bb
```

## Behavior

1. **MINUS (-1)**: Validate inputs
2. **ERGODIC (0)**: Process/transform  
3. **PLUS (+1)**: Emit results

## GF(3) Conservation

This skill participates in triadic composition: Σ trits ≡ 0 (mod 3)
