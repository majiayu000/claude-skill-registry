---
name: plans-randlee-synaptic-canvas
description: 'Last Updated: 2025-01-22'
---

# Claude Skill Creation Skill – Plan
Status: Proposed
Owner: TBD
Last Updated: 2025-01-22

## Goals
- Provide a repeatable `/skill-plan` and `/skill-review` workflow for creating/updating Claude Code skills, commands, and agents.
- Enforce v0.4 guidelines (`docs/claude-code-skills-agents-guidelines-0.4.md`) and mirror the Anthropic `skill-creator` reference (`/Users/randlee/Documents/github-radiant/claude-skills/skill-creator`).
- Keep commands thin; delegate planning/review work to agents with structured, fenced JSON outputs.

## References
- Guidelines: `docs/claude-code-skills-agents-guidelines-0.4.md`
- Example skill: `/Users/randlee/Documents/github-radiant/claude-skills/skill-creator/SKILL.md`
- Agent version registry: `.claude/agents/registry.yaml` (required for version enforcement)

## User Commands (all support `--help`)
- `/skill-plan [<path>] [--name <plan-name>] [--from <existing-plan>] [--template <path>]`
  - If `<path>` exists (file or folder), resume and append to the plan; otherwise start a wizard-driven planning session and write to `plans/<plan-name>.md`.
  - Minimal responsibility: collect inputs and invoke agents; business logic lives in skills/agents.
- `/skill-review <target> [--scope command|skill|agent|all] [--fix]`
  - `target` can be a name or path to a command/skill/agent.
  - Runs background review against guidelines and manifests; optional `--fix` triggers suggested updates.

## Modes & Flow
- Planning mode (wizard):
  1) Capture core responsibilities and success criteria.
  2) Capture use cases and variants.
  3) Define command UX: options/flags, `--help` text, required args.
  4) Map agents and fenced JSON inputs/outputs; note registry versions.
  - Produces preliminary plan (Status: Preliminary), then upgrades to Proposed after user confirms summary.
- Review loop:
  - Sequence: plan → review → update → review → approve.
  - Skill produces a concise 40–80 line overview with full plan path for user approval (Status: Approved).

## Agents (single-responsibility)
- `skill-planning-agent` (background): synthesizes plan drafts, suggests architecture, ensures progressive disclosure, proposes file layout.
- `skill-review-agent` (background): checks commands/skills/agents vs guidelines (versioning, fenced JSON, envelopes, registry alignment, safety checks).
- Agent runner usage is required; resolves path+version from registry and fences JSON outputs.

## Data Contracts
- All agent outputs fenced as ```json blocks with minimal envelope:
  ```json
  { "success": true, "data": { "summary": "...", "actions": [] }, "error": null }
  ```
- Review agent may return structured findings:
  ```json
  { "success": true, "data": { "issues": [{ "severity": "error", "path": "skills/x/SKILL.md", "rule": "fenced-json" }] }, "error": null }
  ```
- Plan document fields: Status, Context/Goals, Command UX, Agent inventory (name/version/path), Data contracts, File layout, Open questions.

## File Layout (proposed)
- Plans: `plans/skill-creation-skill.md` (this plan; becomes Approved after user sign-off).
- Commands: `.claude/commands/skill-plan.md`, `.claude/commands/skill-review.md` (thin wrappers).
- Skill: `.claude/skills/skill-creation/SKILL.md` (planning/review orchestrator using Agent Runner).
- Agents: `.claude/agents/skill-planning-agent.md`, `.claude/agents/skill-review-agent.md` with YAML frontmatter `name` + `version`.
- References: `.claude/references/plan-skeleton.md`, `.claude/references/skill-patterns.md` (templates/patterns); keep SKILL.md lean and point here.
- Reports: default to `reports/skill-reviews/...` (fallback `.tmp/skill-reviews/`).

## Safety & Validation
- Enforce version sync with `.claude/agents/registry.yaml`; validate via `scripts/validate-agents.py`.
- All command inputs validated before agent calls; dangerous operations require explicit confirmations.
- Keep main conversation clean: summarize outcomes; omit tool traces.

## Next Steps
- Confirm plan scope/owner and finalize plan Status to Approved after review.
- Implement command markdowns, SKILL.md, and agents following this plan and guidelines.
