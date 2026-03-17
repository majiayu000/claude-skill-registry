---
name: draft-email-message
description: Draft a decision-ready outbound or response email artifact with channel-safe structure, clear CTA, and review checklist.
---

# Draft Email Message

Create high-quality email artifacts for business execution plans.

## When to Use

Use this skill when a task deliverable is an email (outbound, follow-up, or direct response) and you need a reusable artifact in-repo.

For inbox triage workflows, prefer `/process-emails`.

## Operating Mode

**ARTIFACT DRAFTING ONLY**

**Allowed:** draft/edit email content, create review checklists, save artifacts under `docs/`.

**Not allowed:** sending live emails automatically, inventing facts, bypassing explicit constraints.

## Inputs

- Objective (what this email should achieve)
- Audience/recipient segment
- Offer or request
- Required facts/source notes
- Tone and brand constraints
- CTA and response deadline (if any)

If any input is missing and blocks quality, ask for it before drafting.

## Output

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

## Workflow

1. Restate objective and audience.
2. Draft primary version optimized for clarity and action.
3. Add one alternate version when strategy/tone uncertainty exists.
4. Run checklist and revise.
5. Save artifact and summarize recommended send context.

## Completion Message

> "Email artifact ready: `docs/comms/email/<slug>-email.md`. Includes primary draft, optional variant, and quality checklist."
