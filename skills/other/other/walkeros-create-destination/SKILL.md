---
name: walkeros-create-destination
description:
  Use when creating a new walkerOS destination. Example-driven workflow starting
  with research and examples before implementation.
---

# Create a New Destination

## Prerequisites

Before starting, read these skills:

- [understanding-flow](../walkeros-understanding-flow/SKILL.md) - How
  destinations fit in architecture
- [understanding-destinations](../walkeros-understanding-destinations/SKILL.md) -
  Destination interface
- [understanding-transformers](../walkeros-understanding-transformers/SKILL.md) -
  Transformer chaining to destinations
- [understanding-mapping](../walkeros-understanding-mapping/SKILL.md) - Event
  transformation
- [testing-strategy](../walkeros-testing-strategy/SKILL.md) - How to test with
  env pattern
- [writing-documentation](../walkeros-writing-documentation/SKILL.md) -
  Documentation standards (for Phase 7)

## Choose Your Template

| Complexity | Template     | When to Use                         |
| ---------- | ------------ | ----------------------------------- |
| Simple     | `plausible/` | Single SDK call, minimal config     |
| Complex    | `gtag/`      | Multiple services, sub-destinations |
| Server     | `gcp/`       | Server-side, batching, SDK init     |

## Process Overview

```
1. Research     → Find SDK, understand vendor API
2. Examples     → Create dev entry with real usage patterns
3. Mapping      → Define walkerOS → vendor transformation
4. Scaffold     → Copy template and configure
5. Implement    → Build using examples as test fixtures
6. Test         → Verify against example variations
7. Document     → Write README
```

---

## Phase 1: Research

**Goal:** Understand the vendor API before writing any code.

### 1.1 Find Official Resources

- [ ] **Vendor API Documentation** - Endpoints, authentication, rate limits
- [ ] **Official TypeScript SDK** - Check npm for `@vendor/sdk` or
      `vendor-types`
- [ ] **Event Schema** - What fields are required/optional for each event type

```bash
# Search npm for official packages
npm search [vendor-name]
npm search @[vendor]

# Check for TypeScript types
npm info @types/[vendor]
```

### 1.2 Identify Event Types

List the vendor's event types and their required fields:

| Vendor Event | Required Fields       | walkerOS Equivalent  |
| ------------ | --------------------- | -------------------- |
| `pageview`   | `url`, `title`        | `page view`          |
| `track`      | `event`, `properties` | `product view`, etc. |
| `identify`   | `userId`, `traits`    | User identification  |

### 1.3 Check Existing Patterns

Review similar destinations in the codebase:

```bash
# List existing destinations
ls packages/web/destinations/

# Reference implementations
# - plausible: Simple, script-based
# - gtag: Complex, multiple services
# - meta: Pixel with custom events
```

### Gate: Research Complete

- [ ] API pattern identified (SDK function / HTTP / pixel)
- [ ] Auth method documented (API key, token, none)
- [ ] Event types mapped to walkerOS equivalents

### Checkpoint: Research Review (Optional)

If working with human oversight, pause here to confirm:

- API pattern and auth method correct?
- Event mapping makes sense for the use case?
- Any vendor quirks or rate limits to handle?

---

## Phase 2: Create Examples (BEFORE Implementation)

**Goal:** Define expected API calls in `dev` entry FIRST.

### 2.1 Scaffold Directory Structure

```bash
mkdir -p packages/web/destinations/[name]/src/{examples,schemas,types}
```

### 2.2 Create Example Files

Create these files based on the templates in this skill:

| File                  | Purpose                              | Template                            |
| --------------------- | ------------------------------------ | ----------------------------------- |
| `examples/outputs.ts` | Vendor API calls we will make        | [outputs.ts](./examples/outputs.ts) |
| `examples/events.ts`  | walkerOS events that trigger outputs | [events.ts](./examples/events.ts)   |
| `examples/env.ts`     | Mock environment for testing         | [env.ts](./examples/env.ts)         |
| `examples/mapping.ts` | Default event transformation         | [mapping.ts](./examples/mapping.ts) |

### 2.3 Export via dev.ts

```typescript
export * as schemas from './schemas';
export * as examples from './examples';
```

### Gate: Examples Valid

