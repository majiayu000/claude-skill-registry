---
name: strategy-selection
description: Match problems to the right solving strategy. Covers working backwards, pattern recognition, simplification, systematic listing, trial and error, means-ends analysis, analogical transfer, and decomposition. Use after comprehension is complete to narrow from "general problem" to a concrete approach before committing time and effort.
type: skill
category: problem-solving
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/problem-solving/strategy-selection/SKILL.md
superseded_by: null
---
# Strategy Selection

Strategies are general-purpose operators on problems. Polya called them heuristics. Simon and Newell formalized some of them as search operators in a state-space. A good solver has many strategies and picks the right one; a weak solver has few and applies them indiscriminately. This skill is the strategy catalog and the decision rules for matching strategies to problem features.

**Agent affinity:** polya-ps (overall framing), simon (state-space strategies), newell (means-ends analysis)

**Concept IDs:** prob-working-backwards, prob-pattern-recognition, prob-simplification, prob-systematic-listing, prob-trial-error-iteration

## The Strategy Catalog at a Glance

| # | Strategy | When it applies | Key signal |
|---|---|---|---|
| 1 | Working backwards | Goal is clear, path is obscure | "You need the goal to find the start" |
| 2 | Pattern recognition | Problem looks like one you've seen | "This is a ___ problem in disguise" |
| 3 | Simplification | Full problem is intractable | Solve for n=2, then generalize |
| 4 | Systematic listing | Finite solution space, risk of missing cases | Combinatorics, case analysis |
| 5 | Trial and error with tracking | No obvious path, need to explore | Try, evaluate, adjust, track |
| 6 | Means-ends analysis | Goal and current state both known | Reduce the difference |
| 7 | Analogical transfer | Known solution to structurally similar problem | Map source to target domain |
| 8 | Decomposition | Problem is large but separable | Sub-problems with clean interfaces |
| 9 | Drawing a diagram | Structure is hidden in prose | Spatial, relational, flow problems |
| 10 | Forward chaining | Start is clear, goal is vague | Explore from knowns |

## Strategy 1 — Working Backwards

**Pattern:** Start from the goal state and ask "what would have to be true one step before this?" Repeat until you reach the initial state.

**When it applies:**
- Goal is precisely specified
- Initial state allows many possible first moves (high branching factor)
- Inverse operators exist for most forward operators

**Worked example.** *"Find x such that 3x + 5 = 20."* Working backwards: if 3x + 5 = 20, then 3x = 15 (inverse of +5), then x = 5 (inverse of *3). Done.

## Strategy 2 — Pattern Recognition

**Pattern:** Ask "have I seen this problem before?" If yes, transfer the known solution structure.

**When it applies:**
- The problem has a familiar shape even if the surface details differ
- You have solved similar problems before and remember the method
- The mapping between the new problem and the known solution is clean

## Strategy 3 — Simplification

**Pattern:** Reduce the problem to a smaller or simpler version, solve that, then generalize or scale up.

**Worked example.** *"In how many ways can n students line up?"* Try n=1 (1 way), n=2 (2 ways), n=3 (6 ways), n=4 (24 ways). Pattern: n!. The full problem is solved by solving the small cases first.

## Strategy 4 — Systematic Listing

**Pattern:** Enumerate all possibilities in a structured way to guarantee completeness.

**When it applies:**
- The solution space is finite and small enough to enumerate
- Missing a case would be catastrophic (correctness critical)
- The structure of the enumeration is clear

## Strategy 5 — Trial and Error with Tracking

**Pattern:** Try an approach, evaluate, note what you learned, try a modified approach. Track attempts so you do not repeat failures.

**When it applies:**
- No obvious strategy applies
- Problem is small enough that multiple attempts are affordable
- Evaluation after each attempt is cheap

This is not random guessing; each trial is informed by the previous one.

## Strategy 6 — Means-Ends Analysis

**Pattern:** Compute the difference between the current state and the goal state. Choose an operator that reduces the difference. Apply. Repeat.

**When it applies:**
- Both current state and goal are known
- Operators can be ranked by how much they reduce the state difference
- This is the core strategy of Simon and Newell's General Problem Solver

## Strategy 7 — Analogical Transfer

**Pattern:** Find a solved problem with the same structural form, map entities between source and target, transfer the solution.

**When it applies:**
- A known solved problem shares underlying structure with the target
- The mapping is clean (each entity in the source corresponds to one in the target)
- The solution method in the source has no hidden domain-specific steps

Analogy is powerful but risky: surface similarity without structural similarity produces wrong answers.

## Strategy 8 — Decomposition

**Pattern:** Break the problem into sub-problems with clean interfaces. Solve each sub-problem. Combine.

**When it applies:**
- Problem is large but separable
- Sub-problems are roughly independent
- The combination step is well-defined

## Strategy 9 — Drawing a Diagram

**Pattern:** Translate the problem into a spatial or relational representation. Geometry, flow diagrams, graphs, state-spaces.

**When it applies:**
- Problem has spatial, relational, or temporal structure
- The structure is hidden in prose
- The diagram reveals constraints or symmetries not obvious in words

## Strategy 10 — Forward Chaining

**Pattern:** Start from the knowns and generate consequences until you reach (or approach) the goal.

**When it applies:**
- Initial state is well specified
- Goal is vague or distant
- Operators are well-understood forward rules

## The Strategy Decision Tree

A rough procedure for choosing:

1. **Is the problem familiar?** → Pattern recognition (Strategy 2)
2. **Is the goal clearer than the path?** → Working backwards (Strategy 1)
3. **Is the full problem too big?** → Simplification or decomposition (Strategy 3 or 8)
4. **Is the solution space finite and small?** → Systematic listing (Strategy 4)
5. **Do you know both endpoints?** → Means-ends analysis (Strategy 6)
6. **Is there a solved problem with the same structure?** → Analogical transfer (Strategy 7)
7. **Does the problem have spatial or relational structure?** → Draw a diagram (Strategy 9)
8. **None of the above?** → Trial and error with tracking (Strategy 5) + forward chaining (Strategy 10)

## Combining Strategies

Most real problems need more than one strategy. A typical pattern:

1. **Decompose** the problem into sub-problems
2. **Pattern-match** each sub-problem to a known type
3. Apply the strategy specific to each type
4. **Combine** results
5. Use **metacognitive-monitoring** to check that combined pieces answer the original question

## When Strategy Selection Fails

- **Premature commitment.** Locking in on the first strategy that comes to mind. Evaluate at least two before picking.
- **Strategy without comprehension.** Strategies are operators on a problem representation. No representation → no strategy.
- **Wrong-level strategy.** Applying a structural strategy (decomposition) to a problem that is actually a pattern-recognition problem wastes effort.
- **No fallback.** If the chosen strategy fails, have a second strategy ready rather than starting over.

## Cross-References

- **problem-comprehension** produces the representation that strategy selection operates on
- **mathematical-problem-solving** applies many of these strategies to math-specific contexts
- **design-thinking-ps** adds ideation and prototyping strategies for ill-defined problems
- **metacognitive-monitoring** evaluates whether a chosen strategy is actually working
- **collaborative-problem-solving** allows different team members to pursue different strategies in parallel
