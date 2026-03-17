---
name: walkeros-understanding-destinations
description:
  Use when working with walkerOS destinations, understanding the destination
  interface, or learning about env pattern and configuration. Covers interface,
  lifecycle, env mocking, and paths.
---

# Understanding walkerOS Destinations

## Overview

Destinations receive processed events from the collector and deliver them to
third-party tools (analytics, marketing, data warehouses).

**Core principle:** Destinations transform and deliver. They don't capture or
process—that's sources and collector.

## Destination Interface

See
[packages/core/src/types/destination.ts](../../packages/core/src/types/destination.ts)
for canonical interface.

| Method                      | Purpose                    | Required     |
| --------------------------- | -------------------------- | ------------ |
| `init(context)`             | Load scripts, authenticate | Optional     |
| `push(event, context)`      | Transform and send event   | **Required** |
| `pushBatch(batch, context)` | Batch processing           | Optional     |
| `config`                    | Settings, mapping, consent | **Required** |

## The env Pattern

Destinations use dependency injection via `env` for external APIs. This enables
testing without mocking.

```typescript
// Destination defines its env type
export interface Env extends DestinationWeb.Env {
  window: {
    gtag: Gtag.Gtag;
    dataLayer: unknown[];
  };
}

// Destination uses env, not globals
async function push(event, context) {
  const { env } = context;
  env.window.gtag('event', mappedName, mappedData);
}
```

### Testing with env

**REQUIRED SKILL:** See
[testing-strategy](../walkeros-testing-strategy/SKILL.md) for full testing
patterns.

```typescript
import { mockEnv } from '@walkeros/core';
import { examples } from '../dev';

const calls: Array<{ path: string[]; args: unknown[] }> = [];
const testEnv = mockEnv(examples.env.push, (path, args) => {
  calls.push({ path, args });
});

await destination.push(event, { ...context, env: testEnv });

expect(calls).toContainEqual({
  path: ['window', 'gtag'],
  args: ['event', 'purchase', expect.any(Object)],
});
```

## Destination Config

```typescript
config: {
  settings: { /* destination-specific */ },
  mapping: { /* event transformation rules */ },
  data: { /* global data mapping */ },
  consent: { /* required consent states */ },
  policy: { /* processing rules */ },
  queue: boolean,  // queue events
  dryRun: boolean, // test mode
}
```

## Destination Paths

| Type   | Path                            | Examples                             |
| ------ | ------------------------------- | ------------------------------------ |
| Web    | `packages/web/destinations/`    | gtag, meta, api, piwikpro, plausible |
| Server | `packages/server/destinations/` | aws, gcp, meta                       |

## Template Destination

Use as starting point: `packages/web/destinations/plausible/`

## Transformer Wiring

Destinations can wire to post-collector transformer chains via the `before`
property:

```typescript
destinations: {
  gtag: {
    code: destinationGtag,
    before: 'redact'  // First transformer to run before this destination
  }
}
```

The transformer chain runs after collector enrichment, before the destination
receives events. Each destination can have its own chain. See
[understanding-transformers](../walkeros-understanding-transformers/SKILL.md)
for chain details.

## Related Skills

- [walkeros-understanding-flow](../walkeros-understanding-flow/SKILL.md) - How
  destinations fit in architecture
- [walkeros-understanding-mapping](../walkeros-understanding-mapping/SKILL.md) -
  Configure transformations
- [walkeros-create-destination](../walkeros-create-destination/SKILL.md) -
  Create new destination

**Source Files:**

- [packages/core/src/types/destination.ts](../../packages/core/src/types/destination.ts) -
  Interface

**Package READMEs:**

- [packages/web/destinations/gtag/README.md](../../packages/web/destinations/gtag/README.md) -
  gtag example
- [packages/web/destinations/plausible/README.md](../../packages/web/destinations/plausible/README.md) -
  Plausible (template)

**Documentation:**

- [Website: Destinations](../../website/docs/destinations/index.mdx) - Overview
- [Website: Create Your Own](../../website/docs/destinations/create-your-own.mdx) -
  Guide
