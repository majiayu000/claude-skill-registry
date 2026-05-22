---
name: react-principle-engineer
description: React development principles from official documentation. Teaches component purity, state management, effects, refs, reducers, context, and event handling patterns. Use when writing React components with hooks, managing state, synchronizing with external systems, debugging re-renders, or choosing between state management approaches.
---

# React Core Team React Principles Best Practices

Comprehensive React development principles extracted from the official React documentation. Contains 52 rules across 8 categories prioritized by impact on code quality and maintainability.

## When to Apply

Reference these guidelines when:
- Writing React components with hooks
- Managing component and application state
- Synchronizing with external systems (APIs, browser APIs)
- Debugging unexpected re-renders or stale state
- Structuring state for complex UIs
- Deciding between state, refs, context, and reducers

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Component Purity | HIGH | `pure-` |
| 2 | State Structure | HIGH | `state-` |
| 3 | State Sharing | HIGH | `share-` |
| 4 | Effect Patterns | HIGH | `effect-` |
| 5 | Refs Usage | MEDIUM | `ref-` |
| 6 | Reducer Patterns | MEDIUM | `reducer-` |
| 7 | Context Patterns | MEDIUM | `context-` |
| 8 | Event Handling | MEDIUM | `event-` |

## Quick Reference

### 1. Component Purity (HIGH)

- `pure-no-external-mutations` - Never mutate external variables during render
- `pure-same-inputs-same-outputs` - Same props/state always produce same JSX
- `pure-local-mutation-allowed` - Local mutation during render is fine
- `pure-strict-mode-detection` - Use StrictMode to catch purity violations
- `pure-side-effects-in-handlers` - Put side effects in event handlers
- `pure-props-as-readonly` - Treat props as immutable snapshots
- `pure-render-independence` - Render order shouldn't matter
- `pure-use-effect-last-resort` - Effects are escape hatches, not primary pattern
- `pure-why-purity-matters` - Pure components enable React's features

### 2. State Structure (HIGH)

- `state-group-related` - Group related state variables together
- `state-avoid-contradictions` - Avoid contradictory state (use enums)
- `state-avoid-redundant` - Don't store values that can be derived
- `state-avoid-duplication` - Store IDs, not duplicate objects
- `state-flatten-nested` - Flatten deeply nested state
- `state-no-mirror-props` - Don't initialize state from props
- `state-immutable-updates` - Always create new objects/arrays
- `state-snapshot-behavior` - State is a snapshot at render time
- `state-updater-functions` - Use updaters for sequential updates
- `state-keys-reset` - Use key to reset component state

### 3. State Sharing (HIGH)

- `share-lift-state-up` - Lift state to nearest common ancestor
- `share-single-source-truth` - One source of truth for each piece
- `share-controlled-uncontrolled` - Controlled vs uncontrolled patterns
- `share-props-down-events-up` - Props flow down, events bubble up
- `share-composition-over-drilling` - Use composition to avoid drilling
- `share-preserve-reset-identity` - Component identity affects state

### 4. Effect Patterns (HIGH)

- `effect-synchronization` - Effects sync with external systems
- `effect-cleanup` - Always provide cleanup functions
- `effect-dependencies` - Include all dependencies in array
- `effect-separate-concerns` - Separate independent synchronizations
- `effect-think-sync-not-lifecycle` - Think sync/unsync, not mount/unmount
- `effect-not-for-derived-state` - Don't use effects for derived state
- `effect-not-for-events` - Don't use effects for event responses
- `effect-data-fetching` - Proper patterns for data fetching
- `effect-never-suppress-linter` - Never suppress dependency warnings
- `effect-remove-unnecessary` - Remove effects that don't need to be effects

### 5. Refs Usage (MEDIUM)

- `ref-escape-hatch` - Refs are escape hatches from React
- `ref-no-render-access` - Don't read/write refs during render
- `ref-dom-manipulation` - Use refs for DOM manipulation
- `ref-mutable-values` - Refs for mutable values like timers
- `ref-best-practices` - When to use refs vs state

### 6. Reducer Patterns (MEDIUM)

- `reducer-when-to-use` - When to use reducers over useState
- `reducer-actions` - Actions describe what happened
- `reducer-pure-functions` - Reducers must be pure
- `reducer-structure` - Standard reducer structure patterns
- `reducer-extract-from-component` - Extract reducers to separate files

### 7. Context Patterns (MEDIUM)

- `context-when-to-use` - When to use context vs props
- `context-create-use-provide` - Create, use, provide pattern
- `context-with-reducer` - Combine context with reducers
- `context-default-values` - Meaningful default values

### 8. Event Handling (MEDIUM)

- `event-pass-handlers` - Pass handlers, don't call them inline
- `event-side-effects` - Side effects belong in handlers
- `event-propagation` - Event propagation and stopPropagation
- `event-naming` - Handler naming conventions (handle/on)

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- Example rules: [pure-no-external-mutations](references/pure-no-external-mutations.md), [effect-synchronization](references/effect-synchronization.md)

## Full Compiled Document

For the complete guide with all rules expanded: [AGENTS.md](AGENTS.md)
