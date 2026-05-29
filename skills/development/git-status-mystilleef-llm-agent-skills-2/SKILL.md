---
name: git-status
description:
  Present the status of the git repository to the user. Use to display
  the status of the repository after a successful git commit by the
  agent. The agent should not use this internally for its own needs.
---

# Present git status

**`GOAL`**: present the git status in a visually appealing and
consistent way.

**`WHEN`**: use after a successful git commit by the agent when it needs
to display the status of the repository to the user.

**`NOTE`**: _The agent shouldn't use this internally for its own needs._

## Efficiency directives

- Optimize all operations for token and context efficiency
- Batch operations on file groups, avoid individual file processing
- Use parallel execution when possible
- Target only relevant files
- Reduce token usage

## Git directives

### For repository status

```bash
git status --porcelain=v2 --branch
```

## References

The following reference file serves as a strict guideline:

- **`references/git-status-unified.md`**: unified reference for parsing
  git status output and presentation guidelines

## Workflow

**`IMPORTANT`**: _To avoid a recursive loop, **`DON'T`** invoke the
`git-status` skill here._

- Without using the `git-status` skill, get repository status
- Use the reference files templates to present final status to user
- **`DONE`**
