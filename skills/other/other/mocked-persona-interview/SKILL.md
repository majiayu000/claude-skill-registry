---
name: mocked-persona-interview
description: "Use when real user interviews aren't possible (solo/hobby/dogfood projects) but persona work is still needed. Enforces epistemic discipline: adversarial spectrum, pre-committed stop conditions, speculation tagging. NOT a substitute for /user-interview when real users are available."
instruction_budget: 70
---

# Mocked Persona Interview Skill

A disciplined alternative to real user interviews when:
- You're a solo developer and cannot talk to users this week
- You're on a hobby/learning project with no user research budget
- You're running a meta-project dogfood session (see `dogfood_modifier`)
- You're in early L0/L1 exploration where real interviews are premature

**This skill is NOT a substitute for `/user-interview` when real users are available.** Mocked personas are simulation. They catch some mistakes, miss others, and — without discipline — become a confirmation-bias machine. This skill's job is to enforce the discipline.

## Why This Skill Exists

From the macos-fileviewer dogfood session (2026-04-09, finding G2):

> Solo founder, no user research budget, hobby/learning project. Real user interviews aren't going to happen. Yet the framework's L0–L2 evidence gates require multi-source user evidence. Mycelium has `/user-interview` (Torres-style real interviews) but no equivalent for the very common case of "I cannot or will not talk to real users right now". An agent invited to "mock some personas" with no discipline guidance would, in 9 of 10 cases, produce 5 sympathetic NPCs and call it validation.

This skill is the disciplined alternative. It was invented ad-hoc during the dogfood session and caught the value-risk failure on the fileviewer project. Without the discipline, the session would have produced confident-sounding validation and the failure would have been missed.

## Discipline Rules (Non-Negotiable)

These rules are what separate "mocked personas as a learning tool" from "mocked personas as a confirmation-bias machine." Every rule must be followed in order.

### 1. Pre-define the persona spectrum BEFORE generating any personas

Brainstorm the spectrum FIRST, in the chat with the user, before writing any persona profiles. The spectrum must include:

- **The founder-twin** (someone who thinks like you, the person doing the research)
- **The modal user** (the most likely actual user if the product shipped today — NOT the ideal user)
- **An adversarial persona** (someone who will plausibly reject the product for good reasons — e.g., "already has a workflow they love", "terminal purist", "zero-tolerance-for-yet-another-tool")
- **A cost-conscious persona** (someone whose constraint is time, money, or cognitive load)
- **A niche-fit persona** (accessibility needs, localization needs, unusual workflow)
- **One wildcard** (someone unexpectedly outside the assumed target audience)

**Minimum 6 personas.** Fewer than 6 invites clustering around the founder-twin.

**Pre-commit the spectrum in the decision log**: write the 6 archetypes BEFORE generating the profiles. This creates accountability.

### 2. Write the profile FIRST, the interview SECOND

