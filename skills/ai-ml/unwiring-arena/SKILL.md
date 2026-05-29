---
name: unwiring-arena
description: Play/Coplay arena theory for autopoietic closure with GF(3) conservation
version: 1.0.0
---


# Unwiring Arena Skill

**Status**: ✅ Production Ready  
**Trit**: 0 (ERGODIC - balanced flow)  
**Principle**: Play/Coplay autopoietic closure with GF(3) conservation  
**Source**: plurigrid/UnwiringDiagrams.jl#1 + Capucci et al. Arena Theory

---

## Overview

**Unwiring Arena** unifies three categorical patterns:

1. **Wiring Diagrams** (AlgebraicJulia/Catlab) - Compositional system construction
2. **Unwiring Rules** (GayUncommonsSimulator) - Learning through constraint release
3. **Arena Protocol** (Plurigrid Amelia v0.4) - Play/Coplay bidirectional channels

```
┌─ Play Channel (Outbound) ─────────────────┐
│ Local arena mutations → NATS broadcast    │
│ Strategy profiles → Action selection      │
└────────────────────────────────────────────┘
                    ↕ (Autopoietic closure)
┌─ Coplay Channel (Inbound) ───────────────┐
│ Peer arena submissions → Reconciliation   │
│ Rewards/feedback → Identity update        │
└────────────────────────────────────────────┘
```

## Mathematical Foundation

### Arenas as Parametrised Lenses

From Capucci, Ghani, Ledent, Forsberg:

```
Arena A_G : Lens_{(Ω,℧)}(X,S)(Y,R)

where:
  Ω = Π_{p∈P} Ωₚ     (strategy profiles)
  ℧ = Π_{p∈P} ℧ₚ     (reward vectors)
  X, Y = states
  S, R = costates (feedback)
```

**Play**: `play_A : Ω × X → Y` (forward pass)
**Coplay**: `coplay_A : Ω × X × R → ℧ × S` (backward pass with feedback)

### Unwiring = Learning Through Constraint Release

```julia
struct UnwiringRule
    source_gf3::Int         # Source polarity {-1, 0, +1}
    target_gf3::Int         # Target polarity
    learning_rate::Float64  # How fast to unwire
    threshold::Float64      # Discrepancy threshold to trigger
end

# Unwiring shifts internal toward external (learning)
function apply_unwiring(rule, internal, external)
    α = rule.learning_rate
    return (1-α) * internal + α * external
end
```

### GF(3) Tripartite Channels

```
MINUS (-1)   : Constraint verification (coplay focus)
ERGODIC (0)  : Balance/coordination (arena equilibrium)
PLUS (+1)    : Generative exploration (play focus)

Conservation: sum(trits) ≡ 0 (mod 3) per triplet
```

## Arena Protocol v0.4 (Amelia)

### Schema (JSONSchema v7)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "arena_id": { "type": "string", "format": "uuid" },
    "seed": { "type": "integer", "description": "SplitMix64 seed" },
    "players": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "strategy_space": { "type": "array" },
          "gf3_polarity": { "enum": [-1, 0, 1] }
        }
      }
    },
    "play_channel": {
      "type": "object",
      "properties": {
        "topic": { "type": "string", "pattern": "^plurigrid\\.arena\\.play\\." },
        "mutations": { "type": "array" }
      }
    },
    "coplay_channel": {
      "type": "object", 
      "properties": {
        "topic": { "type": "string", "pattern": "^plurigrid\\.arena\\.coplay\\." },
        "reconciliations": { "type": "array" }
      }
    }
  }
}
```

### NATS Topics

```
plurigrid.arena.play.{agent}.{focus}     # Outbound mutations
plurigrid.arena.coplay.{agent}.{focus}   # Inbound feedback
plurigrid.arena.peers.>                  # Peer discovery
plurigrid.arena.reconcile                # Conflict resolution
```

## Julia Implementation

### Core Types

```julia
using Catlab.WiringDiagrams
using Catlab.Programs

# Arena as parametrised lens
struct Arena{Ω, U, X, S, Y, R}
    play::Function      # Ω × X → Y
    coplay::Function    # Ω × X × R → U × S
    strategies::Ω
    rewards::U
end

# Unwiring rule for learning
struct UnwiringRule
    source_gf3::Int
    target_gf3::Int
    learning_rate::Float64
    threshold::Float64
end

# Agent with reafferent identity
mutable struct ArenaAgent
    id::UInt64
    internal_state::Vector{Float64}
    external_observation::Vector{Float64}
    discrepancy::Float64
    gf3::Int
    unwiring_count::Int
    current_rule::Int
