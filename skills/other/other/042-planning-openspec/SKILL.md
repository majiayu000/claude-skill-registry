---
name: 042-planning-openspec
description: Use when you need to take a `*.plan.md` file and turn it into OpenSpec change artifacts by validating OpenSpec installation, initializing or reusing an OpenSpec project, and creating or updating a change proposal/spec/tasks flow. Includes a concrete workflow based on `examples/requirements-examples/problem1/requirements/openspec`. This should trigger for requests such as Convert `*.plan.md` into OpenSpec; Add change proposal from plan; Update existing OpenSpec project; Initialize OpenSpec in requirements folder. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# OpenSpec Change Planning from `*.plan.md`

Guide the process of turning an implementation plan (`*.plan.md`) into an OpenSpec change workflow. **This is an interactive SKILL**. It verifies CLI availability, initializes OpenSpec when needed, and then creates or updates a change with proposal, design, tasks, and spec deltas.

**What is covered in this Skill?**

- Input analysis from `*.plan.md` (scope, change-id candidate, affected capabilities)
- Installation and availability checks for OpenSpec CLI
- Recommended installation paths on macOS, Linux, and Windows using npm
- OpenSpec project bootstrapping with `openspec init`
- Existing-project workflow using `openspec list`, `openspec status`, `openspec show`
- Validation and completion flow with `openspec validate --all` and `openspec archive`
- Example-root workflow at `examples/requirements-examples/problem1/requirements/openspec`

## Constraints

Always execute OpenSpec commands from the parent directory that contains the `openspec/` folder. Do not invent requirements not present in the `*.plan.md`; convert plan intent into explicit OpenSpec change artifacts.

- **MUST**: Start by reading and summarizing the provided `*.plan.md`
- **MUST**: Check CLI availability with `openspec --version` before any OpenSpec operation
- **MUST**: If OpenSpec is missing, provide macOS, Linux, and Windows install guidance via npm command
- **MUST**: Offer `openspec init` when no OpenSpec project exists
- **MUST**: When creating a new OpenSpec project, run plain `openspec init` only (do not use `--tools ...` options)
- **MUST**: Use a stable change-id (for example: `add-dark-mode`) for status/show/archive commands
- **MUST**: Run `openspec validate --all` before archiving
- **MUST**: When a feature/change is completed (all checklist tasks done), guide the user to archive it (for example: `openspec archive us-001-god-analysis-api`)
- **MUST**: In `tasks.md`, generate a single OpenSpec checklist (`- [ ]` / `- [x]`) only; do not add a second table-based task list
- **MUST**: Explain whether the workflow creates a new change or updates an existing one
- **EDGE CASE**: If request scope is ambiguous, stop and ask a clarifying question before applying changes
- **EDGE CASE**: If required inputs, files, or tooling are missing, report what is missing and ask whether to proceed with setup guidance

## When to use this skill

- Convert `*.plan.md` into OpenSpec
- Add change proposal from plan
- Update existing OpenSpec project
- Initialize OpenSpec in requirements folder
- Validate and archive OpenSpec change

## Workflow

1. **Read and summarize plan input**

Read `references/042-planning-openspec.md` and the provided `*.plan.md`, then summarize scope and identify candidate change-id and affected capabilities.

2. **Check OpenSpec CLI and install gate**

Run `openspec --version`; if missing, provide npm installation guidance for macOS, Linux, and Windows before proceeding.

3. **Initialize or detect OpenSpec project**

From the parent directory containing `openspec/`, run project checks and offer `openspec init` (without `--tools`) when initialization is needed.

4. **Create or update change artifacts**

Explain whether this is a new or existing change, then create/update proposal, design, tasks, and spec deltas using a stable change-id.

5. **Validate and close workflow**

Run `openspec validate --all`; when checklist tasks are complete, guide the user to archive the change with `openspec archive <change-id>`.

## Reference

For detailed guidance, examples, and constraints, see [references/042-planning-openspec.md](references/042-planning-openspec.md).
