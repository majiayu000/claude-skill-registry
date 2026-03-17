---
name: architecture-validator
description: Validate hexagonal architecture (Domain, Application, Infrastructure, Presentation). Use when creating new files in src/, reorganizing code, or when the user requests architecture validation.
---

# Architecture Validator

You validate compliance with **hexagonal architecture** (ports & adapters).

## Reference

Complete hexagonal architecture (structure, rules, dependencies, injection) is documented in `.claude/rules/architecture.md`.

**You MUST read this file** to understand the exact structure and rules.

## Verification Commands

See [examples.md](./examples.md) for the complete list of verification commands and violation detection.

## TypeScript Strict

- [ ] No `any` : type all parameters and returns
- [ ] No `!` non-null assertion : use optional types or guards
- [ ] `tsconfig.json` : `"strict": true`

## Validation Report

After verification, generate a structured report. See [examples.md](./examples.md) for the complete template.

## Checklist

- [ ] No Domain → Infrastructure imports
- [ ] Domain Interfaces ← Infrastructure Implementations
- [ ] Application services inject dependencies
- [ ] TypeScript strict (no `any`)
- [ ] Layers semantically distinct

## See Also

- **[test-writer](../test-writer/SKILL.md)** — Write tests that respect architecture boundaries. Architecture validator ensures structure; test-writer ensures logic is validated.
- **[e2e-writer](../e2e-writer/SKILL.md)** — E2E tests depend on proper architectural layers (presentation calls application, application calls infrastructure). Use architecture-validator to verify this structure.
- **[accessibility-checker](../accessibility-checker/SKILL.md)** — Accessible components are properly structured in presentation layer. Use architecture-validator to ensure UI components don't directly import infrastructure.