end
```

### Compositional Arena Construction

```julia
using Catlab.WiringDiagrams: WiringDiagram, add_box!, add_wire!

"""
Build arena wiring diagram from player specifications.
"""
function build_arena_diagram(players::Vector{Tuple{Symbol, Int}})
    d = WiringDiagram([:X], [:Y])
    
    for (name, arity) in players
        box = add_box!(d, Box(name, fill(:strategy, arity), [:action]))
    end
    
    # Wire sequentially (can be customized)
    for i in 1:(length(players)-1)
        add_wire!(d, (i, 1) => (i+1, 1))
    end
    
    return d
end

"""
Unwire a connection (remove constraint, enable learning).
"""
function unwire!(d::WiringDiagram, wire_id::Int)
    # Remove wire - allows independent evolution
    delete_wire!(d, wire_id)
end

"""
Apply unwiring rule based on discrepancy.
"""
function apply_unwiring!(agent::ArenaAgent, rules::Vector{UnwiringRule})
    rule = rules[agent.current_rule]
    
    if agent.discrepancy > rule.threshold && agent.gf3 == rule.source_gf3
        α = rule.learning_rate
        agent.internal_state = (1-α) .* agent.internal_state .+ 
                               α .* agent.external_observation
        agent.unwiring_count += 1
        agent.current_rule = mod1(agent.current_rule + 1, length(rules))
    end
    
    update_identity!(agent)
end
```

### Play/Coplay Implementation

```julia
"""
Play: Forward pass through arena.
"""
function arena_play(arena::Arena, strategy::Ω, state::X) where {Ω, X}
    arena.play(strategy, state)
end

"""
Coplay: Backward pass with reward feedback.
"""
function arena_coplay(arena::Arena, strategy::Ω, state::X, reward::R) where {Ω, X, R}
    arena.coplay(strategy, state, reward)
end

"""
Autopoietic closure: play ∘ coplay cycle.
"""
function arena_cycle!(agent::ArenaAgent, arena::Arena, external_reward)
    # Play: agent acts
    action = arena_play(arena, agent.internal_state, agent.external_observation)
    
    # Coplay: receive feedback, update internal state
    utility, new_costate = arena_coplay(arena, agent.internal_state, 
                                         agent.external_observation, external_reward)
    
    # Update discrepancy (reafference)
    agent.external_observation = new_costate
    agent.discrepancy = norm(agent.internal_state - agent.external_observation)
    agent.gf3 = Int(hash(agent.internal_state) % 3) - 1
    
    return action, utility
end
```

## Python Implementation

```python
"""
unwiring_arena.py - Arena Protocol with Unwiring Rules
"""
from dataclasses import dataclass, field
from typing import List, Callable, Tuple, Dict, Any
import numpy as np

# SplitMix64 constants
GOLDEN = 0x9E3779B97F4A7C15
MASK64 = (1 << 64) - 1

@dataclass
class UnwiringRule:
    """How identity transforms through learning."""
    source_gf3: int      # {-1, 0, +1}
    target_gf3: int
    learning_rate: float
    threshold: float

UNWIRING_RULES = [
    UnwiringRule(0, 1, 0.1, 0.2),   # Fresh→Aging: slow learning
    UnwiringRule(1, -1, 0.3, 0.4),  # Aging→Stale: medium learning
    UnwiringRule(-1, 0, 0.5, 0.6),  # Stale→Fresh: fast learning (reset)
    UnwiringRule(0, -1, 0.05, 0.8), # Fresh→Stale: rare leap
]

@dataclass
class ArenaAgent:
    """Agent with reafferent identity."""
    id: int
    internal_state: np.ndarray
    external_observation: np.ndarray
    discrepancy: float = 0.0
    gf3: int = 0
    unwiring_count: int = 0
    current_rule: int = 0
    
    def update_identity(self):
        """Recompute identity from internal/external discrepancy."""
        self.discrepancy = np.linalg.norm(
            self.internal_state - self.external_observation
        )
        h = hash(self.internal_state.tobytes())
        self.gf3 = (h % 3) - 1

@dataclass 
class Arena:
    """Parametrised lens for game-theoretic interaction."""
    play: Callable      # (strategy, state) -> action
    coplay: Callable    # (strategy, state, reward) -> (utility, costate)
    
    def cycle(self, agent: ArenaAgent, external_reward: float) -> Tuple[Any, float]:
        """Execute play/coplay autopoietic cycle."""
        # Play: forward pass
        action = self.play(agent.internal_state, agent.external_observation)
        
        # Coplay: backward pass with feedback
        utility, new_costate = self.coplay(
            agent.internal_state, 
            agent.external_observation,
            external_reward
        )
        
        # Update agent's external observation
        agent.external_observation = new_costate
        agent.update_identity()
        
        return action, utility

