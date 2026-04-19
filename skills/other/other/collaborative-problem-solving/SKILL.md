---
name: collaborative-problem-solving
description: Group problem solving with explicit structure. Covers shared mental models, role allocation, cognitive division of labor, building on ideas (yes-and), productive disagreement, and the moves that prevent social loafing and groupthink. Use for problems that exceed individual capacity or benefit from multiple expertise areas.
type: skill
category: problem-solving
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/problem-solving/collaborative-problem-solving/SKILL.md
superseded_by: null
---
# Collaborative Problem Solving

Groups can outperform individuals when the problem is decomposable, when members have complementary expertise, and when the group has structure. Groups can also underperform individuals when structure is missing: social loafing, groupthink, dominant voices, and coordination costs swallow the gains. This skill is the catalog of moves that produce group gains rather than group losses.

**Agent affinity:** jonassen (ill-structured group problems), brown-ps (reciprocal teaching, community of inquiry), bransford (anchored instruction)

**Concept IDs:** prob-group-problem-process, prob-cognitive-division, prob-idea-building, prob-conflict-in-groups

## Why Groups Can Win

Groups add value through four mechanisms:

1. **Cognitive diversity.** Different members notice different things.
2. **Division of labor.** Sub-problems can be tackled in parallel.
3. **Error checking.** Others catch mistakes you would not.
4. **Idea building.** One member's idea triggers another's, producing solutions no individual would have reached alone.

## Why Groups Often Lose

Groups lose value through four failure modes:

1. **Social loafing.** Individuals put in less effort because they assume others will.
2. **Groupthink.** The desire for harmony suppresses dissent; the group converges on a bad idea everyone quietly doubts.
3. **Dominant voices.** One or two members monopolize airtime; others stop contributing.
4. **Coordination cost.** Time spent managing the group exceeds time spent solving the problem.

Structure is what distinguishes winners from losers.

## The Collaborative Toolbox at a Glance

| # | Move | Purpose | When to use |
|---|---|---|---|
| 1 | Establish shared mental model | Everyone agrees what the problem is | Start of session |
| 2 | Allocate roles | Distribute cognitive load | After shared understanding |
| 3 | Divide sub-problems | Parallelize independent work | Decomposable problems |
| 4 | Yes-and idea building | Build on, do not kill, contributions | Ideation |
| 5 | Explicit devil's advocate | Guard against groupthink | Convergence phase |
| 6 | Round-robin | Give quiet members airtime | Any time dominance emerges |
| 7 | Silent brainstorming | Decouple generation from social pressure | Ideation |
| 8 | Decision protocol | Make decisions fairly | Convergence |
| 9 | Conflict protocol | Productive disagreement | When members disagree |
| 10 | Post-mortem | Extract lessons | After solution |

## Move 1 — Establish Shared Mental Model

**Pattern:** Before any solving begins, every member states their understanding of the problem in their own words. Differences are reconciled.

**Why it matters:** A group that disagrees about the problem produces parallel solutions to different problems, which cannot be combined. Catching this at the start saves enormous downstream rework.

## Move 2 — Allocate Roles

**Pattern:** Assign each member a role that plays to their strength. Common roles:

- **Facilitator:** manages process, not content. Calls on quiet members, times phases, keeps the group on track.
- **Scribe:** captures ideas and decisions in writing, visible to all.
- **Devil's advocate:** specifically tasked with challenging the emerging consensus.
- **Timekeeper:** tracks phase budgets.
- **Domain specialists:** members with relevant expertise, assigned the parts that match.

Rotate roles across sessions to avoid permanent hierarchies.

## Move 3 — Divide Sub-Problems

**Pattern:** After decomposition, assign each sub-problem to one or two members. Define the interfaces (inputs and outputs) so that independent work can be combined without rework.

**Rule of thumb:** If the sub-problem needs more than two people's attention, it was decomposed at the wrong level.

## Move 4 — Yes-And Idea Building

**Pattern:** When a teammate offers an idea, respond with "Yes, and..." rather than "No, but..." Even if the idea is flawed, find the grain of value and extend it.

**Why it matters:** Groups where ideas are killed quickly produce fewer total ideas. Building on a flawed idea often produces a good one that would not have existed otherwise.

