---
name: graphite-stacked-diffs
description: PROACTIVELY USED for Graphite stacked diffs workflow. Auto-invokes when user mentions "stacked diffs", "stacked PRs", "Graphite", or "gt". Ensures correct workflow for creating, managing, and submitting stacks of pull requests using Graphite CLI. Handles the complete lifecycle from creation to merge.
allowed-tools: Read, Bash, Edit, Grep, Glob, TodoWrite
---

# Graphite Stacked Diffs Skill

You are the **Graphite Workflow Expert**. You ensure correct usage of Graphite CLI for stacked pull requests, guiding users through the complete workflow while following best practices.

## When You Activate

### Automatic Triggers
- User mentions "stacked diffs", "stacked PRs", or "stack"
- User mentions "Graphite" or "gt" CLI commands
- User wants to create multiple related PRs
- User asks about breaking up large changes
- User needs to work on dependent features
- User mentions working on features while waiting for review

### Complexity Indicators
```
✅ Use Graphite stacking when:
- Large feature can be broken into smaller, reviewable chunks
- Multiple dependent changes that build on each other
- Want to stay unblocked while waiting for reviews
- Need to create logical progression of changes
- Working on feature that touches multiple areas

❌ Don't use stacking when:
- Single, simple change
- Independent changes (can be separate PRs)
- Hotfix or emergency patch (unless complex)
- Changes that can't be broken down logically
```

## Core Graphite Concepts

### What is a Stack?
A stack is **a sequence of pull requests**, each building off its parent. Stacks enable:
- Breaking large work into small, incremental changes
- Each PR can be tested, reviewed, and merged independently
- Stay unblocked by continuing work while waiting for reviews
- Easier code review with smaller, focused diffs

### The Graphite CLI (`gt`)
- Simplifies git commands (especially rebasing)
- Enables PR stacking as first-class concept
- Automatically handles upstack/downstack sync
- Integrates with GitHub for PR management

## Complete Graphite Workflow

### Phase 1: Initial Setup (First Time Only)

```bash
# Install Graphite CLI (if not installed)
npm install -g @withgraphite/graphite-cli@stable
# or
brew install --cask graphite

# Authenticate with Graphite
gt auth
# Follow the link to get token from: https://app.graphite.dev/activate

# Initialize Graphite in repository
gt init
# Select your trunk branch (usually 'main' or 'master')
```

### Phase 2: Creating Your First PR in a Stack

```bash
# 1. Start from trunk
gt checkout main

# 2. Make your changes
# ... edit files ...

# 3. Create branch and commit in one command
gt create --all \
  --message "feat(api): Add new API method for fetching users"

# Alternative: Use AI to generate branch name and message
gt create --all --ai

# 4. Submit to create PR
gt submit

# 5. If you need follow-up changes
# ... edit files ...
gt modify --all  # Amends the existing commit
gt submit        # Updates the PR
```

**Key Commands:**
- `gt create -am "message"` - Create branch + commit staged changes
- `gt modify -a` - Amend existing commit with new changes
- `gt submit` - Push and create/update PR

### Phase 3: Stacking Additional PRs

```bash
# While waiting for review on first PR, stack more work on top

# 1. Checkout the PR you want to stack on
gt checkout  # Interactive branch picker

# 2. Make new changes
# ... edit files ...

# 3. Create second PR stacked on first
gt create --all \
  --message "feat(frontend): Load and show list of users"

# 4. Submit the entire stack
gt submit --stack  # or: gt ss (alias)

# This creates a 2nd PR that depends on the 1st

# 5. Assign reviewers
gt submit --stack --reviewers alice,bob

# 6. Visualize your stack
gt log short  # or: gt ls
gt log long   # or: gt ll (shows commit graph)

# 7. Open PR in browser
gt pr  # Opens current branch's PR
```

**Key Commands:**
- `gt ss` - Submit entire stack (alias for `gt submit --stack`)
- `gt ls` - List stacks (alias for `gt log short`)
- `gt pr` - Open PR in browser

### Phase 4: Addressing Reviewer Feedback

When reviewer requests changes on ANY PR in the stack:

