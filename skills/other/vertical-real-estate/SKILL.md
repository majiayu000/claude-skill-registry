---
name: vertical-real-estate
description: Residential-proptech domain knowledge so architect / pm aren't naive when speccing real-estate products (listings, lead-crm, transaction-coordination, property-mgmt). Codifies MLS/IDX reality, listing status lifecycle + syndication canonical-source, long-cycle lead nurture, transaction-coordination as the high-pain wedge, and the must-model entities. Applied during spec authoring so the architecture reflects how real estate actually works — not a generic CRUD assumption.
when_to_use: |
  Apply when architect or pm is speccing a residential real-estate / proptech product:
  - listings (content) — build once, syndicate to every portal
  - lead-crm (crm) — capture + long-cycle automated nurture
  - transaction-coordination (crud) — tasks / docs / deadlines to close
  - property-mgmt (crud) — rent, maintenance, tenant comms
  Use to seed the domain model + the "what a naive build gets wrong" checklist before tasks are decomposed.
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Vertical: residential real estate — don't spec it naively

Real estate looks like generic CRUD (a listing is a record, a lead is a contact, a deal is
a checklist). It isn't. The domain has hard-won structure — MLS quirks, status lifecycles,
months-long sales cycles, agent-vs-brokerage data boundaries — that a naive build ignores
and then rebuilds. This skill front-loads that structure so the spec is right the first time.

Incumbents to know (and what they own): **Lone Wolf / Propertybase** (brokerage CRM + back
office), **Follow Up Boss** (lead-to-close CRM, the nurture gold standard), **CINC** (lead-gen
+ CRM), **Top Producer** (legacy CRM), **kvCORE / BoldTrail** (all-in-one platform). They are
expensive, broad, and switching-cost-heavy — which is why the wedge matters (see per-product).

## 1. Domain vocabulary (use these terms in the spec)

- **MLS** (Multiple Listing Service) — regional database of listings; there are ~500+ MLSs in
  the US, each its own system, login, and field set. There is no single national MLS.
- **IDX** (Internet Data Exchange) — the rules + feed that let a brokerage display *other*
  brokers' MLS listings on its own site. Governed by per-MLS display/redistribution rules.
- **RESO** — the standards body. **RESO Web API** (modern REST/OData feed) and **RESO Data
  Dictionary** (canonical field names) are the standard — but adoption and cleanliness vary
  per MLS. "RESO-compliant" still means per-MLS quirks.
- **Listing status** — lifecycle, not a flag: `active → pending / contingent → closed`
  (plus `coming soon`, `active under contract`, `withdrawn`, `expired`, `sold`). Status
  drives display rules and downstream automation.
- **Buyer agent vs seller (listing) agent** — opposite sides of a transaction; data and
  permissions differ. A contact can be a buyer lead and later a seller.
- **Brokerage vs agent** — the brokerage holds the license and (often) the data; the agent is
  the user. Commission **split** is how the deal's commission divides brokerage↔agent.
- **Escrow / settlement / closing** — the funded close; **contingencies** (inspection,
  financing, appraisal) are conditions that must clear first, each with a **deadline**.
- **Transaction coordinator (TC)** — the person who shepherds a deal from accepted-offer to
  close: chasing docs, signatures, and deadlines. Often done in Dotloop / Excel today.
- **CMA** (Comparative Market Analysis) — comp-based price estimate an agent gives a seller.
- **Lead-to-close funnel** — capture → nurture → active → under-contract → closed; months long.
- **Syndication portals** — **Zillow, Realtor.com**, Redfin, Trulia, etc.; a listing is
  pushed (syndicated) to many; our copy is one of many downstream copies.

## 2. Non-obvious domain rules (the stuff that breaks naive specs)

- **There is no one MLS schema.** Each MLS has its own auth, field quirks, photo handling, and
  redistribution rules. RESO standardizes the *intent* but the data is messy per-MLS. Model an
  **integration adapter per MLS**, not one global importer.
- **Transaction-coordination is the underserved, high-pain wedge.** It's the part still done in
  Dotloop/Excel with manual deadline-chasing. Low switching cost (it's not the system of record
  for leads), high pain, clear ROI. Lead this if choosing where to land first.
- **A listing has a canonical source and many syndicated copies.** The MLS record (or our
  record) is the source of truth; portal copies derive from it. Don't model portal copies as
  independent listings — model `source` + `syndication targets`.
- **Lead nurture is long-cycle.** A real-estate lead can sit warm for **6–18 months**. The CRM's
  job is *not* close-this-week; it's stay-top-of-mind for months with automated drip until the
  lead is ready. A short-funnel CRM design is simply wrong for this domain.

