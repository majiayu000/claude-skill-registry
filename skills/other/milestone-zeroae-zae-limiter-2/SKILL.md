---
name: milestone
description: Use when user says "/milestone", mentions a milestone version (e.g., "0.4.0", "v0.4.0"), or asks about release status or milestone progress.
user-invocable: true
argument-hint: [version] | list
allowed-tools: Bash(gh api:*), Bash(gh issue list:*), Bash(gh issue view:*)
context: fork
model: haiku
---

# Milestone Skill

Analyze and summarize GitHub milestone status.

## Modes

| Mode | Trigger | Purpose |
|------|---------|---------|
| **Status** | `/milestone 1.0.0`, `/milestone v0.7.0` | Analyze specific milestone |
| **List** | `/milestone list`, `/milestone` (no args) | Show all open milestones |

## Mode Detection

When this skill is invoked, arguments follow the skill name (e.g., `/milestone v0.5.0` passes "v0.5.0" as arguments).

**IMPORTANT:** Before doing anything else, identify the mode from the invocation arguments:

| Arguments | Mode | Action |
|-----------|------|--------|
| version number (e.g., `1.0.0`, `v0.7.0`) | Status | Follow Status Mode below |
| `list` | List | Follow List Mode below |
| (none) | List | Follow List Mode below |

## Status Mode

Extract the version from the user input. Normalize it (add "v" prefix if missing, e.g., `1.0.0` → `v1.0.0`).

Run these commands (replace VERSION with the normalized version):

**Step 1:** Get milestone details:
```bash
gh api repos/zeroae/zae-limiter/milestones --jq '.[] | select(.title == "VERSION") | {title, description, state, open_issues, closed_issues}'
```

**Step 2:** List all issues:
```bash
gh issue list --milestone "VERSION" --state all --json number,title,state,labels --jq '.[] | "\(.state)\t#\(.number)\t\(.title)"'
```

**Step 3:** If any issue title starts with "🎯", get its body:
```bash
gh issue view <number> --json title,body
```

See `status.md` for output format.

## List Mode

Run this command:
```bash
gh api repos/zeroae/zae-limiter/milestones --jq '.[] | "- \(.title): \(.description)"'
```

Output the results.
