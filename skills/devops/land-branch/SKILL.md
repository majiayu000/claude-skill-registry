---
name: land-branch
description: >
  Land a feature branch: pull from main, rebase the branch, create a PR,
  and merge it via rebase with automatic branch deletion. Use when ready
  to land a completed feature branch.
---

# Land Branch Workflow

**Use this skill to land a feature branch in one smooth flow.**

> **Note:** Steps 1-2 use scripts in `./scripts/` that are pre-allowlisted in settings.json,
> so they won't require permission prompts.

## Prerequisites

- You're on a feature branch (not `main`)
- All changes are committed
- The feature is ready to merge

## Step 1: Verify Branch State

```bash
# Use the allowlisted script to verify we're ready to land
./scripts/verify-branch
```

This script checks:
- You're not on `main` (need to be on a feature branch)
- No uncommitted changes (commit or stash first)

### Recovering from Commits on Main

If you accidentally made commits directly on `main` instead of a feature branch:

```bash
# Check how many commits you're ahead of origin/main
git log --oneline origin/main..HEAD

# Create a new branch with your commits (pick a descriptive name)
git branch my-feature-branch

# Reset main back to match origin/main
git reset --hard origin/main

# Switch to your new branch
git checkout my-feature-branch

# Verify: your commits should now be on the feature branch
git log --oneline -5
```

**Why this works:**
- `git branch` creates a new branch pointing to your current commit
- `git reset --hard origin/main` moves main back to where it should be
- Your commits are preserved on the new branch

Now continue with the land-branch workflow from Step 2.

## Step 2: Pull and Rebase onto Main

```bash
# Use the allowlisted script to fetch, rebase, and push
./scripts/rebase-main
```

This script:
- Detects fork vs direct repo (reads `.claude-workspace`)
- Fetches latest main from correct remote
- Rebases current branch onto main
- Pushes with `--force-with-lease` (safe force push)

If rebase has conflicts, resolve them manually, run `git rebase --continue`, then re-run the script.

## Step 2.5: Check for Downstream Dependencies

**IMPORTANT:** If your changes modified any pattern's input type (the type parameter to `pattern<Input>`), you MUST check if other patterns import and use that pattern.

```bash
# Get list of changed .tsx files
CHANGED_PATTERNS=$(git diff --name-only $MAIN_REMOTE/main...HEAD -- '*.tsx')

if [ -n "$CHANGED_PATTERNS" ]; then
  echo "Changed patterns:"
  echo "$CHANGED_PATTERNS"
  echo ""
  echo "Checking for downstream dependencies..."

  for file in $CHANGED_PATTERNS; do
    # Extract the pattern name from the file path
    PATTERN_NAME=$(basename "$file" .tsx)

    # Search for imports of this pattern in other files
    IMPORTERS=$(grep -l "from.*['\"].*${PATTERN_NAME}['\"]" patterns/**/*.tsx 2>/dev/null | grep -v "$file" || true)

    if [ -n "$IMPORTERS" ]; then
      echo ""
      echo "⚠️  $PATTERN_NAME is imported by:"
      echo "$IMPORTERS"
      echo "   → Check if input type changes require updates to these files!"
    fi
  done
fi
```

**What to check:**
- If you changed a pattern's input type (added/removed/renamed fields)
- Find all patterns that import and instantiate that pattern
- Update their instantiation calls to match the new type
- Common case: `page-creator.tsx` imports many patterns for its launcher buttons

**Example:** If `hotel-membership-extractor.tsx` input changes from 10 fields to 3 fields, `page-creator.tsx` must be updated to only pass the 3 valid fields.

### Verify Importing Patterns Deploy Successfully

After updating any importing patterns, **you MUST verify they compile and deploy**:

```bash
# For each pattern that imports the changed pattern, test deployment
# Example: if page-creator.tsx imports hotel-membership-extractor.tsx

cd ../labs && deno task ct charm new \
  --api-url http://localhost:8000 \
  --identity ../labs/claude.key \
  --space testing \
  /path/to/community-patterns/patterns/$USER/page-creator.tsx
```

**Why this matters:**
- TypeScript compilation happens at deploy time, not at save time
- A pattern may look fine in your editor but fail to deploy due to type mismatches
- Catching these errors before landing prevents broken patterns on main

**If deployment fails:**
1. Read the error message (usually shows the exact type mismatch)
2. Fix the instantiation call to match the new input type
3. Re-deploy to verify the fix
4. Commit the fix before proceeding

## Step 2.6: Verify Pattern README is Up to Date

**IMPORTANT:** Before creating a PR, verify that `patterns/$GITHUB_USER/README.md` is up to date for any patterns touched in this branch.

```bash
# Get list of changed pattern files
CHANGED_PATTERNS=$(git diff --name-only $MAIN_REMOTE/main...HEAD -- 'patterns/*/[^W]*.tsx' 'patterns/*/WIP/*.tsx')

if [ -n "$CHANGED_PATTERNS" ]; then
  echo "Patterns changed in this branch:"
  echo "$CHANGED_PATTERNS"
  echo ""
  echo "⚠️  Verify README.md is updated for these patterns!"
fi
```

