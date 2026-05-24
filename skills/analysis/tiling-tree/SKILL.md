---
name: tiling-tree
description: Exhaustive problem space exploration using the MIT Synthetic Neurobiology "tiling tree" method. Partitions a problem into MECE (Mutually Exclusive, Collectively Exhaustive) subsets recursively via parallel subagents, then evaluates leaf ideas against specified criteria. Use when users say "tiling tree", "tile the solution space", "exhaustively explore approaches to", "what are all the ways to", or request a MECE breakdown of a problem. Requires orchestrating-agents skill.
metadata:
  version: 1.0.1
  depends_on: orchestrating-agents
---

# Tiling Tree

Implements the MIT Synthetic Neurobiology tiling tree method: recursively partition a problem space into non-overlapping, collectively exhaustive subsets until reaching actionable leaf ideas, then evaluate those leaves.

## Core Concept

The method's power comes from MECE splits forcing exploration of unfamiliar territory. A split is only valid when you can state precisely what each branch **excludes** — if you can't, the criterion is too vague and branches will overlap.

Key insight from the source method: always look for the "third option" that falls outside an obvious binary split. The bloodstream-secretion approach to neural recording only emerged because "wired vs. wireless" was defined precisely enough to reveal it covered neither case.

## When to Use

- "What are all the ways we could solve X?"
- "Apply the tiling tree method to Y"
- "Exhaustively map the solution space for Z"
- Any request for MECE decomposition of a problem domain

## Setup

Requires `orchestrating-agents` skill to be installed. Load it first:

```python
import sys
sys.path.insert(0, '/mnt/skills/user/orchestrating-agents/scripts')

from claude_client import invoke_claude, invoke_parallel, parse_json_response
```

## Running the Tiling Tree

```bash
# Basic usage
python3 /mnt/skills/user/tiling-tree/scripts/tiling_tree.py "Your problem here"

# With options
python3 /mnt/skills/user/tiling-tree/scripts/tiling_tree.py \
  "How can we record neural activity?" \
  --depth 3 \
  --criteria "impact,novelty,feasibility" \
  --output /mnt/user-data/outputs/neural_recording_tree.md
```

## Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| `problem` | required | Natural language problem statement |
| `--depth` | 2 | Max recursion depth. Depth 2 ≈ 16 leaves, depth 3 ≈ 64 leaves |
| `--criteria` | `impact,novelty,feasibility` | Comma-separated evaluation dimensions |
| `--output` | `tiling_tree.md` | Output markdown path |

**Depth guidance:** Start with depth 2 to validate the problem framing. Increase to 3 only when the domain genuinely warrants it — depth 3 generates ~64 leaves and ~40 API calls.

## Architecture

- **Orchestrator** (this script): builds tree skeleton, dispatches parallel split jobs per level, merges results, detects gaps
- **Branch agents** (`invoke_parallel`): each receives one node to split, returns MECE branches with explicit exclusion statements
- **Evaluator** (`invoke_claude`): single agent scores all leaves for cross-leaf consistency

Parallel splitting happens level-by-level (not node-by-node), so a depth-2 tree makes only 2 API round-trips for the splitting phase regardless of branching factor.

## Output

A markdown file containing:
1. Full tree diagram with split criteria and evaluation scores at leaves
2. Ranked leaf table sorted by overall score

## Interpreting Results

Good trees have:
- Split criteria that are definitions, not questions ("energy source type" not "is it renewable?")
- Leaf exclusions that confirm non-overlap
- A "surprising" branch — something you wouldn't have thought of without the tree

If all leaves feel obvious, the split criteria were too coarse. Redo the tree with more precise definitions at the branch level where it went flat.
