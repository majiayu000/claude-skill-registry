---
name: kai-sales-meeting-prep
description: >
  Prepare sales meetings from SDR replies, account dossiers, CRM notes, call notes, or transcripts.
  Produces account brief, buyer map, pain hypotheses, discovery questions, objection plan,
  meeting agenda, CRM handoff, follow-up email, and outcome memory. Use when "sales meeting prep",
  "prep this demo", "discovery call", "booked meeting", "SDR handoff", "post-call follow-up",
  "call notes", "sales transcript", or any request to prepare or follow up on sales development meetings.
---

# kai-sales-meeting-prep - Meeting Loop

Prepare a sales conversation and write the post-meeting follow-up. This skill turns SDR signals into a useful human sales briefing.

## Required Context

Load before writing:

- `harness/skill-contracts/sales-meeting-prep.yaml`
- `harness/skill-contracts/sdr-package.yaml`
- The relevant SDR package folder under `workspace/sdr-operator/<package-slug>/`
- Account dossier, contact row, reply triage, source evidence, product context, offer, and claim evidence

If call notes or a transcript are provided after the meeting, treat them as source material. Do not treat transcript statements as verified product facts unless the speaker and context are clear.

## Meeting Types

| Type | Use When | Output Bias |
|---|---|---|
| `first_discovery` | First call from SDR motion | Pain, urgency, owner, current process, next step |
| `demo_prep` | Prospect requested demo or walkthrough | Use case, proof, objections, tailored flow |
| `referral_intro` | Prospect routed to someone else | Context transfer, permission trail, concise ask |
| `revival_call` | Old opp or not-now reply returns | What changed, prior blocker, new trigger |
| `post_call_follow_up` | Notes or transcript available | Summary, commitments, next step, CRM update |

## Workflow

1. Read account, contact, source, reply, and product context.
2. Identify what is known, what is inferred, and what is missing.
3. Build a one-page meeting brief.
4. Draft discovery questions matched to the vertical pack and trigger evidence.
5. Map likely objections to concise responses with proof requirements.
6. Write a proposed agenda.
7. Write CRM handoff notes and proposed tasks.
8. After a call, write a follow-up email and memory candidates from actual outcomes.

## Post-Call Extraction And Scoring

When call notes or a transcript are available, extract only sourced facts and label every item as `prospect_said`, `seller_said`, `inferred`, or `missing`.

Capture:

- Pain stated, current workflow, trigger, desired outcome, decision process, stakeholders, timeline, budget signal, competitor or alternative, objection, commitment, and next step.
- Meeting quality score from 0-100: fit 25, pain clarity 20, urgency 20, authority or path to authority 15, next-step specificity 10, evidence completeness 10.
- Follow-up actions with owner, due date, approval needed, and source line or note reference.
- Memory candidates that can update source quality, trigger quality, objection patterns, and meeting quality after human approval.

Do not score missing budget, authority, or timeline as negative proof. Mark the component as `missing_data` unless the prospect clearly disqualified it.

## Output

Write to:

```text
workspace/sdr-operator/<package-slug>/meetings/<meeting-id>.md
```

Use this shape:

```markdown
# Sales Meeting Prep - <meeting-id>

## Account Snapshot
- Company:
- Contact:
- Role:
- Trigger:
- Fit score:
- Evidence:

## Call Objective
- Primary:
- Secondary:
- Next step:

## Known / Inferred / Missing
| Type | Notes |
|---|---|
| Known | |
| Inferred | |
| Missing | |

## Pain Hypotheses
1.
2.
3.

## Discovery Questions
1.
2.
3.

## Objection Plan
| Objection | Response | Proof needed |
|---|---|---|

## Agenda
1.
2.
3.

## Follow-Up Draft
<Only after call notes or a clear next step exist.>

## CRM Handoff
- Proposed note:
- Proposed task:
- Proposed stage:
- Approval needed:

## Memory Candidate
- Learning type:
- Evidence:
- Promotion status:
```

## Rules

- Do not invent pain, budget, authority, timeline, or competitor usage.
- Label hypotheses clearly.
- Keep the meeting brief one page unless the user asks for an enterprise dossier.
- Do not promise outcomes without source-backed proof.
- Do not mutate CRM or calendar without approval.
- After the meeting, separate prospect commitments from seller assumptions.
