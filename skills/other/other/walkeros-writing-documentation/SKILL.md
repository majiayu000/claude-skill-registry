---
name: walkeros-writing-documentation
description:
  Use when writing or updating walkerOS documentation - README, website docs, or
  skills. Covers quality standards, example validation, and DRY patterns.
---

# Writing Documentation

## When to Use This Skill

- Creating a new package README
- Writing website documentation (MDX)
- Creating or updating skills
- Reviewing documentation for quality
- Documenting Phase 7 of create-destination or create-source

## Prerequisites

- [understanding-flow](../walkeros-understanding-flow/SKILL.md) - Architecture
  context
- [understanding-events](../walkeros-understanding-events/SKILL.md) - Event
  naming rules

---

## Documentation Types

### Where Content Belongs

| Type               | Purpose                                       | Audience                    |
| ------------------ | --------------------------------------------- | --------------------------- |
| **Package README** | Installation, basic usage, API reference      | Package users               |
| **Website docs**   | Guides, integration examples, detailed config | Integrators                 |
| **Skills**         | Process knowledge, workflows                  | AI assistants, contributors |

### Divio Documentation Types

Keep these separate - don't mix tutorials with reference:

| Type             | Purpose            | User State                    |
| ---------------- | ------------------ | ----------------------------- |
| **Tutorial**     | Learning           | Studying, beginner            |
| **How-To Guide** | Problem-solving    | Working, knows what they need |
| **Reference**    | Information lookup | Working, needs facts          |
| **Explanation**  | Understanding      | Studying, needs context       |

---

## Example Validation (CRITICAL)

### The Problem

AI-generated examples can be:

- Syntactically correct but use non-existent APIs
- Plausible-looking but don't match actual exports
- Outdated, referencing deprecated patterns

### Source of Truth Hierarchy

```text
TIER 1: apps/quickstart/
  ✓ Tested  ✓ Compiled  ✓ CI-validated
  → USE FOR: All code examples

TIER 2: packages/core/src/eventGenerator.ts
  ✓ Canonical events  ✓ Real data structures
  → USE FOR: Event examples

TIER 3: packages/*/src/index.ts exports
  ✓ Actual public API
  → USE FOR: Verifying API names exist

TIER 4: Package READMEs & Website docs
  ⚠ May contain errors
  → VERIFY against Tier 1-3 before trusting
```

### Validation Checklist

Before publishing ANY code example:

- [ ] **API exists?** Check `packages/*/src/index.ts` exports
- [ ] **Pattern validated?** Compare against `apps/quickstart/`
- [ ] **Events canonical?** Use patterns from `eventGenerator.ts`
- [ ] **Example compiles?** TypeScript check passes
- [ ] **Imports correct?** Package names match actual packages

### Red Flags

| Red Flag                               | What It Indicates                   |
| -------------------------------------- | ----------------------------------- |
| API name not in package exports        | Hallucinated or outdated API        |
| Import path doesn't match package.json | Wrong package reference             |
| Event name with underscore             | Wrong format (should be space)      |
| No imports shown                       | Context missing, harder to validate |

---

## DRY Patterns

### PropertyTable for Configuration

**When to use:** Any page documenting package configuration with Zod schemas.

```mdx
import { schemas } from '@walkeros/web-destination-gtag/dev';
<PropertyTable schema={schemas.settings} />;

;
```

**When NOT to use:**

- Pages without package configuration
- Reference tables (Logger API, CLI commands)
- Conceptual explanations

### Schema Exports (dev.ts)

Every destination/source should export schemas:

```typescript
// src/dev.ts
export * as schemas from './schemas';
export * as examples from './examples';
```

### Don't Duplicate

- Link to source files instead of copying type definitions
- Reference `apps/quickstart/` examples instead of writing from scratch
- Use PropertyTable instead of hardcoded markdown tables

---

## Quality Checklist

### Structure

- [ ] Follows appropriate Divio type (Tutorial/How-To/Reference/Explanation)
- [ ] Code example within first 100 words
- [ ] First example under 20 lines
- [ ] Uses `<details>` for advanced content
- [ ] Has "Next Steps" or "Related" section

