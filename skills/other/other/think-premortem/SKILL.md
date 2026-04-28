---
name: think-premortem
description: Prospective failure imagination for a plan, decision, or running system. Operates in two modes — **plan mode** (a plan has not yet been committed to; imagine its catastrophic failure broadly) and **scenario mode** (a specific catastrophic scenario is posed against an existing system; investigate causes against the actual code and architecture). Spawns parallel pre-mortemers in isolation across three categories of lens: standard failure classes (technical, operational, estimation, scope, adoption, dependency, team, incentive, detection, reversibility, adversarial), 0-3 ad-hoc target-specific lenses the orchestrator names when warranted, and a first-principles lens that always runs to catch what the prescribed taxonomy misses. Synthesizes into a prioritized risk register with early-warning signals. Produces feedback only — no code, no tickets, no artifacts.
model: opus
---

# Think-Premortem - Prospective Failure Imagination

Imagines a catastrophic failure has already happened and works backward to the causes. Uses the same Nominal-Group-Technique pattern as the rest of the `/think-*` namespace: parallel pre-mortemers, each in a different failure-class lens, generating in isolation. The orchestrator synthesizes into a prioritized risk register with early-warning signals the user can act on.

**This skill produces no tangible artifacts.** It is a consultant, not an implementer. No code, no tickets, no commits. The output is a structured risk register.

## Modes

The skill operates in one of two modes. The orchestrator detects mode from the user's framing and confirms before proceeding.

**Plan mode** — the user has a plan, design, or decision they have not yet committed to, and wants to imagine how it could fail. Pre-mortemers imagine a *broad* catastrophic failure within their lens, against the plan as proposed. The output guides what to change before commitment.

*Plan-mode example:* "Premortem this auth-service migration plan before we kick off."

**Scenario mode** — the user poses a specific catastrophic scenario against an *existing* system and asks how it could have happened. Pre-mortemers investigate the *given* scenario against the actual code, architecture, and configuration. The output guides hardening of the running system.

*Scenario-mode examples:*
- "An undiscovered zero-day exploit was used to attack our users via this app. How did this happen?"
- "A critical design defect destroyed the production database. How did this happen?"
- "A design defect caused AWS hyperscale and a runaway bill. How did this happen?"

