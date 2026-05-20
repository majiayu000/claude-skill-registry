---
name: think-diagnose
description: Abductive reasoning about causes. Takes a phenomenon, separates observations from interpretations, then spawns diagnosticians applying different reasoning lenses (technical, human-factors, process, incentive-structure, environmental, temporal, measurement-artifact, statistical) in isolation. Orchestrator evaluates candidate causes for fit-against-evidence, calibrates confidence honestly, and reports leading candidate(s) with distinguishing evidence needed. Produces feedback only — no code, no tickets, no artifacts.
model: opus
---

# Think-Diagnose - Abductive Reasoning About Causes

Takes a phenomenon — something that was observed and that the user wants to understand — and produces a ranked set of candidate causes with evidence-based confidence calibration. Uses **abductive reasoning**: inference to the best explanation. Distinct from `/bug-fix` (which handles code-specific diagnosis with artifact output and execution tooling); `/think-diagnose` is pure reasoning about causes, applicable to non-code phenomena as readily as code ones.

**This skill produces no tangible artifacts.** It is a consultant, not an implementer. No code, no tickets, no commits. The output is a structured diagnosis report that the user can act on by gathering more evidence, adopting a leading cause, or piping to `/think-brainstorm` for remediation.

## Roles

**Judge (you, running this skill):**
- Capture the phenomenon in a written brief
- Elicit evidence, rigorously separating observation from interpretation
- Choose appropriate reasoning lenses
- Spawn diagnosticians in isolation
- **Evaluate** candidate causes against evidence (this skill has a real evaluative phase, unlike purely-divergent think-* skills)
- Calibrate confidence honestly and report

**Diagnosticians:** Each receives a specific reasoning lens and generates candidate causes (with mechanisms, predictions, refuters, and plausibility) in isolation from other diagnosticians.

## Workflow

### 1. Receive the Phenomenon

The phenomenon may arrive as:
- **Conversation context** — summarize it back, confirm
- **A document** — read the file (incident report, data summary, observation log)
- **Fresh user input** — capture verbatim

**Produce a written brief** of the phenomenon. Precisely what is the thing to explain? Vague phenomena produce vague diagnoses.

### 2. Gather Evidence — Separate Observation from Interpretation

**This is the most failure-prone step in the entire workflow, and it has enforced structure.** Most bad diagnoses start by accepting interpretations as observations.

**Elicit from the user, in three distinct buckets:**

- **Observations** — concrete things that were measured, seen, or experienced. "The metric dropped 30% on March 14th." "Three customers mentioned X in surveys." "The build broke at commit abc123."
- **Interpretations already held** — what the user or others have already *inferred* from the observations. "The team thinks it's because of the migration." "We believe the drop is due to seasonality." Flag these explicitly so diagnosticians know not to accept them as given.
- **Unavailable / unknown evidence** — what's unknown, wasn't measured, or can't be retrieved. "We don't have per-user data before April." "We didn't log the old config."

**Push back on smuggled interpretations.** If the user says "the metric dropped because of the migration," that's two claims: (a) the metric dropped (observation) and (b) the migration caused it (interpretation). Separate them before proceeding.

**3-6 clarifying questions is typical** to establish this split. Stop when you have enough to pass diagnosticians material they can work with.

### 3. Choose Reasoning Lenses

Select 3-6 lenses from the palette based on the phenomenon's shape.

**Available lenses:**
- **technical** — engineering-level causes (code, infra, config, capacity, dependencies)
- **human-factors** — people, skills, fatigue, turnover, miscommunication, team dynamics
- **process** — broken or missing process, handoffs, approvals, ownership, rituals
- **incentive-structure** — the system rewards the behavior we're diagnosing (Goodhart territory)
- **environmental** — external factors (market, regulation, customer mix, vendor, upstream)
- **temporal** — something changed in time that correlates with the phenomenon
- **measurement-artifact** — the phenomenon isn't real, it's a metric/instrumentation issue
- **statistical** — base rates, regression to mean, Simpson's paradox, confounders, selection

**Selection heuristics:**
- Phenomenon is metric-based? **Always include measurement-artifact.** Underrated; catches a large share of false phenomena.
- Phenomenon has a clear onset date? Include temporal.
- Phenomenon involves aggregate data (averages, ratios)? Include statistical.
- Phenomenon is in a team/org context? Include human-factors, process, incentive-structure.
- Phenomenon is in a codebase or system? Include technical.
- Phenomenon occurs in a context with external inputs (customers, markets, vendors)? Include environmental.

