---
name: ts-google
description: Google TypeScript style guide for writing clean, consistent, type-safe code. This skill should be used when writing, reviewing, or refactoring TypeScript code. Triggers on TypeScript files, type annotations, module imports, class design, and code style decisions.
---

# Google TypeScript Best Practices

Comprehensive TypeScript style guide based on Google's internal standards, designed for AI agents and LLMs. Contains 45 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new TypeScript code
- Organizing modules and imports
- Designing type annotations and interfaces
- Creating classes and functions
- Reviewing code for style consistency
- Refactoring existing TypeScript code

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Module Organization | CRITICAL | `module-` |
| 2 | Type Safety | CRITICAL | `types-` |
| 3 | Class Design | HIGH | `class-` |
| 4 | Function Patterns | HIGH | `func-` |
| 5 | Control Flow | MEDIUM-HIGH | `control-` |
| 6 | Error Handling | MEDIUM | `error-` |
| 7 | Naming & Style | MEDIUM | `naming-` |
| 8 | Literals & Coercion | LOW-MEDIUM | `literal-` |

## Quick Reference

### 1. Module Organization (CRITICAL)

- [`module-named-exports`](references/module-named-exports.md) - Use named exports over default exports
- [`module-no-mutable-exports`](references/module-no-mutable-exports.md) - Avoid mutable exports
- [`module-es6-modules`](references/module-es6-modules.md) - Use ES6 modules exclusively
- [`module-no-namespaces`](references/module-no-namespaces.md) - Avoid TypeScript namespaces
- [`module-import-paths`](references/module-import-paths.md) - Use relative paths for project imports
- [`module-import-type`](references/module-import-type.md) - Use import type for type-only imports
- [`module-export-api-surface`](references/module-export-api-surface.md) - Minimize exported API surface

### 2. Type Safety (CRITICAL)

- [`types-no-any`](references/types-no-any.md) - Never use the any type
- [`types-prefer-interfaces`](references/types-prefer-interfaces.md) - Prefer interfaces over type aliases for objects
- [`types-explicit-structural`](references/types-explicit-structural.md) - Explicitly annotate structural types
- [`types-nullable-patterns`](references/types-nullable-patterns.md) - Handle nullable types correctly
- [`types-array-syntax`](references/types-array-syntax.md) - Use consistent array type syntax
- [`types-no-wrapper-types`](references/types-no-wrapper-types.md) - Never use wrapper object types
- [`types-prefer-map-set`](references/types-prefer-map-set.md) - Prefer Map and Set over index signatures
- [`types-no-empty-object`](references/types-no-empty-object.md) - Avoid empty object type

### 3. Class Design (HIGH)

- [`class-parameter-properties`](references/class-parameter-properties.md) - Use parameter properties for constructor assignment
- [`class-readonly-properties`](references/class-readonly-properties.md) - Mark properties readonly when never reassigned
- [`class-no-private-fields`](references/class-no-private-fields.md) - Use TypeScript private over private fields
- [`class-no-static-containers`](references/class-no-static-containers.md) - Avoid container classes with only static members
- [`class-constructor-parens`](references/class-constructor-parens.md) - Always use parentheses in constructor calls
- [`class-no-prototype-manipulation`](references/class-no-prototype-manipulation.md) - Never manipulate prototypes directly

### 4. Function Patterns (HIGH)

- [`func-declarations-over-expressions`](references/func-declarations-over-expressions.md) - Prefer function declarations over expressions
- [`func-arrow-concise-bodies`](references/func-arrow-concise-bodies.md) - Use concise arrow function bodies appropriately
- [`func-avoid-this-rebinding`](references/func-avoid-this-rebinding.md) - Avoid rebinding this
- [`func-rest-parameters`](references/func-rest-parameters.md) - Use rest parameters over arguments
- [`func-generator-syntax`](references/func-generator-syntax.md) - Use correct generator function syntax
- [`func-default-parameters`](references/func-default-parameters.md) - Use default parameters sparingly

### 5. Control Flow (MEDIUM-HIGH)

- [`control-always-use-braces`](references/control-always-use-braces.md) - Always use braces for control structures
- [`control-triple-equals`](references/control-triple-equals.md) - Always use triple equals
- [`control-for-of-iteration`](references/control-for-of-iteration.md) - Prefer for-of over for-in for arrays
- [`control-switch-default`](references/control-switch-default.md) - Always include default case in switch
- [`control-no-assignment-in-condition`](references/control-no-assignment-in-condition.md) - Avoid assignment in conditional expressions

### 6. Error Handling (MEDIUM)

- [`error-throw-errors`](references/error-throw-errors.md) - Always throw Error instances
- [`error-catch-unknown`](references/error-catch-unknown.md) - Type catch clause variables as unknown
- [`error-empty-catch-comments`](references/error-empty-catch-comments.md) - Document empty catch blocks
- [`error-avoid-assertions`](references/error-avoid-assertions.md) - Avoid type and non-null assertions

### 7. Naming & Style (MEDIUM)

- [`naming-identifier-styles`](references/naming-identifier-styles.md) - Use correct identifier naming styles
- [`naming-descriptive-names`](references/naming-descriptive-names.md) - Use descriptive names
- [`naming-no-decorative-underscores`](references/naming-no-decorative-underscores.md) - Avoid decorative underscores
- [`naming-no-interface-prefix`](references/naming-no-interface-prefix.md) - No I prefix for interfaces
- [`naming-constants`](references/naming-constants.md) - Use CONSTANT_CASE for true constants

### 8. Literals & Coercion (LOW-MEDIUM)

- [`literal-single-quotes`](references/literal-single-quotes.md) - Use single quotes for strings
- [`literal-number-formats`](references/literal-number-formats.md) - Use correct number literal formats
- [`literal-explicit-coercion`](references/literal-explicit-coercion.md) - Use explicit type coercion
- [`literal-array-constructor`](references/literal-array-constructor.md) - Avoid Array constructor

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
