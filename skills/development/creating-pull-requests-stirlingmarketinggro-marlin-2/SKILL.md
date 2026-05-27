---
name: creating-pull-requests
description: Use when creating a pull request or preparing changes for review. Ensures PR titles and descriptions accurately reflect ALL changes in the branch AND link to related GitHub issues. Prevents accidentally omitting files, changes, or issue references from PR descriptions.
---

# Creating Pull Requests

## Overview

This skill ensures pull requests are comprehensive, accurate, and useful for future reference. PRs should document the COMPLETE set of changes in a branch, not just what was remembered from the current conversation. PRs must also link to related GitHub issues - most PRs have an associated issue, and these links are critical for tracking work and understanding context.

## Critical Principles

1. **Trust git, not memory** - The git diff is the source of truth, not conversation history
2. **Every changed file matters** - Files are rarely changed by accident; all changes deserve documentation
3. **PRs are searchable documentation** - Titles and descriptions should contain keywords that help find this PR when debugging issues later
4. **Complete > Concise** - A thorough PR description is more valuable than a brief one
5. **Most PRs close an issue** - Actively search for related issues; don't assume none exist just because the user didn't mention one

## Mandatory Workflow

When creating a pull request, execute these steps IN ORDER. Do not skip steps.

### Step 1: Gather Complete Change Information

Run ALL of these commands to understand the full scope of changes:

```bash
# See all files that differ from the base branch
git diff --name-status $(git merge-base HEAD master)..HEAD

# See the full diff to understand what changed
git diff $(git merge-base HEAD master)..HEAD

# See all commits on this branch
git log --oneline $(git merge-base HEAD master)..HEAD

# Check for any uncommitted changes that should be included
git status
```

**IMPORTANT**: Read the FULL output of these commands. Do not skim or summarize prematurely.

### Step 2: Search for Related GitHub Issues

**Most PRs should close an issue.** Before creating the PR, actively search for related issues.

```bash
# Search all issues (open and closed) to find any related context
gh issue list --search "keyword1 keyword2" --state all

# Example: If fixing email notifications, try multiple keyword variations:
gh issue list --search "email notification" --state all
gh issue list --search "notification not sent" --state all
```

**Extract keywords from:**
- The branch name (e.g., `fix/email-notifications` → search "email notifications")
- Commit messages from Step 1
- The problem being solved (what would someone have reported?)

**If you find related issues:**
- Note ALL issue numbers that this PR addresses
- The PR description MUST include `Closes #XXX` or `Fixes #XXX` for each

**If no issues are found after searching:**
- ASK THE USER: "I searched for related issues but didn't find any. Is there a GitHub issue this PR should close?"
- Do NOT proceed without confirming - the user may know of an issue you missed

**Common rationalization to avoid:**
> "The user didn't mention an issue, so there probably isn't one"

This is wrong. Users often forget to mention issue numbers. Your job is to find them.

### Step 3: Categorize All Changes

Group every changed file into categories. Common categories include:
- Bug fixes
- New features
- Refactoring
- Configuration changes
- Dependency updates
- Test additions/changes
- Documentation

Every file from the diff MUST appear in at least one category.

### Step 4: Write a Comprehensive Title

The PR title should:
- Summarize the PRIMARY purpose of the changes
- Include keywords that would help find this PR later
- Be specific enough to distinguish from similar PRs

**Good**: `fix(router): prevent redirect loop for API routes`
**Bad**: `fix redirect issue`

### Step 5: Write the PR Description

The description MUST include:

#### Summary Section
- 2-5 bullet points covering the main changes
- Each major change category should have at least one bullet
- Reference specific files or components when helpful

#### Files Changed Section
List ALL changed files grouped by purpose. Example:
```
### Bug Fixes
- `src/router.ts` - Fixed redirect logic

### New Features
- `src/components/Feature.tsx` - Added new component

### Configuration
- `config/settings.json` - Updated default values
```

#### Test Plan Section
- How to verify the changes work
- Any manual testing steps required

### Step 6: Check Documentation for Needed Updates

**Before creating the PR, review all documentation that may need updating based on your changes.**

Run these commands to find documentation files in the repo:

```bash
# Find all README and documentation files
git ls-files '*.md' 'CLAUDE.md' 'AGENTS.md' '**/*.md'

# See which docs are near the files you changed
git diff --name-only $(git merge-base HEAD main)..HEAD | xargs -I{} dirname {} | sort -u | while read dir; do
  ls "$dir"/*.md "$dir"/README* 2>/dev/null
done
```

**For each documentation file found, check whether your changes require updates to:**