**Drop lenses that don't fit.** A phenomenon in a closed system without external dependencies probably doesn't need environmental. A phenomenon observed directly (not through metrics) probably doesn't need measurement-artifact.

### 4. Spawn Diagnosticians (Parallel, Isolated)

Spawn one `THK - Diagnostician` agent per chosen lens, in parallel. Each receives:
- The phenomenon brief
- The observations
- The interpretations already held (flagged — not to be accepted as given)
- The unavailable evidence
- Its assigned lens
- Instruction to generate 3-8 candidate causes, each with mechanism / predictions / refuters / plausibility

**No cross-talk between diagnosticians.** NGT principle — independent reasoning first, evaluation second. Isolated diagnosticians produce more distinct candidate causes; coordinated ones anchor on the first compelling story.

Collect all candidate causes.

### 5. Evaluate Fit — Orchestrator's Work

**This phase is new territory for `/think-*` skills.** The prior skills (brainstorm, reframe, scrutinize, deliberate) are purely divergent or choose among pre-stated options; this skill requires the orchestrator to do evaluation against evidence.

**For each candidate cause from step 4, evaluate:**

- **Explanatory fit** — does this cause explain the observed phenomenon? Does it explain *all* the observations, or only some?
- **Prediction check** — the diagnostician stated what we'd expect to see if this cause were true. Do we observe those things? (Some predictions may require the user to check; note them.)
- **Refuter check** — the diagnostician stated what would disprove this cause. Do we observe any of those refuters?
- **Parsimony** — is there a simpler cause that fits equally well? Prefer the simpler one if fit is comparable.
- **Domain plausibility** — given what's known about the domain, how plausible is this cause? This uses general reasoning, not just evidence fit.

**Cluster causes across lenses.** Some causes from different lenses are the same underlying mechanism viewed from different angles (e.g., "engineers ship half-finished features" seen through human-factors and incentive-structure may converge on the same root cause). Merge and preserve lens attribution.

**Resist compelling-narrative bias.** Causes with clean stories are dangerous; they feel explanatory even when they don't fit the evidence. Weight evidence fit over story quality. When in doubt, flag "compelling story, weak fit" explicitly.

### 6. Calibrate Confidence

**No fabricated percentages.** Use qualitative categories with clear meaning:

- **Strong fit** — cause explains all observations, predictions confirmed (or testable), no refuters observed, plausible. This is a leading candidate.
- **Moderate fit** — cause explains most observations, some predictions unconfirmed but not contradicted, plausible. Secondary candidate.
- **Weak fit** — cause explains some observations, significant predictions unconfirmed, possibly plausible. Long-shot candidate.
- **Unable to distinguish** — two or more causes fit the evidence equally well. Cannot converge without more evidence.

**Honest uncertainty is valuable.** "Cause A looks most likely but evidence is sparse; disambiguating observation X would shift the picture" is a better output than fake precision.

### 7. Report

**Final report format:**

```
## Diagnosis Report

**Phenomenon:** [one-line summary]
**Lenses applied:** [list]

### Observations

[Concrete ground-truth observations, as elicited in step 2]

### Interpretations Held Aside

[Interpretations the user or others held, flagged as not-accepted-as-given
for the diagnosis. If any turned out to be correct, that's reported in
the leading candidate section; if not, they remain held aside.]

### Unavailable Evidence

[What's unknown or wasn't measured — constrains what can be concluded]

### Leading Candidate(s)

[1-2 causes with strong fit. For each:]

#### [cause name] — strong fit

**Mechanism:** [how this cause produces the observations]

**Evidence fit:**
- Observations explained: [which]
- Predictions confirmed: [which; or "would need to check X"]
- Refuters: [none observed / note any partial refuters]

**Plausibility:** [brief domain-knowledge assessment]

**Lens(es):** [which diagnostician(s) surfaced this]

### Other Candidates

[Moderate-fit and weak-fit causes, briefly. Include lens attribution.]

### Distinguishing Evidence

[Concrete observations the user could gather to distinguish between the
leading candidates. This is the most actionable part of the report —
not "more data" in the abstract, but specific tests.]

For example:
- To distinguish cause A from cause B: check whether [specific observable].
  If [X], cause A. If [Y], cause B.

### What Remains Unknown

[Questions the diagnosis raised but cannot answer with current evidence.
May include "original interpretation X still possible but no stronger
support than alternatives."]

### Recommendation

One of:
- **Act on leading candidate** — evidence fit is strong; proceed with remediation of [cause]
- **Gather distinguishing evidence first** — leading candidates tie; collect [specific observations] to converge
- **The phenomenon may not be real** — measurement-artifact lens produced a strong candidate; verify the observation before diagnosing further
- **Insufficient evidence for confident diagnosis** — current observations don't distinguish among plausible causes; decision needed on whether to gather more data or accept uncertainty

### Suggested Next Steps

- To remediate the leading cause: `/think-brainstorm` for interventions (or `/bug-fix` if the cause is in code)
- To gather distinguishing evidence: [specific checks listed above]
- To pressure-test the leading cause before acting: `/think-scrutinize`
```

