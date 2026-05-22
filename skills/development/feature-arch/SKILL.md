---
name: feature-arch
description: React feature-based architecture guidelines for scalable applications (formerly feature-architecture). This skill should be used when writing, reviewing, or refactoring React code to ensure proper feature organization. Triggers on tasks involving project structure, feature organization, module boundaries, cross-feature imports, data fetching patterns, or component composition.
---

# Feature-Based Architecture Best Practices

Comprehensive architecture guide for organizing React applications by features, enabling scalable development with independent teams. Contains 42 rules across 8 categories, prioritized by impact from critical (directory structure, imports) to incremental (naming conventions).

## When to Apply

Reference these guidelines when:
- Creating new features or modules
- Organizing project directory structure
- Setting up import rules and boundaries
- Implementing data fetching patterns
- Composing components from multiple features
- Reviewing code for architecture violations

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Directory Structure | CRITICAL | `struct-` |
| 2 | Import & Dependencies | CRITICAL | `import-` |
| 3 | Module Boundaries | HIGH | `bound-` |
| 4 | Data Fetching | HIGH | `fquery-` |
| 5 | Component Organization | MEDIUM-HIGH | `fcomp-` |
| 6 | State Management | MEDIUM | `fstate-` |
| 7 | Testing Strategy | MEDIUM | `test-` |
| 8 | Naming Conventions | LOW | `name-` |

## Quick Reference

### 1. Directory Structure (CRITICAL)

- `struct-feature-folders` - Organize by feature, not technical type
- `struct-feature-self-contained` - Make features self-contained
- `struct-shared-layer` - Use shared layer for truly generic code only
- `struct-flat-hierarchy` - Keep directory hierarchy flat
- `struct-optional-segments` - Include only necessary segments
- `struct-app-layer` - Separate app layer from features

### 2. Import & Dependencies (CRITICAL)

- `import-unidirectional-flow` - Enforce unidirectional import flow
- `import-no-cross-feature` - Prohibit cross-feature imports
- `import-public-api` - Export through public API only
- `import-avoid-barrel-files` - Avoid deep barrel file re-exports
- `import-path-aliases` - Use consistent path aliases
- `import-type-only` - Use type-only imports for types

### 3. Module Boundaries (HIGH)

- `bound-feature-isolation` - Enforce feature isolation
- `bound-interface-contracts` - Define explicit interface contracts
- `bound-feature-scoped-routing` - Scope routing to feature concerns
- `bound-minimize-shared-state` - Minimize shared state between features
- `bound-event-based-communication` - Use events for cross-feature communication
- `bound-feature-size` - Keep features appropriately sized

### 4. Data Fetching (HIGH)

- `fquery-single-responsibility` - Keep query functions single-purpose
- `fquery-colocate-with-feature` - Colocate data fetching with features
- `fquery-parallel-fetching` - Fetch independent data in parallel
- `fquery-avoid-n-plus-one` - Avoid N+1 query patterns
- `fquery-feature-scoped-keys` - Use feature-scoped query keys
- `fquery-server-component-fetching` - Fetch at server component level

### 5. Component Organization (MEDIUM-HIGH)

- `fcomp-single-responsibility` - Apply single responsibility to components
- `fcomp-composition-over-props` - Prefer composition over prop drilling
- `fcomp-container-presentational` - Separate container and presentational concerns
- `fcomp-props-as-data-boundary` - Use props as feature boundaries
- `fcomp-colocate-styles` - Colocate styles with components
- `fcomp-error-boundaries` - Use feature-level error boundaries

### 6. State Management (MEDIUM)

- `fstate-feature-scoped-stores` - Scope state stores to features
- `fstate-server-state-separation` - Separate server state from client state
- `fstate-lift-minimally` - Lift state only as high as necessary
- `fstate-context-sparingly` - Use context sparingly for feature state
- `fstate-reset-on-unmount` - Reset feature state on unmount

### 7. Testing Strategy (MEDIUM)

- `test-colocate-with-feature` - Colocate tests with features
- `test-feature-isolation` - Test features in isolation
- `test-shared-utilities` - Create feature-specific test utilities
- `test-integration-at-app-layer` - Write integration tests at app layer

### 8. Naming Conventions (LOW)

- `name-feature-naming` - Use domain-driven feature names
- `name-file-conventions` - Use consistent file naming conventions
- `name-descriptive-exports` - Use descriptive export names

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules
- Individual rules: `references/{prefix}-{slug}.md`

## Related Skills

- For feature planning, see `feature-spec` skill
- For data fetching, see `tanstack-query` skill
- For React component patterns, see `react-19` skill

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
