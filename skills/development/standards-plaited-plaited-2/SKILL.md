---
name: standards
description: Plaited code conventions and development standards. Use when writing or editing TypeScript code in Plaited projects, following code conventions (type system, function style, imports), generating code, or verifying code quality.
license: ISC
compatibility: Requires bun
---

# Plaited Standards

## Purpose

This skill provides code conventions and development standards that apply to **all** Plaited code—whether behavioral programs, UI templates, utilities, or tests.

**Use this when:**
- Writing or editing TypeScript code in Plaited projects
- Following Plaited code conventions
- Generating code for Plaited applications
- Verifying code quality before presenting to users
- Understanding import path standards
- Applying the 95% confidence threshold

## Quick Reference

| Reference | Use For |
|-----------|---------|
| [code-conventions.md](references/code-conventions.md) | Type system, function style, templates, imports, null handling |
| [standards.md](references/standards.md) | 95% confidence threshold, documentation guidelines, Bun APIs |
| [verification-workflow.md](references/verification-workflow.md) | Complete code generation workflow |

## Code Conventions

**[code-conventions.md](references/code-conventions.md)**

### Type System
- Prefer `type` over `interface`
- Use `type` for object shapes, unions, intersections
- Use arrow functions over function declarations

### Function Style
- Arrow functions for all functions
- Object parameters for functions with 2+ parameters
- Destructure in function signature

### Templates
- JSX syntax only (not `h()` or `createTemplate()`)
- Use "template" not "component"

### Imports
- Package imports in tests: `'plaited'`, `'plaited/ui'`, `'plaited/testing'`
- `plaited` for behavioral programming (useBehavioral, useSignal, useWorker)
- `plaited/ui` for templates and custom elements (bElement, createStyles, FT)
- Relative imports within packages

### Null Handling
- Prefer `undefined` over `null`
- Use optional chaining and nullish coalescing

## Development Standards

**[standards.md](references/standards.md)**

### 95% Confidence Threshold
- Verify information before stating implementation details
- Read files in real-time to verify accuracy
- Use typescript-lsp@plaited_development-skills skill for type verification
- Report uncertainty rather than guess

### Documentation Guidelines
- TSDoc for public APIs
- No `@example` sections (tests/stories are living examples)
- Use `@internal` for non-public APIs

### Bun Platform APIs
- Prefer Bun native APIs over Node.js equivalents
- Use `Bun.file()`, `Bun.write()`, `Bun.spawn()`
- Use `bun:test` for testing

## Verification Workflow

**[verification-workflow.md](references/verification-workflow.md)**

### Code Generation Phases

1. **API Verification** - Check imports, verify types with LSP
2. **Code Generation** - Apply patterns from framework skills
3. **Post-Generation Validation** - Verify against standards

### Confidence Protocol

```
Before presenting code:
1. Verify all imports exist
2. Confirm type signatures with LSP
3. Check patterns against skill references
4. Only present if 95%+ confident
```

## Terminology

Plaited is a **template-driven** framework:
- Use "template" not "component"
- Use "behavioral element" or "bElement" for interactive elements
- Refer to browser APIs by specific names (Custom Elements, Shadow DOM)

## Related Skills

- **behavioral-core** - BP coordination patterns
- **ui-patterns** - Templates, bElements, styling
- **typescript-lsp@plaited_development-skills** - Type verification and symbol discovery
- **code-documentation@plaited_development-skills** - TSDoc writing standards
