---
name: vertical-creator
description: Domain-knowledge primer for the marketing & creator vertical (creators, newsletter writers, podcasters, course sellers) so architect/pm don't spec naively against incumbents (Substack ~10%, Patreon 8–12%, Kajabi $149+, beehiiv, Buffer/Hootsuite/Later). Supplies the vocabulary, the non-obvious take-rate/red-ocean rules, the entities a real scheduler/analytics/monetization/sponsorship product must model, and the per-product wedge — with sponsorship-crm flagged as the white-space wedge. Applied by architect/pm during spec authoring for any of the four products in this vertical — content-scheduler, analytics, monetization, sponsorship-crm.
when_to_use: |
  Apply when:
  - architect is writing ARCH-*.md for a marketing/creator product
    (content-scheduler, analytics, monetization, sponsorship-crm)
  - pm is decomposing one of these into tasks and needs to model the
    domain entities (Sponsor, Deal, MediaKit, ScheduledPost, ChannelMetric) correctly
  - any spec touches creator monetization, take-rate, brand deals, or cross-channel publishing
  Do NOT apply for other verticals (home services, restaurants, etc.) —
  the economics here (platform take-rate as the competitive lever, sponsorship
  white-space) are specific.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Vertical: marketing & creator — undercut the take-rate, own the white space

Creators monetize an audience across channels they don't control. Their economics are
dominated by **take-rate** (the platform's cut) and by **brand sponsorships** that most
creators still manage in spreadsheets. Two of the four products here (scheduling,
analytics) sit in **red oceans** owned by entrenched incumbents; one (**sponsorship-crm**)
sits in genuine **white space**. Spec against that asymmetry — don't lead with the
commodity.

## 1. Domain vocabulary

- **CPM (cost per mille)** — ad/sponsor price per 1,000 impressions. The supply side.
- **RPM (revenue per mille)** — revenue the creator actually earns per 1,000 views/opens,
  net of platform cut. RPM < CPM; the gap is fees and unfilled inventory.
- **Sponsorship / brand deal** — a brand pays a creator to promote a product. The unit of
  white-space revenue here.
- **Fee model** — how a deal pays: **flat fee** (fixed $ per deliverable), **affiliate**
  (% of referred sales), or **CPA** (cost-per-action — $ per signup/install). A single deal
  can mix them (flat + affiliate).
- **Deliverables** — the concrete asset(s) owed: posts, stories, dedicated email, video
  **integration** (a segment inside a longer video), etc. Each has a channel and a due date.
- **Usage rights** — whether/how long the brand may reuse the creator's content (e.g.
  "whitelisting" to run as paid ads). Priced separately; easy to give away by accident.
- **Media kit** — the creator's sales one-pager: audience size, demographics, engagement,
  past brands.
- **Rate card** — the creator's published prices per deliverable type. The negotiation anchor.
- **Audience demographics** — geo, age, gender split — what a brand buys against.
- **Engagement rate** — interactions ÷ reach/followers. The quality signal brands price on.
- **Take rate (platform cut)** — the % a monetization platform skims (Substack ~10%,
  Patreon 8–12%). The single biggest competitive lever in this vertical.
- **MRR** — monthly recurring revenue from memberships/subscriptions; the membership KPI.
- **UTM** — campaign tracking params on a link; the raw input to attribution.
- **Cross-channel attribution** — crediting a conversion/revenue back to the right channel
  and post across platforms with different IDs. Hard, and the analytics moat.

## 2. Non-obvious domain rules

- **Scheduling and analytics are RED OCEANS — do not lead there.** Buffer, Hootsuite, and
  Later own cross-channel scheduling; every analytics vendor re-skins channel dashboards.
  Building "yet another scheduler" is a commodity play with no wedge. These two only earn
  their place as the *connective tissue* of a suite, never as the entry point.
- **Sponsorship management is WHITE SPACE — this is the real wedge.** Most creators track
  brand sponsors, deals, and deliverables in **spreadsheets**. There is no entrenched
  category leader. A purpose-built sponsorship CRM is the one product here with a defensible
  reason to exist on day one.
- **Monetization platforms take 8–12% — undercut on take-rate.** The competitive lever is
  not features, it's the cut. If the incumbent takes 10% and you take 3%, that *is* the
  pitch. Take-rate must be a first-class, configurable design decision, not an afterthought.
- **Each social channel has a different API and content shape.** A "post" is not one thing:
  an X post, an IG story, a YouTube integration, and an email all differ in format, limits,
  metrics, and auth. Normalize at the model layer; never assume one channel's shape.
- **Brand deals carry deliverables + usage rights + payment milestones.** A deal is not a
  line item — it's a small project: multiple deliverables across channels, usage-rights
  terms, and staged payments (e.g. 50% on signing, 50% on go-live). Model all three.

## 3. What a naive build gets wrong