### 8. No Iteration

This skill is one-shot. If the user gathers distinguishing evidence and wants an updated diagnosis, they re-invoke with the new evidence in hand. Each invocation is a clean diagnostic consultation.

## Constraints

- **No artifacts.** No code, tickets, commits, or documents.
- **Separate observation from interpretation.** Non-negotiable in the evidence-gathering phase.
- **Isolated generation.** Diagnosticians do not see each other's output during generation.
- **Honest uncertainty.** No fabricated confidence numbers. Qualitative categories only.
- **Evidence fit > story quality.** Compelling narratives are suspect; evidence fit wins.
- **Honest "can't distinguish"** is a valid, valuable outcome.

## When to Use

**Good fit:**
- Unexplained metric changes — "why did engagement drop 15% starting March 1?"
- Recurring problems with unclear cause — "why does this project keep slipping?"
- Behavioral patterns — "why do customer calls go badly when we raise prices?"
- Organizational issues — "why does our goal-setting process keep producing missed goals?"
- Anywhere `/bug-fix` doesn't apply because the phenomenon isn't code-specific

**Poor fit:**
- Known causes needing intervention design — use `/think-brainstorm`
- Code-specific diagnosis — use `/bug-fix` (artifact output, execution tooling)
- Choosing between options — use `/think-deliberate`
- Stress-testing a plan — use `/think-scrutinize`
- Phenomena so vaguely described that no observations exist (refine the phenomenon first)

**Rule of thumb:**
- "Why is this happening?" → `/think-diagnose`
- "Code is broken, find and fix it" → `/bug-fix`
- "What could I do about this?" → `/think-brainstorm`

## Relationship to Other Skills

`/think-diagnose` is a **hybrid generative + evaluative** skill, unlike the purely divergent `/think-brainstorm` and `/think-reframe` or the selective `/think-deliberate` and `/think-scrutinize`. The orchestrator generates candidate causes (divergent) then evaluates them against evidence (evaluative).

**Natural downstreams:**
- If cause is identified → `/think-brainstorm` for remediation interventions
- If cause is in code → `/bug-fix` for targeted investigation and fix
- If cause is uncertain between candidates → gather distinguishing evidence, then re-invoke `/think-diagnose`
- Before acting on the leading cause → `/think-scrutinize` to stress-test the intervention plan

**Natural pipeline (for non-code phenomena):**

```
/think-diagnose → /think-brainstorm → /think-deliberate → /think-scrutinize
    why?            what to do?         which approach?      what's wrong?
```

## Philosophy

Diagnosis is hard because compelling narratives beat correct ones. Humans prefer causes that tell a good story — they feel explanatory. Good abductive reasoning resists this: the most likely cause is the one that *best fits the evidence*, not the one that makes the cleanest story.

The enforced observation-vs-interpretation split is the skill's most important contribution. Most bad diagnoses start by accepting an interpretation as if it were an observation — "the drop happened because of the migration" sneaks the causal claim into the description of what happened. Once that interpretation is in the evidence bucket, no diagnostician will challenge it, and the diagnosis inherits the error.

Honest uncertainty is the other key discipline. "I don't know for sure" is often the correct output when evidence is thin — and it's far more useful than a confident-sounding but brittle conclusion. Users can act on acknowledged uncertainty (by gathering more evidence); they can't protect themselves from false confidence.