- [ ] All example files compile (`npm run build`)
- [ ] Can trace: input event → expected output for each example

---

## Phase 3: Define Mapping

**Goal:** Document transformation from walkerOS events to vendor format.

Use [mapping.ts](./examples/mapping.ts) as your template.

### Verify Mapping Logic

Create a mental (or actual) trace:

```
Input: events.pageView
  ↓ Apply mapping
  ↓ page.view rule matches
  ↓ name: 'pageview'
  ↓ data.path → url, data.title → title
Output: Should match outputs.pageViewCall
```

### Gate: Mapping Verified

- [ ] Mapping covers: page view + at least one conversion event
- [ ] Each mapping rule traces correctly to expected output

---

## Phase 4: Scaffold

**Template destination:** `packages/web/destinations/plausible/`

```bash
cp -r packages/web/destinations/plausible packages/web/destinations/[name]
cd packages/web/destinations/[name]

# Update package.json: name, description, repository.directory
```

**Directory structure:**

```
packages/web/destinations/[name]/
├── src/
│   ├── index.ts           # Main destination (init + push)
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

Destinations can wire to transformer chains via `before` in the init config:

```typescript
destinations: {
  myDestination: {
    code: destinationMyDestination,
    config: { settings: { /* ... */ } },
    before: 'redact'  // Events go through redactor before this destination
  }
}
```

---

## Phase 5: Implement

**Now write code to produce the outputs defined in Phase 2.**

### Template Files

Use these templates as your starting point:

| File             | Purpose          | Template                                |
| ---------------- | ---------------- | --------------------------------------- |
| `types/index.ts` | Type definitions | [types.ts](./templates/simple/types.ts) |
| `index.ts`       | Main destination | [index.ts](./templates/simple/index.ts) |

### Key Patterns

1. **Init receives context**: Destructure `config`, `env`, `logger`, `id` from
   context
2. **Push receives context**: Includes `data`, `rule` (renamed from `mapping`),
   `ingest`
3. **Use `getEnv(env)`**: Never access `window`/`document` directly
4. **Return config from init**: Allows updating config during initialization

### Gate: Implementation Compiles

- [ ] `npm run build` passes
- [ ] `npm run lint` passes

---

## Phase 6: Test Against Examples

**Verify implementation produces expected outputs.**

### Test Template

Use the test template: [index.test.ts](./templates/simple/index.test.ts)

### Key Test Patterns

1. **Use `createPushContext()` helper** - Standardizes context creation
2. **Include `id` field** - Required in context (new requirement)
3. **Use `rule` instead of `mapping`** - Property renamed in PushContext
4. **Use examples for test data** - Don't hardcode test values

### Gate: Tests Pass

- [ ] `npm run test` passes
- [ ] Tests verify against example outputs (not hardcoded values)

---

## Phase 7: Document

Follow the [writing-documentation](../walkeros-writing-documentation/SKILL.md)
skill for:

- README structure and templates
- Example validation against `apps/quickstart/`
- Quality checklist before publishing

Key requirements for destination documentation:

- [ ] Event mapping table (walkerOS → vendor format)
- [ ] Configuration options table (use PropertyTable if schema exists)
- [ ] Working code example with imports
- [ ] Installation instructions

---

## Validation Checklist

Beyond
[understanding-development](../walkeros-understanding-development/SKILL.md)
requirements (build, test, lint, no `any`):

- [ ] Uses `getEnv(env)` pattern (never direct `window`/`document` access)
- [ ] `dev.ts` exports `schemas` and `examples`
- [ ] Examples match type signatures
- [ ] Tests use examples for assertions (not hardcoded values)

---

## Reference Files

| What            | Where                                        |
| --------------- | -------------------------------------------- |
| Simple template | `packages/web/destinations/plausible/`       |
| Complex example | `packages/web/destinations/gtag/`            |
| Types           | `packages/web/core/src/types/destination.ts` |

## Related Skills

- [understanding-destinations](../walkeros-understanding-destinations/SKILL.md) -
  Destination interface and env pattern
- [testing-strategy](../walkeros-testing-strategy/SKILL.md) - Testing with env
  mocking
- [writing-documentation](../walkeros-writing-documentation/SKILL.md) -
  Documentation standards
