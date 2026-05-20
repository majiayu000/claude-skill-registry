---
name: documenting-domain
description: Document business domain concepts, terminology, entity relationships, and domain rules for a project. Produces documentation that establishes the shared language used by both humans and AI agents. Use when (1) a project's domain concepts are undocumented, (2) agents misinterpret business terminology, (3) onboarding new team members who need to understand the business model, or (4) domain knowledge is scattered across code and needs consolidation. This is the most foundational documentation layer — all other docs reference it.
---

# Documenting Domain

Document the business domain of a project: its terminology, entities, relationships, rules, and mental models. This is the **most foundational documentation layer** — architecture, processes, and components all reference domain concepts.

## Core Principles

1. **Ubiquitous Language**: Define terms precisely. Every entity, state, and concept should have one clear definition that the entire team (and every agent) uses consistently.
2. **Business-First (What and Why, Not How)**: Write from the business perspective, not the implementation perspective. Define what concepts ARE and why they exist — never describe step-by-step flows or how things happen at runtime. "A workspace contains projects" is domain; "the workspaces table has a foreign key to projects" is implementation; "when a user creates a workspace, the system first validates..." is a process. If you find yourself writing sequential steps, that content belongs in a process doc.
3. **Accurate Over Comprehensive**: Only document domain concepts that actually exist in the codebase. Don't invent domain models the project doesn't implement.
4. **Non-Technical Where Possible**: Domain docs should be readable by non-technical stakeholders. Minimize code references — save those for component docs.
5. **No Duplication Across Levels**: Domain docs are the canonical source for business concepts. Architecture, process, and component docs **reference** domain docs — they never redefine domain terms. If you find a concept documented elsewhere, consolidate it here and replace the duplicate with a reference.

## Documentation Hierarchy

```
Domain          ← You are here (foundation — all other layers reference this)
  ↓
Architecture    ← References domain concepts
  ↓
Business Processes  ← References domain concepts and architecture
  ↓
Components      ← References all of the above
```

## Workflow

### Step 1: Discover Existing Documentation

Before writing anything:

1. Check for existing documentation directories and domain docs
2. Read AGENTS.md for pointers to existing documentation
3. Check if domain concepts are already documented (even informally) in READMEs, comments, or other docs
4. **If domain docs already exist**: Understand their structure and extend them — don't create a parallel system

### Step 2: Identify Domain Concepts

Analyze the targeted area of the codebase:

1. Read key model/entity definitions — struct names, type names, database schemas
2. Identify the core entities and their relationships
3. Look for business rules encoded in validation logic, state machines, or invariants
4. Note domain-specific terminology used in naming (variables, functions, modules)
5. Identify entity lifecycles — how entities are created, transition between states, and are retired

**Stay within the requested scope.** If asked to document the "billing domain", don't wander into authentication.

### Step 3: Write Domain Documentation

Follow the project's existing doc style. If none exists, use this structure:

```markdown
# <Domain Area>

## Overview
<What this domain area covers and why it exists in the system — 2-3 sentences>

## Key Concepts

### <Entity/Concept Name>
<Definition in plain business language>

- **Lifecycle**: <How it's created, what states it transitions through, when it's retired>
- **Relationships**: <What it belongs to, what it contains, what it interacts with>
- **Key Rules**: <Business invariants — e.g., "a workspace must always have at least one admin">

### <Another Entity/Concept>
...

## Domain Rules
<Cross-cutting business rules that don't belong to a single entity>
- <Rule 1>
- <Rule 2>

## Glossary
<Quick-reference table of domain terms — useful for agents and new team members>

| Term | Definition |
|------|-----------|
| ...  | ...       |
```

### Step 4: Update AGENTS.md Pointers

If new documentation files were created, propose adding a pointer in AGENTS.md:

```markdown
## Domain
See `docs/domain/<area>.md` for <brief description>.
```

**Never put domain knowledge into AGENTS.md itself** — only add a pointer.

## Integration with Other Skills

- **documenting-architecture**: Architecture docs reference domain concepts (e.g., "the auth module handles User authentication — see domain/users.md for the User entity definition")
- **documenting-business-processes**: Process docs describe flows between domain entities (e.g., "the registration process creates a User and assigns them to a Workspace")
- **documenting-components**: Component docs reference domain terms without redefining them
- **project-feature-planning**: The planning skill's Phase 2 benefits from domain docs — agents understand the business context without re-exploring code

## Rules

- **Never document the entire domain at once** — only the targeted area
- **Never define concepts from an implementation perspective** — describe what they ARE, not how they're stored
- **No code snippets** — domain docs describe the business model; component docs show the implementation
- **One definition per concept** — if a term is already defined in domain docs, other layers must reference it, not redefine it
- **Defer process details to process docs** — if a concept involves a multi-step flow (loading chain, resolution sequence, initialization steps), define the concept here and link to the process doc for the "how"
- **No behavioral conditionals** — if you're writing "when X happens", "in Y mode", or "if Z flag is set", that's a process description. Domain docs define static properties of concepts (what they are, what they contain, how they relate). Conditional behavior, modes, flags, and runtime decisions belong in process docs.
- **Use reference-style links** — when linking to other docs or source files, use reference links (`[text][ref]` with `[ref]: path` at the bottom of the file) rather than inline links. They read better in source and are easier to maintain.
- **Propose structure first** — if no domain docs exist yet, propose a directory structure and format to the user before creating files
