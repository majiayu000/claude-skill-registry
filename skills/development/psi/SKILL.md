---
name: psi
description: Plan-spec-implement workflow for structured development. Only use when explicitly directed by user or when mentioned in project AGENTS.md file. Generates ephemeral plans in ~/.dot-agent/, applies specs to project docs, then implements test-first.
license: MIT
---

# PSI - Plan Spec Implement

Structured workflow for planning, specifying, and implementing changes with documentation-first approach.

## When to Use

**Only use when:**
- Explicitly directed by the user
- Mentioned in project `AGENTS.md` file

**Do not use automatically** - this is an opt-in workflow, not a default.

## Core Workflow

**Plan → Spec → Implement**

Phases are **independent** - you can start with any phase, but all must ensure documentation stays up-to-date.

## Key Principles

1. **Ephemeral planning** - Plans stored in `~/.dot-agent/` (not committed)
2. **Documentation-first** - Specs applied to project docs/READMEs/AGENTS.md
3. **Test-first implementation** - Tests for docs/user journeys before code
4. **Design/review embedded** - Design and review integrated into Plan/Spec phases
5. **Phase independence** - Each phase can work standalone, all update docs

## Phase Overview

### Plan Phase
- Generates detailed plans in `~/.dot-agent/repo/YYYY-MM-work-name.plan.md`
- Research stored in `~/.dot-agent/working-dir/repo/YYYY-MM-work-name.research.md`
- Embeds design considerations
- Includes review before proceeding

### Spec Phase
- Generates specs for: API schemas, interfaces, DTOs, database models, config, env vars, architecture, user journeys, package structure, tech choices
- Embeds design considerations
- Reviews specs before applying
- Applies to: `docs/`, README.md files, AGENTS.md files

### Implement Phase
- Test-first: tests for docs/user journeys before code
- CI verification: verify types, tests, lint pass before committing
- Atomic commits: group related changes with tests
- Updates docs, README.md, AGENTS.md as code evolves
- Can work independently if specs exist in docs

## Research Management

Detects phrases like:
- "looking at your research" → Loads research file
- "refine your research" → Updates research file, narrows focus

## Documentation Structure

- **README.md**: Aim for < 1000 lines (not hard rule), can be longer if needed
- **AGENTS.md**: < 200 lines, inline at root/packages/modules/code level
- **docs/**: Architecture, roadmap, tech-choices, setup/, user-journeys/, design/

## References

For detailed protocols, see:
- `references/plan-phase.md` - Plan generation with embedded design/review
- `references/spec-phase.md` - Spec generation and application
- `references/implement-phase.md` - Test-first implementation
- `references/review-protocol.md` - Reviewing plans/specs/design
- `references/research-management.md` - Research file handling
- `references/docs-structure.md` - Documentation organization rules
- `references/file-paths.md` - Storage paths and conventions
