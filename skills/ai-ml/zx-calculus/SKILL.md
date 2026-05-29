---
name: zx-calculus
description: Coecke's ZX-calculus for quantum circuit reasoning via string diagrams with Z-spiders (green) and X-spiders (red)
version: 1.0.0
---


# ZX-Calculus

**Trit**: -1 (MINUS - foundational/classical notation)
**Origin**: Coecke & Duncan (2008)
**Principle**: Quantum computation via string diagram rewriting

---

## Overview

ZX-calculus is a graphical language for quantum computing where:
- **Z-spiders** (green): Phase gates in computational basis
- **X-spiders** (red): Phase gates in Hadamard basis
- **Wires**: Qubits
- **Rewrite rules**: Simplify circuits

## Basic Elements

```
Z-spider (green):        X-spider (red):         Hadamard:
    │                        │                      ╲ ╱
  ┌─┴─┐                    ┌─┴─┐                     ─
  │ α │  = e^{iα}|0⟩⟨0|    │ α │  = H·Z(α)·H        ─
  └─┬─┘    + |1⟩⟨1|        └─┬─┘                    ╱ ╲
    │                        │
```

## GF(3) Color Assignment

| Spider | Color | Trit | Basis |
|--------|-------|------|-------|
| Z | Green #26D826 | 0 | Computational |
| X | Red #D82626 | +1 | Hadamard |
| H-edge | Blue #2626D8 | -1 | Transition |

**Conservation**: Green(0) + Red(+1) + Blue(-1) = 0 ✓

## Core Rules

### Spider Fusion
```
  │       │           │
┌─┴─┐   ┌─┴─┐       ┌─┴─┐
│ α │───│ β │  =    │α+β│
└─┬─┘   └─┬─┘       └─┬─┘
  │       │           │
```

### Bialgebra (Hopf)
```
  ╲ ╱       │ │
   X    =   │ │
  ╱ ╲       │ │
```

### Color Change
```
┌───┐     ┌───┐
│ Z │──H──│ X │
└───┘     └───┘
```

## DisCoPy Implementation

```python
from discopy.quantum.zx import Z, X, H, Id, SWAP, Cap, Cup

# Bell state preparation
bell = Cap(Z(0), Z(0)) >> (Id(1) @ H) >> CNOT

# ZX diagram
diagram = Z(1, 2, phase=0.5) >> (X(1, 1, phase=0.25) @ Z(1, 1))

# Simplify via rewrite rules
simplified = diagram.normal_form()

# Extract circuit
circuit = simplified.to_circuit()
```

## Musical Notation (Quantum Guitar)

From Abdyssagin & Coecke's "Bell" composition:

```
Staff 1 (Piano):     Staff 2 (Quantum Guitar):
    ┌─Z─┐                 ┌─X─┐
    │   │                 │   │
────┴───┴────        ─────┴───┴─────
    Bell pair            Measurement
```

## PyZX Integration

```python
import pyzx as zx

# Create circuit
circuit = zx.Circuit(2)
circuit.add_gate("H", 0)
circuit.add_gate("CNOT", 0, 1)

# Convert to ZX graph
graph = circuit.to_graph()

# Simplify
zx.simplify.full_reduce(graph)

# Extract optimized circuit
optimized = zx.extract_circuit(graph)
print(f"T-count: {optimized.tcount()}")
```

## Quantum Music Score

ZX-calculus as musical notation:

| ZX Element | Musical Meaning |
|------------|-----------------|
| Z-spider | Sustained note (computational) |
| X-spider | Transposed note (Hadamard) |
| Wire | Time/voice continuation |
| H-edge | Key change |
| Cup/Cap | Entanglement (Bell pair) |

## Applications

1. **Circuit optimization**: T-count reduction
2. **Verification**: Equivalence checking
3. **Compilation**: High-level → hardware
4. **Music**: Quantum score notation
5. **NLP**: Compositional semantics (DisCoCat)

## GF(3) Triad

| Component | Trit | Role |
|-----------|------|------|
| **zx-calculus** | **-1** | **Notation** |
| quantum-guitar | 0 | Performance |
| discopy | +1 | Computation |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## References

1. Coecke & Duncan (2008). Interacting quantum observables
2. van de Wetering (2020). ZX-calculus for the working quantum computer scientist
3. Coecke (2023). Basic ZX-calculus. arXiv:2303.03163

---

**Skill Name**: zx-calculus
**Type**: Quantum Computing / Diagrammatic Reasoning
**Trit**: -1 (MINUS)

## Non-Backtracking Geodesic Qualification

**Condition**: μ(n) ≠ 0 (Möbius squarefree)

This skill is qualified for non-backtracking geodesic traversal:

1. **Prime Path**: No state revisited in skill invocation chain
2. **Möbius Filter**: Composite paths (backtracking) cancel via μ-inversion
3. **GF(3) Conservation**: Trit sum ≡ 0 (mod 3) across skill triplets
4. **Spectral Gap**: Ramanujan bound λ₂ ≤ 2√(k-1) for k-regular expansion

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
zx-calculus (○) + SDF.Ch3 (○) + [balancer] (○) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch2: Domain-Specific Languages

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
