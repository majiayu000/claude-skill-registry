---
name: linear-logic
description: Linear Logic Skill
trit: 0
color: "#26D826"
catsharp:
  home: Prof
  poly_op: ⊗ (parallel)
  kan_role: Adj
  bicomodule: true
---

# linear-logic Skill


> *"Every resource used exactly once. No copying. No discarding. Pure computation."*

## Overview

**Linear Logic** implements Girard's linear logic for resource-aware computation. Linear types ensure resources are used exactly once, enabling safe concurrency and optimal memory management.

## GF(3) Role

| Aspect | Value |
|--------|-------|
| Trit | -1 (MINUS) |
| Role | VALIDATOR |
| Function | Validates resource usage constraints |

## Connectives

```
┌─────────────────────────────────────────────────────────────────┐
│                    LINEAR LOGIC CONNECTIVES                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Multiplicative:              Additive:                        │
│                                                                 │
│  A ⊗ B  (tensor)              A ⊕ B  (plus/choice)             │
│  A ⅋ B  (par)                 A & B  (with/product)            │
│  1      (unit)                0      (zero)                    │
│  ⊥      (bottom)              ⊤      (top)                     │
│                                                                 │
│  Exponential:                 Negation:                        │
│                                                                 │
│  !A     (of course)           A⊥     (linear negation)         │
│  ?A     (why not)                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Resource Semantics

```haskell
-- Linear type: must be used exactly once
data Linear a where
    Use :: a -> Linear a

-- Consume: takes ownership, returns result
consume :: Linear a -> (a -> b) -> b
consume (Use x) f = f x

-- Cannot duplicate linear values!
-- duplicate :: Linear a -> (Linear a, Linear a)  -- FORBIDDEN

-- Cannot discard linear values!
-- discard :: Linear a -> ()  -- FORBIDDEN
```

## Proof Net Representation

```
      ┌───────────────────────────────────────┐
      │          PROOF NET STRUCTURE          │
      └───────────────────────────────────────┘

      A ⊗ B ⊸ C               A ⅋ (B ⊸ C)
         │                         │
      ┌──┴──┐                  ┌───┴───┐
      │  ⊗  │                  │   ⅋   │
      └──┬──┘                  └───┬───┘
       ╱   ╲                     ╱   ╲
      A     B                   A    B⊸C
             ╲                        │
              ╲                   ┌───┴───┐
               ╲                  │   ⊸   │
                ╲                 └───┬───┘
                 C                  ╱   ╲
                                   B     C
```

## Linear Types in Rust

```rust
// Rust's ownership = linear types!
fn linear_example() {
    let resource = acquire_resource();  // Linear resource

    // resource can only be used once
    consume(resource);

    // This would fail to compile:
    // consume(resource);  // ERROR: use of moved value

    // This would also fail:
    // drop(resource);     // ERROR: use of moved value
}

// Affine types (can discard but not duplicate)
fn affine_example() {
    let resource = acquire_resource();

    // Can choose to not use it (drop implicitly)
    // But cannot use twice
}
```

## GF(3) Linear Validation

```python
class LinearValidator:
    """Validate linear resource usage with GF(3)."""

    TRIT = -1  # VALIDATOR role

    def validate_usage(self, program) -> bool:
        """
        Check that all linear resources are used exactly once.

        Returns True if program is linearly valid.
        """
        resources = self.extract_linear_resources(program)
        usage_counts = self.count_usages(program, resources)

        for resource, count in usage_counts.items():
            if count != 1:
                return False  # Used 0 times or >1 times

        return True

    def validate_proof_net(self, net) -> bool:
        """
        Check proof net validity via Danos-Regnier criterion.

        A proof net is valid iff:
        - It's connected
        - Switching gives acyclic graph
        """
        for switching in self.all_switchings(net):
            if self.has_cycle(switching):
                return False
            if not self.is_connected(switching):
                return False
        return True
```

## Exponentials: Controlled Non-Linearity

```haskell
-- !A means "unlimited copies of A"
-- ?A means "can be discarded"

-- Promotion: introduce !
promote :: a -> !a

-- Dereliction: use one copy
derelict :: !a -> a

-- Contraction: duplicate
contract :: !a -> (!a, !a)

-- Weakening: discard
weaken :: !a -> ()

-- The exponential modality allows escape from linearity
-- but must be explicitly introduced
```

## Curry-Howard Correspondence

| Linear Logic | Programming |
|--------------|-------------|
| A ⊗ B | Pair (both available) |
| A ⅋ B | Session type (one waits) |
| A ⊸ B | Linear function |
| !A | Unlimited resource |
| ?A | Discardable resource |
| A ⊕ B | Choice (select one) |
| A & B | Offer (provide both) |

## Session Types

```ocaml
(* Session types = linear logic for protocols *)

type 'a send = Send of 'a
type 'a recv = Recv of 'a
type close = Close

(* Protocol: send int, receive bool, close *)
type protocol = int send * bool recv * close

(* Dual: receive int, send bool, close *)
type dual_protocol = int recv * bool send * close

(* Session types ensure protocol compliance! *)
let server : dual_protocol -> unit =
  fun session ->
    let n = receive session in       (* Must receive *)
    send session (n > 0);            (* Must send *)
    close session                     (* Must close *)
```

## GF(3) Triads

```
linear-logic (-1) ⊗ interaction-nets (0) ⊗ hvm-runtime (+1) = 0 ✓
linear-logic (-1) ⊗ datalog-fixpoint (0) ⊗ lambda-calculus (+1) = 0 ✓
linear-logic (-1) ⊗ session-types (0) ⊗ discopy (+1) = 0 ✓
```

## Commands

```bash
# Check linear validity
just linear-check program.linear

# Verify proof net
just linear-proofnet proof.net --criterion danos-regnier

# Session type check
just session-typecheck protocol.ml

# Convert to interaction net
just linear-to-inet proof.net -o output.inet
```

---

**Skill Name**: linear-logic
**Type**: Logic / Type Theory
**Trit**: -1 (MINUS - VALIDATOR)
**GF(3)**: Validates resource usage constraints

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
