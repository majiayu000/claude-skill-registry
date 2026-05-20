---
name: linear-check-deps-omega
description: "{{ 𝛀𝛀𝛀 }} Analyse and assign dependency relationships for Linear tasks"
model: opus
disable-model-invocation: true
allowed-tools: ["mcp__plugin_linear_linear__get_issue", "mcp__plugin_linear_linear__save_issue", "mcp__plugin_linear_linear__list_issues"]
argument-hint: [FOU-123, FOU-456, ...]
---

Analyse dependency relationships for the following Linear task(s):

```
$ARGUMENTS
```

## Tools

Use the Linear MCP tools (`mcp__plugin_linear_linear__*`) for all Linear API interactions.

## Parse the input

Split on `,` or whitespace to extract one or more Linear issue IDs (e.g. `FOU-123`, `FOU-456`).

## Analyse

1. Fetch each provided issue using `mcp__plugin_linear_linear__get_issue` to understand its scope, description, and current relationships
2. Identify the parent project for each issue (if they span multiple projects, analyse each project separately)
3. Fetch active issues in each relevant project using `mcp__plugin_linear_linear__list_issues` with the `project` parameter. **Exclude completed, cancelled, and duplicate issues** — only fetch issues in active states (backlog, todo, in progress, in review, etc.)
4. For each provided issue, analyse the project context and determine:
   - **Blocks**: which project issues cannot proceed until this one is done
   - **Blocked by**: which project issues must be completed before this one can start
   - Skip issues that already have the correct relationship assigned
5. Present a summary table per issue:
   - Issue ID + title
   - Proposed **blocks** relationships (with brief justification)
   - Proposed **blocked by** relationships (with brief justification)
   - Any existing relationships that appear incorrect or redundant

Wait for approval before making changes.

## Apply

Once approved:
- Add all accepted relationship links using `mcp__plugin_linear_linear__save_issue`
- Do not remove existing relationships unless explicitly asked

## Confirm

Return a summary of all relationships added, grouped by issue.