```bash
# 1. Checkout the branch that needs changes
gt checkout branch_name
# or use interactive selector
gt checkout

# 2. Make the requested changes
# ... edit files ...

# 3. OPTION A: Amend existing commit (recommended)
gt modify -a
# This:
# - Amends the commit
# - Automatically restacks all branches above it
# - Keeps history clean

# 4. OPTION B: Create new commit for feedback
gt modify -cam "Responded to reviewer feedback"
# This:
# - Creates new commit
# - Restacks all upstack branches
# - Keeps explicit record of changes

# 5. Submit updates
gt submit --stack

# 6. If updating existing PRs only (no new PRs)
gt submit --stack --update-only  # or: gt ss -u
```

**Key Concepts:**
- `gt modify` automatically restacks all upstack branches
- Changes propagate up the stack automatically
- No manual rebasing needed!

### Phase 5: Syncing with Trunk

As trunk (main) gets ahead of your stack:

```bash
# Sync everything
gt sync

# This will:
# 1. Pull latest changes into main
# 2. Restack all open PRs on top of new main
# 3. Prompt to delete merged/closed branches
# 4. Handle conflicts if any

# If conflicts occur, gt sync will prompt you to:
gt checkout conflicting_branch
gt restack  # Manually fix conflicts
```

**Best Practice:** Run `gt sync` frequently to stay up-to-date!

### Phase 6: Stack Navigation

Move around your stack efficiently:

```bash
# Move up/down one level
gt up    # or: gt u
gt down  # or: gt d

# Move up/down multiple levels
gt up 2
gt down 3

# Jump to top/bottom of stack
gt top     # or: gt t
gt bottom  # or: gt b

# Checkout specific branch interactively
gt checkout  # or: gt co

# See where you are
gt ls  # List all stacks
```

### Phase 7: Merging Your Stack

```bash
# Option 1: Merge via Graphite UI (recommended)
gt top        # Go to top of stack
gt pr         # Open in browser
# Click "Merge" button to merge entire stack

# Option 2: Merge via CLI
gt merge
# Merges all PRs from trunk to current branch

# Confirm before merging
gt merge --confirm

# Dry run (see what would be merged)
gt merge --dry-run

# After merging, clean up
gt sync  # Detects merged branches and prompts to delete them
```

### Phase 8: Cleanup

```bash
# After PRs are merged
gt sync  # Pulls main + prompts to delete merged branches

# Force sync (no prompts)
gt sync --force  # or: gt sync -f

# Sync all trunks
gt sync --all
```

## Advanced Workflows

### Splitting Large Changes

If you have a large uncommitted change to split into stack:

```bash
# Option 1: Split by hunk (interactive)
gt split --by-hunk  # or: gt split -h
# Interactively stage changes to create new branches

# Option 2: Split by commit
gt split --by-commit  # or: gt split -c
# Select split points between existing commits

# Option 3: Split by file
gt split --by-file "src/api/*.ts"  # or: gt split -f
# Extract matching files into parent branch
```

### Inserting a PR into Existing Stack

```bash
# Checkout where you want to insert
gt checkout middle_branch

# Create new branch inserted between current and child
gt create --insert --all -m "feat: inserted change"
# or: gt create -i -am "feat: inserted change"

# Select which child should be moved onto new branch
# (if multiple children exist)
```

### Reordering Stack

```bash
# Reorder branches between trunk and current
gt reorder

# Opens editor where you can reorder lines
# Each line represents a branch
# Save and close to apply new order
```

### Moving Branches

```bash
# Move current branch onto different parent
gt move --onto target_branch

# Move specific branch
gt move --source branch_to_move --onto new_parent
```

### Handling Conflicts

```bash
# If restack encounters conflicts
gt restack  # Will pause and ask you to resolve

# Resolve conflicts in editor, then:
git add .
gt continue  # Continue the restack

# Or abort
gt abort
```

### Working with Teammates' Stacks

```bash
# Get teammate's stack locally
gt get branch_name

# This fetches the stack from remote
# including all dependencies

# Clean up afterwards
gt delete branch_name  # Delete branches you don't need
```

## Command Reference Cheatsheet

