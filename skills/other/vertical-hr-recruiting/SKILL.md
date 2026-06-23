---
name: vertical-hr-recruiting
description: Domain-knowledge primer for the HR & recruiting vertical (ATS, onboarding, workforce scheduling, engagement). Applied by architect/pm during spec authoring so they aren't naive about hiring pipelines, the admitted offer→onboard data-carry gap, EEO/I-9 compliance, and shift-coverage rules. Stops the four products from being specced as generic CRUD when the domain has hard legal and workflow constraints.
when_to_use: |
  Apply when:
  - architect writes ARCH-*.md for ats / onboarding / workforce-scheduling / engagement
  - pm decomposes any of these four products into tasks and needs domain entities
  - a spec touches candidates, requisitions, offers, I-9, shifts, or EEO data
  Do NOT apply for products outside the HR/recruiting vertical.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Vertical: HR & recruiting — don't spec it naive

The incumbents (Workable, BambooHR, Greenhouse, Lever, Zoho Recruit, Manatal) have
trained buyers to expect a hiring pipeline that *works*. A generic CRUD app fails the
moment it meets EEO law, I-9 timing, or the offer→onboard handoff. **Read this before
speccing any of the four products — the domain has hard constraints, not just forms.**

## 1. Domain vocabulary

- **ATS** — applicant tracking system; the system of record for hiring.
- **Requisition (req)** — an approved open role. Hiring happens *against a req*, not in a
  vacuum. Reqs have an approval workflow (hiring manager → finance/HR).
- **Pipeline stages** — `applied → screen → interview → offer → hired` (plus `rejected` /
  `withdrawn`). Stages are **configurable per req** — engineering and sales hire differently.
- **Candidate vs applicant** — an *applicant* applied to a specific req; a *candidate* is a
  person in your talent pool who may map to many applications over time. Don't conflate them.
- **Sourcing** — proactively finding candidates (vs inbound applications).
- **Structured interview + scorecard** — pre-defined questions + a rubric each interviewer
  scores. Reduces bias and legal exposure vs freeform notes.
- **Offer letter** — formal terms; triggers the offer→onboard transition on acceptance.
- **EEO data** — voluntary race/gender/veteran/disability self-ID, collected for
  reporting, **segregated from hiring decisions** (see §2).
- **I-9 + E-Verify** — employment eligibility verification; **strict 3-day timing** (§2).
- **Onboarding checklist** — tasks a new hire/employer must complete before/at start.
- **time-to-hire / time-to-fill** — core recruiting metrics (hire = offer accepted by a
  candidate; fill = req closed). Different denominators; report both correctly.
- **Hourly vs salaried** — drives scheduling, overtime (FLSA), and pay rules.
- **Shift swap / coverage** — hourly workers trade shifts; coverage rules say a slot can't
  go unstaffed below a threshold.
- **eNPS** — employee Net Promoter Score; the headline engagement-survey metric.

## 2. Non-obvious domain rules

- **The offer→onboard handoff is the admitted gap.** Incumbents openly concede onboarding
  is unsolved: data gets *re-entered* between the ATS and the HR/onboarding system. The
  whole onboarding product wedge is **carry the candidate's data forward — zero re-entry.**
- **EEO/OFCCP data must be collected but kept OUT of the hiring-decision view.** Mixing
  self-identified race/gender into the screen/interview UI is an anti-discrimination
  liability. Store it segregated; surface it only in aggregate compliance reports.
- **Structured scorecards reduce bias and legal risk.** They create a defensible,
  consistent record. Freeform-only interview notes are a disparate-impact landmine.
- **I-9 has strict timing**: Section 1 by the employee's first day, Section 2 (employer
  review of documents) **within 3 business days of start.** Onboarding tasks tied to I-9
  carry a hard deadline, not a soft reminder.
- **Workforce scheduling needs coverage rules + labor compliance.** A schedule isn't valid
  just because slots are filled — it must respect minimum coverage, overtime (FLSA),
  predictive-scheduling / fair-workweek laws (advance-notice in some jurisdictions), and
  break rules.
- **Reqs gate hiring.** No offers without an approved req; req approval is a real workflow
  with a budget/headcount check, not a checkbox.

## 3. What a naive build gets wrong

