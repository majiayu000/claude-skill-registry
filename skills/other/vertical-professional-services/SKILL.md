---
name: vertical-professional-services
description: Domain-knowledge primer for the professional-services vertical (agencies, consulting firms, creative studios) so architect/pm don't spec naively against PSA incumbents (Scoro, Productive, Accelo, Ruddr, BigTime). Supplies the vocabulary, the non-obvious billing/margin rules, the entities a real proposal/portal/time/profitability product must model, and the per-product wedge. Applied by architect/pm during spec authoring for any of the four products in this vertical — proposals, client-portal, time-invoicing, profitability.
when_to_use: |
  Apply when:
  - architect is writing ARCH-*.md for a professional-services product
    (proposals, client-portal, time-invoicing, profitability)
  - pm is decomposing one of these into tasks and needs to model the
    domain entities (SOW, retainer, time entry, change order) correctly
  - any spec touches agency/consulting/studio billing, margin, or scope
  Do NOT apply for other verticals (home services, restaurants, etc.) —
  the billing economics here (utilization × realization) are specific.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Vertical: professional services — bill time, defend margin, sell the scope

Agencies, consulting firms, and creative studios sell hours and deliverables, not
units. Their economics are unintuitive: revenue can rise while margin collapses, and the
document that wins the work (the proposal/SOW) is also where margin leaks. Incumbents
(Scoro, Productive, Accelo, Ruddr, BigTime — collectively "PSA", professional-services
automation) model this correctly; a naive build does not. Spec against the real domain.

## 1. Domain vocabulary

- **SOW (statement of work)** — the binding scope: deliverables, timeline, price, terms.
  It IS the contract and the upsell surface.
- **Engagement types**: **project** (fixed scope/price), **retainer** (recurring
  fee for a capacity/hours bucket), **T&M** (time & materials — bill actuals).
- **Utilization rate** — billable hours ÷ available hours. The first lever of margin.
- **Realization rate** — billed amount ÷ standard value of hours worked (i.e. how much
  of what you *could* bill you actually invoiced and collected). The second lever.
- **Billable vs non-billable** — every time entry carries this flag; non-billable
  (admin, sales, rework) is pure cost.
- **WIP (work in progress)** — unbilled-but-delivered work; revenue earned, not yet
  invoiced. Agencies carry it for weeks.
- **Blended rate** — single effective $/hour across a mixed-seniority team on an
  engagement (vs per-person rate cards).
- **Change order** — a formal amendment when scope grows; the antidote to scope creep.
- **Milestone billing** — invoice tied to deliverable acceptance, not the calendar.
- **Scope creep** — uncompensated work beyond the SOW; the silent margin killer.
- **Gross margin per project** — (revenue − cost of delivered hours) ÷ revenue, *per
  engagement* — not company-wide, not revenue.
- **e-signature** — legally binding accept on the proposal (ESIGN/UETA, see §6).
- **Net-30 terms** — payment due 30 days after invoice; drives cash flow and reminders.

## 2. Non-obvious domain rules

- **The proposal/SOW is the contract AND the upsell.** It's not a marketing PDF — it's
  where price, scope, and acceptance live. Optional line items and tiers turn a quote
  into expansion revenue. Treat it as a revenue surface, not a document export.
- **Margin is utilization × realization, not revenue.** A firm can grow billings and
  lose money if people are busy on non-billable work or hours never get invoiced.
  Profitability must compute *margin per engagement*, never top-line revenue.
- **Retainers need burn-down tracking.** A retainer is a bucket of hours/fees that
  depletes through the month. Without burn-down you over-deliver (margin loss) or
  under-deliver (churn). Show consumed vs remaining, continuously.
- **Agencies live and die on scope creep + change orders.** The default human behavior
  is to "just do it" rather than raise a change order — which silently converts billable
  work into non-billable. The product must make raising a change order frictionless.
- **Time tracking is hated but is the source of truth for billing.** No time entry → no
  defensible invoice → realization drops. The constraint is *adoption*, not features.

## 3. What a naive build gets wrong

- **Proposal as a static PDF** instead of **accept-to-pay** — losing the e-sign +
  deposit/first-invoice moment where the deal actually closes and cash starts.
