---
name: reversible-computing
description: "Janus and reversible languages: run programs backwards, time-symmetric computation."
version: 1.0.0
---


# Reversible Computing Skill

> *"Every computation can be undone. Time flows both ways."*

## Core Concept

Reversible computing ensures:
1. **Bijective** — every state has exactly one predecessor AND successor
2. **No information loss** — can always recover input from output
3. **Time-symmetric** — run program forwards or backwards
4. **Landauer limit** — theoretical minimum energy (no erasure = no heat)

```
        forward
Input ─────────────▶ Output
      ◀─────────────
        backward
```

## Why It's Strange

1. **No destructive updates** — `x = 5` is illegal (loses old value)
2. **No `if` without `fi`** — conditionals must be invertible
3. **No garbage** — all temporary values must be "uncomputed"
4. **Quantum-ready** — unitary operations are reversible

## Janus Language

```janus
procedure swap(int x, int y)
    x ^= y      // x' = x ⊕ y
    y ^= x      // y' = y ⊕ (x ⊕ y) = x
    x ^= y      // x'' = (x ⊕ y) ⊕ x = y

// Running BACKWARDS automatically inverts!
// uncall swap(a, b)  ← swaps back
```

### Reversible Conditionals

```janus
// Forward: if-then-else-fi
if x = 0 then
    x += 1
else
    x += 2
fi x = 1    // <-- ASSERTION: must be true after forward

// Backward: uses fi-assertion to know which branch was taken
```

### Reversible Loops

```janus
// Forward: from-do-loop-until
from x = 0 do
    x += 1
loop
    y += x
until x = 10

// Backward: runs until x = 0, undoing each iteration
```

## Bennett's Trick

How to make irreversible computation reversible:

```
1. Compute f(x) → y, keeping all intermediate garbage g
2. Copy y to output
3. UNCOMPUTE: run step 1 backwards to clean up g

    ┌─────────────────────────────────────┐
    │ x ──▶ COMPUTE ──▶ (y,g) ──▶ COPY    │
    │                       │       │     │
    │                       ▼       ▼     │
    │                  UNCOMPUTE   y_out  │
    │                       │             │
    │                       ▼             │
    │                      (x,0)          │
    └─────────────────────────────────────┘
```

Space: O(T) → O(T log T) with checkpointing

## Implementation

```python
class ReversibleMachine:
    def __init__(self):
        self.tape = {}  # variable → value
        self.history = []  # for reversal
    
    def xor_assign(self, var, value):
        """x ^= value (self-inverse!)"""
        old = self.tape.get(var, 0)
        self.tape[var] = old ^ value
        self.history.append(('xor', var, value))
    
    def add_assign(self, var, value):
        """x += value"""
        old = self.tape.get(var, 0)
        self.tape[var] = old + value
        self.history.append(('add', var, value))
    
    def sub_assign(self, var, value):
        """x -= value (inverse of add)"""
        old = self.tape.get(var, 0)
        self.tape[var] = old - value
        self.history.append(('sub', var, value))
    
    def reverse_step(self):
        """Undo last operation."""
        if not self.history:
            return False
        
        op, var, value = self.history.pop()
        if op == 'xor':
            self.tape[var] ^= value  # XOR is self-inverse
        elif op == 'add':
            self.tape[var] -= value
        elif op == 'sub':
            self.tape[var] += value
        return True
    
    def reverse_all(self):
        """Run entire program backwards."""
        while self.reverse_step():
            pass
```

## Reversible Gates (Hardware)

```
Fredkin Gate (CSWAP):      Toffoli Gate (CCNOT):
                           
  a ─────●───── a            a ─────●───── a
         │                          │
  b ───┬─┼─┬─── b'           b ─────●───── b
       │ │ │                        │
  c ───┴─●─┴─── c'           c ─────⊕───── c ⊕ (a ∧ b)

If a=1: swap b,c            If a=b=1: flip c
If a=0: pass through        Otherwise: pass through
```

Both are **universal** for reversible classical computation.

## GF(3) Integration

```julia
# Reversible operations on GF(3)
# x ⊕₃ y = (x + y) mod 3 is reversible (inverse: x ⊖₃ y)

function gf3_add!(state, var, value)
    state[var] = (state[var] + value) % 3
    # Inverse: gf3_sub!(state, var, value)
end

function gf3_sub!(state, var, value)
    state[var] = (state[var] - value + 3) % 3
end

# Trit-preserving swap
function trit_swap!(state, a, b)
    # XOR doesn't work in GF(3), use:
    state[a], state[b] = state[b], state[a]
    # Self-inverse: swap is its own reverse
end
```

## Quantum Connection

All quantum gates are unitary → reversible:

```
        ┌───┐
|ψ⟩ ────┤ U ├──── U|ψ⟩
        └───┘
        
        ┌────┐
U|ψ⟩ ───┤ U† ├─── |ψ⟩   (U† = inverse)
        └────┘
```

Irreversible measurement "collapses" superposition → information loss.

## Energy and Landauer's Principle

```
Irreversible:  Erase 1 bit → kT ln(2) energy released as heat
                            ≈ 2.8 × 10⁻²¹ J at room temperature

Reversible:    No erasure → no theoretical minimum energy
               (practical limits remain)
```

## Languages & Tools

| Language | Description |
|----------|-------------|
| **Janus** | First reversible imperative language |
| **RFUN** | Reversible functional |
| **SyReC** | Reversible circuit synthesis |
| **Quipper** | Quantum (inherently reversible) |
| **Theseus** | Type-safe reversible |

## Example: Reversible Fibonacci

```janus
procedure fib(int n, int x1, int x2)
    from x1 = 1 ∧ x2 = 0 do
        x1 += x2
        x1 <=> x2    // swap
        n -= 1
    until n = 0
    
// call fib(10, x1, x2)  → x1 = 55, x2 = 89
// uncall fib(10, x1, x2) → x1 = 1, x2 = 0
```

## Literature

1. **Landauer (1961)** - "Irreversibility and Heat Generation"
2. **Bennett (1973)** - "Logical Reversibility of Computation"
3. **Yokoyama & Glück (2007)** - "A Reversible Programming Language"
4. **Fredkin & Toffoli (1982)** - "Conservative Logic"

## Related Skills

- `quantum-computing` - Unitary = reversible
- `thermodynamics` - Landauer limit
- `bidirectional-programming` - Lenses
- `interaction-nets` - Reduction is reversible



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 6. Layering

**Concepts**: layered data, metadata, provenance, units

### GF(3) Balanced Triad

```
reversible-computing (+) + SDF.Ch6 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch1: Flexibility through Abstraction
- Ch2: Domain-Specific Languages
- Ch7: Propagators

### Connection Pattern

Layering adds metadata. This skill tracks provenance or annotations.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.