---
name: vertical-logistics
description: Domain knowledge for the logistics & supply-chain vertical (SMB shipping & inventory) so architect and pm don't spec naively. Covers the vocabulary (TMS vs WMS, multi-carrier rate shopping, dimensional weight, BOL/ASN, lot/batch, reorder point), the non-obvious rules incumbents get right, what a naive build gets wrong, and the entities each of the four products (shipment-tracking, warehouse-lite, route-optimization, po-mgmt) must model. Applied by architect when writing ARCH-{slug}.md and by pm when writing PLAN-{slug}.md for any logistics product.
when_to_use: |
  Apply when:
  - architect writes ARCH-{slug}.md for shipment-tracking, warehouse-lite, route-optimization, or po-mgmt
  - pm writes PLAN-{slug}.md and needs to scope logistics work without underestimating carrier/inventory complexity
  - any spec touches shipments, carriers, tracking, warehouses, inventory, purchase orders, or routes
  Do NOT apply to non-logistics products (use the matching vertical skill instead).
effort: low
allowed-tools: Read, Write, Grep, Glob
paths:
  - "docs/architecture/**"
  - "docs/plans/**"
  - "docs/design/**"
---

# Vertical: Logistics & supply chain — spec it like you've shipped a pallet

SMB shipping & inventory has a deep vocabulary and a pile of rules that look optional
until a real customer's data hits them. The incumbents (ShipHero, CartonCloud, Descartes
ShipRush, GoFreight, AfterShip, FreightPOP) encode decades of this. A naive spec models a
"shipment" as a tracking number and a "warehouse" as a quantity column — and ships a toy.
This skill is the domain framing so architect/pm don't.

The four products and their incumbents:

| Product | Archetype | Wedge | Closest incumbent |
|---|---|---|---|
| shipment-tracking | dashboard | branded customer-facing tracking | AfterShip (lite) |
| warehouse-lite | crud | small-warehouse WMS | ShipHero / CartonCloud |
| route-optimization | booking | multi-stop route optimization | Descartes / FreightPOP |
| po-mgmt | crud | purchase-order lifecycle | GoFreight / FreightPOP |

## 1. Domain vocabulary (use these terms in the spec, not paraphrases)

- **TMS vs WMS** — Transportation Management System (moving goods between places:
  carriers, rates, routes, tracking) vs Warehouse Management System (goods at rest inside
  a building: SKUs, locations, pick/pack/ship). Don't conflate them; route-optimization +
  shipment-tracking are TMS-flavoured, warehouse-lite is WMS, po-mgmt straddles.
- **Multi-carrier** — a shipment can go via USPS / UPS / FedEx / DHL / regional carriers.
  Each has its own API, label format, status codes, and webhook shape.
- **Rate shopping** — given a parcel, query carriers and pick cheapest/fastest meeting the
  SLA. Drives carrier choice; depends on dimensional weight.
- **Zones** — carrier distance bands (origin→dest); rate is a function of zone × weight.
- **Dimensional weight (DIM)** — billable weight = max(actual weight, L×W×H / DIM divisor).
  A big light box bills as if heavy. Ignoring DIM under-quotes every rate.
- **BOL (Bill of Lading)** — the carrier contract / receipt for a shipment (esp. freight).
- **ASN (Advance Ship Notice)** — supplier's heads-up of an inbound shipment; feeds
  receiving so the warehouse knows what's arriving before it lands.
- **SKU + lot/batch** — SKU identifies the product; lot/batch identifies a specific
  production run (expiry, recall, FIFO). Same SKU, different lots, are not interchangeable.
- **Pick / pack / ship** — the outbound fulfilment sequence inside a warehouse.
- **Putaway** — placing received inventory into its storage location.
- **Cycle count** — periodic partial inventory audit (vs full physical count); keeps
  on-hand honest without shutting the warehouse.
- **Reorder point + safety stock + lead time** — reorder when on-hand ≤ (demand ×
  lead-time) + safety stock. Drives PO creation timing.
- **3PL** — third-party logistics provider; runs the warehouse/shipping on behalf of others.
- **PO → receiving → put-away** — the inbound lifecycle: order goods, receive against the
  PO, put away into locations.
- **Dropship** — supplier ships direct to the end customer; inventory never touches your
  warehouse.
- **Last-mile** — final leg to the customer's door; where most delivery cost/failure lives.
- **Proof of delivery (POD)** — signature / photo / timestamp confirming delivery.
- **SLA / transit time** — promised delivery window; the constraint rate-shopping optimises
  against.

## 2. Non-obvious domain rules (the ones incumbents get right)

- **Tracking is multi-carrier with NORMALIZED statuses.** Every carrier's webhook payload
  and status vocabulary differs ("In Transit" vs "MV" vs "departed facility"). You must
  map each carrier's raw events onto ONE normalized status enum
  (e.g. `pending → info_received → in_transit → out_for_delivery → delivered / exception`).
  The normalized timeline is the product; the raw event is provenance.
