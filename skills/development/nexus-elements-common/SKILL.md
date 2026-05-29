---
name: nexus-elements-common
description: Shared Nexus Elements hooks and utilities (components/common). Use when you need common hooks like usePolling, useStopwatch, or transaction step utilities outside of the widgets.
---

# Nexus Elements - Common

## Overview
Use the shared hooks/utilities under `components/common` (polling, debouncing, transaction steps, constants) when building custom Nexus UI.

## When to use
- You want to import `usePolling`, `useStopwatch`, `useTransactionSteps`, or shared constants like `SHORT_CHAIN_NAME`.
- You are building a custom component and need the common ErrorBoundary.

## Install
There is no standalone `@nexus-elements/common` registry item. Common files are bundled into most component registries.

### Option A: Install any widget that includes common
Install a widget (fast-bridge, transfer, deposit, bridge-deposit, swaps, unified-balance, view-history). It will lay down `components/common/*` files.

### Option B: Manual copy
Copy the files from:
- `registry/nexus-elements/common/*` in this repo, or
- Any `https://elements.nexus.availproject.org/r/<component>.json` that includes `components/common/*` in its `files` list.

## Usage
```ts
import {
  usePolling,
  useStopwatch,
  useTransactionSteps,
  SHORT_CHAIN_NAME,
} from "@/components/common";
```

## Notes
- Keep `components/common/index.ts` intact to preserve exports.
- `useTransactionSteps` pairs with `NEXUS_EVENTS` (`STEPS_LIST`, `STEP_COMPLETE`, `SWAP_STEP_COMPLETE`) for progress UIs.
- These utilities are internal helpers; prefer using full widgets unless you need custom UI.
