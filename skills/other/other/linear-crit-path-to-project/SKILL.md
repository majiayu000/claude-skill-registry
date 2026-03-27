---
name: linear-crit-path-to-project
description: "{{ 𝛀𝛀𝛀 }} Decompose a Linear project into a critical path of granular issues"
model: opus
disable-model-invocation: true
allowed-tools: ["mcp__plugin_linear_linear__get_issue", "mcp__plugin_linear_linear__get_project", "mcp__plugin_linear_linear__save_issue", "mcp__plugin_linear_linear__list_issues", "mcp__plugin_linear_linear__list_projects", "Read", "Glob", "Grep"]
argument-hint: [project name or slug]
---

## Objective

Decompose Linear project `$ARGUMENTS` into a set of granular, dependency-ordered issues that form a critical path from the current state of the codebase to the project's stated goals.

## Process

### 1. Gather Context

- Fetch the full details of the project matching `$ARGUMENTS` from Linear (include milestones and resources)
- List existing issues already in this project to understand what's been planned and what gaps remain
- Analyse the codebase to understand the current state relevant to this project's goals
- List all active Linear projects to understand the wider landscape (some work may belong elsewhere)

### 2. Identify Gaps

Compare the project's description/goals against:
- What the codebase already has
- What issues already exist in the project

Only create issues for **work that isn't already captured**. Flag any existing issues that appear redundant or stale.

### 3. Decompose

Break the remaining work into the smallest meaningful units. Each issue should be:

- **Independently deliverable** — can be completed, reviewed, and merged on its own
- **Single responsibility** — one clear outcome per issue
- **Well-scoped** — achievable in a focused session (hours, not days)

### 4. Classify Relationships

Apply consistent reasoning to distinguish between relationship types:

**Blocking relationships** (use `blocks`/`blockedBy`) when:
- One issue is a prerequisite for another
- Infrastructure or setup work that must land before dependent work can begin
- A clear temporal dependency exists

**Related relationships** (use `relatedTo`) when:
- Issues touch the same area but don't strictly depend on each other
- Changes in one might affect the other but neither blocks progress

**Cross-project blockers**: If a prerequisite logically belongs in a different project, create it there instead and set up the blocking relationship across projects.

### 5. Determine Placement

Most issues will belong to the target project. However, for each issue consider:
- Does this work serve the project's goals specifically, or is it broader infrastructure?
- If broader: place it in the more appropriate project and link it as a blocker
- If project-specific: place it in the target project

### 6. Build the Critical Path

Order the issues by dependency. The critical path should flow logically:
1. Foundation/infrastructure work first
2. Core implementation in the middle
3. Integration, polish, and verification last

Account for existing issues — new issues should slot into the dependency chain alongside them where appropriate.

### 7. Present the Plan

Before creating anything, present:

**Existing issues** (already in the project):
- Which ones are still relevant
- Any that appear stale or redundant
- Where new issues connect to them in the dependency chain

**New issues to create** — a summary table showing:
- Issue title
- Target project (most will be the target project; some may be elsewhere)
- Dependencies (blocks / blocked by, including existing issue identifiers)
- Priority (2=High, 3=Normal, 4=Low)

**Wait for approval before creating issues.**

### 8. Create Issues

Once approved, create all issues in dependency order (foundations first). For each issue:
- Assign to `me`
- Set `project` to the determined project
- Set `blocks`/`blockedBy` using identifiers of both new and existing issues
- Set `priority` based on critical path position
- Write a clear description in markdown including:
  - What needs to be done
  - Acceptance criteria
  - Any relevant context about the current codebase state

### 9. Confirm

After all issues are created, provide a summary of what was created with their identifiers and a visual representation of the full dependency graph (including existing issues).
