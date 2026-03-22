---
name: optimize-model-compute
description: Optimize BigQuery compute costs by assigning Dataform actions to slot reservations. USE FOR managing which models use reserved slots vs on-demand pricing, updating reservation assignments, or analyzing cost vs priority tradeoffs for data pipelines.
---

# Optimize Model Compute (BigQuery Reservations)

## Purpose

Automatically assign Dataform actions to BigQuery slot reservations based on priority and cost optimization strategy. Routes high-priority workloads to reserved slots while using on-demand pricing for low-priority tasks.

## When to Use

- Assigning new models/actions to appropriate compute tiers (reserved vs on-demand)
- Rebalancing reservation assignments based on priority changes
- Optimizing costs by moving low-priority workloads to on-demand
- Ensuring critical pipelines get guaranteed compute resources

## Configuration File

Reservations are configured in `definitions/_reservations.js`:

```javascript
const { autoAssignActions } = require("@masthead-data/dataform-package");

const RESERVATION_CONFIG = [
  {
    tag: "reservation", // Human-readable identifier
    reservation: "projects/.../reservations/...", // BigQuery reservation path
    actions: [
      // Models assigned to this tier
      "httparchive.crawl.pages",
      "httparchive.f1.pages_latest",
    ],
  },
  {
    tag: "on_demand",
    reservation: "none", // On-demand pricing
    actions: ["httparchive.sample_data.pages_10k"],
  },
];

autoAssignActions(RESERVATION_CONFIG);
```

## Implementation Steps

### Step 1: Source Configuration

**TODO**: _User will provide details on how to determine which models should use reserved vs on-demand compute_

### Step 2: Update Configuration

1. Open `definitions/_reservations.js`
2. Add or move actions between reservation tiers:

- **Reserved slots** (`reservation: 'projects/...'`): Critical, high-priority, SLA-sensitive workloads
- **On-demand** (`reservation: 'none'`): Low-priority, ad-hoc, or experimental workloads

### Step 3: Verify Changes

```bash
# Check syntax
dataform compile

# Validate no duplicate assignments
grep -r "\.actions" definitions/_reservations.js
```

## Decision Criteria

| Factor           | Reserved Slots     | On-Demand             |
| ---------------- | ------------------ | --------------------- |
| **Priority**     | High, SLA-bound    | Low, flexible         |
| **Frequency**    | Regular, scheduled | Ad-hoc, occasional    |
| **Cost Pattern** | Predictable usage  | Variable, sporadic    |
| **Impact**       | Critical pipelines | Experimental, samples |

## Key Notes

- Each action should appear in only ONE reservation config
- File starts with `_` to ensure it runs first in Dataform queue
- Changes take effect on next Dataform workflow run
- Package automatically handles global assignment (no per-file edits needed)

## Package Reference

Using `@masthead-data/dataform-package` (see [package.json](../../../package.json))
