---
name: recursive-string-diagrams
description: recursive-string-diagrams
version: 1.0.0
---

# recursive-string-diagrams

Recursive random string diagram generation with white trapezoid as the atomic skill primitive.

## Primitives

| Symbol | Name | Meaning |
|--------|------|---------|
| `◁═══▷` | **White Trapezoid** | Skill = morphism with typed ports |
| `∘` | Compose | Sequential skill chaining |
| `⊗` | Tensor | Parallel skill execution |
| `↺` | Trace | Feedback loop / recursion |

## GF(3) Trit Assignment

Each white trapezoid carries a trit:
- **MINUS (-1)**: Constraining/validating skill
- **ERGODIC (0)**: Neutral/transforming skill
- **PLUS (+1)**: Generating/expanding skill

Conservation: `Σ trits ≡ 0 (mod 3)` across diagram

## Usage

```clojure
;; Generate random diagram depth 4
(random-diagram 0 4)

;; Render ASCII
(render-ascii diagram 0)
```

## Example Output

```
⊗ tensor
  ↺ trace[1]
    ◁═══▷ [3→2] ergodic
  ∘ compose
    ◁═══▷ [2→2] minus
    ◁═══▷ [3→3] plus
```

## Semantics (Rama Connection)

| String Diagram | Rama Primitive |
|----------------|----------------|
| White Trapezoid | ETL topology |
| Compose (∘) | Depot chain |
| Tensor (⊗) | Parallel PStates |
| Trace (↺) | Recursive query |

## DisCoPy Integration

```python
from discopy import Ty, Box, Diagram

# White trapezoid as Box
skill = Box('skill', Ty('in'), Ty('out'))

# Compose
d1 >> d2

# Tensor
d1 @ d2

# Trace
d.trace(n)
```

## Skill Creation Protocol

1. **Seed**: White trapezoid with `[inputs → outputs]`
2. **Recurse**: Apply random `{∘, ⊗, ↺}` up to depth
3. **Color**: Assign GF(3) trits, verify conservation
4. **Render**: ASCII or DisCoPy SVG
5. **Save**: Write to `~/.claude/skills/<name>/SKILL.md`

## Related

- `discopy` - String diagram library
- `acsets` - Algebraic databases
- `rama-gay-clojure` - Rama + GF(3) colors