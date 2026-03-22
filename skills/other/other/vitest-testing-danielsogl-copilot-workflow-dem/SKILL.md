---
name: vitest-testing
description: Project-specific testing patterns using Vitest with Angular TestBed. Activates when writing tests, discussing test setup, creating spec files, mocking dependencies, or running tests.
---

# Vitest Testing (Project-Specific)

For complete testing patterns, read `.github/instructions/angular-testing.instructions.md`.
For NgRx store testing, read `.github/instructions/ngrx-signals-testing.instructions.md`.

## Quick Reference

```bash
npm test              # Run all unit tests
npm test -- --watch   # Watch mode
```

## Mandatory Rules

- **`provideZonelessChangeDetection()`** in every test setup
- **Vitest globals** pre-configured — never import `describe`, `it`, `expect`, `vi`
- **Signal inputs** set via `componentRef.setInput('name', value)`
- **AAA pattern** — Arrange, Act, Assert
- **No `any`** — properly type all mocks

## Reference Tests

- Component: `src/app/features/tasks/ui/task-card/task-card.spec.ts`
- Service: `src/app/features/tasks/data/infrastructure/task-api.spec.ts`
- Store: `src/app/features/tasks/data/state/task-store.spec.ts`
