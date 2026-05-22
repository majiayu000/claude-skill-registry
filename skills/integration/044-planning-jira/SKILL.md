---
name: 044-planning-jira
description: Use when you need the Jira CLI (`jira`) to verify installation, configure Jira Cloud access, list issues (all or by JQL) as markdown tables, and fetch issue descriptions and comments for analysis. Uses an interactive install gate - if `jira` is missing, ask whether to show installation guidance before any issue commands. This should trigger for requests such as jira issue list; List Jira issues; Jira JQL issue query; jira issue view comments; Jira CLI issue workflow. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.15.0-SNAPSHOT
---
# Jira CLI - issues, workflows, and discussion for analysis

Use **`jira`** to work with Jira issues: **first** run an **interactive** check - if `jira` is not installed, **stop**, ask whether the user wants installation guidance, **wait** for an answer, then continue. When `jira` is available, validate configuration, list issues with optional JQL filters, render **markdown tables** from command output, and load **full issue descriptions and comment threads** for analysis.

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

## When to use this skill

- jira issue list
- List Jira issues
- Jira JQL issue query
- jira issue view comments
- Jira CLI issue workflow

## Workflow

1. **Run interactive install gate**

Check `jira version`; if missing, stop and ask whether the user wants installation guidance before any issue operations.

2. **Verify Jira CLI configuration**

Ensure Jira CLI is configured (site/account/token flow via CLI prompts) before running private workspace commands.

3. **List issues with optional JQL**

Retrieve issues using basic listing or JQL filters and present summaries as markdown pipe tables.

4. **Load issue details and discussion**

Read full issue descriptions and all comments for analysis, explicitly noting any omissions when summarizing.

5. **Execute core Jira actions when requested**

Support create, assign, transition, and add-comment actions using CLI commands while avoiding secret exposure.

## Reference

For detailed guidance, examples, and constraints, see [references/044-planning-jira.md](references/044-planning-jira.md).
