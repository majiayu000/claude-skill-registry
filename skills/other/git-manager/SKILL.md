---
name: git-manager
description: This skill should be used when the user mentions "git", "branch", "commit", "merge", "pull request", "PR", "version control", discusses branching strategy, commit conventions, collaboration workflows, or needs help with git operations. Addresses git best practices, branch management, commit messages, and LazyGit integration.
version: 1.0.0
---

# Git Workflow Patterns

Comprehensive git workflow guidance covering branch management, commit conventions, pull request best practices, conflict resolution, and LazyGit integration. Emphasizes clean history, collaboration patterns, and the user's established branch naming conventions.

---

## When This Skill Applies

Use this skill when:
- Creating or managing branches
- Writing commit messages
- Preparing pull requests
- Resolving merge conflicts
- Reviewing code changes
- Collaborating with team
- Questions about git best practices
- Using LazyGit for version control

---

## Branch Naming Strategy

### Standard Prefixes

**Core Development**:
- `feat/` - New features (user-facing or API)
- `enhance/` - Improvements to existing features (not bugs)
- `fix/` - Bug fixes
- `hotfix/` - Critical production fixes

**Code Quality**:
- `refactor/` - Code restructuring (no behaviour change)
- `types/` - Type definitions (interfaces, types, contracts)
- `perf/` - Performance improvements
- `test/` - Adding/updating tests
- `debug/` - Debugging/investigation branches (temporary)

**Documentation & Content**:
- `docs/` - Documentation changes
- `content/` - Content updates (copy, text, data files)

**Styling & UI**:
- `styles/` - Visual styling (colors, fonts, spacing)
- `layout/` - Structural positioning (grid, flexbox, responsive)
- `a11y/` - Accessibility improvements

**Dependencies & Configuration**:
- `deps/` - Dependency updates
- `build/` - Build system, bundler, tooling
- `config/` - Configuration files (non-Claude)
- `agents/` - Claude Code configuration
- `chore/` - Maintenance tasks (cleanup, file moves)

**CI/CD & DevOps**:
- `ci/` - CI/CD pipeline changes
- `deploy/` - Deployment-specific changes

**Experimental**:
- `spike/` - Research/proof-of-concept (not intended for merge)
- `experiment/` - Experimental features (may be discarded)
- `wip/` - Work in progress (explicit "not ready" signal)

### Naming Conventions

**Structure**: `<prefix>/<short-description>`

**Rules**:
- All lowercase
- Hyphens between words (no underscores or spaces)
- Imperative mood: `add-feature`, not `adds-feature` or `adding-feature`
- Descriptive but concise: `feat/calculate-user-stats` not `feat/stats`
- No ticket numbers

### Good Examples
```
feat/add-user-dashboard
feat/implement-search
enhance/improve-search-speed
enhance/add-sorting-options
fix/correctly-render-button
fix/handle-null-user
hotfix/patch-security-vulnerability
hotfix/restore-payment-flow
refactor/extract-auth-logic
refactor/simplify-validation
types/add-api-response-types
types/define-user-interfaces
perf/optimize-graph-rendering
perf/lazy-load-images
styles/update-button-colors
layout/make-nav-responsive
docs/add-api-examples
test/add-e2e-tests
deps/upgrade-svelte-5
config/update-prettier-rules
agents/add-roadmap-workflow
chore/remove-deprecated-code
spike/investigate-neo4j
```

### Bad Examples
```
feature/new-stuff              # Vague, use feat/ not feature/
fix-button                     # Missing prefix separator
FIX/button-bug                 # Uppercase (should be lowercase)
feat/adding-dashboard          # Not imperative (should be "add")
fix/bug                        # Not descriptive enough
refactor/fix-login             # Wrong prefix (it's a fix, not refactor)
feat/user_dashboard            # Underscores (should be hyphens)
```

### Breaking Changes

For breaking changes, prefix the description with `breaking-`:
```
feat/breaking-api-redesign
refactor/breaking-rename-core-types
enhance/breaking-change-auth-flow
```

**Why prefix not suffix**:
- Branch type stays in consistent position
- Easy to scan in branch lists
- Easy to grep: `git branch | grep breaking`
- Breaking nature still prominent (first word after `/`)

