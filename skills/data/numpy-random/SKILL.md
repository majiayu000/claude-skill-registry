---
name: numpy-random
description: NumPy's random module shifted from the legacy RandomState to the modern
  Generator API. This new approach provides better statistical properties, faster
  algorithms, and a robust system for parallel random number generation using SeedSequence.
---

---
name: numpy-random
description: Modern random number generation using the Generator API, focusing on statistical properties, parallel streams, and reproducibility. Triggers: random, rng, default_rng, SeedSequence, probability distributions, shuffle.
---

## Overview
NumPy's `random` module shifted from the legacy `RandomState` to the modern `Generator` API. This new approach provides better statistical properties, faster algorithms, and a robust system for parallel random number generation using `SeedSequence`.

## When to Use
- Stochastic simulations requiring high-quality random bits.
- Shuffling datasets for machine learning training.
- Generating independent random streams for parallel computing workers.
- Creating reproducible experiments across different runs.

## Decision Tree
1. Starting a new project?
   - Use `np.random.default_rng()`. Do not use `np.random.seed()`.
2. Need independent streams for multiple CPUs?
   - Use `SeedSequence.spawn()` to create children.
3. Shuffling in-place?
   - Use `rng.shuffle(arr)`. For a copy, use `rng.permuted(arr)`.

## Workflows
1. **Parallel Random Stream Generation**
   - Initialize a SeedSequence with a high-quality entropy source.
   - Use the `.spawn(n)` method to create independent seed sequences for workers.
   - Instantiate a new Generator for each worker using its specific child sequence.

2. **Reproducible Simulation Setup**
   - Obtain a 128-bit seed (e.g., using `secrets.randbits(128)`).
   - Initialize the generator: `rng = np.random.default_rng(seed)`.
   - Log the seed to allow exact reproduction of the stochastic results in future runs.

3. **In-Place Array Shuffling**
   - Create a Generator instance.
   - Pass an existing array to `rng.shuffle(arr)` to modify it in-place.
   - Specify the `axis` parameter if only certain dimensions (e.g., rows) should be rearranged.

## Non-Obvious Insights
- **Legacy Discouragement:** `RandomState` is essentially in maintenance mode; `Generator` is faster and has better statistical distribution qualities.
- **Small Seed Limitation:** Seeding with small integers (0-100) limits the reachable state space; `SeedSequence` ensures high-entropy starting states.
- **Bitstream Instability:** Even with the same seed, the bitstream is not guaranteed to be identical across different NumPy versions due to algorithmic improvements.

## Evidence
- "In general, users will create a Generator instance with default_rng and call the various methods on it to obtain samples." [Source](https://numpy.org/doc/stable/reference/random/index.html)
- "SeedSequence mixes sources of entropy in a reproducible way to set the initial state for independent and very probably non-overlapping BitGenerators." [Source](https://numpy.org/doc/stable/reference/random/bit_generators/index.html)

## Scripts
- `scripts/numpy-random_tool.py`: Implements parallel seed spawning and reproducible RNG.
- `scripts/numpy-random_tool.js`: Basic random sampling logic.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)