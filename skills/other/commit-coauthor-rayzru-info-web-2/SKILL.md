---
name: commit-coauthor
description: Create git commit with co-author attribution and comprehensive safety checks
context: fork
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Commit with Co-Author

Creates git commits with proper co-author attribution, following repository conventions and safety protocols.

**Token Efficiency**: Automates git safety checks and commit message generation (40% savings: 1,000 → 600 tokens)

## Usage

Invoke with: `/commit-coauthor [optional-message]`

**Examples**:
- `/commit-coauthor` - Auto-generate commit message from staged changes
- `/commit-coauthor "Fix authentication bug"` - Use provided message
- `/commit-coauthor "feat: Add user profile page"` - Follow conventional commits

## Prerequisites

- Git repository initialized
- Changes staged for commit (`git add` already executed)
- Git user.name and user.email configured
- No pre-commit hooks that would block commit (or hooks pass)

## Workflow

### Step 1: Safety Checks

**Run git status to verify staged changes**:

```bash
git status --porcelain
```

**Check for**:
- At least 1 file staged (M, A, D in column 1)
- No unresolved merge conflicts (UU status)
- Working directory state is clean enough to commit

**If no staged changes**:
- Return error: "No changes staged for commit. Use `git add` first."
- Exit Skill

**If merge conflicts exist**:
- Return error: "Unresolved merge conflicts detected. Resolve conflicts first."
- Exit Skill

### Step 2: Sensitive File Detection

**Check staged files for sensitive patterns**:

```bash
# Get list of staged files
git diff --cached --name-only
```

**Scan for sensitive file patterns**:
- `.env` files (environment variables)
- `credentials.json`, `secrets.yaml` (credential files)
- `*.pem`, `*.key` (private keys)
- `id_rsa`, `*.p12` (SSH/certificate files)
- Files containing `password`, `secret`, `token` in name

**If sensitive files detected**:
- Warn user: "⚠️ Sensitive file detected: [filename]. Are you sure you want to commit this?"
- List all detected sensitive files
- Ask user to confirm or exclude files

**Grep staged files for sensitive content patterns**:

```bash
# Check for hardcoded secrets in staged changes
git diff --cached | grep -iE "(api_key|secret_key|password|access_token|private_key)" || true
```

**If sensitive content found**:
- Warn user with context (line numbers, file names)
- Recommend using environment variables or git-crypt
- Ask for confirmation before proceeding

### Step 3: Analyze Staged Changes

**Get comprehensive diff of staged changes**:

```bash
# Show staged changes with file names and line counts
git diff --cached --stat
git diff --cached
```

**Analyze changes to determine**:
- **Change type**: New feature, bug fix, refactor, docs, test, chore
- **Scope**: Which files/modules affected (frontend, backend, database, config)
- **Impact**: Breaking change, enhancement, minor fix
- **File count**: Single file or multiple files

**Read recent commits for style**:

```bash
# Get last 5 commit messages to match repo style
git log -5 --pretty=format:"%s"
```

**Identify commit message conventions**:
- Conventional Commits format: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Imperative mood: "Add feature" vs "Added feature"
- Scope usage: `feat(auth):`, `fix(api):`
- Length: Short (50 chars) vs detailed

### Step 4: Generate Commit Message (if not provided)

**Only if user didn't provide message**

**Message structure**:

