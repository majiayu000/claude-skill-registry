---
name: sync-copilot-workflows
version: 1.0.0
description: '[AI & Tools] Sync workflow catalog from workflows.json to GitHub Copilot instructions. Run after adding/removing/modifying workflows to keep copilot-instructions.md up to date. Copilot has no hooks, so this manual sync replaces the auto-injection that Claude Code gets from workflow-router.cjs.'
allowed-tools: Bash, Read
---

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Sync Copilot Workflows

Generate and update the workflow catalog in `.github/copilot-instructions.md` from the source of truth `.claude/workflows.json`.

---

## When to Use

- After adding, removing, or modifying workflows in `.claude/workflows.json`
- After running `/ai-dev-tools-sync` to ensure workflow parity
- When copilot workflow catalog is stale or drifted

**NOT for**: Claude Code workflow issues (Claude gets auto-injected catalog via `workflow-router.cjs` hook).

---

## What To Do

1. Run the sync script:

```bash
node .claude/scripts/sync-copilot-workflows.cjs
```

2. Verify the output shows the correct workflow count and "Updated" message
3. Optionally preview first with `--dry-run`:

```bash
node .claude/scripts/sync-copilot-workflows.cjs --dry-run
```

---

## How It Works

- **Source of truth:** `.claude/workflows.json` (32 workflows, keyword matching, sequences)
- **Target:** `.github/copilot-instructions.md` section `## Workflow Catalog`
- **Script:** `.claude/scripts/sync-copilot-workflows.cjs`
- The script generates a keyword lookup table, full workflow details, handoff table, and execution protocol
- The generated section has `<!-- AUTO-GENERATED -->` markers to prevent manual edits

---

## Why This Exists

Claude Code has `workflow-router.cjs` hook that auto-injects the workflow catalog on every prompt.
GitHub Copilot has no hook system, so the catalog must be statically embedded in `copilot-instructions.md`.
This skill bridges that gap with a one-command sync.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
