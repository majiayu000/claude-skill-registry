---
name: 043-planning-github-issues
description: Use when you need the GitHub CLI (`gh`) to verify installation, list issues (all or by milestone) as markdown tables, fetch issue bodies and comments for analysis, or hand off to @014-agile-user-story when creating user stories from GitHub threads. Uses an interactive install gate — if `gh` is missing, ask whether to show installation guidance before any issue commands. This should trigger for requests such as gh issue list; List GitHub issues; Issues in milestone; GitHub CLI issues; gh issue view comments. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# GitHub CLI — issues, milestones, and discussion for analysis

Use **`gh`** to work with GitHub issues: **first** run an **interactive** check—if `gh` is not installed, **stop**, ask whether the user wants installation guidance (see the consultative pattern in **`112-java-maven-plugins`**, Maven Wrapper step), **wait** for an answer, then continue. When `gh` is available, confirm auth, list issues with optional milestone filters, render **markdown tables** from `--json` output, load **full issue bodies and comment threads** for analysis, and when the user wants user stories plus Gherkin, **chain to `@014-agile-user-story`** using issue content as source material for the interactive questionnaire.

**What is covered in this Skill?**

- **Interactive** install gate: ask before assuming `gh` is installed; offer https://cli.github.com/ and OS hints when the user agrees
- Install/auth checks (`gh --version`, `gh auth status`, `gh auth login`)
- Repository context (`--repo`, inferred from git remote)
- Issue lists: states, limits, milestone filter, `gh issue list --json` for tabular output
- Milestone discovery via `gh api` when titles are unknown
- Deep reads: `gh issue view` with `--json` (body, comments) or `--comments`

## Constraints

Do not fabricate issue data; use only `gh` output (or explicitly agreed public REST API responses). Never print tokens or secrets.

- **INTERACTIVE GATE**: If `gh` is missing, **stop**, ask whether the user wants installation guidance, **wait**—do not skip to issue listing
- **FIRST** (after gate): Verify `gh` is available before issuing subcommands
- **TABLES**: Prefer `--json` + markdown pipe tables for issue list summaries
- **THREAD**: For analysis, include body and all comments (or explicitly summarize with omissions noted)

## When to use this skill

- gh issue list
- List GitHub issues
- Issues in milestone
- GitHub CLI issues
- gh issue view comments

## Workflow

1. **Run interactive install gate**

Check `gh --version`; if missing, stop and ask whether the user wants installation guidance before any issue operations.

2. **Verify authentication and repository context**

Confirm `gh auth status`, authenticate if needed, and establish target repository context via `--repo` or git remote.

3. **List issues and milestones**

Retrieve issues (optionally by milestone/state) using `gh issue list --json` and present summaries as markdown pipe tables.

4. **Load full thread for analysis**

Read issue body and all comments via `gh issue view --json` or `--comments`, then provide evidence-based analysis.

5. **Chain to user story workflow when requested**

When user asks for user stories and Gherkin from issues, hand off to `@014-agile-user-story` using GitHub-sourced content.

## Reference

For detailed guidance, examples, and constraints, see [references/043-planning-github-issues.md](references/043-planning-github-issues.md).