For each persona:
1. Write a one-paragraph profile (name, role, context, constraints, why they would/wouldn't adopt the product)
2. ONLY AFTER the profile is written, conduct the in-character interview
3. The interview questions come from `/user-interview` (Torres story-based format)
4. The in-character answers must be consistent with the profile — if the profile says "hates yet another tool," the interview answers cannot contradict that

This ordering prevents backfilling profiles to justify interview answers.

### 3. Pre-commit the stop condition BEFORE conducting any interviews

Agree a stop condition with the user, in writing, before any interviews happen. Example stop conditions:

- "If 3 of 6 personas hard-reject the core value proposition, the exercise is FAILED"
- "If 4 of 6 personas identify the same showstopper, we pause the diamond"
- "If the modal user rejects, we treat this as a value-risk failure regardless of what the others say"

Write the stop condition in the decision log BEFORE conducting interviews. This is load-bearing — without it, the temptation to soften the conclusion when the stop condition triggers is enormous.

### 4. Tag every canvas update with `evidence_type: speculation`

Every canvas entry that comes from this exercise MUST be tagged:

```yaml
provenance:
  evidence_type: speculation  # NOT anecdotal, NOT data-supported
  evidence_sources:
    - "mocked-persona-interview-2026-04-09"
  captured_at: "..."
  confidence: 0.2  # Or lower. Speculation is speculation.
```

**Never upgrade the evidence_type based on mocked interviews.** Real interviews are anecdotal. Data is data-supported. Mocked is speculation. The distinction matters.

### 5. Honest synthesis discipline

When synthesizing across personas:
- **If all 6 agree, that's a tell** — redo with more adversarial bias, you probably wrote sympathetic NPCs
- **If the stop condition triggered, flag the exercise as FAILED** in the output, not "mostly positive with some concerns"
- **Never average out the rejections** — a single hard rejection from the modal user outweighs 5 enthusiastic yeses from niche personas
- **Do not paper over the failure to be helpful to the user** — the user invoked this skill because they want honest epistemic discipline, not cheerleading
- **Map each rejection to a JTBD job ID** (v0.11.1) — cross-reference `canvas/jobs-to-be-done.yml`. For each persona that rejected, identify which specific job(s) are at risk. This prevents implicit connections between "persona rejects" and "which job fails." If a rejection can't be mapped to an existing job, that's a signal the JTBD canvas is incomplete.

### 6. Document the exercise in the decision log

After the exercise, log a decision-log entry with:
- Date and scope (which diamond / canvas this feeds)
- The pre-committed spectrum (6 archetypes with rationale)
- The pre-committed stop condition
- The result (did it trigger? yes/no)
- Confidence delta on the target diamond (explicit number)
- Next action (pivot / park / continue / kill)

## Workflow

### Step 1: Gate check
Verify the project is a legitimate use case for mocked personas:

- Is this project flagged `dogfood: true`? → OK
- Is this `solo_hobby` with no real user access? → OK
- Is this L0/L1 pre-product-market-fit exploration? → OK
- Does the user have access to real users? → **Stop. Use `/user-interview` instead.**
- Does the user have >5 unique target users reachable this week? → **Stop. Use `/user-interview`.**

If the gate fails, do not proceed. Say: "You have access to real users. Mocked personas would produce weaker evidence than a single real interview. Run `/user-interview` instead."

### Step 2: Pre-commit the spectrum

Ask the user to agree on the 6 persona archetypes. Write them to the decision log before generating any profiles.

### Step 3: Pre-commit the stop condition

Ask the user: "What would make us say this exercise FAILED? Write the condition before we start, so we hold ourselves to it."

Examples to offer:
- "If N of 6 hard-reject, fail"
- "If the modal user hard-rejects, fail regardless of others"
- "If all 6 have the same showstopper, fail"

Log the agreed condition in the decision log.

### Step 4: Generate profiles (not interviews yet)

For each of the 6 archetypes, write a one-paragraph profile. Do NOT write interview answers yet.

### Step 5: Conduct in-character interviews

Using Torres's story-based format from `/user-interview`, conduct interviews for each persona. The answers must be consistent with the profile written in Step 4.

### Step 6: Synthesize honestly

Evaluate against the pre-committed stop condition. Report the result FIRST (pass / fail), then nuance.

If triggered: say so clearly. Do not soften. Do not average. Do not "mostly positive with some concerns."

### Step 7: Update canvas with `evidence_type: speculation`

Write to relevant canvas files (user-needs.yml, opportunities.yml) with provenance showing `evidence_type: speculation` and low confidence.

### Step 8: Log the decision

Decision log entry with all 6 fields from Rule 6 above.

## Output Format

```
## Mocked Persona Interview Report
Date: [date]
Scope: [diamond ID and phase]
Project: [object project name]
Dogfood mode: [yes/no]

### Pre-committed discipline
- Spectrum (6 archetypes): [list with rationale]
- Stop condition: [exact wording agreed before interviews]

### Personas generated
[6 one-paragraph profiles, written before interview answers]

### Interview findings
[per-persona Torres-style interview summary, answers consistent with profile]

### Stop condition evaluation
[TRIGGERED / NOT TRIGGERED — with evidence]

### Synthesis (honest)
- Consensus points: [not "everyone agreed" — look for what was IGNORED]
- Adversarial signals: [the rejections matter more than the approvals]
- Modal user verdict: [the most likely actual user's position]
- JTBD risk mapping: [for each rejection, which job ID from jobs-to-be-done.yml is at risk and why]
- Recommendation: [continue / pivot / park / kill — with rationale]

### Canvas updates
- user-needs.yml: N entries added with evidence_type: speculation
- opportunities.yml: N entries updated
- Diamond confidence delta: [before → after, e.g., 0.4 → 0.25]
- All entries tagged provenance.evidence_type: speculation

### Decision log entry
Logged at .claude/harness/decision-log.md with: spectrum, stop condition, trigger status, next action.
```

## Anti-Patterns This Skill Prevents

- **Sympathetic NPC syndrome**: generating 5 personas who all love the product
- **Backfilled profiles**: writing interview answers first, then inventing profiles to justify them
- **Softening the stop condition**: "technically the stop condition triggered but the feedback was mostly positive"
- **Evidence_type inflation**: tagging mocked data as `data-supported` or `anecdotal`
- **Averaging rejections**: treating a 4-accept / 2-reject result as "mostly positive"
- **Post-hoc rationalization**: changing the stop condition after seeing the results

## Canvas Output

Update `.claude/canvas/user-needs.yml` (high-stakes canvas) with new needs entries, each tagged:

```yaml
provenance:
  evidence_type: speculation
  evidence_sources:
    - "mocked-persona-interview-YYYY-MM-DD"
  captured_at: "..."
  confidence: 0.2
```

Update `.claude/canvas/opportunities.yml` (high-stakes canvas) with any new opportunities surfaced, also tagged `evidence_type: speculation`.

## Theory Citations

- **Torres** — Continuous Discovery Habits (source for the story-based interview format; this skill is the disciplined substitute when real interviews aren't available)
- **Kahneman** — Thinking, Fast and Slow (confirmation bias, the specific trap this skill is designed to prevent)
- **Shotton** — The Choice Factory (behavioral framing bias in research design)
- **Dogfood session 2026-04-09** — macos-fileviewer (the session that invented this discipline and proved it works)

## Related Skills

- `/user-interview` — the real thing. Use this whenever possible.
- `/devils-advocate` — run after synthesis to challenge the recommendation
- `/canvas-update` — for applying the exercise results to canvas files
- `/bias-check` — run BEFORE the exercise to pre-screen the agent's own biases

## Honest Caveat

Mocked personas are weaker evidence than real interviews. This skill exists because real interviews are sometimes impossible, not because mocked personas are equivalent. If you can talk to real users, do. If you can't, use this skill and treat the output as speculation — because it is.
