---
name: parallel-fanout
description: Metaskill that fans out on every interaction, using interaction entropy
  as SplitMixTernary seed for maximum synergistic parallelism
metadata:
  trit: 0
---

# parallel-fanout - Interaction-Entropy-Seeded Parallel Skill Dispatch

## Overview

A **metaskill** that transforms every user interaction into a maximally parallel skill invocation, using the **interaction's entropy** as the seed for deterministic SplitMixTernary forking.

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                              │
│  "implement feature X with Y constraints"                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │   ENTROPY   │
                    │  EXTRACTION │
                    │ (Shannon H) │
                    └──────┬──────┘
                           │ seed = hash(interaction) & MASK64
                    ┌──────▼──────┐
                    │ SplitMix64  │
                    │   .fork(3)  │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │  GENERATOR  │ │ COORDINATOR │ │  VALIDATOR  │
    │   (+1 RED)  │ │  (0 GREEN)  │ │  (-1 BLUE)  │
    │ child[0]    │ │  child[1]   │ │  child[2]   │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                    ┌──────▼──────┐
                    │   MERGE     │
                    │  GF(3) = 0  │
                    └─────────────┘
```

## Interaction Entropy → Seed

```ruby
def interaction_to_seed(interaction_text)
  # Shannon entropy of interaction
  chars = interaction_text.chars
  freq = chars.tally
  total = chars.size.to_f
  
  h = freq.values.sum { |c| 
    p = c / total
    -p * Math.log2(p) 
  }
  
  # Hash interaction with entropy weight
  fnv1a = 0xcbf29ce484222325
  interaction_text.bytes.each do |b|
    fnv1a ^= b
    fnv1a = (fnv1a * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
  end
  
  # Combine hash with entropy bits
  entropy_bits = (h * 1_000_000).to_i
  (fnv1a ^ (entropy_bits * GOLDEN)) & MASK64
end
```

## Triadic Skill Selection

Given a task domain, select a **GF(3)-balanced triad**:

```ruby
SKILL_TRIADS = {
  sonification: {
    generator: 'supercollider-osc',      # +1: Create sound
    coordinator: 'parameter-mapping',    #  0: Map data→audio
    validator: 'spectral-invariants'     # -1: Verify bounds
  },
  derivation: {
    generator: 'gay-mcp',                # +1: Generate colors
    coordinator: 'unworld',              #  0: Chain derivations
    validator: 'three-match'             # -1: Verify 3-SAT
  },
  repl: {
    generator: 'cider-clojure',          # +1: Evaluate code
    coordinator: 'borkdude',             #  0: Select runtime
    validator: 'slime-lisp'              # -1: Type check
  },
  database: {
    generator: 'rama-gay-clojure',       # +1: Generate queries
    coordinator: 'acsets',               #  0: Schema navigation
    validator: 'clj-kondo-3color'        # -1: Lint/validate
  },
  proof: {
    generator: 'gay-mcp',                # +1: Generate terms
    coordinator: 'squint-runtime',       #  0: JS interop
    validator: 'proofgeneral-narya'      # -1: Type check
  },
  game: {
    generator: 'rubato-composer',        # +1: Compose music
    coordinator: 'glass-bead-game',      #  0: Connect domains
    validator: 'bisimulation-game'       # -1: Verify equivalence
  }
}
```

## Parallel Fanout Algorithm

```ruby
class ParallelFanout
  def initialize(interaction)
    @interaction = interaction
    @seed = interaction_to_seed(interaction)
    @rng = SplitMixTernary::Generator.new(@seed)
    @domain = detect_domain(interaction)
    @triad = SKILL_TRIADS[@domain]
  end
  
  def fanout!
    # Fork into 3 independent streams
    children = @rng.fork(3)
    
    # Dispatch in parallel (SPI-compliant)
    results = Parallel.map(0..2, in_threads: 3) do |i|
      role = [:generator, :coordinator, :validator][i]
      skill = @triad[role]
      child_seed = children[i].seed
      
      {
        role: role,
        skill: skill,
        seed: child_seed,
        trit: i - 1,  # -1, 0, +1
        result: invoke_skill(skill, @interaction, child_seed)
      }
    end
    
    # Verify GF(3) conservation
    trit_sum = results.sum { |r| r[:trit] }
    raise "GF(3) violation!" unless trit_sum % 3 == 0
    
    # Merge results
    merge_results(results)
  end
  
  private
  
  def invoke_skill(skill_name, context, seed)
    # Load skill and execute with seeded determinism
    skill = Skill.load(skill_name)
    skill.execute(context: context, seed: seed)
  end
  
  def merge_results(results)
    {
      domain: @domain,
      seed: @seed,
      seed_hex: "0x#{@seed.to_s(16)}",
      gf3_sum: 0,
      generator: results[0],
      coordinator: results[1],
      validator: results[2],
      merged: combine_outputs(results)
    }
  end
end
```

## Interaction Entropy Metrics

Track entropy across interactions for adaptive seeding:

```sql
CREATE TABLE interaction_entropy (
  interaction_id VARCHAR PRIMARY KEY,
  timestamp TIMESTAMP,
  text_length INT,
  char_entropy FLOAT,        -- Shannon entropy of characters
  word_entropy FLOAT,        -- Shannon entropy of words
  topic_entropy FLOAT,       -- Entropy of detected topics
  mode_entropy FLOAT,        -- Entropy of interaction type
  combined_entropy FLOAT,    -- Weighted combination
  seed_derived BIGINT,       -- SplitMixTernary seed
  triad_used VARCHAR[3],     -- Skills invoked
  gf3_verified BOOLEAN
);
```

## Integration with Existing Skills

### From triad-interleave
- Interleaves 3 parallel skill outputs into single stream
- Maintains per-stream ordering while maximizing parallelism

### From epistemic-arbitrage
- Triangle inequality for skill selection
- Knowledge transfer between domains via propagator network

### From spi-parallel-verify
- Guarantees `sequential == parallel` (bitwise)
- Verifies GF(3) conservation per triplet

## Commands

```bash
# Fan out on interaction
just parallel-fanout "implement X with Y"

# Show skill triad for domain
just fanout-triad sonification

# Verify SPI across all triads
just fanout-spi-verify

# Compute interaction entropy
just interaction-entropy "your message here"

# Demo full pipeline
just parallel-fanout-demo
```

## Justfile Recipes

```just
# Parallel fanout metaskill
parallel-fanout interaction:
    @echo "🔀 PARALLEL FANOUT: {{interaction}}"
    ruby -I lib -r parallel_fanout -e "ParallelFanout.new('{{interaction}}').fanout!"

# Show triad for domain
fanout-triad domain:
    @echo "🎭 SKILL TRIAD for {{domain}}"
    ruby -I lib -r parallel_fanout -e "puts ParallelFanout::SKILL_TRIADS[:{{domain}}].to_yaml"

# Interaction entropy
interaction-entropy text:
    @echo "📊 INTERACTION ENTROPY"
    ruby -I lib -r parallel_fanout -e "puts ParallelFanout.interaction_entropy('{{text}}')"

# Full demo
parallel-fanout-demo:
    @echo "🚀 PARALLEL FANOUT DEMO"
    ruby -I lib -r parallel_fanout -e "ParallelFanout.demo"
```

## GF(3) Conservation Proof

For any interaction, the metaskill selects exactly one skill per polarity:

```
Σ trits = (+1) + (0) + (-1) = 0 ≡ 0 (mod 3) ✓
```

This ensures **color balance** across the triadic dispatch:
- Generator creates (+1 RED)
- Coordinator transports (0 GREEN)  
- Validator constrains (-1 BLUE)

## Self-Reference: Metaskill as Skill

This skill can invoke itself recursively with forked seeds:

```ruby
def meta_fanout(depth: 3)
  return fanout! if depth == 0
  
  children = @rng.fork(3)
  children.map.with_index do |child, i|
    sub = ParallelFanout.new(@interaction)
    sub.instance_variable_set(:@seed, child.seed)
    sub.meta_fanout(depth: depth - 1)
  end
end
```

This creates a **skill tree** of depth N with 3^N leaves, all deterministically seeded.

## See Also

- `triad-interleave` - Stream interleaving
- `spi-parallel-verify` - Parallelism verification
- `epistemic-arbitrage` - Knowledge transfer
- `gay-mcp` - Color generation backend
- `INTERACTION_ENTROPY_FRAMEWORK.md` - Entropy metrics
- `lib/spi_parallel.rb` - SPI implementation
