---
name: commit
description: Create logical, well-described git commits for session changes. Reviews changes, groups them logically, writes descriptive commit messages, and requires confirmation before committing.
---

# Commit Changes with Review

Create git commits for changes made during this session.

## CRITICAL RULES

1. **NEVER commit without describing what will be committed first**
2. **NEVER use `git add -A` or `git add .`**
3. **ALWAYS review conversation history to write accurate commit messages**
4. **ALWAYS make multiple logical commits instead of one large commit**
5. **NEVER add co-author or AI attribution** (commits authored by human only)

## Process

### Step 1: Review What Changed

```bash
# Show all changes
git status

# Review each file
git diff path/to/file1
git diff path/to/file2
```

### Step 2: Describe Changes to User

Present a structured description:

```
I've made changes to the following files:

1. src/components/Login.tsx
   - Added OAuth provider selection
   - Implemented token refresh logic
   - Added error boundary for auth failures

2. src/utils/auth.ts
   - Created validateToken helper
   - Added token expiry checking

3. tests/auth.test.ts
   - Added tests for new OAuth flow
   - Added tests for token validation

These changes can be grouped into logical commits:

Commit 1: "Add OAuth provider selection to login"
- src/components/Login.tsx
- src/utils/auth.ts

Commit 2: "Add token validation and refresh"
- src/utils/auth.ts (additional changes)
- tests/auth.test.ts

Shall I proceed with these commits?
```

### Step 3: Wait for Confirmation

**Do not proceed until the user confirms or provides guidance.**

### Step 4: Execute Commits

For each approved commit:

```bash
# Add specific files only
git add src/components/Login.tsx
git add src/utils/auth.ts

# Create commit with descriptive message
git commit -m "add(auth): OAuth provider selection in login

Added UI for selecting OAuth provider (Google, GitHub, Microsoft).
Implemented provider-specific configuration and redirect handling.

- LoginForm component now displays provider buttons
- auth.ts handles provider-specific OAuth flows
- Error states for unsupported providers"

# Verify
git log --oneline -1
```

### Step 5: Repeat for Additional Commits

Continue with remaining logical groups of changes.

## Commit Message Format

```
<type>(<scope>): <short description>

<detailed description of what and why>

- Bullet points for key changes
- Focus on the 'why' not just the 'what'
```

**Types:** add, update, fix, refactor, docs, test, chore

## Good vs Bad Commits

### ❌ Bad Approach
```bash
git add -A
git commit -m "updates"
```

### ✅ Good Approach
```bash
git add src/auth/oauth.ts
git add src/auth/providers.ts
git commit -m "add(auth): OAuth provider abstraction

Created provider interface and implementations for Google, GitHub.
Each provider handles its own authorization URLs and token exchange.

- BaseProvider interface defines contract
- GoogleProvider and GitHubProvider implementations
- Provider registry for runtime selection"
```

## Verification Checklist

Before each commit:
- [ ] Reviewed git diff for each file
- [ ] Grouped changes logically
- [ ] Written descriptive commit message with context
- [ ] Used explicit file paths in git add
- [ ] No AI attribution in commit message
- [ ] Commit message explains why, not just what
