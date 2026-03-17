---
name: walkeros-create-source
description:
  Use when creating a new walkerOS source. Example-driven workflow starting with
  research and input examples before implementation.
---

# Create a New Source

## Prerequisites

Before starting, read these skills:

- [understanding-flow](../walkeros-understanding-flow/SKILL.md) - How sources
  fit in architecture
- [understanding-sources](../walkeros-understanding-sources/SKILL.md) - Source
  interface
- [understanding-transformers](../walkeros-understanding-transformers/SKILL.md) -
  Transformer chaining from sources
- [understanding-events](../walkeros-understanding-events/SKILL.md) - Event
  structure sources emit
- [understanding-mapping](../walkeros-understanding-mapping/SKILL.md) -
  Transform raw input to events
- [testing-strategy](../walkeros-testing-strategy/SKILL.md) - How to test
- [writing-documentation](../walkeros-writing-documentation/SKILL.md) -
  Documentation standards (for Phase 7)

## Source Types

| Type   | Platform | Input                   | Example                             |
| ------ | -------- | ----------------------- | ----------------------------------- |
| Web    | Browser  | DOM events, dataLayer   | `browser`, `dataLayer`              |
| Server | Node.js  | HTTP requests, webhooks | `gcp`, `express`, `lambda`, `fetch` |

## Source Categories

| Category           | Purpose                                   | Examples                | Key Concern          |
| ------------------ | ----------------------------------------- | ----------------------- | -------------------- |
| **Transformation** | Convert external format → walkerOS events | `dataLayer`, `fetch`    | Mapping accuracy     |
| **Transport**      | Receive events from specific platform     | `gcp`, `aws`, `express` | Platform integration |

## Choose Your Template

| Complexity            | Template       | When to Use                           |
| --------------------- | -------------- | ------------------------------------- |
| Simple transformation | `fetch/`       | Generic HTTP handler, data conversion |
| Platform transport    | `gcp/`, `aws/` | Cloud platform integration            |
| Browser interception  | `dataLayer/`   | DOM events, array interception        |

## Process Overview

```
1. Research     → Understand input format, find SDK/types
2. Examples     → Create input examples in dev entry FIRST
3. Mapping      → Define input → walkerOS event transformation
4. Scaffold     → Copy template and configure
5. Implement    → Build using examples as test fixtures
6. Test         → Verify against example variations
7. Document     → Write README
```

---

## Phase 1: Research

**Goal:** Understand the input format before writing any code.

### 1.1 Identify Input Source

- [ ] **What triggers events?** - HTTP POST, webhook, DOM mutation, dataLayer
      push
- [ ] **What data is received?** - Request body, headers, query params
- [ ] **Authentication?** - API keys, signatures, tokens

### 1.2 Find Official Resources

```bash
# Search npm for official types
npm search @[platform]
npm info @types/[platform]

# Check for official SDK
npm search [platform]-sdk
```

### 1.3 Document Input Schema

| Field        | Type   | Required | Description            |
| ------------ | ------ | -------- | ---------------------- |
| `event`      | string | Yes      | Event type from source |
| `properties` | object | No       | Event data             |
| `userId`     | string | No       | User identifier        |
| `timestamp`  | number | No       | Event time             |

### 1.4 Check Existing Patterns

```bash
# List existing sources
ls packages/web/sources/
ls packages/server/sources/

# Reference implementations
# - dataLayer: DOM-based, array interception
# - express: HTTP middleware
# - fetch: Generic HTTP handler (simplest server pattern)
# - gcp: Cloud Functions specific
```

### Gate: Research Complete

- [ ] Input trigger identified (HTTP, webhook, DOM, dataLayer)
- [ ] Input schema documented (required/optional fields)
- [ ] Fields mapped to walkerOS event structure

---

## Phase 2: Create Input Examples (BEFORE Implementation)

**Goal:** Define realistic input data in `dev` entry FIRST.

### 2.1 Scaffold Directory Structure

```bash
mkdir -p packages/server/sources/[name]/src/{examples,schemas,types}
```

### 2.2 Create Example Files

| File                   | Purpose                        | Template                              |
| ---------------------- | ------------------------------ | ------------------------------------- |
| `examples/inputs.ts`   | Incoming data examples         | [inputs.ts](./examples/inputs.ts)     |
| `examples/outputs.ts`  | Expected walkerOS events       | [outputs.ts](./examples/outputs.ts)   |
| `examples/requests.ts` | HTTP request examples (server) | [requests.ts](./examples/requests.ts) |
| `examples/mapping.ts`  | Event name/data transformation | [mapping.ts](./examples/mapping.ts)   |

### 2.3 Export via dev.ts

```typescript
export * as schemas from './schemas';
export * as examples from './examples';
```

### Gate: Examples Valid

- [ ] All example files compile (`npm run build`)
- [ ] Can trace: input → expected output for each example
- [ ] Edge cases included (minimal input, invalid input)

---

## Phase 3: Define Mapping

