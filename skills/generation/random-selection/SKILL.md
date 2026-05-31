---
name: random-selection
description: Randomly select items from lists using various algorithms for fair and unbiased selection
---

# Random Selection Skill

Perform random selection with various algorithms for fair, unbiased outcomes.

## When to Use
- Prize drawings
- Random sampling
- A/B test group assignment
- Survey participant selection

## Core Capabilities
- Simple random selection
- Weighted random selection
- Stratified sampling
- Shuffle/randomize lists
- Unique selection (no duplicates)
- Reproducible randomness (seeded)

## Examples
```bash
# Bash: Random line from file
shuf -n 1 items.txt

# Python: Simple random
import random
items = ['A', 'B', 'C', 'D']
selected = random.choice(items)

# Python: Multiple unique items
selected = random.sample(items, 2)

# Python: Weighted selection
weights = [10, 5, 3, 1]
selected = random.choices(items, weights=weights, k=1)

# Python: Seeded (reproducible)
random.seed(42)
selected = random.choice(items)
```

## Algorithms
- **Uniform**: Equal probability
- **Weighted**: Based on weights
- **Reservoir sampling**: For streams
- **Fisher-Yates shuffle**: Unbiased shuffling

## Best Practices
- Use cryptographically secure random for security
- Document seed for reproducibility
- Verify distribution for large samples
- Handle edge cases (empty list, single item)

## Resources
- Python random: https://docs.python.org/3/library/random.html
- secrets (secure): https://docs.python.org/3/library/secrets.html