## 3. What a naive build gets wrong

- ❌ **One MLS schema.** Assuming a single import format. Reality: per-MLS adapter, per-MLS
  redistribution rules, RESO Data Dictionary as the *target* normalization, not the source.
- ❌ **Listing without status lifecycle + syndication canonical.** A flat "listing" row with no
  status state machine and no source/target model can't drive display rules or feed portals.
- ❌ **TC checklist without deadline + contingency tracking.** A plain task list misses the
  point: the value is enforced **deadlines** and **contingency** clearing, with alerts.
- ❌ **Lead CRM without long-cycle nurture.** Stage + next-touch + multi-month drip is the core;
  a pipeline-only CRM (close/lost in weeks) doesn't fit.
- ❌ **Ignoring agent-vs-brokerage data boundaries.** Who owns the lead and listing data —
  agent or brokerage — is a real permission/ownership boundary. Bake it into the model, not
  bolt it on later.

## 4. Must-model entities

Seed the domain model with these (exact fields negotiable; the *shape* is not):

- **Listing** — `status` (lifecycle state machine, §1), `source_ref` (MLS id / RESO key — the
  canonical source), `syndication_targets[]` (Zillow/Realtor.com/… with per-target state),
  price, address, beds/baths, floorSize, photos, listing_agent, brokerage.
- **Lead** — `stage` (capture→nurture→active→under-contract→closed), `last_contact_at`, owning
  agent, source, buyer/seller intent, and an attached **long-cycle nurture** (drip campaign,
  next-touch date). Tie to [[lifecycle-messaging]].
- **Transaction** — `checklist[]` (tasks), `deadlines[]` (each dated + owner + alert),
  `contingencies[]` (inspection/financing/appraisal, each with clear-by date + status),
  `documents[]` (e-signed), parties (buyer/seller/agents/TC), close date.
- **Property / Unit** + **MaintenanceRequest** (status, priority, tenant, assignee, photos),
  Lease/rent (amount, due date, tenant), tenant-comms thread. (property-mgmt.)

## 5. Per-product notes (wedge + the one domain thing to get right)

- **listings** (content) — *the one thing*: **MLS/IDX correctness** — per-MLS adapter,
  `source_ref` canonical, status lifecycle, redistribution-compliant display. Pairs with
  [[local-seo]] (listings must rank + syndicate; our page is the canonical, portal copies
  point back) and [[migration-ready-schema]] (`source_ref` = MLS/RESO key for re-import/dedupe).
- **lead-crm** (crm) — *the one thing*: **long-cycle nurture** — months-long automated drip,
  stage + last-contact, top-of-mind not close-now. Competes with Follow Up Boss; the bar is
  nurture quality. Pairs with [[lifecycle-messaging]].
- **transaction-coordination** (crud) — *the one thing*: this **IS the wedge** — low switching
  cost, high pain, replaces Dotloop/Excel. Get **deadline + contingency tracking** right (dated,
  owned, alerted); the checklist alone is table stakes. Recommend landing here first.
- **property-mgmt** (crud) — *the one thing*: **maintenance-request + rent + tenant-comms** as
  first-class flows; don't reduce it to a generic ticket list. Don't hold tenant/owner funds
  naively (see §6 escrow/trust).

## 6. Compliance (light — flag for the reviewer, don't solve here)

- **MLS / IDX redistribution + display rules** — per-MLS; controls what may be displayed, for
  how long, with what attribution. The integration adapter must honor them.
- **Fair Housing Act** — listing/ad copy and targeting must not discriminate (protected
  classes). Applies to listing descriptions and any lead-targeting automation.
- **Escrow / trust-account basics** — do **not** hold or move client/tenant funds naively.
  Earnest money and rent flow through trust/escrow with strict accounting; integrate a
  compliant provider rather than building a wallet.
- **E-sign** — transaction docs need legally-valid e-signature (ESIGN/UETA); use a real e-sign
  provider, capture audit trail.

## Output

When applied, contribute a **Domain model** block to the architecture/design doc:

```
## Domain model (real estate)
- entities: Listing(status lifecycle + source_ref + syndication_targets) · Lead(stage + last_contact + nurture) · Transaction(checklist + deadlines + contingencies + docs) · Property/Unit + MaintenanceRequest
- wedge: <which product lands first + why> (default: transaction-coordination)
- MLS/IDX: per-MLS adapter · RESO Data Dictionary as normalization target · redistribution rules honored
- nurture: long-cycle (6–18mo) drip, not short funnel
- compliance flags: IDX display rules · Fair Housing (copy) · escrow/trust (no naive funds) · e-sign
```
