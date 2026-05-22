---
name: using-jj
description: Use this skill for ANY task involving jj or jujutsu version control. ALWAYS trigger when the user mentions jj, jujutsu, revsets, change IDs, bookmarks, or oplog. Also trigger when the user wants to squash, split, or reorder commits in a stack, write a revset query, absorb fixup changes, undo or restore a previous operation, resolve conflicts after rebasing, recover from force-pushes, rewrite protected/immutable commits, view change evolution (evolog), or try parallel approaches. Trigger even if "jj" is not explicitly said — "changes" instead of "commits", "stack" instead of "branch", "absorb", "squash into the right commit", "undo my last operation", "conflict after rebase", or "compare approaches in parallel" are strong jj signals. This skill contains critical non-obvious rules (like always using -m flags) that prevent broken workflows.
---

# jj Workflow

## Philosophy

1. **Commits are cheap, descriptions are mandatory.** The working copy is always a commit. Never leave it as "(no description set)".
2. **Experiment freely, the oplog is your safety net.** Every mutation is recorded. `jj undo` and `jj op restore` make anything reversible.
3. **Conflicts are state, not emergencies.** jj stores conflicts in commits as structured data. Rebase succeeds even with conflicts. Resolve when ready.
4. **Change IDs are your handle on work.** Commit hashes change on rewrite; change IDs don't. Use change IDs to refer to work across rebases and squashes.
5. **Bookmarks exist for GitHub, not for you.** Work with anonymous changes. Add bookmarks only when you need to push.
6. **Keep the stack shallow.** Squash early. Don't let history grow 10 commits deep before curating.
7. **Use `absorb` over manual squash routing.** When fixing across a stack, let jj figure out where each hunk belongs.
8. **Colocated = invisible to the team.** Teammates see standard git. They don't know you use jj.

## CRITICAL: AI-Specific Rules

**Always use `-m` flag** to prevent jj from opening an editor:

```bash
# WRONG - opens editor, blocks AI
jj new
jj describe
jj commit
jj squash

# CORRECT - non-interactive
jj new -m "message"
jj describe -m "message"
jj commit -m "message"
jj squash -m "message"
```

**Never use these interactive commands** (no non-interactive mode):

- `jj split` / `jj split -i`
- `jj squash -i`
- `jj diffedit`

## Core Concepts

### Working Copy = Commit

There is no staging area. Every file edit is automatically tracked in `@` (the current change). No `git add` needed.

- `@` = your current change (working copy commit)
- `@-` = parent of current change
- `@--` = grandparent

### Change IDs vs Commit IDs

Every change has two identifiers:

- **Change ID** (e.g., `kpqxywon`) — stable across rewrites. Use this to refer to work.
- **Commit ID** (e.g., `a1b2c3d4`) — changes when content is rewritten.

When you squash, rebase, or amend, the change ID stays the same. This means you can bookmark a change ID mentally and it always resolves, unlike git commit hashes.

#### Accessing Previous Versions (`xyz/n` syntax)

Every rewrite of a change is recorded. Access previous versions with `<change-id>/n`:

- `xyz/0` — latest (current) version (same as `xyz`)
- `xyz/1` — previous version
- `xyz/2` — two versions ago

This is useful for restoring a change to its earlier state:

```bash
jj restore --from xyz/1 --to xyz    # Revert xyz to its previous contents
jj diff --from xyz/1 --to xyz      # See what changed between versions
```

### Conflicts Are Just State

When a rebase produces conflicts, jj records the conflict in the commit and succeeds. No "rebase in progress" blocking state. No `--continue` ceremony.

- Descendants of conflicted commits work normally
- Resolve conflicts whenever convenient — check out the commit, fix files, done
- `jj log` marks conflicted commits so you can spot them

## Workflows

### The Squash Workflow (Recommended)

```bash
jj describe -m "feat: what I'm building"   # State intent on current change
jj new -m "wip"                             # New empty change on top
# ... make changes ...
jj squash -m "feat: done"                   # Squash into parent
```

### The Commit Workflow (Simpler)

```bash
# ... make changes ...
jj commit -m "feat: what I did"             # Describe + create new change in one step
# ... keep working ...
```

`jj commit` is equivalent to `jj describe -m "..." && jj new`.

### The Edit Workflow (Mid-Stack Fixes)

Need to fix something in an older change? No stash/rebase-i dance:

```bash
jj edit <change-id>        # Switch working copy to that change
# ... make your fix ...
jj new -m "back to work"   # Return to tip (descendants auto-rebased)
```

All descendants of the edited change are automatically rebased.

### Parallel Experiments

```bash
jj new main -m "approach A"           # Branch from main
jj new main -m "approach B"           # Another branch from main (not from A)
jj diff --from <A-id> --to <B-id>    # Compare approaches
jj edit <winner-id>                   # Continue with the winner
jj abandon <loser-id>                 # Discard the loser
```

## Absorb: Smart Squash Routing

When you have a stack of changes and make fixes in `@`, `jj absorb` automatically distributes each hunk to the ancestor where those lines were last modified.

```bash
# You're at the top of a 3-commit stack, fixing bugs across all of them
jj absorb    # Each fix goes to the right commit automatically
```

Use `jj absorb` when fixing across a stack. Use `jj squash` when you know exactly where changes should go.

## Bookmarks & Pushing

Bookmarks are jj's equivalent of git branches, but they **don't auto-advance**. You must move them explicitly.

### Push to main

```bash
jj bookmark set master -r @-        # Point bookmark at your commit (not empty @)
jj git push
```

### Feature branches

```bash
# Create and push
jj bookmark create feature-x -r @-
jj git push

# Update after more work
jj bookmark set feature-x -r @-
jj git push
```

### Addressing PR feedback

```bash
jj new feature-x- -m "address review feedback"
# ... make changes ...
jj squash -m "feat: updated per review"
jj bookmark set feature-x -r @-
jj git push
```

## Revsets

Revsets are a functional language for selecting commits. Beyond `@` and `@-`:

| Expression            | Meaning                    |
| --------------------- | -------------------------- |
| `@`                   | Current working copy       |
| `@-`                  | Parent                     |
| `@--`                 | Grandparent                |
| `x+`                  | Children of x              |
| `x::`                 | All descendants of x       |
| `::x`                 | All ancestors of x         |
| `trunk()`             | The trunk/main commit      |
| `bookmarks()`         | All bookmarked commits     |
| `empty()`             | Empty commits              |
| `divergent()`         | Divergent changes          |
| `remote_tags()`       | Remote tags                |
| `diff_lines("text")`  | Commits with matching diff |
| `description("text")` | Filter by description      |
| `author("name")`      | Filter by author           |

Useful examples:

```bash
jj log -r 'trunk()..@'              # Everything between main and here
jj log -r '::@ & ~::trunk()'         # My branch only
jj log -r 'author("trevor")'         # My commits
```

## Syncing with Remote

```bash
jj git fetch                         # Pull from remote
jj rebase -d master@origin           # Rebase onto updated main
```

## Temporarily Disabling Immutable Commits

When you need to rewrite a commit protected by `immutable_heads()` (e.g., squashing into a remote bookmark):

```bash
# Disable protection (quote the key — parentheses are invalid TOML bare keys)
jj config set --repo 'revset-aliases."immutable_heads()"' 'none()'

# Do your rewrite
jj squash -m "updated message"

# ALWAYS restore protection immediately after
jj config set --repo 'revset-aliases."immutable_heads()"' 'builtin_immutable_heads() | remote_bookmarks()'
```

**Important:** The `NAME` argument requires shell quoting around the TOML key because `immutable_heads()` contains parentheses. Use single quotes around the full dotted key with inner double quotes: `'revset-aliases."immutable_heads()"'`.

**CRITICAL: Always ask the user before disabling immutable protection.** Rewriting remote bookmarks means force-pushing, which rewrites shared history. Confirm with the user before proceeding — never silently disable immutability.

## Recovery

The operation log records every mutation. Nothing is ever truly lost.

```bash
jj op log                            # See all operations
jj undo                              # Undo last operation
jj op restore <id>                   # Jump to any past state
jj evolog                            # See how current change evolved
jj evolog -r <change-id>             # See how any change evolved
```

## Recommended Config

User config lives at `~/.config/jj/config.toml`:

```toml
[remotes.origin]
auto-track-bookmarks = "*"

[revset-aliases]
# Prevent rewriting pushed commits
'immutable_heads()' = 'builtin_immutable_heads() | remote_bookmarks()'
# Shorthand for trunk
'trunk()' = 'master@origin'
```

## Bail Out

```bash
rm -rf .jj    # Delete jj state, keep git unchanged
```
