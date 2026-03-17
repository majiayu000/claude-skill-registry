---
name: ln-003-push-all
description: "Commit and push ALL changes (staged + unstaged + untracked) to the remote repository"
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

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
Analyze → Doc Check → Lint Check → Stage → Commit → Push → Report
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

**Skip:** Version bumps (CHANGELOG, version fields) — those are done only on explicit user request.

### Phase 3: Lint Check
**MANDATORY READ:** `shared/references/ci_tool_detection.md` (Discovery Hierarchy + Command Registry)

Discover and run project linters before committing, per ci_tool_detection.md.

**Step 1: Discover linter setup** per ci_tool_detection.md discovery hierarchy. Also check: `CLAUDE.md`, `README.md`, `CONTRIBUTING.md` for lint instructions.

**Step 2: Run linters with auto-fix**

1. Run discovered lint commands with `--fix` flag (or equivalent per ci_tool_detection.md Auto-Fix column)
2. If linter reports errors that auto-fix cannot resolve — fix manually
3. If no linter config found in project — skip this phase (log: "No linter configuration found, skipping")
**Step 3: Verify**
1. Re-run linters without `--fix` to confirm zero errors
2. If errors remain after 2 fix attempts — report remaining errors to user and proceed

### Phase 4: Stage and Commit

1. Run `git add -A` to stage everything
2. Run `git diff --cached --stat` to show what will be committed
3. Run `git log --oneline -3` to match recent commit style
4. Compose a concise commit message summarizing ALL changes
5. Commit with `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>`

### Phase 5: Push and Report

1. Push to the current branch's remote tracking branch
2. Report: **branch name**, **commit hash**, **files changed count**

---

## Critical Rules

- **Stage everything:** `git add -A` — no partial commits
- **Match commit style:** Follow the project's existing commit message convention
- **Co-Author tag:** Always include `Co-Authored-By` line
- **No version bumps:** Skip CHANGELOG/version updates unless explicitly requested
- **Lint before commit:** Always attempt lint discovery; skip gracefully if no config found

---

**Version:** 1.0.0
**Last Updated:** 2026-02-12
