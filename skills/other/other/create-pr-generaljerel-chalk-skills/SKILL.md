---
name: create-pr
description: Create a GitHub pull request with structured body, visual preview from screenshots, and test instructions derived from project context
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Bash, Read, Glob, Grep
argument-hint: "[optional: PR description or target branch]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: git, pr, automation
---

Create a GitHub pull request from the current branch using `gh` CLI. Reads `chalk.json` for project context to generate better test instructions and embeds visual artifacts if available.

## Workflow

1. **Check prerequisites** — Run `git status` to verify:
   - Not on `main`/`master` (if so, warn and suggest creating a branch)
   - No uncommitted changes (if there are, suggest running `/commit` first)
   - Branch has commits ahead of base branch

2. **Analyze changes** — Run `git log main..HEAD --oneline` and `git diff main...HEAD --stat` to understand all changes.

3. **Read project context** — Read `.chalk/chalk.json` if it exists:
   - `test.command` — for test plan instructions
   - `dev.command` — for setup instructions
   - `routes` — to identify affected pages
   - `project.framework` — for framework-specific review notes

4. **Determine base branch** — Default to `main`. If the user specifies a different target, use that.

5. **Push the branch** — Run `git push -u origin <branch>` if not already pushed.

6. **Create the PR** — Use `gh pr create` with:
   - A concise title (under 70 characters) following conventional commit style
   - A structured body (see format below)

7. **Report** — Show the user the PR URL.

## PR Body Format

```markdown
## Summary
<1-3 bullet points describing what changed and why>

## Changes
<Bulleted list of specific changes, grouped by area>

## Test plan
<How to verify — include actual commands from chalk.json if available>
<e.g., "1. Run `npm run dev` 2. Navigate to /dashboard 3. Verify...">

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Visual Preview Section

After generating the body, check if `.github/pr-screenshots/` exists and contains `.png` or `.gif` files. If it does, append a `## Visual Preview` section before the footer:

```markdown
## Visual Preview

### <Page Name>
![<page-name>](/.github/pr-screenshots/<page-name>.png)
![<page-name> interaction](/.github/pr-screenshots/<page-name>.gif)
```

- Group images by page/route with subheadings
- Include both screenshots and GIFs if both exist
- Use relative paths — GitHub renders these inline in PR descriptions
- If no screenshots exist, omit this section

If no screenshots exist and the branch has UI changes (changes to components, pages, styles, templates), suggest running `/capture-pr-visuals` first.

## Title Convention

Match the conventional commit style of the primary change:
- `feat(scope): description` for feature branches
- `fix(scope): description` for bug fix branches
- If the branch has mixed types, use the most significant one

## Rules

- NEVER force push
- NEVER create PRs to `main` without user confirmation if there are destructive changes
- Always use `gh pr create` (not the GitHub web UI)
- Pass the PR body via HEREDOC for proper formatting
- If `gh` is not authenticated, tell the user to run `gh auth login`
- Include relevant issue references (e.g., "Closes #34") if the branch name or commits reference an issue
- Test plan should use actual commands from `chalk.json` when available (e.g., real `test.command`, real `dev.command`)
