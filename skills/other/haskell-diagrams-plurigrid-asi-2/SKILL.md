---
name: haskell-diagrams
description: 'haskell-diagrams - Declarative Vector Graphics with Diagrams DSL'
version: 1.0.0
---

# haskell-diagrams - Declarative Vector Graphics with Diagrams DSL

## Overview

Integrates the Haskell [diagrams](https://hackage.haskell.org/package/diagrams) embedded domain-specific language for creating declarative vector graphics. Used for:

1. **Tsillerson Automata Visualization**: 2+1D lattice with vortex/antivortex defects
2. **Golden Thread Color Spirals**: φ-angle (137.508°) color progression
3. **Path Equivalence Diagrams**: Kleppmann-Bumpus-Gay path comparison
4. **GF(3) Trit Coloring**: Triadic conservation visualizations

**Trit**: +1 (PLUS) - Generates vector graphics artifacts

## Core Formula

```haskell
-- Diagrams is a monoid: composition via <>
diagram :: Diagram B
diagram = shape1 <> shape2 `atop` shape3

-- Transformation pipeline
transform :: Diagram B -> Diagram B
transform = scale 2 . rotate (45 @@ deg) . fc red
```

## Predicates

| Predicate | Description | GF(3) Role |
|-----------|-------------|------------|
| `DiagramValid(d)` | Diagram is well-formed | Structure |
| `ColorConserved(ds)` | Σ trits = 0 across diagrams | Conservation |
| `PathEquivalent(p1,p2)` | Visual fingerprints match | Equivalence |
| `GoldenAngle(θ)` | θ ≈ 137.508° | Dispersion |

## Architecture

```
┌────────────────────────────────────────────────────────────────┐
│                  Haskell Diagrams Pipeline                     │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Source (.hs)          Diagram B              Output           │
│       │                     │                     │             │
│       ▼                     ▼                     ▼             │
│  ┌──────────┐    ┌───────────────────┐    ┌─────────────┐      │
│  │ DSL Code │───▶│  Monoid Compose   │───▶│ SVG / PNG   │      │
│  │ shapes,  │    │  atop, beside,    │    │ PDF / PS    │      │
│  │ colors   │    │  vsep, hsep       │    │ Canvas      │      │
│  └──────────┘    └───────────────────┘    └─────────────┘      │
│                                                                 │
│   Backends: -fsvg (default), -fcairo, -frasterific, -fcanvas   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

## Triads (GF(3) = 0)

```
# Diagrams Generation Bundle
three-match (-1) ⊗ haskell-diagrams (0) ⊗ gay-mcp (+1) = 0 ✓  [Core Diagrams]
temporal-coalgebra (-1) ⊗ haskell-diagrams (0) ⊗ topos-generate (+1) = 0 ✓  [Animation]
sheaf-cohomology (-1) ⊗ haskell-diagrams (0) ⊗ rubato-composer (+1) = 0 ✓  [Music Notation]
persistent-homology (-1) ⊗ haskell-diagrams (0) ⊗ gay-mcp (+1) = 0 ✓  [TDA Viz]
```

## Installation

```bash
# Install with SVG backend (default)
cabal update && cabal install --lib diagrams diagrams-svg diagrams-contrib

# With cairo backend for PNG/PDF
cabal install gtk2hs-buildtools
cabal install --lib -fcairo diagrams

# With rasterific for Haskell-native PNG
cabal install --lib -frasterific diagrams
```

## Core API

### Shapes

```haskell
import Diagrams.Prelude

-- Basic shapes
circle 1         :: Diagram B
square 2         :: Diagram B  
rect 3 4         :: Diagram B
triangle 1       :: Diagram B
pentagon 1       :: Diagram B

-- Paths and trails
fromVertices [p2 (0,0), p2 (1,1), p2 (2,0)]
arc (0 @@ deg) (90 @@ deg)
```

### Composition

```haskell
-- Monoid: overlay at origin
d1 <> d2

-- Explicit overlay
d1 `atop` d2

-- Spatial arrangement
d1 ||| d2          -- beside horizontally
d1 === d2          -- beside vertically
hcat [d1, d2, d3]  -- horizontal list
vcat [d1, d2, d3]  -- vertical list
hsep 0.5 [d1, d2]  -- with spacing
vsep 0.5 [d1, d2]
```

### Styling

```haskell
-- Fill and stroke
diagram # fc red           -- fill color
diagram # lc blue          -- line color
diagram # lw thick         -- line width
diagram # opacity 0.5

-- Transforms
diagram # scale 2
diagram # rotate (45 @@ deg)
diagram # translate (r2 (1, 2))
```

### Colors (Gay.jl Integration)

```haskell
import Data.Colour.SRGB (sRGB24read)

-- Golden thread colors (seed 1069)
goldenThreadColors :: [Colour Double]
goldenThreadColors = map sRGB24read
  [ "#DD3C3C", "#3CDD6B", "#9A3CDD"  -- steps 1-3
  , "#DDC93C", "#3CC2DD", "#DD3C93"  -- steps 4-6
  , "#64DD3C", "#433CDD", "#DD723C"  -- steps 7-9
  ]

-- GF(3) trit colors
tritColor :: Trit -> Colour Double
tritColor Minus = sRGB24read "#2626D8"  -- Blue (validator)
tritColor Zero  = sRGB24read "#26D826"  -- Green (coordinator)
tritColor Plus  = sRGB24read "#D82626"  -- Red (generator)
```

## Tsillerson Automata Example

```haskell
-- Cell state visualization
data CellState = Empty | Vortex | Antivortex | Path0 | Path1 | Path2

cell :: CellState -> Diagram B
cell Empty       = square 1 # fc white # lw thin
cell Vortex      = circle 0.35 # fc vortexColor <> square 1 # lw thin
cell Antivortex  = circle 0.35 # fc antivortexColor <> square 1 # lw thin
cell Path0       = square 0.6 # fc path0Color <> square 1 # lw thin
cell Path1       = square 0.6 # fc path1Color <> square 1 # lw thin
cell Path2       = circle 0.3 # fc path2Color <> square 1 # lw thin

-- 8x8 lattice grid
latticeGrid :: [[CellState]] -> Diagram B
latticeGrid rows = vcat $ map (hcat . map cell) rows

-- Main diagram with legend
tsillersonDiagram :: Diagram B
tsillersonDiagram = vsep 0.5
  [ titleBlock
  , hsep 1 [latticeGrid initialLattice, legend]
  , goldenThreadBar
  ] # bg white # frame 0.5
```

## Animation Support

```haskell
import Diagrams.Backend.Cairo.CmdLine
import Diagrams.Animation

-- Animated diagram (t ∈ [0, 1])
spinningSquare :: Animation B V2 Double
spinningSquare = animEnvelope $ \t ->
  square 1 # rotate (t * 360 @@ deg) # fc (blend t red blue)

-- Render as GIF
main = mainWith spinningSquare
```

## Commands

```bash
just diagrams-install       # Install diagrams library
just diagrams-tsillerson    # Generate Tsillerson SVG
just diagrams-list          # List Haskell diagram files
just kbg-diagram-hs         # Generate KBG third diagram
```

## File Structure

```
lib/
├── TsillersonDiagram.hs    # 2+1D automata visualization
├── GoldenThread.hs         # φ-spiral color generation
└── PathEquivalence.hs      # Kleppmann-Bumpus-Gay comparison

diagrams/
├── tsillerson.svg          # Generated Tsillerson diagram
├── golden_thread.svg       # Golden angle color spiral
└── path_equiv.svg          # Path equivalence visualization
```

## Neighbor Awareness

| Position | Skill | Role |
|----------|-------|------|
| Left (-1) | `three-match` | Validates diagram constraints |
| Right (+1) | `gay-mcp` | Provides deterministic colors |

## References

- [diagrams.github.io](https://diagrams.github.io) - Official documentation
- [Hackage: diagrams](https://hackage.haskell.org/package/diagrams) - Package info
- [TsillersonDiagram.hs](file:///Users/bob/ies/music-topos/lib/TsillersonDiagram.hs) - Local implementation
- [diagrams-lib](https://hackage.haskell.org/package/diagrams-lib) - Core library

---

**Status**: ✅ L4 Admissible
**Trit**: 0 (ERGODIC) - Coordinates graphics generation
**Date**: 2025-12-25
