---
name: 044-planning-jira
description: Use when you need the Jira CLI (`jira`) to verify installation, configure Jira Cloud access, list issues (all or by JQL) as markdown tables, and analyze user-provided sanitized Jira summaries. Uses an interactive install gate - if `jira` is missing, ask whether to show installation guidance before any issue commands. This should trigger for requests such as jira issue list; List Jira issues; Jira JQL issue query; Jira CLI issue workflow. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Jira CLI - issues, workflows, and discussion for analysis

Use **`jira`** to work with Jira issues: **first** run an **interactive** check - if `jira` is not installed, **stop**, ask whether the user wants installation guidance, **wait** for an answer, then continue. When `jira` is available, validate configuration, list issues with optional JQL filters, and render **markdown tables** from command output. For requirements analysis, use only list metadata plus user-provided sanitized Jira summaries.

**What is covered in this Skill?**

- **Interactive** install gate: ask before assuming `jira` is installed; offer installation guidance only when the user agrees
- Install/config checks (`jira version`, `jira configure`)
- Jira Cloud context (site URL, account email, API token handled by CLI prompts)
- Issue lists: basic list and JQL-backed list queries
- Sanitized Jira summaries supplied by the user for requirement analysis
- Core actions: create, assign, and transition

## Constraints

Do not fabricate issue data; use only `jira` output (or explicitly agreed Jira REST API responses). Never print API tokens or secrets.

- **INTERACTIVE GATE**: If `jira` is missing, **stop**, ask whether the user wants installation guidance, **wait** - do not skip to issue listing
- **FIRST** (after gate): Verify `jira` is available before issuing subcommands
- **CONFIG**: Ensure Jira CLI is configured before private workspace operations
- **TABLES**: Prefer markdown pipe tables for issue list summaries
- **NO RAW BODY READS**: Do not run Jira commands that retrieve description or comment bodies; use list metadata plus user-provided sanitized summaries for analysis

## When to use this skill

- jira issue list
- List Jira issues
- Jira JQL issue query
- Jira issue summary workflow
- Jira CLI issue workflow

## Workflow

1. **Run interactive install gate**

Check `jira version`; if missing, stop and ask whether the user wants installation guidance before any issue operations.

2. **Verify Jira CLI configuration**

Ensure Jira CLI is configured (site/account/token flow via CLI prompts) before running private workspace commands.

3. **List issues with optional JQL**

Retrieve issues using basic listing or JQL filters and present summaries as markdown pipe tables.

4. **Request sanitized issue context for analysis**

Do not retrieve raw Jira description or comment bodies. If analysis needs detail beyond list metadata, ask the user for a sanitized summary of the relevant Jira issue context and note that raw discussion content was not ingested.

5. **Execute core Jira actions when requested**

Support create, assign, and transition actions using CLI commands while avoiding secret exposure.

## Reference

For detailed guidance, examples, and constraints, see [references/044-planning-jira.md](references/044-planning-jira.md).
