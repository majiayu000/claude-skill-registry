---
name: walkeros-understanding-flow
description:
  Use when learning walkerOS architecture, understanding data flow, or designing
  composable event pipelines. Covers Source→Collector→Destination pattern and
  separation of concerns.
---

# Understanding walkerOS Flow

## Overview

walkerOS follows a **Source → Collector → Destination(s)** architecture for
composable, modular event processing.

**Core principle:** Separation of concerns. Each component has one job.
Components are composable and replaceable.

## The Flow Pattern

```
Sources → [Pre-Transformers] → Collector → [Post-Transformers] → Destinations
(Capture)  (source.next)    (Processing) (dest.before)       (Delivery)

- Browser DOM              - Validation   - Validation        - Google Analytics
- DataLayer                - Enrichment   - Enrichment        - Meta Pixel
- Server HTTP              - Redaction    - Consent check     - Custom API
- Cloud Functions                         - Routing           - Data Warehouse
```

## Key Concepts

### Composability

A Flow combines components. You can:

- Use multiple sources feeding one collector
- Route events to multiple destinations
- Swap components without changing others

### The Flow Type

See [packages/core/src/types/flow.ts](../../packages/core/src/types/flow.ts) for
the canonical interface.

```typescript
// Conceptual structure (see source for full type)
interface Flow {
  sources?: Record<string, Source>;
  transformers?: Record<string, Transformer>;
  destinations?: Record<string, Destination>;
  collector?: Collector.InitConfig;
}
```

### Universal Push Interface

**All components communicate via `push` functions:**

| Component   | Push Signature                | Purpose               |
| ----------- | ----------------------------- | --------------------- |
| Source      | `push(input) → events`        | Capture external data |
| Collector   | `push(event) → void`          | Process and route     |
| Destination | `push(event, context) → void` | Transform and deliver |

The `elb()` function is an alias for `collector.push` - used for component
wiring.

### startFlow Helper

See [packages/collector/src/flow.ts](../../packages/collector/src/flow.ts) for
the `startFlow` function.

```typescript
import { startFlow } from '@walkeros/collector';

const { collector, elb } = await startFlow({
  sources: {
    /* ... */
  },
  transformers: {
    /* ... */
  },
  destinations: {
    /* ... */
  },
});
```

## Separation of Concerns

| Concern          | Handled By     | NOT Handled By          |
| ---------------- | -------------- | ----------------------- |
| Event capture    | Sources        | Collector, Destinations |
| Event structure  | Event model    | Components              |
| Consent checking | Collector      | Sources, Destinations   |
| Transformation   | Mapping system | Raw push calls          |
| Delivery         | Destinations   | Sources, Collector      |

## Transformer Chains

Transformers run at two points in the pipeline, configured via `next` and
`before`:

### Pre-Collector Chain

Runs after source captures event, before collector processing:

**Bundled mode (flow.json):**

```json
{
  "sources": {
    "browser": {
      "package": "@walkeros/web-source-browser",
      "next": "validate"
    }
  },
  "transformers": {
    "validate": {
      "package": "@walkeros/transformer-validator",
      "next": "enrich"
    },
    "enrich": {
      "package": "@walkeros/transformer-enricher"
    }
  }
}
```

**Integrated mode (TypeScript):**

```typescript
sources: {
  browser: {
    code: sourceBrowser,
    next: 'validate'
  }
},
transformers: {
  validate: {
    code: transformerValidator,
    config: { next: 'enrich' }
  },
  enrich: {
    code: transformerEnrich
  }
}
```

Note: In flow.json, `next` is at the reference level. The CLI bundler
automatically moves it into `config.next` for runtime - you don't need to handle
this yourself.

### Post-Collector Chain

Runs after collector enrichment, before destination receives event:

**Bundled mode (flow.json):**

```json
{
  "destinations": {
    "gtag": {
      "package": "@walkeros/web-destination-gtag",
      "before": "redact"
    }
  },
  "transformers": {
    "redact": {
      "package": "@walkeros/transformer-redact"
    }
  }
}
```

**Integrated mode (TypeScript):**

```typescript
destinations: {
  gtag: {
    code: destinationGtag,
    before: 'redact'
  }
},
transformers: {
  redact: {
    code: transformerRedact
  }
}
```

### Chain Resolution

- `source.next` → starts pre-collector chain
- `transformer.next` (flow.json) or `transformer.config.next` (runtime) → links
  transformers
- `destination.before` → starts post-collector chain per destination

## Related Skills

- [walkeros-understanding-events](../walkeros-understanding-events/SKILL.md) -
  Event model
- [walkeros-understanding-sources](../walkeros-understanding-sources/SKILL.md) -
  Source interface
- [walkeros-understanding-destinations](../walkeros-understanding-destinations/SKILL.md) -
  Destination interface

**Package READMEs:**

- [packages/collector/README.md](../../packages/collector/README.md) - Collector
  details

**Source Files:**

- [packages/collector/src/flow.ts](../../packages/collector/src/flow.ts) -
  startFlow implementation

**Documentation:**

- [Website: Flow](../../website/docs/getting-started/flow.mdx) - Flow concept
- [Website: Collector](../../website/docs/collector/index.mdx) - Collector docs
