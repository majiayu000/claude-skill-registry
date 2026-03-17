---
name: claude-md-doctor
description: Audit and improve CLAUDE.md files. Use when rules aren't working, context is bloated, or after learning a lesson that should become a rule.
disable-model-invocation: true
---

# CLAUDE.md Doctor

Audit, diagnose, and improve CLAUDE.md files for this project.

## Usage

- `/claude-md-doctor` or `/claude-md-doctor audit` — Full audit of all CLAUDE.md files
- `/claude-md-doctor add-rule <description>` — Add a new rule based on a lesson learned

## Audit Procedure

When invoked with `audit` or no arguments:

### Step 1: Discover All CLAUDE.md Files

Search for CLAUDE.md files at all levels:
- Project root: `./CLAUDE.md`
- Subdirectories: `./**/CLAUDE.md`
- User-level: `~/.claude/CLAUDE.md`

Report which files exist and their line counts.

### Step 2: Check Structure Against Best Practices

A well-structured CLAUDE.md should have these sections (in order of importance):

1. **What** — Project architecture overview (what this project IS)
2. **Domain** — Tech stack, key dependencies, language/framework conventions
3. **Validation** — Build, test, and lint commands (the verification loop)
4. **Critical Rules** — Never/always rules that prevent recurring mistakes

Check for each section. Report missing sections as warnings.

### Step 3: Analyze Health Metrics

- **Line count**: Warn if >200 lines (bloat risk — Claude loads this into every context)
- **Duplicate rules**: Flag rules that say the same thing in different words
- **Stale references**: Flag mentions of files/paths that don't exist
- **Vague rules**: Flag rules without concrete actions (e.g., "write clean code" — too vague)
- **Missing validation loop**: Critical warning if no build/test/lint commands are defined

### Step 4: Check Git Status

Run `git status CLAUDE.md` to check if the file is:
- Tracked and committed (good)
- Modified but uncommitted (warn: team won't see changes)
- Untracked (warn: not shared with team)

### Step 5: Generate Report

Output a structured report:

```
## CLAUDE.md Health Report

### Files Found
- ./CLAUDE.md (N lines) [committed/uncommitted/untracked]
- ./src/CLAUDE.md (N lines) [committed/uncommitted/untracked]

### Section Coverage
- [x] What (architecture)
- [ ] Domain (tech stack) — MISSING
- [x] Validation (build/test/lint)
- [ ] Critical Rules — MISSING

### Warnings
- Line count: N (target: <200)
- Duplicate rules found: ...
- Stale path references: ...

### Recommendations
1. Add a "Domain" section describing...
2. Add a "Critical Rules" section with...
```

## Add Rule Procedure

When invoked with `add-rule <description>`:

### Step 1: Parse the Lesson

Read the `$ARGUMENTS` after `add-rule` to understand what lesson was learned.

### Step 2: Formulate the Rule

Convert the lesson into a concrete, actionable rule:
- Start with "Always" or "Never"
- Be specific (mention files, commands, patterns)
- Include the WHY (so future Claude instances understand the reason)

Example: "Never use `rm -rf` on the build directory — use `make clean` instead, which preserves the cache"

### Step 3: Add to CLAUDE.md

- If a "Critical Rules" section exists, append the rule there
- If not, create the section at the end of the file
- Format as a bullet point

### Step 4: Confirm

Show the user the exact rule added and its location.