- **Building yet another scheduler** — treating content-scheduler as the hero product. It's
  a commodity in a red ocean; shipped standalone it competes head-on with Buffer and loses.
- **sponsorship-crm as a generic CRM** — modeling a "deal" as a contact + amount + stage
  misses the domain. It needs **deliverables**, **rate card**, **usage rights**, **fee
  model**, and **payment milestones** — a generic pipeline CRM captures none of these.
- **Analytics that just re-skins one channel** — pulling YouTube Studio numbers into a
  prettier chart adds nothing. The only defensible analytics is **normalized cross-channel**
  with attribution, not a single-channel mirror.
- **Monetization that ignores take-rate as the lever** — copying Substack's feature set at
  Substack's 10% cut. If take-rate isn't the design center, there's no reason to switch.

## 4. Must-model entities

Spec these explicitly; they recur across the four products. Build them
[[migration-ready-schema]] (stable external IDs, soft-delete, audit timestamps) because
creators arrive mid-stream from spreadsheets and incumbents and import open deals + members.

- **Sponsor** — the brand: contact(s), past deals, status. Distinct from the Deal.
- **Deal** — the unit of sponsorship revenue: **stage** (prospect → negotiating → signed →
  delivering → paid), **fee model** (flat / affiliate / CPA, possibly mixed), **deliverables**
  (each with channel + due date + status), **usage rights** (scope + duration), and
  **payment milestones** (amount + trigger + paid state). This is the white-space product —
  model it richly.
- **MediaKit / RateCard** — audience stats + demographics + engagement (media kit) and
  per-deliverable prices (rate card). The sales surface; feeds the Deal negotiation.
- **ScheduledPost** — one logical post with **per-channel variants** (content, format,
  limits, asset refs differ per channel), schedule time, and publish status per channel.
  Never a single body string shared across channels.
- **ChannelMetric** — a **normalized cross-channel** metric row (channel, post ref, metric
  type, value, period) so analytics can sum/compare across platforms with different native IDs.
- **Membership / Paywall tier** — name, price, interval, **take-rate**, entitlements, member
  count; the unit of recurring (MRR) monetization.

## 5. Per-product notes (wedge vs incumbent + the one thing to nail)

- **sponsorship-crm** (crm) — **THE WEDGE. White space.** Creators do this in spreadsheets;
  no category leader. **Must nail: the Deal as a project, not a contact** — deliverables +
  rate card + usage rights + fee model + payment milestones, with a stage machine. A generic
  CRM is a non-answer. See [[vertical-onboarding]]: first activation = first sponsor + deal
  imported off the spreadsheet.
- **monetization** (content) — wedge: **undercut take-rate**. Paywalls, memberships, tips at
  3% vs incumbents' 8–12%. **Must nail: take-rate as a first-class, configurable design
  center** and MRR tracking; consent for member comms defers to [[lifecycle-messaging]].
- **content-scheduler** (content) — **commodity, red ocean.** Only worth building as the
  publishing layer of the suite, never standalone. **Must nail: per-channel post variants**
  (one calendar, N channel shapes) — that's the only non-commodity part.
- **analytics** (dashboard) — **commodity unless cross-channel.** A single-channel re-skin is
  worthless. **Must nail: normalized cross-channel metrics + attribution**; ingestion of each
  channel's API is a [[connector-builder]] job, not bespoke glue.

## 6. Compliance (light)

Keep this proportionate — defer money-movement and message-sending specifics to the
relevant engineer/skill.

- **FTC disclosure** — sponsored content must be clearly disclosed (`#ad` / "sponsored" /
  paid-partnership label). If the product publishes brand deals, surface and enforce the
  disclosure as part of the deliverable, not an optional toggle.
- **1099 for creator income** — creators (and their sponsors/affiliates) generate reportable
  income; if the product touches payouts, track payee tax info for 1099-NEC/1099-K (US). Note
  it; don't build a tax engine into a CRM.
- **Email/SMS consent for membership comms** — member announcements and lifecycle sends need
  consent (CAN-SPAM/TCPA, double opt-in, suppression). Defer the deliverability + consent
  posture entirely to [[lifecycle-messaging]].
- **Platform ToS for cross-posting** — each channel's terms govern API auth, automation, and
  re-posting. Cross-channel publishing must respect per-platform rate limits and automation
  rules; don't assume one channel's allowances apply to all.

## Output

When applied, contribute a **Domain model** note to the architecture doc capturing: the
products in scope and which are commodity vs wedge (sponsorship-crm = white space), the
must-model entities above that this product owns, the **take-rate** decision if monetization
is in scope, the **Deal** shape (deliverables + usage rights + fee model + payment milestones)
if sponsorship-crm is in scope, and the **per-channel variant** + **normalized cross-channel**
contract if scheduler/analytics is in scope.
