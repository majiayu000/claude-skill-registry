---
name: git-storytelling-commit-strategy
description: Use when planning commit strategies or determining when to commit changes. Helps developers commit early and often to tell the story of their development process.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Git Storytelling - Commit Strategy

This skill helps you understand and implement effective commit strategies that tell the story of your development process through small, focused commits.

## Key Concepts

### Commit Early, Commit Often

The practice of making small, frequent commits throughout development rather than large, infrequent commits. This approach:

- Creates a detailed history of your thought process
- Makes it easier to understand changes
- Simplifies debugging and reverting changes
- Enables better code reviews
- Tells the story of how the solution evolved

### Atomic Commits

Each commit should represent a single logical change:

- One feature addition
- One bug fix
- One refactoring
- One documentation update

This makes the git history navigable and meaningful.

### The Story Arc

Your commits should read like a story:

1. **Setup**: Initial project structure, dependencies
2. **Development**: Incremental feature additions
3. **Refinement**: Bug fixes, optimizations
4. **Polish**: Documentation, cleanup

## Best Practices

### DO Commit When

✅ You've completed a logical unit of work (even if small)
✅ Tests pass for the changes made
✅ You're about to switch tasks or take a break
✅ You've refactored code to be clearer
✅ You've fixed a bug (one commit per bug)
✅ You've added a new file or module
✅ You've updated documentation
✅ You're at a stable checkpoint

### DON'T Commit When

❌ Code doesn't compile or has syntax errors
❌ Tests are failing (unless documenting a known issue)
❌ You have unrelated changes mixed together
❌ You have debugging code or temporary comments
❌ You have secrets or sensitive data

## Commit Message Patterns

### Good Commit Messages

```
feat: add user authentication with JWT

Implement JWT-based authentication system with:
- Login endpoint
- Token generation
- Token validation middleware

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
fix: resolve memory leak in websocket handler

Close websocket connections properly when client disconnects
to prevent memory accumulation.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
refactor: extract validation logic into separate module

Move validation functions from controllers to validators/
for better reusability and testing.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Commit Prefixes

- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code restructuring without behavior change
- `test:` - Adding or updating tests
- `docs:` - Documentation changes
- `style:` - Formatting, whitespace changes
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

## Examples

### Example 1: Building a REST API

Good storytelling commits:

```bash
# 1. Setup
git commit -m "feat: initialize Express server with basic configuration"

# 2. Foundation
git commit -m "feat: add database connection with Prisma"

# 3. Feature development
git commit -m "feat: create user model and migration"
git commit -m "feat: add user registration endpoint"
git commit -m "feat: add user login endpoint"
git commit -m "test: add user authentication tests"

# 4. Refinement
git commit -m "fix: validate email format in registration"
git commit -m "refactor: extract password hashing to utility"

# 5. Documentation
git commit -m "docs: add API endpoint documentation"
```

### Example 2: Bug Fix Process

```bash
# 1. Identify and reproduce
git commit -m "test: add failing test for pagination edge case"

# 2. Fix the issue
git commit -m "fix: handle empty results in pagination"

# 3. Verify
git commit -m "test: verify pagination works with edge cases"

# 4. Cleanup
git commit -m "refactor: simplify pagination logic"
```

### Example 3: Refactoring

```bash
# 1. Prepare
git commit -m "test: add comprehensive tests before refactoring"

# 2. Small steps
git commit -m "refactor: extract common validation logic"
git commit -m "refactor: rename confusing variable names"
git commit -m "refactor: split large function into smaller units"

