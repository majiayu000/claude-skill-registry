---
name: vertical-construction
description: Domain knowledge for the construction vertical (contractors, field crews) so architect and pm don't spec construction products naively. Covers the vocabulary (bid vs estimate, takeoff, retainage, change order, AIA G702/G703, lien waiver, draw schedule), the non-obvious money rules that incumbents like Procore price out of reach for small contractors, what a naive build gets wrong (no assemblies, ignored retainage, ungated sub payments), and the entities that must be modelled. Applied by architect when writing ARCH-{slug}.md and by pm when writing PLAN-{slug}.md for any of the four construction products (bid-builder, project-mgmt, subcontractor-portal, field-docs).
when_to_use: |
  Apply when:
  - architect writes ARCH-{slug}.md for a construction product (bid-builder,
    project-mgmt, subcontractor-portal, field-docs)
  - pm decomposes a construction feature into PLAN-{slug}.md tasks
  - design-advisor wireframes a construction screen (estimate, billing, sub payment, daily log)
  - any spec touches money flow (billing, payment, retainage) in the construction vertical
  Do NOT apply to non-construction verticals — the money rules (retainage, lien waivers,
  AIA pay apps) are construction-specific and will mislead elsewhere.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Vertical: construction — don't spec it naive

Construction has its own money physics. A spec that treats a contractor's billing like a
SaaS invoice will ship something no contractor can use, because the cash flow it ignores
(retainage held back, draws against a schedule of values, subs gated on lien waivers) is
*the* thing the contractor is trying to manage. This skill gives architect and pm the
vocabulary and the non-obvious rules so the four construction products are specced from
domain reality, not intuition.

The four products and their incumbents:

| Product | Archetype | Wedge against |
|---|---|---|
| bid-builder | marketplace-lite | Excel (small contractors estimate in spreadsheets) |
| project-mgmt | crud | Buildertrend, Contractor Foreman |
| subcontractor-portal | marketplace-lite | Procore, manual COI/payment tracking |
| field-docs | crud | Procore field tools, paper daily reports |

Incumbents: **Procore** (enterprise, ~$375+/mo minimum — too expensive and heavy for small
contractors; do not fight it head-on), **Buildertrend** (residential-focused),
**Contractor Foreman**, **Autodesk Construction Cloud** (enterprise). The opening is small
contractors priced and complexity'd out of these.

## Domain vocabulary (use these terms exactly in specs)

- **Estimate** — internal cost calculation (what the job will cost the contractor).
  **Bid** — the priced number submitted to win the job (estimate + markup). **Proposal** —
  the customer-facing document wrapping the bid with scope, terms, exclusions. *Estimate →
  bid → proposal* are three artifacts, not synonyms.
- **Takeoff (quantity takeoff)** — counting/measuring quantities from plans (sq ft of
  drywall, linear ft of pipe) that feed the estimate. Garbage takeoff = garbage bid.
- **Unit cost + assembly** — an estimate is built from line items priced per unit (e.g.
  $/sq ft). An **assembly** bundles several unit-cost items into one (a "door assembly" =
  door + frame + hardware + labor). Real estimating is assemblies, not freehand numbers.
- **Markup vs margin** — markup is added *on top of* cost (cost × 1.20). Margin is the cut
  *of the bid price* (price − cost) / price. 20% markup ≠ 20% margin. Mixing them mis-prices
  the job. Spec which one a field means.
- **Change order (CO)** — a contracted change to scope/price after the bid is signed.
  Untracked COs are where margin leaks and disputes start.
- **RFI (request for information)** — formal question to the architect/owner about ambiguous
  plans; the answer can change scope (→ change order).
- **Submittal** — contractor's proposed material/product samples sent for approval before
  install.
- **Draw schedule + progress billing** — payment isn't lump-sum. The contractor bills in
  **draws** as work completes, against a **schedule of values** (the job broken into line
  items each with a contract value); each billing claims a % complete per line.
- **Retainage / retention** — the owner withholds a slice (typically **5–10%**) of each
  payment until the job is complete/accepted. It is owed money the contractor can't touch
  yet — a first-class concept, not a discount.
- **Lien / lien waiver** — a mechanic's lien is a legal claim against the property for
  unpaid work; a **lien waiver** is the sub/supplier signing away that right in exchange for
  payment. Conditional (on payment clearing) vs unconditional (already paid).
- **AIA G702/G703** — the industry-standard pay-application forms. G702 is the summary
  (application + certificate for payment); G703 is the continuation sheet (the schedule of
  values with this-period / to-date / retainage columns). Many owners require these exact
  forms.
- **1099 subcontractor** — subs are typically 1099 contractors, not employees; the GC must
  collect a W-9 and issue a 1099 for tax reporting.
- **COI (certificate of insurance)** — proof a sub carries required insurance; must be
  current (not expired) before the sub works or gets paid.
- **Daily log** — the dated field record (crew on site, work done, weather, deliveries,
  delays). It is **legal/dispute evidence**, not a status update.
