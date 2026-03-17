---
name: aoc
description: "Solve Advent of Code puzzles, algorithm challenges, and competitive programming problems. Activate when user provides AoC problem context/input, mentions solving puzzles/challenges, asks about algorithm selection (BFS, DFS, DP, etc.), or needs help with parsing structured input."
---

# Advent of Code Solver

Language-agnostic problem-solving with **TDD** and **correctness-first** approach.

## Workflow

```
1. READ      → Study problem + examples (examples are your spec)
2. PARSE     → Extract data structures from input
3. TEST      → Write tests from example input/output
4. IMPLEMENT → Minimal code to pass
5. RUN       → Execute on real input
6. ADAPT     → Refactor for Part 2
```

## Solution Architecture

```
parse(input) → data structure
part1(data)  → answer
part2(data)  → answer
```

Parse once. Solve both parts. Test each function independently.

## Algorithm Selection

| Scenario | Algorithm |
|----------|-----------|
| Unweighted shortest path | BFS |
| Path existence / exhaustive | DFS |
| Weighted shortest path | Dijkstra |
| Weighted + good heuristic | A* |
| "After N iterations..." (huge N) | Cycle detection |
| "Find minimum X such that..." | Binary search |
| "Count ways..." / "Min/max..." | Dynamic programming |
| Connected regions | Flood fill |

**Deep dive**: See [algorithms.md](cookbook/algorithms.md)

## Input Patterns

| Format | Approach |
|--------|----------|
| Numbers in text | Regex `-?\d+` |
| Grid of chars | 2D array or dict by coords |
| Blank-line groups | Split on `\n\n` first |
| Key-value pairs | Parse into map/dict |
| Instructions/opcodes | Pattern match each line |

**Grids**: Use `(row, col)` with row↓. Sparse dict for infinite/sparse grids.
**Directions**: `UP=(-1,0), DOWN=(1,0), LEFT=(0,-1), RIGHT=(0,1)`

**Deep dive**: See [parsing.md](cookbook/parsing.md)

## Part 2 Patterns

1. **Scale up** → Optimize algorithm
2. **Add dimensions** → 2D → 3D/4D
3. **Many iterations** → Find cycle, skip ahead
4. **Reverse question** → "Find X" → "Given X, find Y"
5. **Add constraints** → New rules or edge cases

## Debugging

- Print intermediate state at each step
- Compare with example walkthrough
- Add assertions for every assumption
- Test parsing separately from logic
- Binary search on input size to isolate failures

## Complexity Targets

| Input Size | Target |
|------------|--------|
| n ≤ 20 | O(2^n) OK |
| n ≤ 500 | O(n³) OK |
| n ≤ 10,000 | O(n²) OK |
| n ≤ 1,000,000 | O(n log n) |
| n > 1,000,000 | O(n) or O(log n) |

## Research Tools

```
# gh search code for algorithm implementations
gh search code "heapq.heappush" --language=python   # Dijkstra/priority queue
gh search code "collections.deque" --language=python # BFS patterns
gh search code "fn dijkstra" --language=rust
```

## References

- [algorithms.md](cookbook/algorithms.md) - Graph traversal, DP, cycle detection, search
- [parsing.md](cookbook/parsing.md) - Input formats, grids, coordinates, hex grids
- [reference.md](reference.md) - Data structures, optimization, anti-patterns
