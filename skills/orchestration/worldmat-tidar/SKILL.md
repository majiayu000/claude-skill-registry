---
name: worldmat-tidar
description: worldmat-tidar
version: 1.0.0
---

# worldmat-tidar

> World Matrices via TiDAR Executions: 3×3×3 Parallel Triadic Computation

**Version**: 1.0.0
**Trit**: 0 (ERGODIC - coordinates execution)
**Color**: #55D9A0

## Overview

**Worldmat** is a 3×3×3 matrix of TiDAR executions where:
- **Rows**: MINUS/ERGODIC/PLUS polarities (GF(3) agents)
- **Columns**: PAST/PRESENT/FUTURE temporal phases
- **Depth**: OBSERVATION/ACTION/PREDICTION modalities

Each cell executes the TiDAR pattern:
1. **DIFFUSION**: Draft tokens in parallel (like SplitRng.split)
2. **AR VERIFY**: Verify sequentially (autoregressive)

## Architecture

```
                    TEMPORAL AXIS
                 PAST    PRESENT   FUTURE
                  ↓        ↓        ↓
            ┌─────────────────────────────┐
            │  ┌───┐ ┌───┐ ┌───┐         │
     MINUS  │  │-1 │ │ 0 │ │+1 │  ← GF(3)=0
            │  └───┘ └───┘ └───┘         │
POLARITY    │  ┌───┐ ┌───┐ ┌───┐         │
     ERGODIC│  │ 0 │ │+1 │ │-1 │  ← GF(3)=0
            │  └───┘ └───┘ └───┘         │
            │  ┌───┐ ┌───┐ ┌───┐         │
     PLUS   │  │+1 │ │-1 │ │ 0 │  ← GF(3)=0
            │  └───┘ └───┘ └───┘         │
            └─────────────────────────────┘
                  ↑    ↑    ↑
               GF(3)=0 for each column
```

## Key Properties

| Property | Value | Guarantee |
|----------|-------|-----------|
| **GF(3) Conservation** | All slices sum to 0 | Row, Column, Depth |
| **SPI** | Same seed → Same result | Parallel or Sequential |
| **Spectral Gap** | 0.25 (1/4) | Ergodic mixing |
| **Cells** | 27 | 3³ TiDAR executions |

## TiDAR Pattern (arXiv:2511.08923)

```python
# Phase 1: DIFFUSION (parallel drafting)
def diffusion_draft(self, n_tokens: int = 8):
    streams = self.rng.split(n_tokens)
    return [stream.next()[0] for stream in streams]

# Phase 2: AR VERIFY (sequential verification)
def ar_verify(self):
    prev = self.seed
    for token in self.draft_tokens:
        verified = mix64(prev ^ token)
        self.verified_tokens.append(verified)
        prev = verified
```

## Work Stealing

Idle agents steal work from busy agents:

```python
class WorkStealingScheduler:
    def steal_work(self, thief: Polarity) -> Optional[TiDARCell]:
        busiest = max(self.queues.keys(), key=lambda p: len(self.queues[p]))
        if busiest != thief and self.queues[busiest]:
            return self.queues[busiest].pop(0)
        return None
```

## ACSet Export

```python
wm = Worldmat(master_seed=0x87079c9f1d3b0474)
wm.execute_parallel()
acset = wm.to_acset()
# Returns: {schema, parts, subparts, metadata}
```

## Commands

```bash
# Run demo
python worldmat.py

# Verify SPI
python worldmat.py verify

# Export ACSet
python worldmat.py acset > worldmat.json
```

## GF(3) Triads

```
worldmat-tidar (0) forms balanced triads:

three-match (-1) ⊗ worldmat-tidar (0) ⊗ gay-mcp (+1) = 0 ✓
spi-parallel-verify (-1) ⊗ worldmat-tidar (0) ⊗ triad-interleave (+1) = 0 ✓
tidar_streaming (-1) ⊗ worldmat-tidar (0) ⊗ gay_triadic_exo (+1) = 0 ✓
```

## Integration

### With OpenAI ACSet

```python
from worldmat import Worldmat
from openai_acset import build_openai_acset

# Process conversations through worldmat
wm = Worldmat(master_seed=conv_fingerprint)
wm.execute_parallel()

# Each message → cell in worldmat
# Role (user/assistant/tool) → polarity
# Time → temporal phase
# Type (obs/action/pred) → modality
```

### With Gay-MCP

```python
from gay import SplitMixTernary

# Worldmat colors from Gay-MCP
gen = SplitMixTernary(seed=worldmat.fingerprint())
palette = gen.palette_hex(n=27)  # One color per cell
```

## Files

| File | Purpose |
|------|---------|
| `worldmat.py` | Core implementation |
| `SKILL.md` | This documentation |

## References

- TiDAR: arXiv:2511.08923
- Gay.jl/src/spc_repl.jl - Whale synergy matrix
- rio/gayzip/tidar_streaming.py - TiDAR ZIP implementation
- gay_triadic_exo.py - Triadic agent orchestration

Base directory: file:///Users/bob/.claude/skills/worldmat-tidar



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