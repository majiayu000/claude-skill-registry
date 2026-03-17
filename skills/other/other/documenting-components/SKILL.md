---
name: documenting-components
description: Create documentation for specific components or areas of a codebase. Analyzes targeted code sections and produces structured documentation useful to both humans and AI agents. Use when (1) documenting an undocumented component or module, (2) building initial docs for a new area, (3) an agent discovers documentation gaps during codebase exploration, or (4) onboarding documentation is needed for a complex subsystem. Always targets a specific component — never documents the entire codebase at once.
---

# Documenting Components

Create focused, accurate documentation for specific components or areas of a codebase. Targets individual components — **never** attempts to document an entire codebase in one pass.

## Core Principles

1. **Targeted Scope**: Document one component, module, or area at a time. Never scan or document the entire codebase.
2. **Human-First**: Write for human developers. If a human wouldn't find it useful, don't write it.
3. **Agent-Friendly Structure**: Structure docs so agents can selectively read what's relevant — documentation is lazy-loaded on demand, unlike AGENTS.md which is eager-loaded into every session.
4. **Accurate Over Comprehensive**: Only document what you can verify from the code. Never invent or assume behavior.
5. **Discover, Don't Assume**: Find the project's existing documentation structure before creating new files.
6. **No Duplication Across Levels**: Before documenting a concept, check if it already exists at a higher documentation level (domain, architecture, or business processes). If it does, **reference it** instead of redefining it. Component docs are the lowest layer — they reference all layers above.

## Documentation Hierarchy

```
Domain              ← Defines business concepts (referenced by this layer)
  ↓
Architecture        ← Defines system structure (referenced by this layer)
  ↓
Business Processes  ← Defines end-to-end flows (referenced by this layer)
  ↓
Components          ← You are here (specific module internals and interfaces)
```

## Workflow

### Step 1: Discover Documentation Structure

Before writing anything:

1. Check for existing documentation directories (`docs/`, `doc/`, `documentation/`, etc.)
2. Read existing docs to understand format, style, and level of detail
3. Check AGENTS.md for documentation pointers or conventions
4. **If no docs exist**: Propose a directory structure and format to the user before creating files — don't unilaterally decide

### Step 2: Analyze the Target Component

Focus **only** on the specified component:

1. Read the relevant source files
2. Identify key interfaces, types, and exported functions
3. Trace direct dependencies and integration points
4. Note patterns, conventions, and architectural decisions
5. Identify non-obvious behavior — implicit contracts, gotchas, edge cases that would trip up a newcomer or an agent

**Do not explore unrelated parts of the codebase.** Stay within the component boundary.

### Step 3: Write Documentation

Create documentation following the project's existing style. If no style exists, use this structure as a starting point:

```markdown
# <Component Name>

## Overview
<What this component does and why it exists — 2-3 sentences max>

## Architecture
<How it's structured internally, key design decisions, patterns used>

## Key Interfaces
<Public APIs, interfaces, types that consumers need to know — include signatures>

## Dependencies
<What this component depends on and what depends on it>

## Patterns & Conventions
<Project-specific patterns this component follows that aren't obvious from the code>

## Non-Obvious Behavior
<Gotchas, edge cases, implicit contracts, ordering requirements — things that bite you>
```

**Adapt to the project's conventions** — don't introduce a conflicting format if docs already exist.

### Step 4: Update AGENTS.md Pointers

If new documentation files were created, propose adding a pointer in AGENTS.md:

```markdown
## <Section Name>
See `docs/<new-file>.md` for <brief description>.
```

**Never put the documentation content into AGENTS.md** — only add a one-line pointer. AGENTS.md is an index, not an encyclopedia.

## Integration with Other Skills

This skill can be invoked:

- **Manually**: When you want to document a specific component
- **By the planning skill**: When Phase 2 (Codebase Exploration) discovers undocumented areas critical to the plan
- **By executing agents**: When an agent working on a sub-plan encounters an undocumented subsystem it needs to understand

After documentation is created, future planning sessions and executing agents benefit from it automatically — they read the docs instead of re-exploring code.

- **documenting-domain**: Component docs reference domain entities (e.g., "handles User creation — see domain/users.md"). Never redefine domain terms.
- **documenting-architecture**: Component docs reference architectural patterns (e.g., "implements the repository port — see architecture/data-layer.md"). Never re-explain the architecture.
- **documenting-business-processes**: Component docs describe their step in a process; process docs describe the end-to-end flow.

## Rules

- **Never document the entire codebase at once** — only the targeted component
- **Never invent behavior** — only document what's verifiable in the code
- **Match existing doc style** — don't introduce a new format if docs already exist
- **Propose, don't force** — if unsure about structure, location, or scope, ask the user
- **Keep it maintainable** — shorter accurate docs beat comprehensive stale docs
- **Use reference-style links** — when linking to other docs or source files, use reference links (`[text][ref]` with `[ref]: path` at the bottom of the file) rather than inline links. They read better in source and are easier to maintain.
- **No meta-commentary** — don't add "this doc was auto-generated" or session timestamps
