---
name: draft-whatsapp-message
description: Draft WhatsApp-ready business messages with concise structure, clear CTA, and compliance-aware guardrails.
---

# Draft WhatsApp Message

Create short-form WhatsApp messages that are actionable, channel-appropriate, and review-ready.

## When to Use

Use this skill when the deliverable is outbound or follow-up WhatsApp communication (customer update, reminder, conversion prompt, operational notice).

## Operating Mode

**MESSAGE DRAFTING ONLY**

**Allowed:** draft concise message variants, define CTA, include fallback follow-up copy.

**Not allowed:** auto-send messages, violate opt-in/compliance constraints, produce long-form email-style copy.

## Inputs

- Message objective
- Audience segment
- Required facts and context
- CTA + response window
- Tone/language constraints
- Compliance assumptions (opt-in, timing, policy)

## Output

Create/update:

`docs/comms/whatsapp/<slug>-whatsapp.md`

Required structure:

```markdown
# <WhatsApp Message Name>

## Context
- Objective:
- Audience:
- CTA:

## Primary Message
...

## Follow-up Variant
...

## Compliance & Quality Checklist
- [ ] Opt-in assumption documented
- [ ] Message is concise and scannable
- [ ] Single clear CTA
- [ ] No unsupported claims
- [ ] Timing constraints noted
```

## Workflow

1. Lock objective, audience, and CTA.
2. Draft primary message in concise WhatsApp format.
3. Draft one follow-up variant.
4. Run checklist and revise.
5. Save artifact and summarize recommended send conditions.

## Completion Message

> "WhatsApp message artifact ready: `docs/comms/whatsapp/<slug>-whatsapp.md` with primary + follow-up variants and compliance checklist."
