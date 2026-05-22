---
name: copilot-review
description: Perform code reviews using GitHub Copilot CLI to identify bugs, security vulnerabilities, performance issues, and code quality problems. Use when the user asks to review code, check for issues, security audit, or before committing. Requires Copilot CLI installed.
allowed-tools: Bash, Read, Grep, Glob
---

# Copilot Review Skill

Use GitHub Copilot CLI to perform automated code reviews that identify issues and suggest improvements. This is a read-only analysis skill.

## When to Use

- User asks to review code
- User wants to check for bugs or issues
- User mentions security, performance, or quality
- Before committing code
- During pull request review
- User asks "what's wrong with this code?"

## Prerequisites

Verify GitHub Copilot CLI is available:

```bash
copilot --version
```

Note: Copilot will ask you to trust the files in the current folder before it can read them.

## Basic Usage

### Step 1: Determine Scope

Decide what to review:

- Uncommitted changes
- Specific files
- Last commit
- Pull request
- Entire codebase

### Step 2: Check Current State

```bash
git status
git diff --stat
git diff
```

### Step 3: Launch Copilot CLI

```bash
cd /path/to/project
copilot
```

### Step 4: Execute Review

Use a structured prompt:

```
Perform a comprehensive code review of [SCOPE].

Check for:
1. Critical issues (must fix): security vulnerabilities, runtime errors, data loss risks
2. Important issues (should fix): logic bugs, performance problems, type safety gaps
3. Suggestions (nice to have): refactors, better patterns, documentation

For each issue:
- Severity (Critical/Important/Suggestion)
- File path and line number
- Why it matters
- How to fix it

Do NOT make any changes - this is review only.
```

### Step 5: Present Findings

Organize results by severity.

## Tips

- Use `@path/to/file` to focus on specific files.
- Use `/usage` to view session usage details.
- Use `/model` to pick another model if needed.
- Use `?` or `copilot help` to see available commands.

## Use Custom Instructions

Copilot CLI automatically loads repository instructions if present:

- `.github/copilot-instructions.md`
- `.github/copilot-instructions/**/*.instructions.md`
- `AGENTS.md` (agent instructions)

## Error Handling

- If Copilot is not found, ensure it is installed per the prerequisites in README.md and available in PATH.
- If authentication fails, run `/login` and follow prompts.
- If output is too high-level, narrow scope and include file paths.

## Related Skills

- `copilot-ask` for read-only questions
- `copilot-exec` for code modifications

## Limitations

- Read-only analysis
- Interactive mode only
- Limited by current codebase context
