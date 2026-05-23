---
name: jj-merge-repos
description: Merges two separate Jujutsu (jj) repositories into one. Use when combining repos, rebasing one repo onto another, or recovering from diverged histories.
---

# Merging JJ Repositories

Guide for merging two separate Jujutsu repositories into a single unified repo.

## When to Use This Skill

- Combining two unrelated repositories into one
- Recovering from diverged histories (local vs remote rewrites)
- Splicing commit histories together
- Rebasing an entire repository onto another

## How It Works

All JJ repos share a common empty root commit. When you add a remote from another repo and fetch, you get two diverging chains from that root. You can then:

1. Delete one chain (if you just want the other repo's history)
2. Rebase one chain onto the other (splice them together)

## Quick Reference

### Add and Fetch Another Repository

```bash
# Add the other repo as a remote
jj git remote add other-repo <url-or-path>

# Fetch all commits from it
jj git fetch --remote other-repo
```

### View Both Histories

After fetching, you'll see two separate commit chains:

```bash
jj log
```

Both chains start from the shared empty root commit.

### Option 1: Keep Only One History

Delete the unwanted chain of commits:

```bash
# Abandon all commits from the old/unwanted branch
jj abandon <commit-range>
```

### Option 2: Splice Repositories Together

Rebase one repo's history onto the other:

```bash
# Move all commits from one chain atop the other
jj rebase --source <root-of-chain-to-move> --destination <tip-of-other-chain>
```

## Example: Recovering from Diverged Histories

When local and remote diverged due to history rewriting:

```bash
# Add the remote (source of truth)
jj git remote add origin <url>

# Fetch remote commits
jj git fetch

# You now have two chains from root
# Delete the local chain you don't want
jj abandon <local-commits>

# Or rebase local work onto remote
jj rebase --source <local-root> --destination <remote-tip>
```

## Example: Combining Two Unrelated Projects

```bash
# Start in repo A
cd repo-a

# Add repo B as a remote
jj git remote add repo-b /path/to/repo-b

# Fetch repo B's history
jj git fetch --remote repo-b

# Rebase repo B's commits onto repo A's main
jj rebase --source <repo-b-root> --destination main
```

## Caveats

- **Merge conflicts are likely** when combining unrelated repos with overlapping files
- Resolve conflicts during the rebase as needed
- Consider whether you actually want the combined history or just the files

## Tips

- Use `jj log --all` to see all commits including from other remotes
- The root commit (empty) is always shared between all chains
- `jj abandon` removes commits without affecting working copy
- After cleanup, run `jj git push` to update remotes if needed
