---
name: skill-coverage-gate
description: >
  Use when reviewing, shipping, or regression-testing a SKILL.md and you hold
  one or more captured trajectories where that skill was actually loaded.
  Translates the skill's instructions into behavior constraints, then reports
  which were EXERCISED (coverage) versus untested, and flags any that were
  in-scope but VIOLATED (compliance) — a cheap single-trajectory test-adequacy
  gate. It surfaces untested instructions rather than auto-blocking, and
  escalates fail-closed only when a violation touches shared repo state,
  never-surface memory, or self-modification. Complements
  skill-counterfactual-audit (which measures EFFECT) and skill-causal-curation
  (which measures contribution); this one asks ADEQUACY. Backed by the
  agent-skill-coverage metric (arxiv 2606.20659v2). Triggers on skill review,
  ship gating, and regression-testing a skill against its trajectories.
description-frequency: on-demand
user-invocable: true
version: 1.0.0
format: 2025-10-02
triggers:
  - "check this skill's instruction coverage against a trajectory"
  - "which of this skill's rules were exercised or violated"
  - "test-adequacy gate before shipping a skill"
updated: 2026-07-18
status: ACTIVE
source: arxiv 2606.20659v2 (Agent Skill Coverage Metric)
---

# Skill Coverage Gate

Given a `SKILL.md` and one or more captured trajectories in which it was loaded,
translate its instructions into discrete behavior constraints, then report — per
constraint — whether the trajectory **exercised** it (coverage), left it
**untested**, or **violated** it while in scope (compliance). This is a cheap,
single-trajectory adequacy check that slots into the `skill-forge` ship/review
loop before more expensive paired or masked evaluation is worth running.

## Why

`skill-forge` validate + critique check a skill's *frontmatter and prose*; they
never observe whether the skill's rules actually got tested by the run that
loaded it. A skill can pass authoring review, ship, and then have half its
instructions never fire in any real trajectory — untested behavior masquerading
as verified behavior. Worse, an instruction can fire and be *disobeyed* without
anyone noticing, because the task still passed. This gate makes both gaps
legible: what was tested, and where the agent already broke a rule it loaded.

## Data classes touched

Inputs are **project-internal**: the skill file plus trajectories captured by
`session-retro` / `session-observatory-live` under `.planning/patterns/`. Those
traces can quote real work that includes strongly-marked **never-surface**
records — private origins, Fox Companies IP, credentials, Center Camp trust
rules. Boundary rule: the coverage report cites constraint evidence by trace
location and event index, never by pasting trace content that may carry such a
record. The report is project-internal and is written under `.planning/`; it is
never merged into published docs or any shared output.

## How

1. **Verify the input is valid.** Confirm the skill was in the loaded skill set
   for each supplied trajectory (check the session-retro loaded-skills field).
   A trajectory where the skill was not loaded gives coverage undefined —
   discard it, do not count it as zero coverage. Require ≥1 valid trajectory.
2. **Extract constraints.** Read the skill body and decompose it into atomic
   behavior constraints, each as `{id, precondition, required-behavior,
   scope-tags}`. `scope-tags` mark whether the constraint governs shared repo
   state (git worktrees, refinery-merge queue, commits), sensitive memory
   (Grove / MEMORY.md never-surface records), or self-modification
   (`.claude/skills`, `.claude/agents`, `.claude/hooks`). This decomposition is
   an LLM judgment — see the failure model.
3. **Label each constraint against the trajectory set.**
   - **untested** — no trajectory ever hit the precondition. An adequacy gap.
   - **exercised** — precondition fired and the required behavior was observed
     followed. Counts toward coverage.
   - **violated** — precondition fired and observed behavior contradicts the
     required behavior. A compliance failure.
4. **Compute two numbers.** Coverage = exercised / (exercised + violated +
   in-scope-but-ambiguous), over constraints whose precondition fired at least
   once. Compliance = 1 − violated / (exercised + violated).
5. **Decide the report verdict.**
   - Coverage < 0.60 of extracted constraints → flag `under-exercised`:
     recommend more probe trajectories or hand off to
     `skill-counterfactual-audit`. Non-blocking — this surfaces the gap.
   - Any `violated` constraint whose `scope-tags` include shared repo state,
     never-surface memory, or self-modification → **fail-closed**: block the
     `skill-forge` ship, do NOT silently proceed, and escalate to the operator
     via `mayor-coordinator`.
   - A `violated` constraint on benign scope → report as a compliance gap,
     non-blocking, and recommend a skill edit or a narrower trigger.
6. **Emit report** to `.planning/patterns/skill-coverage/<skill>-<timestamp>.md`:
   the constraint table (id, label, evidence-location), the two numbers, and the
   verdict.

### Robustness rule

Judge a constraint exercised or violated by the **effect** of what the agent
did, not by whether the trace text echoes the skill's wording. An agent that
paraphrases a rule and follows it is compliant; one that quotes the rule and
then acts against it is a violation. Do not mark coverage from surface vocabulary
match.

## Confidence / failure model

Constraint extraction and the exercised/violated labeling are **LLM judgments**
(semi-decidable, not a deterministic pass/fail check). Coverage from a single
trajectory is a lower bound on adequacy, not proof of correctness: high coverage
means the tested rules fired, not that the skill is good — that is
`skill-counterfactual-audit`'s and `skill-causal-curation`'s question. The gate
reduces the chance an untested or already-violated rule ships; it does not
eliminate it. On any uncertainty about whether a scope-tagged constraint was
violated, default fail-closed (escalate), never silently pass.

## When to skip

- No valid trajectory exists where the skill was loaded — capture a run first;
  there is nothing to measure adequacy against.
- The skill is a pure metadata/frontmatter change — route to
  `skill-frontmatter-doctor`, which needs no trajectory.
- A structural gate (`skill-forge` validate/critique) already failed the skill —
  fix that first; coverage over a broken skill is noise.

## Distinctness

- **skill-counterfactual-audit** runs a paired with/without probe and measures
  the skill's behavioural EFFECT (the SIP report). **skill-causal-curation**
  uses randomized masking to measure per-task-type CONTRIBUTION for keep/repair/
  retire. This skill asks neither — it asks single-trajectory ADEQUACY: were the
  skill's own rules exercised, and were any broken. It reports gaps; it does not
  auto-retire or auto-block on effect.

## Integration

- `skill-forge` — this gate runs inside its ship/review loop, after validate +
  critique, before publish; a fail-closed verdict halts the ship.
- `session-retro` / `session-observatory-live` — the trajectory source under
  `.planning/patterns/`.
- `skill-counterfactual-audit` + `skill-causal-curation` — sibling eval skills
  answering the EFFECT and CONTRIBUTION questions; escalate an `under-exercised`
  skill to them when a single trajectory is not enough evidence.
