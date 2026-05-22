---
name: fresh-eyes
description: Re-reads code you just wrote with fresh perspective to catch bugs, errors, and issues. Use after completing a feature, fixing a bug, or any code changes. Triggers on "review my code", "fresh eyes", "check for bugs", "did I miss anything", or "sanity check".
---

# Fresh Eyes Review

Re-read all code you just wrote or modified with a fresh perspective. Look for obvious bugs, errors, problems, and confusion that are easy to miss when deep in implementation.

## When to Use

- After completing a feature or fix
- Before committing changes
- When you feel like something might be off
- After a long coding session

## Process

### 1. Identify Changed Code

Find all files you modified in this session. If unclear, ask the user or check recent git changes:

```bash
git diff --name-only HEAD~1
git diff --name-only --cached
```

### 2. Re-read with Fresh Eyes

Read each modified file completely. Pretend you've never seen this code before. Look for:

**Logic errors**
- Off-by-one errors
- Inverted conditions
- Missing null/undefined checks
- Race conditions
- Incorrect comparisons (== vs ===, > vs >=)

**Obvious bugs**
- Typos in variable names
- Copy-paste errors
- Forgotten return statements
- Unused variables that should be used
- Wrong function called

**Missing pieces**
- Error handling gaps
- Edge cases not covered
- Cleanup code missing (close connections, clear timeouts)
- Validation missing at boundaries

**Confusion risks**
- Misleading variable names
- Complex logic without comments
- Inconsistent patterns within the file
- Magic numbers without explanation

### 3. Fix Issues

For each issue found:
1. Explain what's wrong in 1 sentence
2. Fix it immediately
3. Move to the next issue

Don't ask for permission. Just fix obvious problems.

### 4. Report Summary

After fixing, provide a brief summary:

```
## Fresh Eyes Review

Fixed 3 issues:
- `api/users.ts:47` — Missing null check on user.profile
- `api/users.ts:82` — Off-by-one in pagination (used > instead of >=)
- `utils/format.ts:15` — Typo: `formattedDte` → `formattedDate`

No other issues found.
```

If nothing found:
```
## Fresh Eyes Review

Reviewed 4 files. No issues found.
```

## What NOT to Do

- Don't refactor working code
- Don't add features
- Don't change style preferences
- Don't optimize prematurely
- Don't add comments to obvious code
- Don't reorganize file structure

Focus only on **bugs, errors, and problems**. If it works and isn't broken, leave it alone.

## Checklist

Run through mentally for each file:

- [ ] All variables initialized before use?
- [ ] All functions return what they should?
- [ ] All loops terminate correctly?
- [ ] All conditions handle both branches?
- [ ] All async operations awaited?
- [ ] All errors caught or propagated?
- [ ] All resources cleaned up?
- [ ] All edge cases handled (empty, null, zero, negative)?
