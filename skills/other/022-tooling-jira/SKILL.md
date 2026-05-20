---
name: 022-tooling-jira
description: Use when you need the Jira CLI (`jira`) to verify installation, configure Jira Cloud access, list issues (all or by JQL) as markdown tables, fetch issue descriptions and comments for analysis, or hand off to @014-agile-user-story when creating user stories from Jira threads. Uses an interactive install gate - if `jira` is missing, ask whether to show installation guidance before any issue commands. Part of the skills-for-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.14.0-SNAPSHOT
---
# Jira CLI - issues, workflows, and discussion for analysis

Use **`jira`** to work with Jira issues: **first** run an **interactive** check - if `jira` is not installed, **stop**, ask whether the user wants installation guidance, **wait** for an answer, then continue. When `jira` is available, validate configuration, list issues with optional JQL filters, render **markdown tables** from command output, load **full issue descriptions and comment threads** for analysis, and when the user wants user stories plus Gherkin, **chain to `@014-agile-user-story`** using Jira issue content as source material.

**What is covered in this Skill?**

- **Interactive** install gate: ask before assuming `jira` is installed; offer installation guidance only when the user agrees
- Install/config checks (`jira version`, `jira configure`)
- Jira Cloud context (site URL, account email, API token handled by CLI prompts)
- Issue lists: basic list and JQL-backed list queries
- Deep reads: issue detail and comments for requirement analysis
- Core actions: create, assign, transition, and add comments


## Constraints

Do not fabricate issue data; use only `jira` output (or explicitly agreed Jira REST API responses). Never print API tokens or secrets.

- **INTERACTIVE GATE**: If `jira` is missing, **stop**, ask whether the user wants installation guidance, **wait** - do not skip to issue listing
- **FIRST** (after gate): Verify `jira` is available before issuing subcommands
- **CONFIG**: Ensure Jira CLI is configured before private workspace operations
- **TABLES**: Prefer markdown pipe tables for issue list summaries
- **THREAD**: For analysis, include description and all comments (or explicitly summarize with omissions noted)
- **014**: For user stories from Jira issues, use `@014-agile-user-story` and align answers with Jira-sourced text

## When to use this skill

- jira issue list
- List Jira issues
- Jira JQL issue query
- jira issue view comments
- Jira CLI issue workflow

