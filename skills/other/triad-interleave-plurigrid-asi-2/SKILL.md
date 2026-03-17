---
name: triad-interleave
description: Interleave three deterministic color streams into balanced schedules for parallel execution and evaluation.
---

# Triad Interleave

Use this skill when asked to interleave three color streams, build triad schedules, or combine "color://" resources.

## Inputs
- sources: list of three sources (splitmix_ternary, xoroshiro_3color, gay_mcp)
- seed: hex or int
- n: number of triplets
- policy: round_robin | gf3_balanced

## Workflow
1. Generate triplets from each source.
2. Validate GF(3) sum per triplet.
3. Build schedule per policy.
4. Emit deterministic log.

## Source commands (music-topos)
- SplitMixTernary:
  `ruby -I lib -r splitmix_ternary -e "p SplitMixTernary.tripartite(0x42D).generate(5)"`
- Xoroshiro3Color:
  `ruby -I lib -r xoroshiro_3color -e "p Xoroshiro3Color::TripartiteStreams.new(0x42D).generate(5)"`
- Gay MCP: use `interleave` with `n_streams: 3` and `count: N`.

## Output schema
- schedule_id, seed, n, policy
- entries: index, stream_id, triplet_id, trit, hex, L, C, H

## Checks
- same seed -> same output
- per-stream order preserved
- GF(3) sum == 0 for each triplet

## Example prompt
"Interleave three streams (SplitMixTernary, Xoroshiro3Color, Gay MCP) for N=10 and output a deterministic schedule."
