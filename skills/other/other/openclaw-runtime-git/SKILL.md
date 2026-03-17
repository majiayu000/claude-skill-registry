---
name: openclaw-runtime-git
description: Manage the openclaw-runtime git repository and its 13 agent workspace submodules. Use when adding a new agent workspace, cloning the runtime repo, updating submodule references, committing changes to the parent repo, or troubleshooting submodule state. Triggers on tasks involving workspace repos, submodule operations, agent onboarding git setup, or any git operations in ~/.openclaw/.
---

# openclaw-runtime-git

Git workflow patterns for the openclaw-runtime parent repo and its agent workspace submodules.

## Repo Structure

`~/.openclaw/` is the parent repo (`openclaw-runtime`). Each `workspace*/` directory is a git submodule pointing at its own GitHub repo under `delorenj/agent-oc-*`.

### Submodule Map

| Directory | GitHub Repo |
|---|---|
| `workspace/` | `delorenj/agent-oc-cack` |
| `workspace-cack-app/` | `delorenj/agent-oc-lala` |
| `workspace-dumpling/` | `delorenj/agent-oc-dumpling` |
| `workspace-eng/` | `delorenj/agent-oc-eng` |
| `workspace-grolf/` | `delorenj/agent-oc-grolf` |
| `workspace-infra/` | `delorenj/agent-oc-infra` |
| `workspace-lenoon/` | `delorenj/agent-oc-lenoon` |
| `workspace-overworld/` | `delorenj/agent-oc-pepe` |
| `workspace-rar/` | `delorenj/agent-oc-rar` |
| `workspace-rererere/` | `delorenj/agent-oc-rererere` |
| `workspace-svgme/` | `delorenj/agent-oc-momo` |
| `workspace-tonny/` | `delorenj/agent-oc-tonny` |
| `workspace-wean/` | `delorenj/agent-oc-tongy` |

## Hook Protection

A git hook guards workspace paths from accidental staging via `git add`. When adding or committing submodule references in the parent repo, use `command git` to bypass:

```bash
command git add workspace-<name>
command git commit -m "message"
```

This is safe and expected for submodule pointer commits. The hook exists to prevent accidentally staging workspace *contents* as tracked files in the parent repo.

## Common Workflows

### Clone the Runtime Repo (Fresh Machine)

```bash
git clone --recurse-submodules git@github.com:delorenj/<runtime-repo>.git ~/.openclaw
```

Or if already cloned without submodules:

```bash
cd ~/.openclaw
git submodule update --init --recursive
```

### Add a New Agent Workspace as a Submodule

1. Create the GitHub repo:
```bash
gh repo create delorenj/agent-oc-<name> --private
```

2. Initialize the workspace if it doesn't have a git repo yet:
```bash
cd ~/.openclaw/workspace-<name>
git init && git add -A && git commit -m "initial commit"
```

3. Add the remote and push:
```bash
gh repo create delorenj/agent-oc-<name> --private --source=~/.openclaw/workspace-<name> --push
```
Or if the repo already exists:
```bash
git remote add origin git@github.com:delorenj/agent-oc-<name>.git
git push -u origin main
```

4. Register as submodule in the parent repo:
```bash
cd ~/.openclaw
git submodule add git@github.com:delorenj/agent-oc-<name>.git workspace-<name>/
```
If the directory already exists with a `.git`, git will say "Adding existing repo" which is correct.

5. Commit in the parent:
```bash
command git add .gitmodules workspace-<name>
command git commit -m "feat: add workspace-<name> as submodule"
```

### Update a Submodule Reference (After Pushing Changes in a Workspace)

When you commit and push inside a workspace, the parent repo sees a dirty submodule pointer. To record the new commit:

```bash
cd ~/.openclaw
command git add workspace-<name>
command git commit -m "chore: update workspace-<name> submodule ref"
```

### Update All Submodules to Latest Remote

```bash
cd ~/.openclaw
git submodule update --remote --merge
```

Then commit any updated pointers:
```bash
command git add workspace*
command git commit -m "chore: update all workspace submodule refs"
```

### Check Submodule Status

```bash
git submodule status
# Or more detail:
git submodule foreach --quiet 'echo "$sm_path: $(git log --oneline -1)"'
```

### Remove a Submodule

```bash
git submodule deinit -f workspace-<name>
rm -rf .git/modules/workspace-<name>
git rm -f workspace-<name>
git commit -m "chore: remove workspace-<name> submodule"
```

## Naming Convention

- Workspace directory: `workspace-<suffix>/` (suffix matches agent id or is descriptive)
- GitHub repo: `delorenj/agent-oc-<persona-name>` (lowercase persona name)
- The main workspace (`workspace/`) is an exception with no suffix

## Gotchas

- **Never `git add -A` or `git add .` in the parent repo** without checking what you're staging. The hook guards against this, but be aware.
- **Submodules track a specific commit, not a branch.** After pushing changes inside a workspace, you must also update and commit the submodule pointer in the parent.
- **Detached HEAD in submodules** is normal after `git submodule update`. To work in a submodule, `cd` into it and `git switch main` first.
- **`.gitmodules` is the source of truth** for submodule URL mappings. If a remote URL changes, update it here and run `git submodule sync`.
