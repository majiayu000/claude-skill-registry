---
name: linear-create-issue-in-project
description: "{{ 𝛀𝛀𝛀 }} Create a new Linear issue with automatic dependency detection"
model: opus
disable-model-invocation: true
allowed-tools: ["mcp__plugin_linear_linear__get_issue", "mcp__plugin_linear_linear__save_issue", "mcp__plugin_linear_linear__list_issues", "mcp__plugin_linear_linear__list_projects"]
argument-hint: [description | project name (optional)]
---

Create a new Linear issue from the following input:

```
$ARGUMENTS
```

## Parse the input

Split on `|`:
- Everything before `|` is the issue description
- Everything after `|` (if present) is a project name hint (e.g. `Foundry`, `Platform`)

## Before creating

1. Fetch the list of Linear projects
2. If a project name was provided:
   - Attempt to match it to an existing project (fuzzy match on name)
   - If no confident match is found, ask the user: "No project matching '[name]' was found. Should I create a new project with that name, or would you like to pick from the existing list?"
   - If no project name was provided, do not set a project
3. If a project was identified, fetch all existing issues in that project to understand current scope and state
4. If issues were fetched, analyse them to identify natural dependencies:
   - Issues this new one **blocks** (must be done first before others can proceed)
   - Issues this new one is **blocked by** (must wait for others to complete)
   - Issues this new one **relates to** (thematically linked but no hard dependency)
5. Propose: title, description, project (if any), priority, and all identified relationships — then wait for approval

## Create the issue

Once approved:
- Assign to `me`
- Set `project` only if one was determined above
- Set `priority` (default: Normal)
- Apply all relationship links
- Write a clear description in markdown covering what needs to be done and acceptance criteria

## Confirm

Return the new issue identifier and a direct link.
