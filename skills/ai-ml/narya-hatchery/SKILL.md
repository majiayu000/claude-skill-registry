---
name: narya-hatchery
description: Narya Hatchery
version: 1.0.0
---

# Narya Hatchery

---
name: narya-hatchery
description: Higher-dimensional type theory proof assistant with observational Id/Bridge types, parametricity, and ProofGeneral integration.
trit: 0
color: "#3A71C0"
---

## Overview

**Narya** is a proof assistant implementing Multi-Modal, Multi-Directional, Higher/Parametric/Displayed Observational Type Theory.

## Core Features

- **Normalization-by-evaluation** algorithm and typechecker
- **Observational-style theory** with Id/Bridge types satisfying parametricity
- **Variable arity and internality** for bridge types
- **User-definable mixfix notations**
- **Record types, inductive datatypes, coinductive codatatypes**
- **Matching and comatching case trees**
- **Import/export and separate compilation**
- **Typed holes** with later solving
- **ProofGeneral interaction mode**

## Type Theory Features

### Bridge Types with Parametricity

```narya
-- Observational identity via bridges
bridge : (A : Type) → (x y : A) → Bridge x y → x ≡ y
```

### Higher-Dimensional Structure

Narya supports higher-dimensional type theory where:
- Types can have internal dimensions
- Parametricity is built into the type theory
- Bridge types generalize equality

## Gay.jl Integration

```julia
# Initialize with Narya's chromatic seed
gay_seed!(0xbfe738ce2e1c5f1f)

# P3 extension gamut learning
function loss(params, seed, target_gamut=:p3_extension)
    color = forward_color(params, projection, seed)
    return out_of_gamut_distance(color, target_gamut)
end
```

## Installation

```bash
# From source
git clone https://github.com/mikeshulman/narya
cd narya
dune build
```

## Documentation

- [Installation Guide](https://narya.readthedocs.io/en/latest/installation.html)
- [Full Documentation](https://narya.readthedocs.io/en/latest/)
- [Contributing](https://narya.readthedocs.io/en/latest/contributing.html)

## Repository

- **Source**: TeglonLabs/narya (fork of mikeshulman/narya)
- **Seed**: `0xbfe738ce2e1c5f1f`
- **Index**: 49/1055
- **Color**: #d6621c

## GF(3) Triad

```
proofgeneral-narya (-1) ⊗ narya-hatchery (0) ⊗ gay-mcp (+1) = 0 ✓
```

## Related Skills

- `proofgeneral-narya` - Emacs integration
- `holes` - Interactive proof development
- `move-narya-bridge` - Move contract verification