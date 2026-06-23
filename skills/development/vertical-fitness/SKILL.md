---
name: vertical-fitness
description: Domain-knowledge pack for fitness & wellness (boutique studios, gyms, coaches, on-demand brands) — the membership vocabulary, non-obvious billing/booking rules, and retention realities a builder must know so fitness products aren't speced naive. Covers the four products this niche ships (class-booking, coaching, churn-prevention, on-demand-video), how they wedge against Mindbody / PushPress / Zen Planner / Wodify / WellnessLiving, and the must-model entities (membership with freeze, recurring class template, waitlist, no-show policy, access tier). Applied by architect/pm during spec authoring so the schema and flows reflect how a studio actually bills and books, not a generic CRUD app.
when_to_use: |
  Apply when architect/pm specs a fitness/wellness product:
  - architect writes ARCH-*.md for a class-booking / coaching / churn-prevention / on-demand-video product in the fitness niche
  - pm decomposes any of those four products into tasks and needs the domain rules to not under-scope (billing + waitlist are where naive specs fail)
  - design-advisor wireframes a member-facing booking flow or a studio-owner dashboard
  Do NOT apply for non-membership verticals (the entity model here assumes recurring billing, class capacity, and attendance-driven retention).
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Fitness & wellness — spec it like a studio bills and books

Boutique studios, gyms, coaches, on-demand brands. Members on recurring
plans, classes with finite capacity, retention won or lost on attendance.
A builder who models this as "events + tickets" ships something no studio
owner will run their business on — because the hard parts are *billing*
and *waitlists*, not the calendar. This skill is the domain briefing so
the spec is right before code starts.

## 1. Domain vocabulary (know these or look naive)

- **Class pack vs unlimited membership vs drop-in** — three distinct
  products. A **pack** is N prepaid classes that decrement (10-class pack);
  an **unlimited membership** is a recurring plan (often monthly auto-renew)
  with no per-class deduction; a **drop-in** is a single paid visit. The
  schema must hold all three, not collapse them into "credits".
- **Recurring billing / auto-renew** — memberships rebill on a cycle
  (monthly is the norm) until cancelled. This is the revenue engine and the
  hardest thing to get right (see §2).
- **Waitlist** — a full class has an ordered queue; when a spot opens
  (someone late-cancels), the system **auto-promotes** the next person and
  notifies them. Core, not optional.
- **Late-cancel / no-show fee** — cancelling inside the policy window
  (e.g. <12h) or not showing forfeits the class (pack decrements) or charges
  a fee. The policy *is* the booking discipline.
- **Class capacity** — every class has a hard cap (bikes, mats, reformers).
  Booking beyond cap goes to the waitlist, never overbooks.