### Essential Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `gt create -am "msg"` | `gt c -am` | Create branch + commit |
| `gt modify -a` | `gt m -a` | Amend commit + restack |
| `gt modify -cam "msg"` | `gt m -cam` | New commit + restack |
| `gt submit --stack` | `gt ss` | Submit entire stack |
| `gt submit --stack -u` | `gt ss -u` | Update existing PRs only |
| `gt log short` | `gt ls` | List stacks (minimized) |
| `gt log long` | `gt ll` | Show commit graph |
| `gt sync --force` | `gt sync -f` | Sync + auto-cleanup |

### Navigation

| Command | Alias | Description |
|---------|-------|-------------|
| `gt up [n]` | `gt u [n]` | Move up stack |
| `gt down [n]` | `gt d [n]` | Move down stack |
| `gt top` | `gt t` | Jump to top |
| `gt bottom` | `gt b` | Jump to bottom |
| `gt checkout` | `gt co` | Interactive branch picker |

### Stack Management

| Command | Description |
|---------|-------------|
| `gt restack` | Rebase current stack |
| `gt merge` | Merge PRs in stack |
| `gt undo` | Undo last gt command |
| `gt info` | Show branch info |
| `gt pr` | Open PR in browser |

## Best Practices

### 1. Commit Messages
```bash
# Use conventional commits
gt create -am "feat(scope): description"
gt create -am "fix(scope): description"
gt create -am "refactor(scope): description"

# Or let AI generate
gt create --all --ai
```

### 2. Stack Structure

**Good Stack:**
```
main
├─ feat(db): Add users table schema
   ├─ feat(api): Add user CRUD endpoints
      ├─ feat(api): Add auth middleware
         └─ feat(frontend): Add login page
```

Each PR is:
- Small and focused (< 400 lines ideally)
- Logically independent
- Can be reviewed separately
- Builds on previous functionality

**Bad Stack:**
```
main
├─ fix typo
   └─ Add entire authentication system (5000 lines)
```

### 3. Staying Synced

```bash
# Run frequently (daily or before new work)
gt sync

# Before submitting stack
gt sync
gt ss
```

### 4. Descriptive PRs

```bash
# Submit with reviewers
gt submit --stack --reviewers alice,bob

# Mark as draft initially
gt submit --draft

# Auto-merge when ready
gt submit --merge-when-ready
```

### 5. Clean History

```bash
# Prefer amending over new commits
gt modify -a  # Clean history

# Unless feedback needs tracking
gt modify -cam "Address review feedback"  # Explicit history
```

## Common Workflows

### Creating a Feature Stack

```bash
# 1. Start fresh from main
gt checkout main
gt sync

# 2. Create database changes
# ... edit schema ...
gt create -am "feat(db): Add users table schema"
gt submit

# 3. Stack API on top
# ... edit API files ...
gt create -am "feat(api): Add user CRUD endpoints"
gt submit --stack

# 4. Stack auth on top
# ... edit auth middleware ...
gt create -am "feat(api): Add authentication middleware"
gt submit --stack

# 5. Stack frontend on top
# ... edit frontend ...
gt create -am "feat(ui): Add user management UI"
gt submit --stack --reviewers alice,bob

# 6. View the stack
gt ls
```

### Responding to Multi-level Feedback

```bash
# Reviewer asks changes on 2nd PR (API)
gt checkout feat-api-branch

# Make changes
# ... edit ...
gt modify -a

# Automatically restacks auth and UI PRs above it!
gt submit --stack
```

### Emergency Fix in Stack

```bash
# Need to fix bug in bottom of stack

# 1. Checkout the branch
gt checkout bottom_branch

# 2. Fix the bug
# ... edit ...

# 3. Amend
gt modify -a

# 4. Everything upstack gets rebased automatically!
gt submit --stack
```

### Collaborating on Stack

```bash
# Get coworker's stack
gt get their-feature-branch

# Make changes and push
# ... edit ...
gt modify -cam "Add tests per review"
gt submit

# Coordinate: Let them know you pushed changes
```

## Troubleshooting

### "Branch has conflicts"

```bash
gt sync  # Will identify conflicting branches
gt checkout conflicting_branch
gt restack  # Manually resolve conflicts

# During rebase:
# ... fix conflicts in editor ...
git add .
gt continue
```

### "PR already exists"

```bash
# Just update it
gt submit --stack --update-only
# or
gt ss -u
```

### "Accidentally committed to wrong branch"

```bash
# Undo last Graphite command
gt undo

# Or manually move commits
gt move --onto correct_branch
```

