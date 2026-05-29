---
name: glass-bead-game
description: Hesse-inspired interdisciplinary synthesis game with Badiou triangle inequality for possible world hopping across mathematical, musical, and philosophical domains.
source: music-topos/skills
license: MIT
---

# Glass Bead Game: Topos of Music

The Glass Bead Game (Glasperlenspiel) is an interdisciplinary synthesis engine that connects:
- **Mathematics** (category theory, algebraic geometry, number theory)
- **Music** (harmony, counterpoint, electronic synthesis)
- **Philosophy** (Badiou's ontology, Girard's linear logic, Lawvere's topos theory)

## Core Concept: World Hopping

Each **bead** represents a concept in a specific domain. Beads connect via **morphisms** that preserve essential structure. The game consists of finding paths between distant beads that illuminate hidden connections.

### Badiou Triangle Inequality

For any three worlds W₁, W₂, W₃:

```
d(W₁, W₃) ≤ d(W₁, W₂) + d(W₂, W₃)
```

This is the **triangle inequality** that governs world hopping:

- **Being**: Current ontological state (the bead's position in possibility space)
- **Event**: A rupture that creates new possibilities (the hop between worlds)  
- **Truth**: What persists across the transition (the invariant structure)

### Distance Metric

Distance between worlds is measured by:

```ruby
def world_distance(w1, w2)
  being_diff = (w1.seed ^ w2.seed).to_s(2).count('1')  # Hamming distance
  event_diff = (w1.epoch - w2.epoch).abs               # Temporal distance
  truth_diff = conjugacy_distance(w1.invariant, w2.invariant)
  
  Math.sqrt(being_diff**2 + event_diff**2 + truth_diff**2)
end
```

## Bead Types

### Mathematical Beads
- **Number**: Prime, composite, transcendental, p-adic
- **Structure**: Group, ring, field, category, topos
- **Morphism**: Homomorphism, functor, natural transformation
- **Invariant**: Fixed point, eigenvalue, cohomology class

### Musical Beads  
- **Pitch**: Frequency, pitch class, interval
- **Harmony**: Chord, progression, voice leading
- **Rhythm**: Duration, meter, polyrhythm
- **Timbre**: Spectrum, envelope, modulation

### Philosophical Beads
- **Ontological**: Being, becoming, event, void
- **Logical**: Proposition, proof, cut, polarity
- **Categorical**: Object, morphism, limit, adjunction

## Game Moves

### 1. CONNECT: Link Two Beads
Find a morphism that connects bead A to bead B while preserving structure.

```ruby
move = GlassBeadGame::Connect.new(
  from: Bead.new(:prime, 17),
  to: Bead.new(:pitch_class, 5),  # 17 mod 12 = 5
  via: :modular_arithmetic
)
```

### 2. TRANSPOSE: Shift Domain
Apply a functor to move an entire structure to a new domain.

```ruby
move = GlassBeadGame::Transpose.new(
  structure: :circle_of_fifths,
  from_domain: :music,
  to_domain: :number_theory,
  functor: :chromatic_to_modular
)
```

### 3. REFLECT: Find Dual
Discover the contravariant counterpart of a structure.

```ruby
move = GlassBeadGame::Reflect.new(
  structure: :major_scale,
  reflection: :phrygian_mode,  # Dual via interval inversion
  symmetry: :diatonic_mirror
)
```

### 4. HOP: World Transition
Execute a Badiou-style event that transitions between possible worlds.

```ruby
move = GlassBeadGame::Hop.new(
  from_world: current_world,
  event: :modulation,
  to_world: target_world,
  truth_preserved: :tonal_center
)
```

## Scoring

Points are awarded for:

| Move Type | Base Points | Multipliers |
|-----------|-------------|-------------|
| CONNECT | 10 | ×2 if cross-domain |
| TRANSPOSE | 25 | ×3 if structure-preserving |
| REFLECT | 15 | ×2 if self-dual found |
| HOP | 50 | ×(1/distance) for elegant hops |

### Elegance Bonus

Shorter paths between distant concepts receive elegance bonuses:

```ruby
elegance = conceptual_distance / path_length
bonus = (elegance > 3) ? elegance * 10 : 0
```

## Example Game Session

```
Turn 1: CONNECT(Ramanujan's 1729, "taxicab number")
        → Linked to: Hardy-Littlewood circle method
        Points: 10

Turn 2: TRANSPOSE(circle method, analysis → music)
        → Produces: Spectral analysis of timbre
        Points: 25 × 3 = 75

Turn 3: REFLECT(timbre spectrum)
        → Dual: Temporal envelope (Fourier duality)
        Points: 15 × 2 = 30

Turn 4: HOP(acoustic → electronic)
        → Event: Synthesis (analog → digital)
        → Truth preserved: Harmonic ratios
        Points: 50 × 0.8 = 40

Total: 155 points
```

## Integration with Music Topos

### Using with World Broadcast

```ruby
# Create game from mathematician broadcast
system = WorldBroadcast::TripartiteSystem.new([:ramanujan, :grothendieck, :euler])
game = GlassBeadGame.from_broadcast(system)

# Each mathematician contributes beads
game.add_bead_from_agent(system.agents[0])  # Ramanujan's partitions
game.add_bead_from_agent(system.agents[1])  # Grothendieck's schemes
game.add_bead_from_agent(system.agents[2])  # Euler's series
```

### Using with Synadia

```ruby
# Publish moves to NATS
SynadiaBroadcast.publish("game.move.connect", move.to_json)

# Subscribe to opponent moves
SynadiaBroadcast.subscribe("game.move.*") do |msg|
  game.apply_move(GlassBeadGame::Move.from_json(msg.data))
end
```

### Using with Propagators

```ruby
# Create propagator network for game state
network = PropagatorNetwork.new

# Cells for each bead
beads.each { |b| network.add_cell(b.id, b.state) }

# Propagators for constraints
network.add_propagator(:triangle_inequality) do |w1, w2, w3|
  world_distance(w1, w3) <= world_distance(w1, w2) + world_distance(w2, w3)
end
```

## Philosophical Foundation

### Badiou's Ontology

- **Situation**: The current game state (set of beads and connections)
- **State**: The meta-structure organizing beads (rules, scoring)
- **Event**: A move that exceeds the situation (creates new possibilities)
- **Truth**: The generic procedure that extends from the event

### Lawvere's Topos

The game forms a **topos** where:
- Objects are beads (concepts)
- Morphisms are connections (structural mappings)
- Subobject classifier Ω distinguishes "in play" vs "potential"
- Internal logic is intuitionistic (constructive proofs via game moves)

### Girard's Linear Logic

Resources are **linear** (used exactly once):
- Each bead can only be connected once per turn
- Connections consume "attention" (a limited resource)
- Exponentials (!) allow reuse of fundamental beads

## Commands

```bash
just glass-bead              # Start interactive game
just glass-bead-solo         # Single-player mode
just glass-bead-tournament   # Multi-round competition
just world-hop from to       # Execute world hop
```
