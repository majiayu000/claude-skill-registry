---
name: quantum-music
description: Quantum computer music composition and performance using quantum circuits, ZX-calculus notation, and quantum instruments
version: 1.0.0
---


# Quantum Music

**Trit**: 0 (ERGODIC - bridging classical and quantum)
**Field**: Quantum Computer Music
**Reference**: Miranda (2022) "Quantum Computer Music" Springer

---

## Overview

Quantum Music encompasses:
1. **Composition**: Using quantum algorithms/circuits
2. **Notation**: ZX-calculus augmented scores
3. **Instruments**: Quantum Guitar, Q1Synth, Actias
4. **Performance**: Live quantum state manipulation

## History

| Year | Milestone |
|------|-----------|
| 2022 | First quantum-composed music (Ludovico Quanthoven) |
| 2022 | Miranda's "Quantum Computer Music" book |
| 2023 | Q1Synth (Miranda, Thomas, Itaboraí) |
| 2024 | Quantum Guitar debuts (Edinburgh) |
| 2024 | Black Tish at Wacken with quantum |
| 2025 | "Bell" composition (ZX notation) |

## Compositional Approaches

### 1. Quantum Random (QRandom)

```python
from qiskit import QuantumCircuit, execute, Aer

def quantum_melody(n_notes, n_pitches=12):
    """Generate melody via quantum measurement."""
    qc = QuantumCircuit(4, 4)
    qc.h(range(4))  # Superposition
    qc.measure(range(4), range(4))
    
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=n_notes).result()
    
    melody = []
    for bitstring, count in result.get_counts().items():
        pitch = int(bitstring, 2) % n_pitches
        melody.extend([pitch] * count)
    
    return melody
```

### 2. Quantum Walk Composition

```python
def quantum_walk_melody(graph, steps):
    """Melody from quantum walk on graph."""
    from discopy.quantum import qubit, H, CNOT
    
    # Initialize walker in superposition
    walker = uniform_superposition(len(graph.nodes))
    
    for _ in range(steps):
        # Coin flip
        walker = apply_coin(walker)
        # Shift
        walker = apply_shift(walker, graph)
    
    # Measure to get note sequence
    return measure_melody(walker)
```

### 3. Grover Search for Harmony

```python
def find_chord(target_quality='major'):
    """Use Grover to find chord voicing."""
    # Oracle marks good voicings
    oracle = chord_quality_oracle(target_quality)
    
    # Grover iterations
    circuit = grover_circuit(oracle, n_qubits=12)
    
    # Measure result
    return measure_chord(circuit)
```

## ZX-Calculus Notation

"Bell" by Abdyssagin & Coecke uses ZX as score:

```
  Quantum Guitar          Grand Piano
       │                      │
    ┌──┴──┐                ┌──┴──┐
    │  X  │                │  Z  │
    └──┬──┘                └──┬──┘
       │                      │
       └──────────────────────┘
              Bell pair
              
  Measurement collapses entanglement
  → Correlated musical phrases
```

## Instruments

| Instrument | Creator | Mechanism |
|------------|---------|-----------|
| Q1Synth | Miranda et al. | Software qubit synth |
| Actias | Moth | Web-based, MIDI control |
| Quantum Guitar | Coecke | Physical + Actias |
| Quantum Piano | Abdyssagin | Mental model + notation |

## Genre Applications

### Industrial/Metal
- Black Tish: Full album with Quantum Guitar
- NIN-style experimentation
- Wacken performances

### Classical/Contemporary
- Cathedral Organ + Quantum Guitar
- "Quantum Universe" Symphony
- Chamber music with ZX notation

### Electronic
- EDM descendants of industrial
- Quantum random for generative

## DisCoPy for Composition

```python
from discopy import Ty, Box, Diagram
from discopy.quantum import qubit, Ket, Bra, H, CX

# Musical types
note = Ty('note')
chord = Ty('chord')

# Quantum composition as diagram
def compose_phrase():
    # Prepare Bell state
    bell = Ket(0, 0) >> (H @ Id(1)) >> CX
    
    # Map to musical space
    to_music = Box('sonify', qubit @ qubit, note @ note)
    
    return bell >> to_music
```

## Live Performance Protocol

```yaml
quantum_music_performance:
  setup:
    - Actias on dedicated laptop
    - MIDI routing configured
    - Bloch sphere projection
  
  soundcheck:
    - Test foot controllers
    - Verify measurement response
    - Classical/quantum blend levels
  
  performance:
    - Smooth classical→quantum transitions
    - Real-time qubit manipulation
    - Measured moments for phrase endings
```

## GF(3) Conservation in Music

| Section | Trit | Character |
|---------|------|-----------|
| Intro (classical) | -1 | Grounded |
| Development (quantum) | 0 | Superposed |
| Resolution (measured) | +1 | Collapsed |

**Σ = 0**: Complete musical arc conserves

## References

1. Miranda, E.R. (2022). Quantum Computer Music. Springer
2. Coecke, B. (2025). A Quantum Guitar. arXiv:2509.04526
3. Abdyssagin & Coecke (2025). Bell composition
4. Miranda et al. (2023). Q1Synth. Applied Sciences

---

**Skill Name**: quantum-music
**Type**: Composition / Performance
**Trit**: 0 (ERGODIC)

## Non-Backtracking Geodesic Qualification

**Condition**: μ(n) ≠ 0 (Möbius squarefree)

This skill is qualified for non-backtracking geodesic traversal.

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 1. Flexibility through Abstraction

**Concepts**: combinators, compose, parallel-combine, spread-combine, arity

### GF(3) Balanced Triad

```
quantum-music (○) + SDF.Ch1 (+) + [balancer] (−) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)


### Connection Pattern

Combinators compose operations. This skill provides composable abstractions.
