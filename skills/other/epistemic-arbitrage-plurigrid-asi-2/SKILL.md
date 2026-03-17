---
name: epistemic-arbitrage
description: Propagator-based parallel structure for exploiting knowledge differentials across domains using local scoped propagators and SplitMixTernary RNG.
source: music-topos/skills
license: MIT
---

# Epistemic Arbitrage: Propagator-Based Knowledge Synthesis

Epistemic arbitrage exploits **knowledge differentials** between domains. When concept A in domain X is well-understood, but its isomorphic counterpart A' in domain Y is mysterious, we can **arbitrage** by transferring understanding.

## Core Architecture

### Propagator Networks (Radul/Sussman)

A propagator network consists of:

```
┌─────────┐     ┌─────────────┐     ┌─────────┐
│  Cell A │────▶│ Propagator  │────▶│  Cell B │
│ (known) │     │  (transfer) │     │(derived)│
└─────────┘     └─────────────┘     └─────────┘
```

- **Cells**: Containers for partial information
- **Propagators**: Functions that combine/transform information
- **Merging**: Monotonic accumulation (information only increases)

### SplitMixTernary RNG

For parallel propagation with determinism:

```ruby
class SplitMixTernary
  GOLDEN = 0x9e3779b97f4a7c15  # Golden ratio constant
  
  def initialize(seed)
    @state = seed
  end
  
  def next_ternary
    # Advance state (SplitMix64)
    @state = (@state + GOLDEN) & 0xFFFFFFFFFFFFFFFF
    z = @state
    z = ((z ^ (z >> 30)) * 0xbf58476d1ce4e5b9) & 0xFFFFFFFFFFFFFFFF
    z = ((z ^ (z >> 27)) * 0x94d049bb133111eb) & 0xFFFFFFFFFFFFFFFF
    z = z ^ (z >> 31)
    
    # Map to ternary: -1, 0, +1
    (z % 3) - 1
  end
  
  def split(index)
    # Create independent child stream
    child_seed = @state ^ (index * GOLDEN)
    SplitMixTernary.new(child_seed)
  end
end
```

## Arbitrage Patterns

### Pattern 1: Domain Transfer

```ruby
# Knowledge in domain A
cell_a = Cell.new(:music, :circle_of_fifths)
cell_a.add_info(:structure, :cyclic_group_12)
cell_a.add_info(:generator, :perfect_fifth)

# Unknown in domain B
cell_b = Cell.new(:number_theory, :modular_arithmetic)

# Propagator transfers structure
propagator = Propagator.new(:domain_transfer) do |source, target|
  if source.has?(:structure)
    target.merge(:structure, source.get(:structure))
    target.merge(:insight, "Z/12Z isomorphic to circle of fifths")
  end
end

propagator.connect(cell_a, cell_b)
propagator.fire!
```

### Pattern 2: Dual Discovery

```ruby
# Known: Fourier transform on functions
cell_time = Cell.new(:analysis, :time_domain)
cell_freq = Cell.new(:analysis, :frequency_domain)

# Propagator: Fourier duality
duality_propagator = Propagator.new(:fourier_duality) do |time, freq|
  time.each_property do |prop, val|
    dual_prop = fourier_dual(prop)  # convolution ↔ multiplication, etc.
    freq.merge(dual_prop, val)
  end
end
```

### Pattern 3: Triangle Arbitrage

When three domains have pairwise connections, exploit the triangle:

```ruby
# Three domains with partial knowledge
cell_math = Cell.new(:mathematics, :group_theory)
cell_music = Cell.new(:music, :harmony)
cell_physics = Cell.new(:physics, :symmetry)

# Pairwise propagators
math_music = Propagator.new(:pitch_class_groups)
music_physics = Propagator.new(:overtone_series)
physics_math = Propagator.new(:lie_groups)

# Triangle inequality enables arbitrage:
# d(math, physics) ≤ d(math, music) + d(music, physics)
# 
# If direct math→physics is hard, go via music!
```

## Local Scoped Propagators

### Scoping for Parallelism

Each propagator runs in a local scope with:

```ruby
class ScopedPropagator
  def initialize(name, rng_seed, &block)
    @name = name
    @rng = SplitMixTernary.new(rng_seed)
    @block = block
    @local_cells = {}
  end
  
  def fork(n)
    # Create n parallel scopes with independent RNG streams
    n.times.map do |i|
      child_rng = @rng.split(i)
      ScopedPropagator.new("#{@name}/#{i}", child_rng.state, &@block)
    end
  end
  
  def run(inputs)
    # Execute in isolated scope
    @local_cells = inputs.dup
    @block.call(self, @local_cells)
    @local_cells
  end
end
```

### Parallel Arbitrage Network

```ruby
# Master network
network = ArbitrageNetwork.new(seed: 1069)

# Add cells for each domain
network.add_cell(:category_theory, knowledge: 0.9)
network.add_cell(:music_theory, knowledge: 0.7)
network.add_cell(:physics, knowledge: 0.5)
network.add_cell(:philosophy, knowledge: 0.3)

# Add arbitrage propagators
network.add_propagator(:category_to_music, [:category_theory], [:music_theory])
network.add_propagator(:music_to_physics, [:music_theory], [:physics])
network.add_propagator(:physics_to_philosophy, [:physics], [:philosophy])

# Run in parallel (SPI-compliant)
results = network.run_parallel(n_workers: 4)
```

## Integration with Music Topos

### With World Broadcast

```ruby
# Each mathematician is a knowledge source
broadcasters = WorldBroadcast::TripartiteSystem.new([:ramanujan, :grothendieck, :euler])

# Create cells from mathematician expertise
cells = broadcasters.agents.map do |agent|
  Cell.new(agent.profile[:domain], 
           knowledge: agent.history.size,
           operations: agent.profile[:operations])
end

# Arbitrage between mathematicians
network = ArbitrageNetwork.from_cells(cells)
network.add_all_pairwise_propagators
network.run!
```

### With Synadia

```ruby
# Publish arbitrage opportunities
network.on_arbitrage do |source, target, gain|
  SynadiaBroadcast.publish("arbitrage.opportunity", {
    from: source.domain,
    to: target.domain,
    knowledge_gain: gain
  })
end

# Subscribe to external knowledge
SynadiaBroadcast.subscribe("knowledge.*") do |msg|
  domain = msg.subject.split('.').last.to_sym
  network.cells[domain].merge(:external, msg.data)
end
```

### With Glass Bead Game

```ruby
# Arbitrage opportunities become game moves
network.on_arbitrage do |source, target, gain|
  if gain > threshold
    move = GlassBeadGame::Connect.new(
      from: Bead.new(source.domain, source.best_concept),
      to: Bead.new(target.domain, target.mystery),
      via: :epistemic_transfer,
      value: gain
    )
    game.propose_move(move)
  end
end
```

## Guarantees

1. **SPI Compliance**: Parallel execution ≡ sequential (bitwise identical)
2. **Determinism**: Same seed → same arbitrage discoveries
3. **Monotonicity**: Knowledge only increases (no forgetting)
4. **Locality**: Propagators only access explicitly connected cells
5. **Triangle Inequality**: d(A,C) ≤ d(A,B) + d(B,C) for all knowledge transfers

## Commands

```bash
just arbitrage               # Run arbitrage network
just arbitrage-domains a b   # Arbitrage between specific domains
just propagator-network      # Visualize propagator network
just knowledge-flow          # Show knowledge flow diagram
```
