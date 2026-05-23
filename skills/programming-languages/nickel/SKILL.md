---
name: nickel
description: Nickel configuration language with gradual typing, contracts, and dynamic sufficiency verification. Use for type-safe configs, transformation contracts, and validation pipelines.
version: 1.0.0
---


# Nickel Configuration Language

Gradual typing + contracts for configuration that composes correctly.

## Dynamic Sufficiency

A Nickel config is **dynamically sufficient** when:

1. **Structural**: Contract coverage is complete (all fields typed)
2. **Computational**: Same outputs for all valid inputs
3. **Semantic**: Olog types preserved through transformations

```nickel
# Sufficiency levels (from dynamic_sufficiency.jl)
let SufficiencyLevel = [|
  'NOT_SUFFICIENT,           # Different behavior
  'WEAKLY_SUFFICIENT,        # Same structure, different labels  
  'COMPUTATIONALLY_SUFFICIENT,  # Same outputs
  'SEMANTICALLY_SUFFICIENT      # Same olog meaning
|]
```

## Core Contracts

Import from workspace:
```nickel
let contracts = import ".topos/nickel/contracts/transformation-contracts.ncl"
```

Available contracts:
- `TransformationPattern` - rename/refactor operations
- `TransformationStrategy` - checkpoint + rollback + validation
- `BalancedTernarySelector` - GF(3) strategy selection (seed 1069)
- `ValidationResult` - gate pass/fail with exit codes

## Gradual Typing Pattern

```nickel
# Untyped (dynamic) - simple configs
{ name = "example", count = 42 }

# Typed block - contract enforcement
let typed_config : { name: String, count: Number } = 
  { name = "example", count = 42 }

# Contract annotation - runtime validation
let validated = config | TransformationStrategy
```

## Idempotent Contracts

```nickel
# Good: applying twice yields same result
let Positive = std.contract.from_predicate (fun x => x > 0)
5 | Positive | Positive  # ✓ idempotent

# Key property for dynamic sufficiency:
# ∀c: Contract, ∀x: (x | c) | c ≡ x | c
```

## Workspace Integration

| Path | Purpose |
|------|---------|
| `.topos/nickel/contracts/` | Reusable contract library |
| `.topos/nickel/examples/` | Transformation examples |
| `environment-specs/environments.ncl` | Flox env specs |
| `seth-rs/nickel/` | Pipeline + telemetry modules |

## CLI Usage

```bash
# Evaluate config
nickel eval config.ncl

# Type-check without eval
nickel typecheck config.ncl

# Export to JSON
nickel export config.ncl --format json

# REPL
nickel repl
```

## GF(3) Integration

```
Trit: 0 (ERGODIC - synthesis/validation)
Home: Prof
Poly Op: ⊗
Color: #FFFF00
```

Triadic pairing:
- `dune-analytics` (+1) - expanding/querying
- `nickel` (0) - contract validation
- `sicp` (-1) - foundational evaluation

## Dynamic Sufficiency Verification

```nickel
# Verify sufficiency between two configs
let verify_sufficiency = fun cfg1 cfg2 =>
  let fields1 = std.record.fields cfg1 in
  let fields2 = std.record.fields cfg2 in
  if std.array.all (fun f => std.array.elem f fields2) fields1
  then 'COMPUTATIONALLY_SUFFICIENT
  else 'NOT_SUFFICIENT
```

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 8. Degeneracy

**Concepts**: redundancy, fallback, multiple strategies, robustness

### GF(3) Balanced Triad

```
nickel (−) + SDF.Ch8 (−) + [balancer] (−) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch5: Evaluation
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages

### Connection Pattern

Degeneracy provides fallbacks. This skill offers redundant strategies.
