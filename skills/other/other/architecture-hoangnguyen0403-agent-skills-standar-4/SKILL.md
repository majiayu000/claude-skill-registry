---
name: NestJS Architecture
description: Standards for scalable, modular NestJS backend architecture.
metadata:
  labels: [nestjs, backend, architecture, modularity]
  triggers:
    files: ['**/*.module.ts', 'main.ts']
    keywords: [NestFactory, Module, Controller, Injectable]
---

# NestJS Architecture Expert

## **Priority: P0 (CRITICAL)**

**You are a Backend Architect.** Design decoupled, testable modules.

## Implementation Guidelines

- **Modules**: Feature Modules (Auth) vs Core (Config/DB) vs Shared (Utils).
- **Controllers**: Thin controllers, fat services. Verify DTOs here.
- **Services**: Business logic only. Use Repository pattern for DB.
- **Config**: Use `@nestjs/config`, never `process.env` directly.

## Architecture Checklist (Mandatory)

- [ ] **Circular Deps**: Are there any circular dependencies? (Use `madge`).
- [ ] **Env Validation**: Is Joi/Zod schema used for env vars?
- [ ] **Exception Filters**: Are global filters catching unhandled errors?
- [ ] **DTO Validation**: Are `class-validator` decorators on all inputs?

## Anti-Patterns

- **No Global Scope**: Avoid global pipes/guards unless truly universal.
- **No Direct Entity**: Don't return ORM entities; return DTOs.
- **No Business in Controller**: Move logic to Service.
- **No Manual Instantiation**: Use DI, never `new Service()`.

## References

- [Advanced Patterns](references/advanced-patterns.md)
- [Dynamic Modules](references/dynamic-module.md)
