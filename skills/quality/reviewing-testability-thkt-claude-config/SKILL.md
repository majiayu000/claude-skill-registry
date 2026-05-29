---
name: reviewing-testability
description: >
  Testable code design patterns for TypeScript/React applications.
  Use when reviewing code for testability, implementing dependency injection,
  or when user mentions テスト容易性, モック, mock-friendly, DI.
allowed-tools: [Read, Grep, Glob, Task]
agent: testability-reviewer
context: fork
user-invocable: false
---

# Testability Review

## Detection

| ID  | Pattern                      | Fix                             |
| --- | ---------------------------- | ------------------------------- |
| TE1 | Direct `import { db }` usage | Inject dependency as parameter  |
| TE1 | `new Service()` inside class | Constructor injection           |
| TE2 | `fetch()` inside component   | Extract to hook/service, inject |
| TE2 | Mixed side effects + logic   | Separate pure/impure            |
| TE3 | Deep mock chains             | Simplify dependencies           |
| TE4 | Global `config` access       | Pass config as prop/parameter   |
| TE4 | `Date.now()` in logic        | Inject clock/time provider      |
| TE5 | Tight coupling               | Depend on abstractions (DIP)    |

## Criteria

Test setup < 10 lines. No deep mock chains. Dependencies explicit.

## References

| Topic   | File                                 |
| ------- | ------------------------------------ |
| DI      | `references/dependency-injection.md` |
| Pure    | `references/pure-functions.md`       |
| Mocking | `references/mock-friendly.md`        |
