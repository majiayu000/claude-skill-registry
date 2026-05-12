---
name: constitution
description: "Creates, updates, validates, and displays the architectural DNA of a project through two shared documents: docs/specs/architecture.md (technology stack, architectural rules, security constraints, AI guardrails) and docs/specs/ontology.md (domain glossary / Ubiquitous Language). Use BEFORE brainstorm as a project setup step, or at any point in the SDD lifecycle to validate specs/tasks against architecture principles. Triggers on 'create constitution', 'update constitution', 'constitution check', 'validate against constitution', 'project principles', 'architectural guardrails', 'setup project architecture', 'define ontology'."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion, TodoWrite
---

## Instructions

1. Identify the operation from `$ARGUMENTS` or user intent: `create`, `update`, `check`, or `show`.
2. For **create**: ask which files to create (architecture.md, ontology.md, or both), gather required information via `AskUserQuestion`, then write the files using the templates below.
3. For **update**: identify the target file and section, apply the change surgically, update the `Last Updated` date.
4. For **check**: read both constitution files, read the target file, validate against architectural rules and ontology terms, output a Constitution Check Report.
5. For **show**: read and display both files formatted for readability.
6. Always confirm with the user before writing or overwriting files.

## Examples

**Create constitution before first brainstorm:**
```
/developer-kit-specs:constitution create
```

**Validate a spec against architecture and ontology:**
```
/developer-kit-specs:constitution check --target=docs/specs/001/2024-01-15--user-auth.md
```

**Update the security constraints section:**
```
/developer-kit-specs:constitution update --file=architecture --section=security
```

**Show current constitution:**
```
/developer-kit-specs:constitution show
```

---

# Constitution Skill

## Overview

The **Constitution** is the architectural DNA of a project, expressed through two shared documents:

| File | Purpose |
|------|---------|
| `docs/specs/architecture.md` | Technology stack, infrastructure choices, architectural rules, security constraints, AI guardrails |
| `docs/specs/ontology.md` | Domain glossary (Ubiquitous Language) — terms, definitions, bounded contexts |

These files live at the `docs/specs/` level and are **shared across all specifications**.

**Key difference from the old constitution.md approach**: instead of a single monolithic file, the constitution is split into two focused documents that are also created and enriched by `brainstorm` (Phase 6.8.6) and `spec-to-tasks` (Phase 1.5). This skill lets you create or manage them **before brainstorm**, as a project setup step.

## When to Use

| Scenario | Operation |
|----------|-----------|
| New project — define stack and domain language before first brainstorm | `create` |
| Stack or security rules changed | `update` |
| Validate a spec, task, or file against architecture and ontology | `check` |
| Review current architecture and ontology | `show` |

**Trigger phrases:**
- "Create constitution", "Setup project architecture", "Define ontology"
- "Update constitution", "Update architecture", "Update ontology"
- "Constitution check", "Validate against constitution"
- "Show constitution", "Project principles", "Architectural guardrails"

## Available Operations

**1. create** — Create one or both files interactively
**2. update** — Update a specific section of one file
**3. check** — Validate a spec/task/file against both documents
**4. show** — Display the current state of both documents

---

## Operation: create

1. Ask the user which files to create (if not specified in `$ARGUMENTS`):
   - Options: "Both architecture.md and ontology.md" (recommended), "architecture.md only", "ontology.md only"

2. For each file to create, check if it already exists. If yes, ask: overwrite or skip.

3. **For `docs/specs/architecture.md`**, gather via `AskUserQuestion`:

   **Q1 — Software Stack**:
   - Options: "Java / Spring Boot", "TypeScript / NestJS", "TypeScript / React", "Python / Django or FastAPI", "PHP / Laravel or Symfony", or freeform

   **Q2 — Data Architecture**:
   - Options: "PostgreSQL", "MySQL", "MongoDB", "Multiple databases", or freeform

   **Q3 — Infrastructure**:
   - Options: "AWS", "Docker / Docker Compose", "Kubernetes", "Serverless", "Not yet decided", or freeform

   **Q4 — Architectural Rules** (optional, freeform):
   - Forbidden patterns, required patterns, security constraints, AI guardrails

   Then create `docs/specs/architecture.md` using the **Architecture Template** below.

4. **For `docs/specs/ontology.md`**, gather via `AskUserQuestion`:

   Ask the user to list the main domain terms and their definitions. Explain:
   > "The ontology captures the Ubiquitous Language of your project. It is normally enriched during brainstorming when terms emerge from the idea. You can seed it now with known terms, or create an empty scaffold to fill later."

   - Options: "Seed with known terms (I'll provide them)", "Create empty scaffold", "Skip for now"

   Then create `docs/specs/ontology.md` using the **Ontology Template** below.

5. Confirm with the user before writing each file.

---

## Operation: update

1. Identify the target file and section from `$ARGUMENTS`:
   - `--file=architecture` or `--file=ontology`
   - `--section=<section-name>` (e.g., `--section=security`, `--section=glossary`)
2. Read the target file.
3. Apply the update surgically — do not touch other sections.
4. Update the `Last Updated` date.
5. Write the updated file.

---

## Operation: check

1. Read both `docs/specs/architecture.md` and `docs/specs/ontology.md`. If either is missing, warn the user but continue with the available file(s).
2. Read the target file from `$ARGUMENTS` (`--target=<path>`).
3. Check against **architecture.md**:
   - Forbidden libraries/imports present?
   - Unapproved patterns used?
   - Security constraints violated (raw SQL, hardcoded secrets, etc.)?
   - AI guardrails violated?
