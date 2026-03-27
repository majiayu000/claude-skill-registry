---
name: linear-create-issue-related-to
description: "{{ ƔƔƔ }} Create a new Linear issue with optional relations"
model: sonnet
disable-model-invocation: true
allowed-tools: ["mcp__plugin_linear_linear__get_issue", "mcp__plugin_linear_linear__save_issue", "mcp__plugin_linear_linear__list_issues", "mcp__plugin_linear_linear__list_projects"]
argument-hint: [description | FOU-123, FOU-456 (optional)]
---

Create a new Linear issue from the following input:

```
$ARGUMENTS
```

## Parse the input

Split on `|`:
- Everything before `|` is the issue description
- Everything after `|` (if present) is a comma-separated list of related issue IDs (e.g. `FOU-123, FOU-456`)

## Before creating

1. Fetch the list of Linear projects to identify the best placement based on the description
2. If related issue IDs were provided, fetch each one to understand their context and determine the correct relationship type:
   - **Blocks**: the new issue must be completed before the related issue can proceed
   - **Blocked by**: the related issue must be completed before this one
   - **Relates to**: general relation with no dependency direction
3. Infer the appropriate project from the description and related issues' projects
4. Propose: title, description, project, priority, and relationships — then wait for approval

## Create the issue

Once approved:
- Assign to `me`
- Set `project` if determined above
- Set `priority` (default: Normal)
- Apply relationship links to all provided issue IDs
- Write a clear description in markdown with what needs to be done and acceptance criteria

## Confirm

Return the new issue identifier and a direct link.
