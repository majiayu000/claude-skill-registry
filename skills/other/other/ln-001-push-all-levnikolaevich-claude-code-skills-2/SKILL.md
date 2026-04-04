---
name: ln-001-push-all
description: "Commits and pushes all changes (staged, unstaged, untracked) to remote. Use when you need a quick push of everything at once."
disable-model-invocation: true
license: MIT
model: claude-sonnet-4-6
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Push All (Standalone Utility)

**Type:** Standalone Utility
**Category:** 0XX Shared

Commits and pushes ALL current changes (staged, unstaged, untracked) to the remote repository in a single operation.

---

## When to Use This Skill

- Quick push of all accumulated changes without manual staging
- End-of-session commit when all changes are ready
- Any situation where `git add -A && git commit && git push` is the intent

---

## Workflow

```
Analyze → Doc Check → CHANGELOG → Lint Check → Stage → Commit → Push → Report
```

### Phase 1: Analyze Changes

1. Run `git diff --stat` and `git status` to understand ALL changes (staged, unstaged, untracked)
2. Identify what was changed and why

### Phase 2: Documentation Check

Check if related documentation needs updating:

| Change Type | Action |
|-------------|--------|
| Code behavior changed | Update affected docs, comments, examples |
| New files/folders added | Update relevant index or list sections |
| Config files changed | Check README or setup docs |
| No doc impact | Skip |

**Skip:** Version bumps (version fields in SKILL.md, README badge) — those are done only on explicit user request.

### Phase 3: CHANGELOG Update

If `CHANGELOG.md` exists and changes are significant (not just lint/formatting fixes):

1. Check if today's date already has an entry (`## YYYY-MM-DD`)
2. If yes — append new bullets to existing entry
3. If no — add new `## YYYY-MM-DD` entry (newest first)
4. Write **max 5 bullets**, each starting with `- **Bold label** — description`
5. Only user-visible or architecturally significant changes. Skip: renumbering, internal refactoring, structural fixes, deduplication

| Include | Skip |
|---------|------|
| New capabilities / skills | Renumbering, renaming |
| Workflow changes | Internal refactoring (D1-D9 fixes) |
| Breaking changes | Deduplication passes |
| New integrations | Reference file moves |
| Performance improvements users notice | Token efficiency numbers |

**Skip if:** no `CHANGELOG.md` in project, or changes are trivial (whitespace, lint auto-fixes only).

### Phase 4: Lint Check
**MANDATORY READ:** `shared/references/ci_tool_detection.md` (Discovery Hierarchy + Command Registry)

Discover and run project linters before committing, per ci_tool_detection.md.

**Step 1: Discover linter setup** — first check `docs/project/runbook.md` for explicit lint/format commands (they take priority over auto-detection), then follow ci_tool_detection.md discovery hierarchy. Also check: `CLAUDE.md`, `README.md`, `CONTRIBUTING.md` for lint instructions.

**Step 2: Run linters with auto-fix**

1. Run discovered lint commands with `--fix` flag (or equivalent per ci_tool_detection.md Auto-Fix column)
2. If linter reports errors that auto-fix cannot resolve — fix manually
3. If no linter config found in project — skip this phase (log: "No linter configuration found, skipping")
**Step 3: Verify**
1. Re-run linters without `--fix` to confirm zero errors
2. If errors remain after 2 fix attempts — report remaining errors to user and proceed

### Phase 5: Stage and Commit

1. Run `git add -A` to stage everything
2. Run `git diff --cached --stat` to show what will be committed
3. Run `git log --oneline -3` to match recent commit style
4. Compose a concise commit message summarizing ALL changes
5. Commit with `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`

### Phase 6: Push and Report

1. Push to the current branch's remote tracking branch
2. Report: **branch name**, **commit hash**, **files changed count**

---

## Critical Rules

- **Stage everything:** `git add -A` — no partial commits
- **Match commit style:** Follow the project's existing commit message convention
- **Co-Author tag:** Always include `Co-Authored-By` line
- **No version bumps:** Skip version field updates (SKILL.md Version, README badge) unless explicitly requested
- **Lint before commit:** Always attempt lint discovery; skip gracefully if no config found

---

## Definition of Done

- [ ] All changes staged (untracked + modified)
- [ ] Commit created with descriptive message
- [ ] Pushed to remote successfully

---

**Version:** 1.0.0
**Last Updated:** 2026-02-12
