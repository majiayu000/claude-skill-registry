---
name: git-status
description:
  Present the status of the git repository to the user. Use when the
  agent needs to display the status of the git repository to the user.
  The agent should not use this internally for its own needs.
---

# Present git status

**`GOAL`**: present the git status in a visually appealing and
consistent way.

**`WHEN`**: use when the agent needs to display the status of the
repository to the user.

**`NOTE`**: _The agent shouldn't use this internally for its own needs._

## Efficiency directives

- Batch operations on file groups, avoid individual file processing
- Use parallel execution when possible
- Target only relevant files
- Reduce token usage

## Task management

For complex tasks: use `todo` system to break down, plan, and optimize
workflow.

## Git directives

### For repository status

```bash
git status --porcelain=v2 --branch
```

## References

The following reference files serve as strict guidelines:

- **`references/git-status-codes.md`**: complete reference for parsing
  git status output
- **`references/git-status-presentation.md`**: git status presentation
  guidelines, examples, and templates

## Workflow

- Execute `git status` command
- Study `git-status-codes.md`
- Study `git-status-presentation.md`
- Present final status to user
- **`DONE`**
