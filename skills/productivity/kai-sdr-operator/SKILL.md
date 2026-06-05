---
name: kai-sdr-operator
description: >
  Build a plug-in-ready SDR operator package for sales development and outbound pipeline work:
  ICP definition, compliant lead-source plan, enrichment/research workflow, account scoring,
  outbound assets, CRM handoff, reply triage, meeting prep, approval gates, and loop memory. Use when "SDR",
  "sales development", "outbound SDR", "operator room", "lead gen pipeline",
  "prospecting pipeline", "ICP targeting", "Apify", "RapidAPI", "Clay", "Apollo",
  "agentic SDR workflow", "sales operating loop", "sales dashboard handoff", or any request
  to package outbound sales workflows that can later connect to data tools, CRMs, or operator surfaces.
---

# kai-sdr-operator - SDR Package Builder

Create a reusable SDR operating package. The package should let a human or future agent connect lead sources, enrich accounts, score fit, prepare compliant outreach, triage replies, prep meetings, write follow-up, update CRM handoff records, and learn from outcomes.

This skill is the orchestrator. Use `/kai-cold-outreach` for the actual cold email copy after the lead-source, suppression, sender, and claim evidence gates are clear. Use `/kai-sdr-reply-triage` for replies and `/kai-sales-meeting-prep` for booked calls. Use `/kai-data-dashboard` only when the user explicitly asks for a dashboard surface.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the project root.

If it exists, read it before asking questions. If it does not exist, run `/kai-start` or infer a temporary brief from trusted project files and mark unknowns as `[TODO]`.

Load these files before production:

- `harness/skill-contracts/sdr-package.yaml`
- `harness/skill-contracts/cold-email.yaml`
- `harness/references/cold-email-rules.md`
- `knowledge/playbooks/demand-generation.md`
- `knowledge/playbooks/account-based-marketing.md` when named accounts or enterprise targets matter
- `knowledge/channels/email-lifecycle.md` when email deliverability or sender setup matters
- `harness/skills/kai-sdr-operator/references/sdr-data-model.md`
- `harness/skills/kai-sdr-operator/references/connector-recipes.md`
- `harness/skills/kai-sdr-operator/references/connector-action-contracts.md`
- `harness/skills/kai-sdr-operator/references/vertical-packs.md`
- `harness/skills/kai-sdr-operator/references/human-approval-gates.md`
- `harness/skills/kai-sdr-operator/references/operating-loop.md`
- `harness/skills/kai-sdr-operator/references/loop-events-and-transitions.md`
- `harness/skills/kai-sdr-operator/references/compliance-matrix.md`
- `harness/skills/kai-sdr-operator/references/observability-and-run-ledger.md`
- `harness/skills/kai-sdr-operator/references/evaluation-harness.md`
- `harness/skills/kai-sdr-operator/references/external-loop-research.md`

## Phase 1: Package Mode

Choose one package mode from the request or product context:

| Mode | Best Fit | Output Bias |
|---|---|---|
| `pipeline_prototype` | Interview demo, founder experiment, first outbound system | Small sample list, visible workflow, dashboard-ready schema |
| `b2b_sdr_engine` | SaaS, agency, service firm, consulting offer | ICP scorecard, lead sources, email/LinkedIn/call handoff |
| `abm_sdr_engine` | Named accounts or enterprise targets | Account dossiers, buying committee, 1:1 research tasks |
| `local_phone_led` | Local services, legal, home services, clinics | Call capture, speed-to-lead, KaiCalls fit review |
| `recruiting_sdr_engine` | Staffing, recruiting, talent marketplace | Candidate/client split, employment-policy caution, role-fit evidence |
| `partner_sdr_engine` | Co-marketing, channels, affiliates, agencies | Partner-fit matrix, mutual value, low-volume relationship motion |
| `sdr_migration_audit` | Existing SDR team moving work into Claude/Kai loops | Workflow map, automation readiness, cost model, approval plan |

Default to `pipeline_prototype` when the user is building a showcase or proof-of-work asset.

## Phase 2: Discovery

Read from `MARKETING.md`. Ask only for missing facts:

1. Offer and desired conversion: meeting, demo, audit, quote, trial, or call.
2. ICP filters: industry, geography, company size, tech stack, budget, trigger events.
3. Lead sources available: CRM export, event list, partner list, Apollo, Clay, Apify, RapidAPI, public directories, user-provided CSV.
4. Outreach channels: email, LinkedIn, phone, SMS, ads, direct mail.
5. Sender stack: domain, ESP, CRM, sequencer, calendar, suppression list.
6. Volume target and human review capacity.
7. Regulated or sensitive categories: healthcare, finance, legal, minors, employment, housing, credit, political, or consumer data.

## Phase 3: Source And Compliance Plan

Before building any list, write `_lead-source-plan.md`.

Required lead-source plan sections:

- Approved source inventory with owner, access method, terms notes, and data fields.
- Disallowed sources and why they are blocked.
- Suppression source and opt-out sync path.
- Consent or lawful-interest basis by region.
- Data minimization rules: collect only fields needed for fit, relevance, routing, and compliance.
- Connector notes for tools such as Apify or RapidAPI.
- Human approval required before any live connector run, import, export, enrichment credit spend, message send, call, SMS, or CRM mutation.

Apify, RapidAPI, Clay, Apollo, CRM exports, and similar tools are adapters, not permission slips. Use current vendor docs and account terms before running a connector. Do not bypass logins, CAPTCHAs, robots restrictions, paywalls, platform rate limits, or social-network terms. Do not use personal email scrapes, consumer lists, sensitive personal attributes, or bought accounts.

Do not start billable API runs, export contacts to a CRM, send email, send DMs, place calls, or mutate any live system without explicit human approval.

## Phase 4: SDR Workflow Architecture

Design the operator workflow as linked agents or queues:

1. **Source Scout** - finds lawful account sources and writes source rows.
2. **ICP Scorer** - scores accounts against fit, intent, timing, and disqualification rules.
3. **Contact Mapper** - identifies likely buyers, influencers, blockers, and routing contacts.
4. **Personalization Researcher** - writes one sourced relevance note per contact or account.
5. **Outreach Producer** - hands approved rows to `/kai-cold-outreach`.
6. **Test Cohort Runner** - prepares a tiny approved test cohort before any broad activation.
7. **Compliance Reviewer** - checks suppression, sender identity, claims, opt-out, and list risk.
8. **Reply Router** - invokes `/kai-sdr-reply-triage` to classify replies and draft next actions.
9. **Meeting Prepper** - invokes `/kai-sales-meeting-prep` for booked meetings and discovery calls.
10. **CRM Handoff Writer** - prepares records, notes, tasks, owners, and stage changes for approval.
11. **Daily Briefing Writer** - summarizes pipeline alerts, blocked rows, reply queue, meeting prep, and approvals.
12. **Outcome Learner** - updates memory ledgers for source quality, trigger quality, objection patterns, meetings, and wins.

Keep each worker's input and output explicit enough that a future sub-agent, MCP connector, or dashboard can call it.

### Signal Routing, Suppression, And Approval Queue

Route every account or contact through a deterministic queue before outreach:

- Ingest signals as separate rows: fit signal, timing signal, pain evidence, reply signal, referral, opt-out, bounce, competitor mention, or meeting intent.
- Apply suppression before scoring promotion. Suppression includes prior opt-out, existing customer conflict, active opportunity owner, disallowed source, sensitive-data risk, bad domain, region restriction, or missing lawful basis.
- Promote only `suppression_status=clear` rows to `approved_for_copy`; send `needs_review`, `conflict`, and `blocked` rows to the approval queue.
- Store the approval queue with row ID, requested live action, reason, evidence, approver, decision, timestamp, and next state.
- Never let a signal alone trigger a live send, CRM mutation, connector spend, call, SMS, or calendar action without explicit approval.

## Phase 5: Produce The SDR Package

Write output to:

```text
workspace/sdr-operator/<package-slug>/
```

Required files:

```text
_brief.md
_lead-source-plan.md
_icp-scorecard.md
_account-scoring-model.md
_research-workflows.md
connector-plan.md
connector-action-contracts.md
approval-plan.md
approval-queue-template.csv
loop-state-model.md
loop-events-and-transitions.md
compliance-matrix.md
run-ledger-template.json
memory-ledger.md
daily-briefing-template.md
test-cohort-plan.md
lead-ledger-template.csv
account-dossier-template.md
sequence-brief.md
reply-triage.md
meeting-prep.md
follow-up-workflows.md
crm-handoff.md
data-handoff.md
sales-role-handoff.md
sdr-package.json
_data-sources.md
_data-gaps.md
_quality-report.md
_evaluation-report.md
```

For outbound copy, create `sequence-brief.md` and then invoke `/kai-cold-outreach` to produce email touches. Do not hand off raw rows to the copy step until each row has source, suppression, relevance, and sender fields.

## Lead Ledger Schema

Use these minimum columns in `lead-ledger-template.csv`:

```text
account_id,company,website,industry,geo,company_size,source_name,source_url,source_retrieved_at,fit_score,intent_signal,trigger_event,problem_evidence,contact_name,contact_role,contact_channel,personalization_note,personalization_source,confidence,suppression_status,consent_basis,next_action,owner,status
```

Use `confidence` values: `high`, `medium`, `hypothesis`, `blocked`.

Use `status` values: `sourced`, `enriched`, `approved_for_copy`, `queued`, `sent`, `replied`, `meeting_booked`, `disqualified`, `suppressed`, `blocked`.

## Scoring Model

Score accounts from 0-100:

- Fit: 40 points for industry, size, geography, budget, and use case match.
- Timing: 20 points for trigger events such as hiring, funding, expansion, new regulation, new location, tech migration, or active demand.
- Pain evidence: 20 points for public proof, owned data, CRM notes, reviews, job posts, pages, or user-provided research.
- Reachability: 10 points for valid business contact path and routing clarity.
- Compliance confidence: 10 points for lawful source, suppression clear, and no sensitive-data concerns.

Block accounts with missing source, missing suppression check, sensitive personal data, prior opt-out, disallowed source, or unsupported claim dependency.

## Operating Loop

Write `loop-state-model.md`, `memory-ledger.md`, and `sdr-package.json` so the SDR motion can run repeatedly. Include:

- Package mode, retrieval dates, and data mode.
- Counts by ledger status.
- Source inventory and source gaps.
- Account and contact state transitions.
- Approval state for every live action.
- Reply categories, objections, referrals, and booked meetings.
- Source-quality, trigger-quality, message-quality, and meeting-quality memory.
- Quality gates, blockers, and next actions.

Do not invent reply rates, meeting rates, benchmarks, TAM, revenue, or conversion numbers. Use real data, user-provided targets, or mark the field as a data gap.

## Specialist Skills

Use the specialist skills inside the loop:

- `/kai-sdr-reply-triage` after any reply, bounce, opt-out, referral, objection, or interested response.
- `/kai-sales-meeting-prep` after a meeting is booked or after call notes/transcripts arrive.

Each specialist writes outputs back to the same package folder and updates the memory ledger. Do not let either specialist mutate live CRM, sequencer, calendar, SMS, phone, or email systems without approval.

## Quality Gates

Before handoff:

1. Run `python scripts/quality_gates/banned_word_check.py --file <file>` against every customer-facing markdown file.
2. Run `python scripts/quality_gates/four_us_score.py --file <file>` on `sequence-brief.md`, `_brief.md`, and any produced outreach copy. Minimum score: 10/16 for outreach, 12/16 for strategic package docs.
3. Apply `harness/skill-contracts/sdr-package.yaml` checks manually if no runner exists.
4. Apply `harness/skill-contracts/cold-email.yaml` before any email copy is approved.
5. Apply `harness/skill-contracts/sdr-reply-triage.yaml` before reply actions are approved.
6. Apply `harness/skill-contracts/sales-meeting-prep.yaml` before meeting prep or follow-up is handed to sales.
7. Confirm no quantitative or client-facing claim lacks a source, retrieval date, or data-gap note.
8. Confirm no live action was taken without approval.

## Output Summary

Final response should include:

- Package path.
- Package mode.
- What was produced.
- Any blocked sources or missing data.
- Whether `/kai-cold-outreach`, `/kai-sdr-reply-triage`, or `/kai-sales-meeting-prep` should run next.