- **No change-order flow** — scope creep eats margin invisibly because over-delivery is
  never captured as a billable amendment.
- **Time entry so tedious nobody uses it** — a 12-field modal per entry kills adoption;
  with no entries, billing and profitability are both fiction. Timers + one-tap +
  defaults beat a perfect schema.
- **Profitability that shows revenue, not margin** — a dashboard of billings is
  vanity; the firm needs margin per project/retainer with cost-of-hours subtracted.
- **Ignoring retainer burn-down** — treating a retainer like a flat subscription
  instead of a depleting bucket misses the entire reason retainers are risky.

## 4. Must-model entities

Spec these explicitly; they recur across all four products. Build them
[[migration-ready-schema]] (stable external IDs, soft-delete, audit timestamps) because
agencies switch from incumbents mid-engagement and import open work.

- **SOW / Proposal** — header (client, engagement type, terms, net-N) + **line items**
  (description, qty, rate, optional/tiered flags) + **e-signature** state (sent → viewed
  → signed) + **accept-to-pay** link (deposit or first invoice on acceptance). Status
  machine: draft → sent → signed → active → closed.
- **Retainer** — period, committed hours/fee, **burn-down** (consumed vs remaining),
  rollover policy, renewal date.
- **TimeEntry** — who, project/task, duration, **billable flag**, **rate** (snapshot at
  entry time, not a live lookup), billed/unbilled (WIP) status.
- **Project** — budget (hours and/or fee), engagement type, rate card, computed
  **margin** (revenue − cost-of-delivered-hours), milestones.
- **ChangeOrder** — links to a Project/SOW, delta scope + delta price, its own
  e-sign/acceptance, and a reason — so scope growth becomes captured revenue.

## 5. Per-product notes (wedge vs incumbent + the one thing to nail)

- **proposals** (marketplace-lite) — **the wedge.** Revenue-adjacent and **low switching
  cost**: a firm can adopt it for the *next* proposal without migrating anything, and it
  touches money immediately. Incumbents bury proposals inside a heavy PSA suite. **Must
  nail: accept-to-pay** — e-sign that flows straight into a deposit/first invoice. See
  [[vertical-onboarding]]: first activation = first signed, paid proposal.
- **client-portal** (crud) — wedge: one clean client-facing surface for deliverables,
  approvals, status, and billing, vs incumbents' internal-ops focus. **Must nail:
  approvals as billing triggers** — an approved deliverable should be invoiceable
  (milestone billing), not just a checkbox.
- **time-invoicing** (crud) — wedge: timers → invoices → reminders with **no spreadsheet
  in between**; incumbents make time entry a chore. **Must nail: frictionless capture +
  rate snapshot** — adoption is the product; a wrong/stale rate corrupts every downstream
  invoice and the realization number.
- **profitability** (dashboard) — wedge: **real-time margin**, not month-end revenue
  reporting. **Must nail: margin = utilization × realization per engagement**, with
  cost-of-hours subtracted and retainer burn-down surfaced — not a billings chart.

## 6. Compliance (light)

Keep this proportionate — defer anything money-movement-shaped to the
subscription-billing-engineer.

- **e-signature validity** — ESIGN Act + UETA (US): capture intent-to-sign, consent to
  electronic records, an audit trail (timestamp, IP, signer identity), and a tamper-
  evident copy. For EU clients, eIDAS levels apply. This is what makes accept-to-pay
  legally binding.
- **Invoice / tax basics** — sequential invoice numbers, required fields, sales-tax/VAT
  where applicable. **Defer the engine** (tax calc, payment rails, dunning) to the
  subscription-billing-engineer; the architecture doc only needs the *contract* with it.
- **1099 for contractors** — agencies pay sub-contractors/freelancers; if the product
  touches contractor payouts, track payee tax info for 1099-NEC reporting (US). Note it;
  don't build a payroll system into a proposals tool.

## Output

When applied, contribute a **Domain model** note to the architecture doc capturing: the
engagement types in scope (project/retainer/T&M), the must-model entities above that this
product owns, the margin definition (utilization × realization, per engagement) if
profitability is in scope, and the e-sign/accept-to-pay contract if proposals is in scope.