# 3. Verify
git commit -m "test: verify all tests still pass after refactor"
```

## Common Patterns

### Working on a Feature

1. Commit initial structure/skeleton
2. Commit each component or module
3. Commit tests as you write them
4. Commit bug fixes immediately when found
5. Commit documentation when complete
6. Final commit for integration

### Debugging

1. Commit reproduction test case
2. Commit the fix
3. Commit any related improvements discovered
4. Commit documentation of the issue

### Code Review Feedback

1. Commit each suggested change separately
2. Use descriptive messages referencing the feedback
3. Keep commits small for easier review

## Anti-Patterns

### Avoid These Commit Styles

❌ **The Dump Truck**

```bash
git commit -m "updated files"  # Too vague, too many changes
```

❌ **The Novel**

```bash
git commit -m "fixed bug and added feature and updated docs and refactored code and..."
```

❌ **The WIP Spam**

```bash
git commit -m "wip"
git commit -m "wip2"
git commit -m "wip3"
# Use better descriptions even for work-in-progress
```

❌ **The Time Machine**

```bash
# Making 50 commits then squashing them ALL into one
# This destroys the development story entirely
```

✅ **Better Approach**: Clean up meaningless commits locally before pushing, but preserve the logical story:

```bash
# Keep logical commits that tell the story
git rebase -i origin/main

# Result: Clean story with meaningful commits
# feat: implement user authentication
# test: add authentication tests
# fix: handle edge cases
# docs: document authentication API
```

## Workflow Integration

### With Feature Branches

```bash
# On feature branch
git checkout -b feature/user-auth

# Make small commits
git commit -m "feat: add User model"
git commit -m "feat: add authentication middleware"
git commit -m "test: add auth tests"

# Clean history is preserved when merging
git checkout main
git merge feature/user-auth
```

### With Pull Requests

Small commits make code review easier:

- Reviewers can understand changes step-by-step
- Discussion can happen on specific commits
- Changes are easier to test individually

### With CI/CD

Frequent commits trigger CI more often:

- Catch issues earlier
- Smaller changesets are easier to debug
- Faster feedback loop

## Cleaning Up Local Commits

### The Golden Rule: Local vs Pushed

**✅ Safe to rebase: Local commits (not yet pushed)**

- You can freely rewrite, reorder, squash, or edit local commits
- Interactive rebase is your friend for cleaning up messy history
- No one else has based work on these commits yet

**❌ Dangerous to rebase: Pushed commits (already on remote)**

- Rewriting pushed commits creates conflicts for collaborators
- Only rebase pushed commits if you're the only person on the branch
- Requires force push which can lose others' work
- Exception: Personal feature branches where you're the only contributor

### When to Clean Up Local Commits

Before pushing your work, consider cleaning up if you have:

- **WIP commits**: Multiple "work in progress" or "wip" commits
- **Fix commits**: "oops fix typo" or "forgot to add file" commits
- **Debug commits**: Commits that added then removed debugging code
- **Logical grouping**: Related changes split across multiple commits
- **Commit message errors**: Typos or unclear messages in commit history

### Interactive Rebase for Cleanup

Use `git rebase -i` to clean up your local commit history before pushing:

```bash
# Check what commits you haven't pushed yet
git log origin/main..HEAD --oneline

# Interactive rebase for last 5 commits
git rebase -i HEAD~5

