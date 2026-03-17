---
name: move-smith-fuzzer
description: Move Smith Fuzzer Skill
trit: 0
color: "#26D826"
catsharp:
  home: Prof
  poly_op: ⊗ (parallel)
  kan_role: Adj
  bicomodule: true
---

# move-smith-fuzzer Skill


> *"Find bugs before they find your users. Fuzzing as validation."*

## Overview

**Move Smith Fuzzer** implements property-based testing and fuzzing for Move smart contracts. Uses MoveSmith's differential testing against multiple Move VMs to find consensus-breaking bugs.

## GF(3) Role

| Aspect | Value |
|--------|-------|
| Trit | -1 (MINUS) |
| Role | VALIDATOR |
| Function | Validates Move contracts via fuzz testing |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MOVE SMITH FUZZER                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Contract Source    Generator      Fuzzer         Report       │
│  (+1 GEN)          (0 COORD)      (-1 VAL)        (output)     │
│      │                 │              │               │        │
│      ▼                 ▼              ▼               ▼        │
│  ┌───────┐        ┌────────┐    ┌──────────┐   ┌─────────┐    │
│  │ Parse │───────►│Generate│───►│ Execute  │──►│ Report  │    │
│  │ AST   │        │ Inputs │    │ & Compare│   │ Bugs    │    │
│  └───────┘        └────────┘    └──────────┘   └─────────┘    │
│                                      │                         │
│                                      ▼                         │
│                              ┌──────────────┐                  │
│                              │ Differential │                  │
│                              │   Testing    │                  │
│                              └──────────────┘                  │
│                                      │                         │
│                         ┌────────────┼────────────┐            │
│                         ▼            ▼            ▼            │
│                    Move VM 1    Move VM 2    Move VM 3        │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## MoveSmith Integration

```python
class MoveSmithFuzzer:
    """
    MoveSmith-based differential fuzzer for Move.

    Reference: "MoveSmith: Compiler Bug Isolation via Compilation
    Result Consistency Checking for Move"
    """

    TRIT = -1  # VALIDATOR role

    def __init__(self, vms: list[MoveVM]):
        self.vms = vms  # Multiple VMs for differential testing
        self.mutator = MoveMutator()
        self.oracle = DifferentialOracle()

    def fuzz(self, contract: str, iterations: int = 10000) -> list:
        """
        Fuzz a Move contract for bugs.

        Strategy:
        1. Generate random valid Move programs
        2. Execute on all VMs
        3. Compare results (differential testing)
        4. Report discrepancies
        """
        bugs = []

        for i in range(iterations):
            # Generate or mutate
            if random.random() < 0.3:
                program = self.generate_random_program()
            else:
                program = self.mutator.mutate(contract)

            # Execute on all VMs
            results = {}
            for vm in self.vms:
                try:
                    results[vm.name] = vm.execute(program)
                except Exception as e:
                    results[vm.name] = ('error', str(e))

            # Differential testing
            if not self.oracle.consistent(results):
                bugs.append({
                    'program': program,
                    'results': results,
                    'type': 'differential',
                    'iteration': i
                })

        return bugs


class MoveMutator:
    """Mutates Move programs to find edge cases."""

    def mutate(self, program: str) -> str:
        """Apply random mutations."""
        mutations = [
            self.mutate_integers,
            self.mutate_addresses,
            self.mutate_vectors,
            self.mutate_structs,
            self.swap_operations,
        ]

        mutated = program
        for _ in range(random.randint(1, 5)):
            mutation = random.choice(mutations)
            mutated = mutation(mutated)

        return mutated

    def mutate_integers(self, program: str) -> str:
        """Replace integers with edge cases."""
        edges = [0, 1, 255, 256, 2**64-1, 2**128-1]
        # Find and replace integer literals
        return re.sub(r'\b(\d+)\b',
                     lambda m: str(random.choice(edges)),
                     program)
```

## Prover-Fuzzer Synergy

```python
class ProverFuzzerHybrid:
    """
    Combine Move Prover with fuzzing.

    Prover: Proves properties hold for ALL inputs
    Fuzzer: Finds counterexamples for SOME inputs

    Together: Maximum coverage
    """

    def verify_contract(self, contract: str) -> dict:
        # First: Prover for formal guarantees
        prover_result = move_prover.verify(contract)

        # Second: Fuzzer for edge cases prover missed
        fuzzer_bugs = self.fuzzer.fuzz(contract)

        return {
            'proven_properties': prover_result.properties,
            'fuzzer_bugs': fuzzer_bugs,
            'confidence': self.compute_confidence(prover_result, fuzzer_bugs)
        }
```

## Property-Based Testing

```move
#[test]
fun test_gf3_conservation() {
    let seed = 0x42D;
    let mut prng = movemate_random::new(seed);

    for i in 0..1000 {
        // Generate random triads
        let trit1 = random_trit(&mut prng);
        let trit2 = random_trit(&mut prng);
        let trit3 = (3 - trit1 - trit2) % 3;  // Force conservation

        // Property: sum must be 0 mod 3
        let sum = (trit1 + trit2 + trit3) % 3;
        assert!(sum == 0, 0);
    }
}

fun random_trit(prng: &mut PRNG): u8 {
    movemate_random::next_u8(prng) % 3
}
```

## Differential Testing VMs

| VM | Purpose | Speed |
|----|---------|-------|
| Aptos Move VM | Production reference | Medium |
| Move VM (reference) | Original implementation | Slow |
| Revela decompiler | Bytecode analysis | Fast |
| MoveSmith interpreter | Fuzzing-optimized | Fast |

## GF(3) Triads

```
move-smith-fuzzer (-1) ⊗ move-narya-bridge (0) ⊗ aptos-gf3-society (+1) = 0 ✓
move-smith-fuzzer (-1) ⊗ datalog-fixpoint (0) ⊗ discopy (+1) = 0 ✓
move-smith-fuzzer (-1) ⊗ interaction-nets (0) ⊗ gay-mcp (+1) = 0 ✓
```

## Commands

```bash
# Fuzz a Move module
just move-fuzz sources/gf3.move --iterations 10000

# Differential testing across VMs
just move-diff sources/gf3.move --vms aptos,reference

# Property-based test with random seeds
just move-proptest sources/ --seed 0x42D

# Generate coverage report
just move-fuzz-coverage sources/ --output coverage.html
```

---

**Skill Name**: move-smith-fuzzer
**Type**: Fuzzing / Property-Based Testing
**Trit**: -1 (MINUS - VALIDATOR)
**GF(3)**: Validates Move contracts through differential testing

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