- **Punch list** — the end-of-job list of defects/incomplete items to fix before final
  payment / retainage release.
- **Schedule of values (SOV)** — the contract sum allocated across work items; the
  backbone of progress billing and G703.

## Non-obvious domain rules (the ones that trip a naive spec)

1. **Procore is enterprise and expensive.** Don't out-feature it for small contractors —
   undercut on price and simplicity. The wedge is "good enough, cheap, no onboarding consultant."
2. **Small contractors estimate in Excel.** bid-builder's wedge is replacing the spreadsheet
   with *real* estimate math (unit costs + assemblies + markup). It's revenue-adjacent and
   low-switching — the easiest first sale.
3. **Retainage is core, not an edge case.** 5–10% withheld until completion changes every
   billing number. A billing model that doesn't carry a retainage column is wrong.
4. **Progress billing runs through the schedule of values.** You bill % complete per SOV
   line, not a flat invoice. Model the SOV first; billing falls out of it.
5. **Subs are gated on documents before payment.** A sub can't be paid until COI is current
   and the lien waiver for the period is signed. Payment without that gate is a real-money
   liability for the GC.
6. **Untracked change orders eat margin and cause disputes.** Every CO must adjust the
   contract sum and the SOV, with a signature trail.
7. **Daily logs are dispute evidence.** Photo + timestamp + weather + crew make them hold up;
   a free-text note that "we worked today" does not.

## What a naive build gets wrong

- Estimating as a flat list of typed-in dollar amounts — **no unit costs, no assemblies, no
  markup/margin distinction**. Result: numbers nobody can defend or reuse.
- **Billing that ignores retainage** — invoices the full amount, so the contractor's books
  don't match what the owner actually pays.
- **project-mgmt that ignores the draw schedule / progress billing** — a generic task board
  that never connects to how money actually arrives.
- **Subcontractor payment with no lien-waiver / COI gate** — pays subs without the documents
  that protect the GC from liens and uninsured-work liability.
- **No change-order flow** — scope changes live in email; margin leaks; disputes have no
  paper trail.
- **Daily logs without photo + timestamp + weather** — useless as evidence when a delay or
  defect claim arrives.

## Must-model entities

Hand these to the data model in ARCH (and apply [[migration-ready-schema]] — contractors
bring their job list and customer list from the incumbent).

- **Estimate** — line items with `unit_cost`, quantity, and **assemblies**; carries a
  **markup** (and derived margin) → produces a **Bid**.
- **Bid / Proposal** — the priced submission; references the Estimate it came from.
- **ChangeOrder** — adjusts contract sum + SOV; has status + signature trail; linked to the
  Project.
- **Subcontractor** — its own entity (not an inline field) with **COI status + expiry**,
  **lien-waiver status** (the payment gate), and **1099 / W-9** info.
- **Project** — carries a **Schedule of Values**, a **draw schedule**, and a **retainage**
  percentage/balance.
- **DailyLog** — photos, weather, crew, timestamp; append-only enough to serve as evidence.

Money in integer minor units (`*_cents`); retainage and SOV math must not float-drift.

## Per-product notes

- **bid-builder (marketplace-lite)** — Wedge: revenue-adjacent, low-switching replacement for
  the estimating spreadsheet. The one domain thing: **real estimate math** — unit costs +
  assemblies + the markup/margin distinction producing a defensible bid. Get this wrong and
  it's just a worse Excel.
- **project-mgmt (crud)** — Wedge: lightweight project + daily-log tool vs heavy
  Buildertrend/Contractor Foreman. The one domain thing: **draw schedule / progress billing
  off the schedule of values** — don't ship a generic task board disconnected from billing.
- **subcontractor-portal (marketplace-lite)** — Wedge: manage subs, docs, and payments
  without Procore. The one domain thing: **lien-waiver + COI gating before payment** — the
  portal's whole value is that a sub can't be paid until the documents are clean.
- **field-docs (crud)** — Wedge: photo/daily-report/inspection capture vs paper and Procore's
  field module. The one domain thing: **photo + timestamp + weather + crew on every entry**
  so the record is dispute-grade evidence.

## Compliance (light — flag, don't gold-plate)

- **Lien law is state-specific** — preliminary notice deadlines and lien-waiver forms vary by
  state; treat waiver forms as state-configurable, not hardcoded.
- **Retainage law** — many states cap the retainage % and regulate timing of release; surface
  it as a setting.
- **1099 for subs** — collect W-9, track payments, support 1099 reporting.
- **Prevailing wage** — on public/government projects (Davis-Bacon), wage rates are mandated
  and certified payroll is required; flag if the product targets public work.
- **COI verification** — verify current (non-expired) coverage before sub work/payment.
- **OSHA** — relevant to field-docs (safety inspections, incident records) but keep light.

These pair with [[vertical-onboarding]] (importing the contractor's existing jobs, subs, and
customers as the low-switching wedge) and [[lifecycle-messaging]] (COI-expiry reminders,
lien-waiver requests, draw/payment notifications — the messages that make the money flow run).
