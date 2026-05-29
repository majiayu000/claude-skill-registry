---
name: solver-fee
description: Solver Fee Skill
version: 1.0.0
---


# solver-fee Skill


> *"Fair compensation for coordination. The solver's incentive to find optimal solutions."*

## Overview

**Solver Fee** implements fee mechanisms for intent solvers in Anoma-style architectures. Solvers coordinate between intent generators and validators, earning fees for finding optimal matches.

## GF(3) Role

| Aspect | Value |
|--------|-------|
| Trit | 0 (ERGODIC) |
| Role | COORDINATOR |
| Function | Coordinates fee distribution between parties |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     SOLVER FEE FLOW                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Intent Creator     Solver          Validator       Executor   │
│  (+1 GEN)          (0 COORD)        (-1 VAL)        (output)   │
│      │                 │                │               │      │
│      ▼                 ▼                ▼               ▼      │
│  ┌───────┐        ┌────────┐       ┌──────────┐   ┌─────────┐  │
│  │ Offer │───────►│ Match  │──────►│ Validate │──►│ Execute │  │
│  │+ fee  │        │+ solve │       │+ verify  │   │         │  │
│  └───────┘        └────────┘       └──────────┘   └─────────┘  │
│      │                 │                                       │
│      │                 ▼                                       │
│      │          ┌──────────┐                                   │
│      └─────────►│ Fee Pool │                                   │
│                 └──────────┘                                   │
│                      │                                         │
│                      ▼                                         │
│                Solver Reward                                   │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## Fee Models

```python
class FeeModel:
    """Base class for solver fee computation."""

    TRIT = 0  # COORDINATOR role

    def compute_fee(self, intent, solution) -> int:
        raise NotImplementedError


class PercentageFee(FeeModel):
    """Fee as percentage of transaction value."""

    def __init__(self, basis_points: int = 30):
        self.basis_points = basis_points  # 30 = 0.30%

    def compute_fee(self, intent, solution) -> int:
        value = solution.output_value
        return value * self.basis_points // 10000


class GasPlusPremium(FeeModel):
    """Gas cost plus fixed premium."""

    def __init__(self, premium_bps: int = 10):
        self.premium_bps = premium_bps

    def compute_fee(self, intent, solution) -> int:
        gas_cost = estimate_gas(solution) * gas_price()
        premium = gas_cost * self.premium_bps // 10000
        return gas_cost + premium


class AuctionFee(FeeModel):
    """Competitive auction for solver fees."""

    def compute_fee(self, intent, bids: list) -> int:
        # Second-price auction: winner pays second-highest bid
        sorted_bids = sorted(bids, key=lambda b: b.fee, reverse=True)
        if len(sorted_bids) >= 2:
            return sorted_bids[1].fee  # Second price
        return sorted_bids[0].fee if sorted_bids else 0
```

## GF(3) Fee Conservation

```python
class GF3FeeDistribution:
    """Distribute fees while maintaining GF(3) conservation."""

    def distribute(self, total_fee: int) -> dict:
        """
        Split fee across GF(3) roles.

        GENERATOR (+1): Intent creator rebate (optional)
        COORDINATOR (0): Solver fee
        VALIDATOR (-1): Validator reward

        Sum must balance.
        """
        solver_share = total_fee * 60 // 100    # 60% to solver
        validator_share = total_fee * 30 // 100  # 30% to validator
        rebate = total_fee - solver_share - validator_share  # 10% rebate

        return {
            'generator': rebate,      # +1 role
            'coordinator': solver_share,  # 0 role
            'validator': validator_share,  # -1 role
            'sum': rebate + solver_share + validator_share,
            'conserved': True  # Fees sum to original total
        }
```

## Juvix Implementation

```juvix
-- Solver fee in Juvix
module SolverFee;

type Fee := mkFee : Nat -> Fee;

computeFee : Intent -> Solution -> Fee;
computeFee intent solution :=
  let value := solution-output-value solution in
  let bps := 30 in  -- 0.30%
  mkFee (value * bps / 10000);

type FeeDistribution :=
  mkDistribution : Fee -> Fee -> Fee -> FeeDistribution;

-- Fields: solver, validator, rebate

distribute : Fee -> FeeDistribution;
distribute (mkFee total) :=
  let solver := total * 60 / 100 in
  let validator := total * 30 / 100 in
  let rebate := total - solver - validator in
  mkDistribution (mkFee solver) (mkFee validator) (mkFee rebate);
```

## Integration with Anoma Intents

```python
def solve_with_fee(intent, solver):
    """
    Complete solving workflow with fee handling.

    GF(3) triad:
    - intent (+1): User creates
    - solver (0): Finds match
    - validator (-1): Verifies
    """
    # Solver finds optimal solution
    solution = solver.solve(intent)

    # Compute fee
    fee = compute_fee(intent, solution)

    # Attach fee to solution
    solution.solver_fee = fee
    solution.solver = solver.address

    return solution
```

## GF(3) Triads

```
solver-fee (0) ⊗ anoma-intents (+1) ⊗ intent-sink (-1) = 0 ✓
solver-fee (0) ⊗ polyglot-spi (+1) ⊗ dynamic-sufficiency (-1) = 0 ✓
solver-fee (0) ⊗ aptos-gf3-society (+1) ⊗ merkle-proof-validation (-1) = 0 ✓
```

---

**Skill Name**: solver-fee
**Type**: Fee Mechanism / Economic Coordination
**Trit**: 0 (ERGODIC - COORDINATOR)
**GF(3)**: Coordinates fee distribution between intent roles


## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 4. Pattern Matching

**Concepts**: unification, match, segment variables, pattern

### GF(3) Balanced Triad

```
solver-fee (+) + SDF.Ch4 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch1: Flexibility through Abstraction

### Connection Pattern

Pattern matching extracts structure. This skill recognizes and transforms patterns.
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