- **Hardcoded pipeline stages.** A fixed `applied→hired` enum breaks the first time a
  customer wants a take-home or panel stage. Stages must be **configurable per req.**
- **EEO data in the candidate decision view.** Putting self-ID fields on the candidate card
  the hiring manager sees is a legal-risk bug, not a UX choice. Segregate it.
- **Onboarding that re-enters candidate data.** Rebuilding name/email/role/comp from
  scratch *is* the gap incumbents have. If onboarding starts from a blank form, you built
  the incumbent's weakness, not our wedge.
- **I-9 modeled as a generic checklist item.** Without the 3-business-day deadline and
  Section 1 / Section 2 split, it's non-compliant.
- **Scheduling as a calendar.** Drag-and-drop shifts with no coverage minimum, no overtime
  flag, and no swap-approval flow is a toy, not a workforce tool.

## 4. Must-model entities

| Entity | Must include | Why |
|---|---|---|
| **Requisition** | approval state, headcount, stage config | hiring is per-req; stages vary |
| **Candidate** | stage history, scorecards, EEO (segregated store) | audit trail + bias defense; EEO must not leak into decision view |
| **Offer → Onboarding** | carries candidate data forward (no re-entry) | this IS the wedge; the handoff is the gap |
| **OnboardingTask** | deadline field (I-9 3-day timing) | compliance is time-bound, not soft |
| **Shift** | coverage rules, overtime flag, swap/approval state | a schedule must be *valid*, not just full |

## 5. Per-product notes

| product | archetype | wedge | the one domain thing |
|---|---|---|---|
| **ats** | crud | crowded market — needs a sharp angle, not "another tracker" | configurable-per-req pipeline stages + structured scorecards; don't ship a generic Kanban |
| **onboarding** | crud | **the offer→onboard data-carry gap incumbents admit is unsolved** | carry candidate data forward with zero re-entry; I-9 tasks with 3-day deadlines |
| **workforce-scheduling** | booking | shift scheduling for hourly teams | coverage rules + overtime + swap/coverage approval, not a bare calendar |
| **engagement** | crm | engagement surveys for SMB | eNPS as the headline metric; anonymity threshold so small teams can't deanonymize responses |

`onboarding` is the differentiated bet (solve the admitted gap). `ats` is the crowded one
— architect must name the sharp angle in the ARCH doc or it's dead on arrival.

## 6. Compliance (light)

Flag these in the ARCH doc; route AI-screening to a reviewer.

- **EEO / OFCCP** — collect voluntary self-ID; aggregate reporting; **never** in the
  decision path.
- **I-9 / E-Verify** — Section 1 by day one, Section 2 within **3 business days**; model the
  deadline.
- **Anti-discrimination** — disparate impact in screening. **If any product uses AI to
  screen/rank candidates, flag it to `hr-ai-reviewer`** (or the AI-security reviewer) before
  senior-dev starts — automated screening is a high-risk surface.
- **Ban-the-box** — many jurisdictions forbid asking criminal history before an offer.
  Don't put it on the application form by default.
- **FLSA / overtime** — scheduling must compute overtime for hourly workers; respect
  fair-workweek / predictive-scheduling laws where they apply.
- **Data retention** — candidate/applicant records have minimum retention (e.g. EEOC
  ~1 year) and deletion obligations (GDPR/CCPA right-to-erasure). State a retention policy.

## Output

When applied, contribute a **Domain constraints** block to the architecture doc:

```
## Domain constraints (HR/recruiting)
- pipeline: stages configurable per req (not a fixed enum)
- EEO data: segregated store, excluded from decision view
- offer→onboard: candidate data carried forward, zero re-entry
- I-9: Section 2 deadline = start + 3 business days (modeled)
- scheduling: coverage rule = <min staffed>, overtime flag, swap-approval
- AI screening: <none | flagged to hr-ai-reviewer>
- retention: <policy + jurisdiction>
```

## Cross-references

- [[vertical-onboarding]] — the import-first onboarding funnel; the offer→onboard
  data-carry here *is* the import that feeds first-run for the onboarding product.
- [[migration-ready-schema]] — model Candidate/Offer/Onboarding so data carries forward
  cleanly (the no-re-entry wedge depends on it).
- [[lifecycle-messaging]] — candidate-stage and onboarding-task notifications (offer sent,
  I-9 due, shift posted, survey open).