4. Check against **ontology.md**:
   - Are domain terms used consistently (no synonyms for defined terms)?
   - Are new domain concepts introduced without being added to the glossary?
5. Output a **Constitution Check Report** (see format below).

---

## Operation: show

1. Read `docs/specs/architecture.md` and `docs/specs/ontology.md`.
2. Print both files formatted for readability, with a header indicating which file is which.

---

## Architecture Template

```markdown
# Project Architecture

**Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD

## Software Stack

| Component | Technology | Notes |
|-----------|-----------|-------|
| Language | [e.g., TypeScript] | [version if known] |
| Framework | [e.g., NestJS] | [version if known] |
| Key Libraries | [e.g., Drizzle ORM, Passport] | |

## Data Architecture

| Component | Technology | Notes |
|-----------|-----------|-------|
| Primary Database | [e.g., PostgreSQL] | |
| Caching | [e.g., Redis, none] | |
| ORM / Data Access | [e.g., Drizzle, Hibernate] | |
| Migrations | [e.g., Flyway, Drizzle Kit] | |

## Infrastructure

| Component | Technology | Notes |
|-----------|-----------|-------|
| Hosting | [e.g., AWS ECS] | |
| CI/CD | [e.g., GitHub Actions] | |
| Containerization | [e.g., Docker] | |
| Orchestration | [e.g., Kubernetes, none] | |

## Architectural Rules

- [Rule 1, e.g., "Use constructor injection. Never use @Autowired on fields."]
- [Rule 2, e.g., "Domain entities must not depend on framework annotations."]

## Security Constraints

- Forbidden patterns:
  - No raw SQL string concatenation (SQL injection — CWE-89)
  - No hardcoded secrets or credentials (CWE-798)
  - No deserialization of untrusted data (CWE-502)
- Required patterns:
  - [e.g., All inputs validated with Bean Validation]
  - [e.g., All secrets via environment variables or Secrets Manager]

## AI Guardrails

Rules that AI agents MUST follow when generating code for this project:

- [Guardrail 1, e.g., "Never generate @Transactional on repository methods."]
- [Guardrail 2, e.g., "Always generate tests alongside implementation code."]
- [Guardrail 3, e.g., "Do not introduce new dependencies without explicit approval."]

## Architecture Decisions

> Significant modifications to this architecture document must be tracked
> via **ADR (Architecture Decision Records)** using the `adr-drafting` skill.
>
> ADR location: `docs/architecture/adr/`
```

---

## Ontology Template

```markdown
# Project Ontology — Ubiquitous Language

**Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD

## Domain Glossary

| Term | Definition | Bounded Context |
|------|-----------|-----------------|
| [Term 1] | [Definition] | [Context where this term applies] |
| [Term 2] | [Definition] | [Context where this term applies] |

## Bounded Contexts

| Context | Description | Key Terms |
|---------|-------------|-----------|
| [Context 1] | [Description] | [Key terms] |

## Conceptual Mapping

[Relationships between key domain entities — to be refined during brainstorming and task generation]
```

---

## Constitution Check Report Format

```
## Constitution Check Report
Target: <file or spec path>
Date: YYYY-MM-DD

### Architecture Check

| Rule | Status | Detail |
|------|--------|--------|
| Constructor injection required | ✅ OK | No field injection found |
| No hardcoded secrets | ❌ CRITICAL | Line 42: hardcoded password string |
| JWT authentication | ⚠️ WARNING | Missing @PreAuthorize on endpoint |

### Ontology Check

| Term | Status | Detail |
|------|--------|--------|
| "Reservation" used consistently | ✅ OK | No synonym "Booking" found |
| New term "Voucher" introduced | ⚠️ WARNING | Not defined in ontology.md |

### Summary
- CRITICAL violations: 1 (must fix before proceeding)
- WARNING violations: 2 (should fix)
- Compliant rules: 2
```

---

## Relationship with brainstorm and spec-to-tasks

This skill is the **pre-brainstorm setup** entry point. The same files are also created/enriched by:

| Command | When | What it does |
|---------|------|-------------|
| `constitution create` | Before brainstorm (this skill) | Creates architecture.md and/or ontology.md from scratch |
| `brainstorm` Phase 6.8.6 | During brainstorming | Creates/enriches ontology.md with terms extracted from the idea |
| `spec-to-tasks` Phase 1.5 | After brainstorm | Creates architecture.md if missing; enriches ontology.md with new terms from the spec |

**If you run `constitution create` before brainstorm**, the brainstorm and spec-to-tasks commands will detect the existing files and load them instead of creating new ones — no duplication.

**Note on ontology.md**: The ontology is normally most naturally created during brainstorming, because domain terms emerge from the idea description. Using `constitution create` to seed it beforehand is useful when the team already has a well-defined domain language.

---

## Integration with SDD Workflow

```
[Optional] constitution create        ← this skill (pre-brainstorm setup)
        ↓
brainstorm                            ← enriches ontology.md (Phase 6.8.6)
        ↓
spec-to-tasks                         ← loads/creates architecture.md, enriches ontology.md (Phase 1.5)
        ↓
task-implementation                   ← AI guardrails from architecture.md prevent unapproved patterns
        ↓
task-review / ralph-loop              ← constitution check validates implementation
```

---

## Constraints

- **Does NOT modify source code** — only creates/updates `docs/specs/architecture.md` and `docs/specs/ontology.md`
- **Constitution Check is advisory for WARNINGs** — CRITICAL violations must be resolved
- **One architecture.md and one ontology.md per project** — shared across all specs
- **Version the architecture** — update `Last Updated` date on every change; use ADRs for significant decisions
