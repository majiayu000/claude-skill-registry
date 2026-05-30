---
name: constitution
description: "Creates, updates, validates, and displays the architectural DNA of a project through two shared documents: docs/specs/architecture.md (technology stack, architectural rules, security constraints, AI guardrails) and docs/specs/ontology.md (domain glossary / Ubiquitous Language). Use BEFORE brainstorm as a project setup step, or at any point in the SDD lifecycle to validate specs/tasks against architecture principles. Triggers on 'create constitution', 'update constitution', 'constitution check', 'validate against constitution', 'project principles', 'architectural guardrails', 'setup project architecture', 'define ontology'."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion, TodoWrite
---

## Overview

The Constitution skill manages the architectural DNA of a project through two shared documents:

| File | Purpose |
|------|---------|
| `docs/specs/architecture.md` | Technology stack, infrastructure, architectural rules, security constraints, AI guardrails |
| `docs/specs/ontology.md` | Domain glossary (Ubiquitous Language) — terms, definitions, bounded contexts |

These files live at `docs/specs/` and are shared across all specifications. Unlike a monolithic `constitution.md`, these are created/enriched by `brainstorm` (Phase 6.8.6) and `spec-to-tasks` (Phase 1.5).

## Instructions

1. Identify the operation from `$ARGUMENTS` or user intent: `create`, `update`, `check`, or `show`.
2. For **create**: ask which files to create (architecture.md, ontology.md, or both), gather required information via `AskUserQuestion`, then write the files using the templates below.
3. For **update**: identify the target file and section, apply the change surgically, update the `Last Updated` date.
4. For **check**: read both constitution files, read the target file, validate against architectural rules and ontology terms, output a Constitution Check Report.
5. For **show**: read and display both files formatted for readability.
6. Always confirm with the user before writing or overwriting files.

## Examples

```bash
# Create constitution before first brainstorm
/developer-kit-specs:constitution create

# Validate a spec against architecture and ontology
/developer-kit-specs:constitution check --target=docs/specs/001/2024-01-15--user-auth.md

# Update the security constraints section
/developer-kit-specs:constitution update --file=architecture --section=security

# Show current constitution
/developer-kit-specs:constitution show
```


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

## Operations

### create
1. Ask which files to create: "Both" (recommended), "architecture.md only", "ontology.md only"
2. Check if files exist → ask to overwrite or skip
3. For **architecture.md**: gather via `AskUserQuestion` (domains, infrastructure, stack, data, style, rules)
4. For **ontology.md**: ask for terms or create empty scaffold
5. Confirm before writing each file

Template lookup order:
- Primary: `${CLAUDE_PLUGIN_ROOT}/templates/architecture.md`
- Fallback: `skills/constitution/references/architecture.md`

### update
1. Parse `--file=architecture|ontology` and `--section=<name>`
2. Read target file, apply change surgically
3. Update `Last Updated` date
4. Write file

### check
1. Read both constitution files
2. Read target file (`--target=<path>`)
3. Validate against architecture rules, security constraints, and ontology
4. Output **Constitution Check Report**

### show
1. Read both `docs/specs/architecture.md` and `docs/specs/ontology.md`
2. Display formatted for readability

## Context Rot Prevention

The Constitution survives context rot through file-based storage:

- **Read at session start**: Both `docs/specs/architecture.md` and `docs/specs/ontology.md`
- **Never assume in context**: MUST be read from file before implementation
- **Validate work**: Compare against constitution, not memory

For detailed scenarios and recovery protocols, see `references/context-rot-prevention.md`.

## Constraints and Warnings

- **Does NOT modify source code** — only creates/updates constitution files
- **CRITICAL violations MUST be resolved** — WARNINGs are advisory
- **One architecture.md and one ontology.md per project** — shared across all specs
- **Update `Last Updated` date** on every change
- **Use ADRs** for significant architectural decisions
- **Context rot risk**: Files > 30 days old may have drifted

## Best Practices

- **Create before brainstorm**: Constitution established early ensures consistency
- **Library Verification**: Before using ANY external library, verify it's in the architecture's Library Verification section
- **Spec Death Principle**: Archive completed specs to `archived/` — never let specs become stale
- **Ontology enrichment**: Updated by `brainstorm` (Phase 6.8.6) and `spec-to-tasks` (Phase 1.5)
- **Report format**: Security section first, then CWE compliance, architecture, library verification, ontology

## Constitution Check Report Format

```
## Constitution Check Report
Target: <file path>
Date: YYYY-MM-DD

### Security Check (CWE/OWASP Compliance)
| Rule | Level | Status | Location | CWE/OWASP |
|------|-------|--------|----------|-----------|
| No SQL injection | CRITICAL | ✅ OK | - | CWE-89 |

### CWE Compliance Report
| CWE | OWASP | Status | Location |
|-----|-------|--------|----------|
| CWE-89 | A03 | ✅ OK | - |

### Architecture Check
| Rule | Status | Detail |
|------|--------|--------|
| Constructor injection | ✅ OK | - |

### Library Verification Check
| Library | Status | Detail |
|---------|--------|--------|
| bcrypt | ✅ OK | Using hash(password, 12) |

### Ontology Check
| Term | Status | Detail |
|------|--------|--------|
| "User" used consistently | ✅ OK | - |

### Summary
- CRITICAL violations: 0
- WARNING violations: 0
- Compliant rules: N
```

For detailed security patterns (CWE/OWASP mappings), see `references/security-patterns.md`.

## Integration with SDD Workflow

```
[Session Start] → Read Constitution files
        ↓
[Optional] constitution create        ← this skill (pre-brainstorm setup)
        ↓
brainstorm                            ← Constitution loaded before brainstorming
        ↓
spec-to-tasks                         ← Constitution validates spec
        ↓
task-implementation                   ← Constitution guardrails active
        ↓
task-review                           ← Constitution check validates
        ↓
[Session End] → Constitution files updated if needed
```

Required loading before:
- `specs.brainstorm` — Validate requirements align with architecture
- `specs.spec-to-tasks` — Check stack compatibility
- `specs.task-implementation` — Apply AI guardrails
- `specs.task-review` — Constitution check

## Reference Files

| File | Purpose |
|------|---------|
| `references/architecture.md` | Full architecture template |
| `references/ontology.md` | Full ontology template |
| `references/security-patterns.md` | CWE/OWASP patterns, verification format |
| `references/context-rot-prevention.md` | Detailed scenarios and recovery protocols |
| `references/constitution-check-report.md` | Complete report examples |

For complete templates and detailed reference material, consult the `references/` directory.