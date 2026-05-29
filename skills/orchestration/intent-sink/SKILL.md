---
name: intent-sink
description: Intent Sink Skill
version: 1.0.0
---


# intent-sink Skill


> *"Where intents go to be validated. The final checkpoint before execution."*

## Overview

**Intent Sink** is the validation endpoint for intent-centric architectures. It validates that intents are well-formed, satisfiable, and safe before allowing execution.

## GF(3) Role

| Aspect | Value |
|--------|-------|
| Trit | -1 (MINUS) |
| Role | VALIDATOR |
| Function | Validates intents before execution |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      INTENT FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Intent    Solver       Intent Sink      Execution         │
│  (+1 GEN)      (0 COORD)     (-1 VAL)        (output)          │
│      │             │              │               │             │
│      ▼             ▼              ▼               ▼             │
│  ┌───────┐    ┌────────┐    ┌──────────┐    ┌─────────┐        │
│  │Declare│───►│ Solve  │───►│ Validate │───►│ Execute │        │
│  └───────┘    └────────┘    └──────────┘    └─────────┘        │
│                                  │                              │
│                                  ▼                              │
│                           ┌──────────┐                          │
│                           │ Reject ? │                          │
│                           └──────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Validation Checks

```python
class IntentSink:
    """Final validation before intent execution."""

    TRIT = -1  # VALIDATOR role

    def validate(self, intent, solution):
        """Run all validation checks."""
        checks = [
            self.check_well_formed(intent),
            self.check_resource_conservation(solution),
            self.check_authorization(intent),
            self.check_deadlines(intent),
            self.check_slippage(intent, solution),
        ]
        return all(checks)

    def check_well_formed(self, intent):
        """Intent has valid structure."""
        required = ['type', 'constraints', 'deadline']
        return all(k in intent for k in required)

    def check_resource_conservation(self, solution):
        """Inputs balance outputs (no creation/destruction)."""
        input_sum = sum(r.quantity for r in solution.inputs)
        output_sum = sum(r.quantity for r in solution.outputs)
        return input_sum == output_sum

    def check_authorization(self, intent):
        """User authorized to create this intent."""
        return verify_signature(intent.signature, intent.user)

    def check_deadlines(self, intent):
        """Intent hasn't expired."""
        return intent.deadline > current_time()

    def check_slippage(self, intent, solution):
        """Solution meets slippage constraints."""
        if intent.type == 'swap':
            actual_rate = solution.output_amount / solution.input_amount
            min_rate = intent.min_rate * (1 - intent.slippage)
            return actual_rate >= min_rate
        return True
```

## Sink Modes

```python
class SinkMode(Enum):
    STRICT = "reject on any failure"
    LENIENT = "allow with warnings"
    DRY_RUN = "validate but don't execute"

class ConfigurableSink:
    def __init__(self, mode: SinkMode):
        self.mode = mode

    def process(self, intent, solution):
        result = self.validate(intent, solution)

        if self.mode == SinkMode.DRY_RUN:
            return {"valid": result, "executed": False}

        if not result and self.mode == SinkMode.STRICT:
            raise ValidationError("Intent failed validation")

        if not result and self.mode == SinkMode.LENIENT:
            log.warning(f"Intent {intent.id} has warnings")

        return {"valid": result, "executed": True}
```

## GF(3) Integration

```python
def intent_triad(intent, solver, sink):
    """
    Complete intent lifecycle with GF(3) conservation.

    intent (+1) + solver (0) + sink (-1) = 0 ✓
    """
    # Generation phase
    raw_intent = intent.declare()  # +1

    # Coordination phase
    solution = solver.solve(raw_intent)  # 0

    # Validation phase
    if sink.validate(raw_intent, solution):  # -1
        return solution.execute()
    else:
        return None

    # Net GF(3): +1 + 0 + (-1) = 0 ✓
```

## Anoma Integration

```juvix
-- Intent sink in Juvix
module IntentSink;

type ValidationResult :=
  | Valid : Solution -> ValidationResult
  | Invalid : Error -> ValidationResult;

validate : Intent -> Solution -> ValidationResult;
validate intent solution :=
  if (all-checks-pass intent solution)
    then Valid solution
    else Invalid (first-failure intent solution);

-- Compose with solver
process : Intent -> Maybe Transaction;
process intent :=
  case solve intent of
    | Nothing -> Nothing
    | Just solution ->
        case validate intent solution of
          | Valid s -> Just (execute s)
          | Invalid _ -> Nothing;
```

## GF(3) Triads

```
intent-sink (-1) ⊗ solver-fee (0) ⊗ anoma-intents (+1) = 0 ✓
intent-sink (-1) ⊗ dynamic-sufficiency (0) ⊗ polyglot-spi (+1) = 0 ✓
```

---

**Skill Name**: intent-sink
**Type**: Intent Validation
**Trit**: -1 (MINUS - VALIDATOR)
**GF(3)**: Final checkpoint for intent execution


## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 1. Flexibility through Abstraction

**Concepts**: combinators, compose, parallel-combine, spread-combine, arity

### GF(3) Balanced Triad

```
intent-sink (−) + SDF.Ch1 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)

### Secondary Chapters

- Ch7: Propagators

### Connection Pattern

Combinators compose operations. This skill provides composable abstractions.
## Cat# Integration

This skill maps to Cat# = Comod(P) as a bicomodule in the Prof home:

```
Trit: 0 (ERGODIC)
Home: Prof (profunctors/bimodules)
Poly Op: ⊗ (parallel composition)
Kan Role: Adj (adjunction bridge)
```

### GF(3) Naturality

The skill participates in triads where:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.