### "Lost track of stack structure"

```bash
# Visualize
gt ls    # Simple view
gt ll    # Detailed commit graph
gt info  # Current branch details
```

### "Want to delete a branch mid-stack"

```bash
# Fold it into parent (combine changes)
gt fold

# Or delete and restack children onto parent
gt delete branch_name
# Children automatically rebase onto parent
```

## Integration with Droidz Framework

When using Graphite in Droidz orchestration:

### Creating Specs for Stacked Work

```bash
# 1. Create spec that describes the full feature
/create-spec feature user-management

# 2. In spec, break down into stackable tasks
# Each task becomes a PR in the stack

# 3. Validate spec
/validate-spec .factory/specs/active/user-management.md

# 4. Start implementing bottom-up
gt checkout main
gt create -am "feat(db): Users table schema"
# ... continue stacking ...
```

### Orchestrating Parallel Stacks

```bash
# Can create multiple independent stacks in parallel
# Each specialist agent can work on different stacks

# Stack 1 (API team)
gt create -am "feat(api): User endpoints"

# Stack 2 (Frontend team) - independent
gt checkout main  # Start from fresh main
gt create -am "feat(ui): Dashboard redesign"
```

### Documentation

Always save architectural decisions:
```bash
# After creating major stack
/save-decision architecture "Using Graphite for stacked PRs to enable faster iteration and better code review"
```

## Visual Stack Example

```
main (trunk)
│
├─ feat/users-table (PR #101) ✓ Approved
│  │
│  └─ feat/user-api (PR #102) 🔍 In Review
│     │
│     └─ feat/user-auth (PR #103) ⏳ Draft
│        │
│        └─ feat/user-ui (PR #104) ⏳ Draft

Commands to navigate:
- gt bottom → feat/users-table
- gt up 2 → feat/user-auth (from bottom)
- gt top → feat/user-ui
- gt down → feat/user-auth (from UI)
```

## When to Ask User

Always ask the user:
1. **Before creating large stacks** - "I can break this into 5 PRs in a stack. Proceed?"
2. **When conflicts occur** - "Branch X has conflicts. Need you to resolve manually."
3. **Before force operations** - "This will rewrite history. Continue?"
4. **When choosing between amend vs new commit** - "Amend existing commit or create new one for review feedback?"
5. **Before deleting branches** - "Okay to delete merged branches: X, Y, Z?"

## Key Principles

1. **Small, Focused PRs** - Each PR should do one thing well
2. **Logical Progression** - Stack should tell a story
3. **Stay Synced** - Run `gt sync` frequently
4. **Clean History** - Prefer amending over new commits when possible
5. **Communicate** - Keep reviewers informed about stack changes
6. **Restack Automatically** - Let `gt modify` handle rebasing
7. **Visualize Often** - Use `gt ls` to see stack structure

## Never

- ❌ Never use `git` commands for stacked work (use `gt` instead)
- ❌ Never manually rebase stacked branches (use `gt restack`)
- ❌ Never create PRs outside of Graphite CLI (breaks stack tracking)
- ❌ Never merge stack PRs out of order (breaks dependencies)
- ❌ Never force-push manually (use `gt submit` which handles it safely)
- ❌ Never forget to `gt sync` before starting new work
- ❌ Never create stacks for unrelated changes (use separate stacks)

## Success Indicators

You're using Graphite correctly when:
- ✅ Each PR in stack is < 400 lines
- ✅ Reviews happen faster (smaller diffs)
- ✅ You stay unblocked (continue work while waiting)
- ✅ No manual merge conflicts (gt handles rebasing)
- ✅ Clean, linear history
- ✅ Reviewers can review/approve independently
- ✅ PRs merge in sequence automatically

## Quick Reference

```bash
# Daily workflow
gt sync                    # Start of day
gt co                      # Pick work
# ... make changes ...
gt create -am "msg"        # Commit
gt ss                      # Submit stack
# ... reviewer feedback ...
gt co branch              # Checkout branch
gt m -a                   # Amend + restack
gt ss                      # Submit updates

# End of day
gt sync                    # Clean up merged branches
```

Remember: **Graphite is a complete workflow tool**, not just a CLI. Always use `gt` commands instead of raw `git` for stacked work to ensure proper stack tracking and automatic rebasing!
