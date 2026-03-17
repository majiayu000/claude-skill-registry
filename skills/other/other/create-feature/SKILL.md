---
name: create-feature
version: 1.0.0
description: '[Implementation] Scaffold a new feature with backend and frontend components'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** before executing:

- `.claude/skills/shared/understand-code-first-protocol.md`
- `.claude/skills/shared/evidence-based-reasoning-protocol.md`

## Quick Summary

**Goal:** Scaffold a new full-stack feature with backend (entities, CQRS, controllers) and frontend (Angular components, services).

**Workflow:**

1. **Analyze** — Break down requirements, identify scope (backend/frontend/full-stack)
2. **Identify** — Determine target microservice and Angular app/module
3. **Plan** — Map out entities, commands/queries, endpoints, components, DTOs
4. **Approve** — Present plan, wait for explicit user approval before creating files
5. **Create** — Scaffold files in order: entities → application → DTOs → controllers → frontend

**Key Rules:**

- DO NOT proceed without explicit user approval
- Follow platform patterns from CLAUDE.md and `.github/prompts/` templates
- Build order: Domain → Application → API → Frontend
- Verify with `dotnet build` and `nx build` after creation

Create a new feature: $ARGUMENTS

## Steps:

1. **Analyze Requirements**
    - Break down the feature requirements
    - Identify the scope (backend only, frontend only, or full-stack)

2. **Identify Service Location**
    - Determine the appropriate microservice for backend
    - Identify the Angular app/module for frontend

3. **Plan Implementation**
    - Domain entities needed
    - CQRS Commands/Queries
    - API endpoints (controllers)
    - Angular components and services
    - DTOs and validation

4. **Use Platform Patterns**
    - Reference patterns from CLAUDE.md
    - Use `.github/prompts/` templates for scaffolding:
        - `create-cqrs-command.prompt.md`
        - `create-cqrs-query.prompt.md`
        - `create-entity-event.prompt.md`
        - `create-angular-component.prompt.md`
        - `create-api-service.prompt.md`

5. **Wait for Approval**
    - Present the implementation plan
    - **DO NOT proceed without explicit approval**

6. **Create Files (After Approval)**
   Execute in this order:
    1. Domain entities (`.Domain/Entities/`)
    2. Application layer (`.Application/UseCaseCommands/`, `.Application/UseCaseQueries/`)
    3. Entity DTOs (`.Application/EntityDtos/`)
    4. API controllers (`.Api/Controllers/`)
    5. Frontend components and services

7. **Verify**
    - Build backend: `dotnet build`
    - Build frontend: `nx build <app-name>`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