- **README files** - Do new features, config changes, or API changes need documenting?
- **CLAUDE.md / AGENTS.md** - Do new patterns, commands, or conventions need recording?
- **Inline docs** (e.g., `docs/`, `references/`) - Are there guides that reference changed behavior?
- **Skill files** (`.claude/skills/`) - Do any skills reference patterns or code you changed?
- **Config examples** - Do example configs (`.example`, `.sample`) need updating to reflect new options?
- **API documentation** - Do endpoint docs match the current request/response shape?

**What to look for in the diff vs docs:**

- New environment variables or config options → documented somewhere?
- Changed function signatures or API endpoints → docs still accurate?
- New commands or CLI flags → added to usage instructions?
- Renamed or moved files → links and references still valid?
- Changed behavior or defaults → docs describe current behavior?
- New dependencies or setup steps → installation/setup docs updated?

**If documentation updates are needed:**
1. Make the updates in the same PR (don't leave docs stale)
2. List doc updates in the PR description under a "Documentation" category
3. If unsure whether a doc change is needed, ASK THE USER

**Common rationalization to avoid:**
> "The docs are close enough" or "someone else will update the docs later"

Stale documentation is worse than no documentation. If your code changes make any doc inaccurate, fix it now.

### Step 7: Self-Review Checklist

Before creating the PR, verify:

- [ ] Every file from `git diff --name-status` is mentioned in the description
- [ ] The title contains searchable keywords related to the changes
- [ ] The description explains WHY changes were made, not just WHAT changed
- [ ] Any breaking changes or migration steps are clearly documented
- [ ] **Issue search completed** - You searched GitHub issues with relevant keywords
- [ ] **Issue linking resolved** - Either: (a) PR includes `Closes #XXX` for found issues, OR (b) You asked the user and confirmed no issue exists
- [ ] **Documentation checked** - You reviewed README files, CLAUDE.md, AGENTS.md, and other docs near changed files for anything that needs updating based on the diff

## Common Mistakes to Avoid

### Relying on Session Memory
**Wrong**: "I changed the router to fix redirects"
**Right**: Run `git diff` and document ALL changes, including ones from earlier in the session or previous sessions

### Omitting "Minor" Changes
**Wrong**: Leaving out config file changes because they seem unimportant
**Right**: Every changed file is documented - config changes often matter for deployment

### Vague Descriptions
**Wrong**: "Fixed some bugs and updated configs"
**Right**: Specific descriptions of what was fixed and why, with file references

### Forgetting Uncommitted Changes
**Wrong**: Creating PR with unstaged changes still pending
**Right**: Run `git status` first and decide if pending changes should be committed

### Assuming No Issue Exists
**Wrong**: "The user didn't mention an issue, so I'll just create the PR without one"
**Right**: Search GitHub for related issues using keywords from the branch name and commit messages. If nothing found, ask the user before proceeding.

### Treating Issue Links as Optional
**Wrong**: `Fixes #1234 (if there was an issue)` or skipping the search entirely
**Right**: Always search for issues. Most PRs have one. Include `Closes #XXX` for every related issue found.

## PR Description Template

Use this template structure:

```markdown
## Summary
- [Primary change/fix with context]
- [Secondary changes]
- [Any additional notable changes]

Closes #XXX

## Changes

### [Category 1]
- `path/to/file.ext` - Description of change

### [Category 2]
- `path/to/file.ext` - Description of change

## Test Plan
- [ ] Step to verify change 1
- [ ] Step to verify change 2

## Notes
[Any additional context, breaking changes, or follow-up work needed]
```

## Rationalizations That Mean You're About to Skip Issue Search

If you catch yourself thinking any of these, STOP. You are rationalizing skipping a required step.

| Excuse | Reality |
|--------|---------|
| "User didn't mention an issue" | Users forget. Search anyway. |
| "This seems like new work, not a fix" | New features often have tracking issues too. Search. |
| "I'll let the user add issue links" | Your job is to create a complete PR. Search. |
| "Searching would slow things down" | It takes 10 seconds. Do it. |
| "The PR description says 'if applicable'" | Issue search is NOT optional. Always search. |
| "I already know what the PR is about" | You might miss related issues. Search. |

**All of these mean: Run `gh issue list --search` before creating the PR.**

## Rationalizations That Mean You're About to Skip Documentation Review

| Excuse | Reality |
|--------|---------|
| "These are just code changes" | Code changes often affect documented behavior, commands, or patterns. Check. |
| "The docs are close enough" | Stale docs are worse than no docs. If anything is inaccurate, fix it now. |
| "Someone else will update the docs" | No they won't. You're already here with full context. Update them. |
| "It's just a small change" | Small changes to defaults, env vars, or flags are exactly what gets missed in docs. Check. |
| "The README doesn't cover this area" | Maybe it should now. Or maybe nearby docs do. Search. |

**All of these mean: Review docs near changed files and update anything that's now inaccurate.**