def apply_unwiring(agent: ArenaAgent, rules: List[UnwiringRule] = UNWIRING_RULES):
    """Apply unwiring rule to shift internal toward external."""
    rule = rules[agent.current_rule]
    
    if agent.discrepancy > rule.threshold and agent.gf3 == rule.source_gf3:
        α = rule.learning_rate
        agent.internal_state = (
            (1 - α) * agent.internal_state + 
            α * agent.external_observation
        )
        agent.unwiring_count += 1
        agent.current_rule = (agent.current_rule + 1) % len(rules)
    
    agent.update_identity()
```

## NATS Integration

```python
import nats
import json

NATS_SERVER = "nats://nonlocal.info:4222"

async def publish_arena_play(nc, agent_id: str, focus: str, mutation: dict):
    """Publish play channel mutation."""
    topic = f"plurigrid.arena.play.{agent_id}.{focus}"
    await nc.publish(topic, json.dumps(mutation).encode())

async def subscribe_arena_coplay(nc, agent_id: str, handler):
    """Subscribe to coplay channel feedback."""
    topic = f"plurigrid.arena.coplay.{agent_id}.>"
    await nc.subscribe(topic, cb=handler)

async def broadcast_reconciliation(nc, arena_state: dict):
    """Broadcast arena state for reconciliation."""
    await nc.publish("plurigrid.arena.reconcile", json.dumps(arena_state).encode())
```

## Integration with GayUncommonsSimulator

```julia
# From GayUncommonsSimulator.jl - the key insight
# Wiring = constraint (commons pooling)
# Unwiring = freedom (uncommons differentiation)

const UNWIRING_RULES = [
    UnwiringRule(0, 1, 0.1, 0.2),  # Fresh→Aging
    UnwiringRule(1, 2, 0.3, 0.4),  # Aging→Stale
    UnwiringRule(2, 0, 0.5, 0.6),  # Stale→Fresh (reset cycle)
]

# Identity IS discrepancy
struct ReafferentID
    internal::RGB
    external::RGB
    discrepancy::Float64
    hash::UInt64
    gf3::Int
end

# ID = hash(internal ⊻ external)
function ReafferentID(internal::RGB, external::RGB)
    disc = abs(spectrum_t(internal) - spectrum_t(external))
    id_hash = mix(to_hash(internal) ⊻ to_hash(external))
    gf3 = Int(id_hash % 3)
    ReafferentID(internal, external, disc, id_hash, gf3)
end
```

## Chronoscope Video Integration

The Arena Protocol includes video orchestration for 69 demonstrations:

```julia
# 7 categories × ~10 videos each
CHRONOSCOPE_CATEGORIES = [
    :categorical_ops,      # Operad operations
    :quantum,              # ZX calculus
    :hypergraph,           # Hypergraph rewriting
    :ducklake,             # Time-travel queries
    :embodied_gradualism,  # Learning dynamics
    :ontology,             # Schema evolution
    :arena_protocol,       # This very protocol
]

# Deterministic scheduling with seed 1069
schedule_videos(seed=1069, categories=CHRONOSCOPE_CATEGORIES)
```

## Commands

```bash
# Julia - run arena simulation
julia -e "include(\"GayUncommonsSimulator.jl\"); simulate_wev(n_steps=100)"

# Python - NATS arena client
uv run --with nats-py arena_client.py