### Decision Tree

When creating a new branch, ask these questions in order:

1. **Does it add NEW functionality?** → `feat/`
2. **Does it fix something BROKEN?** → `fix/` (or `hotfix/` if critical)
3. **Does it IMPROVE existing functionality (not broken)?** → `enhance/`
4. **Does it restructure code WITHOUT changing behaviour?** → `refactor/`
5. **Is it ONLY type definitions (interfaces, types)?** → `types/`
6. **Does it improve PERFORMANCE?** → `perf/`
7. **Is it STYLING changes (colors, fonts, spacing)?** → `styles/`
8. **Is it LAYOUT changes (positioning, grid, responsive)?** → `layout/`
9. **Is it DOCUMENTATION?** → `docs/`
10. **Is it TESTING?** → `test/`
11. **Is it dependency/config/build?** → `deps/`, `config/`, `build/`, `agents/`
12. **Is it CI/CD related?** → `ci/` or `deploy/`
13. **Is it research/experimental?** → `spike/` or `experiment/`
14. **Is it just maintenance/cleanup?** → `chore/`
15. **Still unsure?** → Use the PRIMARY purpose of the branch

### Common Scenarios

**Styles vs Layout**:

Use `styles/` for:
- Colors, fonts, typography
- Spacing, padding, margins
- Borders, shadows, visual effects
- Theme variables
- CSS properties that don't affect structure

Use `layout/` for:
- Grid/flexbox structure
- Responsive breakpoints
- Component positioning
- Page structure
- Display/position properties

**Multiple Changes in One Branch**:
Use the prefix for the PRIMARY purpose.

Examples:
- Adding a feature that requires refactoring → `feat/add-user-dashboard`
- Fixing a bug that requires tests → `fix/handle-null-user`
- Enhancing feature with performance improvements → `enhance/improve-search-speed`

---

## Commit Message Conventions

### Standard Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**: Same as branch prefixes (feat, fix, docs, etc.)
**Scope**: Component/module affected (optional)
**Subject**: Brief description (50 chars max)
**Body**: Detailed explanation (optional, wrap at 72 chars)
**Footer**: Breaking changes, issue references (optional)

### Examples

**Simple commit**:
```
fix(auth): prevent token expiration race condition
```

**With body**:
```
feat(dashboard): add real-time activity feed

Implements WebSocket connection to stream user activities.
Includes reconnection logic and offline handling.
```

**With footer**:
```
fix(api): correct user data validation

BREAKING CHANGE: email field now required in user creation

Closes #123
Fixes #456
```

### Commit Message Guidelines

**Subject line rules**:
- Start with lowercase
- No period at end
- Imperative mood ("add" not "added" or "adds")
- Max 50 characters

**Good subjects**:
```
fix(login): handle empty password field
feat(search): add fuzzy matching
refactor(db): extract connection pool logic
docs(readme): update installation steps
```

**Bad subjects**:
```
Fixed bug
Updated stuff
Changes to the user service
WIP - still working on this
```

**Body rules**:
- Explain *what* and *why*, not *how*
- Wrap at 72 characters
- Separate from subject with blank line

**Good body**:
```
feat(export): add CSV export functionality

Users can now export their data as CSV files. This addresses
frequent requests from enterprise customers who need to import
data into their analytics tools.

The implementation uses streaming to handle large datasets
without memory issues.
```

### Atomic Commits

**One logical change per commit**:

**Good** (atomic):
```
1. feat(user): add user profile endpoint
2. test(user): add profile endpoint tests
3. docs(api): document profile endpoint
```

**Bad** (mixed concerns):
```
1. feat(user): add profile endpoint, fix login bug, update dependencies
```

### Commit Frequency

**Commit often, push strategically**:
```bash
# Local development: Commit frequently
git commit -m "feat(auth): add basic login form"
git commit -m "feat(auth): add form validation"
git commit -m "feat(auth): connect to API"
git commit -m "test(auth): add login tests"

# Before pushing: Consider squashing if appropriate
git rebase -i HEAD~4  # Interactive squash if needed

# Push clean history
git push origin feat/add-user-authentication
```

---

## Branch Lifecycle

### Creating Branches

