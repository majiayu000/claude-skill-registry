---
name: orthogonalize-pr
description: Identify and separate orthogonal (independent) change sets within a decomposed PR. Creates branches for each set that could theoretically be reviewed or merged separately.
---

# Orthogonalize PR

Identify independent change sets within a PR and separate them into branches.

## Why This Exists

Many PRs bundle unrelated changes together. A "fix retry logic" PR might also add logging, refactor a helper, and update tests for something else. These orthogonal changes:

- Make review harder (reviewer context-switches between concerns)
- Make bisect harder (which change caused the regression?)
- Make reverts harder (can't revert just the problematic part)

By identifying orthogonal components, you can suggest splitting the PR or understand its independent pieces.

## Prerequisites

Run `/decompose-pr` first. Orthogonalize operates on a decomposed branch where each commit represents a logical change.

## Phase 1: Analyze Dependencies

Review each commit from the decomposed branch and map dependencies.

```bash
# List commits on the decomposed branch
git log --oneline <base>..HEAD

# For each commit, examine what it touches
git show --stat <commit>
git show <commit>
```

**For each commit, identify:**

1. **What it introduces** — New types, functions, files
2. **What it depends on** — Types/functions from other commits in this branch
3. **What depends on it** — Later commits that use what this introduces

**Build a dependency table:**

```
| Commit | Introduces | Depends On | Depended By |
|--------|------------|------------|-------------|
| 1 | CacheEntry type | - | 2, 3 |
| 2 | Cache struct | 1 | 3 |
| 3 | Cache integration | 1, 2 | - |
| 4 | RateLimiter type | - | 5 |
| 5 | RateLimiter integration | 4 | - |
```

## Phase 2: Identify Orthogonal Sets

Group commits into **orthogonal sets** — clusters with internal dependencies but no cross-cluster dependencies.

**Algorithm:**

1. Build a graph where commits are nodes and dependencies are edges
2. Find connected components — each component is an orthogonal set
3. Commits with no dependencies on other branch commits are their own set

From the example above:

- **Set A**: Commits 1, 2, 3 (Cache feature)
- **Set B**: Commits 4, 5 (RateLimiter feature)

These sets are orthogonal — they don't depend on each other.

**Present to user:**

```
## Orthogonal Sets

| Set | Commits | Description | Files |
|-----|---------|-------------|-------|
| A | 1, 2, 3 | Cache feature | cache.ts, index.ts |
| B | 4, 5 | Rate limiting | limiter.ts, index.ts |

Sets A and B are independent. They touch `index.ts` in different places
but don't share types or call each other.
```

**Get user input:** They may want to name the sets differently, or may see dependencies you missed.

## Phase 3: Create Branches

Create a branch for each orthogonal set.

```bash
# Start from the decomposed branch
git checkout <user>/decompose/<pr-branch>

# For each set, create a branch with just those commits
git checkout -b <user>/orthogonalize/<pr-branch>/cache <base>
git cherry-pick <commit-1> <commit-2> <commit-3>

git checkout -b <user>/orthogonalize/<pr-branch>/rate-limiter <base>
git cherry-pick <commit-4> <commit-5>
```

**Verify each branch:**

```bash
# Should build independently
# (prettier, cargo fmt, black, etc.)
# (npm run build, cargo check, make build, etc.)
```

If a branch doesn't build, either:

- A dependency was missed — revisit Phase 2
- The changes aren't truly orthogonal — merge the sets

## Phase 4: Summarize

Present the orthogonal structure:

```
## Orthogonalization Complete

Original PR: #123 "Add caching and rate limiting"
Decomposed branch: user/decompose/feature-branch
Orthogonal branches:

| Branch | Commits | Description | Builds? |
|--------|---------|-------------|---------|
| user/orthogonalize/feature-branch/cache | 3 | Cache feature | Yes |
| user/orthogonalize/feature-branch/rate-limiter | 2 | Rate limiting | Yes |

**Recommendation:** These could be two separate PRs:
1. "Add response caching" (cache branch)
2. "Add rate limiting" (rate-limiter branch)

Merging in either order would work. No conflicts expected.
```

## When Sets Aren't Worth Splitting

Sometimes orthogonal sets exist but splitting isn't worthwhile:

- **Too small**: A 5-line logging change isn't worth its own PR
- **Conceptually unified**: Author bundled them intentionally for a reason
- **Review overhead**: Two PRs means twice the CI, review cycles, merge conflicts

Note these cases but don't force splits. The goal is to _identify_ orthogonality, not mandate separation.

## Edge Cases

**Shared base refactor:** Sometimes commit 1 is a refactor that enables both Set A and Set B. Options:

- Include it in both branches (duplication, but each stands alone)
- Make it a third "foundation" set that both depend on
- Leave sets coupled if the refactor is small

**File-level overlap:** Two sets may touch the same file in different places. This is fine — they're still orthogonal if changes don't interact. Git can merge them.

**Test coupling:** Tests might span multiple sets. Options:

- Include tests with the code they test
- Create a separate "tests" set if tests are truly independent
- Accept some test duplication across branches

## Anti-patterns

- Orthogonalizing without decomposing first (you need to understand the changes)
- Creating too many tiny sets (defeats the purpose)
- Missing semantic dependencies (two functions that must exist together)
- Forcing orthogonality when changes are genuinely coupled

---

Enter orthogonalization mode now. Confirm which decomposed branch to analyze, then begin Phase 1.