# Catlab wiring diagram
julia -e "using Catlab.WiringDiagrams; d = WiringDiagram([:X], [:Y])"
```

## Key Patterns

| Pattern | Wiring | Unwiring |
|---------|--------|----------|
| **Semantics** | Constraint | Freedom |
| **Direction** | Composition | Decomposition |
| **Learning** | Fixed relationship | Adaptive relationship |
| **GF3 Flow** | -1 (MINUS) | +1 (PLUS) |

## See Also

- [GayUncommonsSimulator.jl](file:///Users/bob/ies/GayUncommonsSimulator.jl) - Full implementation
- [plurigrid/UnwiringDiagrams.jl#1](https://github.com/plurigrid/UnwiringDiagrams.jl/pull/1) - Arena Protocol PR
- [Capucci et al.](file:///Users/bob/ies/paper_extracts/mathpix_snips/obsidian/math/M.%20Capucci,%20N.%20Ghani,%20J.%20Ledent,%20F.%20Nordvall%20Forsberg.md) - Arenas with players
- [gay-mcp](file:///Users/bob/.claude/skills/gay-mcp/SKILL.md) - Deterministic colors
- [triad-interleave](file:///Users/bob/.claude/skills/triad-interleave/SKILL.md) - GF(3) scheduling

## Thread History (Extracted Patterns)

### Core Arena/Games Threads

| Thread | Messages | Key Pattern |
|--------|----------|-------------|
| [GayUncommonsSimulator with reafference](https://ampcode.com/threads/T-019b22bf-11fd-73ad-a61a-e7c40373fd49) | 61 | ID = hash(internal ⊻ external), WEV extraction |
| [GAY protocol stack + open games](https://ampcode.com/threads/T-019b22cd-ef86-77eb-a285-8dbe2312558f) | 39 | 3-coloring guarantees, Hedges open games |
| [DiscoHy operadic framework](https://ampcode.com/threads/T-019b44e5-39bb-7251-a8fa-5d1efaa5dafa) | 55 | ParaLens, Hedges equilibria, operads |
| [Random walk spectral gap](https://ampcode.com/threads/T-019b43de-907c-7008-a545-57e8ff698498) | 104 | Open-games + active-inference GF(3) balance |

### Wiring/Category Threads

| Thread | Messages | Key Pattern |
|--------|----------|-------------|
| [Load acset skill](https://ampcode.com/threads/T-019b43a6-11f7-77a8-a9cd-ea618e457b70) | 88 | C-set as functor, DPO rewriting |
| [Formalize skills with interaction entropy](https://ampcode.com/threads/T-019b44d2-05db-72e2-9a4a-23b7e1085b25) | 61 | DisCoPy boxes, ACSet integration |
| [Install plurigrid ASI skills](https://ampcode.com/threads/T-019b44c6-bfa3-7371-b238-023eb308d12b) | 124 | SchOperadNetwork, morphism traversal |
| [P2P file exchange + skills](https://ampcode.com/threads/T-019b4464-a75b-714e-9f73-e4e1dfd82ab7) | 162 | DiscoPy operads, 1069 subscales |

### WEV/Value Extraction Threads

| Thread | Messages | Key Pattern |
|--------|----------|-------------|
| [Comprehensive GAY protocol](https://ampcode.com/threads/T-019b22d0-c29f-72e7-a229-57a99774d3fa) | 160 | 3-match guarantee, pigeonhole bound |
| [Find recent fork threads](https://ampcode.com/threads/T-019b22aa-e7ef-779c-9246-9977c1c6a9ae) | 150 | WEV formula, colored operad schema |
| [Self-reflexive triadic subagent](https://ampcode.com/threads/T-019b233a-7ddf-734c-b117-2dd65ae97a80) | 141 | Tripartite network, GF(3) conservation |

### Key Extracted Formulas

```julia
# WEV (World Extractable Value)
WEV(agent, world) = base_value × staleness_mult × scarcity_mult

where:
  base_value     = agent.discrepancy × 10.0
  staleness_mult = 1.0 + Σ(days_since_asked) × 0.1
  scarcity_mult  = 1.0 + (1.0 - occupancy[color] / total)

# 3-Coloring Guarantees
∀ i: color[i] ≠ color[i+1]           # Adjacent Distinct
∀ window of 3: {R, Y, B} all present  # 3-Match Property

# Reafferent Identity
ID = hash(internal_color ⊻ external_color)
discrepancy = |spectrum_t(internal) - spectrum_t(external)|
```

### ACSet Schema for Arena Protocol

```julia
@present SchArenaProtocol(FreeSchema) begin
    Agent::Ob
    Arena::Ob
    Channel::Ob
    Message::Ob
    
    agent_arena::Hom(Agent, Arena)
    msg_channel::Hom(Message, Channel)
    channel_arena::Hom(Channel, Arena)
    
    # Attributes
    Name::AttrType
    Trit::AttrType
    Seed::AttrType
    
    agent_name::Attr(Agent, Name)
    agent_trit::Attr(Agent, Trit)
    arena_seed::Attr(Arena, Seed)
    channel_type::Attr(Channel, Name)  # "play" or "coplay"
end
```

---

**Skill Name**: unwiring-arena  
**Type**: Compositional Game Theory / Learning  
**Trit**: 0 (ERGODIC)  
**GF(3)**: Play/Coplay closure maintains conservation  
**SPI**: Deterministic arena fingerprints via seed chain
**Threads**: 15+ related threads with 1400+ combined messages



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