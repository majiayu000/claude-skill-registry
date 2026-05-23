---
name: draft-email
description: Draft a decision-ready outbound or response email artifact with channel-safe structure, clear CTA, and review checklist.
---

# Draft Email Message

Create high-quality email artifacts for business execution plans.

## When to Use

Use this skill when a task deliverable is an email (outbound, follow-up, or direct response) and you need a reusable artifact in-repo.

For inbox triage workflows, prefer `/ops-inbox`.

## Operating Mode

**ARTIFACT DRAFTING ONLY**

**Allowed:** draft/edit email content, create review checklists, save artifacts under `docs/`.

**Not allowed:** sending live emails automatically, inventing facts, bypassing explicit constraints.

## Inputs

- Mode (`--mode single|sequence`, default: `single`)
- Objective (what this email should achieve)
- Audience/recipient segment
- Offer or request
- Required facts/source notes
- Tone and brand constraints
- CTA and response deadline (if any)

### Mode Behavior

**single** (default) - Produces a standalone email artifact. Output: `docs/comms/email/<slug>-email.md`

**sequence** - Produces a multi-email sequence (welcome, abandon cart, post-purchase, winback) with timing and triggers between emails. Output: `docs/comms/email/<slug>-sequence.md`

If any input is missing and blocks quality, ask for it before drafting.

## Output

### Single Mode (Default)

Create/update:

`docs/comms/email/<slug>-email.md`

Use this structure:

```markdown
# <Email Name>

## Context
- Objective:
- Audience:
- CTA:

## Draft v1
**Subject:** ...
**Preview:** ...

Hello ...,

...

## Variant (optional)
...

## Quality Checklist
- [ ] Facts verified against provided sources
- [ ] One primary CTA
- [ ] Clear next step + deadline (if applicable)
- [ ] Tone matches audience
- [ ] No ambiguous promises or unsupported claims
```

### Sequence Mode

Create/update:

`docs/comms/email/<slug>-sequence.md`

Use this structure:

```markdown
# <Sequence Name>

## Sequence Overview
- Type: (welcome / abandon cart / post-purchase / winback / nurture)
- Total emails: N
- Duration: X days
- Primary goal:

## Trigger Rules
- Entry condition:
- Exit conditions:
- Suppression rules:

---

## Email 1: <Name>

**Timing:** Immediately / +X hours / +X days after trigger
**Subject:** ...
**Preview:** ...

Hello ...,

...

**CTA:** [Primary action]

---

## Email 2: <Name>

**Timing:** +X hours/days after Email 1 (condition: if [action] not taken)
**Subject:** ...
**Preview:** ...

Hello ...,

...

**CTA:** [Primary action]

---

## Email N: <Name>

[Repeat structure]

---

## Sequence Quality Checklist
- [ ] Clear entry trigger defined
- [ ] Exit conditions prevent over-messaging
- [ ] Each email has distinct value/angle
- [ ] Timing intervals are customer-appropriate
- [ ] CTAs build urgency without desperation
- [ ] Facts verified against provided sources
```

## Workflow

### Single Mode

1. Restate objective and audience.
2. Draft primary version optimized for clarity and action.
3. Add one alternate version when strategy/tone uncertainty exists.
4. Run checklist and revise.
5. Save artifact and summarize recommended send context.

### Sequence Mode

1. Define sequence type, trigger rules, and total flow.
2. Draft each email with distinct value angle and timing.
3. Map conditional logic between emails (send next if action not taken).
4. Ensure urgency progression without over-messaging.
5. Run sequence checklist and revise.
6. Save artifact with implementation notes.

## Completion Message

**Single mode:**
> "Email artifact ready: `docs/comms/email/<slug>-email.md`. Includes primary draft, optional variant, and quality checklist."

**Sequence mode:**
> "Email sequence ready: `docs/comms/email/<slug>-sequence.md`. Includes N emails with trigger rules, timing, and sequence checklist."
