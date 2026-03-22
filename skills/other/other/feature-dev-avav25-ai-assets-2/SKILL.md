---
name: feature-dev
description: Develop a feature from documentation (PRD, ARD, design doc, implementation plan) with automatic role detection based on project tech stack
context: fork
argument-hint: [PRD path or feature description]
---

# Feature Development

End-to-end feature implementation from documentation to working code. Automatically detects and applies the appropriate engineering role based on the project's tech stack.

## 1. Receive and Parse Documentation

Gather all input documentation provided by the user:

- **Accepted formats**: PRD, ARD (Architecture Decision Record), design doc, implementation plan, ticket/issue, or any structured feature specification
- Read every provided document thoroughly
- Extract and organize:
  - **Goal**: what the feature does (1–2 sentences)
  - **Requirements**: functional and non-functional
  - **Acceptance criteria**: how to verify the feature works
  - **Implementation plan**: ordered steps, architecture decisions, data models, API contracts
  - **Constraints**: performance, security, compatibility, dependencies
  - **Out of scope**: what this feature explicitly does NOT cover

If the documentation is ambiguous or incomplete, ask the user before proceeding.

## 2. Detect Tech Stack and Apply Role

Determine the project's tech stack and apply the appropriate engineering role:

1. **Read project's `CLAUDE.md`** — look for tech stack declaration (language, framework, runtime)
2. **Scan project files** — check `package.json`, `pom.xml`, `*.csproj`, `requirements.txt`, `go.mod`, `Cargo.toml`, or equivalent to confirm
3. **Role matching** — Claude Code's (agent) trigger auto-matches roles whose `description` matches the detected stack:
   - If multiple specializations match (e.g., fullstack) — apply all relevant roles
   - If no specialization role exists — fall back to base engineering principles
4. **Announce** the detected stack and applied role(s) to the user for confirmation

**Examples:**
- Next.js + TypeScript → `Agent(frontend-engineer)` applies
- Spring Boot → `Agent(java-engineer)` applies
- Python + FastAPI → `Agent(python-engineer)` applies
- Terraform / Docker / K8s → `Agent(devops-engineer)` applies
- Cloud architecture / landing zones / networking / multi-cloud → `Agent(cloud-architect)` applies
- GitHub Actions / CI/CD pipelines / deployment strategy → `Agent(devops-architect)` applies
- React Native / Flutter / iOS / Android → `Agent(mobile-engineer)` applies
- ETL / Spark / dbt / Airflow / data pipelines → `Agent(data-engineer)` applies
- SQL / database schema / migrations / query optimization → `Agent(db-engineer)` applies
- ARCHITECTURE.md / system design / component boundaries → `Agent(system-architect)` applies
- LLM / RAG / agents / memory / multi-agent / AI pipelines → `Agent(ml-engineer)` applies + consult `context-engineering` skill for context pipeline design

## 3. Analyze Codebase Context

Before writing any code, understand the existing codebase:

1. **Project structure** — directory layout, module boundaries, entry points
2. **Existing patterns** — naming conventions, error handling, logging, testing approach
3. **Dependencies** — installed packages, available libraries, version constraints
4. **Related code** — files and modules the new feature will interact with, extend, or modify
5. **Test infrastructure** — test framework, test file locations, existing test patterns

Map how the new feature fits into the existing architecture. Identify:
- Files to **create** (new modules, components, tests)
- Files to **modify** (integration points, routes, configs)
- Files to **not touch** (unrelated code — minimize blast radius)

## 4. Create Implementation Plan

Break the feature into ordered, atomic implementation steps:

1. Number each step sequentially
2. Each step = one logical unit of work (one file or one cohesive change across tightly coupled files)
3. Order by dependency — implement foundations before consumers
4. Interleave test steps with implementation (do not defer all tests to the end)

Present the plan to the user:

```
Feature: [name]
Stack: [detected] | Role: [applied]
Steps:
  1. [description] → [file(s)]
  2. [description] → [file(s)]
  ...
  N. [description] → [file(s)]
```

Wait for user approval before proceeding. The user may reorder, add, remove, or modify steps.

## 5. Implement

Execute the approved plan step by step.

**For each step:**
1. State what you are about to do (step number, file, change summary)
2. Write code following:
   - Project's existing patterns and conventions
   - Active role's guidelines (stack-specific best practices)
   - Documentation's architecture decisions and constraints
3. Verify the code compiles/parses without errors after each step
4. If a step introduces a new dependency — install it immediately

**Rules:**
- Minimal, focused changes — do not refactor unrelated code
- Follow existing code style (indentation, naming, imports)
- Add imports at the top of files
- Production-quality code — no TODOs, no placeholders, no stubs (unless the plan explicitly calls for them)
- If you encounter an unexpected issue — stop and consult the user

## 6. Write Tests

For each implemented component, write tests following the project's test infrastructure:

1. **Unit tests** — business logic, utilities, data transformations
2. **Integration tests** — API endpoints, database queries, service interactions
3. **Component tests** (frontend) — UI components with user interactions
4. Cover both **happy path** and **edge cases** (error handling, boundary values, empty states)
5. Run the tests and verify they pass

If the documentation specifies acceptance criteria, write tests that directly verify each criterion.

## 7. Verify

Run the full verification sequence:

1. **Build/compile** — project builds without errors or warnings
2. **Lint** — run the project's linter if configured
3. **Test** — run the full test suite (new + existing) to catch regressions
4. **Acceptance check** — review implementation against documentation's acceptance criteria

**Checklist:**
- [ ] All acceptance criteria from the documentation are met
- [ ] No new warnings or errors in build output
- [ ] All tests pass (new and existing)
- [ ] No unrelated files were modified
- [ ] Code follows project conventions and active role's guidelines

If any check fails — fix the issue and re-verify.

## 8. Summary

Present the completed work:

- **Feature**: what was implemented
- **Stack / Role**: detected tech stack and applied role(s)
- **Files changed**: list of created and modified files with brief descriptions
- **Tests**: number of tests added, pass status
- **Acceptance criteria**: status of each criterion (met / partially met / not met)
- **Notes**: deviations from original plan, trade-offs, follow-up items

## Integration

- **Precedes**: `/run-tests`, `/pre-commit`, `/create-pr`
- **Planning**: `/feature-plan` (produces the implementation plan this workflow executes)
- **Skills**: `testing-procedures` skill (test strategy), `code-review` skill (review standards), `context-engineering` skill (context pipelines, RAG, agent harness, production checklists — for AI/LLM features)
