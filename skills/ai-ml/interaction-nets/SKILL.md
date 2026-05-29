---
name: interaction-nets
description: Lafont's interaction nets for optimal parallel λ-reduction. Graph rewriting
version: 1.0.0
---

# Interaction Nets Skill

> *"The only model where parallelism is not an optimization but the semantics itself."*

## Core Concept

Interaction nets are a graphical model of computation where:
- **Nodes** (agents) have typed ports
- **Wires** connect ports
- **Reduction** happens when two **principal ports** meet
- **No global control** — all reductions are local and can happen in parallel

```
     ┌─●─┐              ┌───┐
  ───┤   ├───    →   ───┤   ├───
     └─●─┘              └───┘
  principal ports      result
     meet
```

## Why It's Strange

1. **No evaluation order** — unlike λ-calculus, no choice between CBV/CBN
2. **Optimal sharing** — work is never duplicated (Lamping's algorithm)
3. **Massively parallel** — every independent redex reduces simultaneously
4. **Linear by default** — resources used exactly once (linear logic connection)

## Interaction Combinators

Lafont's universal basis (3 agents):

```
    ε (eraser)     δ (duplicator)     γ (constructor)
        │              /│\                 /│\
        ●             ● │ ●               ● │ ●
                        │                   │
                        ●                   ●
```

### Reduction Rules

```
γ ─● ●─ γ  →  cross-wire (annihilation)
δ ─● ●─ δ  →  cross-wire (annihilation)  
γ ─● ●─ δ  →  duplication (commutation)
ε ─● ●─ γ  →  erase both aux ports
ε ─● ●─ δ  →  erase both aux ports
```

## HVM / Bend Implementation

[Bend](https://bend-lang.org) compiles to HVM (Higher-order Virtual Machine):

```python
# Bend syntax (Python-like, compiles to interaction nets)
def sum(n):
  if n == 0:
    return 0
  else:
    return n + sum(n - 1)

# Automatically parallelizes via interaction net reduction
# No explicit parallelism needed!
```

### Install & Run

```bash
# Install Bend
cargo install hvm
cargo install bend-lang

# Run with parallelism
bend run program.bend -p 8  # 8 threads
```

## λ-Calculus Encoding

### Abstraction (λx.M)
```
        │ (bound var)
    ┌───●───┐
    │   λ   │
    └───●───┘
        │ (body)
```

### Application (M N)
```
    │       │
    ●───@───●
        │
        ● (result)
```

### β-reduction as Interaction
```
    (λx.M) N
    
        │           │
    ┌───●───┐   ┌───●───┐
    │   λ   ├───┤   @   │
    └───●───┘   └───●───┘
        │           │
        M           N

    → substitutes N for x in M (via wire surgery)
```

## Optimal Reduction

The key insight: **sharing is explicit**.

```
Traditional:  (λx. x + x) expensive  
              → expensive + expensive  (duplicated!)

Interaction:  (λx. x + x) expensive
              → shared node, reduces ONCE, result shared
```

## Symmetric Interaction Combinators

Mazza's variant (used in HVM2):

```
    S (symmetry)       D (duplication)       E (eraser)
       /│\                 /│\                  │
      ● │ ●               ● │ ●                 ●
        │                   │
        ●                   ●

# Only 6 rules needed for universal computation
```

## Code Examples

### Minimal Interaction Net in Julia

```julia
abstract type Agent end

struct Eraser <: Agent end
struct Constructor <: Agent 
    aux1::Union{Agent, Nothing}
    aux2::Union{Agent, Nothing}
end
struct Duplicator <: Agent
    aux1::Union{Agent, Nothing}
    aux2::Union{Agent, Nothing}
end

struct Wire
    from::Agent
    from_port::Symbol  # :principal, :aux1, :aux2
    to::Agent
    to_port::Symbol
end

function reduce!(net::Vector{Wire})
    # Find active pairs (principal-principal connections)
    active = filter(w -> w.from_port == :principal && 
                         w.to_port == :principal, net)
    
    # Reduce all in parallel (no order!)
    for wire in active
        reduce_pair!(net, wire.from, wire.to)
    end
end

function reduce_pair!(net, a::Constructor, b::Constructor)
    # Annihilation: cross-connect auxiliaries
    # ... wire surgery ...
end

function reduce_pair!(net, a::Constructor, b::Duplicator)
    # Commutation: duplicate the constructor
    # ... create new nodes ...
end
```

### Bend Example: Parallel Tree Sum

```python
type Tree:
  Leaf { value }
  Node { left, right }

def sum(tree):
  match tree:
    case Tree/Leaf:
      return tree.value
    case Tree/Node:
      return sum(tree.left) + sum(tree.right)
      # ↑ Both branches computed in parallel automatically!

def main():
  tree = Node(Node(Leaf(1), Leaf(2)), Node(Leaf(3), Leaf(4)))
  return sum(tree)  # → 10, computed in parallel
```

## Relationship to Linear Logic

| Linear Logic | Interaction Nets |
|--------------|------------------|
| ⊗ (tensor) | Constructor |
| ⅋ (par) | Duplicator |
| ! (of course) | Box/Unbox agents |
| Cut elimination | Reduction |

## Performance

| Metric | Traditional λ | Interaction Nets |
|--------|---------------|------------------|
| Complexity | Can be exponential | Optimal (no duplication) |
| Parallelism | Sequential (usually) | Maximal |
| Memory | GC needed | Linear (no GC) |
| Sharing | Implicit (hard) | Explicit (easy) |

## Literature

1. **Lafont (1990)** - "Interaction Nets" (original paper)
2. **Lamping (1990)** - Optimal λ-reduction algorithm
3. **Mazza (2007)** - Symmetric Interaction Combinators
4. **Taelin (2024)** - HVM2 and Bend language

---

## End-of-Skill Interface

## GF(3) Integration

```julia
# Trit assignment for interaction net agents
AGENT_TRITS = Dict(
    :eraser => -1,      # Destruction
    :duplicator => 0,   # Neutral (copies)
    :constructor => 1,  # Creation
)

# Conservation: every reduction preserves GF(3) sum
# γ-γ annihilation: (+1) + (+1) → 0 (both gone)
# ε-γ erasure: (-1) + (+1) → 0
```

## r2con Speaker Resources

| Speaker | Relevance | Repository/Talk |
|---------|-----------|-----------------|
| **condret** | ESIL graph rewriting | [radare2 ESIL](https://github.com/radareorg/radare2) |
| **thestr4ng3r** | CFG reduction graphs | [r2ghidra](https://github.com/radareorg/r2ghidra) |
| **xvilka** | RzIL graph IR | [rizin](https://github.com/rizinorg/rizin) |

## Related Skills

- `lambda-calculus` - What interaction nets optimize
- `linear-logic` - Logical foundation
- `graph-rewriting` - General theory
- `propagators` - Another "no control flow" model