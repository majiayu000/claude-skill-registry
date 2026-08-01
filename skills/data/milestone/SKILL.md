---
name: milestone
description: Analyze and summarize GitHub milestone status.
---

---
description: When users mention a milestone version (e.g., "0.4.0", "v0.4.0") or ask about release status, invoke this skill to analyze GitHub milestone progress, issues, and suggest next steps.
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

1. **If version number provided** (e.g., `1.0.0`, `v0.7.0`, `0.5`) → **Status mode**
2. **If `list` keyword** → **List mode**
3. **If no arguments** → **List mode**

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
