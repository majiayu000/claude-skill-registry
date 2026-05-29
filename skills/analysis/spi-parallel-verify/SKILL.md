---
name: spi-parallel-verify
description: Verify Strong Parallelism Invariance (SPI) and GF(3) conservation for 3-way color streams with arbitrary precision.
---

# SPI Parallel Verify

Use when validating that parallel, shuffled, or split execution yields identical results.

## Inputs
- seed, indices, precision
- sources (optional): splitmix_ternary, xoroshiro_3color, gay_mcp

## Workflow
1. Compute ordered, reversed, shuffled results.
2. Compute parallel split if available.
3. Compare at fixed precision or via hex.
4. Validate GF(3) per triplet.
5. Emit a deterministic report.

## Commands (music-topos)
- `just spi-verify`
- `just spi-gf3-parallel`
- `ruby -I lib -r splitmix_ternary -e "require 'json'; puts JSON.pretty_generate(SplitMixTernary.prove_out_of_order)"`

## Acceptance
- ordered == reversed == shuffled
- parallel == sequential
- gf3_ok == true
- avoid float truncation of RNG state

## Report fields
- seed, indices, all_equal, parallel_ok, gf3_ok, precision

## Example prompt
"Verify SPI and GF(3) for 3-stream triads at seed 0x42D and report determinism."
