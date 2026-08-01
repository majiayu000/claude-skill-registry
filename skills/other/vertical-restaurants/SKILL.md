---
name: vertical-restaurants
description: "Domain-knowledge primer for the restaurants & hospitality vertical (dine-in, pickup, delivery). Gives architect and pm the vocabulary, non-obvious operating rules, must-model entities, and incumbent landscape so a restaurant-product spec isn't naive about modifiers, 86'd items, aggregator commissions, tip law, and razor-thin margins. Covers the 4 products: online-ordering, reservations, loyalty, shift-scheduling."
when_to_use: |
  Apply when speccing a restaurant / hospitality product:
  - architect writing ARCH-*.md for online-ordering, reservations, loyalty, or shift-scheduling
  - pm decomposing a restaurant feature and sizing tasks
  - anyone modelling a menu, order, booking, or rota and at risk of a flat/naive data model
  Do NOT apply for generic booking/CRM/content products outside food & hospitality.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Vertical: restaurants & hospitality — don't spec it naive

Restaurants run on razor-thin margins (net 3–6%) with a hostile incumbent
stack. A spec that treats a menu as a flat list of `{name, price}` or
ignores who already owns the POS will ship something no operator can use.
This skill loads the domain so architect/pm sound like they've worked a
shift.

The 4 products in this vertical:

| Product | Archetype | One-liner |
|---|---|---|
| online-ordering | content | Own menu + checkout for dine-in/pickup/delivery — dodge aggregator fees |
| reservations | booking | Bookings, tables, text-the-waitlist |
| loyalty | crm | Points, offers, win-back |
| shift-scheduling | booking | Rota, open shifts, swaps with coverage rules |

Incumbents to position against: **Toast** (POS, ~$69–165/mo + hardware +
2.49%+ per swipe), **Square** (POS/SMB), **SevenRooms** (reservations/CRM,
upmarket), **ChowNow** (commission-free ordering), **DoorDash / Uber Eats /
Grubhub** (aggregators, **15–30% commission** per order).

## 1. Domain vocabulary (use these words in the spec)

- **COGS / food cost %** — cost of ingredients ÷ menu price. Target ~28–35%.
- **Prime cost** — food cost + labor cost; the number operators obsess over
  (target ≤ ~60% of sales).
- **Menu engineering** — classifying items by popularity × margin into
  stars (high/high), plowhorses, puzzles, **dogs** (low/low). Drives what
  gets promoted or cut.
- **86'd** — an item is out of stock / unavailable ("we're 86 on the
  salmon"). Must propagate instantly to every ordering channel.
- **Modifiers / mods** — choices on an item (size, temp, add bacon, no
  onions, sub fries). Grouped, with required/optional + min/max rules.
- **Covers** — number of guests served (a "200-cover night").
- **Turn time** — how long a table is occupied; reservations math depends
  on it (a 2-top turns in ~75 min).
- **FOH / BOH** — front of house (servers, host, bar) / back of house
  (kitchen, prep, dish). Scheduling and tips differ between them.
- **Tip pooling** — pooled tips split by rule (hours, role, points).
  Legally constrained — see §6.
- **Comps / voids** — comp = item given free (manager discretion); void =
  item removed before it's made. Both need audit trails.
- **Ticket times** — elapsed time from order fired to served; the kitchen's
  core SLA.
- **Third-party aggregator commission** — the 15–30% DoorDash/Uber Eats/
  Grubhub take. The pain that makes owned ordering a wedge.
- **KDS (kitchen display system)** — screen in the kitchen that replaces
  paper tickets; orders route to it by station.

## 2. Non-obvious domain rules

- **The POS is the sticky system of record — don't fight it.** Toast/Square
  own the menu, payments, and floor. Our products integrate with or sit
  beside the POS; they don't try to replace it. Sync the menu, don't fork it.
- **Aggregator commission is the wound; owned online-ordering is the wedge.**
  A restaurant paying 25% to DoorDash on a $40 order keeps $30. Commission-
  free direct ordering is the single clearest ROI pitch — lead with it.
- **Menus have deep modifier hierarchies, not flat prices.** "Burger" → size
  group (required, choose 1) → temp group (required) → add-ons (optional,
  0–5) → side (required, choose 1, sub upcharges). Price = base + mods.
- **86'd / out-of-stock is real-time and must sync everywhere.** When the
  kitchen 86's an item it must vanish from online ordering, KDS, and the
  POS simultaneously, or you sell what you can't make.
- **Tips have legal handling.** Pooling rules, who can share (FLSA bars
  managers/owners from tip pools), tip credit, and service-charge vs tip
  distinction are labor-law constrained, not free-form.
