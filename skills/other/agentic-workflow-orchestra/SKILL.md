---
name: agentic-workflow-orchestra
description: |
  Orchestrates AI agent work across planning, implementation, integration, QA,
  and release. Defines phases, gates, handoff logs, startup checklists, and
  parallel-safety rules for software projects.
license: MIT
metadata:
  author: PeterOla
  version: "2.0.0"
---

# Agentic Workflow Orchestra

Agentic Workflow Orchestra is a reusable framework for coordinating AI agent work on software projects.

This skill defines how agents operate together. Each consuming project defines what gets built through its own `orchestra/` directory.

## When To Use This Skill

Use this skill when a task or project benefits from multiple specialized agent roles, explicit sequencing, and repeatable verification.

Good fits:

- full-stack applications with multiple domains
- projects with shared contracts between teams or components
- work that benefits from phased execution and formal handoffs
- repositories where mistakes are expensive and verification must be explicit

Skip this skill for:

- one-file scripts
- tiny fixes with no cross-file coordination
- work that has no meaningful handoff or verification needs

## Core Terms

### Agent

An agent is one AI work session operating in a defined role. Roles describe ownership, not identity. A single session may take multiple roles if the work is small enough to keep coherent.

Common roles:

| Role | Primary domain | Typical outputs |
|---|---|---|
| Planner | architecture and contracts | design docs, API specs, data models |
| Backend | services and persistence | routers, schemas, models, tests |
| Frontend | user interface and client state | pages, components, hooks, tests |
| Pipeline | async processing and data flow | workers, processors, queue wiring |
| Integrator | end-to-end wiring | adapters, clients, coordination logic |
| QA | validation and regressions | tests, gate reports, release checks |
| DevOps | delivery infrastructure | CI, deployment config, runtime setup |

### Workflow

A workflow is a domain-specific playbook stored in `orchestra/workflows/`. It defines scope, build order, tests, verification, and handoff expectations for one role or one tightly related slice of work.

### Phase

A phase is a stage in the overall delivery lifecycle. Phases are sequential. Workflows inside a phase may run sequentially or in parallel if they do not touch the same outputs.

### Gate

A gate is a verification checkpoint between phases or features. Downstream work should not begin until the current gate passes.

### Handoff Log

A handoff log is a file written to `agents/logs/` that captures what was built, which contracts changed, known issues, and what the next agent must know.

## Required Project Structure

Create these files and directories in the consuming project:

```text
your-project/
├── agents/
│   └── logs/
├── orchestra/
│   ├── README.md
│   ├── lessons.md
│   └── workflows/
│       ├── 01-planning.md
│       ├── 02-core.md
│       └── ...
└── optional master instructions file
```

The optional master instructions file may be named `CLAUDE.md`, `AGENTS.md`, `.instructions.md`, or any equivalent project-level instructions artifact.

## Quick Start

1. Install this skill.
2. Create `agents/logs/` for handoff summaries.
3. Create `orchestra/README.md` with project-specific roles, phases, dependencies, and gate definitions.
4. Create `orchestra/lessons.md` to capture durable lessons.
5. Create numbered workflow files under `orchestra/workflows/`.
6. Keep shared contracts single-owner and define them before implementation starts.

After publishing this repository, install it with:

```bash
npx skills add PeterOla/agentic-workflow-orchestra --agent github-copilot --copy -y
```

## Default Framework Model

The default model uses five phases. Projects may rename them, but the sequencing intent should remain stable.

```text
Phase 0: Plan       -> design, contracts, decisions
Phase 1: Skeleton   -> parallel-safe scaffolding by domain
                       CONTRACT GATE
Phase 2: Core Flow  -> critical path features in dependency order
                       INTEGRATION GATE
Phase 3: Expand     -> independent features and polish
                       PRODUCTION GATE
Phase 4: Ship       -> deployment, rollout, operational readiness
```

If a project uses different names such as `Foundation` or `MVP Flow`, document the mapping in `orchestra/README.md` so agents do not treat the difference as a behavioral conflict.

## Parallel-Safety Rules

Work can run in parallel only when all of the following are true:

- the tasks do not edit the same files
- the tasks do not write to the same shared contract
- the tasks do not require the same migration slot or serialized resource
- the downstream verification can still determine which change caused a regression

Keep work sequential when:

- planning defines contracts for implementation
- one feature consumes the outputs of another
- shared types or schemas must change first
- integration depends on both sides existing
- deployment depends on passing verification

