---
name: project-init
description: Initialize Codex project context for an existing repository by generating root and scoped AGENTS.md files plus supporting ARCHITECTURE.md and TESTING.md documentation.
context: fork
---

# Project Init

Deep-scan an existing repository and generate Codex-ready context files.

## Outputs

- Root `AGENTS.md`
- Scoped `AGENTS.md` files for significant directories
- `ARCHITECTURE.md`
- `TESTING.md`

## 1. Reconnaissance

Scan:

- Root structure
- Build and dependency files
- Test infrastructure
- Existing docs
- Significant service or package boundaries

Read existing `AGENTS.md`, `ARCHITECTURE.md`, and `TESTING.md` before creating anything new.

## 2. Detect Project Boundaries

Identify:

- Monorepo services and packages
- Shared libraries
- Infrastructure directories
- Content or documentation areas with special conventions

Create a compact project map before drafting files.

## 3. Generate Root `AGENTS.md`

Use `.codex/templates/root-agents.template.md` as the starting point.

The root file should include:

- Product purpose
- Service map
- Mandatory engineering rules
- Repository structure
- Codex operating guidance

## 4. Generate `ARCHITECTURE.md`

Document the current system:

- Services and responsibilities
- Runtime stack
- Data flow
- Deployment shape
- External integrations

Prefer concise diagrams and concrete facts over aspirational prose.

## 5. Generate `TESTING.md`

Document:

- Test types
- Commands
- Required infrastructure
- Service-specific test entry points
- Any known preconditions for local verification

## 6. Generate Scoped `AGENTS.md`

Create scoped files only where a directory has its own conventions or responsibilities.

Good candidates:

- Service roots
- `src` subtrees with strong conventions
- Infrastructure directories
- Content or docs directories with distinct workflows

Use `.codex/templates/service-agents.template.md`.

## 7. Review Before Writing

Present:

- Files to create or update
- Project map
- Detected stacks
- Significant directories selected for scoped guidance

If the user has asked for autonomous execution, proceed unless there is a genuine risk of mis-scoping critical files.

## 8. Verify

After writing:

- Confirm all created files exist
- Confirm scoped `AGENTS.md` files are not redundant with the root file
- Confirm `AGENTS.md` references line up with `.agents` and `.codex`
- Confirm no file contains Claude-specific runtime assumptions

## Integration

- Templates: `.codex/templates/root-agents.template.md`, `.codex/templates/service-agents.template.md`
- Companion docs: `ARCHITECTURE.md`, `TESTING.md`
- Enables: `feature-plan`, `feature-dev`, `bugfix`, `run-tests`
