---
name: conventional-commits
description: >
  Git commit management following Conventional Commits specification for Aurora projects.
  Trigger: When creating commits, analyzing git history, or reviewing commit messages.
license: MIT
metadata:
  author: aurora
  version: "1.0"
  auto_invoke: "Creating commits, git operations, analyzing commit history"
---

## When to Use
- User asks to create a commit or "commit changes"
- User asks to review git status or diff
- User wants to analyze commit history
- After completing features/fixes that need to be committed
- User mentions "conventional commits" or asks about commit format

---

## Critical Patterns

### Commit Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Types (in order of usage frequency)
| Type | Description | Example |
|------|-------------|---------|
| `feat` | New functionality | `feat(library/book): add ISBN validation` |
| `fix` | Bug fix | `fix(auth): resolve token refresh race condition` |
| `refactor` | Code refactoring, no functional change | `refactor(core): extract validation logic to service` |
| `test` | Add or modify tests | `test(book): add unit tests for create handler` |
| `docs` | Documentation changes | `docs(readme): add installation instructions` |
| `chore` | Maintenance tasks | `chore(deps): update nestjs to v10` |
| `style` | Formatting, semicolons, etc. | `style(api): apply prettier formatting` |
| `perf` | Performance improvements | `perf(query): optimize book search with index` |
| `ci` | CI/CD changes | `ci(github): add deployment workflow` |
| `build` | Build system or dependencies | `build(docker): optimize production image` |
| `revert` | Revert previous commit | `revert: feat(book): add ISBN validation` |

### Subject Rules
1. ✅ Use imperative mood: "add" NOT "added" or "adds"
2. ✅ Lowercase first letter
3. ✅ No period at the end
4. ✅ Maximum 120 characters
5. ✅ Describe WHAT, not HOW

**Good:**
- `feat(book): add publication date validation`
- `fix(auth): resolve token refresh issue`

**Bad:**
- `feat(book): Added publication date validation` (past tense)
- `fix(auth): Resolve token refresh issue` (uppercase)
- `feat(book): add publication date validation.` (period)

### Body Rules (Optional)

1. Separate from subject with blank line
2. Explain WHY, not WHAT
3. Wrap at 72 characters per line
4. Can use bullet points with `-`

### Footer Rules (Optional)

1. Reference issues: `Closes #123`, `Fixes #456`
2. Breaking changes: `BREAKING CHANGE: <description>`
3. ❌ **NEVER** add "Co-Authored-By" or AI attribution

---

## Commit Workflow

### 1. Analyze Changes
```bash
git status                # See modified/untracked files
git diff                  # See unstaged changes
git diff --staged         # See staged changes
git log --oneline -10     # See recent commit style
```

### 2. Group Related Changes

**Rules:**
- One commit = one logical change
- ❌ Don't mix features with fixes
- ❌ Don't mix multiple unrelated modules
- ✅ Multiple files are OK if they implement one feature

### 3. Generate Message
Analyze the changes and determine:
1. **Type**: feat, fix, refactor, etc.
2. **Scope**: Which module/component is affected?
3. **Subject**: What does this change do?
4. **Body** (if needed): Why was this change necessary?
5. **Footer** (if needed): Issue references, breaking changes

### 4. Execute Commit
```bash
git add <files>
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

<footer>
EOF
)"
```

---

## Code Examples

### Simple Feature
```
feat(library/book): add publication date validation

Validate that publication date is not in the future
when creating or updating a book.

Closes #234
```

### Bug Fix with Context
```
fix(auth): resolve token refresh race condition

Multiple simultaneous requests could trigger parallel
token refreshes, causing some requests to fail.

- Add mutex lock during refresh
- Queue pending requests until refresh completes
- Add retry logic for failed requests

Fixes #567
```

### Refactor (No Functional Change)
```
refactor(library/book): extract ISBN validation to service

Move ISBN validation logic from command handler to
dedicated IsbnValidatorService for reusability.

No functional changes.
```

### Breaking Change
```
feat(api)!: change pagination response format

BREAKING CHANGE: Pagination response now uses cursor-based
format instead of offset-based.

Before: { items: [], total: 100, page: 1 }
After: { items: [], nextCursor: "abc", hasMore: true }

Migration guide in docs/migration/v2-pagination.md
```

### Aurora YAML Changes
```
feat(aurora): add category entity to library module

Define new Category aggregate with:
- id, name, description fields
- many-to-many relation with Book

Run: aurora load back module -n=library/category
```

### Dependency Update
```
chore(deps): update @nestjs packages to v10.2.0

- @nestjs/core: 10.1.0 -> 10.2.0
- @nestjs/common: 10.1.0 -> 10.2.0
- @nestjs/platform-express: 10.1.0 -> 10.2.0

No breaking changes in this update.
```

