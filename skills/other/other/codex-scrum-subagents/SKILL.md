---
name: codex-scrum-subagents
description: Install and operate a Scrum-oriented subagent kit for Codex projects. Use when work should follow Scrum roles or ceremonies such as Product Owner, Scrum Master, backlog refinement, sprint planning, daily scrum, sprint review, retrospective, story delivery, or release readiness with explicit handoffs between planning, implementation, QA, security, UX, and DevOps.
---

# Codex Scrum Subagents

## Overview

Materialize a project-local Scrum kit that adds two layers on top of the existing CodexAI skills:

- `.agent/` for ceremony playbooks, role briefs, and workflow manifests
- `.codex/agents/` for native Codex custom-agent TOMLs that follow the official subagent discovery path

Use this skill when the team needs explicit role boundaries and delivery handoffs instead of a single monolithic assistant flow.

## Quick Start

1. Run `python scripts/install_scrum_subagents.py --help`.
2. Install the bundled kit into the target project:

```bash
python scripts/install_scrum_subagents.py --target-root <project-root>
python scripts/install_scrum_subagents.py --target-root <project-root> --native-scope both
```

3. Inspect differences before updating:

```bash
python scripts/install_scrum_subagents.py --target-root <project-root> --diff --format json
```

4. Refresh only missing or changed files, with automatic backups for overwritten files:

```bash
python scripts/install_scrum_subagents.py --target-root <project-root> --update
```

5. Validate either the bundled kit or an installed `.agent` tree:

```bash
python scripts/validate_scrum_agent_kit.py --help
python scripts/validate_scrum_agent_kit.py
python scripts/validate_scrum_agent_kit.py --install-root <project-root>/.agent
python scripts/validate_scrum_agent_kit.py --target-root <project-root> --install-dir .meta/.agent --native-scope both
```

## Command Aliases

Use [references/command-aliases.md](references/command-aliases.md) when the user wants a shorthand trigger instead of the raw Python entry point.

Common shortcuts:

- `$scrum-install`: install the local `.agent` kit plus native `.codex/agents` Codex custom agents
- `$scrum-diff`: compare installed `.agent` and `.codex/agents` files against the source bundle
- `$scrum-update`: update only missing or changed files across both layers
- `$scrum-validate`: validate the bundle or installed `.agent` plus `.codex/agents` tree
- `$story-ready-check`, `$sprint-plan`, `$daily-scrum`, `$story-delivery`, `$sprint-review`, `$retro`, `$release-readiness`: jump straight to the ceremony or delivery workflow
- `scripts/run_scrum_alias.py`: execute an alias and optionally generate the mapped artifact
- `scripts/generate_scrum_artifact.py`: render reusable Scrum markdown artifacts from bundled templates
- Workflow artifacts now require complete fields by default; use `--allow-placeholders` only when you explicitly want a scaffold artifact with `_TODO_` markers.

## What Gets Installed

- `agents/`: Scrum core roles plus delivery specialists tuned for this pack.
- `workflows/`: ceremony-driven playbooks for refinement, planning, execution, review, retro, and release.
- `services/`: lightweight JSON manifests for docs tooling or UI surfaces.
- `ARCHITECTURE.md` and `README.md`: onboarding docs for the installed `.agent` kit.
- `assets/artifact-templates/`: user story, sprint goal, daily scrum, retrospective, story delivery, and release readiness templates.
- `.codex/agents/*.toml`: native Codex custom agents rendered from the Scrum role briefs so subagent activity can surface in the Codex app and CLI.

## Role Routing

- Start with [references/scrum-role-routing.md](references/scrum-role-routing.md) to choose the right subagent set for the request.
- Load [references/scrum-ceremonies.md](references/scrum-ceremonies.md) when the task is driven by a Scrum ceremony rather than a code change.
- Load [references/command-aliases.md](references/command-aliases.md) when the request uses shorthand commands like `$scrum-install`, `$story-ready-check`, or `$release-readiness`.
- Load [references/artifact-templates.md](references/artifact-templates.md) when the workflow needs a repeatable markdown output instead of free-form notes.
- Load [references/delivery-contracts.md](references/delivery-contracts.md) when multiple roles need explicit artifact handoffs.
- Load [references/subagent-boundaries.md](references/subagent-boundaries.md) before large orchestrations so responsibilities do not bleed across roles.

## Installation Notes

- Default install targets are `<project-root>/.agent` and `<project-root>/.codex/agents`.
- `--native-scope project|personal|both` controls whether native Codex custom agents land in the project, the personal `~/.codex/agents` folder, or both.
- Existing pack-managed files in either location block installation unless `--force` is supplied.
- `--diff` reports missing, changed, same, and extra files for both the `.agent` bundle and the native `.codex/agents` layer.
- `--update` copies only missing or changed files across both layers and writes a fresh provenance stamp.
- Validator supports both `--install-root` and the symmetric `--target-root` + `--install-dir` form so custom install directories stay aligned with native-agent validation.
- `--backup-dir` lets the caller choose where overwritten files are archived during update.
- The installer writes `.codexai-scrum-kit.json` into the installed folder so the project can track provenance and bundle counts.
- The installed subagents are designed to call back into existing skills like `codex-plan-writer`, `codex-domain-specialist`, `codex-security-specialist`, `codex-execution-quality-gate`, and `codex-project-memory` instead of duplicating that knowledge.
- Restart Codex after installation if you want newly installed native custom agents to be picked up immediately by the app or CLI.

## Guardrails

- Keep Product Owner focused on value, backlog, acceptance criteria, and sequencing.
- Keep Scrum Master facilitative; it owns flow and impediments, not solution details or scope decisions.
- Use delivery specialists only after backlog intent and sprint goal are explicit.
- Keep QA, security, and release checks attached to each story before marking it done.