**Goal:** Document transformation from input format to walkerOS events.

Use [mapping.ts](./examples/mapping.ts) as your template.

### Verify Mapping Logic

```text
Input: inputs.pageViewInput (event: 'page_view')
  ↓ Match mapping rule: page_view.*
  ↓ Apply rule.name: 'page_view' → 'page view'
  ↓ Apply rule.data.map transformations
  ↓ properties.page_title → title
  ↓ properties.page_path → path
Output: Should match outputs.pageViewEvent
```

### Gate: Mapping Verified

- [ ] Mapping rules cover main input event types
- [ ] Each rule.name transforms to correct walkerOS event name
- [ ] Each mapping rule traces correctly to expected output

---

## Phase 4: Scaffold

**Template sources:**

- Web: `packages/web/sources/dataLayer/`
- Server: `packages/server/sources/fetch/` (simplest pattern)

```bash
cp -r packages/server/sources/fetch packages/server/sources/[name]
cd packages/server/sources/[name]

# Update package.json: name, description, repository.directory
```

**Directory structure:**

```
packages/server/sources/[name]/
├── src/
│   ├── index.ts           # Main export
│   ├── index.test.ts      # Tests against examples
│   ├── dev.ts             # Exports schemas and examples
│   ├── examples/
│   ├── schemas/
│   └── types/
├── package.json
├── tsconfig.json
├── tsup.config.ts
├── jest.config.mjs
└── README.md
```

### Transformer Chain Integration

Sources can wire to transformer chains via `next` in the init config:

```typescript
sources: {
  mySource: {
    code: sourceMySource,
    config: { settings: { /* ... */ } },
    next: 'validate'  // Events go through validator before collector
  }
}
```

---

## Phase 5: Implement

**Now write code to transform inputs to expected outputs.**

### Template Files

| File               | Purpose                | Template                                    |
| ------------------ | ---------------------- | ------------------------------------------- |
| `types/index.ts`   | Type definitions       | [types.ts](./templates/server/types.ts)     |
| `schemas/index.ts` | Zod validation schemas | [schemas.ts](./templates/server/schemas.ts) |
| `index.ts`         | Main source            | [index.ts](./templates/server/index.ts)     |

### Key Patterns

1. **Context destructuring**: Extract `config`, `env`, `logger`, `id` from
   context
2. **Schema validation**: Use Zod schemas to validate settings and provide
   defaults
3. **Forward to collector**: Call `env.push()` to send events to the collector
4. **Error logging**: Use `logger?.error()` for errors only, not routine
   operations
5. **Return Source.Instance**: Return `{ type, config, push }` object

### Gate: Implementation Compiles

- [ ] `npm run build` passes
- [ ] `npm run lint` passes

---

## Phase 6: Test Against Examples

**Verify implementation produces expected outputs.**

### Test Template

Use the test template: [index.test.ts](./templates/server/index.test.ts)

### Key Test Patterns

1. **Use `createSourceContext()` helper** - Standardizes context creation
2. **Mock `env.push`** - Verify events are forwarded to collector
3. **Use examples for test data** - Don't hardcode test values
4. **Test error paths** - Verify graceful error handling and logging

### Gate: Tests Pass

- [ ] `npm run test` passes
- [ ] Tests verify against example outputs (not hardcoded values)
- [ ] Invalid input handled gracefully (no crashes)

---

## Phase 7: Document

Follow the [writing-documentation](../walkeros-writing-documentation/SKILL.md)
skill for:

- README structure and templates
- Example validation against `apps/quickstart/`
- Quality checklist before publishing

Key requirements for source documentation:

- [ ] Input format table documenting expected fields
- [ ] Event name mapping table (source format → walkerOS format)
- [ ] Configuration options table
- [ ] Working code example with imports
- [ ] Installation instructions

---

## Validation Checklist

Beyond
[understanding-development](../walkeros-understanding-development/SKILL.md)
requirements (build, test, lint, no `any`):

- [ ] `dev.ts` exports `schemas` and `examples`
- [ ] Examples include edge cases (minimal, invalid input)
- [ ] Invalid input returns gracefully (no crashes, clear error)
- [ ] Tests use examples for assertions (not hardcoded values)

---

## Reference Files

| What            | Where                               |
| --------------- | ----------------------------------- |
| Web template    | `packages/web/sources/dataLayer/`   |
| Server template | `packages/server/sources/fetch/`    |
| Source types    | `packages/core/src/types/source.ts` |
| Event creation  | `packages/core/src/lib/event.ts`    |

## Related Skills

- [understanding-sources](../walkeros-understanding-sources/SKILL.md) - Source
  interface and push pattern
- [understanding-events](../walkeros-understanding-events/SKILL.md) - Event
  structure
- [testing-strategy](../walkeros-testing-strategy/SKILL.md) - Testing with env
  mocking
- [writing-documentation](../walkeros-writing-documentation/SKILL.md) -
  Documentation standards
