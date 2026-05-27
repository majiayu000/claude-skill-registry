---
name: do-issue
description: |

Triggers: github, automation, parallel, subagents, issue
  Fix GitHub issues using subagent-driven-development with parallel execution
  where appropriate.

  Triggers: fix issue, github issue, issue resolution, subagent development,
  parallel execution, issue workflow, gh issue, fix github

  Use when: addressing GitHub issues systematically, multiple related issues
  need fixing, tasks can be parallelized across subagents, quality gates needed
  between task batches

  DO NOT use when: single simple fix - just implement directly.
  DO NOT use when: issue needs clarification - comment first to clarify scope.

  Uses subagents for parallel execution with code review gates between batches.
category: workflow-automation
tags: [github, issues, subagents, parallel, automation]
dependencies:
  - superpowers:subagent-driven-development
  - superpowers:writing-plans
  - superpowers:test-driven-development
  - superpowers:requesting-code-review
  - superpowers:finishing-a-development-branch
tools:
  - gh (GitHub CLI)
  - Task (subagent dispatch)
usage_patterns:
  - issue-discovery
  - task-planning
  - parallel-execution
  - quality-gates
complexity: advanced
estimated_tokens: 2500
modules:
  - modules/issue-discovery.md
  - modules/task-planning.md
  - modules/parallel-execution.md
  - modules/quality-gates.md
  - modules/completion.md
  - modules/troubleshooting.md
---
## Table of Contents

- [Key Features](#key-features)
- [Workflow Overview](#workflow-overview)
- [Required TodoWrite Items](#required-todowrite-items)
- [GitHub CLI Commands](#github-cli-commands)
- [Configuration](#configuration)
- [Detailed Resources](#detailed-resources)


# Fix GitHub Issue(s)

Retrieves GitHub issue content and uses subagent-driven-development to systematically address requirements, executing tasks in parallel where dependencies allow.

## Key Features

- **Flexible Input**: Single issue number, GitHub URL, or space-delimited list
- **Parallel Execution**: Independent tasks run concurrently via subagents
- **Quality Gates**: Code review between task groups
- **Fresh Context**: Each subagent starts with clean context for focused work

## Workflow Overview

| Phase | Description | Module |
|-------|-------------|--------|
| 1. Discovery | Parse input, fetch issues, extract requirements | [issue-discovery](modules/issue-discovery.md) |
| 2. Planning | Analyze dependencies, create task breakdown | [task-planning](modules/task-planning.md) |
| 3. Execution | Dispatch parallel subagents for independent tasks | [parallel-execution](modules/parallel-execution.md) |
| 4. Quality | Code review gates between task batches | [quality-gates](modules/quality-gates.md) |
| 5-6. Completion | Sequential tasks, final review, issue updates | [completion](modules/completion.md) |

## Required TodoWrite Items

1. `do-issue:discovery-complete`
2. `do-issue:tasks-planned`
3. `do-issue:parallel-batch-complete`
4. `do-issue:review-passed`
5. `do-issue:sequential-complete`
6. `do-issue:issues-updated`

## GitHub CLI Commands

```bash
# Fetch issue details
gh issue view <number> --json title,body,labels,comments

# Add completion comment
gh issue comment <number> --body "message"

# Close issue
gh issue close <number> --comment "reason"
```
**Verification:** Run the command with `--help` flag to verify availability.

## Configuration

```yaml
fix_issue:
  parallel_execution: true
  max_parallel_subagents: 3
  review_between_batches: true
  auto_close_issues: false
  commit_per_task: true
```
**Verification:** Run the command with `--help` flag to verify availability.

## Detailed Resources

- **Phase 1**: See [modules/issue-discovery.md](modules/issue-discovery.md) for input parsing and requirement extraction
- **Phase 2**: See [modules/task-planning.md](modules/task-planning.md) for dependency analysis
- **Phase 3**: See [modules/parallel-execution.md](modules/parallel-execution.md) for subagent dispatch
- **Phase 4**: See [modules/quality-gates.md](modules/quality-gates.md) for review patterns
- **Phase 5-6**: See [modules/completion.md](modules/completion.md) for finalization
- **Errors**: See [modules/troubleshooting.md](modules/troubleshooting.md) for common issues