- **Branded tracking is the low-switching customer-facing wedge.** The shipper's customers
  see a branded tracking page instead of the carrier's. Cheap to switch to, sticky once
  adopted — it's the AfterShip-lite entry point. (See shipment-tracking below.)
- **Route-optimization is a real VRP** (Vehicle Routing Problem), not "sort stops by
  distance". Capacity, time windows, vehicle count, and service times make it NP-hard.
  **Defer the algorithm to [[geo-routing-engineer]]** — this skill only frames the domain
  and the entity shape; do not let the spec hand-roll the solver.
- **Dimensional weight drives cost.** Any rate-shopping or quoting feature that ignores DIM
  produces wrong prices. Capture L×W×H on every parcel.
- **Warehouse needs lot/batch + cycle counts**, not just a quantity integer. Recalls,
  expiry (FIFO/FEFO), and audit honesty all require lot granularity and periodic counts.
- **PO lifecycle = create → approve → receive → reconcile.** A PO isn't a row that flips to
  "done"; it accrues received quantities (often partial, across multiple receipts) and is
  reconciled against the invoice. Skipping receive/reconcile makes the PO a sticky note.

## 3. What a naive build gets wrong

- **Single-carrier tracking** — hardcodes one carrier; real shippers use several.
- **Un-normalized carrier statuses** — stores raw carrier strings, so the UI and any
  automation can't reason across carriers. Normalize on ingest.
- **Route-opt as nearest-neighbour** — greedy nearest-stop gives bad routes and ignores
  capacity/time-windows. It's VRP → [[geo-routing-engineer]].
- **Inventory without lot/batch or cycle count** — a bare `quantity` column can't do
  recalls, expiry, or audit; on-hand drifts and nobody trusts it.
- **PO without receiving/reconciliation** — no partial receipts, no invoice match; the PO
  is decorative.
- **Ignoring dimensional weight in rate shopping** — quotes are systematically too low;
  margins evaporate on bulky-light parcels.

## 4. Must-model entities (the shapes that prevent rework)

Pair these with [[migration-ready-schema]] (source_ref + import_batch_id on importable
entities; model carriers/suppliers/customers as their own tables, not inline fields).

- **Shipment** — carrier (FK) + a **normalized status** + a **tracking-event timeline**
  (ordered events, each with carrier-raw payload + normalized status + timestamp + location).
  Parcel dims (L×W×H + weight) for DIM. POD reference.
- **InventoryItem** — SKU (FK) + **lot/batch** + **location** (bin/shelf, its own entity) +
  on-hand qty + **cycle-count** records (counted qty, variance, timestamp, counter).
- **PurchaseOrder** — full lifecycle: `create → approve → receive → reconcile`. Line items
  with ordered vs received qty (partial receipts → a Receipt entity), supplier (FK),
  reconciliation against invoice.
- **Route** — ordered **stops** + **constraints** (vehicle capacity, time windows, service
  time per stop). **Hand the optimisation algorithm to [[geo-routing-engineer]]** — the
  spec defines the entity and constraints, not the solver.

## 5. Per-product notes (wedge + the one domain thing)

- **shipment-tracking** (dashboard) — *wedge:* branded customer-facing tracking page
  (AfterShip-lite, low switching cost). *The one thing:* multi-carrier ingestion with
  **normalized status mapping** — every carrier's webhook normalized onto one enum.
  Carrier/tracking ingestion → [[connector-builder]].
- **warehouse-lite** (crud) — *wedge:* small-warehouse WMS for shops outgrowing
  spreadsheets. *The one thing:* **lot/batch + location + cycle count** — inventory is not
  a quantity column.
- **route-optimization** (booking) — *wedge:* multi-stop route optimization; **highest
  value, hardest.** *The one thing:* it's a **real VRP** — model stops + constraints here,
  but the solver is [[geo-routing-engineer]]'s. Do not ship nearest-neighbour.
- **po-mgmt** (crud) — *wedge:* purchase-order management. *The one thing:* the full
  **create → approve → receive → reconcile** lifecycle with partial receipts, not a status
  flag.

## 6. Compliance (light — flag, don't over-build)

- **Carrier ToS** — each carrier API has terms on caching/displaying tracking data and
  branding. Respect them; don't scrape where an API exists.
- **Hazmat** — if shipping dangerous goods, special labelling/declaration applies. Flag if
  in scope; defer the heavy ruleset.
- **Customs (cross-border)** — commercial invoice, HS codes, duties for international
  parcels. Capture the basics (declared value, HS code) if cross-border is in scope;
  **defer heavy customs** brokerage logic.
- **Proof-of-delivery retention** — PODs (signatures/photos) are dispute evidence; retain
  them per the shipper's policy and don't expire them early.

---

Cross-refs: [[geo-routing-engineer]] (route VRP solver), [[connector-builder]] (carrier &
tracking ingestion), [[migration-ready-schema]] (importable entities).