```
[type]([scope]): [short summary]

[optional body - detailed explanation]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Type classification logic**:

| Files Changed | Patterns Found | Type |
|--------------|----------------|------|
| `src/**/*.tsx`, `components/**` | New component created | `feat` |
| `*.tsx`, `*.ts` | Bug fix in existing code | `fix` |
| `README.md`, `docs/**` | Documentation only | `docs` |
| `*.test.ts`, `*.spec.ts` | Test files only | `test` |
| Code structure changes, no new behavior | Refactoring | `refactor` |
| Build config, dependencies | Configuration | `chore` |

**Scope extraction**:
- Auth files (`auth/**`, `*Auth*`): `auth`
- API files (`api/**`, `*api*`): `api`
- Database (`db/**`, `*.drizzle.*`): `db`
- UI components (`components/**`): `ui`
- Multiple areas: Omit scope or use general scope

**Summary guidelines**:
- Start with verb in imperative mood: "Add", "Fix", "Update", "Remove"
- Keep under 50 characters
- Focus on "what" and "why", not "how"
- No period at end

**Example auto-generated messages**:

```
feat(auth): Add password reset functionality

Implements password reset flow with email verification.
Adds /api/auth/reset-password endpoint and email templates.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

```
fix(api): Resolve null pointer in user profile endpoint

Adds null check before accessing user.shifts property.
Fixes TypeError that prevented profile page from loading.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Step 5: Create Commit

**Format commit message with co-author trailer**:

If user provided message:
```
[user-message]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

If auto-generated:
```
[generated-message-with-body]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Execute commit with HEREDOC for proper formatting**:

```bash
git commit -m "$(cat <<'EOF'
[commit-message-here]

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

**CRITICAL Git Safety Rules**:
- ✅ Use co-author trailer (required)
- ❌ NEVER use `--no-verify` (skip hooks)
- ❌ NEVER use `--amend` unless:
  - User explicitly requested amend, AND
  - HEAD commit was created by Claude in this conversation, AND
  - Commit has NOT been pushed to remote
- ❌ NEVER use `--force` or `--force-with-lease`
- ❌ NEVER commit without user awareness

### Step 6: Verify Commit Success

**Check git status after commit**:

```bash
git status
git log -1 --pretty=format:"%h %s%n%b"
```

**Success indicators**:
- Working tree clean or only unstaged files remain
- Latest commit matches expected message
- Co-author trailer present in commit body
- Commit hash generated

**If commit failed**:
- Extract error message from git output
- Identify failure cause (pre-commit hook, invalid message, etc.)
- Provide fix recommendation
- DO NOT retry automatically

**If commit succeeded**:
- Display commit hash and message
- Show files committed
- Note if there are remaining unstaged changes
- Ask if user wants to push to remote (don't push automatically)

### Step 7: Return Commit Summary

**Return structured result**:

```json
{
  "success": true,
  "commit_hash": "a1b2c3d",
  "commit_message": "[full commit message]",
  "files_committed": ["src/components/Auth.tsx", "src/api/auth.ts"],
  "files_count": 2,
  "insertions": 45,
  "deletions": 12,
  "unstaged_changes": 0,
  "co_author_added": true
}
```

**If commit failed**:

```json
{
  "success": false,
  "error": "Pre-commit hook failed: ESLint errors",
  "recommendation": "Fix ESLint errors and retry commit"
}
```

## Success Criteria

- [x] Safety checks completed (staged changes verified)
- [x] Sensitive files/content detected and warned
- [x] Commit message follows repository conventions
- [x] Co-author trailer added to commit body
- [x] Git Safety Protocol followed (no --no-verify, no --amend without checks)
- [x] Commit success verified
- [x] Structured result returned

## Git Safety Protocol

### Never Skip Hooks

**CRITICAL**: Never use `--no-verify` or `-n` flag

```bash
# ❌ WRONG - Skips pre-commit hooks
git commit --no-verify -m "message"

# ✅ CORRECT - Respects hooks
git commit -m "message"
```

**If pre-commit hook fails**:
- Show error message from hook
- Fix the issue (lint errors, format issues, etc.)
- Create NEW commit after fixing
- Do NOT use `--no-verify` to bypass

### Amend Rules

**Only use `--amend` when ALL conditions met**:

1. **User explicitly requested amend**, OR
2. **Commit SUCCEEDED** but pre-commit hook auto-modified files
3. **HEAD commit was created by Claude** in this conversation:
   ```bash
   git log -1 --format='%an %ae' | grep -q "Claude"
   ```
4. **Commit has NOT been pushed** to remote:
   ```bash
   git status | grep -q "Your branch is ahead"
   ```

**NEVER amend if**:
- ❌ Commit failed or was rejected by hook
- ❌ HEAD commit was created by user or other tool
- ❌ Commit already pushed to remote (requires force push)
- ❌ User didn't explicitly request amend

**If commit FAILED or REJECTED**:
- Fix the issue
- Create NEW commit (do NOT amend)

### Force Push Protection

**NEVER run force push unless**:
- User explicitly requested: "force push to main"
- Even then, warn if branch is main/master

```bash
# ❌ NEVER run automatically
git push --force
git push --force-with-lease

# ✅ Only if user explicitly requests and confirms
# Show warning: "⚠️ Force push to main can overwrite team's work. Are you sure?"
```

### Sensitive Content Rules

**NEVER commit without warning**:
- `.env` files (recommend `.env.example` instead)
- `credentials.json`, `secrets.yaml`
- Private keys (`.pem`, `.key`)
- Files with `password`, `secret`, `token` in content

**If user requests committing sensitive file**:
- Show warning with explanation
- Recommend alternatives (environment variables, git-crypt, secrets manager)
- Require explicit confirmation: "Type 'yes' to commit anyway"

## Error Handling

### Error 1: No Staged Changes

**Symptom**: `git status` shows no files in staging area
**Cause**: User forgot to `git add` files
**Solution**:
```bash
# Show what files can be staged
git status --short

# Return error
echo "No changes staged for commit. Use 'git add <file>' first."
```

### Error 2: Pre-Commit Hook Failed

**Symptom**: Commit rejected with hook error message
**Cause**: Code doesn't pass lint, format, or test checks
**Solution**:
- Display full hook error message
- Identify issue (ESLint errors, Prettier format, failing tests)
- Recommend fix: "Run `npm run lint:fix` to auto-fix errors"
- Create NEW commit after fixing (do NOT use `--no-verify`)

### Error 3: Invalid Commit Message Format

**Symptom**: Commit rejected due to commit message validation hook
**Cause**: Message doesn't follow Conventional Commits or repo standards
**Solution**:
- Show expected format from hook error
- Regenerate message following correct format
- Retry commit with corrected message

### Error 4: Merge Conflict Detected

**Symptom**: `git status` shows UU (unmerged) files
**Cause**: User in middle of merge with conflicts
**Solution**:
```bash
echo "Unresolved merge conflicts detected in:"
git diff --name-only --diff-filter=U

echo "Resolve conflicts first using 'git mergetool' or manually edit files."
```

### Error 5: Detached HEAD State

**Symptom**: `git status` shows "HEAD detached at [commit]"
**Cause**: User checked out specific commit instead of branch
**Solution**:
```bash
echo "⚠️ In detached HEAD state. Commit will not be on any branch."
echo "Checkout a branch first: 'git checkout main'"
```

## Examples

### Example 1: Auto-Generated Message

**User**: `/commit-coauthor`

**Git status**:
```
M  src/components/Settings.tsx
M  src/api/settings.ts
A  src/types/settings.d.ts
```

**Auto-generated commit**:
```
feat(settings): Add user notification preferences

Implements email and SMS notification toggles.
Adds Settings API endpoint and TypeScript types.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Output**:
```json
{
  "success": true,
  "commit_hash": "7f3a8c2",
  "commit_message": "feat(settings): Add user notification preferences\n\nImplements email and SMS notification toggles.\nAdds Settings API endpoint and TypeScript types.\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
  "files_committed": ["src/components/Settings.tsx", "src/api/settings.ts", "src/types/settings.d.ts"],
  "files_count": 3,
  "insertions": 87,
  "deletions": 5,
  "co_author_added": true
}
```

**Console log**: "✅ Commit created: 7f3a8c2 'feat(settings): Add user notification preferences'"

### Example 2: User-Provided Message

**User**: `/commit-coauthor "Fix null pointer in scheduler view"`

**Commit**:
```
Fix null pointer in scheduler view

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Output**:
```json
{
  "success": true,
  "commit_hash": "b4c8d1e",
  "commit_message": "Fix null pointer in scheduler view\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>",
  "files_committed": ["src/components/SchedulerView.tsx"],
  "files_count": 1,
  "insertions": 3,
  "deletions": 1,
  "co_author_added": true
}
```

### Example 3: Sensitive File Warning

**User**: `/commit-coauthor`

**Staged files**: `.env`, `src/config/database.ts`

**Output**:
```
⚠️ Sensitive file detected: .env

This file may contain secrets or credentials.

Recommendations:
1. Create .env.example with placeholder values instead
2. Add .env to .gitignore
3. Use environment variables for sensitive data

Detected patterns in .env:
- DATABASE_URL (contains connection string)
- JWT_SECRET (contains secret key)

Do you want to proceed with committing .env? (Type 'yes' to confirm)
```

**If user confirms 'yes'**:
- Create commit with warning in commit body
- Log sensitive file commit for audit

**If user cancels**:
- Exit Skill
- Suggest: `git reset HEAD .env` to unstage

### Example 4: Pre-Commit Hook Failure

**User**: `/commit-coauthor`

**Pre-commit hook output**:
```
ESLint found 3 errors:
  src/components/Settings.tsx
    42:15  error  'user' is not defined  no-undef
    58:22  error  Missing semicolon      semi
```

**Skill output**:
```json
{
  "success": false,
  "error": "Pre-commit hook failed: ESLint errors",
  "details": "3 errors in src/components/Settings.tsx",
  "recommendation": "Fix ESLint errors:\n1. Line 42: Define 'user' variable\n2. Line 58: Add missing semicolon\n\nRun 'npm run lint:fix' to auto-fix, then retry commit."
}
```

**Console log**: "❌ Commit failed: ESLint errors detected. Fix errors and retry."

### Example 5: Conventional Commits Format

**User**: `/commit-coauthor`

**Staged files**: Multiple test files added

**Auto-detected type**: `test`

**Commit**:
```
test(auth): Add unit tests for password reset flow

Tests email verification and token expiration.
Achieves 95% coverage for auth module.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## Integration with Development Workflow

**Use this Skill**:
- ✅ After implementing feature (stage changes, commit with co-author)
- ✅ After fixing bugs (proper commit message with fix type)
- ✅ Before creating pull request (commit all work)
- ✅ During code review fixes (commit review changes)

**Combine with other Skills**:
1. Implement feature
2. Run `/debug-console` (verify no console errors)
3. Run `/visual-test-figma` (verify design matches)
4. Run `/commit-coauthor` (commit changes with co-author)
5. Run `/create-pr` (create pull request) - P2 Skill

**Integration with Git Workflow**:
```bash
# Feature development workflow
git checkout -b feature/user-settings
# ... make changes ...
git add .
/commit-coauthor  # ← This Skill
git push -u origin feature/user-settings
/create-pr  # ← P2 Skill (next phase)
```

## Conventional Commits Reference

**Type prefixes**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, missing semicolons)
- `refactor`: Code restructuring without behavior change
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Build process, dependencies, tooling

**Scope examples**:
- `(auth)`: Authentication/authorization
- `(api)`: API endpoints
- `(db)`: Database schema/queries
- `(ui)`: UI components
- `(build)`: Build system
- `(deps)`: Dependencies

**Breaking changes**:
```
feat(api)!: Change user endpoint response format

BREAKING CHANGE: User endpoint now returns 'id' instead of 'userId'
```

## Token Efficiency

**Baseline (manual git commit)**:
- Read git commit guidelines: 200 tokens
- Check staged files: 100 tokens
- Analyze changes: 200 tokens
- Write commit message: 200 tokens
- Execute commit: 100 tokens
- Verify success: 200 tokens
- **Total**: ~1,000 tokens

**With commit-coauthor Skill**:
- Skill invocation: 150 tokens
- Safety checks: 100 tokens
- Auto-generate message: 200 tokens
- Execute commit: 50 tokens
- Verify success: 100 tokens
- **Total**: ~600 tokens

**Savings**: 400 tokens (40% reduction)

**Projected usage**: 20x per week
**Weekly savings**: 8,000 tokens
**Annual savings**: 416,000 tokens (~$1.04/year)

## Related Documentation

- [Git Safety Protocol](../../README.md) - Git safety rules in system prompt
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message standard
- [TOKEN_EFFICIENCY.md](../../guidelines/TOKEN_EFFICIENCY.md) - Token optimization patterns

---

**Skill Version**: 1.0
**Created**: 2026-01-09
**Last Updated**: 2026-01-09
**Requires**: Claude Code v2.1.0+, Git repository
