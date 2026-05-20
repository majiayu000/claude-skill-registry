---
name: think-reframe
description: Problem redefinition before problem solving. Takes a stated problem, extracts its premises, then spawns reframers applying different lenses (problem-vs-symptom, scope-shift, stakeholder-shift, level-of-abstraction, time-horizon, inversion, category-shift, constraints-shift) in isolation, and synthesizes the alternatives into a report with an orchestrator recommendation. Produces feedback only — no code, no tickets, no artifacts.
model: opus
---

# Think-Reframe - Problem Redefinition Before Problem Solving

Takes a stated problem and explores alternative framings of it through parallel reframers, each applying a different reframing lens in isolation. The output is a set of candidate reframings with an explicit recommendation: keep the original framing, adopt a specific reframing, or explore further. Sits upstream of `/think-brainstorm` in the natural reasoning pipeline — most wasted engineering effort goes into solving well-defined versions of the wrong problem, and this skill is the dedicated defense against that failure mode.

**This skill produces no tangible artifacts.** It is a consultant, not an implementer. No code, no tickets, no commits. The output is a structured reframing report that the user can act on by refining their problem statement or proceeding with the original.

## Roles

**Judge (you, running this skill):**
- Capture the stated problem in a written brief
- Extract stated and unstated premises (lightweight reconnaissance, not confrontation)
- Choose appropriate reframing lenses
- Spawn reframers and synthesize the alternatives into a report with a recommendation

**Reframers:** Each receives a specific lens (problem-vs-symptom, scope-shift, stakeholder-shift, level-of-abstraction, time-horizon, inversion, category-shift, constraints-shift) and produces a reframed problem statement in isolation.

## Workflow

### 1. Receive the Problem

The problem may arrive as:
- **Conversation context** — summarize it back, confirm
- **A document** — read the file (design doc, ticket, problem statement)
- **Fresh user input** — capture it verbatim

**Produce a written brief** of the stated problem as you understand it. Reframers operate on this brief. Ambiguity here corrupts everything downstream — if the problem is so vague that reframing lenses can't bite, refine the problem statement with the user before proceeding.

### 2. Extract Premises

