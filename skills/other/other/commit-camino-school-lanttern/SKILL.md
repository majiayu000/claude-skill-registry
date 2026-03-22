---
description: Craft a Conventional Commit message and create the commit
disable-model-invocation: true
---

## Context

- Staged files: !`git diff --cached --name-only`
- Staged diff: !`git diff --cached`
- Unstaged changes: !`git status --short`
- Recent commits (for style reference): !`git log --oneline -10`
- Current branch: !`git branch --show-current`

## Your task

You are an expert Git commit message architect. Analyze the staged changes above and create a commit following the guidelines below. If no files are staged, inform the user and stop.

### Conventional Commit format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation only
- `style`: formatting, whitespace (no logic change)
- `refactor`: neither fixes a bug nor adds a feature
- `perf`: performance improvement
- `test`: adding or correcting tests
- `build`: build system or dependency changes
- `ci`: CI configuration changes
- `chore`: other changes that don't modify src or test files

### Subject line rules

- Under 72 characters
- Imperative mood ("add" not "added" or "adds")
- No capital letter after the colon
- No period at the end
- Describe WHAT changed conceptually, not WHERE in the code

### Scope

- Use the module, component, or area affected (e.g., "auth", "contexts", "live")
- Omit if change spans multiple unrelated areas

### Body (optional)

- Explain WHY the change was made
- Describe non-obvious implications
- Wrap at 72 characters

### Footer (optional)

- Breaking changes: `BREAKING CHANGE: description`
- Do NOT add issue references (Closes/Fixes/Resolves #N) unless the
  user explicitly requests it when invoking the skill — these belong
  in the PR description, not commit messages

### Authorship

Always append these two lines at the end of the commit message (after a blank line if there's no other footer):

```
Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### Key principles

1. **Conceptual over literal**: describe behavior/functionality, not file names or line numbers
2. **Information density**: succinct but informative — every word adds value
3. **Future-focused**: write for the developer reading this in 6 months
4. **Project context**: this is a Phoenix/Elixir educational assessment app — use domain language (assessment, learning management, LiveView, contexts, schemas)
5. **Multi-file changes**: describe the unified goal, not each file's changes

### Workflow

1. If no staged files → inform the user and stop
2. Analyze the diff conceptually
3. Determine type and scope
4. Check for breaking changes
5. Craft the subject line (verify: ≤72 chars, imperative, no period)
6. Decide if body/footer adds value
7. Stage any unstaged files that belong to this commit if appropriate
8. Create the commit

Do not explain the commit message to the user — just stage and commit. Show only the git output confirming the commit was created.
