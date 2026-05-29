---
name: walkeros-create-transformer
description:
  Use when creating a new walkerOS transformer. Example-driven workflow for
  validation, enrichment, or redaction transformers.
---

# Create a New Transformer

## Prerequisites

Before starting, read these skills:

- [understanding-flow](../walkeros-understanding-flow/SKILL.md) - How
  transformers fit in architecture
- [understanding-transformers](../walkeros-understanding-transformers/SKILL.md) -
  Transformer interface
- [understanding-events](../walkeros-understanding-events/SKILL.md) - Event
  structure
- [testing-strategy](../walkeros-testing-strategy/SKILL.md) - How to test
- [writing-documentation](../walkeros-writing-documentation/SKILL.md) -
  Documentation standards (for Phase 6)

## Transformer Categories

| Category     | Purpose                       | Example                      |
| ------------ | ----------------------------- | ---------------------------- |
| **Validate** | Check event structure/content | JSON Schema, required fields |
| **Enrich**   | Add data to events            | Server timestamps, geo data  |
| **Redact**   | Remove/mask sensitive data    | Strip PII, anonymize IPs     |

## Process Overview

```
1. Research     → Understand use case (validate/enrich/redact)
2. Examples     → Create event before/after examples FIRST
3. Scaffold     → Copy template, configure package.json
4. Implement    → Build transformer with TDD
5. Test         → Verify against example transformations
6. Document     → Write README
```

## Supporting Files

This skill includes reference files you can copy:

- **[examples/](examples/)** - Example events and configs to adapt for your
  transformer
  - [events.ts](examples/events.ts) - Before/after event examples
  - [config.ts](examples/config.ts) - Configuration examples
- **[templates/validation/](templates/validation/)** - Complete redact
  transformer template
  - [index.ts](templates/validation/index.ts) - Implementation with context
    pattern
  - [types.ts](templates/validation/types.ts) - Type definitions
  - [schemas.ts](templates/validation/schemas.ts) - Zod validation schemas
  - [index.test.ts](templates/validation/index.test.ts) - Test suite with
    helpers

---

## Phase 1: Research

**Goal:** Understand what the transformer needs to do.

### 1.1 Define Use Case

- [ ] **Category**: Validate, Enrich, or Redact?
- [ ] **Input**: What events will this process?
- [ ] **Output**: What should change? What should be blocked?
- [ ] **Configuration**: What settings does user need?

### 1.2 Check Existing Patterns

```bash
# Reference implementation
ls packages/transformers/validator/

# Transformer types
cat packages/core/src/types/transformer.ts
```

### Gate: Research Complete

- [ ] Category identified (validate/enrich/redact)
- [ ] Input/output transformation defined
- [ ] Configuration options listed

---

## Phase 2: Create Examples (BEFORE Implementation)

**Goal:** Define event transformations in `dev` entry FIRST.

### 2.1 Scaffold Directory Structure

```bash
mkdir -p packages/transformers/[name]/src/{examples,schemas,types}
```

### 2.2 Create Event Examples

Adapt [examples/events.ts](examples/events.ts) for your transformer's use case.
Each example file should include:

- Events that should pass through (modified)
- Expected output after processing
- Events that should be blocked (for validators)

### 2.3 Create Config Examples

Adapt [examples/config.ts](examples/config.ts) for your transformer's settings.

### 2.4 Export via dev.ts

```typescript
export * as schemas from './schemas';
export * as examples from './examples';
```

### Gate: Examples Valid

- [ ] All example files compile (`npm run build`)
- [ ] Can trace: input event → expected output for each example

---

## Phase 3: Scaffold

**Template transformer:** `packages/transformers/validator/`

```bash
cp -r packages/transformers/validator packages/transformers/[name]
cd packages/transformers/[name]

# Update package.json: name, description, repository.directory
```

**Directory structure:**

```
packages/transformers/[name]/
├── src/
│   ├── index.ts           # Main export
│   ├── transformer.ts       # Transformer implementation
│   ├── index.test.ts      # Tests against examples
│   ├── dev.ts             # Exports schemas and examples
│   ├── examples/
│   │   ├── index.ts       # Re-exports
│   │   ├── events.ts      # Before/after event examples
│   │   └── config.ts      # Configuration examples
│   ├── schemas/
│   │   └── index.ts       # Zod schemas for settings
│   └── types/
│       └── index.ts       # Settings, Types interfaces
├── package.json
├── tsconfig.json
├── tsup.config.ts
├── jest.config.mjs
└── README.md
```

---

## Phase 4: Implement

**Now write code to transform examples as expected.**

### 4.1 Define Types

See [templates/validation/types.ts](templates/validation/types.ts) for the
pattern. Define `Settings` and `Types` interfaces.

### 4.2 Implement Transformer (Context Pattern)

Transformers use the **context pattern** - they receive a single `context`
object containing `config`, `env`, `logger`, `id`, and `collector`.

See [templates/validation/index.ts](templates/validation/index.ts) for a
complete implementation example.

**Key patterns:**

1. **Context destructuring**: Extract `config`, `logger`, `id` from init context
2. **Schema validation**: Use Zod schemas to validate settings and provide
   defaults (see
   [templates/validation/schemas.ts](templates/validation/schemas.ts))
3. **Push receives pushContext**: The `push` function gets event + push context
4. **Return values**: `event` (continue), `void` (passthrough), `false` (cancel)

### 4.3 Export

`src/index.ts`:

```typescript
export { transformerRedact } from './transformer';
export type { Settings, Types } from './types';
```

### Gate: Implementation Compiles

- [ ] `npm run build` passes
- [ ] `npm run lint` passes

---

## Phase 5: Test Against Examples

**Verify implementation produces expected outputs.**

See [templates/validation/index.test.ts](templates/validation/index.test.ts) for
a complete test suite showing:

1. **`createTransformerContext()` helper** - Standardizes init context creation
2. **`createPushContext()` helper** - Standardizes push context creation
3. **Examples for test data** - Don't hardcode test values
4. **Return value testing** - Verify `event`, `void`, or `false` returns

### Gate: Tests Pass

- [ ] `npm run test` passes
- [ ] Tests verify against example outputs

---

## Phase 6: Document

Follow the [writing-documentation](../walkeros-writing-documentation/SKILL.md)
skill for:

- README structure and templates
- Quality checklist before publishing

Key requirements for transformer documentation:

- [ ] Use case description (validate/enrich/redact)
- [ ] Configuration options table
- [ ] Working code example with imports
- [ ] Installation instructions
- [ ] Link to website docs

---

## Transformer-Specific Validation

Beyond
[understanding-development](../walkeros-understanding-development/SKILL.md)
requirements (build, test, lint, no `any`):

- [ ] `dev.ts` exports `schemas` and `examples`
- [ ] Examples include before/after event pairs
- [ ] Return values handle all cases (event, void, false)
- [ ] Tests use examples for assertions (not hardcoded values)

---

## Reference Files

| What           | Where                                    |
| -------------- | ---------------------------------------- |
| Template       | `packages/transformers/validator/`       |
| Types          | `packages/core/src/types/transformer.ts` |
| Chaining logic | `packages/collector/src/transformer.ts`  |

## Related Skills

- [walkeros-understanding-transformers](../walkeros-understanding-transformers/SKILL.md) -
  Transformer interface and chaining
- [walkeros-testing-strategy](../walkeros-testing-strategy/SKILL.md) - Testing
  patterns and env mocking
- [walkeros-writing-documentation](../walkeros-writing-documentation/SKILL.md) -
  Documentation standards
