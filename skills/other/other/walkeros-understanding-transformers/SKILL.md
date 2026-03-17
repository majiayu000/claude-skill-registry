---
name: walkeros-understanding-transformers
description:
  Use when working with walkerOS transformers, understanding event
  validation/enrichment/redaction, or learning about transformer chaining.
  Covers interface, return values, and pipeline integration.
---

# Understanding walkerOS Transformers

## Overview

Transformers are middleware for **validating**, **enriching**, and **redacting**
events in the walkerOS pipeline. They run in chains at configurable points
between sources, collector, and destinations.

**Core principle:** Transformers transform events. They don't capture (sources)
or deliver (destinations)—they modify events in-flight.

## Use Cases

| Use Case     | Purpose                                   | Example                  |
| ------------ | ----------------------------------------- | ------------------------ |
| **Validate** | Ensure events match schema contracts      | JSON Schema validation   |
| **Enrich**   | Add server-side data to events            | User segments, geo data  |
| **Redact**   | Remove sensitive data before destinations | Strip PII, anonymize IPs |

## Transformer Interface

See
[packages/core/src/types/transformer.ts](../../packages/core/src/types/transformer.ts)
for canonical interface.

### Init Function (Context Pattern)

Transformers use a context-based initialization pattern:

```typescript
import type { Transformer } from '@walkeros/core';

export const transformerMyTransformer: Transformer.Init<Types> = (context) => {
  const { config = {}, env, logger, id } = context;
  const settings = SettingsSchema.parse(config.settings || {});

  return {
    push(event, pushContext) {
      // Process event
      return event;
    },
  };
};
```

**Init Context contains:**

| Property    | Type                 | Purpose                       |
| ----------- | -------------------- | ----------------------------- |
| `config`    | `Transformer.Config` | Settings, mapping, next chain |
| `env`       | `Types['env']`       | Environment dependencies      |
| `logger`    | `Logger`             | Logging functions             |
| `id`        | `string`             | Transformer identifier        |
| `collector` | `Collector.Instance` | Reference to collector        |
| `ingest`    | `Ingest` (optional)  | Request metadata from source  |

### Instance Methods

| Method    | Purpose                              | Required     |
| --------- | ------------------------------------ | ------------ |
| `push`    | Process event, return modified/false | **Required** |
| `init`    | One-time initialization              | Optional     |
| `destroy` | Cleanup resources                    | Optional     |

## Return Values

The `push` function controls event flow:

| Return  | Behavior                           |
| ------- | ---------------------------------- |
| `event` | Continue chain with modified event |
| `void`  | Continue chain, event unchanged    |
| `false` | Stop chain, event dropped          |

```typescript
push(event, context) {
  if (!event.data?.id) {
    context.logger.error('Missing required id');
    return false;  // Stop chain
  }

  event.data.enrichedAt = Date.now();
  return event;  // Continue with modified event
}
```

## Inline Code Transformers

For simple transformations without external packages, use inline code with the
`$code:` string prefix in JSON configs. The `$code:` prefix tells the CLI
bundler to parse the following string as executable JavaScript:

```json
{
  "transformers": {
    "enrich": {
      "code": {
        "push": "$code:(event) => { event.data.enrichedAt = Date.now(); return event; }"
      },
      "next": "validate"
    }
  }
}
```

**Inline code structure:**

| Property    | Purpose                             |
| ----------- | ----------------------------------- |
| `code.init` | Code run once during initialization |
| `code.push` | Code run for each event             |

**Push code has access to:**

- `event` - The event being processed
- `context` - Push context with logger, config, etc.

**Return values in push code:**

- Return modified event to continue chain
- Return `undefined` to pass event unchanged
- Return `false` to drop event from chain

**Example: Filtering internal events**

```json
{
  "transformers": {
    "filter": {
      "code": {
        "push": "$code:(event) => { if (event.name.startsWith('internal_')) return false; return event; }"
      }
    }
  }
}
```

**Mixing inline and package transformers:**

```json
{
  "transformers": {
    "addTimestamp": {
      "code": {
        "push": "$code:(event) => { event.data.processedAt = new Date().toISOString(); return event; }"
      },
      "next": "validate"
    },
    "validate": {
      "package": "@walkeros/transformer-validator"
    }
  }
}
```

## Pipeline Integration

Transformers run at two points in the pipeline:

```
Source → [Pre-Transformers] → Collector → [Post-Transformers] → Destination
          (source.next)                   (destination.before)
```

### Pre-Collector Chain

Runs after source captures event, before collector enrichment:

```typescript
sources: {
  browser: {
    code: sourceBrowser,
    next: 'validate'  // First transformer in pre-chain
  }
}
```

### Post-Collector Chain

Runs after collector enrichment, before destination receives event:

```typescript
destinations: {
  gtag: {
    code: destinationGtag,
    before: 'redact'  // First transformer in post-chain
  }
}
```

### Chain Linking

Transformers link together via `next`:

```typescript
transformers: {
  validate: {
    code: transformerValidator,
    config: { next: 'enrich' }  // Chain to next transformer
  },
  enrich: {
    code: transformerEnrich,
    config: { next: 'redact' }
  },
  redact: {
    code: transformerRedact
    // No next = end of chain
  }
}
```

## Push Context

The `push` function receives a context with event metadata:

| Property    | Purpose                      |
| ----------- | ---------------------------- |
| `config`    | Transformer configuration    |
| `env`       | Environment dependencies     |
| `logger`    | Scoped logger for output     |
| `id`        | Transformer identifier       |
| `collector` | Access to collector instance |
| `ingest`    | Request metadata from source |

```typescript
push(event, context) {
  const { logger, id, ingest } = context;

  logger.debug('Processing', { transformer: id, event: event.name });

  // Access request metadata if available
  if (ingest?.ip) {
    event.data = { ...event.data, clientIp: ingest.ip };
  }

  return event;
}
```

## Transformer Paths

| Path                               | Description           |
| ---------------------------------- | --------------------- |
| `packages/transformers/`           | Transformer packages  |
| `packages/transformers/validator/` | Validator transformer |

## Related Skills

- [walkeros-understanding-flow](../walkeros-understanding-flow/SKILL.md) - How
  transformers fit in architecture
- [walkeros-create-transformer](../walkeros-create-transformer/SKILL.md) -
  Create new transformer

**Source Files:**

- [packages/core/src/types/transformer.ts](../../packages/core/src/types/transformer.ts) -
  Interface

**Package READMEs:**

- [packages/transformers/validator/README.md](../../packages/transformers/validator/README.md) -
  Validator transformer

**Documentation:**

- [Website: Transformers](../../website/docs/transformers/index.mdx) - Overview
- [Website: Validator](../../website/docs/transformers/validator.mdx) -
  Validator docs
- [Website: Create Your Own](../../website/docs/transformers/create-your-own.mdx) -
  Guide
