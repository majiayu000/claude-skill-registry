---
name: openfga
description: OpenFGA authorization modeling best practices and guidelines. This skill should be used when authoring, reviewing, or refactoring OpenFGA authorization models. Triggers on tasks involving OpenFGA models, relationship definitions, permission structures, .fga files, .fga.yaml test files, or OpenFGA SDK usage in JavaScript, TypeScript, Go, Python, Java, or .NET.
license: MIT
metadata:
  author: openfga
  version: "1.1.0"
---

# OpenFGA Best Practices

Comprehensive guide for authoring OpenFGA authorization models and using OpenFGA SDKs, maintained for AI agents and developers. Contains rules across 7 categories covering core concepts, relationship patterns, testing, custom roles, model optimization, and language-specific SDK usage.

## When to Apply

Reference these guidelines when:
- Creating new OpenFGA authorization models
- Defining types and relations in `.fga` files
- Writing relationship tuples
- Testing models with `.fga.yaml` files
- Implementing custom roles
- Reviewing or refactoring existing models
- Integrating OpenFGA with JavaScript/TypeScript, Go, Python, Java, or .NET applications

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Core Concepts | CRITICAL | `core-` |
| 2 | Relationship Definitions | CRITICAL | `relation-` |
| 3 | Testing & Validation | HIGH | `test-` |
| 4 | Model Design | HIGH | `design-` |
| 5 | Custom Roles | MEDIUM | `roles-` |
| 6 | Optimization | MEDIUM | `optimize-` |
| 7 | SDK Integration | HIGH | `sdk-` |
| 8 | Workflow | CRITICAL | `workflow-` |

## Quick Reference

### 1. Core Concepts (CRITICAL)

- `core-types` - Define types for all entity classes
- `core-schema-version` - Always use schema 1.1
- `core-relations` - Define relations on object types, not user types
- `core-tuples` - Write relationship tuples to establish facts
- `core-separation` - Separate schema (model) from data (tuples)

### 2. Relationship Definitions (CRITICAL)

- `relation-direct` - Use `[type]` for direct assignments
- `relation-concentric` - Use `or` for permission inheritance
- `relation-indirect` - Use `X from Y` for hierarchical access
- `relation-usersets` - Use `type#relation` for group-based access
- `relation-conditions` - Use CEL conditions for contextual authorization
- `relation-wildcards` - Use `type:*` for public access carefully
- `relation-wildcards-as-booleans` - To use `type:*`to model boolan attributes

### 3. Model Design (HIGH)

- `design-permissions` - Define `can_*` relations for permissions
- `design-hierarchy` - Model parent-child relationships correctly
- `design-organization` - Structure organization-level access
- `design-naming` - Use clear, consistent naming conventions
- `design-modules` - Split a model in modules for collaboration among multiple teams.

### 4. Testing & Validation (HIGH)

- `test-fga-yaml` - Structure tests in `.fga.yaml` files
- `test-check-assertions` - Write check assertions for permission verification
- `test-list-objects` - Test list_objects queries
- `test-list-users` - Test list_users queries
- `test-conditions` - Test conditional relationships with context
- `test-cli` - Use OpenFGA CLI for model testing

### 5. Custom Roles (MEDIUM)

- `roles-simple` - Implement simple user-defined roles
- `roles-assignments` - Use role assignments for resource-specific roles
- `roles-static-combo` - Combine static and custom roles
- `roles-when-to-use` - Choose the right role pattern

### 6. Optimization (MEDIUM)

- `optimize-simplify` - Remove unused types and relations
- `optimize-tuples` - Use indirect relationships to reduce tuple count
- `optimize-type-restrictions` - Apply appropriate type restrictions

### 7. SDK Integration (HIGH)

- `sdk-javascript` - JavaScript/TypeScript SDK usage
- `sdk-go` - Go SDK usage
- `sdk-python` - Python SDK usage (async and sync)
- `sdk-java` - Java SDK usage
- `sdk-dotnet` - .NET SDK usage

### 8. Workflow (CRITICAL)

- `workflow-validate` - Always validate models before delivery

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/core-types.md
rules/relation-concentric.md
rules/test-fga-yaml.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
