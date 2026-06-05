---
name: kai-sdr-reply-triage
description: >
  Triage SDR replies and turn inbound responses into safe next actions, CRM handoff notes,
  suppression updates, objection responses, referrals, and meeting prep triggers. Use when
  "SDR reply", "triage replies", "outbound replies", "interested reply", "objection reply",
  "not interested", "unsubscribe", "wrong person", "bounce", "sales follow-up", "booked meeting",
  or any request to classify and respond to sales development replies.
---

# kai-sdr-reply-triage - Reply Loop

Classify SDR replies and produce the next safe action. This skill is for inbound responses after outbound, referrals, bounces, opt-outs, objections, and interested replies.

## Required Context

Load before triage:

- `harness/skill-contracts/sdr-reply-triage.yaml`
- `harness/skill-contracts/sdr-package.yaml`
- `harness/references/cold-email-rules.md`
- The relevant SDR package folder under `workspace/sdr-operator/<package-slug>/`
- Sender identity, suppression list, message history, and source evidence for the contact

If any required context is missing, write a triage hold note instead of drafting a send-ready response.

## Reply Categories

Classify exactly one primary category:

| Category | Action |
|---|---|
| `interested` | Prepare meeting handoff and short response. Trigger `/kai-sales-meeting-prep`. |
| `objection` | Identify objection type and draft one respectful response. |
| `referral` | Capture referred person, source, and permission trail. |
| `not_now` | Draft low-pressure close and future reminder task. |
| `wrong_person` | Ask for routing only when appropriate. Do not pressure. |
| `opt_out` | Suppress globally. Do not draft further outreach except opt-out confirmation if required. |
| `bounce` | Mark invalid contact path and block follow-up on that address. |
| `complaint` | Stop sequence, suppress, and route to human owner. |
| `unsubscribe_confirmed` | Record suppression and no further action. |
| `needs_human_review` | Use for legal, regulated, sensitive, hostile, ambiguous, or high-value replies. |

## Triage Workflow

1. Read the reply, original message, account row, contact row, source evidence, and suppression state.
2. Classify category, sentiment, urgency, and risk tier.
3. Identify whether the reply changes consent, suppression, routing, meeting status, objection state, or CRM state.
4. Draft the next message only when allowed.
5. Write CRM handoff notes and proposed tasks. Do not mutate CRM.
6. Update memory candidates for objection pattern, source quality, and message quality.
7. Trigger `/kai-sales-meeting-prep` when the reply implies a meeting, demo, call, referral intro, or buying conversation.

## Output

Write to:

```text
workspace/sdr-operator/<package-slug>/replies/<reply-id>.md
```

Use this shape:

```markdown
# Reply Triage - <reply-id>

## Classification
- Category:
- Risk tier:
- Sentiment:
- Urgency:
- Suppression action:

## Evidence
- Original message:
- Reply source:
- Account/contact row:
- Claim evidence:

## Next Action
- Owner:
- Action:
- Approval needed:
- Due:

## Draft Response
<Only include when allowed.>

## CRM Handoff
- Proposed note:
- Proposed task:
- Proposed field changes:

## Memory Candidate
- Learning type:
- Signal:
- Do not promote until:
```

## Rules

- Honor opt-outs immediately.
- Do not argue with complaints.
- Do not invent context or a prior relationship.
- Do not add new claims without evidence.
- Do not reply to bounces.
- Do not route sensitive, legal, or regulated replies without human review.
- Keep responses under 120 words unless the user asks for a longer sales response.
- Use one CTA or one next action.
