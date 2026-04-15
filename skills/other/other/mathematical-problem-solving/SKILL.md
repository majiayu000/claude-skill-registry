---
name: mathematical-problem-solving
description: Polya's four-phase method applied to mathematical problems, extended with Schoenfeld's control/monitoring layer. Covers understand, devise plan, carry out, look back. Includes heuristics specific to math (specialize, generalize, vary the problem, introduce auxiliary elements) and the metacognitive discipline that separates routine computation from genuine problem solving.
type: skill
category: problem-solving
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/problem-solving/mathematical-problem-solving/SKILL.md
superseded_by: null
---
# Mathematical Problem Solving

Mathematics is the original proving ground for problem-solving theory. Polya's *How to Solve It* introduced the four phases (understand, plan, execute, review) that every subsequent framework builds on. Schoenfeld showed that phases alone are insufficient: without active monitoring ("control"), novices spend 20 minutes on a dead end without noticing. This skill combines the two: Polya's phases as the scaffold, Schoenfeld's control as the supervisor.

**Agent affinity:** polya-ps (overall framing), schoenfeld (control and monitoring), simon (search structure)

**Concept IDs:** prob-problem-representation, prob-goal-decomposition, prob-pattern-recognition, prob-simplification, prob-systematic-listing

## The Four Phases at a Glance

| Phase | Polya question | Schoenfeld control check |
|---|---|---|
| 1. Understand | What is the unknown? What is given? What is the condition? | Do I actually understand this, or am I about to solve the wrong problem? |
| 2. Plan | Do I know a related problem? Can I solve part of it? | Is this plan likely to work, and how much budget do I give it? |
| 3. Execute | Can I check each step? | Is this step still making progress, or have I wandered? |
| 4. Look back | Can I verify the result? Can I use it for another problem? | Does the answer actually answer the original question? |

## Phase 1 — Understand the Problem

**Goal:** Produce a clean problem representation. Most of this is already covered by **problem-comprehension**, but math adds specific operations.

**Math-specific operations:**

- **Identify the unknown.** What is being asked for? Is it a number, a set, a function, a proof?
- **Identify the data.** What is given? Numerical values, geometric conditions, functional relationships.
- **Identify the condition.** What links the data to the unknown?
- **Introduce notation.** Assign variables, name points, label sides.
- **Draw a figure.** Geometry problems often solve themselves once the figure is accurate.
- **Restate in your own symbols.**

**Control check:** "Can I solve this problem without the original statement by looking only at my notation and figure?" If not, return to understanding.

## Phase 2 — Devise a Plan

**Goal:** Choose a method to connect the data to the unknown. Polya's heuristics are central here.

**Polya heuristics:**

- **Have you seen this problem before, perhaps in a slightly different form?**
- **Do you know a related problem?**
- **Look at the unknown. Can you think of a familiar problem with the same unknown?**
- **Can you restate the problem?**
- **Can you solve part of the problem?**
- **If you cannot solve the proposed problem, first try to solve a related one.**
- **Specialize:** solve a simpler or more specific case first.
- **Generalize:** can the problem be viewed as a special case of something larger?
- **Vary the problem:** weaken an assumption, strengthen a conclusion.
- **Introduce auxiliary elements:** a point, a line, an equation that did not appear in the original.

**Control check:** "Does this plan connect the data to the unknown? What is my time budget for this plan? What is my fallback if it fails?"

## Phase 3 — Carry Out the Plan

**Goal:** Execute the plan carefully, checking each step.

**Rules:**

- Work in small, verifiable steps.
- Write enough that a reader (including future you) can follow each step.
- When a step introduces a result, note whether it is exact or approximate.
- When a step is ad hoc, flag it — ad hoc steps are common error sites.

**Schoenfeld's observation:** Novices spend 90% of their time in this phase; experts allocate more to Phase 2 and return to Phase 2 when execution stalls. The boundary between phases is porous.

**Control check (every few steps):** "Is this still on the plan? Am I making progress? Should I reconsider the plan?"

## Phase 4 — Look Back

**Goal:** Verify the answer, extract the lesson, build transfer.

**Operations:**

- **Check the result.** Does the answer satisfy the original conditions? Is it dimensionally consistent? Does it have the right sign or magnitude?
- **Check the argument.** Is every step justified? Any unstated assumptions?
- **Is there a different way?** Alternative solutions often reveal more about the problem.
- **Can the method be used for another problem?** Transfer is the long-term payoff of problem solving.
- **Is the answer the answer to the original question?** Easy to lose track during execution.

**Control check:** "Am I confident in this answer? On what basis?"

## Schoenfeld's Control Layer

Schoenfeld's contribution is that the four phases are not enough. Novices skip Phase 1, short-circuit Phase 2, grind through Phase 3, and neglect Phase 4. The fix is **control**: a supervisor process that interrupts execution at regular intervals to ask whether the current activity is the right activity.

**Control operations:**

1. **Plan monitoring.** Is the current plan still the best available?
2. **Progress monitoring.** Am I moving toward the goal or wandering?
3. **Time budgeting.** How much time have I spent vs. budgeted?
4. **Strategy switching.** When to abandon a plan and try another.
5. **Resource assessment.** What do I know that I haven't used?

Without control, problem solving is a random walk through the strategy space. With control, it is a bounded search.

## Worked Example — A Geometry Problem

*Prove: In any triangle, the sum of the interior angles is 180 degrees.*

**Phase 1 — Understand.** Unknown: a proof. Data: any triangle (three vertices, three sides, three interior angles). Condition: the angles must sum to 180. Draw a figure: triangle ABC with angles alpha, beta, gamma.

**Phase 2 — Plan.** Related problem: parallel lines cut by a transversal produce equal alternate angles. Can we introduce a parallel line through one vertex? Yes — a line through A parallel to BC creates two transversals (AB and AC) producing angles equal to beta and gamma on the other side of A. Then alpha + beta + gamma = straight angle at A = 180.

**Phase 3 — Execute.** Draw line l through A parallel to BC. By alternate interior angles on transversal AB: the angle on the other side of A equal to beta. By alternate interior angles on transversal AC: the angle on the other side equal to gamma. The three angles at A (gamma, alpha, beta) form a straight line, so gamma + alpha + beta = 180.

**Phase 4 — Look back.** Check: does this use any assumption beyond Euclidean geometry? Yes — the parallel postulate. On a sphere, triangles sum to more than 180. The proof is correct for Euclidean geometry only. The auxiliary line (introduce a parallel through A) was the key move; this generalizes to many problems where a single auxiliary element unlocks the solution.

## When Mathematical Problem Solving Fails

- **Racing to Phase 3.** Execution without understanding produces symbol manipulation that does not answer the question.
- **No plan.** Writing equations with no idea where they lead wastes time and produces no insight.
- **No control.** Ten minutes in, the solver has no idea whether they are making progress. Control checks every 2-3 minutes catch this early.
- **Skipping Phase 4.** The answer is written, the problem is "done," but the lesson is not extracted. Without Phase 4, problem-solving skill does not accumulate.

## Cross-References

- **problem-comprehension** provides the base comprehension operations that Phase 1 builds on
- **strategy-selection** is the broader context for Polya's Phase 2 heuristics
- **metacognitive-monitoring** implements Schoenfeld's control layer explicitly
- **design-thinking-ps** replaces proof-style execution with iterative prototyping for ill-defined problems
- **collaborative-problem-solving** distributes phases across team members
