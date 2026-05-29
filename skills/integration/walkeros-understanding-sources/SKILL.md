---
name: walkeros-understanding-sources
description:
  Use when working with walkerOS sources, understanding event capture, or
  learning about the push interface. Covers browser, dataLayer, and server
  source patterns.
---

# Understanding walkerOS Sources

## Overview

Sources capture events from the external world (browser DOM, dataLayer, HTTP
requests, cloud functions) and feed them to the collector.

**Core principle:** Sources capture. They don't process or deliver—that's
collector and destinations.

## Source Interface

See [packages/core/src/types/source.ts](../../packages/core/src/types/source.ts)
for canonical interface.

### Init Function (Context Pattern)

Sources use a context-based initialization pattern:

```typescript
import type { Source } from '@walkeros/core';

export const sourceMySource: Source.Init<Types> = async (context) => {
  const { config = {}, env, logger, id } = context;
  // ...
};
```

**Context contains:**

| Property    | Type                 | Purpose                    |
| ----------- | -------------------- | -------------------------- |
| `config`    | `Source.Config<T>`   | Settings, mapping, options |
| `env`       | `Types['env']`       | Environment (push, logger) |
| `logger`    | `Logger`             | Logging functions          |
| `id`        | `string`             | Source identifier          |
| `collector` | `Collector.Instance` | Reference to collector     |

### Push Method

| Method        | Purpose                             |
| ------------- | ----------------------------------- |
| `push(input)` | Receive external input, emit events |

## Push Signatures by Type

| Source Type    | Signature                           | Example      |
| -------------- | ----------------------------------- | ------------ |
| Cloud Function | `push(req, res) → Promise<void>`    | HTTP handler |
| Browser        | `push(event, data) → Promise<void>` | DOM events   |
| DataLayer      | `push(event, data) → Promise<void>` | GTM-style    |

**Key insight:** Source `push` IS the handler. No wrappers needed.

```typescript
// Direct deployment
http('handler', source.push);
```

## Source Paths

| Type   | Path                       | Examples           |
| ------ | -------------------------- | ------------------ |
| Web    | `packages/web/sources/`    | browser, dataLayer |
| Server | `packages/server/sources/` | gcp                |

## Browser Source

The browser source captures events from DOM using data attributes.

```html
<button data-elb="product" data-elb-product="id:P123;name:Laptop">
  <span data-elbaction="click">Add to Cart</span>
</button>
```

See [packages/web/sources/browser/](../../packages/web/sources/browser/) for
implementation.

## DataLayer Source

Captures events from a GTM-style dataLayer array.

```typescript
window.dataLayer.push({
  event: 'product view',
  product: { id: 'P123', name: 'Laptop' },
});
```

See [packages/web/sources/dataLayer/](../../packages/web/sources/dataLayer/) for
implementation.

## Server Sources

Handle HTTP requests in cloud functions. Server sources use the context pattern:

```typescript
import type { Source } from '@walkeros/core';

export const sourceCloudFunction: Source.Init<Types> = async (context) => {
  const { config = {}, env } = context;
  const { push: envPush } = env;

  // Validate settings with Zod schema
  const settings = SettingsSchema.parse(config.settings || {});

  const push = async (req: Request, res: Response): Promise<void> => {
    // Transform HTTP request → walkerOS event
    const event = transformRequest(req);
    await envPush(event);
    res.json({ success: true });
  };

  return { type: 'cloudfunction', config: { ...config, settings }, push };
};

// Direct deployment
export const handler = source.push;
```

See [packages/server/sources/gcp/](../../packages/server/sources/gcp/) for
implementation.

## Transformer Wiring

Sources can wire to pre-collector transformer chains via the `next` property:

```typescript
sources: {
  browser: {
    code: sourceBrowser,
    next: 'validate'  // First transformer to run after this source
  }
}
```

The transformer chain runs before events reach the collector. See
[understanding-transformers](../walkeros-understanding-transformers/SKILL.md)
for chain details.

## Related Skills

- [walkeros-understanding-flow](../walkeros-understanding-flow/SKILL.md) - How
  sources fit in architecture
- [walkeros-understanding-events](../walkeros-understanding-events/SKILL.md) -
  Events that sources emit
- [walkeros-create-source](../walkeros-create-source/SKILL.md) - Create new
  source

**Source Files:**

- [packages/core/src/types/source.ts](../../packages/core/src/types/source.ts) -
  Interface

**Package READMEs:**

- [packages/web/sources/browser/README.md](../../packages/web/sources/browser/README.md) -
  Browser source
- [packages/web/sources/dataLayer/README.md](../../packages/web/sources/dataLayer/README.md) -
  DataLayer source

**Documentation:**

- [Website: Sources](../../website/docs/sources/index.mdx) - Overview
- [Website: Browser Source](../../website/docs/sources/web/browser/index.mdx) -
  Browser docs
- [Website: Create Your Own](../../website/docs/sources/create-your-own.mdx) -
  Guide
