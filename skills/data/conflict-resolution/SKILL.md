---
name: conflict-resolution
description: Use when encountering merge conflicts - handle conflicts cleanly, verify resolution, and maintain code integrity
---

# Conflict Resolution

## Overview

Handle merge conflicts systematically to maintain code integrity.

**Core principle:** Conflicts require careful resolution, not just picking one side.

**Announce at start:** "I'm using conflict-resolution to handle these merge conflicts."

## When Conflicts Occur

Conflicts happen when:

| Situation | Example |
|-----------|---------|
| Rebasing on updated main | `git rebase origin/main` |
| Merging main into branch | `git merge origin/main` |
| Cherry-picking commits | `git cherry-pick [sha]` |
| Pulling with local changes | `git pull` |

## The Resolution Process

```
Conflict Detected
       │
       ▼
┌─────────────────┐
│ 1. UNDERSTAND   │ ← What's conflicting and why?
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. ANALYZE      │ ← Review both versions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. RESOLVE      │ ← Make informed decision
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. VERIFY       │ ← Tests pass, code works
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. CONTINUE     │ ← Complete the operation
└─────────────────┘
```

## Step 1: Understand the Conflict

### See Conflicting Files

```bash
# List files with conflicts
git status

# Output shows:
# Unmerged paths:
#   both modified:   src/services/user.ts
#   both modified:   src/utils/validation.ts
```

### View the Conflict

```bash
# See the conflict markers
cat src/services/user.ts
```

```typescript
<<<<<<< HEAD
// Your changes
function createUser(data: UserData): User {
  return { ...data, id: generateId() };
}
=======
// Their changes (main branch)
function createUser(data: UserData): Promise<User> {
  return db.create({ ...data, id: generateId() });
}
>>>>>>> main
```

### Understand the History

```bash
# See what changed in each branch
git log --oneline --left-right HEAD...main -- src/services/user.ts

# See the actual changes
git diff HEAD...main -- src/services/user.ts
```

## Step 2: Analyze Both Versions

### Questions to Answer

| Question | Consider |
|----------|----------|
| What was the intent of your change? | Your feature/fix |
| What was the intent of their change? | Their feature/fix |
| Are they mutually exclusive? | Can both coexist? |
| Which is more recent/correct? | Check issue references |
| Do both need to be kept? | Merge the logic |

### Compare Approaches

```markdown
## Conflict Analysis: src/services/user.ts

### My Change (feature/issue-123)
- Made createUser synchronous
- Reason: Simplified for local testing
- Issue: #123

### Their Change (main)
- Made createUser async with DB
- Reason: Production database integration
- Issue: #456

### Resolution
Keep their async version (production requirement).
My testing simplification should use mocks instead.
```

## Step 3: Resolve the Conflict

### Resolution Strategies

#### Keep Theirs (Main)

When main's version is correct:

```bash
# Use their version
git checkout --theirs src/services/user.ts
git add src/services/user.ts
```

#### Keep Ours (Your Branch)

When your version is correct:

```bash
# Use your version
git checkout --ours src/services/user.ts
git add src/services/user.ts
```

#### Manual Merge (Both)

When both changes are needed:

```typescript
// Remove conflict markers
// Combine both changes intelligently

// Result: Keep async from main, add your new validation
async function createUser(data: UserData): Promise<User> {
  // Your addition: validation
  validateUserData(data);

  // Their change: async DB call
  return db.create({ ...data, id: generateId() });
}
```

```bash
# After editing
git add src/services/user.ts
```

### Conflict Markers

Remove ALL conflict markers:

```
<<<<<<< HEAD      ← Remove
=======           ← Remove
>>>>>>> main      ← Remove
```

The final file should have NO conflict markers.

## Step 4: Verify Resolution

### Syntax Check

```bash
# TypeScript: Check types
pnpm typecheck

# Or for specific file
npx tsc --noEmit src/services/user.ts
```

### Run Tests

```bash
# Run all tests
pnpm test

# Run tests for affected area
pnpm test --grep "user"
```

### Visual Review

```bash
# See final resolved state
git diff --cached

# Ensure no conflict markers remain
grep -r "<<<<<<" src/
grep -r "======" src/
grep -r ">>>>>>" src/
```

## Step 5: Continue the Operation

### After Rebase

```bash
# Continue the rebase
git rebase --continue

# If more conflicts, repeat resolution
# When complete:
git push --force-with-lease
```

### After Merge

```bash
# Complete the merge
git commit -m "Merge main into feature/issue-123"

# Push
git push
```

### Abort if Needed

If resolution goes wrong:

```bash
# Abort rebase
git rebase --abort

# Abort merge
git merge --abort

# Start fresh
```

## Complex Conflicts

### Multiple Files

Resolve one file at a time:

```bash
# See all conflicts
git status

# Resolve each
# 1. Edit file
# 2. git add file
# 3. Next file

# When all resolved
git rebase --continue
```

### Semantic Conflicts

Sometimes code merges cleanly but is semantically broken:

```typescript
// main: Function signature changed
function process(data: NewFormat): Result

// yours: Called with old format
process(oldFormatData);  // No conflict marker, but broken!
```

**Always run tests after resolution.**

### Conflicting Dependencies

```json
// package.json conflict
<<<<<<< HEAD
  "dependencies": {
    "library": "^2.0.0"
=======
  "dependencies": {
    "library": "^1.5.0"
>>>>>>> main
```

Resolution:
1. Choose the appropriate version
2. Delete `pnpm-lock.yaml`
3. Run `pnpm install`
4. Commit the new lock file

## Best Practices

### Before Resolution

- Pull latest main frequently to minimize conflicts
- Keep branches short-lived
- Communicate about shared files

### During Resolution

- Take your time
- Understand both changes
- Don't just pick "ours" or "theirs" blindly
- Test after resolution

### After Resolution

- Run full test suite
- Review the merged result
- Commit with clear message

## Conflict Message

When conflicts occur during PR:

```markdown
## Merge Conflict Resolution

This PR had conflicts with main that have been resolved.

### Conflicting Files
- `src/services/user.ts`
- `src/utils/validation.ts`

### Resolution Summary

**user.ts:**
Kept async implementation from main, added validation from this PR.

**validation.ts:**
Merged both validation rules (main added email, this PR added phone).

### Verification
- [x] All tests pass
- [x] Build succeeds
- [x] No conflict markers in code
- [x] Functionality verified manually
```

## Checklist

When resolving conflicts:

- [ ] All conflicting files identified
- [ ] Each conflict analyzed (understood both sides)
- [ ] Resolution chosen (ours/theirs/merge)
- [ ] Conflict markers removed
- [ ] Files staged (`git add`)
- [ ] Tests pass
- [ ] Build succeeds
- [ ] No remaining conflict markers
- [ ] Operation completed (rebase --continue / commit)

## Integration

This skill is called when:
- `git rebase` encounters conflicts
- `git merge` encounters conflicts
- PR shows conflicts

This skill ensures:
- Clean resolution
- No lost changes
- Working code after merge
