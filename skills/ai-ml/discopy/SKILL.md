---
name: discopy
description: "DisCoPy: Python library for computing with string diagrams - monoidal"
version: 1.0.0
---

# DisCoPy: String Diagrams in Python

> *"String diagrams are the syntax, functors are the semantics."*

## bmorphism Contributions

> *"all is bidirectional"*
> — [@bmorphism](https://gist.github.com/bmorphism/ead83aec97dab7f581d49ddcb34a46d4), Play/Coplay gist

**Active Inference Implementation**: DisCoPy provides the foundation for implementing [Active Inference in String Diagrams](https://arxiv.org/abs/2308.00861) (Tull, Kleiner, Smithe). The paper's core insight — that perception and action form a bidirectional loop — maps directly to DisCoPy's composition operators:
- **Sequential** (`>>`) → temporal flow (action → perception → action)
- **Parallel** (`@`) → concurrent sensory channels
- **Dagger** (`[::-1]`) → time reversal (perception as action's adjoint)

**Categorical Cybernetics**: DisCoPy's parametrised optics implement the cybernetic lens pattern from [Towards Foundations of Categorical Cybernetics](https://arxiv.org/abs/2105.06332), enabling the Play/Coplay duality bmorphism references.

**String Diagram Coloring**: Gay.jl colors can be applied to DisCoPy diagrams for deterministic visualization — each wire type gets a consistent color from the splittable RNG.

## Overview

DisCoPy is a Python library for computing with **string diagrams** - the graphical language of monoidal categories. It provides:

1. **Categorical Framework**: Ty, Ob, Box, Arrow, Diagram, Category
2. **Operads**: CFG as free operads, operad algebras, colored operads
3. **Quantum Computing**: Circuits, gates, ZX-calculus, pytket/qiskit integration
4. **QNLP**: Pregroup grammars, DisCoCat, ansätze for quantum NLP
5. **Tensor Networks**: NumPy/JAX/PyTorch backends, tensornetwork contraction
6. **Visualization**: Matplotlib/TikZ drawing with color customization

---

## Core Architecture (DeepWiki 2025-12-22)

### Class Hierarchy

```
Category
├── ob: Ob (objects/systems)
└── ar: Arrow (morphisms/processes)

Ob → Ty (monoidal: tuple of objects, tensor = concatenation)

Arrow → Diagram (monoidal: boxes + offsets, parallel composition)
     └── Box (atomic operations with dom/cod)
```

### Composition Operators

| Operator | Method | Description |
|----------|--------|-------------|
| `>>` | `then` | Sequential: f >> g (f.cod == g.dom) |
| `@` | `tensor` | Parallel: f @ g (side-by-side) |
| `[::-1]` | `dagger` | Adjoint/reverse |

```python
from discopy.monoidal import Ty, Box, Diagram

x, y, z = Ty('x'), Ty('y'), Ty('z')
f = Box('f', x, y)
g = Box('g', y, z)

# Sequential: x → y → z
sequential = f >> g

# Parallel: x ⊗ y → y ⊗ z
parallel = f @ g

# Both: (f ⊗ id) >> (id ⊗ g)
mixed = f @ Diagram.id(y) >> Diagram.id(y) @ g
```

---

## Operads (DeepWiki 2025-12-22)

DisCoPy implements operads via `discopy.grammar.cfg`:

### Operad Structure

- **Colors**: `Ty` objects (types of operations)
- **Operations**: `Tree` objects (composable rules)
- **Algebras**: `Functor` from free operad to target operad

```python
from discopy.grammar.cfg import Ty, Rule, Word, Tree

# Define colors (types)
n, v, s = Ty('N'), Ty('V'), Ty('S')
vp, np = Ty('VP'), Ty('NP')

# Define operations (rules)
Caesar = Word('Caesar', n)
crossed = Word('crossed', v)
VP = Rule(n @ v, vp)
NP = Rule(Ty('D') @ n, np)
S = Rule(vp @ np, s)

# Build tree (operadic composition)
sentence = S(VP(Caesar, crossed), NP(Word('the', Ty('D')), Word('Rubicon', n)))
# Axioms of multicategories (operads) hold on the nose
```

### Colored Operads

Types (`Ty`) act as colors - operations can have different input/output colors:

```python
x, y = Ty('x'), Ty('y')
f = Rule(x @ x, x, name='f')   # x ⊗ x → x
g = Rule(x @ y, x, name='g')   # x ⊗ y → x  
h = Rule(y @ x, x, name='h')   # y ⊗ x → x

# Operadic composition
assert f(g, h) == Tree(f, *[g, h])
```

---

## Color Configuration (DeepWiki 2025-12-22)

### Default Color Palette

```python
from discopy.config import COLORS

COLORS = {
    "white": "#ffffff",
    "red": "#e8a5a5",
    "green": "#d8f8d8", 
    "blue": "#776ff3",
    "yellow": "#f7f700",
    "black": "#000000"
}
```

### ZX-Calculus Colors

```python
from discopy.quantum.zx import Z, X, Y

# Z spiders: GREEN
Z(1, 1, phase=0.5).color  # "green"

# X spiders: RED  
X(1, 1, phase=0.25).color  # "red"

# Y spiders: BLUE
Y(1, 1).color  # "blue"
```

### Custom Box Colors

```python
from discopy.monoidal import Ty, Box

x = Ty('x')
blue_box = Box('f', x, x, color="blue")
blue_box.draw()

# Spider with custom color
from discopy.frobenius import Spider
spider = Spider(2, 3, x)
spider.color = "red"
spider.draw_as_spider = True
```

### Drawing API

```python
diagram.draw(
    figsize=(8, 6),
    color="blue",           # Default box color
    draw_as_nodes=True,     # Draw boxes as nodes
    wire_labels=True,       # Show type labels on wires
    draw_box_labels=True,   # Show box names
    path="output.png",      # Save to file
    to_tikz=True           # Output TikZ code
)
```

---

## Quantum Computing (DeepWiki 2025-12-22)

### Quantum Circuits

```python
from discopy.quantum import qubit, H, X, CX, Ket, Bra, Measure

# Bell state preparation
bell = Ket(0, 0) >> H @ qubit >> CX

# Evaluation
state_vector = bell.eval()  # Returns Tensor[complex]

# Measurement probability
experiment = Ket(0, 0) >> bell >> Bra(0, 0)
amplitude = experiment.eval().array
probability = abs(amplitude) ** 2
```

### Gate Library

| Gate | Description | Code |
|------|-------------|------|
| H | Hadamard | `H` |
| X, Y, Z | Pauli | `X`, `Y`, `Z` |
| CX, CZ | Controlled | `CX`, `CZ` |
| Rx, Ry, Rz | Rotation | `Rx(phase)`, `Ry(phase)`, `Rz(phase)` |
| Ket, Bra | State prep/measure | `Ket(0, 1)`, `Bra(0, 0)` |

### External Integration

```python
# pytket integration
from discopy.quantum.tk import mockBackend

circuit = H @ qubit >> CX >> Measure() @ Measure()
tk_circuit = circuit.to_tk()  # Convert to pytket

# Run on backend
backend = mockBackend({(0, 1): 512, (1, 0): 512})
counts = circuit.eval(backend=backend, n_shots=1024)

# PennyLane integration
pennylane_qnode = circuit.to_pennylane()
```

### ZX-Calculus

```python
from discopy.quantum.zx import Z, X, circuit2zx

# Convert circuit to ZX diagram
zx_diagram = circuit2zx(circuit)

# Z spider (green) with phase
z_spider = Z(2, 1, phase=0.5)

# X spider (red) with phase  
x_spider = X(1, 2, phase=0.25)

# PyZX integration for optimization
pyzx_graph = zx_diagram.to_pyzx()
# Apply PyZX simplification algorithms
simplified = pyzx_graph.simplify()
```

---

## QNLP (DeepWiki 2025-12-22)

### Pregroup Grammar

```python
from discopy.grammar.pregroup import Ty, Word, Cup, Diagram

s, n = Ty('s'), Ty('n')

Alice = Word('Alice', n)
loves = Word('loves', n.r @ s @ n.l)
Bob = Word('Bob', n)

# Parse sentence
sentence = Alice @ loves @ Bob >> Cup(n, n.r) @ s @ Cup(n.l, n)
sentence.draw()
```

### DisCoCat: Diagrams to Quantum Circuits

```python
from discopy.quantum import circuit, qubit, Ket, H, CX
from discopy.cat import Category

# Define semantic functor
F = circuit.Functor(
    ob={s: qubit ** 0, n: qubit ** 1},  # Type → Qubits
    ar={
        Alice: Ket(0),
        loves: sqrt(2) @ Ket(0, 0) >> H @ X >> CX,
        Bob: Ket(1)
    }
)
F.dom = Category(Ty, Diagram)

# Apply functor to get quantum circuit
quantum_sentence = F(sentence)
quantum_sentence.draw()
```

### Ansätze

Parameterized quantum circuits for word meanings:

```python
from discopy.quantum.ansatze import IQPAnsatz, Sim14Ansatz

# IQP ansatz for nouns
noun_ansatz = IQPAnsatz(n_qubits=2, n_layers=3)

# Sim14 ansatz for verbs
verb_ansatz = Sim14Ansatz(n_qubits=4, n_layers=2)
```

---

## Tensor Networks (DeepWiki 2025-12-22)

### Multi-Backend Support

```python
from discopy.tensor import Tensor, backend
import jax.numpy
import torch

# Default: NumPy
assert isinstance(Tensor.id().array, np.ndarray)

# JAX backend
with backend('jax'):
    assert isinstance(Tensor.id().array, jax.numpy.ndarray)

# PyTorch backend
with backend('pytorch'):
    assert isinstance(Tensor.id().array, torch.Tensor)
```

### Functor to Tensors

```python
from discopy.tensor import Dim, Tensor, Functor
from discopy.cat import Category

# Define tensor functor
F = Functor(
    ob={n: Dim(2), s: Dim(1)},
    ar={
        Alice: [1, 0],
        loves: [[0, 1], [1, 0]],
        Bob: [0, 1]
    },
    cod=Category(Dim, Tensor)
)

result = F(sentence)
```

### Contraction with tensornetwork

```python
import tensornetwork as tn
from discopy.tensor import Box, Dim

vector = Box('v', Dim(1), Dim(2), [0, 1])
contracted = (vector >> vector[::-1]).eval(contractor=tn.contractors.auto)
```

---

## Advanced Categories (DeepWiki 2025-12-22)

### Hypergraph Categories

```python
from discopy.hypergraph import Hypergraph

# Canonical form for diagram equality
hyp = diagram.to_hypergraph()
# Composition via pushouts
```

### Frobenius Algebras and Spiders

```python
from discopy.frobenius import Spider, Diagram

x = Ty('x')

# Special commutative Frobenius algebra
spider = Spider(n_legs_in=2, n_legs_out=3, typ=x)

# Unfuse to canonical primitives
primitives = diagram.unfuse()
```

### Markov Categories

```python
from discopy.markov import Copy, Merge, Discard, Diagram

x = Ty('x')

# Copy wire n times
copy = Diagram.copy(x, n=2)

# Merge n wires to one
merge = Diagram.merge(x, n=2)

# Discard wire
discard = Diagram.copy(x, n=0)  # Copy with n=0
```

### Traced Categories

```python
from discopy.traced import Diagram

# Feedback loop: output fed back to input
traced = diagram.trace()
```

---

## GF(3) Triad Integration

DisCoPy as ERGODIC coordinator (trit 0):

```
three-match (-1) ⊗ discopy (0) ⊗ gay-mcp (+1) = 0 ✓  [Diagram Coloring]
sheaf-cohomology (-1) ⊗ discopy (0) ⊗ operad-compose (+1) = 0 ✓  [Operadic]
proofgeneral-narya (-1) ⊗ discopy (0) ⊗ rubato-composer (+1) = 0 ✓  [Music]
persistent-homology (-1) ⊗ discopy (0) ⊗ gay-mcp (+1) = 0 ✓  [Quantum]
```

### Color ↔ Gay.jl Integration

```python
from discopy.monoidal import Box, Ty

# Use Gay.jl deterministic colors for boxes
def gay_colored_box(name, dom, cod, seed, index):
    """Create box with deterministic color from Gay.jl"""
    # Gay.jl: golden angle dispersion
    hue = ((seed * 0x9E3779B97F4A7C15 + index) >> 16) % 360
    hex_color = hsl_to_hex(hue, 0.7, 0.55)
    return Box(name, dom, cod, color=hex_color)

# Example: colored diagram
x = Ty('x')
boxes = [gay_colored_box(f'f{i}', x, x, 0x42D, i) for i in range(5)]
```

---

---

---

## DeepWiki Integration Notes

| Query Topic | Key Insight |
|-------------|-------------|
| Core Architecture | Ty→Ob→Arrow→Diagram hierarchy, >> and @ operators |
| Operads | CFG as free operads, Tree = operations, Algebra = functor |
| Colors | COLORS dict, ZX: Z=green, X=red, Y=blue |
| Quantum | Circuit.eval(), pytket/PennyLane integration |
| QNLP | Pregroup → Diagram → Functor → Quantum Circuit |
| Tensor Networks | backend() context, tensornetwork contractors |
| Hypergraph | Canonical form via cospans, equality checking |
| ZX-Calculus | circuit2zx, PyZX optimization, phase gates |

**DeepWiki URL**: https://deepwiki.com/discopy/discopy

---

**Version**: 2.0.0
**Trit**: 0 (ERGODIC - coordinates categorical computation)
**GF(3)**: Substitutes for other ERGODIC skills in triads
**Qualified**: 2025-12-22 (8 DeepWiki interactions)

---

## End-of-Skill Interface

## Commands

```bash
just discopy-demo           # Run DisCoPy demonstration
just discopy-quantum        # Quantum circuit examples
just discopy-qnlp          # QNLP parsing examples
just discopy-zx            # ZX-calculus optimization
just discopy-tensor        # Tensor network contraction
just discopy-operad        # Operad composition examples
```

## Related Skills

- **operad-compose**: Operadic composition patterns (+1)
- **gay-mcp**: Deterministic colors for diagram elements (+1)
- **proofgeneral-narya**: Type-theoretic diagram verification (-1)
- **rubato-composer**: Musical diagram applications (+1)
- **three-match**: 3-coloring for diagram validation (-1)

## r2con Speaker Resources

Color and diagram repositories from r2con speakers relevant to DisCoPy:

| Speaker | Repository | Relevance |
|---------|-----------|-----------|
| bmorphism | [bmorphism/Gay.jl](https://github.com/bmorphism/Gay.jl) | Deterministic diagram coloring |
| bmorphism | [bmorphism/r2-zignatures](https://github.com/bmorphism/r2-zignatures) | Function signatures as categorical objects |
| pancake | [radare2/radare2](https://github.com/radare2/radare2) | CFG as monoidal diagrams |
| thestr4ng3r | [rizinorg/cutter](https://github.com/rizinorg/cutter) | Graph visualization backend |