- **Margins are razor-thin.** A feature that adds 30¢/order of cost can erase
  the margin on that order. Cost-consciousness is a feature, not a nicety.
- **Reservations + waitlist are SMS-driven.** "Your table's ready" is a text,
  not an email. Waitlist quote times and ready-pings are the product.

## 3. What a naive build gets wrong

- **Flat menu, no modifier hierarchy.** `{name, price}` can't express
  "medium, well-done, add bacon, sub fries (+$2)". Model modifier groups
  with required/optional + min/max from day one.
- **Ignoring 86'd / out-of-stock.** Selling a sold-out item online is a
  refund, an angry guest, and a chargeback. Stock state is first-class.
- **Online ordering that doesn't sync the menu.** A second menu that drifts
  from the POS menu means wrong prices and phantom items. One source of
  truth, synced.
- **Tip handling that breaks labor law.** Letting managers into the pool, or
  mislabeling a service charge as a tip, is an FLSA violation, not a bug.
- **No dine-in vs pickup vs delivery distinction.** Each channel has
  different fulfillment, timing, fees, address/table data, and tax. One
  generic "order" type is wrong.
- **Loyalty that's points-only with no win-back.** Points without a lapsed-
  guest re-engagement flow (offers, "we miss you") leaves the highest-ROI
  CRM lever on the table.

## 4. Must-model entities

- **MenuItem** — base price, category, station, tax class, availability
  state (available / **86'd** / scheduled), with one or more **ModifierGroup**s.
- **ModifierGroup** — `{required: bool, min, max}` + ordered **Modifier**s
  (name, price delta, default, in-stock). Hierarchy, not a flat list.
- **Order** — **channel** (`dine_in | pickup | delivery`), **status**
  (`placed → confirmed → preparing → ready → completed | cancelled`), line
  items with resolved modifiers, computed total, table/address per channel.
- **Reservation** — party size, time, turn-time estimate, table assignment,
  status; plus **Waitlist** entry (quoted wait, ready-ping, SMS thread).
- **Shift** — role (FOH/BOH), start/end, **coverage rule** (min staff per
  role/time), **open shift** + **swap** request with approval/coverage check.
- **LoyaltyMember** — identity (phone-first), points balance, earn/redeem
  ledger, last-visit (for **win-back** segmentation), consent state.

## 5. Per-product notes (wedge + the one domain thing)

- **online-ordering** (content) — **Wedge:** commission-free direct ordering
  vs DoorDash's 15–30% and Toast Online Ordering's per-order fee. **The one
  thing:** the menu + modifier hierarchy must sync from the POS and honor
  86'd state, across dine-in/pickup/delivery, or it's worse than the
  aggregator it replaces. Menus rank locally → see [[local-seo]].
- **reservations** (booking) — **Wedge:** SevenRooms is upmarket/expensive;
  give SMBs bookings + waitlist without the price tag. **The one thing:**
  it's SMS-first — text-the-waitlist and ready-pings are the product; turn
  time drives table availability. SMS consent → [[lifecycle-messaging]].
- **loyalty** (crm) — **Wedge:** most POS loyalty is points-only; we add
  offers + **win-back**. **The one thing:** lapsed-guest re-engagement
  (segment by last-visit, send an offer) is where the revenue is — design
  win-back, not just an earn-points counter. Sends → [[lifecycle-messaging]].
- **shift-scheduling** (booking) — **Wedge:** rota + open shifts + swaps
  cheaper/simpler than the incumbents. **The one thing:** swaps must enforce
  **coverage rules** (min staff per role per time band) — an unconstrained
  swap that leaves the line uncovered is the failure mode.

## 6. Compliance (light — defer the heavy lifts)

- **Tip pooling / labor law (FLSA)** — managers/owners may not share in tip
  pools; keep tip vs service-charge distinct; honor tip-credit rules. State
  law varies (e.g. CA). Surface as a constraint; get specifics confirmed.
- **Food-allergen disclosure** — the big 9 US allergens must be declarable
  on menu items; some jurisdictions require menu labeling. Model allergen
  tags on MenuItem.
- **SMS consent for waitlist/loyalty** — TCPA consent, STOP/HELP, quiet
  hours apply to every text. Defer the mechanics to [[lifecycle-messaging]].
- **Payment** — PCI scope, SCA, refunds/chargebacks. Defer billing/payment
  design to the billing/PCI track; don't hand-roll card handling here.

---

Cross-refs: [[lifecycle-messaging]] (every SMS/email leg — consent + deliver-
ability), [[local-seo]] (menus and reservations rank locally; "best tacos
near me" is the funnel), [[migration-ready-schema]] (importing an existing
menu / guest list from the incumbent POS without losing modifier structure).
