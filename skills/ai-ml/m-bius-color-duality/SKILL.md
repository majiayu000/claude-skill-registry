---
name: möbius-color-duality
description: Möbius inversion for Gay.jl color duality - closes sparsification spine gap
version: 1.0.0
---


# Möbius Color Duality Skill

> *"Möbius inversion recovers local structure from global aggregates."*

## The Gap

The Amp thread corpus (1,807 threads) is **85.6% mapped to sparsification spine** but has a critical gap:

```
Generation (Synthesis)     ████████░  49.2% ⭐ WELL-DEVELOPED
Validation (Verification)  ████░░░░░  21.6% ✓ SOLID
Execution (Control)        ███░░░░░░  15.2% ✓ ADEQUATE
Ontology (ACSet)           ██░░░░░░░   6.8% ⚠️ THIN
Decomposition (Hierarchy)  █░░░░░░░░   5.6% ⚠️ WEAK
Inversion (Duality)        ░░░░░░░░░   1.6% ❌ CRITICAL GAP
```

The system can **generate** but not **invert**. This skill closes that gap.

## Core Insight

**Forward (Generation)**: seed → color indices → structures  
**Backward (Inversion)**: structures → color distributions → recover seed

## Implementation

Module: `lib/gay_möbius_inversion.py` (490 lines)

Key classes:
- `ColorMöbiusInverter`: Numerical inversion for color spaces
- `TriadicColorInverter`: GF(3) ternary extension

## Status

✓ **Core implementation**: Möbius function, forward/backward inversion  
✓ **Duality graph generation**: Contravariant functor structures  
⊘ **GF(3) integration**: Ternary state extension  
⊘ **Amp corpus application**: Test on actual thread colorization  

## Sparsification Spine Integration

**Tier**: Layer 5 - INVERSION (Duality/Reversal)  
**Trit**: +1 (PLUS/Generator)  
**Coverage**: Begins to fill 1.6% → expand to 10%+ target