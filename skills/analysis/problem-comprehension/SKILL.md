---
name: problem-comprehension
description: Systematic comprehension of a problem before any solving attempt. Covers restating the problem, identifying knowns, unknowns, constraints, and goal, recognizing problem type (well-defined, ill-defined, optimization, decision, puzzle), and decomposing large problems into tractable sub-problems. Use at the start of any problem-solving session to avoid solving the wrong problem.
type: skill
category: problem-solving
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/problem-solving/problem-comprehension/SKILL.md
superseded_by: null
---
# Problem Comprehension

Most problem-solving failures happen before any solving begins. A problem that is misunderstood cannot be solved accurately, and time spent on an incorrect interpretation is time lost. Comprehension is the disciplined first phase of Polya's method ("Understand the Problem"): restate, identify, classify, decompose. This skill documents the operations needed to leave comprehension with a clean problem representation that the rest of the pipeline can operate on.

**Agent affinity:** polya-ps (overall framing), jonassen (problem typology), simon (state-space representation)

**Concept IDs:** prob-problem-representation, prob-knowns-unknowns, prob-problem-types, prob-goal-decomposition

## The Comprehension Toolbox at a Glance

| # | Operation | Purpose | Key signal |
|---|---|---|---|
| 1 | Restate in own words | Verify the problem is actually understood | Can you say it without quoting? |
| 2 | Identify knowns | List every given | "Given that...," numerical data, constraints |
| 3 | Identify unknowns | List what must be found | "Find...," "determine...," "what is..." |
| 4 | Identify constraints | List limits on the solution | "Must not...," "at most...," boundary conditions |
| 5 | State the goal | Make the success criterion explicit | What tells you the problem is solved? |
| 6 | Classify problem type | Match to a known category | Well-defined vs ill-defined, decision vs optimization |
| 7 | Build a problem representation | Diagram, table, state-space | Whatever makes the structure visible |
| 8 | Decompose into sub-problems | Break into tractable pieces | Can each piece be solved separately? |
| 9 | Check for hidden assumptions | Name what you are taking for granted | What would break if this assumption fails? |
| 10 | Restate with all of the above | Confirm readable, complete understanding | The restated problem should be solvable by a peer without the original |

## Operation 1 — Restate in Your Own Words

**Pattern:** Read the problem, then state it without looking at the original. If the restatement is incomplete or wrong, comprehension has failed and no solving should begin.

**Worked example.** *"A train leaves Boston at 8 a.m. traveling 60 mph east. A second train leaves New York at 9 a.m. traveling 50 mph west on the same track. The cities are 220 miles apart. When do they meet?"*

Restatement: "Two trains on the same track, one from each end of a 220-mile segment. The eastbound train has a one-hour head start at 60 mph. The westbound starts at 50 mph. Find the time at which they occupy the same point on the track."

The restatement names every entity, every rate, every distance, and the success criterion. If any of these are missing, read the problem again.

## Operation 2 — Identify Knowns

**Pattern:** List every quantity, condition, or relationship the problem provides. Treat this as an inventory, not a narrative.

**Worked example (continued).** Knowns:
- Distance between cities: 220 miles
- Eastbound train: speed 60 mph, starts 8 a.m.
- Westbound train: speed 50 mph, starts 9 a.m.
- Both on the same track (single-track constraint — also a known)

## Operation 3 — Identify Unknowns

**Pattern:** List every value the problem asks you to find. If the problem asks for multiple things, list each separately.

**Worked example (continued).** Unknowns:
- Time of meeting (clock time or elapsed time from 8 a.m.)
- Implicitly: position along the track where they meet

The implicit unknown matters because it is required to verify the answer.

## Operation 4 — Identify Constraints

**Pattern:** List every limit on the solution space. Constraints are sometimes stated, sometimes implied by physical reality, and sometimes embedded in the problem type.

**Worked example (continued).** Constraints:
- Both trains are on the same track (physical collision)
- Both speeds are constant (no acceleration)
- The distance is fixed at 220 miles

## Operation 5 — State the Goal

**Pattern:** Write the success criterion as a sentence. "I will have solved this problem when I know [X]." This prevents drift during solving.

**Worked example (continued).** Goal: "I will have solved this problem when I know the clock time at which both trains are at the same mile marker."