Decision rule:

```text
Does task B read or modify outputs from task A?
  Yes -> sequence A then B
  No  ->
    Do the tasks share files or shared contracts?
      Yes -> sequence them
      No  -> parallel is acceptable
```

## Shared Contract Rules

Shared contracts are the highest-conflict assets in multi-agent work. Treat them explicitly.

Rules:

1. Assign one owner for each shared contract.
2. Define shared contracts before downstream implementation begins.
3. Import contracts everywhere else. Do not redefine them.
4. If a contract must change mid-stream, sequence the change and re-run the relevant gate.

Examples of shared contracts:

- frontend types and backend response schemas
- API route definitions and client paths
- database models and migrations
- pipeline payload formats and service consumers

## Workflow Template

Use this minimal template for each file in `orchestra/workflows/`.

```markdown
# Workflow 01: Planning

> Agent Role: Planner
> Phase: Plan
> Depends on: project instructions
> Produces: design docs, contracts, delivery plan

## Purpose

State what this workflow owns and what it must not touch.

## Deliverables

- files or artifacts to create
- contracts to define or validate
- decisions to lock for downstream work

## Build Order

1. gather context
2. define scope
3. create or update artifacts
4. verify outputs

## Verification Checklist

- required outputs exist
- assumptions are documented
- downstream agents can consume the result

## Handoff

Write `agents/logs/<workflow>-complete.md` with built files, contracts, issues, and next steps.
```

## Handoff Protocol

When a workflow or significant work slice is complete:

1. Write a completion log in `agents/logs/`.
2. Record durable lessons in `orchestra/lessons.md`.
3. Update the active progress tracker or todo list.
4. Leave the repository clean and verifiable.

A useful handoff log includes:

- built or modified files
- contracts or interfaces added or changed
- known issues, assumptions, or TODOs
- recommended next step

## Lessons Format

Use this format in `orchestra/lessons.md`:

```markdown
### [Category]: [Short title]
**Date:** YYYY-MM-DD
**Workflow:** [workflow name]
**What happened:** [brief description]
**Rule:** [reusable rule]
```

## Unified Session Startup Checklist

Before starting substantive work:

1. Read the project's master instructions file if one exists.
2. Read this skill.
3. Read `orchestra/README.md`.
4. Read `orchestra/lessons.md`.
5. Read all files in `agents/logs/`.
6. Read the relevant file in `orchestra/workflows/`.
7. Identify the current phase and the next required gate.
8. Plan the task before editing.
9. Execute, verify, log, and hand off.

## Verification Gates

Start from these generic gates and adapt them to the project stack in `orchestra/README.md`.

### Contract Gate

- shared routes, schemas, and client calls agree
- auth expectations are consistent
- error response shapes are consistent
- naming and ownership of contracts are clear

### Behavior Gate

- happy path works
- loading state exists where async work occurs
- error state is explicit
- empty state exists where data may be absent
- the smallest supported viewport or interface target still works

### Integration Gate

- end-to-end critical path works
- retries and failure states are explicit for async tasks
- status transitions are observable and correct
- primary user-facing output is generated correctly
- minimum tests for touched surfaces exist

### Production Gate

- all earlier gates pass
- no hardcoded environment values remain
- input validation exists on user-controlled inputs
- auth covers non-public surfaces
- deployment or release process has been exercised
- monitoring or error capture strategy is defined

### Adapting Gates By Stack

Examples:

- API-only project: replace UI viewport checks with client contract and pagination checks.
- Frontend-only project: replace backend schema checks with mocked contract and runtime data-shape checks.
- Data or pipeline project: emphasize payload schemas, retries, idempotency, and processing observability.

## Rules

1. Project-specific instructions win over generic framework defaults.
2. One agent should own one workflow at a time unless the work is intentionally integrated.
3. Shared contracts must have a clear owner.
4. Do not parallelize overlapping file ownership.
5. Test and verify during implementation, not only at the end.
6. Log decisions and lessons so future sessions inherit context.
7. Keep changes as small and defensible as possible.
8. Do not mark work complete without evidence.

## Publish Sanity Check

Before releasing this skill publicly, confirm that:

- the install command points to the real public repository
- setup instructions create every required directory
- the skill reads coherently in a repository with no project-specific history
- examples are generic and not tied to one product
- one external user can follow the quick start without additional explanation