### Content

- [ ] All event names use `"entity action"` format with space
- [ ] Flow config shown as primary usage pattern
- [ ] Examples are complete and copy-pasteable
- [ ] Includes imports in code examples

### AI Readability

- [ ] Clear semantic headers (H2, H3, H4 hierarchy - no skipped levels)
- [ ] Tables for structured data
- [ ] Links to source of truth TypeScript files
- [ ] Static fallback content alongside dynamic components

### Consistency

- [ ] Uses standard table formats
- [ ] Follows package/skill/website templates
- [ ] Terminology matches: walkerOS, collector, destination, source
- [ ] Headings use sentence case (e.g., "Next steps" not "Next Steps")

---

## Templates

### Package README Template

````markdown
# @walkeros/[package-name]

[1-sentence description]

[Source Code](link) | [NPM](link) | [Documentation](link)

## Quick Start

```json
{
  "version": 1,
  "flows": {
    "default": {
      "web": {},
      "[sources|destinations]": {
        "[name]": {
          "package": "@walkeros/[package-name]",
          "config": { ... }
        }
      }
    }
  }
}
```
````

## Features

- **Feature 1**: Brief description
- **Feature 2**: Brief description

## Installation

```bash
npm install @walkeros/[package-name]
```

## Configuration Reference

| Name | Type | Description | Required | Default |
| ---- | ---- | ----------- | -------- | ------- |

## Examples

### Basic

[Simple example]

<details>
<summary>Advanced: Custom Mapping</summary>

[Complex example]

</details>

## Type Definitions

See [src/types.ts](./src/types.ts) for TypeScript interfaces.

## Related

- [Documentation](website/docs/...)

````

### Website Doc Template (MDX)

```mdx
---
title: [Title]
description: [SEO description]
sidebar_position: [N]
---

# [Title]

<PackageLink package="@walkeros/[package]" />

[1-sentence description]

## Quick Start

```json
// Flow config example (<15 lines)
````

## Features

- **Feature 1**: Description

## Installation

<Tabs>
  <TabItem value="npm" label="npm">
    ```bash
    npm install @walkeros/[package]
    ```
  </TabItem>
</Tabs>

## Configuration

<PropertyTable schema={schemas.settings} />

## Next Steps

- [Related guide 1](/docs/...)

````mdx
---

## Priority Matrix

### Issue Classification

| Priority | Criteria | Action |
|----------|----------|--------|
| **P0 Critical** | Incorrect examples, wrong APIs, security issues | Fix immediately |
| **P1 High** | Missing PropertyTable, outdated domains, missing sections | Fix soon |
| **P2 Medium** | Inconsistent terminology, skipped headings | Plan to fix |
| **P3 Low** | Style issues, minor wording | Backlog |

---

## Non-Negotiables

### Event Naming

```text

CORRECT: "page view", "product add", "order complete" WRONG: "page_view",
"pageView", "PAGE VIEW"
```
````

### Package References

```text

CORRECT: `@walkeros/collector` (with backticks) WRONG: @walkeros/collector (no
backticks)

```

### Domain References

```text

CORRECT: `www.walkeros.io` or relative paths DO NOT USE: legacy domain
references

```

---

## Process

### For New Package Documentation

1. **Verify examples exist** in `apps/quickstart/` or create them first
2. **Write README** using template above
3. **Write website doc** using MDX template
4. **Run quality checklist**
5. **Verify all code examples** against Tier 1-3 sources

### For Documentation Updates

1. **Identify issue priority** using matrix above
2. **Check current state** against source of truth
3. **Make minimal changes** - don't over-engineer
4. **Verify examples still compile**
5. **Run quality checklist**

---

## Related Skills

- [walkeros-understanding-flow](../walkeros-understanding-flow/SKILL.md) - Data
  flow architecture
- [walkeros-understanding-events](../walkeros-understanding-events/SKILL.md) -
  Event structure and naming
