---
name: work-issue
description: Pick up a GitHub issue — fetch details, create a branch, and set up context for implementation
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Bash, Read, Glob, Grep
argument-hint: "<issue number or URL>"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: git, issues, automation
---

Start working on a GitHub issue. Fetches the issue details, creates a properly named branch, reads project context from `chalk.json`, and sets up a todo list for implementation.

## Workflow

1. **Fetch issue details** — Use `gh issue view <number> --json title,body,labels,assignees,milestone` to get the full issue context.

2. **Read project context** — If `.chalk/chalk.json` exists, read it to understand:
   - `sourceLayout` — where to create/modify files
   - `routes` — which pages might be affected
   - `project.framework` — framework-specific patterns to follow
   - `dev.command` — how to run the project for testing

3. **Create a branch** — Name it based on the issue:
   - Feature: `feat/<issue-number>-<short-description>`
   - Bug fix: `fix/<issue-number>-<short-description>`
   - Chore: `chore/<issue-number>-<short-description>`
   - Derive the type from issue labels (`bug` → fix, `enhancement` → feat, default → feat)
   - Keep the description to 3-5 kebab-case words from the issue title

   ```bash
   git checkout -b feat/<issue-number>-<description>
   ```

4. **Analyze scope** — Based on the issue description and chalk.json:
   - Identify which files/directories will likely need changes
   - Identify affected routes (from `chalk.json` routes + sourceLayout mapping)
   - Note any related files that should be read before starting

5. **Set up todo list** — Create a task list based on the issue requirements:
   - Break the issue into specific implementation steps
   - Include a "verify changes" step at the end
   - If the issue mentions testing, include a test step

6. **Report** — Print:
   - Issue title and key details
   - Branch name created
   - Files/areas likely to be affected
   - Todo list for implementation
   - Suggest: "Read the relevant source files, then start implementing."

## Rules

- Always create the branch from `main` (checkout main and pull first)
- Never assign the issue unless the user asks
- If the issue is already assigned to someone else, warn the user
- If there's already a branch for this issue (check `git branch -a`), ask the user if they want to use the existing branch
- Keep branch names short — max 50 characters total
- If `chalk.json` doesn't exist, skip the project context step — the skill still works, just with less context
