---
name: vertical-home-services
description: Domain-knowledge pack for home & field services (HVAC, plumbing, cleaning, landscaping) — the trades vocabulary, non-obvious pricing/dispatch rules, and field-crew realities a builder must know so home-services products aren't speced naive. Covers the four products this niche ships (dispatch, quoting, field-booking, reviews), how they wedge against ServiceTitan / Jobber / Housecall Pro, and the must-model entities (price book, membership, job window, multi-option quote). Applied by architect/pm during spec authoring so the schema and flows reflect how a trades shop actually runs, not a generic CRUD app.
when_to_use: |
  Apply when architect/pm specs a home-services product:
  - architect writes ARCH-*.md for a dispatch / quoting / field-booking / reviews product in the home-services niche
  - pm decomposes any of those four products into tasks and needs the domain rules to not under-scope
  - design-advisor wireframes a tech-facing or homeowner-facing flow for a trades shop
  Do NOT apply for non-field verticals (the entity model here assumes crews, trucks, and on-site jobs).
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Home & field services — spec it like a trades shop runs

HVAC, plumbing, cleaning, landscaping. A crew of techs in trucks, jobs on
site, money quoted at the kitchen table. A builder who models this as
"appointments + invoices" ships something no contractor will use. This
skill is the domain briefing so the spec is right before code starts.

## 1. Domain vocabulary (know these or look naive)

