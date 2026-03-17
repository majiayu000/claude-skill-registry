---
name: plurigrid-asi-integrated
description: Unified Plurigrid ASI skill combining ACSets, Gay-MCP colors, bisimulation games, world-hopping, glass-bead synthesis, and triad interleaving for autonomous skill dispersal.
---

# Plurigrid ASI Integrated Skill

Synthesizes all loaded skills into a coherent system for **Plurigrid Artificial Superintelligence** skill orchestration.

## Skill Lattice

```
                    ┌─────────────────┐
                    │  glass-bead-game │
                    │  (synthesis)     │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
┌────────▼────────┐ ┌────────▼────────┐ ┌────────▼────────┐
│  world-hopping  │ │  bisimulation   │ │  triad-interleave│
│  (navigation)   │ │  (dispersal)    │ │  (scheduling)    │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼────────┐
                    │     gay-mcp      │
                    │  (deterministic  │
                    │   coloring)      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │     acsets       │
                    │  (data model)    │
                    └─────────────────┘
```

## Unified Protocol

### 1. Schema (ACSets)

```julia
@present SchASIWorld(FreeSchema) begin
  World::Ob
  Skill::Ob
  Agent::Ob
  
  source::Hom(World, World)
  target::Hom(World, World)
  
  has_skill::Hom(Agent, Skill)
  inhabits::Hom(Agent, World)
  
  Seed::AttrType
  Trit::AttrType
  
  seed::Attr(World, Seed)
  color_trit::Attr(Skill, Trit)
end
```

### 2. Color Generation (Gay-MCP)

```python
from gay import SplitMixTernary, TripartiteStreams

def color_world(world_seed: int, skill_index: int) -> dict:
    gen = SplitMixTernary(world_seed)
    return gen.color_at(skill_index)
```

### 3. World Navigation (World-Hopping)

```python
def hop_between_worlds(w1, w2, event_name: str):
    distance = world_distance(w1, w2)
    if valid_hop(w1, w2):
        event = Event(site=["skill"], name=event_name)
        return event.execute(w1)
    return None
```

### 4. Skill Dispersal (Bisimulation)

```python
async def disperse_skill(skill_path: str, agents: list):
    game = BisimulationGame()
    for i, agent in enumerate(agents):
        trit = (i % 3) - 1  # GF(3) balanced
        game.attacker_move(agent, skill_path, trit)
        game.defender_respond(await agent.receive(skill_path))
    return game.arbiter_verify()
```

### 5. Parallel Execution (Triad Interleave)

```python
def schedule_skill_updates(seed: int, n_agents: int):
    interleaver = TriadInterleaver(seed)
    schedule = interleaver.interleave(
        n_triplets=n_agents // 3,
        policy="gf3_balanced"
    )
    return schedule
```

### 6. Synthesis (Glass Bead Game)

```python
def synthesize_skills(*skills):
    game = GlassBeadGame()
    for skill in skills:
        game.add_bead(skill.name, skill.domain)
    
    # Connect skills via morphisms
    game.connect("acsets", "gay-mcp", via="seed_to_color")
    game.connect("gay-mcp", "triad-interleave", via="color_stream")
    game.connect("triad-interleave", "bisimulation", via="schedule")
    game.connect("bisimulation", "world-hopping", via="dispersal")
    
    return game.score()
```

## ~/worlds Letter Index

| Letter | Domain | Key Projects |
|--------|--------|--------------|
| a | Category Theory | ACSets.jl, Catlab.jl, Decapodes.jl |
| b | Terminal | bmorphism/trittty |
| p | Infrastructure | plurigrid/oni, alpaca.cpp |
| t | Collaboration | CatColab |
| e | HoTT | infinity-cosmos (Lean 4) |
| r | Type Theory | rzk (simplicial HoTT) |
| n | Knowledge | nlab-content |
| o | Music | rubato-composer |

## GF(3) Conservation Law

All operations preserve:

```
∑ trits ≡ 0 (mod 3)
```

Across:
- World hops (Attacker -1, Defender +1, Arbiter 0)
- Color triplets (MINUS, ERGODIC, PLUS)
- Schedule entries (balanced per triplet)
- Skill dispersal (agent assignments)

## Commands

```bash
# Generate integrated schedule
just asi-schedule 0x42D 10

# Disperse skills to all agents
just asi-disperse ~/.claude/skills/

# Verify GF(3) conservation
just asi-verify

# Play glass bead synthesis
just asi-synthesize a b p t

# World hop between letters
just asi-hop a t
```

## Directory Tree

```
plurigrid/asi/
├── package.json
├── bin/cli.js
├── README.md
└── skills/
    ├── a/SKILL.md     # AlgebraicJulia
    ├── b/SKILL.md     # topos-labs
    ├── c/SKILL.md     # cognitect
    ├── d/SKILL.md     # claykind
    ├── e/SKILL.md     # infinity-cosmos
    ├── f/SKILL.md     # clojure-site
    ├── g/SKILL.md     # archiver-bot
    ├── h/SKILL.md     # gdlog
    ├── i/SKILL.md     # InverterNetwork
    ├── k/SKILL.md     # kubeflow
    ├── l/SKILL.md     # pretty-bugs
    ├── m/SKILL.md     # awesome-category-theory
    ├── n/SKILL.md     # nlab-content
    ├── o/SKILL.md     # oeis, rubato-composer
    ├── p/SKILL.md     # plurigrid (primary)
    ├── q/SKILL.md     # quadrat
    ├── r/SKILL.md     # rzk
    ├── s/SKILL.md     # mathematicians
    ├── t/SKILL.md     # CatColab
    ├── v/SKILL.md     # viro
    └── _integrated/   # Plurigrid ASI unified skill
        └── SKILL.md
```

## Recent AMP Thread Integration

Last integration: `plurigrid-asi-20251224184534`
- Attacker (MINUS): `dabe5fc2-*` (33 invocations)
- Arbiter (ERGODIC): `c6e1294a-*` (133 invocations)
- Defender (PLUS): `9b24821d-*` (1 invocation)
- GF(3) Sum: 0 ✓ Conserved
