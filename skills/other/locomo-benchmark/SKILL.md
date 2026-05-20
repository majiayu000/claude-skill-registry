---
name: locomo-benchmark
description: Run LoCoMo benchmark for long-term conversational memory
execution: inline
model: inherit
aliases: [locomo, benchmark-memory]
---

# LoCoMo Benchmark

Evaluate cc-soul's memory against the [LoCoMo benchmark](https://github.com/snap-research/locomo) (ACL 2024) for long-term conversational memory.

## Quick Start

Run the benchmark script:

```bash
# Test one conversation (default: conv-26)
python3 $PLUGIN_DIR/scripts/locomo-benchmark.py

# Test specific conversations
python3 $PLUGIN_DIR/scripts/locomo-benchmark.py conv-26 conv-30

# Full benchmark (all 10 conversations)
python3 $PLUGIN_DIR/scripts/locomo-benchmark.py --full

# Limit QA pairs per conversation
python3 $PLUGIN_DIR/scripts/locomo-benchmark.py --max-qa 20
```

Where `$PLUGIN_DIR` is `/maps/projects/fernandezguerra/apps/repos/cc-soul` (or installed plugin path).

## What the Script Does

1. **Downloads** LoCoMo data from GitHub to `/tmp/locomo/` (if not present)
2. **Ingests** conversations into cc-soul memory:
   - Extracts session summaries as observations
   - Creates triplets for speaker facts
   - Tags with sample_id for retrieval
3. **Evaluates** QA pairs:
   - Retrieves context using `chitta recall --tag {sample_id}`
   - Calculates F1 score vs ground truth
4. **Reports** results by category

## Categories

| Cat | Name | Description |
|-----|------|-------------|
| 1 | Multi-hop | Requires connecting multiple facts |
| 2 | Single-hop | Direct fact retrieval |
| 3 | Temporal | Date/time questions |
| 4 | Open-domain | General knowledge |
| 5 | Adversarial | Should answer "no information" |

## Baseline Scores (from paper)

| Model | F1 |
|-------|-----|
| Human ceiling | 87.9% |
| AutoMem | 90.5% |
| GPT-4 | 32.1% |
| GPT-3.5 | 23.7% |
| Mistral-7B | 13.9% |

## Data

- Repository: `https://github.com/snap-research/locomo`
- Local cache: `/tmp/locomo/data/locomo10.json`
- 10 conversations, ~200 QA pairs each, ~35 sessions per conversation

## Manual Execution

If you prefer to run manually:

```bash
# Ensure data exists
git clone https://github.com/snap-research/locomo /tmp/locomo

# Run benchmark
python3 /maps/projects/fernandezguerra/apps/repos/cc-soul/scripts/locomo-benchmark.py conv-26
```

## Expected Output

```
=== LoCoMo Benchmark Results ===

Total QA Pairs: 50
Overall F1: XX.X%

By Category:
  Multi-hop (n=XX): XX.X%
  Single-hop (n=XX): XX.X%
  Temporal (n=XX): XX.X%
  Open-domain (n=XX): XX.X%
  Adversarial (n=XX): XX.X%

Per Conversation:
  conv-26: XX.X% (50 QA)

Comparison (from paper):
  Human ceiling: 87.9%
  GPT-4 baseline: 32.1%
  cc-soul: XX.X%
```
