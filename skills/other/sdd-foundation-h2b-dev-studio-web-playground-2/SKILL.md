---
name: sdd-foundation
description: |
  Create Foundation documents defining web-playground identity.
  Use when: starting a new package, defining project scope, establishing identity anchors.
  Triggers: "create foundation", "define identity", "sdd foundation"
---

# Web Playground Foundation

Create Foundation documents that define identity and scope for packages.

## Anchor Prefixes

### Root Level

| Prefix | Meaning | Example |
|--------|---------|---------|
| SCOPE- | What the project does/doesn't do | SCOPE-MONOREPO |
| QUALITY- | Code quality standards | QUALITY-TYPESCRIPT |
| AUDIENCE- | Target users | AUDIENCE-DEVELOPER |

### Package Level (extends root)

| Prefix | Meaning | Example |
|--------|---------|---------|
| TECH- | Technology-specific constraints | TECH-REACT-18 |
| PATTERN- | Design patterns to demonstrate | PATTERN-HOOKS |
| DEMO- | What the sample showcases | DEMO-STATE-MANAGEMENT |

## Instructions

### 1. Choose Level

- **Root:** `spec/foundation.md` (project-wide identity)
- **Package:** `packages/{pkg}/spec/foundation.md` (sample-specific identity)

### 2. Write Frontmatter

```yaml
---
title: "{Package} Foundation"
version: 1.0.0
status: draft
---
```

### 3. Write Identity Section

Answer in 1-2 sentences:
- What is this? (root: collection of samples; package: specific technology demo)
- Who is it for?

### 4. Define Scope

- **In Scope:** Features this package demonstrates
- **Out of Scope:** What it explicitly won't cover

### 5. List Identity Anchors

Use prefixes from table above. Package foundations must align with root anchors.

For packages, reference root anchors: `Inherits: root::SCOPE-SHOWCASE, root::QUALITY-TYPESCRIPT`

### 6. Update State

Claim ownership and update `.sdd/state.yaml`:

```yaml
documents:
  foundation: { status: draft, version: 1.0.0, owner: claude }
```

## Example: Package Foundation

```markdown
---
title: "React Sample Foundation"
version: 1.0.0
status: draft
inherits:
  - root::foundation.md@1.0.0
---

# React Sample

## Identity

A React 18 sample demonstrating modern patterns: hooks, context, and functional components.

## Inherits

- root::SCOPE-SHOWCASE
- root::QUALITY-TYPESCRIPT
- root::AUDIENCE-DEVELOPER

## Identity Anchors

- **TECH-REACT-18:** Uses React 18 with concurrent features
- **TECH-RSBUILD:** Build tooling via Rsbuild
- **PATTERN-HOOKS:** All state via useState/useReducer
- **PATTERN-CONTEXT:** Global state via React Context
- **DEMO-TODO-APP:** Classic todo list showcasing patterns

## Scope

### In Scope

- Functional components with hooks
- Context-based state management
- Component composition patterns
- Testing with React Testing Library

### Out of Scope

- Class components
- Redux or other external state libraries
- Server-side rendering
```

## Verification

After creating Foundation:

- [ ] Frontmatter has title, version, status
- [ ] Identity answers "what is this?"
- [ ] Scope separates in/out clearly
- [ ] Every anchor uses correct prefix (SCOPE-/QUALITY-/AUDIENCE- for root, TECH-/PATTERN-/DEMO- for packages)
- [ ] Package foundations list inherited root anchors
- [ ] Anchors are specific enough to align requirements against

## State Update

After verification passes:
```yaml
documents:
  foundation: { status: verified, version: 1.0.0, owner: human }
current_phase: requirements
```

Transfer ownership to `human` or `unassigned` when complete.

## Next Phase

When foundation is verified, proceed to requirements:
- Create requirements with `@aligns-to` links to each anchor
- Ensure every anchor has at least one requirement

## Reference

For full details: `docs/sdd-guidelines.md` section 1.1