- **Recurring class schedule** — classes are templates ("Mon/Wed/Fri 6am
  Spin") that generate dated instances, with per-instance overrides
  (holiday cancel, sub instructor). Not a list of one-off events.
- **Check-in** — marking a member present at class; drives attendance
  history, which drives churn signals and pack decrement.
- **Freeze / hold** — a member pauses a membership (travel, injury) without
  cancelling; billing suspends, the plan resumes later. Expected feature.
- **MRR / churn rate / LTV** — monthly recurring revenue, the % of members
  who cancel per month, and lifetime value. The owner's scoreboard.
- **Punch card** — a physical-metaphor pack (10 punches); same model as a
  class pack with a remaining balance.
- **Family / household account** — one billing account, multiple members
  (parent + kids, couples); shared or separate balances.
- **Mindbody discovery marketplace** — Mindbody's consumer app where users
  *find and book* studios. Listing there is a customer-acquisition channel,
  not just software — see §2 and §5.

## 2. Non-obvious domain rules (what makes this vertical specific)

- **Billing is the hard part, not booking.** Packs that decrement,
  memberships that auto-renew, **freezes/holds** that suspend billing,
  **proration** on mid-cycle plan changes, and failed-payment retry/dunning
  are where naive specs collapse. Design the membership/pack/freeze model
  first; the calendar is the easy half.
- **No-show / late-cancel fees + waitlist promotion are core booking
  logic.** A cancel inside the window triggers a fee *and* frees a spot that
  must **auto-promote** the next waitlisted member with a notification. The
  two rules are coupled — model them together.
- **Recurring class schedules generate per-instance bookings.** Members
  book a *specific dated instance* ("this Friday's 6am"), but the schedule
  is a recurring template with exceptions. Booking, capacity, and waitlist
  all attach to the instance, not the template.
- **Class capacity + waitlist auto-promote is the heart of booking.** Cap is
  hard; overflow queues; promotion is automatic and time-sensitive (a spot
  freed 2h before class should offer to the waitlist immediately).
- **Mindbody's moat is the consumer discovery app — displacing it is a real
  trade-off.** Replacing Mindbody as the studio's software is easy
  software-wise, but a studio that delists loses Mindbody's marketplace as a
  lead source. **Surface this trade-off in the spec** (see §5) — don't
  silently assume displacement is free.

## 3. What a naive build gets wrong

- ❌ **Membership without freeze/hold + proration.** Modeling a plan as a
  flat recurring charge with no pause and no mid-cycle math. Members travel
  and get injured; owners offer holds. No freeze = cancellations instead of
  pauses = churn the product *caused*.
- ❌ **No waitlist auto-promotion.** A waitlist that's just a list nobody
  acts on. The value is the *automatic* promote-and-notify when a spot
  frees; without it the feature is theatre.
- ❌ **Ignoring no-show / late-cancel policy.** Free cancellation anytime
  wrecks class economics (members hoard spots they won't use). The fee/
  forfeit window is load-bearing booking logic.
- ❌ **Class schedule as one-off events.** Hand-creating every class instead
  of a recurring template with exceptions. Unmaintainable, and it breaks the
  moment an owner cancels one holiday occurrence.
- ❌ **Churn-prevention with no real at-risk signal.** "Members who haven't
  paid" is too late. The real leading signal is an **attendance drop** (was
  coming 3×/wk, now 0× for 2 weeks) — that's where win-back must fire,
  before the cancel.

## 4. Must-model entities / fields (beyond generic CRUD)

Schema hints — keep these migration-friendly (see [[migration-ready-schema]]):

- **Membership / ClassPack** — `type` (pack | unlimited | drop-in),
  `remaining_balance` (packs), `billing_interval` + `auto_renew` + `price`
  (memberships), `freeze_state {active, frozen_until}`, `start/end`, linked
  account. Freeze suspends billing; proration on plan change.
- **RecurringClass** (template) — `cadence` (days/times), `instructor`,
  `capacity`, `service_type`; generates **ClassInstance** rows.
- **ClassInstance** — dated occurrence of a template; `start`, `capacity`,
  `instructor` (sub override), `cancelled` flag; bookings attach here.
- **Booking** — member ↔ ClassInstance; `status` (booked → checked_in |
  late_cancel | no_show), `pack_decremented`, `fee_charged`.
- **Waitlist** — ordered queue per ClassInstance; `position`,
  `auto_promote` action that converts to a Booking + notification.
- **NoShowPolicy** — `cancel_window` (e.g. 12h), `late_cancel_fee`,
  `no_show_fee`, pack-forfeit rule; referenced at booking time.
- **Member** — profile + **attendance history** (the churn signal:
  visits/week trend), household links, consent flags.
- **AccessTier** — for on-demand-video: which content a plan unlocks
  (free / member / premium), gating the streaming library.

## 5. Per-product notes (wedge + the one thing to get right)

- **class-booking** (booking) — sell memberships/packs, members book classes
  with waitlists. *Wedge:* Mindbody is $99–599/mo and bloated for a single
  studio; a clean booking + membership system a small studio actually runs
  is the wedge. *Must get right:* the coupled **capacity → waitlist →
  auto-promote** loop and the **no-show/late-cancel policy**, on top of a
  real membership/pack/**freeze** billing model. **Trade-off to surface:**
  displacing Mindbody as the studio's software also drops the studio off
  Mindbody's **consumer discovery marketplace** — a lead-gen channel lost.
  Name it in the spec; don't assume the switch is free.
- **coaching** (content) — deliver programs, plans, habit tracking. *Wedge:*
  give coaches a structured program-delivery surface instead of PDFs and
  spreadsheets. *Must get right:* programs as **structured plans** (weeks →
  sessions → exercises) with member **habit/adherence tracking**, not a file
  dump — adherence data also feeds the churn signal.
- **churn-prevention** (crm) — spot at-risk members, win them back before
  cancel. *Wedge:* automate the retention save that owners do by gut.
  *Must get right:* a **real at-risk signal driven by attendance drop**
  (not by failed payment, which is too late), firing a win-back sequence;
  message mechanics deferred to [[lifecycle-messaging]].
- **on-demand-video** (content) — streaming library with access tiers.
  *Wedge:* **net-new revenue, no displacement risk** — a studio can launch
  this alongside whatever booking software it already runs, so it's the
  safest first product. *Must get right:* **AccessTier** gating (free /
  member / premium) so the library unlocks correctly per plan.

## 6. Compliance / regulatory touchpoints (light — pointers, not full treatments)

- **Recurring-billing / auto-renew law** — auto-renew memberships are
  regulated: clear renewal disclosure at signup, and several US states
  (e.g. CA's ARL) mandate an **easy online cancellation** path. Model
  `auto_renew` with a self-serve cancel; don't make cancellation a phone
  call. Defer PCI scope / processor design to the billing layer — the spec
  needs the renewal + cancel fields, not the gateway.
- **Liability waivers** — studios require a signed waiver before first
  class. Let Member carry a `waiver_signed_at` reference field so a build
  can gate booking on it; don't model the legal doc itself.
- **SMS consent (reminders / win-back)** — booking reminders and win-back
  are SMS/email; consent, STOP/HELP, and quiet hours apply. Defer all
  messaging infra and consent design to [[lifecycle-messaging]] — just flag
  that reminders exist so it's speced in, not bolted on.
- **Health-data sensitivity (light)** — fitness/attendance/habit data is
  *not* HIPAA PHI for a studio, so don't over-engineer a compliance regime.
  But it's personal and sensitive (injuries, body metrics in coaching) —
  keep it access-controlled and out of analytics by default. Light touch,
  not a regulated build.

## Output

When applied, the architect/pm carries these into ARCH-*.md / PLAN-*.md:
the membership/pack/**freeze** billing model, the **capacity → waitlist →
auto-promote** booking loop, the **no-show/late-cancel** policy, the
recurring-class template + per-instance booking, the **attendance-drop**
churn signal, and the on-demand **AccessTier** gating — plus the explicit
**Mindbody discovery-channel trade-off** for class-booking. Cross-reference
[[lifecycle-messaging]] (reminders / win-back), [[migration-ready-schema]]
(a Mindbody export must **preserve pass/pack balances** and membership
state on import), and [[vertical-onboarding]] rather than re-deriving them.
