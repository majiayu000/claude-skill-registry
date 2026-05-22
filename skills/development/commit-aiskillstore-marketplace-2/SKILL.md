---
name: commit
description: Generate commit messages following project conventions for staged changes. Use when the user asks to commit changes or run /commit.
---

# Commit Message Generator

Generate commit messages following project conventions for staged changes.

## Instructions

When this skill is invoked:

1. Run `git diff --staged` to review the staged changes
2. Run `git status` to understand the overall state
3. Run `git log --oneline -10` to see recent commit style for context
4. Analyze what was changed and why
5. Generate a commit message following the format below
6. Present the commit message to the user for approval - **keep it concise, just show the message and ask for approval**
7. If approved, execute the commit

**Presentation Style**: Be direct and minimal. Present only the commit message and ask "Proceed with this commit message?" - no analysis, explanations, or bullet points unless the changes are complex or ambiguous.

## Commit Message Format

```
<type>: <short description>

[optional body with more detail]
```

### Types

- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring without behavior change
- `test` - Adding or updating tests
- `docs` - Documentation changes
- `style` - Formatting, whitespace (no code change)
- `chore` - Build, config, dependency updates

### Rules

1. **First line**: Must be under 72 characters
2. **Tense**: Present tense, imperative mood ("add" not "added" or "adds")
3. **Description**: Complete the sentence "This commit will..."
4. **Body**: Optional, use for explaining "why" not "what"
5. **NO AI attribution**: Never include "Generated with Claude Code" or "Co-Authored-By" lines

### Examples

```
feat: add auto-reveal toggle for estimation rounds

fix: prevent duplicate user connections to lobby

refactor: extract insight resolution logic to separate resolvers

test: add usecase tests for SetEstimateCommand handler

docs: update architecture documentation with processing groups

chore: upgrade Spring Boot to 3.4.12
```

## Analysis Guidelines

When analyzing changes, consider:

- **Module affected**: Which module (api, lobby, session, ui)?
- **Layer affected**: Domain, usecase, adapter, or API contract?
- **Intent**: What problem does this solve or capability does it add?
- **Scope**: Is this a single logical change or mixed concerns?

### Common Patterns to Recognize

**Backend Changes**:
- New Commands/Events/Queries in `api/` → `feat: add X command/event/query`
- Handler implementations → `feat: implement X handler` or `fix: correct X handler logic`
- Domain logic updates → `feat: add X behavior to aggregate` or `refactor: simplify X logic`
- Read model updates → `feat: update X view projection`
- Tests → `test: add tests for X`

**Frontend Changes**:
- New components → `feat: add X component`
- State management → `feat: implement X state handling`
- UI improvements → `feat: enhance X interface`
- Styling → `style: update X component styles`

**Mixed Changes**:
- If frontend + backend for same feature → `feat: add X feature` (describe full feature)
- If unrelated changes → Suggest splitting into multiple commits