**From main/master**:
```bash
# Update main first
git checkout main
git pull origin main

# Create and checkout new branch
git checkout -b feat/add-user-dashboard

# Or in one command
git checkout -b feat/add-user-dashboard origin/main
```

**Branch from another branch**:
```bash
# When feature depends on another feature
git checkout feat/base-feature
git checkout -b feat/add-dependent-feature
```

### Keeping Branches Updated

**Rebase on main** (preferred for clean history):
```bash
# Update main
git checkout main
git pull origin main

# Rebase feature branch
git checkout feat/add-user-dashboard
git rebase main

# If conflicts, resolve and continue
git add .
git rebase --continue

# Force push (rewrites history)
git push --force-with-lease origin feat/add-user-dashboard
```

**Merge main** (preserves branch history):
```bash
git checkout feat/add-user-dashboard
git merge main

# Resolve conflicts if any
git add .
git commit
git push origin feat/add-user-dashboard
```

**When to rebase vs merge**:
- **Rebase**: Feature branches, personal branches, clean history desired
- **Merge**: Shared branches, preserving collaboration history, release branches

### Cleaning Up Branches

**Delete local branch**:
```bash
# After merge
git branch -d feat/add-user-dashboard

# Force delete (if not merged)
git branch -D experiment/test-failed-approach
```

**Delete remote branch**:
```bash
git push origin --delete feat/add-user-dashboard
```

**Prune deleted remote branches**:
```bash
git fetch --prune
```

---

## Pull Request Best Practices

### Before Creating PR

**Checklist**:
- [ ] All tests passing
- [ ] Code follows style guide
- [ ] No console.logs or debugging code
- [ ] Branch rebased on latest main
- [ ] Commit messages follow convention
- [ ] Self-review completed

### PR Title and Description

**Title format**:
- Title case
- Brief and descriptive
- Understandable to non-devs — no jargon, ticket numbers, or type prefixes

**Examples**:
```
Add User Authentication System
Fix Login Button Crash on Mobile
Refactor Database Connection Logic
Update API Documentation
```

**Description template**:
```markdown
## What
Brief description of what this PR does.

## Why
Why this change is needed.

## How
High-level explanation of approach.

## Testing
How to test these changes.

## Screenshots (if applicable)
Visual changes shown here.

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Reviewed own code
```

### PR Size Guidelines

**Ideal PR size**: 200-400 lines changed

**Too large** (>500 lines):
- Hard to review
- Increases merge conflicts
- Higher bug risk
- Consider splitting

**Split large PRs**:
```
Instead of:
- feat/implement-complete-dashboard (1500 lines)

Split into:
- feat/add-dashboard-layout (300 lines)
- feat/add-dashboard-charts (250 lines)
- feat/add-dashboard-filters (200 lines)
- test/add-dashboard-integration (150 lines)
```

### Code Review

**As author**:
- Respond to all comments
- Don't take feedback personally
- Explain reasoning when disagreeing
- Mark conversations resolved
- Request re-review after changes

**As reviewer**:
- Be constructive and specific
- Ask questions rather than demand changes
- Acknowledge good work
- Distinguish: must-fix vs nice-to-have
- Review within 24 hours if possible

---

## Merge Strategies

### Merge Commit (Default)

**When to use**: Preserving complete branch history
```bash
git checkout main
git merge --no-ff feat/add-user-dashboard
```

**Pros**:
- Complete history preserved
- Easy to revert entire feature
- Clear feature boundaries

**Cons**:
- Many merge commits clutter history
- Harder to read linear history

### Squash and Merge

**When to use**: Cleaning up messy branch history
```bash
git checkout main
git merge --squash feat/add-user-dashboard
git commit -m "feat(dashboard): add user dashboard system"
```

**Pros**:
- Clean, linear history
- Single commit per feature
- Easy to read git log

**Cons**:
- Loses granular history
- Harder to revert partial work

### Rebase and Merge

**When to use**: Clean history with atomic commits
```bash
git checkout feat/add-user-dashboard
git rebase main
git checkout main
git merge --ff-only feat/add-user-dashboard
```

**Pros**:
- Linear history
- Preserves atomic commits
- No merge commits

