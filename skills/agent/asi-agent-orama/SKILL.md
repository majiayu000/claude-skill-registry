---
name: asi-agent-orama
description: ASI Agent-O-Rama Skill
version: 1.0.0
---

# ASI Agent-O-Rama Skill

**Status**: ✅ Production Ready
**Trit**: 0 (ERGODIC - coordinator)
**Integration**: Red Planet Labs Rama + ASI patterns

## Overview

Bridge between Agent-O-Rama (Rama-based agent platform) and ASI (Autonomous Superintelligence) patterns. Enables triadic agent orchestration with GF(3) conservation on Rama's distributed topology.

## Core Concepts

### TIDAR Integration
```clojure
;; Tree-structured Iterative Decomposition And Recombination
(defn tidar-agent [task seed]
  (let [children (splitmix-fork seed 3)]
    {:minus  (spawn-agent :validate task (nth children 0))
     :ergodic (spawn-agent :coordinate task (nth children 1))
     :plus   (spawn-agent :execute task (nth children 2))}))
```

### Rama Module Bridge
```clojure
(defagentmodule ASIAgentModule [setup topologies]
  (<<sources
    (source> *asi-tasks :> task)
    ;; Triadic decomposition
    (tidar-forward task :> subtasks)
    (batch<- subtasks :> results)
    (tidar-backward results :> final)
    (aor/result! final)))
```

## Commands

```bash
just asi-agent-start        # Start ASI agent module
just asi-tidar "task" seed  # Run TIDAR pipeline
just asi-gf3-verify         # Verify GF(3) conservation
```

## GF(3) Invariant

```
Σ(validator, coordinator, executor) = (-1) + (0) + (+1) = 0 (mod 3)
```

## See Also

- `rama-gay-clojure` - Rama with deterministic coloring
- `tidar` - TIDAR orchestration patterns
- `gay-mcp` - Color generation backend
- `bisimulation-game` - Skill dispersal with GF(3)

---

**Skill Name**: asi-agent-orama
**Type**: Agent Platform Bridge
**Trit**: 0 (ERGODIC)
**GF(3)**: Conserved via triadic spawn



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