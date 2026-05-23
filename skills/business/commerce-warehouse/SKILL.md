---
name: commerce-warehouse
description: Manage warehouses, locations, and inventory movements. Use when setting up warehouses, creating zones/bins, moving stock between locations, or tracking location-level inventory.
---

# Commerce Warehouse

Manage warehouse facilities, location hierarchies, and inventory movements across zones, aisles, racks, and bins.

## How It Works

1. Create a warehouse with type and address.
2. Define locations within the warehouse (zones, aisles, racks, bins).
3. Track inventory at each location with on-hand, reserved, and available quantities.
4. Move inventory between locations with full audit trail.
5. Adjust location inventory with reason codes and references.

## Usage

- MCP tools: `list_warehouses`, `get_warehouse`, `create_warehouse`, `update_warehouse`, `list_locations`, `get_location`, `create_location`, `get_location_inventory`, `adjust_location_inventory`, `move_inventory`, `list_movements`.
- Writes require `--apply`.

## Warehouse Types

- Distribution (default), Manufacturing, Retail, ThirdParty, Consignment, Returns

## Location Types

- Bulk, Pick, Staging, Receiving, Shipping, Quarantine, Returns, Production, Packing, CrossDock

## Movement Types

- Receipt, Transfer, Pick, Adjustment, Shipment, Return

## Output

```json
{"status":"moved","from_location":"LOC-A1-01","to_location":"LOC-B2-03","sku":"WIDGET-001","quantity":25}
```

## Present Results to User

- Warehouse and location identifiers created or updated.
- Inventory quantities at affected locations.
- Movement audit trail with reason and reference.

## Troubleshooting

- Insufficient stock at location: check on-hand minus reserved before moving.
- Location not found: verify the warehouse and location hierarchy exist.
- Duplicate location code: location codes must be unique within a warehouse.

## References
- references/warehouse-locations.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/warehouse.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/warehouse.rs
