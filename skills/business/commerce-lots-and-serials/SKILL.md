---
name: commerce-lots-and-serials
description: Manage lot/batch tracking and serial number management. Use when tracking product batches with expiration dates, assigning serial numbers, or performing traceability lookups.
---

# Commerce Lots & Serials

Track product batches with lot numbers and expiration dates, and manage individual unit serial numbers for full traceability.

## How It Works

### Lot Tracking
1. Create lots with production date, quantity, and expiration.
2. Track lot inventory across warehouse locations.
3. Consume, adjust, transfer, split, or merge lots.
4. Quarantine lots for quality issues.
5. Attach certificates (COA, COC, MSDS).
6. Trace upstream sources and downstream consumption.

### Serial Number Tracking
1. Create serial numbers individually or in bulk.
2. Track serial lifecycle: Available -> Sold -> Shipped -> InService.
3. Reserve serials for orders with expiration.
4. Transfer ownership and track location changes.
5. Look up complete serial history with warranty info.

## Usage

- MCP tools (Lots): `create_lot`, `list_lots`, `get_lot`, `consume_lot`, `adjust_lot`, `transfer_lot`, `split_lot`, `merge_lots`, `quarantine_lot`, `release_quarantine`, `add_lot_certificate`, `trace_lot`, `get_expiring_lots`.
- MCP tools (Serials): `create_serial`, `bulk_create_serials`, `list_serials`, `get_serial`, `mark_serial_sold`, `mark_serial_shipped`, `reserve_serial`, `release_serial_reservation`, `transfer_serial_ownership`, `lookup_serial`, `validate_serial`, `get_available_serials`.
- Writes require `--apply`.

## Lot Statuses

- Active, Consumed, Expired, Quarantine, Transferred

## Serial Statuses

- Available, Reserved, Sold, Shipped, InService, Returned, Repaired, Quarantine, Scrapped, Unknown

## Certificate Types

- COA (Certificate of Analysis), COC (Certificate of Compliance), MSDS (Material Safety Data Sheet)

## Output

```json
{"status":"lot_created","lot_number":"LOT-2025-A001","sku":"PHARMA-100","quantity":500,"expiration_date":"2026-06-30"}
```

```json
{"status":"serial_created","serial_number":"SN-W001-00001","sku":"WIDGET-PRO","status":"available"}
```

## Present Results to User

- Lot number, SKU, quantity, and expiration date.
- Serial number, current status, and owner.
- Traceability chain (upstream sources, downstream consumers).
- Expiring lots within the requested timeframe.

## Troubleshooting

- Lot in quarantine: must release quarantine before consumption.
- Serial already reserved: release existing reservation first.
- Expired lot: cannot consume expired lots; adjust or scrap.
- Merge conflict: lots must share the same SKU to merge.

## References
- references/traceability.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/lots.rs
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/serials.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/lots.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/serials.rs
