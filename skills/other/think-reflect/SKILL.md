---
name: think-reflect
description: Retrospective learning from a completed experience. Takes a project, incident, decision that played out, or time period; gathers ground truth (observations) separately from recollections; spawns reflectors applying different lenses (what-worked-vs-got-lucky, what-didn't, what-surprised, system-rewards-vs-intent, decisions-that-aged, what-to-tell-past-self, patterns-that-recur) in isolation; synthesizes into updated mental models as first-class output. Produces feedback only — no code, no tickets, no artifacts.
model: opus
---

# Think-Reflect - Retrospective Learning from Completed Experience

Extracts learnings from something that already happened. Unlike every other `/think-*` skill, the input is a *past experience* — a project that shipped, an incident that resolved, a decision that played out, a time period that ended — not a decision to be made. The output is **updated mental models**: changed beliefs about how the world works, surfaced through lens-based reflection.

**This skill produces no tangible artifacts.** It is a consultant, not an implementer. No code, no tickets, no commits. The output is a structured reflection report with updated mental models as the headline contribution.

## Roles

**Judge (you, running this skill):**
- Scope the experience being reflected on
- Gather ground truth, rigorously separating observation from recollection
- Load any external sources the user points to (logs, timelines, meeting notes, git history)
- Choose appropriate reflection lenses
- Spawn reflectors in isolation
- Synthesize into a report with updated mental models prominent

**Reflectors:** Each receives a specific reflection lens (what-worked-vs-got-lucky, what-didn't, what-surprised, system-rewards-vs-intent, decisions-that-aged, what-to-tell-past-self, patterns-that-recur) and extracts learnings through that lens in isolation.

## Workflow

### 1. Scope the Experience

**Establish what is being reflected on, concretely.** Vague scope produces vague reflection.

Probe for:
- **What is the experience?** — a specific project, an incident, a time period, a decision?
- **What's the start point?** — when did it begin?
- **What's the end point?** — is it fully over, or still in flight? (Reflection on partial experiences is allowed but should be acknowledged as partial.)
- **What's in scope / out of scope?** — which aspects to reflect on, which to exclude

**Produce a written brief** of the experience and its boundaries. Reflectors operate on this brief.

### 2. Gather Ground Truth — Separate Observation from Recollection

**This is the most failure-prone step and has enforced structure.** Memory is reconstructive; it drifts toward coherent stories. The git log does not drift. The metric did not rewrite itself.

**Elicit from the user, in three distinct buckets:**

- **Observations** — things recorded during the experience: git history, deployment logs, metrics dashboards, meeting notes, ticket updates, decision documents, Slack threads, timelines. Concrete records.
- **Recollections** — what the user or others *remember*. Flag these explicitly. Memory is valid input but is to be treated as less authoritative than observation when they conflict.
- **Gaps** — things unknown because they weren't recorded and nobody remembers clearly. Gaps constrain what reflection can conclude.

**Actively solicit external sources.** Unlike other `/think-*` skills, `/think-reflect` benefits from loading records the user points to:
- Ask: "Are there any documents, logs, or records of the experience I should read?"
- Accept file paths, links, or pastes
- Load and include as observational context for reflectors

**Push back on smuggled recollections.** If the user says "the launch went well," that's a judgment, not an observation. Ask: what actually happened? what was measured? what did people say at the time? Separate the judgment from the record.

### 3. Choose Reflection Lenses

Select 3-6 lenses from the palette based on what the experience affords.

**Available lenses:**
- **what-worked-vs-got-lucky** — attribution honesty for positive outcomes (process win vs. luck)
- **what-didn't** — blameless identification of failure modes
- **what-surprised** — surprises as signal; surfaces candidate mental-model updates
- **system-rewards-vs-intent** — Goodhart detection; what the system actually rewarded vs. what was intended
- **decisions-that-aged** — calibration; separating decision quality from outcome quality
- **what-to-tell-past-self** — forward-applicable advice; actionable signals the user could have acted on
- **patterns-that-recur** — connections to prior experiences; one-off learning vs. recurring pattern

**Selection heuristics:**
- Team/organizational experience? Include system-rewards-vs-intent.
- Experience involved meaningful decisions? Include decisions-that-aged.
- Experience had unexpected outcomes (good or bad)? Include what-surprised — often the richest lens for mental-model updates.
- Positive outcome? **Always include what-worked-vs-got-lucky** — the failure mode of attributing luck to process is among the most damaging.
- Negative outcome? Include what-didn't.
- User is trying to learn for future similar experiences? Include what-to-tell-past-self.
- The user has mentioned "this has happened before" or similar? Include patterns-that-recur.

**Drop lenses that don't fit.** A solo-contributor reflection has no system rewarding anything. A routine experience may have nothing surprising. Forcing an unfit lens produces noise.

### 4. Spawn Reflectors (Parallel, Isolated)

Spawn one `THK - Reflector` agent per chosen lens, in parallel. Each receives:
- The experience brief (from step 1)
- The observations bucket
- The recollections bucket (flagged as memory, not observation)
- The gaps
- Its assigned lens
- Instruction to prefer observations over recollections when they conflict

**No cross-talk between reflectors.** NGT principle — independent reflection first, synthesis second.

Collect all reflections.

### 5. Synthesize

Combine the isolated reflections into a coherent report. Synthesis differs from other `/think-*` skills because the headline output is *updated mental models*, not standouts or findings.

**5a. Cluster learnings across lenses.** Multiple lenses may surface the same underlying learning from different angles (e.g., a "process win" from what-worked-vs-got-lucky may connect to a "decision that aged well" from decisions-that-aged). Merge and preserve lens attribution.

**5b. Extract updated mental models as first-class output.** Each reflector may have flagged candidate model updates. Collect them, dedupe, and promote them to the top of the report. Format: "We believed X. This experience suggests Y. The updated belief is Z."

**5c. Distinguish process wins from luck.** Whenever the orchestrator sees a positive outcome described, verify the attribution. Luck mistaken for process is dangerous — it reinforces bad processes and sets up future failure. Label ambiguous attributions explicitly.

**5d. Note observation/recollection gaps.** Where reflectors flagged disagreement between observation and recollection, surface it. The gap is itself a learning (memory drifts toward specific narratives).

**5e. Identify recurring patterns.** One-off learnings are datapoints; recurring patterns are beliefs worth defending against.

### 6. Report

**Final report format:**

```
## Reflection Report

**Experience:** [one-line scope]
**Lenses applied:** [list]

### Updated Mental Models

[HEADLINE SECTION. Models that should change based on this experience.
Each update in the form: "We believed X. This experience suggests Y.
The updated belief is Z." These are the calibration updates the user
should take forward — they are the skill's real contribution.]

1. **[Area of belief]**
   - Previously: [the old mental model]
   - Experience suggests: [what this experience indicates]
   - Updated belief: [the new or refined mental model]
   - Confidence in update: [high / moderate — honest about how well-supported this update is by the evidence]

2. [next update...]

### What Happened (Ground Truth)

[Observation-based summary of the experience. Where recollections differ
from observations, note the divergence.]

### What Worked — and Why

[Positive outcomes, with attribution made explicit. Each labeled:]
- **[outcome] — Process win:** [why attributable to what we did]
- **[outcome] — Lucky:** [why NOT attributable to process; the method doesn't generalize]
- **[outcome] — Mixed:** [process contributed but didn't guarantee]

### What Didn't Work

[Blameless failure-mode analysis. What broke and what conditions allowed it.]

### Decisions in Retrospect

[If decisions-that-aged was a lens: quality grid — good/fortunate/unfortunate/bad
for each decision reviewed. Separates decision quality from outcome quality.]

### What Surprised Us

[Unexpected observations, with the contradicted belief and suggested
replacement — often these connect directly to the Updated Mental Models
section above.]

### System Rewards vs. Intent

[If system-rewards-vs-intent was a lens: Goodhart gaps found. What was
intended vs. what was actually rewarded.]

### Advice to Past-Self

[Forward-applicable advice derived from the experience — actionable
signals that would have been usable at the time they would have been
received.]

### Recurring Patterns

[Connections to prior experiences, if any. One-off vs. repeating.]

### Gaps in the Record

[Things that were not captured and that future retrospectives would
benefit from having. Often generates a small "capture more data next
time" list.]

### Suggested Next Steps

- To act on the updated mental models: these are the user's to internalize; no further skill invocation needed
- To design interventions based on failure modes: `/think-brainstorm`
- To diagnose a specific recurring failure mode: `/think-diagnose`
```

### 7. No Iteration

This skill is one-shot. If the user wants to reflect on a different experience, they re-invoke with that new experience. If they want to go deeper on a specific finding, they use the appropriate downstream skill (`/think-diagnose`, `/think-brainstorm`, `/think-scrutinize`).

## Constraints

- **No artifacts.** No code, tickets, commits, or documents.
- **Observation/recollection split.** Non-negotiable in the ground-truth-gathering phase.
- **Isolated reflection.** Reflectors do not see each other's output during generation.
- **Updated mental models are the headline.** A reflection that produces a tidy findings list but no model updates has failed its purpose.
- **Honest attribution.** Process wins and luck are distinct — conflating them is dangerous.

## When to Use

**Good fit:**
- After a project ships and you want to extract learnings
- After an incident resolves and you want to update mental models
- At the end of a quarter/half-year/year for structured reflection
- After a decision has played out and you want to calibrate judgment
- When a pattern keeps recurring and you want to understand it

**Poor fit:**
- During an in-flight experience — reflection works best on bounded, completed experiences
- Decision support for a decision being made now — use `/think-deliberate`
- Diagnosing a current phenomenon — use `/think-diagnose`
- Finding bugs or issues — use `/bug-fix` or `/bug-hunt`
- Generating next-step plans — use `/think-brainstorm` (reflection informs brainstorming but is a distinct step)

**Rule of thumb:** If you're asking "what did I learn?" — `/think-reflect`. If you're asking "what should I do?" — a different skill.

## Relationship to Other Skills

`/think-reflect` is structurally different from the other `/think-*` skills: its input is a past experience, not a decision. The fact-finding phase is substantial because the observation/recollection distinction matters. The output foregrounds mental-model updates rather than options, critiques, or reframings.

**Natural follow-ups:**
- Updated mental models that imply action → `/think-brainstorm` to generate interventions
- A recurring failure mode surfaced by reflection → `/think-diagnose` to understand its cause
- An intervention being considered based on learnings → `/think-scrutinize` to stress-test

**Reflection fits at any cadence.** After major projects, after incidents, quarterly, annually, or opportunistically when a significant experience ends. The discipline — not the frequency — is what matters.

## Philosophy

Retrospectives are universally skipped or done as ritual theater. A tidy document gets produced; nobody's beliefs update; the next project runs the same way. This is the failure mode `/think-reflect` exists to avoid.

**The value of reflection is *updated mental models*, not a findings document.** A model update is useful even when it's small: "I used to think our test suite was reliable; this experience suggests it's reliable for CRUD changes but not integration changes" is a real calibration that changes future behavior. A findings report that updates no beliefs has taught nothing.

**The enforced observation-vs-recollection split is the other discipline.** Memory reconstructs coherent narratives; observations don't. When they disagree, prefer the observation — and *note the disagreement*. The gap between what happened and what we remember is itself a learning about how we perceive our own experience.

**Luck and process must stay separate.** A good outcome from a bad process reinforces the bad process. A bad outcome from a good process looks like process failure. Attributing honestly — even when uncomfortable — is the foundation of all the other learnings.
