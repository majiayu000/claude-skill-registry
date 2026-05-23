---
name: scope
description: Use this to turn a design into a set of small, atomic, achievable tasks that are ready for execution
---

Your goal is to take a design or plan file and to scope a list of tasks that a team of agents or developers can follow to implement the design.

You should be provided with the path to a design or plan file. If you're not sure where the design is you may ask the user.

**CRITICAL** DO NOT modify any code or attempt to make changes during the scoping process.

## Required Information

Before starting, ask the user for:
1. **GitHub repository** - The repo where issues will be created (e.g., `owner/repo`). Ask: "What is the GitHub repository for this work?"

## Process

At the end of scoping you should:
1. Create GitHub milestones for each logical grouping (typically per PR)
2. Create GitHub issues for each task, assigned to the appropriate milestone
3. Create (or update) a ./designs/solution-name/SCOPES.yml file with the outcome of the scoping process

DO look up referenced GitHub issues and repos, find and read relevant files in the current project and use the WebSearch tool to check your work and update your understanding

Read the design file, it should be complete and answer most questions. Identify task boundaries for implementing the design. For some designs it may be only one task, often a design will require multiple tasks. Remember that the design file may be categorized topically not by task, your job is to find the commonalities and dependencies in the design and identify units of work.

A task should be atomic, complete and achievable. A developer or agent should be able to pick up an individual task and carry it to completion quickly and without requiring external feedback.

- **Atomic**: A task focuses on a single, indivisible unit of work that cannot be meaningfully broken down further. It has one clear purpose and produces one discrete outcome. If a task requires multiple distinct changes across unrelated parts of the system, it should be split into separate tasks.

- **Complete**: A task is self-contained with all necessary context, requirements, and acceptance criteria included. The task description should provide enough information that someone unfamiliar with the broader project can understand what needs to be done and why. All dependencies on other tasks should be explicitly identified.

- **Achievable**: A task can be completed in a reasonable timeframe (typically a few hours) with the available tools, knowledge, and resources. It should not require major architectural decisions, extensive research, or waiting on external factors. The scope is small enough that a developer can hold the entire context in their head while implementing it.

## Testing Approach

All tasks are developed using **Test-Driven Development (TDD)**. Do NOT create separate tasks for writing unit tests. Tests are written as part of each implementation task. Only create separate testing tasks for integration tests that span multiple components or require special setup (e.g., in-memory database, external API mocking across the full system).

## Branching and PR Strategy

Once you've identified all the tasks you also need to decide how to best divide the project into branches or PRs.

**Branch naming**: All branches must be prefixed with the GitHub issue number (e.g., `123-feature-name`).

**PR boundaries**: Consider separating work into logical PR boundaries:
- **Additive PRs first**: New code (types, classes, modules) that doesn't change existing behavior can be merged independently and reviewed in isolation.
- **Integration PRs second**: Wiring up new code to existing handlers/entry points should be a separate PR. This makes rollback easier and review clearer.
- **Small unrelated changes**: If there are multiple small unrelated changes that all carry low risk of issues or regression then these can be combined into one branch. If all tasks for the project meet this criteria there may be only one branch for the whole project.

**PR dependencies**: Never assume a previous PR has been merged when planning subsequent work. If a task depends on work from a previous PR:
- The previous PR's branch **must** be set as the `base` branch for the dependent task, OR
- The tasks should be combined into a single PR if the complexity allows

This ensures developers can work on dependent tasks immediately without waiting for PR reviews/merges.

**Remember** PRs should also be reasonably sized and focused so strike a balance between giving every task its own branch vs putting the whole scope of work in a single PR.

## GitHub Milestone & Issue Creation

### Creating Milestones

Group related tasks into milestones (typically one milestone per PR). Use the GitHub API to create milestones:

```bash
gh api repos/{owner}/{repo}/milestones -f title="1. Milestone Name" -f description="Description of this milestone" -f state="open"
```

### Creating Issues

For each task, create a GitHub issue assigned to its milestone:

```bash
gh issue create --repo {owner}/{repo} \
  --title "Task title" \
  --body "Task description with acceptance criteria" \
  --milestone "1. Milestone Name" \
  --label "enhancement"
```

The issue body should include:
- **Description**: What needs to be done
- **Acceptance Criteria**: Checklist of requirements
- **Dependencies**: Links to blocking issues (if any)

### Workflow

1. First, create all milestones
2. Then, create issues for each task, assigning them to the appropriate milestone
3. Record the issue numbers in SCOPES.yml

## SCOPES.yml Format

When you've identified all the tasks, created the GitHub milestones/issues, and determined the branching strategy, create a SCOPES.yml file:

```yaml
project: project name
repo: owner/repo
design_file: path/to/DESIGN.md
scoping_date: 2026-01-01

milestones:
  - number: 1
    title: "1. Milestone Name"
    description: What this milestone accomplishes
    branch:
      working: milestone-branch-name
      base: main

tasks:
  - id: 1
    github_issue: 123  # The GitHub issue number created for this task
    milestone: 1  # References milestones[].number
    title: one sentence description of the task
    description: |
      Task description with all necessary details in MD format
    acceptance_criteria: # at least one, can be more
      - behaviors and must-have implementation details
    depends_on: []  # list of task ids, may be empty
    effort: 1  # 1 = low, 5 = high
    status: scoped  # MUST be exactly "scoped" at this point
```

If a task has an effort over 3 or an acceptance criteria with more than 4 items in it confirm that it is truly atomic. It may be possible to break it down further unless doing so would impact its completeness.

When defining tasks it is not necessary to provide implementation details or code samples but you may choose to do so if it makes the description easier to understand.
