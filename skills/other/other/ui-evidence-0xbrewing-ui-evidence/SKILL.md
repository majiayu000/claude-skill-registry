---
name: ui-evidence
description: Use when an agent needs to bootstrap ui-evidence in a repo, then discover, configure, or run before/after UI screenshot capture, current UI snapshot capture, local HTML review generation, or git-baseline UI evidence workflows for a web app.
---

# UI Evidence

Use this skill when the user wants an agent to:

- bootstrap `ui-evidence` into the current repo
- capture `before` and `after` UI screenshots
- capture the current UI into a reviewable snapshot bundle
- compare two UI states locally
- generate a review page a human can scan quickly
- persist a reusable config for future UI work
- compare the current checkout against another git ref

This skill is intentionally thin. The CLI is the engine.
The skill is the agent-facing entrypoint. The package provides the repo-local executable that actually runs capture and review commands.

## Bootstrap first

1. Detect the repo package manager from `packageManager` or lockfiles.
2. Check whether the repo can already run `ui-evidence`.
3. If the CLI is missing, install it from GitHub:

```bash
pnpm add -D github:0xBrewing/ui-evidence
npm install -D github:0xBrewing/ui-evidence
yarn add -D github:0xBrewing/ui-evidence
bun add -d github:0xBrewing/ui-evidence
```

4. Run the repo bootstrap step with the matching package runner:

```bash
pnpm exec ui-evidence install --agent both --config ./ui-evidence/config.yaml
npx ui-evidence install --agent both --config ./ui-evidence/config.yaml
yarn ui-evidence install --agent both --config ./ui-evidence/config.yaml
bunx ui-evidence install --agent both --config ./ui-evidence/config.yaml
```

That bootstrap should leave repo-local skill copies in `.agents/skills/ui-evidence/` for Codex and `.claude/skills/ui-evidence/` for Claude Code.

## Default flow

1. Run `ui-evidence discover`.
2. Read the suggested config and unresolved list.
3. Ask only about unresolved values.
4. Create or patch `ui-evidence/config.yaml`.
5. Add `ui-evidence/hooks/*` only if deterministic state is needed.
6. Run `ui-evidence doctor`, then `ui-evidence doctor --ready` if route or wait-target confidence is still low.
7. Run `ui-evidence run`, `ui-evidence snapshot`, or `capture/compare/report/review`.
8. Summarize:
   - `review/index.html`
   - `report.<lang>.md`
   - `manifest.json`
   - pair and overview images, or current snapshot captures and overview images

## Commands to prefer

```bash
ui-evidence discover --format json
ui-evidence init --interactive --config ./ui-evidence/config.yaml
ui-evidence doctor --config ./ui-evidence/config.yaml
ui-evidence doctor --config ./ui-evidence/config.yaml --ready --profile mobile-en
ui-evidence run --config ./ui-evidence/config.yaml --stage <stage-id>
ui-evidence run --config ./ui-evidence/config.yaml --stage <stage-id> --before-ref main
ui-evidence run --config ./ui-evidence/config.yaml --stage <stage-id> --after-attach http://127.0.0.1:3000 --resume
ui-evidence snapshot --config ./ui-evidence/config.yaml --scope <scope-id>
ui-evidence review --config ./ui-evidence/config.yaml --stage <stage-id>
```

`ui-evidence review --stage <stage-id>` reuses the latest snapshot `current` captures when a stage has no before/after comparison artifacts yet. If neither stage artifacts nor snapshot artifacts exist, it should fail instead of emitting an empty review.

## What to inspect locally first

- package manager and dev scripts
- Playwright config and existing auth states
- harness routes or storybook routes
- stable `data-testid` targets
- existing screenshot folders
- whether the repo can boot from another git ref

## Rules

- Prefer this skill as the install entrypoint when it is available through `skills add`.
- Use the package-manager-native runner for every `ui-evidence` command.
- Keep stage definitions stable and additive.
- Prefer existing harness routes over fragile live flows.
- Prefer `testId` waits over loose selectors.
- Treat `review/index.html` as the default human-facing artifact.
- Keep hooks small and deterministic.
- Do not re-implement browser automation in prompt text.