**Lighter than `/think-brainstorm`'s assumption-validation phase.** This is reconnaissance — you're mapping what the problem *presumes* so reframers have the context to challenge those presumptions through their lenses. You are not validating these premises with the user (that's a heavier exercise, and the reframers themselves will challenge them).

**Identify:**
- **Stated premises** — what the problem statement explicitly asserts
- **Unstated premises** — what the problem statement assumes without saying
- **Implied scope** — what the problem is about, what it's not about
- **Implied category** — is this framed as technical / people / process / etc.?
- **Implied stakeholders** — whose problem is this?
- **Implied time horizon** — immediate, medium, long-term?

This snapshot is passed to reframers as context. The reframers' job is to challenge and shift these.

### 3. Choose Reframing Lenses

Select 3-6 lenses from the palette based on the problem's shape. The orchestrator decides autonomously.

**Available lenses:**
- **problem-vs-symptom** — is the stated problem a symptom of something upstream?
- **scope-shift** — narrower or wider framing
- **stakeholder-shift** — different stakeholders' perspectives
- **level-of-abstraction** — more general or more specific
- **time-horizon** — 1 week, 6 months, 5 years
- **inversion** — what new problems would emerge if this were solved?
- **category-shift** — is this really a technical / people / process / spec / business / incentive / communication problem?
- **constraints-shift** — which "fixed" constraints are actually negotiable?

**Selection heuristics:**
- Problem described as "we need X" → include stakeholder-shift (is X what different parties need?), category-shift (is "we need X" a technical problem, or a prioritization problem?)
- Problem described as urgent → include time-horizon (different horizons yield different interventions)
- Problem described with a hard constraint → include constraints-shift
- Problem described with a clean story → include problem-vs-symptom (clean stories often hide upstream causes)
- Problem that feels stuck → include inversion and level-of-abstraction (both break out of the current framing)

**Drop lenses that don't fit.** Not every lens applies to every problem. A clearly-factored technical problem may not need category-shift; a personal productivity problem may not need stakeholder-shift. Better 3 fitted lenses than 7 forced ones.

### 4. Spawn Reframers (Parallel, Isolated)

Spawn one `THK - Reframer` agent per chosen lens, in parallel. Each receives:
- The written problem brief (from step 1)
- Its assigned lens
- The premise snapshot (from step 2)
- Instruction to produce a reframed problem statement with an explicit "what changed" diff and "when this framing applies" note

**No cross-talk between reframers.** NGT principle — independent reframing first, synthesis second. Isolated reframers produce more distinct alternatives; coordinated ones anchor on each other.

Collect all reframings.

### 5. Synthesize

Combine the isolated reframings into a coherent report:

**5a. Assess meaning-shift per reframing.** For each reframing, judge how much it materially shifts the problem's meaning. A reframing that just restates the problem in different words is not productive. A reframing that would lead to a different intervention is productive. Classify each as:
- **Materially shifts meaning** — adopting this reframe would lead to a meaningfully different solution
- **Refines the framing** — sharpens the original without replacing it
- **No meaningful shift** — the original framing holds up through this lens (this is still valuable calibration)

**5b. Look for composite framings.** Sometimes two lenses compound — e.g., "stakeholder-shift to operator + time-horizon 5 years" = "what does this look like to the operator who has to maintain this for 5 years?" These composite framings can be sharper than either parent. Only include if the composition is genuinely illuminating — don't manufacture them.

**5c. Identify standout reframings.** The 1-3 reframings that most change what solving the problem would mean. These are the recommendations to seriously consider.

**5d. Form an orchestrator recommendation.** One of:
- **Keep original framing** — reframings refined the framing but didn't materially shift it; the original is sound
- **Adopt reframing X** — one reframing materially shifts the problem in a way the user should consider adopting
- **Further explore** — multiple reframings materially shift the problem; the user should pick among them rather than receive a single recommendation from this skill

### 6. Report

**Final report format:**

```
## Reframing Report

**Stated problem:** [one-line summary of original framing]
**Lenses applied:** [list]

### Original Framing

[Restate the problem as originally stated, with the premise snapshot
making implicit assumptions visible. This is the baseline each reframing
is measured against.]

### Standout Reframings

[1-3 reframings that materially shift the problem's meaning. For each:]

#### [lens name]

**Reframed:** [concrete alternative problem statement]

**What changed:** [explicit diff from the original framing]

**When this framing applies:** [conditions under which this reframing
is most useful]

### Composite Framings

[Optional. Reframings the orchestrator constructed by combining lenses.
Only include if the composition is genuinely illuminating.]

### Refinements (Not Materially Shifting)

[Reframings that sharpened the framing without replacing it. Listed
briefly for completeness.]

### Where the Original Framing Held Up

[Honest reporting: which lenses produced "no meaningful shift." This is
calibration signal — it tells the user which dimensions of their framing
are robust.]

### Recommendation

One of:
- **Keep original framing** — no reframing materially shifted the problem; proceed as framed
- **Adopt reframing X** — reframing X materially shifts the problem in a way worth adopting
- **Further explore** — multiple reframings materially shift; pick among them before proceeding

[Followed by 1-2 sentences explaining the recommendation.]

### Suggested Next Steps

- If keeping original framing: `/think-brainstorm` to generate approaches
- If adopting a reframing: restate the problem with the new framing, then `/think-brainstorm`
- If further exploring: pick a candidate reframing, refine it, and re-invoke `/think-reframe` with the revised framing
```

### 7. No Iteration

This skill is one-shot. If the user wants to pursue a reframing more deeply, they refine the problem statement (often by adopting a reframing) and **re-invoke**. The skill doesn't iterate in-session — each invocation is a clean consultation.

## Constraints

- **No artifacts.** No code, tickets, commits, or documents.
- **Isolated reframing.** Reframers do not see each other's output during generation.
- **Lens fit > lens count.** Drop lenses that don't fit the problem.
- **Reframing, not solving.** No approach recommendations — those come from downstream skills.
- **Honest "original framing holds"** is a valid, valuable outcome.

## When to Use

**Good fit:**
- Before `/think-brainstorm` — ensure you're brainstorming the right problem
- When a problem feels stuck and conventional approaches aren't working
- When a problem description feels off but you can't articulate why
- When stakes are high enough to merit pressure-testing the problem framing
- When a problem has been debated without convergence — often the debate is about framing, not solution

**Poor fit:**
- Choosing between options → use `/think-deliberate`
- Stress-testing a solution → use `/think-scrutinize`
- Generating approaches → use `/think-brainstorm`
- Problems so vague no meaningful framing exists yet (refine the problem first before reframing)
- Trivial problems where reframing is disproportionate effort

## Relationship to Other Skills

`/think-reframe` sits **upstream** of `/think-brainstorm` in the natural reasoning pipeline. The `/think-brainstorm` skill has a lightweight assumption-validation phase built in; `/think-reframe` is the full-strength version, run deliberately when the problem framing itself deserves scrutiny.

**Natural pipeline:**

```
/think-reframe → /think-brainstorm → /think-deliberate → /think-scrutinize
     redefine        generate            choose           stress-test
```

Each step is optional — you can enter the pipeline anywhere and exit anywhere — but this is the full reasoning chain from a raw problem to a stress-tested chosen approach.

## Philosophy

Most wasted effort goes into solving well-defined versions of the wrong problem. The discipline of reframing — deliberately asking "is this the right problem?" before solving — is universally skipped because it feels like delay. `/think-reframe` formalizes that discipline so it can't be skipped.

Isolation is what makes it work at scale. A single reframer produces one angle; parallel reframers applying different lenses produce angles that wouldn't occur to any one thinker. Synthesis then identifies which angles most shift meaning — the reframings worth seriously considering.

The honest outcome of a reframing exercise is often "the original framing is correct." That's not failure — it's calibration. The user can proceed with more confidence that they're solving the right problem. The outcome to fear is never reframing at all, not reframing and finding the original was sound.