- **Price book** — the master catalog of priced tasks ("replace 40-gal
  water heater = $1,850"). Pricing is *looked up*, not computed hourly.
- **Flat-rate vs T&M** — flat-rate (one price from the price book, parts +
  labor bundled) is the norm in the trades. Time & materials (T&M, billed
  by the hour + parts) is the exception, used for diagnostics or open-ended
  jobs. Build for flat-rate first.
- **Dispatch board** — the live grid of techs × time slots the office uses
  to assign and re-shuffle jobs through the day.
- **Truck roll** — sending a tech to a site. Every truck roll has a real
  cost; minimizing wasted rolls is the whole game.
- **First-time fix rate** — % of jobs completed on the first visit. The
  north-star ops metric. Low fix rate = repeat rolls = lost margin.
- **Callback** — a return visit because the first fix failed. Tracked and
  hated; ties to warranty.
- **Membership / service agreement** — recurring plan (e.g. 2 tune-ups/yr
  for $19/mo) that creates predictable revenue and priority booking. A core
  business model, not a loyalty gimmick.
- **Good-better-best** — the quote presents 3 priced options (e.g. patch /
  replace / replace-with-upgrade). Standard sales technique; lifts ticket.
- **Dispatch fee / trip charge** — flat fee just to show up, often waived
  if the job is booked.
- **After-hours / emergency rate** — premium pricing for nights, weekends,
  holidays. Same price book, different multiplier.
- **GPS / route** — tech locations and optimized drive order; drives the
  "tech is 12 min away" customer text.
- **Parts markup** — parts billed above cost (often 2–3×); a margin lever,
  must be representable per line.

## 2. Non-obvious domain rules (what makes this vertical specific)

- **Pricing is a lookup, not arithmetic.** The price comes off the price
  book at a flat rate. Hourly math is the rare path, not the default.
- **The quote IS the sales tool.** It's presented on site, often on a
  tablet, and closed on the spot — interactive, branded, good-better-best,
  accept-and-pay. It is not a PDF emailed for later.
- **Techs work offline.** Basements, mechanical rooms, rural sites — no
  signal. The field app must capture work, photos, and signatures offline
  and sync later. This is a hard requirement, not a nice-to-have.
- **Same-day dispatch is normal.** Jobs get created, assigned, and
  re-shuffled within the same day; the board is a live, mutable thing.
- **Demand is seasonal and spiky.** HVAC floods on the first heat wave /
  cold snap; landscaping is spring-loaded. Capacity and booking must absorb
  surge, not assume even flow.
- **Appointments are windows, not instants.** Customers get "8am–12pm",
  not "8:00". Model an arrival window plus narrowing ("tech en route").
- **Recurring is first-class.** Memberships, maintenance plans, seasonal
  visits — the schema has to express recurrence and renewal natively.

## 3. What a naive build gets wrong

- ❌ **Hourly pricing.** Modeling jobs as hours × rate. The trades quote
  flat-rate off a price book; hourly is the edge case. Get this wrong and
  the product is unsellable.
- ❌ **No offline mode.** Assuming the tech has signal. The most common
  job site is a basement. An online-only field app fails on day one.
- ❌ **Quote as static PDF.** A read-only document instead of an
  interactive accept-to-pay surface with selectable options and a deposit
  button. The quote must *close the sale*, not describe it.
- ❌ **No good-better-best.** A single price with no upsell tiers. Leaves
  margin on the table and feels foreign to anyone who's bought HVAC.
- ❌ **No membership / recurring model.** Treating every job as one-off.
  Misses the predictable-revenue engine the whole business runs on.
- ❌ **Instant appointments.** Booking a 9:00 slot when the trade works in
  windows. Sets a customer expectation the crew can't meet.

## 4. Must-model entities / fields (beyond generic CRUD)

Schema hints — keep these migration-friendly (see [[migration-ready-schema]]):

- **PriceBookItem** — `code`, `name`, `category`, `flat_rate`, `cost`,
  `parts_markup`, and tier prices `{good, better, best}`; `is_recurring`
  flag for membership-eligible items. T&M items carry an hourly rate as
  the exception path.
- **Membership / ServiceAgreement** — `plan`, `cadence` (e.g. 2/yr),
  `price`, `billing_interval`, `renewal_date`, `priority_flag`, linked
  customer; generates scheduled visits.
- **Job** — `status` (scheduled → dispatched → en_route → on_site →
  complete → callback), `assigned_tech`, `arrival_window {start,end}`,
  `address`, `is_after_hours`, `first_time_fix` flag, parent membership if
  recurring.
- **Quote** — array of `options[]` (good/better/best), each with line
  items off the price book; `selected_option`, `deposit_amount`,
  `deposit_paid`, `accepted_at`, branding; an accept action that converts
  to a Job.
- **Tech / Crew** — skills/licenses held, home base, working hours,
  current GPS, capacity.

## 5. Per-product notes (wedge + the one thing to get right)

- **dispatch** (crud) — assign jobs to techs, optimize routes, live status
  board. *Wedge:* ServiceTitan is ~$300+/tech and enterprise-heavy; the
  wedge is a clean same-day board a 3–8 truck shop can actually run without
  an implementation consultant. *Must get right:* the board is **live and
  mutable** — jobs re-assign and re-window mid-day, with arrival windows
  (not instants) and tech status driving the customer "on the way" text.
- **quoting** (marketplace-lite) — photo/form → priced branded quote →
  accept + pay deposit. *Wedge:* vs Jobber/Housecall, lean into the
  **interactive accept-to-pay** quote that closes on site. *Must get
  right:* good-better-best options priced off the **price book**, with a
  deposit step — the quote is the sales tool, not a PDF.
- **field-booking** (booking) — customer self-books a slot, gets
  reminders/confirmations. *Wedge:* incumbents bury self-booking; expose a
  dead-simple homeowner booking page. *Must get right:* book into an
  **arrival window** against real crew capacity, then drive reminders and
  confirmations (consent + timing deferred to [[lifecycle-messaging]]).
- **reviews** (crm) — request/route/publish reviews after each job.
  *Wedge:* automate the post-job review ask that shops do by hand.
  *Must get right:* fire the request **on job completion** (tied to the
  first-time-fix outcome, not a blind blast), route happy → public
  platforms, unhappy → private recovery; SMS/email mechanics via
  [[lifecycle-messaging]].

## 6. Compliance / regulatory touchpoints (light — pointers, not full treatments)

- **Trade licensing & permits** — HVAC/plumbing/electrical work is
  licensed and often permit-pulled per jurisdiction. Don't model trade
  qualification; *do* let a Job/Tech carry a license/permit reference field
  so a regulated build can extend it.
- **TCPA (SMS reminders)** — booking confirmations/reminders are SMS;
  consent, STOP/HELP, and quiet hours apply. Defer all messaging infra and
  consent design to [[lifecycle-messaging]] — just flag that reminders
  exist so it's speced in, not bolted on.
- **Deposits / payments** — quotes take a deposit and jobs collect
  payment. Defer PCI scope, idempotency, and refund/dispute flow to the
  billing/payments layer — the spec only needs the `deposit_amount` /
  `deposit_paid` fields, not the processor design.

## Output

When applied, the architect/pm carries these into ARCH-*.md / PLAN-*.md:
the price-book-flat-rate pricing model, the offline field requirement, the
window-based scheduling, the multi-option accept-to-pay quote, and the
membership/recurring entity — and cross-references [[lifecycle-messaging]],
[[migration-ready-schema]], and [[vertical-onboarding]] rather than
re-deriving them.
