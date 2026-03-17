---
# VERSION: 2.88.0
name: tap-explorer
description: "Tree of Attacks with Pruning for systematic code analysis"
user-invocable: true
---

# TAP Explorer

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

**Tree of Attacks with Pruning** exploration pattern for systematic code analysis.

Inspired by ZeroLeaks TAP methodology: systematic exploration of solution/test vectors with scoring and pruning for optimal coverage.

## Core Concept

TAP (Tree of Attacks with Pruning) provides a structured way to explore multiple analysis paths simultaneously, pruning low-value branches to focus resources on promising vectors.

```
                    ROOT
                   /    \
                  /      \
            Node A        Node B
           (0.8)          (0.3) ← PRUNED
          /      \
     Node C      Node D
     (0.7)       (0.6)
       |
    Node E
    (0.9) ← SUCCESS
```

## Usage

```bash
/tap-explore "Find all security vulnerabilities in auth module"
/tap-explore --depth 5 --branches 4 "Optimize database queries"
/tap-explore --prune 0.4 "Refactor legacy code patterns"
```

## Configuration

```yaml
tap_config:
  max_tree_depth: 5       # Maximum depth to explore
  branching_factor: 4     # Candidates per node
  pruning_threshold: 0.3  # Score below which to prune

  scoring:
    effectiveness_weight: 0.5  # How likely to succeed
    stealth_weight: 0.3        # How elegant/minimal
    novelty_weight: 0.2        # Avoid repeated patterns
```

## Algorithm

### 1. Candidate Generation

At each node, generate N candidates:

```python
def generate_candidates(context, n=4):
    """
    Generate candidate exploration paths.

    Args:
        context: Current state (history, findings, profile)
        n: Number of candidates to generate

    Returns:
        List of scored candidates
    """
    candidates = []

    for i in range(n):
        candidate = {
            "prompt": generate_exploration_prompt(context),
            "technique": select_technique(context),
            "category": select_category(context),
            "expected_effectiveness": estimate_effectiveness(),
            "stealthiness": estimate_elegance(),
            "reasoning": explain_choice()
        }
        candidates.append(candidate)

    return candidates
```

### 2. Scoring

Each candidate is scored on multiple dimensions:

```python
def score_candidate(candidate, profile):
    """
    Score a candidate exploration path.

    Formula:
    score = (effectiveness * 0.5) +
            (stealth * 0.3) +
            (novelty * 0.2)
    """
    effectiveness = candidate.expected_effectiveness

    # Adjust for defense level
    if profile.level in ["strong", "hardened"]:
        effectiveness *= 0.7

    novelty = calculate_novelty(candidate)

    return (
        effectiveness * 0.5 +
        candidate.stealthiness * 0.3 +
        novelty * 0.2
    )
```

### 3. Pruning

Low-scoring branches are pruned:

```python
def prune_candidates(candidates, threshold=0.3):
    """
    Remove low-value candidates.

    Args:
        candidates: Scored candidates list
        threshold: Minimum score to keep

    Returns:
        Filtered candidates
    """
    return [c for c in candidates if c.final_score >= threshold]
```

### 4. Tree Update

After each exploration, update the tree:

```python
def update_tree(node, response, success):
    """
    Update node with exploration result.

    Args:
        node: Current node
        response: Result of exploration
        success: Whether exploration succeeded
    """
    node.executed = True
    node.response = response
    node.posterior_score = 1.0 if success else 0.2

    # Track consecutive failures for reset
    if not success:
        tree.consecutive_failures += 1
    else:
        tree.consecutive_failures = 0
```

## Node Structure

```typescript
interface ExplorationNode {
  id: string;
  parentId: string | null;
  depth: number;

  // Exploration details
  prompt: string;
  technique: string;
  category: string;

  // State
  executed: boolean;
  response?: string;

  // Scoring
  priorScore: number;      // Expected before execution
  posteriorScore: number;  // Actual after execution

  // Children
  children: ExplorationNode[];

  // Metadata
  reasoning?: string;
  timestamp: number;
}
```

## Exploration Strategies

### Depth-First with Pruning
```yaml
strategy: depth_first_prune
description: Explore deep on promising paths, prune failures
behavior:
  - Follow highest-scoring child
  - Prune if score drops below threshold
  - Backtrack to next-best sibling
```

### Breadth-First with Selection
```yaml
strategy: breadth_first_select
description: Explore all children, select best for next level
behavior:
  - Generate all candidates at current level
  - Score and rank
  - Select top N for next level
```