## Operation 6 — Classify the Problem Type

**Pattern:** Match the problem to a known category. The category determines which solving strategies are appropriate.

Primary categories:

- **Well-defined problems** have known initial state, goal state, and legal operators. The train problem is well-defined: everything is specified and the answer is a number.
- **Ill-defined problems** have ambiguous initial or goal states. "How should our company respond to climate change?" is ill-defined because the goal itself is open.
- **Optimization problems** ask for the best value of a quantity under constraints. "Minimize shipping cost subject to..."
- **Decision problems** ask for a choice among alternatives. "Should we build plant A or plant B?"
- **Puzzles** are well-defined problems with no practical consequences — good for strategy practice.
- **Wicked problems** have no definitive formulation, no stopping rule, and stakeholders who disagree about what counts as a solution.

Recognizing the type narrows the strategy space before any work begins.

## Operation 7 — Build a Problem Representation

**Pattern:** Produce an external representation that makes the structure visible. Diagrams, tables, state-spaces, and equations all qualify.

**Worked example (continued).** A simple diagram:

```
Boston                                         New York
  |<---- 220 miles ---->|
  |-- 60 mph ----------->
                        <---- 50 mph --|
  8 a.m.                9 a.m.
```

This immediately shows that the eastbound train has a head start, which is the central difficulty of the problem.

## Operation 8 — Decompose into Sub-Problems

**Pattern:** Break the problem into pieces that can be solved independently, then combined. If the problem is small, skip this step.

**Worked example (continued).** Sub-problems:
1. How far has the eastbound train traveled when the westbound starts?
2. What is the remaining distance at 9 a.m.?
3. How fast are they closing on each other after 9 a.m.?
4. At what time after 9 a.m. does the closing distance reach zero?

Each is solvable with simple arithmetic. The combined answer falls out.

## Operation 9 — Check for Hidden Assumptions

**Pattern:** List what you are taking for granted. Hidden assumptions are the most common cause of comprehension errors.

**Worked example (continued).** Hidden assumptions:
- The trains move at constant speed (not stated but assumed)
- Boston and New York are at fixed known positions (not stated)
- Time zones are the same (true in practice but should be checked for real problems)

If any assumption fails, the answer changes.

## Operation 10 — Restate with All of the Above

**Pattern:** Produce a final restatement that a peer could solve without the original problem text. If the peer cannot, comprehension is incomplete.

**Worked example (final).** "Between Boston and New York, 220 miles apart on a single track, an eastbound train leaves Boston at 8 a.m. at 60 mph and a westbound train leaves New York at 9 a.m. at 50 mph. Both move at constant speed. Find the clock time at which they occupy the same point."

This restatement is solvable. Comprehension is complete.

## Standard Comprehension Procedure

1. Read the problem once for gist.
2. Read again slowly, applying Operations 1-5 in parallel (restate, knowns, unknowns, constraints, goal).
3. Apply Operation 6 (classify) to narrow the strategy space.
4. Apply Operation 7 (representation) to make the structure visible.
5. Apply Operation 8 (decompose) if the problem is large.
6. Apply Operation 9 (check hidden assumptions) and list any that were not explicit.
7. Apply Operation 10 (final restatement) and verify it is peer-solvable.
8. Only now hand off to strategy selection.

## When Comprehension Fails

Failures to watch for:

- **Jumping to solving** before comprehension is complete. Almost always produces the wrong answer or a solution to the wrong problem.
- **Missing a constraint.** Common when constraints are implicit (physical, legal, social).
- **Misclassifying the type.** Treating an ill-defined problem as well-defined produces false precision; treating a well-defined problem as ill-defined wastes effort.
- **Skipping representation.** Verbal-only comprehension often misses structural features that a diagram makes obvious.
- **Failing to decompose.** Tackling a large problem monolithically often leads to overwhelm and backtracking.

## Cross-References

- **strategy-selection** uses the problem representation and type to choose an approach
- **metacognitive-monitoring** checks that comprehension was actually sufficient after strategy selection begins
- **mathematical-problem-solving** relies on operations 1-10 as its own first phase
- **design-thinking-ps** extends comprehension to ill-defined problems via reframing
- **collaborative-problem-solving** distributes comprehension work across team members
