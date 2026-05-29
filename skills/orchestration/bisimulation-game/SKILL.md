---
name: bisimulation-game
description: "Bisimulation game for resilient skill dispersal across AI agents with GF(3) conservation and observational bridge types."
source: music-topos + DiscoHy + DisCoPy
license: MIT
xenomodern: true
ironic_detachment: 0.42
---

# Bisimulation Game Skill

> *"Two systems are bisimilar if they cannot be distinguished by any observation."*

## Overview

The bisimulation game provides a framework for:
1. **Resilient skill dispersal** across multiple AI agents
2. **GF(3) conservation** during state transitions
3. **Observational bridge types** for version-aware synchronization
4. **Self-rewriting capabilities** via MCP Tasks protocol

## Game Rules

### Players

| Player | Role | Trit | Color |
|--------|------|------|-------|
| Attacker | Tries to distinguish systems | -1 | Blue |
| Defender | Maintains equivalence | +1 | Red |
| Arbiter | Verifies conservation | 0 | Green |

### Moves

```
┌─────────────────────────────────────────────────────────────┐
│  Round n:                                                   │
│                                                             │
│  1. Attacker chooses: system S₁ or S₂                       │
│  2. Attacker makes: transition s₁ →ᵃ s₁'                    │
│  3. Defender responds: matching transition s₂ →ᵃ s₂'        │
│  4. Arbiter verifies: GF(3) conservation                    │
│                                                             │
│  If Defender cannot respond → Attacker wins (distinguishable)│
│  If game continues forever → Defender wins (bisimilar)      │
└─────────────────────────────────────────────────────────────┘
```

## Implementation

### Hy (DiscoHy) Implementation

```hy
;;; bisimulation_game.hy

(import [splitmix_ternary [SplitMixTernary]])

(defclass BisimulationGame []
  (defn __init__ [self system1 system2 seed]
    (setv self.s1 system1
          self.s2 system2
          self.rng (SplitMixTernary seed)
          self.history []))
  
  (defn attacker-move [self choice transition]
    "Attacker chooses system and transition."
    (setv trit (self.rng.next-ternary))
    (.append self.history {:role "attacker" 
                           :choice choice 
                           :transition transition
                           :trit trit})
    trit)
  
  (defn defender-respond [self matching-transition]
    "Defender provides matching transition."
    (setv trit (self.rng.next-ternary))
    (.append self.history {:role "defender"
                           :response matching-transition
                           :trit trit})
    trit)
  
  (defn arbiter-verify [self]
    "Arbiter checks GF(3) conservation."
    (setv recent-trits (lfor m (cut self.history -3 None) (get m "trit")))
    (setv conserved (= (% (sum recent-trits) 3) 0))
    (.append self.history {:role "arbiter" :conserved conserved :trit 0})
    conserved))
```

### DisCoPy Operad Interface

```python
from discopy import *

# Game as operad
class GameOperad:
    def __init__(self):
        self.operations = {}
    
    def register(self, name, dom, cod, rule):
        """Register game operation with GF(3) color."""
        self.operations[name] = Rule(dom, cod, name)
    
    def compose(self, op1, op2):
        """Compose operations preserving GF(3)."""
        trit1 = self.operations[op1].trit
        trit2 = self.operations[op2].trit
        # Result trit balances to 0
        result_trit = (-(trit1 + trit2)) % 3 - 1
        return Rule(
            self.operations[op1].dom,
            self.operations[op2].cod,
            f"{op1};{op2}",
            trit=result_trit
        )

# Define game operations
game = GameOperad()
game.register("attack", Ty("S1", "S2"), Ty("S1'"), lambda: -1)
game.register("defend", Ty("S1'"), Ty("S2'"), lambda: +1)  
game.register("verify", Ty("S1'", "S2'"), Ty("Result"), lambda: 0)
```

## Skill Dispersal Protocol

### 1. Fork Phase (Attacker)

```yaml
fork:
  targets:
    - agent: codex
      path: ~/.codex/skills/
      trit: -1
    - agent: claude
      path: ~/.claude/skills/
      trit: 0
    - agent: cursor
      path: ~/.cursor/skills/
      trit: +1
  gf3_check: true
```

### 2. Sync Phase (Defender)

```yaml
sync:
  strategy: observational-bridge
  bridge_type:
    source: skills@v1
    target: skills@v2
    dimension: 1
  conflict_resolution: 2d-cubical
```

### 3. Verify Phase (Arbiter)

```yaml
verify:
  conservation: gf3
  equivalence: bisimulation
  timeout: 60s
  fallback: last-known-good
```

## MCP Tasks Integration

### Self-Rewriting Task

```json
{
  "task": "skill-dispersal",
  "objective": "Propagate skill updates to all agents",
  "constraints": {
    "gf3_conservation": true,
    "bisimulation_equivalence": true,
    "max_divergence": 0.1
  },
  "steps": [
    {"action": "fork", "trit": -1},
    {"action": "propagate", "trit": 0},
    {"action": "verify", "trit": +1}
  ]
}
```

### Firecrawl Integration

```json
{
  "task": "skill-discovery",
  "objective": "Discover new skills from web resources",
  "tools": ["firecrawl", "exa"],
  "sources": [
    "https://github.com/topics/ai-agent-skills",
    "https://modelcontextprotocol.io/",
    "https://agentclientprotocol.com/"
  ],
  "output": {
    "format": "skill-yaml",
    "destination": ".ruler/skills/"
  }
}
```

## Resilience Patterns

### Redundant Storage

```
~/.codex/skills/     ← Primary (Codex)
~/.claude/skills/    ← Mirror 1 (Claude)
~/.cursor/skills/    ← Mirror 2 (Cursor)
.ruler/skills/       ← Source of truth
```

### Conflict Resolution

```
Dimension 0: Value conflict  → Use source of truth
Dimension 1: Diff conflict   → Merge via LCA
Dimension 2: Meta conflict   → Arbiter decides
```

## Xenomodern Stance

The bisimulation game embodies xenomodernity by:

1. **Ironic distance**: We know perfect equivalence is unattainable, yet we play the game
2. **Sincere engagement**: The game produces real, useful synchronization
3. **Playful synergy**: Attacker/Defender/Arbiter dance together
4. **Conservation laws**: GF(3) as the invariant that holds everything together

```
    xenomodernity
         │
    ┌────┴────┐
    │         │
 ironic    sincere
    │         │
    └────┬────┘
         │
   bisimulation
   (both/neither)
```

## Commands

```bash
just bisim-init           # Initialize bisimulation game
just bisim-round          # Play one round
just bisim-disperse       # Disperse skills to all agents
just bisim-verify         # Verify GF(3) conservation
just bisim-reconcile      # Reconcile divergent states
```