# Or rebase everything since branching from main
git rebase -i origin/main
```

#### Rebase Commands

In the interactive rebase editor, you can:

- `pick` - Keep commit as-is
- `reword` - Keep commit but edit message
- `edit` - Pause to amend the commit
- `squash` - Merge into previous commit, keep both messages
- `fixup` - Merge into previous commit, discard this message
- `drop` - Remove commit entirely
- `reorder` - Move lines to reorder commits

#### Common Cleanup Patterns

**Pattern 1: Squash fixup commits**

Before:

```
feat: add user authentication
wip: add tests
fix: oops forgot import
fix: typo in test
test: add more edge cases
```

After rebasing:

```
feat: add user authentication
test: add authentication tests
```

Commands in rebase editor:

```
pick abc123 feat: add user authentication
pick def456 wip: add tests
fixup ghi789 fix: oops forgot import
fixup jkl012 fix: typo in test
squash mno345 test: add more edge cases
```

**Pattern 2: Split WIP into logical commits**

Before:

```
wip: stuff
wip: more stuff
wip: final changes
```

After rebasing:

```
feat: implement user authentication
test: add authentication tests
docs: document auth API
```

Commands in rebase editor:

```
edit abc123 wip: stuff
edit def456 wip: more stuff
edit ghi789 wip: final changes
```

Then for each commit:

```bash
git reset HEAD^           # Unstage the commit
git add -p                # Selectively stage changes
git commit -m "feat: implement user authentication"
git add -p                # Stage more changes
git commit -m "test: add authentication tests"
# ... etc
git rebase --continue
```

**Pattern 3: Improve commit messages**

Before:

```
stuff
more changes
final
```

After rebasing:

```
feat: add JWT authentication
test: add authentication tests
docs: update API documentation
```

Commands in rebase editor:

```
reword abc123 stuff
reword def456 more changes
reword ghi789 final
```

### Example Workflow: Commit Often, Clean Up Before Push

```bash
# During development - commit frequently
git commit -m "wip: start auth implementation"
git commit -m "wip: add JWT generation"
git commit -m "oops: fix import"
git commit -m "wip: add tests"
git commit -m "fix: test typo"
git commit -m "wip: add validation"

# Before pushing - check what you have
git log origin/main..HEAD --oneline
# Shows 6 messy WIP commits

# Clean up with interactive rebase
git rebase -i origin/main

# In editor, consolidate into logical commits:
# - Squash the "oops" and "fix" commits
# - Combine related WIP commits
# - Reword commit messages to be descriptive

# Result: Clean, logical history
git log origin/main..HEAD --oneline
#
# feat: implement JWT authentication
# test: add authentication tests
# feat: add request validation

# Now push your clean history
git push origin feature/user-auth
```

### When NOT to Rebase

Don't rebase if:

- ❌ Commits are already pushed to a shared branch (main, develop)
- ❌ Other people have branched from your commits
- ❌ You're pair programming and both pushing to same branch
- ❌ Commits are part of a merged pull request
- ❌ You're unsure about the impact (when in doubt, don't rebase)

### Recovering from Rebase Mistakes

If a rebase goes wrong:

```bash
# Abort ongoing rebase
git rebase --abort

# Or recover using reflog (rebase already completed)
git reflog                    # Find the commit before rebase
git reset --hard HEAD@{5}     # Go back to that state
```

### Best Practices

1. **Commit frequently during development** - Don't worry about perfect commits
2. **Review before pushing** - Use `git log` to see what you're about to push
3. **Clean up before pushing** - Use interactive rebase to create logical story
4. **Never rebase pushed commits** - Unless you're absolutely sure you're the only one
5. **Use descriptive commit messages** - Even after cleanup, messages should be clear
6. **Test after rebasing** - Make sure tests still pass after rewriting history

## Related Skills

- **git-history-navigation**: Understanding git log, bisect, and blame
- **git-branch-strategy**: Managing branches effectively
- **code-review**: How commit strategy improves reviews

## Tips for Success

1. **Commit before context switching** - Always commit before changing tasks
2. **Review before committing** - Use `git diff` to review changes
3. **Write commit messages for future you** - Explain the "why" not just the "what"
4. **Keep the story coherent** - Each commit should make sense on its own
5. **Use the hook** - Let the jutsu-git-storytelling hook remind you to commit
6. **Clean up before pushing** - Use `git rebase -i` to polish local commits before sharing
7. **Never rebase pushed commits** - Respect shared history, only rebase local work

## Checking Your Commit Story

Review your commits to ensure they tell a good story:

```bash
# View commit history
git log --oneline --graph

# See what changed in each commit
git log -p

# Review recent commits
git log --oneline -10
```

A good story should be:

- Easy to follow
- Logically ordered
- Self-documenting
- Helpful for debugging
