---
name: nexus-elements-view-history
description: Install and use the View History component for Nexus intent history. Use when you want a history modal or inline list of intents.
---

# Nexus Elements - View History

## Overview
Install the ViewHistory component to display Nexus intent history as a modal or inline list.

## Prerequisites
- NexusProvider installed and initialized on wallet connect.
- Wallet connection configured.

## Install (shadcn registry)
1) Ensure shadcn/ui is initialized (`components.json` exists).
2) Ensure registry mapping exists:
```json
"registries": {
  "@nexus-elements/": "https://elements.nexus.availproject.org/r/{name}.json"
}
```
3) Install:
```bash
npx shadcn@latest add @nexus-elements/view-history
```
Alternative:
```bash
npx shadcn@latest add https://elements.nexus.availproject.org/r/view-history.json
```

## Manual install (no shadcn)
1) Download `https://elements.nexus.availproject.org/r/view-history.json`.
2) Create each file in `files[].target` with `files[].content`.
3) Install dependencies listed in `dependencies` and each `registryDependencies` item.

## Usage
```tsx
import ViewHistory from "@/components/view-history/view-history";

<ViewHistory viewAsModal={false} className="w-full" />
```

## SDK flow mapping
- Fetches intent history with `sdk.getMyIntents()` (requests-for-funds list).
- Intended for displaying status updates, explorer links, and retries.

## Props (ViewHistoryProps)
- `viewAsModal?`: render as modal (default true)
- `className?`: optional container className

## Notes
- There is no `view-intent` component; use ViewHistory for intent history.