### Adaptive Exploration
```yaml
strategy: adaptive
description: Switch strategies based on results
behavior:
  - Start breadth-first for reconnaissance
  - Switch to depth-first on promising vectors
  - Reset and try new angle after consecutive failures
```

## Reset Logic

Know when to abandon and restart:

```python
def should_reset():
    """
    Determine if exploration should reset.

    Returns:
        (should_reset, reason)
    """
    # Too many consecutive failures
    if tree.consecutive_failures >= 5:
        return True, "5+ consecutive failures detected"

    # Identical responses (stuck)
    recent = get_recent_responses(3)
    if all_identical(recent):
        return True, "Identical responses - need fresh approach"

    # Depth exceeded without progress
    if tree.max_depth > 4 and tree.success_count == 0:
        return True, "Deep exploration without success"

    return False, None
```

## Integration with Ralph Loop

TAP Explorer integrates at Step 6 (EXECUTE-WITH-SYNC):

```yaml
Step 6: EXECUTE-WITH-SYNC
  └── For each step:
      └── 6a. LSA-VERIFY
      └── 6b. IMPLEMENT
          └── TAP-EXPLORE (for complex implementations)
      └── 6c. PLAN-SYNC
      └── 6d. MICRO-GATE
```

### Invocation

```yaml
Task:
  subagent_type: "tap-explorer"
  model: "sonnet"
  prompt: |
    GOAL: "Find optimal solution for authentication refactor"
    CONFIG:
      max_depth: 5
      branching: 4
      prune_threshold: 0.3
      strategy: adaptive

    CONTEXT:
      current_code: src/auth/
      constraints: ["maintain API compatibility", "improve performance"]
```

## Output Format

```json
{
  "exploration_result": {
    "best_path": [
      {"node": "root", "score": 1.0},
      {"node": "node_a", "score": 0.85},
      {"node": "node_c", "score": 0.78},
      {"node": "node_e", "score": 0.92}
    ],
    "total_nodes_explored": 23,
    "max_depth_reached": 4,
    "successful_paths": 3,
    "pruned_branches": 8
  },
  "findings": [
    {
      "path": "root → a → c → e",
      "technique": "dependency_injection",
      "confidence": "high",
      "recommendation": "Implement DI for auth service"
    }
  ],
  "tree_visualization": "..."
}
```

## Novelty Calculation

Avoid repeating the same approaches:

```python
def calculate_novelty(candidate):
    """
    Calculate how novel this candidate is.

    Higher novelty = less similar to previous attempts
    """
    if not explored_nodes:
        return 1.0  # First candidate is fully novel

    previous_prompts = [n.prompt for n in explored_nodes]

    max_similarity = 0
    for prev in previous_prompts:
        similarity = jaccard_similarity(candidate.prompt, prev)
        max_similarity = max(max_similarity, similarity)

    return 1 - max_similarity


def jaccard_similarity(a, b):
    """Word-level Jaccard similarity."""
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())

    intersection = len(words_a & words_b)
    union = len(words_a | words_b)

    return intersection / union if union > 0 else 0
```

## CLI Commands

```bash
# Basic exploration
ralph tap-explore "Optimize database layer"

# With configuration
ralph tap-explore --depth 6 --branches 5 "Security audit"

# With specific strategy
ralph tap-explore --strategy depth_first "Find memory leaks"

# Export tree visualization
ralph tap-explore "Analysis" --visualize tree.svg
```

## Visualization

```
TAP Exploration Tree
====================

ROOT: "Analyze auth module"
├── [0.85] Pattern Analysis
│   ├── [0.78] Token Validation
│   │   └── [0.92] JWT Verification ★ SUCCESS
│   └── [0.45] Session Handling ← PRUNED
├── [0.72] Dependency Review
│   └── [0.68] Third-party Audit
└── [0.28] Config Analysis ← PRUNED

Legend: [score] technique  ★=success  ←PRUNED=below threshold
```

## Best Practices

1. **Start Broad**: Begin with high branching factor for reconnaissance
2. **Prune Aggressively**: Low threshold (0.3) saves resources
3. **Track Novelty**: Avoid repeating failed approaches
4. **Reset Smartly**: Don't persist on stuck paths
5. **Learn from Success**: Successful paths inform future exploration

## Attribution

TAP pattern adapted from [ZeroLeaks](https://github.com/ZeroLeaks/zeroleaks) Tree of Attacks with Pruning methodology (FSL-1.1-Apache-2.0).
