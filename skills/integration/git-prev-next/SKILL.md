---
name: git-prev-next
description: Walk through git commit history using git prev/next for interactive editing. Use when you need to amend multiple commits in a stack (e.g., adding Differential Revision lines, fixing commit messages, or making small edits across a commit series).
---

# Git Prev/Next - Interactive Commit Stack Walker

## Overview

`git prev` and `git next` are custom scripts (in `~/.local/bin/`) that let you
walk backward and forward through a commit stack, pausing at each commit in an
editable state. Under the hood they manage an interactive rebase automatically.

This is simpler and safer than manually running `git rebase -i` when you need
to amend multiple commits in sequence.

## How It Works

- `git prev` — moves HEAD to the parent commit (goes backward in history).
  If not already in an interactive rebase, starts one automatically.
- `git next` — moves HEAD to the next commit (goes forward in history).
  Only works when already in an interactive rebase (started by `git prev`).
- Both accept an optional count argument: `git prev 3` moves back 3 commits.
- At each stop, HEAD is in "edit" mode — you can amend the commit, stage
  changes, or inspect it.
- When done, use `git rebase --continue` to finish replaying remaining commits.

## Requirements

- Working tree must be clean before using `git prev`.
- Does not support merge commits.
- Does not support non-interactive rebases (`.git/rebase-apply`).

## Common Workflows

### Amend a series of commit messages

For example, adding `Differential Revision:` lines to 5 commits:

```bash
# Start at the top of your stack
git log --oneline -5

# Walk to the bottom commit you want to edit (use count to skip multiple)
git prev 4        # go back 4 commits at once

# At each commit, amend the message using the temp file approach
git log -1 --format=%B > /tmp/commitmsg.txt
echo "" >> /tmp/commitmsg.txt
echo "Differential Revision: https://phabricator.intern.facebook.com/DXXXXXXX" >> /tmp/commitmsg.txt
git commit --amend -F /tmp/commitmsg.txt
rm /tmp/commitmsg.txt

# Move forward to next commit
git next

# Amend that one too (same temp file pattern)
git log -1 --format=%B > /tmp/commitmsg.txt
# ... edit /tmp/commitmsg.txt ...
git commit --amend -F /tmp/commitmsg.txt
rm /tmp/commitmsg.txt

# Repeat git next + amend for each commit, then finish
git rebase --continue
```

### Make code changes to an older commit

```bash
git prev 2                          # walk back 2 commits
# make your edits...
git add <files>
git commit --amend --no-edit        # fold changes into this commit
git next                            # move forward (may need conflict resolution)
git rebase --continue               # finish
```

## Important Notes

- **Run `git status` often** to remind yourself you're in a rebase. It's easy
  to forget, especially across tool calls or context switches. `git status`
  will show `interactive rebase in progress` when you're mid-walk.
- `git prev` uses `git reset --hard HEAD^` internally — ensure your work tree
  is clean before using it.
- `git next` calls `git rebase --continue` internally — conflicts may arise
  if your amendments change code that later commits touch.
- When you're done editing, you must `git rebase --continue` to replay any
  remaining commits. If you forget, you'll be left in a detached HEAD state
  with a `.git/rebase-merge` directory.
- The remaining commits to replay are listed in `.git/rebase-merge/git-rebase-todo`.
  This file shows what's queued but **do NOT edit it directly** — use `git prev`,
  `git next`, and `git rebase --continue` to control the flow.
- `git prev` from a non-rebase state starts a new interactive rebase on HEAD^.
  `git next` from a non-rebase state prints "At top" and exits.