The cognitive mechanism (Klein's *prospective hindsight*) is the same in both modes — the failure is treated as already-having-happened, and pre-mortemers reason backward. What differs is whether they imagine causes broadly (plan mode) or investigate the actual system for causes that could have produced a specific given scenario (scenario mode).

## The technique

Pre-mortem methodology comes from Gary Klein's decision research (*Sources of Power*, 1998; HBR, 2007). The core finding — *prospective hindsight* — is that imagining a failure as if it has already happened produces more concrete and better-calibrated cause identification than imagining failure as a forward-looking risk. Mitchell, Russo, and Pennington (1989) measured the effect: prospective hindsight produced roughly 30% better identification of correct reasons than risk-assessment framing.

The skill operationalizes that mechanism. Each pre-mortemer is told the plan failed, given a specific failure mode to inhabit, and asked to reconstruct how it got there.

## Roles

**Judge (you, running this skill):**
- Detect the mode from the user's framing (plan vs scenario), confirm
- Capture the target (the plan or the system + scenario) in a written brief
- Validate the input is concrete enough to fail concretely
- Choose appropriate failure-class lenses
- Spawn pre-mortemers in isolation
- Synthesize the pool into a prioritized risk register

**Pre-mortemers:** Each receives a specific failure-class lens (technical, operational, estimation, scope, adoption, dependency, team, incentive, detection, reversibility, adversarial), the mode, and the brief. In **plan mode**, they imagine a catastrophic failure within their lens against the plan and reason backward to plausible causes. In **scenario mode**, they investigate the actual system for causes that could have allowed the given scenario to occur — reading code where applicable.

## Workflow

### 1. Detect Mode and Receive the Target

**First, detect the mode** from the user's framing.

- **Plan-mode signals:** future-tense framing ("we're planning to," "before we commit," "we want to do"), reference to a design doc / scope output / ticket, deliberation language. The target is a *plan*.
- **Scenario-mode signals:** past-tense framing of a specific catastrophic event ("X happened, how?"), reference to an existing system or codebase, security-incident phrasing, named adverse outcome. The target is the *running system*, with the scenario as the failure given.

**If the framing is ambiguous, ask.** "Is this a plan you haven't committed to yet, or are you posing a hypothetical catastrophe against an existing system?"

The intake then differs by mode.

#### Plan mode

The plan may arrive as conversation context, a document (design doc, ticket, scope output, ADR), or fresh user input.

**Produce a written brief** of the plan. A good brief includes:
- **What is being attempted** — the deliverable in concrete terms
- **Why** — the goal it serves
- **By when** — the timeframe (if known)
- **Who** — the parties involved
- **Where it sits in the larger system** — dependencies, integrations, downstream consumers

#### Scenario mode

Capture two things:
- **The scenario** — the specific catastrophic event the user is posing. Past-tense, concrete. ("The production database was destroyed by a critical design defect." "An undiscovered zero-day was used to attack our users via this app.")
- **The target system** — what code, service, or component the scenario is posed against. Confirm scope: which directories, which services, which boundaries? Pre-mortemers will read this code; out-of-scope code should be excluded.

**Produce a written brief** that pairs the scenario with the system scope. Pre-mortemers operate on this brief and have read access to the scoped code.

### 2. Validate the Input Is Concrete Enough to Fail Concretely

**A pre-mortem on "we will improve quality" produces noise.** A pre-mortem on "we will replace the auth service over six weeks" produces signal. The same applies to scenarios: "something bad happened" produces noise; "the prod DB was destroyed by a design defect" produces signal.

**Plan mode — check:**
- Is the deliverable named, not gestured at?
- Is the timeframe bounded?
- Are the dependencies visible?
- Is the success criterion something a third party could verify?

**Scenario mode — check:**
- Is the scenario specific (a named catastrophic outcome), not vague ("things went wrong")?
- Is the target system identified and scoped?
- Is the scenario mechanistically plausible against the system as described, even if hypothetical?

If the input fails its checks, **say so plainly and offer the alternative**:
- Plan mode: refine the plan first (`/scope`, `/think-reframe`).
- Scenario mode: refine the scenario into something mechanistically posable, or — if the user is asking about an *actually-occurring* failure rather than a hypothetical — redirect to `/think-diagnose` (causes of an observed phenomenon) or `/think-reflect` (learning from a resolved incident). Scenario-mode pre-mortem is for *hypothetical* catastrophes against running systems, not for incidents that have actually happened.

### 3. Choose Failure-Class Lenses

Pre-mortemers cover three categories of lens:

1. **Standard lenses** — the 11 prescribed failure classes below. Pick 4-7 that fit the target.
2. **Ad-hoc target-specific lenses** — 0-3 additional lenses the orchestrator names when the target has known domain-specific failure modes that don't fit the standard taxonomy.
3. **`first-principles` lens** — always runs. Looks for failure modes specific to *this* target that don't fit cleanly into any standard or ad-hoc lens. Catches what the prescribed taxonomy misses.

The orchestrator decides selection; the user does not pick.

**In plan mode**, standard-lens selection is driven by what the plan affords (technical, operational, estimation are usually present; team, adoption, dependency-and-environment are situational).

**In scenario mode**, standard-lens selection is partly fixed by the scenario itself — a zero-day exploit scenario has *adversarial* as its primary lens; a runaway-bill scenario has *incentive* and *operational*; a DB-destruction scenario has *technical* and *reversibility*. Pick lenses that the scenario plausibly engages, plus 1-2 secondary lenses that often surface contributing causes (typically *detection* and one situational lens).

**Standard lenses:**

- **technical** — implementation broke, design didn't survive contact with reality, system failed under load, integration shattered
- **operational** — couldn't deploy, couldn't observe, couldn't maintain, on-call burden made it untenable
- **estimation** — took 3-5x longer, sandbagged assumptions, hidden complexity surfaced late
- **scope** — built the wrong thing, requirements were misunderstood, the problem moved while we built
- **adoption** — nobody used it, users found a workaround, was replaced by an alternative
- **dependency-and-environment** — external dependency changed/broke, vendor shifted, regulation moved, market changed
- **team-and-coordination** — attrition, knowledge loss, blocked on someone, handoff breakdown, conflicting priorities
- **incentive** — Goodhart; system rewarded the wrong thing; what got measured drove behavior away from intent
- **detection** — failure went unnoticed until catastrophic; instrumentation gap; silent failure
- **reversibility** — couldn't roll back; data corruption was permanent; sunk cost trapped continuation
- **adversarial** — security breach, malicious actor, abuse pattern, untrusted input slipped through

**Selection heuristics for standard lenses:**

- Software project? **Always** include technical, operational, estimation.
- User-facing change? Include adoption.
- Multi-team or multi-person? Include team-and-coordination.
- Long-running (>1 quarter) or external-facing? Include dependency-and-environment.
- High-stakes, hard-to-reverse work? Include reversibility.
- Performance metrics or KPIs involved? Include incentive.
- Complex infrastructure or distributed systems? Include detection.
- Public-facing or security-sensitive? Include adversarial.
- Plan involves a fixed deadline or resource constraint? Lean into estimation.

**Drop standard lenses that don't fit.** A solo prototype has no team-and-coordination story; a behind-the-firewall internal tool may have no adversarial story; a one-day spike has no estimation story worth pre-mortem-ing.

**Ad-hoc target-specific lenses (0-3):**

If the target has known domain-specific failure modes that don't fit the standard taxonomy, the orchestrator names them as ad-hoc lenses. The orchestrator provides a one-sentence definition for each ad-hoc lens when spawning the pre-mortemer.

Add an ad-hoc lens when:

- The target's domain has a recognized class of failure that doesn't map cleanly to a standard lens
- A standard lens would technically cover it but would dilute focus by mixing it with unrelated concerns

Examples:

- ML system → `training-distribution-drift` (model performance degrades as input distribution diverges from training data)
- Multi-tenant SaaS → `tenant-isolation` (one tenant's actions affect another's correctness, performance, or privacy)
- Real-time trading system → `latency-and-jitter` (timing variance produces correctness or ordering failures)
- Federated identity system → `cross-domain-trust` (trust propagation across boundaries amplifies a single compromise)
- Compliance-bound system → `regulatory-shift` (a regulation change retroactively invalidates compliant behavior)

If no ad-hoc lens is warranted, run zero. The standard lenses + first-principles cover most cases. Adding ad-hoc lenses for the sake of comprehensiveness dilutes the register.

**`first-principles` lens (always runs):**

The free-form lens. Its job is to catch what the structured taxonomy misses by reasoning from the irreducible specifics of *this* target rather than from a category. The pre-mortemer is told explicitly: *"Look for failure modes specific to this target that don't fit cleanly into any other lens being applied. If a failure mode you find is squarely within a standard or ad-hoc lens, drop it — that lens has it covered."*

Honest "nothing here that the other lenses don't already catch" is a valid, calibrated outcome from the first-principles lens — same discipline as the standard "lens didn't apply" pattern. Manufactured findings dilute the register.

### 4. Spawn Pre-Mortemers (Parallel, Isolated)

Spawn one `THK - Premortemer` agent per chosen lens, in parallel. Each receives:

- The brief (from step 1)
- The mode (plan or scenario)
- Its assigned lens, with the lens definition:
  - For **standard lenses**, the definition is built into the agent — pass the lens name only
  - For **ad-hoc lenses**, the orchestrator provides the lens name *and* a one-sentence definition
  - For the **first-principles lens**, the agent is instructed to look for what the other lenses miss; pass the names of the other lenses being applied so the pre-mortemer can discriminate
- Relevant context (constraints, dependencies, prior similar attempts if any)

**In plan mode**, instruct the pre-mortemer to imagine the plan **has already failed** within their lens (not "could fail") and reconstruct the path that produced it.

**In scenario mode**, instruct the pre-mortemer to **investigate the actual system** for causes that could have allowed the *given* scenario to occur, viewed through their lens. Tell them which directories / services / files are in scope and that they have read access. They should cite specific code (file:line where applicable) for their findings.

**No cross-talk between pre-mortemers.** This is the NGT principle — independent generation prevents anchoring on the first plausible-sounding failure cause. In scenario mode this is even more important: independent investigation surfaces causes that one shared narrative would miss.

Collect all outputs.

### 5. Synthesize into a Prioritized Risk Register

The synthesis differs from `/think-brainstorm` (which produces a catalog of options) and from `/think-scrutinize` (which produces faults that survived adversarial cross-examination). The output here is a *risk register*: failure modes, calibrated by likelihood and impact, paired with early-warning signals.

**5a. Cluster causes across lenses.** Multiple lenses often surface the same underlying cause (e.g., "underestimated migration complexity" appears under estimation and technical). Merge and preserve lens attribution — multiple angles landing here is signal.

**5b. Calibrate likelihood and impact qualitatively.** Use *high / moderate / low / uncertain* — not fabricated percentages. The discipline is to be honest about confidence, not to fake precision.

- **Likelihood** — how plausible is the failure mode given the target as stated? In plan mode, against the plan; in scenario mode, given the actual system in its current state.
- **Impact** — if it happened, how bad is the outcome?

**5c. Identify early-warning signals.** For each significant failure mode, name the observable signal that would appear *before* the catastrophic outcome.

- In plan mode, signals are things to watch for *during execution* — "X would appear about two weeks before the catastrophe."
- In scenario mode, signals are things observable *now*, in the running system, that would indicate the scenario is brewing — "an audit of the current logs would show Y if this is currently developing."

"We'd see X" is more actionable than "this could go wrong."

**5d. Distinguish defendable from monitor-only.** Some failure modes can be designed against now (defendable). Others cannot — they can only be monitored for and responded to (monitor-only). Label each.

**5e. Surface the top 3-5.** Risk registers with 40 entries get ignored. Pick the 3-5 highest *likelihood × impact* failure modes for headline treatment. The rest go into a tail section for completeness.

**5f. Drop weak findings.** Generic risks ("the project might be late") that any plan would face don't earn a spot. The standout failure modes are specific to *this* plan, this team, this dependency graph.

### 6. Report

**Final report format:**

```
## Pre-Mortem Report

**Mode:** [plan | scenario]
**Target:** [one-line — the plan, or the system + given scenario]
**Lenses applied:** [list]
**Time horizon (plan mode):** [the failure point — e.g., "6 weeks from now"]
   *or*
**Scenario (scenario mode):** [the catastrophic event posed]

### Top Failure Modes

[The 3-5 highest-priority failure modes. Each:]

1. **[Name of failure mode]** — *(lenses: [which lenses surfaced it])*
   - **Failure scenario:** [concrete narrative — 2-3 sentences of what failure looks like]
   - **Causes:** [the path that got us there — 2-4 specific causes; in scenario mode, cite file:line where applicable]
   - **Likelihood:** [high / moderate / low / uncertain] — [brief reasoning]
   - **Impact:** [high / moderate / low] — [brief reasoning]
   - **Early-warning signals:** [what we'd observe — in plan mode, before the catastrophe; in scenario mode, in the system right now]
   - **Defendable / monitor-only:** [classification + brief note]

### Other Failure Modes Worth Tracking

[Lower-priority entries, tabulated:]

| Failure mode | Lens | Likelihood | Impact | Early signal |
|--------------|------|------------|--------|--------------|
| ...          | ...  | ...        | ...    | ...          |

### Cross-Cutting Observations

[Patterns that emerged across lenses — e.g., "three lenses landed on
hidden coupling with the legacy auth service," or "estimation and
adoption both flagged the same training-overhead problem." These
cross-cuts often matter more than any single finding.]

### Load-Bearing Assumptions

[Assumptions the plan depends on that, if false, invalidate it.
Surfaced through the pre-mortem exercise. The user should verify these
before commitment.]

### Lenses That Found Little

[Honest reporting. If a chosen lens produced little for this plan,
note it. This is calibration, not failure.]

### Suggested Next Steps

- To stress-test specific mitigations: `/think-scrutinize`
- To choose between candidate mitigation / hardening approaches: `/think-deliberate`
- To turn defendable failure modes into tickets: `/scope`
- To re-pre-mortem after the plan is revised or the system is hardened: re-invoke `/think-premortem`
```

### 7. No Iteration

This skill is one-shot. If the user revises the plan based on the report, they **re-invoke** with the revised version. If they want to stress-test a specific mitigation, they hand off to `/think-scrutinize`. If they want to choose between mitigations, `/think-deliberate`. Each invocation is a clean consultation.

## Constraints

- **No artifacts.** No code, tickets, commits, or documents.
- **Prospective hindsight framing.** In both modes, the failure is treated as already-having-happened, not as a forward-looking risk. The framing is load-bearing — Klein's mechanism depends on it.
- **Isolated generation.** Pre-mortemers do not see each other's output during generation.
- **Calibrated qualitative confidence.** No fabricated percentages. *High / moderate / low / uncertain* only.
- **Specificity over volume.** A risk register is not a list of every conceivable failure; it is the failure modes specific to this target.
- **Scenario mode requires concrete evidence.** When a pre-mortemer claims the system has a particular weakness, it must point at the specific code / config / architecture that produces it. No hand-waving.
- **Honest "lens didn't apply"** is allowed and valuable.

## When to Use

**Good fit (plan mode):**

- Before committing to a plan, design, or significant decision
- Pre-flight check before invoking `/lead-project` or `/implement-project` on a project that will run for weeks
- Before merging a major architectural change
- Before announcing a deadline, deliverable, or rollout to stakeholders
- When a plan feels solid and there is residual unease — the unease often points at a failure mode worth surfacing

**Good fit (scenario mode):**

- Hardening an existing system against a hypothetical catastrophe ("if a zero-day were used against us, how could it have happened?")
- Investigating worst-case scenarios for a deployed service before adversarial conditions actually materialize
- Stress-testing a system's hidden-coupling, reversibility, or detection assumptions by imagining specific catastrophic outcomes
- Pre-incident-response preparation — surfacing what the on-call team would need if a named scenario hit

**Poor fit:**

- Plans too vague to fail concretely (refine first via `/scope` or `/think-reframe`)
- Currently-failing situations whose cause is unclear (use `/think-diagnose` — that skill handles real, observable failures with unknown causes; scenario-mode pre-mortem is for *hypothetical* catastrophes)
- Already-resolved incidents the user wants to learn from (use `/think-reflect`)
- Choosing between options (use `/think-deliberate`)
- Generating new approaches (use `/think-brainstorm`)

**Rule of thumb:**

- "What could go wrong with this plan?" → `/think-premortem` (plan mode)
- "If [catastrophe] hit our system, how could it have happened?" → `/think-premortem` (scenario mode)
- "What's wrong with this idea right now?" → `/think-scrutinize`
- "Why is this currently broken?" → `/think-diagnose`

## Relationship to Other Skills

`/think-premortem` and `/think-scrutinize` overlap but are not redundant. Pre-mortem is broader and more generative — it sweeps the failure space using prospective hindsight. Scrutinize is narrower and more dialectical — it pits skeptics against an advocate on a specific concern. The natural ordering is *pre-mortem first, scrutinize second*: pre-mortem identifies the top failure modes; scrutinize stress-tests the mitigations or load-bearing assumptions surfaced by the pre-mortem.

`/think-premortem` and `/think-diagnose` are easy to confuse but distinct. Diagnose is for *currently-observable* failures whose causes are unknown — abductive reasoning to infer what is causing a real phenomenon. Scenario-mode pre-mortem is for *hypothetical* catastrophes against running systems — the user posits "imagine X happened" against a system where X has *not* happened, and the skill investigates what features of the system could allow X. If the failure is actually happening now, route to `/think-diagnose`. If it is hypothetical, scenario-mode pre-mortem applies.

`/think-premortem` and `/think-reflect` are matched pairs along the time axis. Pre-mortem is prospective failure imagination *before* the failure occurs; reflect is retrospective learning *after* an experience has played out. They share the design value of separating decision quality from outcome quality (Tetlock) — pre-mortem at the front, reflect at the back.

Natural follow-ups:
- A failure mode the user wants to defend against → `/scope` to ticket the mitigation / hardening work
- A specific mitigation or hardening proposal that needs stress-testing → `/think-scrutinize`
- A choice between hardening approaches → `/think-deliberate`
- A failure mode whose causal path isn't clear during synthesis → `/think-diagnose`

## Philosophy

The default mode of both planning and operating systems is optimistic. People imagine plans succeeding and systems running cleanly, then patch over failure modes that happen to surface. This systematically under-attends to risks and produces post-hoc surprise when those risks materialize.

Klein's contribution is the framing reversal: instead of asking "what could go wrong?" — which the planning brain shrugs off — pre-mortem says "the failure has already happened; figure out why." Prospective hindsight bypasses the optimism filter. People are surprisingly good at imagining concrete failure causes when they are told a failure already occurred.

The technique generalizes. It works on plans before commitment (Klein's original framing) and on running systems against hypothetical catastrophes (the same cognitive trick, applied to a different target). What changes is whether the pre-mortemers imagine causes broadly within the plan, or investigate the actual system for causes that could have produced a specific given scenario.

The plugin operationalizes both with the NGT-isolated parallel-agents pattern that the other `/think-*` skills use. Independent imagination prevents anchoring on the first plausible failure cause; synthesis produces a register the user can act on — not a list of generic risks they can dismiss.

The discipline is: imagine or investigate specifically, generate in isolation, calibrate honestly, surface the early-warning signals. The output is meant to make the plan stronger or the system harder, not to prevent the plan from being attempted or the system from being trusted.
