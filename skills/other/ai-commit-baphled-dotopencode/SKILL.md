---
name: ai-commit
description: Create properly attributed commits for AI-generated code
category: Git
---

# Skill: ai-commit

## What I do

I provide expertise in creating properly attributed commits for AI-generated code using the project's standard workflow. I ensure every commit is atomic, follows conventional commit formats, and includes mandatory co-authoring attribution.

## When to use me

- When creating new commits for code generated or modified by AI
- When you need to split changes into atomic, logical units
- When attributing work to both the human developer and the AI agent

## Core principles

1. **Atomic commits**: Each commit must represent a single, logical change. Do not bundle unrelated fixes or features together.
2. **Standard workflow**: Always write your commit message to a temporary file first, then use the project's make target for execution.
3. **Proper attribution**: Include the Co-authored-by trailer for the AI model used to maintain a clear audit trail.
4. **Conventional format**: Use clear types like feat, fix, docs, or refactor to categorise changes.

## Patterns & examples

**Workflow for a new commit:**
1. Stage your changes with `git add`.
2. Write the message to a file, for example `/tmp/commit.txt`.
3. Run `make ai-commit FILE=/tmp/commit.txt`.

**Example commit message in /tmp/commit.txt:**
```text
feat: add user authentication middleware

Implement JWT validation for all protected routes to ensure secure access.

Co-authored-by: Claude <claude@anthropic.com>
```

**Using fixup commits:**
For small corrections to a previous, unpushed commit, use `git commit --fixup=<hash>` to keep history clean before a final squash.

## Anti-patterns to avoid

- ❌ **Direct git commit**: Skipping the `make ai-commit` target loses consistent formatting and attribution.
- ❌ **Bloated commits**: Bundling multiple logical changes makes code reviews difficult and rollbacks risky.
- ❌ **Missing trailers**: Failing to include co-authoring information breaks the project's attribution rules.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Git/AI Commit.md`

## Related skills

- `git-master`: For advanced history search and planning
- `git-advanced`: For rebase and history management
- `clean-code`: To ensure the committed code meets quality standards
