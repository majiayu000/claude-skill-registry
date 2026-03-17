---
name: quanzhankaifa
description: Use when the user wants a doc-first, end-to-end backend/full-stack project workflow with phase documents, confirmations, and traceability (inputs may be DOC/PDF/MD).
---

# Quanzhankaifa (Full-Stack Project, Doc-First)

## Overview
Use a doc-first delivery flow: from requirements to release, write every step into Markdown, pause for user confirmation after each doc, and prove alignment with the docs before any implementation work.

## Skill Check (Required, Superpowers-Inspired)
- Before any action or clarification, check if other skills apply
- If any apply, invoke them first; process skills take priority
- Common triggers:
  - Brainstorming: new features, unclear requirements, or design choices
  - Systematic debugging: bugs, test failures, unexpected behavior
  - Test-driven development: any code changes or new behavior
  - Verification before completion: claiming work is done or fixed

## Pre-Phase: Intent Clarification (Brainstorming Mode)
- Ask one question at a time; prefer multiple-choice when possible
- Clarify purpose, constraints, success criteria, non-goals, stakeholders
- When options exist, propose 2-3 approaches with trade-offs, recommend one
- Record Q/A, options, and decisions in `00-discovery.md`
- Update `00-index.md` and stop for confirmation after `00-discovery.md`

## Core Workflow (Doc-First)
Produce or update a file at each phase:
0. Discovery and options -> `00-discovery.md`
1. Requirements -> `01-requirements.md`
2. Scope and success -> `02-scope.md`
3. Architecture -> `03-architecture.md`
4. Modules and domain -> `04-module-design.md`
5. Database -> `05-db-design.md`
6. API -> `06-api-spec.md`
7. Implementation plan -> `07-implementation-plan.md`
8. Test plan -> `08-test-plan.md`
9. Release and rollback -> `09-release-plan.md`
10. Decisions and risks -> `10-decision-log.md`, `11-risk-log.md`
11. Traceability -> `12-traceability.md`

## Working Directory + Logging Rules
- Default docs folder: `docs/project/`
- Single entry index: `docs/project/00-index.md`
- Update the index every step (phase, done, open questions, next step)
- End each doc with: Summary + Open questions + Next step
- All doc content must be written in Chinese; keep filenames as specified
- After each doc is written, stop and ask the user to confirm or correct it
- If any Open questions remain, do not proceed until the user answers or defers them explicitly
- Read order each session: `00-index.md` -> current phase doc -> related docs (minimal load)

## Confirmation Gate (Required)
- After producing a phase doc, ask for confirmation in chat and wait
- Show a short "Doc alignment" list that references the doc filename and key bullets you followed
- Copy Open questions into the message and ask the user to answer or confirm deferral
- If the doc is not in Chinese, fix it before asking for confirmation

## Traceability (Doc-to-Work Evidence)
- Maintain `12-traceability.md` with a simple table:
  - Columns: Requirement | Design/Module | DB/API | Implementation/Tests | Status
- Update this table after each phase and before any coding
- Before coding, cite the relevant doc sections and the traceability rows you are implementing

## Language Rule
- Use Chinese templates in `assets/` and keep all headings, bullets, and narrative in Chinese across `00`-`12` docs
- Comments should be written in Chinese unless the existing codebase clearly uses another language

## Step-by-Step Execution
### 0) Discovery and options
- Use the Pre-Phase clarification loop and write `00-discovery.md`
- Stop and confirm

### 1) Requirements intake
- If input is DOCX/PDF: extract key points first, then write to `01-requirements.md`
- Output: features, non-functional requirements, constraints, acceptance criteria
- Stop and confirm

### 2) Architecture and modules
- Output: system boundary, core services/modules, data flow, dependencies
- Write to `03-architecture.md` and `04-module-design.md`
- Stop and confirm

### 3) Database and API design
- Output: ER relations, tables, indexes, enums, constraints
- Output: API list, request/response, auth, error codes
- Write to `05-db-design.md` and `06-api-spec.md`
- Stop and confirm

### 4) Implementation plan
- Output: milestones, task breakdown, dependencies, risks
- Write to `07-implementation-plan.md`
- Stop and confirm

### 5) Testing and release
- Testing: unit, integration, acceptance, performance
- Release: rollout, rollback, monitoring
- Write to `08-test-plan.md` and `09-release-plan.md`
- Stop and confirm

## Context Minimization
- Start by reading `00-index.md`
- Load only docs related to the current phase
- Close the loop by updating docs and reporting the changes

## Quick Reference
| Phase | Output | Key questions |
|---|---|---|
| Discovery | 00-discovery.md | What are goals, constraints, options? |
| Requirements | 01-requirements.md | What is the goal and boundary? |
| Scope | 02-scope.md | What is MVP and what is out? |
| Architecture | 03-architecture.md | How does data and control flow? |
| Modules | 04-module-design.md | Clear responsibilities and deps? |
| Database | 05-db-design.md | Tables, indexes, constraints? |
| API | 06-api-spec.md | Request/response/auth/errors? |
| Plan | 07-implementation-plan.md | Milestones, dependencies, risks? |
| Testing | 08-test-plan.md | Coverage and acceptance? |
| Release | 09-release-plan.md | Rollback and monitoring? |
| Traceability | 12-traceability.md | Does code map to docs? |

## Common Mistakes
- Keep decisions only in chat, not in docs
- Mix requirements and design in one file
- Write code first and backfill docs later
- Skip confirmation after a doc is written
- Code without showing doc alignment or traceability
- Write docs in English or mixed language
- Leave complex logic without comments
- Skip the discovery phase or ask multiple questions at once

## Resources
- Doc templates: `references/api_reference.md`
- MD template: `assets/project-template.md`
- DOC template: `assets/project-template.doc`
- Alibaba Java spec (summary): `references/alibaba-java-spec.md`
- Code comment template: `references/code-comment-template.md`

## Handoff Rules
- For implementation, create `07-implementation-plan.md` before coding
- For code changes, follow test-driven development
- For unexpected behavior, run systematic debugging first
- When writing code, add thorough comments for all non-trivial logic, control flow, and edge cases
- Use `references/code-comment-template.md` for file/module/class/function/logic-block comments
- Before and after coding, cite the docs you followed and update `12-traceability.md`