**For each changed pattern, check:**

1. **New patterns** - Add a complete entry to README.md:
   - Pattern name as heading
   - One-line description
   - "Interesting features" bullet list highlighting notable implementation details
   - Place in correct section (Stable Patterns or WIP Patterns)

2. **Significantly modified patterns** - Review the existing entry:
   - Does the description still match what the pattern does?
   - Are the "Interesting features" still accurate?
   - Did you add new features worth mentioning?

3. **Patterns moved from WIP to root** - Update both sections:
   - Remove from WIP Patterns section
   - Add to Stable Patterns section with full description

**Example README entry format:**
```markdown
#### `pattern-name.tsx`
One-line description of what this pattern does.

**Interesting features:**
- Notable implementation detail or framework feature used
- Interesting pattern or technique
- Integration with other patterns
```

**If README needs updating:**
1. Edit `patterns/$GITHUB_USER/README.md` to add/update pattern entries
2. Commit the README update
3. Continue with creating the PR

## Step 2.7: Verify Pattern Compiles Before PR

**CRITICAL:** Always verify changed patterns compile before creating a PR. This catches missing imports, type mismatches, and other errors that will fail CI.

```bash
# From community-patterns directory, test that a pattern compiles
# Note: Command must be on ONE LINE (multi-line breaks argument parsing)
cd ../labs && deno task ct charm new --identity ../labs/claude.key --api-url http://localhost:8000 --space test-compile ../community-patterns/patterns/$GITHUB_USER/my-pattern.tsx
```

**If compilation succeeds:** You'll see a charm ID like `baedrei...`

**If compilation fails:** You'll see a `CompilerError` with the exact file and line:
```
[ERROR] Cannot find name 'computed'.
1039 |     const notesDiffChunks = computed(() => {
     |                             ^
```

**To fix:**
1. Read the error message - it shows the exact file and line
2. Fix the issue (often a missing import like `computed`, `cell`, `derive`)
3. Commit the fix
4. Re-run to verify
5. Continue with creating the PR

**Why this matters:**
- CI runs typecheck on all PRs - failures will block the merge
- Catching errors locally is faster than waiting for CI
- Common issues: missing imports after adding new framework features

## Step 3: Create PR

```bash
# Check if PR already exists for this branch
EXISTING_PR=$(gh pr view $CURRENT_BRANCH --json number --jq '.number' 2>/dev/null)

if [ -n "$EXISTING_PR" ]; then
  echo "PR #$EXISTING_PR already exists for this branch"
  PR_NUMBER=$EXISTING_PR
else
  # Create new PR
  # Adjust --repo flag based on fork status
  if [ "$IS_FORK" = "true" ]; then
    gh pr create \
      --repo jkomoros/community-patterns \
      --title "$(git log -1 --format=%s)" \
      --body "$(cat <<'EOF'
## Summary
Auto-generated PR for branch landing.

## Testing
- [x] Tested locally

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
  else
    gh pr create \
      --title "$(git log -1 --format=%s)" \
      --body "$(cat <<'EOF'
## Summary
Auto-generated PR for branch landing.

## Testing
- [x] Tested locally

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
  fi

  # Get the PR number
  PR_NUMBER=$(gh pr view --json number --jq '.number')
fi

echo "PR #$PR_NUMBER ready"
```

## Step 4: Wait for CI and Merge

**By default, wait for CI checks to pass before merging.**

```bash
# Wait for CI then merge (default behavior)
./scripts/land-pr

# Or specify a PR number explicitly
./scripts/land-pr 123
```

**To skip waiting for CI (use with caution):**

```bash
# Force merge without waiting for CI
./scripts/land-pr --force

# Or with explicit PR number
./scripts/land-pr --force 123
```

The `land-pr` script:
- Waits for all CI checks to pass (unless `--force` is used)
- Merges with rebase strategy
- Deletes the feature branch
- Switches to main and pulls merged changes
- Pushes to origin (for forks)

## Complete Flow Using Scripts

All steps use allowlisted scripts that don't require permission prompts:

```bash
# Step 1: Verify we're ready
./scripts/verify-branch

# Step 2: Rebase and push
./scripts/rebase-main

# Step 3: Create PR (use gh commands as shown above)

# Step 4: Wait for CI and merge
./scripts/land-pr

# Or force merge without waiting for CI
./scripts/land-pr --force
```

## Important Notes

- **Waits for CI by default** - ensures checks pass before merging
- **Use `--force` sparingly** - only when you're confident CI will pass
- **Always uses `--rebase`** for merging (preserves commit history)
- **Auto-deletes the branch** after successful merge
- **Force-with-lease** is safe - it only pushes if no one else pushed
- If the PR needs review, stop after Step 3 and wait for approval
- For self-merging (when you have write access), all steps can run automatically
- **Always verify README.md** is current with pattern changes (Step 2.6)
- **Always run typecheck** before creating PR to catch CI failures early (Step 2.7)
