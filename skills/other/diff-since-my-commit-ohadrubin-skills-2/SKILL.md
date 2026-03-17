---
name: diff-since-my-commit
description: Show changes to a git branch since your last commit, filtered to only files you touched. Use when user asks to see what others changed on their branch, review changes since they last committed, or compare their work against upstream modifications. Triggers on requests like "what changed on my branch", "show me the diff since my commit", "what did others change to my files", or "review changes to my PR".
---

# Diff Since My Commit

Show changes to a git branch since your last commit, filtered to only the files you originally touched.

## Usage

```bash
scripts/diff_since_my_commit.sh <branch> [email1,email2,...]
```

**Examples:**
```bash
# Use default git config email
scripts/diff_since_my_commit.sh origin/feature-branch

# Specify multiple emails (if you commit with different emails)
scripts/diff_since_my_commit.sh origin/main "me@gmail.com,me@work.com"
```

## What It Does

1. Find your most recent commit on the specified branch
2. Identify files you touched in your commits
3. Show who else committed since your last commit
4. Generate a diff of only your files that were modified by others
5. Open the diff in browser using diff2html (side-by-side view)

## Requirements

- `git` - for diff generation
- `diff2html-cli` - for browser preview (`npm install -g diff2html-cli`)

## Output

The script displays:
- Your last commit on the branch
- Number of commits since yours
- Authors who made changes
- List of files you touched
- Opens filtered diff in browser
