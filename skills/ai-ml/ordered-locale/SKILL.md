---
name: ordered-locale
description: Ordered Locale Skill
version: 1.0.0
---

# Ordered Locale Skill

**Trit**: +1 (PLUS/GENERATOR)
**GF(3)**: Σ(-1,0,+1) = 0 (conserved)

## Overview

Point-free topology with direction. MCP servers indexed by creation-time color via SplitMix64. Every decision trifurcates into MINUS/ERGODIC/PLUS parallel paths. GF(3) conservation guaranteed on every substrate in every interaction.

Implements Heunen-style ordered locales with observational bridge types in Narya proof assistant. Bridge types model the "way below" relation U ≪ V in ordered locales, providing a foundation for:

- **MCP Locale**: Servers as opens, dependencies as way-below
- Causal structure in topological spaces
- Directed homotopy theory
- Sheaves respecting directional constraints
- GF(3) triadic systems

## Files

| File | Description |
|------|-------------|
| `mcp_locale.py` | Python: MCP ordered locale with triadic decisions |
| `mcp_locale.mo` | Modelica: Acausal model (replaces Wolfram) |
| `narya/ordered_locale.ny` | Core definitions: 𝟚, Bridge, WayBelow, frame ops |
| `narya/gf3.ny` | GF(3) arithmetic and conservation |
| `narya/bridge_sheaf.ny` | Sheaves respecting bridge structure |
| `narya/narya-ordered-locale.el` | Emacs/Proof General integration |
| `ordered_locale.jl` | Julia: Frame operations, cones/cocones |

## MCP Locale

Every MCP server is an **open set** in the locale, indexed by creation-time color:

```python
from mcp_locale import create_mcp_locale, trifurcate_decision

locale = create_mcp_locale(seed=0x42D)
# Each MCP gets deterministic color: seed → SplitMix64 → RGB → hue → trit
```

### Triadic Decisions

Every decision trifurcates into parallel paths:

| Path | Trit | Role | Action |
|------|------|------|--------|
| MINUS | -1 | Validator | Check constraints |
| ERGODIC | 0 | Coordinator | Find optimal route |
| PLUS | +1 | Executor | Generate result |

```python
decision = trifurcate_decision(
    "swap 10 APT",
    seed=0x42D,
    minus_fn=validate,
    ergodic_fn=coordinate,
    plus_fn=execute,
    aggregate_fn=aggregate
)
# GF(3): -1 + 0 + 1 = 0 ✓
```

### Safe Parallelism via SplitMix64

```python
def splitmix_ternary(seed):
    """Fork into 3 independent streams."""
    s1 = splitmix64(seed)
    s2 = splitmix64(s1)
    s3 = splitmix64(s2)
    return (s1, s2, s3)  # MINUS, ERGODIC, PLUS
```

Each substrate (Python, Julia, Babashka, Modelica) uses identical SplitMix64, ensuring reproducible parallel execution.

## Key Concepts

### Bridge Types

A bridge from A to B is a directed path through the directed interval 𝟚:

```
def Bridge (A B : Type) : Type := sig (
  path : 𝟚 → Type,
  start : path zero. → A,
  end : B → path one.
)
```

### Way Below (≪)

The way-below relation U ≪ V captures "U is compact relative to V":

```
def WayBelow (U V : Open) : Type := sig (
  bridge : (t : 𝟚) → Open,
  at_zero : ... → U,
  at_one : V → ...,
  directed : ...
)
```

### GF(3) Conservation

All triadic structures conserve sum ≡ 0 (mod 3):

```
def GF3Conserved (a b c : Trit) : Type := 
  Id Trit (trit_sum3 a b c) ergodic.
```

## Commands

```bash
# Verify all files
~/.agents/skills/ordered-locale/narya/run_narya.sh

# Check GF(3) only
~/.agents/skills/ordered-locale/narya/run_narya.sh --gf3

# Run via headless Emacs
~/.agents/skills/ordered-locale/narya/run_narya.sh --emacs
```

## Emacs Integration

```elisp
;; Load the mode
(load "~/.agents/skills/ordered-locale/narya/narya-ordered-locale.el")

;; Key bindings
;; C-c C-n  Step forward
;; C-c C-u  Step backward
;; C-c C-v  Verify all
;; C-c C-g  Check GF(3)
```

## Related Skills

- `proofgeneral-narya` - Proof General + Narya integration
- `gf3` / `gay-mcp` - Triadic color systems
- `segal-types` - Synthetic ∞-categories
- `unworld` - Derivational chains
- `triad-interleave` - Parallel triadic scheduling
- `coequalizers` (0) - Sheaf gluing as dual of coequalizer

## References

- Heunen, C. - "Ordered Locales" (in `~/worlds/ordered-locales/heunen_orderedlocales.pdf`)
- Riehl-Shulman - "A type theory for synthetic ∞-categories" 
- Narya proof assistant - https://github.com/gwaithimirdain/narya

## Mathematical Foundation

Ordered locales extend frame theory with a compatible partial order on opens. The key axiom is:

> Every open V is the join of opens U with U ≪ V

This approximation property connects point-free topology to domain theory and provides a constructive foundation for causal structure.

The bridge type formalization captures ≪ as a directed homotopy: paths that flow from U toward V through the directed interval 𝟚 = {0 → 1}.



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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