**Cons**:
- Rewrites history (don't do on shared branches)
- More complex workflow

---

## Conflict Resolution

### Understanding Conflicts

**Conflict markers**:
```
<<<<<<< HEAD
// Current branch code
const user = getCurrentUser();
=======
// Incoming branch code
const user = fetchUser();
>>>>>>> feat/add-user-dashboard
```

### Resolution Strategies

**Manual resolution**:
```bash
# See conflicted files
git status

# Edit files to resolve conflicts
# Remove markers, keep correct code

# Stage resolved files
git add conflicted-file.ts

# Continue operation
git rebase --continue
# or
git merge --continue
```

**Choose theirs/ours**:
```bash
# Keep incoming changes (theirs)
git checkout --theirs conflicted-file.ts

# Keep current changes (ours)
git checkout --ours conflicted-file.ts

# Then continue
git add conflicted-file.ts
git rebase --continue
```

### Preventing Conflicts

**Strategies**:
- Keep branches short-lived
- Rebase frequently on main
- Coordinate with team on shared files
- Small, focused changes
- Clear code ownership

---

## LazyGit Integration

### Common LazyGit Workflows

**Starting LazyGit**:
```bash
# From project root
lazygit

# Or use alias: lg
lg
```

### LazyGit Key Bindings

**Status panel**:
- `space` - Stage/unstage file
- `a` - Stage all
- `c` - Commit
- `P` - Push
- `p` - Pull

**Branches panel**:
- `space` - Checkout branch
- `n` - New branch
- `d` - Delete branch
- `r` - Rebase
- `M` - Merge

**Commits panel**:
- `s` - Squash commit
- `r` - Reword commit
- `e` - Edit commit
- `d` - Delete commit
- `R` - Revert commit

**Files panel**:
- `space` - Stage changes
- `d` - Discard changes
- `e` - Edit file
- `o` - Open file
- `s` - Stash changes

### LazyGit Best Practices

**Staging workflow**:
```
1. Review changes in Files panel
2. Use arrow keys to navigate
3. Press 'space' to stage individual files
4. Or press 'a' to stage all
5. Press 'c' to commit
6. Write commit message
7. Press 'P' to push
```

**Interactive rebase**:
```
1. Go to Commits panel
2. Navigate to commits
3. Press 'e' to edit/reorder
4. Press 's' to squash
5. Press 'r' to reword
6. Push with force-with-lease
```

**Conflict resolution**:
```
1. LazyGit shows conflicts in red
2. Press 'e' to edit file
3. Resolve conflicts in editor
4. Return to LazyGit
5. Stage resolved files
6. Continue rebase/merge
```

---

## Advanced Patterns

### Git Stash

**Save work in progress**:
```bash
# Stash changes
git stash

# Stash with message
git stash save "WIP: redesign dashboard"

# List stashes
git stash list

# Apply latest stash
git stash apply

# Apply and remove stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Drop stash
git stash drop stash@{0}
```

### Cherry-Picking

**Apply specific commits to another branch**:
```bash
# Get commit hash
git log

# Apply commit to current branch
git cherry-pick abc123

# Cherry-pick multiple commits
git cherry-pick abc123 def456

# Cherry-pick without committing
git cherry-pick --no-commit abc123
```

### Bisect (Find Bug Introduction)

**Binary search for problematic commit**:
```bash
# Start bisect
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good abc123

# Git checks out middle commit
# Test if bug exists

# Mark as good or bad
git bisect good  # or git bisect bad

# Repeat until bug commit found
# Reset when done
git bisect reset
```

### Reflog (Recover Lost Work)

**View all HEAD movements**:
```bash
# Show reflog
git reflog

# Recover deleted branch
git checkout -b recovered-branch abc123

# Undo reset
git reset --hard abc123
```

---

## Breaking Change Detection

**Proactively flag breaking changes** whenever reviewing code, discussing commits, or observing changes - even when the user is handling commits themselves.

### What Constitutes a Breaking Change

#### API & Exports (High Priority)
| Change | Example | Breaking? |
|--------|---------|-----------|
| Removed export | `export function foo()` deleted | YES |
| Renamed export | `foo()` → `bar()` | YES |
| Changed parameters | `foo(a, b)` → `foo(a, b, c)` (required) | YES |
| Changed parameters | `foo(a, b)` → `foo(a, b, c?)` (optional) | NO |
| Reordered parameters | `foo(a, b)` → `foo(b, a)` | YES |
| Changed return type | `returns string` → `returns number` | YES |
| Narrowed return type | `returns string \| null` → `returns string` | NO |
| Widened return type | `returns string` → `returns string \| null` | YES |

#### TypeScript Types & Interfaces
| Change | Breaking? |
|--------|-----------|
| Removed property from exported interface | YES |
| Added required property to exported interface | YES |
| Added optional property to exported interface | NO |
| Renamed exported type/interface | YES |
| Changed property type | YES |
| Made optional property required | YES |
| Made required property optional | NO |

#### Database & Schema
| Change | Breaking? |
|--------|-----------|
| Removed column | YES |
| Renamed column | YES |
| Changed column type | YES |
| Added NOT NULL column without default | YES |
| Added nullable column | NO |
| Removed table | YES |
| Changed foreign key constraints | YES |
| Modified RLS policies (restrictive) | YES |

#### HTTP API Endpoints
| Change | Breaking? |
|--------|-----------|
| Removed endpoint | YES |
| Changed route path | YES |
| Changed HTTP method | YES |
| Removed request field | YES (if was required) |
| Added required request field | YES |
| Removed response field | YES |
| Changed response field type | YES |
| Changed authentication requirements | YES |
| Changed error response format | YES |

#### Configuration & Environment
| Change | Breaking? |
|--------|-----------|
| New required env variable | YES |
| Removed env variable | YES |
| Changed env variable name | YES |
| Changed config file format | YES |
| Changed default values | MAYBE (assess impact) |

#### Component Props (Svelte/React)
| Change | Breaking? |
|--------|-----------|
| Removed prop | YES |
| Renamed prop | YES |
| Changed prop type | YES |
| Added required prop | YES |
| Added optional prop | NO |
| Changed event signature | YES |

### Detection Patterns

When reviewing code, watch for these patterns:

```typescript
// BREAKING: Removed export
- export function calculateTotal(items: Item[]): number { ... }

// BREAKING: Renamed export
- export const UserContext = createContext(...)
+ export const AuthContext = createContext(...)

// BREAKING: Added required parameter
- export function fetchUser(id: string): Promise<User>
+ export function fetchUser(id: string, options: FetchOptions): Promise<User>

// BREAKING: Changed return type
- export function getConfig(): Config
+ export function getConfig(): Config | null

// BREAKING: Removed interface property
  export interface User {
    id: string;
    name: string;
-   email: string;
  }

// BREAKING: Added required property
  export interface CreateUserRequest {
    name: string;
+   email: string;  // required, no ?
  }
```

### How to Flag

When you detect a potential breaking change, flag it clearly:

```
⚠️ **Breaking Change Detected**

This change removes the `email` property from the exported `User` interface.
Any code depending on `User.email` will break.

Consider:
- Adding `BREAKING CHANGE: removed email from User interface` to commit footer
- Or using `feat!:` or `refactor!:` prefix
- Branch naming: `feat/breaking-remove-user-email`
```

### Non-Breaking Alternatives

When flagging, suggest non-breaking alternatives where possible:

| Breaking Change | Non-Breaking Alternative |
|-----------------|-------------------------|
| Remove function | Deprecate first, remove in next major |
| Rename export | Export both names, deprecate old |
| Add required param | Make param optional with default |
| Remove field | Mark as deprecated, return null |
| Change type | Use union type for transition period |

### Commit Message Format

For breaking changes, use one of:

```bash
# Option 1: Footer
feat(api): redesign user authentication

BREAKING CHANGE: removed password field from login endpoint,
now uses OAuth tokens exclusively

# Option 2: ! indicator
feat!: redesign user authentication

# Option 3: Both (for emphasis)
feat(api)!: redesign user authentication

BREAKING CHANGE: removed password field from login endpoint
```

---

## Success Criteria

Git workflow is successful when:
- Branch names follow established conventions
- Commit history is clear and meaningful
- Commits are atomic and well-described
- PRs are appropriately sized
- Conflicts resolved cleanly
- Team understands workflow
- Easy to trace changes and revert if needed
- LazyGit workflows streamlined
- Breaking changes are flagged and documented
