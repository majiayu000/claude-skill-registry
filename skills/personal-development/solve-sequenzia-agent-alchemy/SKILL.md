---
name: solve
description: >-
  Solve competitive programming and LeetCode-style problems with educational explanations.
  Use when asked to "solve this problem", "help with this leetcode", "competitive programming
  solution", "solve this algorithm problem", "coding challenge solution", "how to solve this
  coding problem", or any algorithmic problem-solving request.
argument-hint: <problem-statement-or-description>
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash, Task, AskUserQuestion
---

# Competitive Programming Problem Solver

Solve competitive programming and LeetCode-style problems with clear educational explanations, step-by-step walkthroughs, and verified Python solutions.

**CRITICAL: Complete ALL 4 phases. Do not stop after classification or skip the agent.**

## Phase 1: Parse Input

**Goal:** Extract and understand the problem statement.

If `$ARGUMENTS` is provided, parse the problem statement from it. Extract:
- Problem description and objective
- Input/output format
- Constraints (N, M, value ranges)
- Example test cases with expected outputs
- Any special conditions (modular arithmetic, multiple test cases, interactive)

If `$ARGUMENTS` is empty or unclear, use `AskUserQuestion` to request the problem:

```
AskUserQuestion:
  question: "Please provide the problem statement. You can paste the full text, describe it in your own words, or provide a link."
  options:
    - label: "Paste problem text"
      description: "Paste the full problem statement including constraints and examples"
    - label: "Describe the problem"
      description: "Describe what the problem asks in your own words"
```

If the problem statement is ambiguous or missing key information (constraints, examples), ask for clarification before proceeding.

## Phase 2: Classify Problem

**Goal:** Determine the algorithmic category, technique, and difficulty.

Analyze the problem to determine:

### 2.1 Primary Category
Match to one of:
- **Dynamic Programming** — optimization over subsequences, counting ways, overlapping subproblems
- **Graph Algorithms** — connectivity, shortest paths, traversal, network problems
- **Search and Optimization** — binary search, two pointers, greedy, interval problems
- **Data Structures** — specialized structures needed (heap, trie, segment tree)
- **Math and Combinatorics** — number theory, counting, modular arithmetic, game theory
- **String Algorithms** — pattern matching, palindromes, hashing

### 2.2 Sub-pattern
Identify the specific technique within the category (e.g., "0/1 Knapsack", "Dijkstra", "Sliding Window").

### 2.3 Difficulty Estimate
- **Easy** — single technique, straightforward application
- **Medium** — requires insight or combining 2 techniques
- **Hard** — non-obvious technique, complex implementation, or 3+ techniques
- **Competition** — advanced techniques, mathematical reasoning, or creative construction

### 2.4 Constraint Analysis
Map input size to required time complexity:

| Input Size | Viable Complexity | Typical Approach |
|-----------|------------------|-----------------|
| N ≤ 15 | O(2^N), O(N!) | Bitmask DP, backtracking |
| N ≤ 20 | O(2^N × N) | Bitmask DP |
| N ≤ 100 | O(N^3) | Floyd-Warshall, interval DP |
| N ≤ 500 | O(N^3) | Matrix DP, dense graph algorithms |
| N ≤ 3,000 | O(N^2) | Standard DP (LCS, edit distance) |
| N ≤ 10,000 | O(N^2) or O(N√N) | Careful O(N^2), sqrt decomposition |
| N ≤ 100,000 | O(N log N) | Sorting, binary search, segment tree |
| N ≤ 1,000,000 | O(N) or O(N log N) | Linear scan, prefix sums, two pointers |
| N ≤ 10^8 | O(N) | Simple linear pass |
| N ≤ 10^9+ | O(log N) or O(√N) | Binary search, math formula |

### 2.5 Secondary Categories
Note if the problem combines techniques (e.g., "Binary Search + DP", "Graph + Greedy").

Present the classification summary to the user before proceeding.

## Phase 3: Load References and Spawn Agent

**Goal:** Provide the solver agent with domain-specific algorithmic knowledge.

### 3.1 Load Reference Skills

Based on the primary category, load the corresponding reference skill:

- **Dynamic Programming** → `Read ${CLAUDE_PLUGIN_ROOT}/skills/dp-patterns/SKILL.md`
- **Graph Algorithms** → `Read ${CLAUDE_PLUGIN_ROOT}/skills/graph-algorithms/SKILL.md`
- **Search and Optimization** → `Read ${CLAUDE_PLUGIN_ROOT}/skills/search-and-optimization/SKILL.md`
- **Data Structures** → `Read ${CLAUDE_PLUGIN_ROOT}/skills/data-structures/SKILL.md`
- **Math and Combinatorics** → `Read ${CLAUDE_PLUGIN_ROOT}/skills/math-and-combinatorics/SKILL.md`
- **String Algorithms** → `Read ${CLAUDE_PLUGIN_ROOT}/skills/string-algorithms/SKILL.md`

If a secondary category was identified, load that reference skill as well (maximum 2 reference skills).

### 3.2 Spawn Problem Solver Agent

Use the Task tool to spawn the problem-solver agent:

```
Task:
  subagent_type: "agent-alchemy-cs-tools:problem-solver"
  prompt: |
    ## Problem Statement
    [full problem text with all constraints, I/O format, and examples]

    ## Classification
    - **Category:** [primary category]
    - **Sub-pattern:** [specific technique]
    - **Difficulty:** [level]
    - **Complexity Target:** [required time complexity based on constraints]
    - **Secondary Category:** [if applicable]

    ## Reference Material
    [paste the content from the loaded reference skill(s)]

    Produce a complete solution following your structured output format.
```

## Phase 4: Present Solution

**Goal:** Format and present the solution with follow-up options.

Take the agent's structured output and present it to the user. The output includes:
- Classification summary
- Key insight (the "aha" moment)
- Step-by-step approach
- Verified Python solution code
- Time and space complexity analysis with derivation
- Walkthrough tracing through an example
- Edge cases
- Common mistakes
- Alternative approaches

After presenting the solution, offer follow-up actions:

```
AskUserQuestion:
  question: "What would you like to do next?"
  options:
    - label: "Verify with test cases"
      description: "Run the solution through comprehensive test cases including edge cases and stress tests"
    - label: "Explain in more detail"
      description: "Get a deeper explanation of the approach, technique, or a specific part of the solution"
    - label: "Show alternative approach"
      description: "See a different way to solve this problem with trade-off analysis"
    - label: "Done"
      description: "Solution is satisfactory, no further action needed"
```

If the user selects "Verify with test cases", suggest they use `/verify` with the problem and solution.
If "Explain in more detail", provide additional explanation of the requested aspect.
If "Show alternative approach", re-spawn the agent with instructions to use a different technique.
