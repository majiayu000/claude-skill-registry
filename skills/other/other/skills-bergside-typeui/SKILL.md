---
name: typeui-cli
description: Guide for agentic tools to use the typeui.sh CLI for generating, updating, listing, and pulling design system skill files.
---

# typeui.sh CLI Operator Skill

## Mission

Use `typeui.sh` to generate, update, list, and pull design-system skill files for agentic tooling in a project.

## When To Use This Skill

- User asks to create or refresh design-system instructions for agents.
- User wants to pull an existing style by slug.
- User wants to browse available styles and select one interactively.
- User asks for preview-only runs before writing files.

## Preconditions

- Run commands from the target project root.
- Node.js 18+ is available.
- If running from this repository source, build first:
  - `npm install`
  - `npm run build`

## Command Reference

- `npx typeui.sh generate`
  - Run interactive prompts and create new managed skill content.
- `npx typeui.sh update`
  - Update existing managed sections in generated files.
- `npx typeui.sh pull <slug>`
  - Pull a specific registry skill and write it to selected provider paths.
- `npx typeui.sh list`
  - List available registry slugs, show preview links, and pull one selection.
- `npx typeui.sh verify`
  - Verify and cache license state for license-aware workflows.
- `npx typeui.sh license`
  - Show local cached license summary.
- `npx typeui.sh clear-cache`
  - Clear local `~/.typeui-sh` cache state.

## Local Dev Invocation (This Repo)

- `node dist/cli.js --help`
- `node dist/cli.js generate`
- `node dist/cli.js update`
- `node dist/cli.js list`
- `node dist/cli.js pull <slug>`

## Shared Flags

- `-p, --providers <providers>`
  - Comma-separated providers (example: `cursor,codex`).
- `--dry-run`
  - Preview file changes without writing.

## Provider Behavior

- Universal target is always included: `.agents/skills/design-system/SKILL.md`.
- Selected providers add extra output targets (for example `.cursor/...`, `.codex/...`).

## Registry Behavior

- Source of truth for list/pull data is:
  - `https://github.com/bergside/awesome-design-skills`
- Registry index used by CLI:
  - `https://raw.githubusercontent.com/bergside/awesome-design-skills/main/skills/index.json`
- `pull <slug>` flow:
  1. Validate slug format.
  2. Resolve `skillPath` from index.
  3. Fetch markdown from the raw GitHub path.
- `list` flow:
  - Reads the same index and shows preview links from:
  - `https://www.typeui.sh/design-systems/<slug>`

## Recommended Agent Workflow

1. If user knows the style: run `pull <slug> --dry-run` first.
2. If user does not know the style: run `list` and select one.
3. Re-run without `--dry-run` when preview looks correct.
4. Report generated/updated file paths and whether each changed.

## Troubleshooting

- `Registry pull failed: not_found`
  - Slug is not in registry index or markdown path is missing.
  - Run `list` and pick a valid slug.
- `Slug must contain only lowercase letters, numbers, dashes, or underscores`
  - Normalize slug format before retrying.
- `No existing managed design system found` during `update`
  - Run `generate` first to create managed blocks.
