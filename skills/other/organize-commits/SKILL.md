---
name: organize-commits
description: Organize staged changes into logical commits with conventional commit messages. Groups related changes and creates well-structured commit history.
---

# Organize Commits Skill

Analyzes staged and unstaged changes, groups them into logical commits, and creates well-structured commits.

## When to Use

Invoke with `/organize-commits` when you have multiple changes across files that should be split into separate, focused commits.

## Instructions

### 1. Analyze Current Changes

Run these commands to understand the working state:

```bash
git status
git diff --stat
git diff --staged --stat
```

### 2. Categorize Changes by Purpose

Group files into logical commits based on:

| Category | Prefix | Description |
|----------|--------|-------------|
| Feature | `feat` | New functionality |
| Fix | `fix` | Bug fixes |
| Refactor | `refactor` | Code restructuring without behavior change |
| Style | `style` | CSS, formatting, whitespace |
| Docs | `docs` | Documentation only |
| Chore | `chore` | Build, config, dependencies |
| Test | `test` | Adding or updating tests |
| Perf | `perf` | Performance improvements |

### 3. Identify Logical Groupings

Look for patterns:
- **Same component**: Files in same directory or same feature area
- **Same concern**: All CSS changes, all type changes, all API changes
- **Same ticket/feature**: Changes that implement one cohesive thing
- **Dependencies**: Changes that must go together to avoid breaking

### 4. Present Commit Plan

Show the user a proposed commit plan:

```
Proposed Commits:
================

Commit 1: feat(initiatives): add filter counts to list views
  - src/components/build/InitiativeListView.tsx
  - src/components/build/InitiativeListView.module.css
  - src/components/objectives/ObjectiveList.tsx
  - src/components/objectives/ObjectiveList.module.css

Commit 2: fix(import): add missing fields to import schema
  - app/api/projects/[id]/import/route.ts

Commit 3: refactor(plan): reorder tabs for better workflow
  - app/(protected)/plan/page.tsx

Commit 4: chore: remove unused components
  - (deleted) src/components/initiatives/InitiativeList.tsx
  - (deleted) src/components/initiatives/InitiativeList.module.css
  - (deleted) src/components/RoadmapPage.tsx
  - (deleted) src/components/RoadmapPage.module.css
```

Ask: "Does this grouping look right? Would you like to adjust any commits?"

### 5. Execute Commits

For each approved commit group:

```bash
# Reset staging area
git reset HEAD

# Stage files for this commit
git add <file1> <file2> ...

# Create commit with conventional commit message
git commit -m "$(cat <<'EOF'
type(scope): short description

- Bullet point details if needed
- Another detail

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 6. Handle Edge Cases

**Partial file changes**: If a file has changes for multiple commits:
- Use `git add -p <file>` to stage specific hunks
- Or ask user if the file should go with the most related commit

**Untracked files**: Group new files with their related changes or as a separate "add new component" commit.

**Deletions**: Group deletions as cleanup/chore commits unless they're part of a refactor.

## Commit Message Guidelines

- **First line**: `type(scope): imperative description` (max 72 chars)
- **Body**: Explain "why" not "what" (the diff shows what)
- **Scope**: Component or feature area (optional but helpful)

### Good Examples
```
feat(filters): add item counts to filter buttons
fix(import): include epics and userStories in schema
refactor(plan): reorder tabs to match planning workflow
chore: remove unused InitiativeList and RoadmapPage components
```

### Avoid
```
Updated files
Fixed stuff
WIP
Changes
```

### 7. Track Progress (Optional)

After all commits are created, ask the user:

```
All commits created successfully!

Would you like to track this progress in the changelog? (y/n)
```

If yes:
- Invoke `/track-progress` skill
- Pass the list of commits just created
- The track-progress skill will generate multi-level descriptions and create a changelog entry

This step is optional but recommended to keep the changelog in sync with development.

## Notes

- Prefer more smaller commits over fewer large commits
- Each commit should be atomic (builds and works on its own)
- Don't mix unrelated changes in one commit
- Cleanup/deletion commits are fine to batch together
- Use `/track-progress` to record completed work in the changelog
