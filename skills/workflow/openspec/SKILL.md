---

name: openspec
description: "OpenSpec artifact-driven workflow. Covers OPSX commands, schemas, project config. Keywords: OPSX, artifact graph, /opsx:."
version: "1.1.1"
release_date: "2026-01-30"

# OpenSpec (OPSX) Skill

Use this skill to guide or reason about the OpenSpec artifact-driven workflow system (OPSX), including artifact graphs, schema/template resolution, change lifecycle, and experimental commands/skills.

## When to Use

- You need to explain or apply the artifact-driven workflow (OPSX).
- You are planning or reviewing changes based on artifact dependencies.
- You need to interpret schema/template resolution rules (XDG + built-ins).
- You are asked to design or validate changes to the OpenSpec workflow or schema tooling.
- You are asked to create or operate OpenSpec experimental skills/commands.

## Quick Navigation

- Artifact graph core concepts: references/artifact-core.md
- OPSX workflow behavior and usage: references/opsx-workflow.md
- Schema customization workflow and gaps: references/schema-customization.md
- End-to-end schema workflow gaps and proposed solution: references/schema-workflow-gaps.md
- Experimental release plan and rollout checklist: references/experimental-release-plan.md

## OPSX Commands

| Command              | Purpose                                                  |
| -------------------- | -------------------------------------------------------- |
| `/opsx:explore`      | Think through ideas, investigate problems (no structure) |
| `/opsx:new`          | Start a new change                                       |
| `/opsx:continue`     | Create next artifact based on dependencies               |
| `/opsx:ff`           | Fast-forward — create all planning artifacts at once     |
| `/opsx:apply`        | Implement tasks, updating artifacts as needed            |
| `/opsx:verify`       | Validate implementation matches spec                     |
| `/opsx:sync`         | Sync delta specs to main specs                           |
| `/opsx:archive`      | Archive single completed change                          |
| `/opsx:bulk-archive` | Archive multiple completed changes at once               |

## Schema Management

```bash
openspec schemas                    # List available schemas
openspec schema which --all         # Show resolution sources
openspec schema init my-workflow    # Create new schema interactively
openspec schema fork spec-driven my-workflow  # Fork existing schema
openspec schema validate my-workflow  # Validate schema structure
```

## Project Configuration

Create `openspec/config.yaml` for per-project settings:

```yaml
schema: spec-driven

context: |
  Tech stack: TypeScript, React, Node.js
  Testing: Vitest, Playwright

rules:
  proposal:
    - Include rollback plan
  specs:
    - Use Given/When/Then format
```

**Schema precedence:** CLI flag → Change metadata → Project config → Default (`spec-driven`)

## Core Concepts

- **Artifact graph, not a workflow engine**: Dependencies enable actions; they do not force linear phases.
- **Filesystem-as-database**: Completion is derived from file existence, not stored state.
- **Deterministic CLI**: Commands require explicit change context (agent infers, CLI remains strict).
- **XDG schema resolution**: User overrides take precedence over built-ins.
- **Templates are schema-scoped**: Templates live next to schema and resolve with a strict 2-level fallback.

## Decision Rules

- Prefer **update** when intent stays the same and you are refining scope or approach.
- Prefer **new change** when intent or scope fundamentally shifts, or the original can be completed independently.
- Always preserve a clear history of why artifacts changed (proposal/specs/design/tasks).

## Recipes

### 1) Show what is ready to create next

1. Determine the active change id.
2. Query status and ready artifacts with the change explicitly set.
3. Present ready artifacts and their dependencies.

Expected behavior: show ready artifacts, not required steps.

### 2) Generate instructions for a specific artifact

1. Resolve schema and template with XDG fallback.
2. Build context: change metadata, dependency status, and target paths.
3. Return enriched instructions in plain Markdown.

### 3) Start a new change

1. Validate change name (kebab-case).
2. Create change directory and README.
3. Show initial status and first ready artifact.

### 4) Schema customization guidance

1. Explain XDG override paths.
2. Describe copying built-in schema + templates.
3. Provide verification steps or recommended CLI commands for listing and resolving.

### 5) Explain schema binding for a change

1. Prefer change metadata if available.
2. Fallback to project default schema if configured.
3. Otherwise default to spec-driven.

## Prohibitions

- Do not treat the system as a linear workflow engine.
- Do not assume a change is active without explicit selection.
- Do not silently fall back between schemas or templates without reporting.
- Do not copy long vendor docs verbatim; summarize and provide actionable guidance.

## Output Expectations

- Give clear artifact readiness and dependency explanations.
- Use explicit change identifiers in examples.
- Provide concise, actionable steps and indicate whether they are informational or required.
