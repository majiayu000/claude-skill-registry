---
name: js-google
description: JavaScript style and best practices based on Google's official JavaScript Style Guide. This skill should be used when writing, reviewing, or refactoring JavaScript code to ensure consistent style and prevent common bugs. Triggers on tasks involving JavaScript, ES6, modules, JSDoc, naming conventions, or code formatting.
---

# Google JavaScript Best Practices

Comprehensive JavaScript style and best practices guide based on Google's official JavaScript Style Guide, designed for AI agents and LLMs. Contains 47 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new JavaScript or ES6+ code
- Structuring modules and managing imports/exports
- Adding JSDoc type annotations and documentation
- Reviewing code for naming and style consistency
- Refactoring existing JavaScript code

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Module System & Imports | CRITICAL | `module-` |
| 2 | Language Features | CRITICAL | `lang-` |
| 3 | Type Safety & JSDoc | HIGH | `type-` |
| 4 | Naming Conventions | HIGH | `naming-` |
| 5 | Control Flow & Error Handling | MEDIUM-HIGH | `control-` |
| 6 | Functions & Parameters | MEDIUM | `func-` |
| 7 | Objects & Arrays | MEDIUM | `data-` |
| 8 | Formatting & Style | LOW | `format-` |

## Quick Reference

### 1. Module System & Imports (CRITICAL)

- [`module-avoid-circular-dependencies`](references/module-avoid-circular-dependencies.md) - Prevent loading failures from circular imports
- [`module-file-extension-in-imports`](references/module-file-extension-in-imports.md) - Include .js extension in import paths
- [`module-named-exports-over-default`](references/module-named-exports-over-default.md) - Prefer named exports for consistency
- [`module-no-duplicate-imports`](references/module-no-duplicate-imports.md) - Import from same file only once
- [`module-no-import-aliasing`](references/module-no-import-aliasing.md) - Keep original export names
- [`module-source-file-structure`](references/module-source-file-structure.md) - Follow standard file structure order

### 2. Language Features (CRITICAL)

- [`lang-const-over-let-over-var`](references/lang-const-over-let-over-var.md) - Use const by default, never var
- [`lang-es6-classes-over-prototypes`](references/lang-es6-classes-over-prototypes.md) - Use class syntax over prototype manipulation
- [`lang-explicit-semicolons`](references/lang-explicit-semicolons.md) - Always use explicit semicolons
- [`lang-no-eval`](references/lang-no-eval.md) - Never use eval or Function constructor
- [`lang-no-modify-builtins`](references/lang-no-modify-builtins.md) - Never modify built-in prototypes
- [`lang-no-non-standard-features`](references/lang-no-non-standard-features.md) - Use only standard ECMAScript features
- [`lang-no-primitive-wrappers`](references/lang-no-primitive-wrappers.md) - Never use primitive wrapper objects
- [`lang-no-with-statement`](references/lang-no-with-statement.md) - Never use the with statement

### 3. Type Safety & JSDoc (HIGH)

- [`type-cast-with-parentheses`](references/type-cast-with-parentheses.md) - Use parentheses for type casts
- [`type-enum-annotations`](references/type-enum-annotations.md) - Annotate enums with static literal values
- [`type-explicit-nullability`](references/type-explicit-nullability.md) - Use explicit nullability modifiers
- [`type-jsdoc-required-for-exports`](references/type-jsdoc-required-for-exports.md) - Require JSDoc for exported functions
- [`type-template-parameters`](references/type-template-parameters.md) - Always specify template parameters
- [`type-typedef-for-complex-types`](references/type-typedef-for-complex-types.md) - Use typedef for complex object types

### 4. Naming Conventions (HIGH)

- [`naming-constant-case-for-constants`](references/naming-constant-case-for-constants.md) - Use CONSTANT_CASE for immutable values
- [`naming-descriptive-over-brief`](references/naming-descriptive-over-brief.md) - Prefer descriptive names over brevity
- [`naming-file-naming-conventions`](references/naming-file-naming-conventions.md) - Use lowercase with dashes or underscores
- [`naming-lowercamelcase-for-methods`](references/naming-lowercamelcase-for-methods.md) - Use lowerCamelCase for methods and variables
- [`naming-no-dollar-prefix`](references/naming-no-dollar-prefix.md) - Avoid dollar sign prefix in identifiers
- [`naming-uppercamelcase-for-classes`](references/naming-uppercamelcase-for-classes.md) - Use UpperCamelCase for classes

### 5. Control Flow & Error Handling (MEDIUM-HIGH)

- [`control-comment-empty-catch`](references/control-comment-empty-catch.md) - Document empty catch blocks
- [`control-for-of-over-for-in`](references/control-for-of-over-for-in.md) - Prefer for-of over for-in
- [`control-strict-equality`](references/control-strict-equality.md) - Use strict equality except for null checks
- [`control-switch-default-last`](references/control-switch-default-last.md) - Always include default case in switch
- [`control-throw-error-objects`](references/control-throw-error-objects.md) - Always throw Error objects

### 6. Functions & Parameters (MEDIUM)

- [`func-arrow-functions-for-nested`](references/func-arrow-functions-for-nested.md) - Prefer arrow functions for nested functions
- [`func-arrow-parentheses`](references/func-arrow-parentheses.md) - Always use parentheses around arrow params
- [`func-default-parameters`](references/func-default-parameters.md) - Use default parameters instead of conditionals
- [`func-rest-parameters-over-arguments`](references/func-rest-parameters-over-arguments.md) - Use rest parameters over arguments
- [`func-spread-over-apply`](references/func-spread-over-apply.md) - Use spread operator instead of apply

### 7. Objects & Arrays (MEDIUM)

- [`data-array-literals-over-constructor`](references/data-array-literals-over-constructor.md) - Use array literals over Array constructor
- [`data-destructuring-for-multiple-values`](references/data-destructuring-for-multiple-values.md) - Use destructuring for multiple properties
- [`data-no-mixing-quoted-unquoted-keys`](references/data-no-mixing-quoted-unquoted-keys.md) - Never mix quoted and unquoted keys
- [`data-object-literals-over-constructor`](references/data-object-literals-over-constructor.md) - Use object literals over constructor
- [`data-spread-over-concat-slice`](references/data-spread-over-concat-slice.md) - Use spread over concat and slice
- [`data-trailing-commas`](references/data-trailing-commas.md) - Use trailing commas in multi-line literals

### 8. Formatting & Style (LOW)

- [`format-braces-required`](references/format-braces-required.md) - Always use braces for control structures
- [`format-column-limit`](references/format-column-limit.md) - Limit lines to 80 characters
- [`format-one-statement-per-line`](references/format-one-statement-per-line.md) - Place one statement per line
- [`format-single-quotes`](references/format-single-quotes.md) - Use single quotes for string literals
- [`format-two-space-indent`](references/format-two-space-indent.md) - Use two-space indentation

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Full Compiled Document

For a complete compiled guide with all rules, see [AGENTS.md](AGENTS.md).

## Reference Files

| File | Description |
|------|-------------|
| [AGENTS.md](AGENTS.md) | Complete compiled guide with all rules |
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
