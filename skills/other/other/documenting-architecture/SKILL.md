---
name: documenting-architecture
description: Document system architecture, design decisions, layer boundaries, and how components connect and communicate. Use when (1) a project's architecture is undocumented, (2) agents can't figure out how the system fits together, (3) after major refactoring that changed system structure, or (4) onboarding developers who need to understand the big picture. References domain concepts — never redefines them.
---

# Documenting Architecture

Document how a system is designed: its layers, boundaries, communication patterns, and the rationale behind key design decisions. Architecture docs explain **how the system is built** and **why it was built that way**.

## Core Principles

1. **Decisions Over Descriptions**: The most valuable architecture documentation explains WHY, not just WHAT. "We use event-driven communication between services because X" is more useful than "services communicate via events."
2. **Boundary-Focused**: Emphasize where boundaries are drawn — between layers, modules, services. These are where misunderstandings cause the worst bugs.
3. **Accurate to the Code**: Document the architecture as it IS, not as it was designed to be. If the code has drifted from the original vision, document reality.
4. **No Duplication Across Levels**: Architecture docs reference domain concepts — they never redefine business terms. If you need to mention a domain entity, link to the domain docs. Similarly, don't describe individual component internals — that belongs in component docs.
5. **Discover, Don't Assume**: Read the code to understand the actual architecture. Don't project patterns onto it based on naming alone.

## Documentation Hierarchy

```
Domain              ← Defines business concepts (referenced by this layer)
  ↓
Architecture        ← You are here (system structure and design decisions)
  ↓
Business Processes  ← References architecture for "how the system implements this flow"
  ↓
Components          ← References architecture for "where this component fits"
```

## Workflow

### Step 1: Discover Existing Documentation

Before writing anything:

1. Check for existing architecture docs, ADRs (Architecture Decision Records), or design docs
2. Read AGENTS.md for pointers to existing documentation
3. Check for diagrams, READMEs in key directories, or informal architecture notes
4. **If architecture docs already exist**: Understand their structure and extend them

### Step 2: Analyze System Structure

Focus on the targeted area:

1. Identify the major layers or modules and their responsibilities
2. Trace the dependency graph — what depends on what, in which direction
3. Identify communication patterns — synchronous calls, events, shared state, message passing
4. Look for boundary enforcement — interfaces, ports, adapters, API contracts
5. Find key design decisions — patterns chosen (hexagonal, layered, CQRS, etc.) and evidence of why
6. Note where the architecture is inconsistent — places where different patterns coexist

**Stay within the requested scope.** If asked to document the API layer's architecture, don't document the entire system.

### Step 3: Write Architecture Documentation

Follow the project's existing doc style. If none exists, use this structure:

```markdown
# <System/Area> Architecture

## Overview
<What this system/area does and how it's structured — 3-5 sentences>

## Design Principles
<The guiding principles behind the architecture — what trade-offs were made and why>
- <Principle 1>: <rationale>
- <Principle 2>: <rationale>

## Structure

### <Layer/Module Name>
- **Responsibility**: <What this layer owns>
- **Boundaries**: <What it exposes, what it hides>
- **Dependencies**: <What it depends on — direction matters>

### <Another Layer/Module>
...

## Communication Patterns
<How layers/modules communicate with each other>
- <Pattern>: <where it's used and why>

## Key Design Decisions
<Important architectural choices and their rationale>

| Decision | Choice | Rationale | Alternatives Considered |
|----------|--------|-----------|------------------------|
| ...      | ...    | ...       | ...                    |

## Constraints
<Technical constraints, platform limitations, or organizational factors that shaped the architecture>
```

#### Mermaid Diagrams

Architecture docs should include a mermaid diagram showing how the major parts relate. Place it in or after the Structure section to give humans an instant visual overview.

Choose the diagram type based on what you're showing:

- **Flowchart** (`flowchart TD/LR`): Best for showing layers, dependency direction, and data flow between components.
- **Sequence diagram** (`sequenceDiagram`): Best when showing how components interact over time (e.g., request lifecycle).

Guidelines:
- Show structure and relationships, not process steps — those belong in process docs
- Use subgraphs to group layers or modules
- Label edges with what flows between components (data, calls, events)
- Keep it high-level — detailed internal flows belong in process or component docs

### Step 4: Update AGENTS.md Pointers

If new documentation files were created, propose adding a pointer in AGENTS.md:

```markdown
## Architecture
See `docs/architecture/<area>.md` for <brief description>.
```

**Never put architecture details into AGENTS.md itself** — only add a pointer.

## Integration with Other Skills

- **documenting-domain**: Architecture docs reference domain entities (e.g., "the auth layer manages User sessions — see domain/users.md"). Never redefine domain terms here.
- **documenting-business-processes**: Process docs explain how business workflows traverse the architecture
- **documenting-components**: Component docs explain internals; architecture docs explain how components relate to each other
- **project-feature-planning**: The planning skill's Phase 2 benefits enormously from architecture docs — agents understand system structure without reverse-engineering it from code

## Rules

- **Never document the entire system architecture at once** — only the targeted area
- **Never redefine domain concepts** — reference domain docs instead
- **Never describe component internals** — that belongs in component docs; architecture describes how components relate
- **Document reality, not aspirations** — if the code doesn't match the intended architecture, document what exists and note the drift
- **Rationale is mandatory** — every design decision must include "why", not just "what"
- **Use reference-style links** — when linking to other docs or source files, use reference links (`[text][ref]` with `[ref]: path` at the bottom of the file) rather than inline links. They read better in source and are easier to maintain.
- **Propose structure first** — if no architecture docs exist yet, propose a directory structure and format before creating files
