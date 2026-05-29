---
name: discopy-operads
description: DiscoPy Operads Skill
version: 1.0.0
---

# DiscoPy Operads Skill

> **Repo Color:** `#64e3ec` | **Seed:** `0x128b6ef4564e3a00` | **Index:** 224/1055

DisCoPy: Python toolkit for computing with string diagrams, monoidal categories, and operads.

## bmorphism Contributions

> *"universal topos construction for social cognition and democratization of mathematical approach to problem-solving to all"*
> — [Plurigrid: the story thus far](https://gist.github.com/bmorphism/a400e174b9f93db299558a6986be0310)

**Operads as Skill Composition**: DisCoPy's operad module implements the colored operad structure that bmorphism uses for skill composition. Each skill is an operation with typed inputs/outputs; composition follows operad laws.

**Active Inference Connection**: The operadic structure enables hierarchical [Active Inference in String Diagrams](https://arxiv.org/abs/2308.00861) — nested perception-action loops where higher-level beliefs parameterize lower-level policies.

**GF(3) Colored Operads**: Following the paper "On the homotopy theory of equivariant colored operads" (Bonventre & Pereira), colors can encode trit values {-1, 0, +1} for balanced skill composition.

## Quick Reference

```python
from discopy.monoidal import Ty, Box, Id, Diagram
from discopy.grammar.cfg import Tree, Rule, Word, Operad, Algebra
from discopy import symmetric, braided, compact, frobenius, hypergraph
```

## String Diagram Syntax

```python
# Types are objects in monoidal categories
x, y, z = Ty('x'), Ty('y'), Ty('z')
unit = Ty()  # monoidal unit

# Tensor product (horizontal composition)
xy = x @ y  # x ⊗ y

# Boxes are morphisms
f = Box('f', x, y)           # f: x → y
g = Box('g', y, z)           # g: y → z

# Sequential composition (vertical)
fg = f >> g                   # g ∘ f: x → z

# Parallel composition (tensor of morphisms)
f_par_g = f @ g              # f ⊗ g: x ⊗ y → y ⊗ z

# Identity morphisms
idx = Id(x)                  # id_x: x → x

# Interchange law
d = Id(x) @ g >> f @ Id(z)   # = (f @ g).interchange(0, 1)
```

## Monoidal Category Operations

```python
# Dagger (adjoint)
f_dag = f[::-1]              # f†: y → x

# Diagram slicing
d = f >> g >> h
first_two = d[:2]            # f >> g
last_box = d[2]              # h

# Interchange normalization
for step in (f @ g).normalize():
    print(step)              # yields normal form steps

normal = d.normal_form()     # boundary-connected normal form
```

### Category Hierarchy

```
cat.Category
    └── monoidal.Category (planar diagrams)
        └── braided.Category (overcrossings)
            └── symmetric.Category (swaps)
                └── traced.Category (feedback loops)
                    └── compact.Category (cups/caps)
                        └── frobenius.Category (spiders)
```

## Operad Composition

```python
from discopy.grammar.cfg import Ty, Rule, Tree, Id, Operad

# Operads: multicategories with multi-input operations
x, y = Ty('x'), Ty('y')

# Rules are operad generators (atomic type codomain)
f = Rule(x @ x, x, name='f')  # f: x ⊗ x → x
g = Rule(x @ y, x, name='g')  # g: x ⊗ y → x
h = Rule(y @ x, x, name='h')  # h: y ⊗ x → x

# Tree construction via operadic composition
tree = f(g, h)               # plug g, h into f's inputs
assert tree == Tree(f, g, h)

# Axioms hold on the nose
assert Id(x)(f) == f == f(Id(x), Id(x))  # identity
left = f(Id(x), h)(g, Id(x), Id(x))
right = f(g, Id(x))(Id(x), Id(x), h)
assert f(g, h) == left == right          # associativity

# Nested diagram substitution (Patterson et al.)
diagram.substitute(i, other)  # replace box i with diagram other
```

### Nested Operad Composition (Advanced)

```python
from discopy.grammar.cfg import Ty, Rule, Tree, Id

# Multi-level nesting example
a, b, c = Ty('a'), Ty('b'), Ty('c')

# Arity-2 rules
add = Rule(a @ a, a, name='+')       # +: a ⊗ a → a
mul = Rule(a @ a, a, name='*')       # *: a ⊗ a → a
neg = Rule(a, a, name='-')           # -: a → a (unary)

# Deep composition: (a + b) * (-c)
# Corresponds to tree: mul(add(id_a, id_a), neg(id_a))
expr1 = mul(add, neg)                 # plug add and neg into mul's inputs
assert expr1.dom == a @ a @ a         # 3 leaves (a, a, a for left+, right*, and neg arg)

# Even deeper: ((a + b) * c) + (a * (b + c))
left_tree = mul(add, Id(a))           # (a + b) * c
right_tree = mul(Id(a), add)          # a * (b + c)  
full_expr = add(left_tree, right_tree)
print(f"Depth: {full_expr.depth}, Leaves: {len(list(full_expr.leaves))}")

# Operad morphism (algebra) evaluation
@Algebra.from_callable(a >> int)
def eval_int(rule: Rule, *args: int) -> int:
    if rule.name == '+': return args[0] + args[1]
    if rule.name == '*': return args[0] * args[1]
    if rule.name == '-': return -args[0]
    return args[0]

# Evaluate: (2 + 3) * (-4) = 5 * (-4) = -20
tree_with_leaves = mul(add(2, 3), neg(4))  # conceptual
```

### CFG Example

```python
n, d, v = Ty('N'), Ty('D'), Ty('V')
vp, np, s = Ty('VP'), Ty('NP'), Ty('S')

Caesar = Word('Caesar', n)
crossed = Word('crossed', v)
the, Rubicon = Word('the', d), Word('Rubicon', n)

VP = Rule(n @ v, vp)
NP = Rule(d @ n, np)
S = Rule(vp @ np, s)

sentence = S(VP(Caesar, crossed), NP(the, Rubicon))
# "Caesar crossed the Rubicon"
```

## Hypergraph Categories

```python
from discopy.hypergraph import Hypergraph, Spider

# Spiders: n-to-m operations with labeled nodes
spider = Spider(2, 3, label='x')  # 2 inputs, 3 outputs

# Wiring diagrams as cospans of hypergraphs
wires = (('a', 'b'), (('c',), ('d', 'e')), ('f',))
```

## Color Integration via Gay.jl

```python
# Initialize with repo seed
GAY_SEED = 0x128b6ef4564e3a00

def gay_color_box(box: Box, seed: int = GAY_SEED) -> str:
    """Generate deterministic color for diagram box."""
    h = hash((box.name, seed)) & 0xFFFFFFFF
    # SplitMix64 step
    h = ((h ^ (h >> 16)) * 0x85ebca6b) & 0xFFFFFFFF
    return f"#{h:06x}"[:7]

# Color diagram boxes
for box in diagram.boxes:
    color = gay_color_box(box)
    # Use in drawing.draw() with box_colors={box: color}
```

### GF(3) Trit Conservation

```python
def box_trit(box: Box) -> int:
    """Map box to balanced ternary trit."""
    return hash(box.name) % 3 - 1  # {-1, 0, +1}

def diagram_trit_sum(d: Diagram) -> int:
    """Diagrams conserve trit parity under composition."""
    return sum(box_trit(b) for b in d.boxes) % 3
```

### GF(3) Integration with Verification

```python
from discopy.monoidal import Box, Diagram, Ty
from typing import Dict, Tuple

# GF(3) = Z/3Z with balanced representation {-1, 0, +1}
class GF3Diagram:
    """Diagram with GF(3) trit annotations for conservation checking."""
    
    TRIT_NAMES = {-1: "MINUS", 0: "ZERO", 1: "PLUS"}
    
    def __init__(self, diagram: Diagram, trit_map: Dict[Box, int] = None):
        self.diagram = diagram
        self.trit_map = trit_map or {b: hash(b.name) % 3 - 1 for b in diagram.boxes}
    
    def total_trit(self) -> int:
        """Sum of trits mod 3, in balanced form."""
        s = sum(self.trit_map.values()) % 3
        return s if s <= 1 else s - 3
    
    def compose(self, other: 'GF3Diagram') -> 'GF3Diagram':
        """Compose diagrams, verify trit conservation."""
        new_diagram = self.diagram >> other.diagram
        new_trit_map = {**self.trit_map, **other.trit_map}
        result = GF3Diagram(new_diagram, new_trit_map)
        
        # Conservation check: sequential composition preserves total
        expected = (self.total_trit() + other.total_trit()) % 3
        expected = expected if expected <= 1 else expected - 3
        assert result.total_trit() == expected, "GF(3) conservation violated!"
        return result
    
    def verify_identity_neutral(self) -> bool:
        """Identity morphisms have trit 0 (neutral element)."""
        for box in self.diagram.boxes:
            if box.name.startswith('Id'):
                if self.trit_map.get(box, 0) != 0:
                    return False
        return True

# Usage
x, y = Ty('x'), Ty('y')
f = Box('f', x, y)  # trit = hash('f') % 3 - 1
g = Box('g', y, x)  # trit = hash('g') % 3 - 1

gf3_f = GF3Diagram(f)
gf3_g = GF3Diagram(g)
composed = gf3_f.compose(gf3_g)

print(f"f trit: {gf3_f.total_trit()}")
print(f"g trit: {gf3_g.total_trit()}")
print(f"f>>g trit: {composed.total_trit()}")
print(f"Conservation: {(gf3_f.total_trit() + gf3_g.total_trit()) % 3}")
```

## Hyperlang Embedding

```python
# Hyperlang: diagrams as executable specifications
from discopy.python import Function

# Interpret diagram as Python function
@Function.from_callable(x, y)
def f_impl(data):
    return transform(data)

# Functor maps syntax to semantics
F = Functor(
    ob={x: int, y: str},
    ar={f: f_impl},
    cod=Function
)

result = F(diagram)(input_data)
```

### Quantum Circuit Embedding

```python
from discopy.quantum import qubit, Ket, H, CX, Measure

# Quantum circuits as diagrams
circuit = Ket(0, 0) >> H @ qubit >> CX >> Measure() @ Measure()

# Interpret via tensor contraction
from discopy.quantum.circuit import Circuit
amplitude = circuit.eval()
```

## Drawing Diagrams

```python
from discopy.drawing import Equation

# Draw single diagram
diagram.draw(figsize=(8, 4))

# Draw equation
Equation(lhs, rhs).draw()

# Custom colors
diagram.draw(
    box_colors={f: '#64e3ec', g: '#150448'},
    wire_colors={x: '#ff0000'}
)
```

## Recent Commits (Dec 2024)

- `c456c37`: Fix generic type handling in assert_isinstance
- `467c8c4`: **Operadic composition** (#292) - nested diagram substitution
- `2cb5579`: Fix Frobenius bubble

## Links

- [DiscoPy Docs](https://discopy.readthedocs.io/)
- [GitHub](https://github.com/discopy/discopy)
- [Gay.jl Integration](https://github.com/bmorphism/Gay.jl)
- [Patterson et al. - Wiring Diagrams (arXiv:2101.12046)](https://arxiv.org/abs/2101.12046)

### Patterson et al. "Wiring Diagrams as Morphisms of Operads" (2021)

Key concepts from the paper:

1. **Wiring diagrams** = morphisms in an operad of typed, directed wires
2. **Operadic composition** = nested substitution of boxes
3. **Cospans of hypergraphs** = the universal property for wiring

```python
# Patterson's wiring diagram composition pattern
# (Box A with 2 outputs) composed with (Box B taking 2 inputs)

from discopy.hypergraph import Hypergraph, Spider

# Outer box: 2 inputs, 2 outputs
outer = Hypergraph(
    dom=['in1', 'in2'], 
    cod=['out1', 'out2'],
    boxes=[Spider(2, 2, 'process')]
)

# Inner box to substitute: 1 input, 1 output  
inner = Hypergraph(
    dom=['x'],
    cod=['y'],
    boxes=[Spider(1, 1, 'transform')]
)

# Operadic substitution: replace one port of outer with inner
# This is the key insight - wiring diagrams compose as operad morphisms
```

**Citation**:
```bibtex
@article{patterson2021wiring,
  title={Wiring diagrams as normal forms for computing in symmetric monoidal categories},
  author={Patterson, Evan and Baas, Amar and Hosgood, Timothy and Fairbanks, James},
  journal={arXiv:2101.12046},
  year={2021}
}
```

---

*Chromatic seed: `0x128b6ef4564e3a00` | Color: `#64e3ec`*



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `category-theory`: 139 citations in bib.duckdb
- `operads`: 5 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 9. Generic Procedures

**Concepts**: dispatch, multimethod, predicate dispatch, generic

### GF(3) Balanced Triad

```
discopy-operads (+) + SDF.Ch9 (○) + [balancer] (−) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch5: Evaluation
- Ch3: Variations on an Arithmetic Theme
- Ch1: Flexibility through Abstraction
- Ch4: Pattern Matching
- Ch2: Domain-Specific Languages
- Ch6: Layering

### Connection Pattern

Generic procedures dispatch on predicates. This skill selects implementations dynamically.
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