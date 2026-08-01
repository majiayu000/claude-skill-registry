---
name: univer-workspace-cli
description: "Use when installing or operating the independent Univer Workspace CLI application (`univer-workspace-cli`) for remote Workspace files, Personal or Team Spaces, task Worktrees, Sheet/Doc/Slide Units, Facade authoring, inspection, verification, import/export, screenshots, or review handoff. Do not use for local targets handled by `univer`."
hidden: true
---

# Univer Workspace CLI

Remote authoring and inspection for Univer Workspace files. The CLI provides Space discovery,
per-task Worktrees, version-matched Facade guidance, model readback, and browser review.

`univer-workspace-cli` is independent from `univer`, not a variant: it operates remote Workspace
files, while `univer` operates local univerfiles.

Install and configure the target Workspace:

```bash
npm install -g univer-workspace-cli
univer-workspace-cli config set-origin https://workspace.example.com
univer-workspace-cli login --username <name>
univer-workspace-cli doctor
```

## Keep the CLI current

Use these commands to compare the installed CLI with the latest public release:

```bash
univer-workspace-cli --version
npm view univer-workspace-cli@latest version --registry=https://registry.npmjs.org/
```

Complete the current Workspace task before upgrading. This CLI has no `update` command; install the
new package version explicitly, then reload its operational Skills:

```bash
npm install -g univer-workspace-cli@latest
univer-workspace-cli doctor --json
univer-workspace-cli skills get core
```

## Start here

This file is the discovery entry, not the operational guide. Before using Workspace commands for a
task, load the complete core Skill from the installed CLI:

```bash
univer-workspace-cli skills get core          # remote model, workflow, evidence, and handoff
univer-workspace-cli skills get core --full   # include direct references
```

Runtime Skills ship with the CLI so their commands and Facade APIs match the installed version.

## Core Model

- Configure one Workspace origin, then authenticate against it.
- A Space is the file container users browse. Personal and Team Spaces expose files identified by
  `fileId`.
- A Unit is editable Sheet, Doc, or Slide content identified by `unitId` after it is staged in a
  Worktree.
- Start every new task in a new Worktree. Continue a known Worktree only for rework on that same
  task; there is no implicit current Worktree or Unit.
- Command success is not correctness evidence. Read back the stored model and inspect rendered
  output when appearance matters.

Use public CLI and Facade surfaces. `execute` commits captured mutations as one Worktree revision,
and merge remains an explicit user review decision.

## Unit Skills

After core, load the Skill matching the target top-level Unit before authoring:

```bash
univer-workspace-cli skills get sheet
univer-workspace-cli skills get doc
univer-workspace-cli skills get slide
```

Use `univer-workspace-cli skills list` to discover the installed set. Each Unit Skill owns its
creation recipe, injected Facade root, readback guidance, and visual verification requirements.
Base and Board authoring are outside the current Workspace Skill surface.

## Task Routing

| Task | Load and use |
| --- | --- |
| Authenticate or discover a Personal/Team Space file | core |
| Stage an existing file or create/import a new Unit in a task Worktree | core + target Unit |
| Inspect or edit Sheet values, formulas, formatting, charts, or tables | core + `sheet` |
| Create or refine Doc paragraphs, rich text, tables, charts, or pagination | core + `doc` |
| Build or review Slide pages, shapes, text, images, tables, or charts | core + `slide` |
| Verify, screenshot, export, mark ready, or generate a review URL | core + target Unit |

## Why Univer Workspace CLI

- Space discovery resolves remote files before they enter a Worktree.
- Worktrees isolate one agent task until review, merge, or discard.
- Offline `api show` / `api find` resolves exact Facade symbols for the installed SDK.
- Runtime inspection and the Workspace review page verify stored and rendered results.
- Import/export and screenshots use the Workspace product runtime rather than unrelated file
  writers.

Do not substitute local office writers or bypass the remote Worktree lifecycle. Follow the loaded
core and Unit Skills for the supported path.

## Diagnose

```bash
univer-workspace-cli --help
univer-workspace-cli doctor
univer-workspace-cli skills list
univer-workspace-cli skills path
```

Use `univer-workspace-cli <command> --help` for exact syntax. If the CLI is unavailable, the
Workspace origin is not configured, authentication is missing, or `doctor` reports a blocking
runtime failure, stop and report the diagnostic instead of switching tools.