**Exception:** During explicit evaluation phases, critical feedback is appropriate. Yes-and is for generation, not evaluation.

## Move 5 — Explicit Devil's Advocate

**Pattern:** Assign one member the role of challenging the emerging consensus. This person is required to find the strongest objection, not because they hold it personally, but because the role demands it.

**Why it matters:** Groupthink is the default. Explicit dissent has to be structured in, or it will not happen.

## Move 6 — Round-Robin

**Pattern:** The facilitator calls on each member in turn, ensuring everyone contributes. Silent members contribute; dominant members wait their turn.

**When to use:** Any time two members have been talking for more than 50% of the session.

## Move 7 — Silent Brainstorming

**Pattern:** Each member writes ideas on sticky notes (or the digital equivalent) for a fixed time, with no talking. Notes are then posted and clustered together.

**Why it matters:** Decouples generation from social pressure. Members who would not speak up produce ideas in writing. The group then builds on the written ideas as a unit.

## Move 8 — Decision Protocol

**Pattern:** Make the decision-making rule explicit before the decision is needed.

**Options:**

- **Consensus:** Everyone must agree. Slow, but buy-in is high.
- **Majority vote:** Faster but can leave dissenters unrepresented.
- **Leader decides after input:** Fastest but depends on a trusted leader.
- **Multi-voting:** Each member has N votes to distribute across options. Good for idea ranking.

Pick one and announce it. Silent rule disagreements poison execution.

## Move 9 — Conflict Protocol

**Pattern:** Disagreements are productive when they are about the problem, not the people. Protocol:

1. Both sides state their positions explicitly.
2. Each side restates the other's position accurately (Rogerian).
3. The group identifies the specific point of disagreement — usually narrower than the original dispute.
4. The group resolves by evidence, by testing, by escalation, or by agreeing to disagree and proceeding with the tradeoff documented.

## Move 10 — Post-Mortem

**Pattern:** After the session, extract lessons. What worked? What did not? What would you do differently?

**Rules:**

- Blameless (focus on process, not people)
- Concrete (specific moves, not vague generalities)
- Actionable (what will we do next time?)
- Documented (the lessons are written down where the next group can find them)

## Worked Example — A Design Review Session

A four-person team reviews a proposed system design.

**Move 1 (Shared mental model):** Each member states their understanding of the problem the system is meant to solve. One member's understanding is different; the group reconciles.

**Move 2 (Roles):** Facilitator assigned to keep the review on track. Scribe captures feedback. Devil's advocate tasked with finding the worst-case failure mode.

**Move 7 (Silent brainstorming):** Each member spends 5 minutes listing concerns on sticky notes. 23 concerns collected in silence.

**Move 4 (Yes-and):** Concerns are clustered. For each, the group builds on it rather than dismissing: "Yes, the authentication is weak, and we could add..."

**Move 5 (Devil's advocate):** The advocate presents the worst-case scenario: the system is breached on day one. What is the worst thing that happens? The discussion surfaces two previously-invisible risks.

**Move 8 (Decision protocol):** Multi-voting on which concerns are must-fix vs nice-to-have. Top 5 become blockers.

**Move 10 (Post-mortem):** After the session, the team notes that silent brainstorming surfaced concerns that would never have come up in open discussion. Adopt the move permanently.

## When Collaborative Problem Solving Fails

- **No shared mental model.** Members solve different problems in parallel.
- **No role allocation.** Some members do all the work, others none.
- **Dominant voices.** One or two members suppress the group's diversity.
- **Premature convergence.** The group agrees too fast, missing better options.
- **Unresolved conflict.** Surface agreement hides underlying disagreement, which reappears during execution.
- **No post-mortem.** The group makes the same mistakes next time.

## Cross-References

- **problem-comprehension** is done in parallel by each member, then reconciled
- **strategy-selection** applies to the group's shared problem, not individual sub-problems
- **design-thinking-ps** uses group brainstorming and critique as core activities
- **metacognitive-monitoring** is harder in groups — the facilitator is often the monitor
- **mathematical-problem-solving** can be distributed via dividing phases across members
