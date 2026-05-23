---
name: commerce-fulfillment
description: Manage fulfillment waves, pick tasks, pack tasks, and ship tasks. Use when processing outbound orders through the warehouse pick-pack-ship workflow.
---

# Commerce Fulfillment

Orchestrate outbound order fulfillment through wave planning, picking, packing, and shipping handoff.

## How It Works

1. Create a wave to group orders for efficient processing.
2. Generate pick tasks for items in the wave.
3. Workers complete picks, recording actual quantities.
4. Create pack tasks and assign items to cartons.
5. Create ship tasks and complete with carrier and tracking.

## Usage

- MCP tools: `create_wave`, `list_waves`, `release_wave`, `create_pick_task`, `complete_pick`, `create_pack_task`, `add_carton`, `create_ship_task`, `complete_ship`.
- Writes require `--apply`.

## Wave Types

- Batch (default): group multiple orders
- Priority: expedited orders
- Zone: orders for a specific warehouse zone
- Single: one order per wave

## Status Flows

**Wave:** Draft -> Released -> InProgress -> Completed (or Cancelled)

**Pick:** Pending -> Assigned -> InProgress -> Completed (or Short/Cancelled)

**Pack:** Pending -> Assigned -> ReadyToPack -> InProgress -> Completed (or Cancelled)

**Ship:** Pending -> ReadyToShip -> LabelPrinted -> Shipped (or Cancelled)

## Package Types

- Box (default), Envelope, Tube, Pallet, Custom

## Output

```json
{"status":"shipped","wave_id":"WAVE-2025-001","picks_completed":12,"cartons_packed":3,"tracking":"1Z999AA10123456784"}
```

## Present Results to User

- Wave number and order count.
- Pick completion rates and any short picks.
- Carton counts with dimensions and weights.
- Shipping labels and tracking numbers.

## Troubleshooting

- Short pick: item not at expected location; check inventory and create adjustment.
- Wave stuck in progress: verify all pick tasks are completed.
- Carton overweight: split items across multiple cartons.

## References
- references/fulfillment-flow.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/fulfillment.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/fulfillment.rs
