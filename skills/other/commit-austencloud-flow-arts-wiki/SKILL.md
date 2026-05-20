---
description: Analyze changes and commit in logical chunks
allowed-tools: Bash(git *)
---

# Smart Commit

## Step 1: Analyze All Changes

!`git status`
!`git diff`
!`git diff --cached`

## Step 2: Plan Logical Commits

Group changes by these dimensions:
- **Feature work** vs **refactoring** vs **bug fixes**
- **Area/scope** (which part of the wiki? config, content, infra, skin, extensions?)
- **Content** vs **infrastructure**
- **Deps/config** vs **behavior changes**
- **Docs** vs **code**

If everything belongs together -> single commit.
If changes span multiple concerns -> plan multiple commits.

## Step 3: Present the Plan (CONCISE)

Show a **brief table** - one row per commit group:

| # | Message | Files |
|---|---------|-------|
| 1 | `fix(config): correct upload size limit in LocalSettings` | 1 file |
| 2 | `feat(content): add Poi article draft` | 2 files |

**Do NOT:**
- List every file individually
- Explain what each file does
- Provide detailed breakdowns
- Add commentary about the changes

Just: commit message + file count. User can ask for details if needed.

**Wait for confirmation before proceeding.**

## Step 4: Execute

For each planned commit:
1. Stage only the relevant files: `git add <files>`
2. For mixed files, use patch staging: `git add -p <file>`
3. Commit with the planned message
4. Verify with `git status`

After all commits, show `git log --oneline -n <count>` to confirm.

## Rules

- Never commit unrelated changes together
- If a commit can't be described in one line, it's too broad--split it
- Each commit should be independently meaningful
- Think: "Will this make sense when generating the changelog?"
