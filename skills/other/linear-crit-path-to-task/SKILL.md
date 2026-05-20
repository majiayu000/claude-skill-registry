---
name: linear-crit-path-to-task
description: "{{ 𝛀𝛀𝛀 }} Decompose a Linear issue into a critical path of granular issues"
model: opus
disable-model-invocation: true
allowed-tools: ["mcp__plugin_linear_linear__get_issue", "mcp__plugin_linear_linear__save_issue", "mcp__plugin_linear_linear__list_issues", "mcp__plugin_linear_linear__list_projects", "Read", "Glob", "Grep"]
argument-hint: [issue number]
---

## Objective

Decompose Linear issue `FOU-$ARGUMENTS` into a set of granular, dependency-ordered sub-issues that form a critical path from the current state of the codebase to the completed feature.

## Process

### 1. Gather Context

- Fetch the full details of `FOU-$ARGUMENTS` from Linear (include relations)
- Analyse the codebase to understand the current state relevant to this issue
- List all active Linear projects to understand where issues should be placed

### 2. Decompose

Break the issue into the smallest meaningful units of work. Each issue should be:

- **Independently deliverable** — can be completed, reviewed, and merged on its own
- **Single responsibility** — one clear outcome per issue
- **Well-scoped** — achievable in a focused session (hours, not days)

### 3. Classify Relationships

Apply consistent reasoning to distinguish between two relationship types:

**Child issues** (use `parentId`) when the work is:
- A direct sub-task that exists solely to accomplish part of the parent
- Meaningless without the parent issue's context
- Something that would naturally nest under the parent in a work breakdown

**Blocking issues** (use `blocks`/`blockedBy`) when the work is:
- A prerequisite that has independent value beyond the parent issue
- Infrastructure, refactoring, or setup that other work also depends on
- Something that must be completed first but isn't conceptually "part of" the parent

An issue can be both a child AND have blocking relationships with siblings.

### 4. Determine Project Placement

For each issue, select the most appropriate existing Linear project based on:
- The issue's domain (frontend, backend, infrastructure, etc.)
- Which project's scope best encompasses the work
- If no project fits well, omit the project field rather than forcing a bad fit

### 5. Build the Critical Path

Order the issues by dependency. The critical path should flow logically:
1. Foundation/infrastructure work first
2. Core implementation in the middle
3. Integration, polish, and verification last

### 6. Present the Plan

Before creating anything, present a summary table showing:
- Issue title
- Relationship type (child / blocker)
- Dependencies (what it blocks / is blocked by)
- Target project
- Priority (2=High, 3=Normal, 4=Low)

**Wait for approval before creating issues.**

### 7. Create Issues

Once approved, create all issues in dependency order (foundations first). For each issue:
- Assign to `me`
- Set the appropriate `parentId` for child issues
- Set `blocks`/`blockedBy` using the identifiers of previously created issues
- Set `project` if determined in step 4
- Set `priority` based on critical path position
- Write a clear description in markdown including:
  - What needs to be done
  - Acceptance criteria
  - Any relevant context about the current codebase state

### 8. Confirm

After all issues are created, provide a summary of what was created with their identifiers and a visual representation of the dependency graph.
