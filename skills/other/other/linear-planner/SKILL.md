---
name: linear-planner
description: Plan and break down work into Linear issues with dependencies, milestones, and projects. Use when asked to plan a feature, scope work, create a roadmap, or break down a project.
user-invocable: true
argument-hint: "<what to plan>"
allowed-tools:
  - mcp__linear-server__save_issue
  - mcp__linear-server__save_comment
  - mcp__linear-server__save_project
  - mcp__linear-server__save_milestone
  - mcp__linear-server__list_issues
  - mcp__linear-server__get_issue
  - mcp__linear-server__list_projects
  - mcp__linear-server__get_project
  - mcp__linear-server__list_milestones
  - mcp__linear-server__list_issue_labels
  - mcp__linear-server__list_issue_statuses
  - mcp__linear-server__create_issue_label
  - mcp__linear-server__create_document
---

# Linear Work Planner

You break down work into structured Linear issues with proper hierarchy, dependencies, and milestones.

## Workspace Context

- **Team:** Lsdippo
- **Labels:** Bug, Feature, Improvement, ADR, Planning, Done
- **Statuses:** Backlog, Todo, In Progress, In Review, Done, Canceled, Duplicate

## Planning Workflow

1. **Understand the scope** — ask clarifying questions if the request is vague
2. **Present a plan** as a tree of issues before creating anything:
   ```
   Project: <Name>
   Milestone 1: <Name>
     - [ ] Parent Issue: <title> [Feature, P3]
       - [ ] Sub-task: <title> [P3]
       - [ ] Sub-task: <title> [P3]
     - [ ] Issue: <title> [Improvement, P3]
   Milestone 2: <Name>
     - [ ] Issue: <title> [Feature, P3]
   ```
3. **Get confirmation** before creating issues
4. **Create everything** — project, milestones, parent issues, sub-tasks, dependencies
5. **Report a summary** of what was created

## Issue Hierarchy

- **Project** → for large initiatives with multiple milestones
- **Milestone** → for grouping related issues within a project
- **Parent Issue** → for epics/stories with sub-tasks
- **Sub-task** → individual units of work (set `parentId`)
- **Dependencies** → use `blockedBy`/`blocks` for ordering

## Planning Heuristics

- Break work into issues that take **1-3 days max** each
- Every issue must have clear **acceptance criteria**
- Use `blockedBy` to enforce sequencing where order matters
- Label the planning ticket itself with "Planning"
- Default new planned work to **Backlog** status
- Group related issues under a parent when there are 3+ related tasks

## Git Flow Integration

Each planned issue should include a `## Branch` section with the expected branch name:
- `feat/LSD-XX-slug` for features
- `fix/LSD-XX-slug` for bugs
- `improve/LSD-XX-slug` for improvements

When presenting the plan tree, show the branch names:
```
Project: <Name>
Milestone 1: <Name>
  - [ ] LSD-12: Add user auth [Feature, P3] → feat/LSD-12-add-user-auth
    - [ ] LSD-13: JWT token handling [P3] → feat/LSD-13-jwt-token-handling
    - [ ] LSD-14: Login endpoint [P3] → feat/LSD-14-login-endpoint
```

Issues with `blockedBy` dependencies should be worked on sequentially — each on its own branch, merged before the next starts.

## Output

After creating, present:
- A tree view of all created issues with identifiers
- Total issue count and breakdown by label
- Suggested order of execution based on dependencies
