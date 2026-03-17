---
name: structure-boundaries
description: "Use when project structure makes ownership or dependency boundaries hard to infer and navigation cost is high. Goal: project structure makes responsibilities and dependency boundaries legible."
---

# Structure Boundaries

Restructure a project so responsibilities and dependency direction are readable from the directory tree and boundary-crossing imports.

## Response Contract

- Deliverable: apply the requested changes to the target artifact.
- Chat output: no additional output beyond the deliverable.

## Structure Model

### Directory meaning

Each directory level should communicate exactly one meaning.

#### Collection

Children are interchangeable items of the same kind.

#### Roles

Children are distinct responsibilities within a fixed set.

## Standards

Apply these standards throughout the edit. Each standard is single-sourced here and referenced elsewhere by its ID.

- **levels.one_meaning — One meaning per level**
  Each directory level is either a Collection or Roles level. Do not mix meanings at the same level.

- **shape.flat — Prefer shallow structure**
  Add a subdirectory only when it reflects a real grouping or a clear sub-responsibility.

- **naming.context — Context-aware naming**
  Names should express the responsibility of the item without repeating what the parent already implies. Avoid catch-all buckets unless their responsibility is explicit and stable.

- **imports.crossing_visible — Make boundary crossing visible**
  Import forms must make boundary crossing easy to detect. Avoid upward relative imports that traverse out of the current subtree, for example `..`, because they hide crossings. Use an import form that makes the crossed boundary explicit.

- **deps.direction_readable — Dependency direction is readable**
  The structure and imports should collectively imply a consistent dependency direction. Treat reverse or cyclic cross-boundary dependencies as boundary violations to address.

- **shared.kit — Boundary-scoped shared code**
  Use `…kit` to hold shared support code within a specific boundary. `…kit` is not a new domain; it is support code for that boundary.

- **shared.utils — Domain-free utilities**
  Use `utils` only for domain-free primitives: no domain terminology and no dependencies on domain or layer code. If code carries domain meaning or belongs to a boundary, place it in that boundary or its `…kit`.

## Workflow

1. Inspect the tree and imports to identify blurred responsibilities and hidden boundary crossings.
2. Classify each directory level as Collection or Roles; restructure or rename to remove ambiguity. Apply `levels.one_meaning`.
3. Flatten over-nesting and introduce subdirectories only when they represent a real grouping or stable sub-responsibility. Apply `shape.flat`.
4. Fix naming so responsibilities are explicit given directory context, and buckets are eliminated or made precise. Apply `naming.context`.
5. Adjust import conventions so boundary crossings are obvious, then address violations of dependency direction. Apply `imports.crossing_visible`, `deps.direction_readable`.
6. Place shared code into the correct boundary (`…kit`) or domain-free `utils` as appropriate. Apply `shared.kit`, `shared.utils`.
7. Apply the moves, renames, and import updates needed to satisfy the standards.

## Acceptance Criteria

A revision is complete only if all checks pass.

- **Response**: Output satisfies the Response Contract.
- **Standards satisfied**: `levels.one_meaning`, `shape.flat`, `naming.context`, `imports.crossing_visible`, `deps.direction_readable`, `shared.kit`, `shared.utils`.
