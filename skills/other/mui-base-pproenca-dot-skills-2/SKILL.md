---
name: mui-base
description: MUI Base UI style guidelines for building headless React component libraries (formerly headless-ui-style). This skill should be used when creating unstyled UI components, compound components with render props, accessibility-first patterns, or component libraries that separate logic from styling. Extracted from the MUI Base UI codebase (github.com/mui/base-ui).
---

# MUI Headless UI Best Practices

Comprehensive style guide for building headless React component libraries following MUI Base UI patterns. Contains 48 rules across 5 categories, prioritized by impact.

## When to Apply

Reference these guidelines when:
- Building headless/unstyled component libraries
- Creating compound components with context-based composition
- Implementing accessible UI primitives with ARIA patterns
- Using render props and className callbacks for styling flexibility
- Writing components that support both controlled and uncontrolled modes

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Component Patterns | CRITICAL | `comp-` |
| 2 | Naming Conventions | HIGH | `name-` |
| 3 | Organization | HIGH | `org-` |
| 4 | Error Handling | HIGH | `err-` |
| 5 | Style | MEDIUM | `style-` |

## Quick Reference

### 1. Component Patterns (CRITICAL)

- `comp-forward-ref-named` - Use forwardRef with Named Function
- `comp-props-parameter-naming` - Name Props Parameter componentProps
- `comp-use-render-element` - Use useRenderElement for DOM Rendering
- `comp-context-undefined-default` - Create Context with Undefined Default
- `comp-context-error-message` - Context Error Messages with Hierarchy
- `comp-use-controlled` - Use useControlled Hook for Dual Modes
- `comp-state-memoization` - Memoize State Objects
- `comp-context-value-memo` - Memoize Context Provider Values
- `comp-plain-function-root` - Plain Function for Non-DOM Roots
- `comp-hook-namespace-exports` - Hook Namespace Exports
- `comp-props-destructure-order` - Props Destructuring Order
- `comp-use-client-directive` - Add use client Directive

### 2. Naming Conventions (HIGH)

- `name-component-naming` - Component Naming as ParentPart
- `name-file-matches-export` - File Name Matches Primary Export
- `name-directory-kebab-case` - Directory Naming kebab-case
- `name-part-directory-lowercase` - Part Directory Naming lowercase
- `name-context-suffix` - Context Naming with Suffix
- `name-context-hook` - Context Hook as useComponentContext
- `name-props-interface` - Props Interface as ComponentProps
- `name-state-interface` - State Interface as ComponentState
- `name-namespace-type-exports` - Namespace Type Exports
- `name-event-type` - Event Type Naming Convention
- `name-constants` - Constant Naming SCREAMING_SNAKE_CASE
- `name-data-attributes` - Data Attribute Naming lowercase
- `name-hooks` - Hook Naming with use Prefix
- `name-refs` - Ref Variable Naming with Suffix
- `name-handlers` - Handler Naming Convention

### 3. Organization (HIGH)

- `org-component-directory` - Component Directory Structure
- `org-dual-barrel-exports` - Dual Barrel Export Pattern
- `org-test-colocation` - Test File Colocation
- `org-context-placement` - Context File Placement
- `org-data-attributes-file` - Data Attributes Documentation File
- `org-state-attributes-mapping` - State Attributes Mapping File
- `org-css-vars-file` - CSS Variables Documentation File
- `org-package-exports` - Package-Level Wildcard Exports

### 4. Error Handling (HIGH)

- `err-dev-only-warnings` - Development-Only Warnings
- `err-deduplicated-warnings` - Deduplicated Warning Messages
- `err-message-prefix` - Message Prefix Standard
- `err-context-error-guidance` - Context Error Guidance
- `err-prop-validation-timing` - Prop Validation Timing
- `err-cancelable-events` - Cancelable Event Pattern
- `err-event-reason-constants` - Event Reason Constants
- `err-typed-event-reasons` - Type-Safe Event Reasons

### 5. Style (MEDIUM)

- `style-react-import` - React Import as Namespace
- `style-internal-imports` - Internal Import Paths
- `style-explicit-undefined` - Explicit Undefined in Prop Types
- `style-default-values` - Default Values in Destructuring
- `style-jsdoc-documentation` - JSDoc Documentation

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules
- Example: [comp-forward-ref-named](references/comp-forward-ref-named.md)
- Example: [org-component-directory](references/org-component-directory.md)

## Source

Extracted from [MUI Base UI](https://github.com/mui/base-ui) codebase on 2026-01-17.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