### Multiple Modules (Related Change)
```
feat(tesla): add maintenance validation across models

- Add validation in Model aggregate
- Update MaintenanceHistory to check model status
- Add integration tests for both modules

This ensures consistency when creating maintenance records.
```

---

## Commands
```bash
# View status
git status

# View changes
git diff                    # Unstaged changes
git diff --staged          # Staged changes
git diff --cached          # Same as --staged

# Stage files
git add <file>             # Stage specific file
git add -p                 # Interactive staging (choose hunks)

# Commit
git commit -m "message"    # Simple commit
git commit                 # Opens editor for body

# View history
git log --oneline -20                      # Last 20 commits
git log --pretty=format:"%h %s" -20       # Custom format
git log --graph --oneline --all           # Visual graph

# Amend last commit (use with caution)
git commit --amend -m "new message"       # Change message
git commit --amend --no-edit              # Add files to last commit
```

---

## Anti-Patterns to Avoid
| ❌ Bad | ✅ Good |
|--------|---------|
| `git commit -m "fix"` | `fix(auth): resolve token expiration bug` |
| `git commit -m "WIP"` | Finish the work or use feature branch |
| `git commit -m "changes"` | `refactor(core): extract common validation logic` |
| `git commit -m "update files"` | `feat(book): add ISBN field to entity` |
| `git commit -am "everything"` | Split into logical commits |
| Mix feat + fix + refactor | Separate commits for each type |
| Commit generated files only | Commit YAML changes + explain regeneration |

---

## Aurora-Specific Notes

### 1. YAML Changes
```
feat(aurora): add category entity to library module

Define new Category aggregate with id, name, description.

Run: aurora load back module -n=library/category
```

### 2. Custom Logic in Generated Files
```
feat(library/book): add complex ISBN validation logic

Implement custom validation in CreateBookHandler:
- Validate ISBN format (10 or 13 digits)
- Check checksum digit
- Verify not in blacklist

This logic is in a generated file marked as custom.
```

### 3. Multiple Related Modules
```
feat(tesla): integrate maintenance history with models

- Update Model aggregate with maintenance status
- Add validation in MaintenanceHistory creation
- Add integration tests

Changes span tesla/model and tesla/maintenance-history.
```

### 4. Test Commits

**Option A: Combined with feature**
```
feat(book): add ISBN validation with tests

- Add ISBN validation in CreateBookHandler
- Add unit tests for validation logic
- Add e2e tests for create endpoint
```

**Option B: Separate commit**
```
test(book): add unit tests for ISBN validation

Add comprehensive test coverage for:
- Valid ISBN-10 and ISBN-13 formats
- Invalid formats and checksums
- Edge cases (empty, null, special chars)
```

---

## Decision Trees

### Should I commit now?
```
Has code changed? ────NO───> No commit needed
      │
     YES
      │
Is it a logical unit? ────NO───> Break into smaller commits
      │
     YES
      │
Do tests pass? ────NO───> Fix tests first
      │
     YES
      │
  Create commit
```

### What type should I use?
```
New functionality? ────YES───> feat
      │
      NO
      │
Fixing a bug? ────YES───> fix
      │
      NO
      │
No functional change? ────YES───> refactor
      │
      NO
      │
Only tests? ────YES───> test
      │
      NO
      │
Dependencies? ────YES───> chore(deps)
      │
      NO
      │
Documentation? ────YES───> docs
      │
      NO
      │
    Default: chore
```

### How to scope?
```
Single module changed? ────YES───> Use <bc>/<module>
      │
      NO
      │
Multiple related modules? ────YES───> Use common <bc> or higher scope
      │
      NO
      │
Infrastructure? ────YES───> Use: ci, docker, config, deps
      │
      NO
      │
Core/API/GraphQL? ────YES───> Use: core, api, graphql
      │
      NO
      │
    Omit scope or use project name
```

---

## Related Skills
This skill works with:
- **aurora-cli**: Commit YAML changes and regenerated code
- **aurora-development**: Commit business logic implementations (feat commits)
- **jest-nestjs**: Commit test files (test commits or include with feat)
- **logger**: Log commit information in session reports

**Workflow:**
1. Make changes (YAML modifications, business logic, tests)
2. Use **aurora-cli** to regenerate code (if YAML changed)
3. Use **conventional-commits** to create proper commit
4. Use **logger** to document the session (optional)

---

## Resources
- **Specification**: https://www.conventionalcommits.org/
- **Aurora Config**: `commitlint.config.js` (read this for project-specific rules)
- **Git Hooks**: Pre-commit hooks may enforce format validation
