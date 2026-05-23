---
name: test-resolve-review
description: Integration test for /resolve-review skill. Creates fixtures, guides manual testing, verifies results.
---

# Test resolve-review

Integration test for the resolve-review skill with preset fixtures.

## Usage

```
/test-resolve-review
```

## Flow

1. **Setup** - Creates branch, PR, review threads, and PR comments
2. **Manual execution** - User runs `/resolve-review --self --pr=<N>`
3. **Verify** - Checks thread resolution, comment minimization, commits, summary
4. **Cleanup** - Closes PR, deletes branch

## Instructions

### Phase 1: Setup

Run the setup script:

```bash
SETUP_OUTPUT=$(plugins/pr/skills/test-resolve-review/scripts/setup-test-pr.sh)
PR_NUMBER=$(echo "$SETUP_OUTPUT" | jq -r '.pr_number')
BRANCH=$(echo "$SETUP_OUTPUT" | jq -r '.branch')
```

Create the tmp directory and write execution guide to `.claude/tmp/test-resolve-review-guide.md`:

```bash
mkdir -p .claude/tmp
```

```markdown
# Test Execution Guide

## Start Prompt
Select both:
- ☑ Post summary comment
- ☑ Push commits

## Items

| Item | Description | Action |
|------|-------------|--------|
| 1+2 | "null check" threads (grouped) | ADDRESS |
| 3 | "Complex refactor needed" | **DEFER** |
| 4 | "Add loading state" (PR comment) | ADDRESS |
| 5a | "Fix error handling" (part 1/3) | ADDRESS |
| 5b | "Also add types" (part 2/3) | ADDRESS |
| 5c | "And tests" (part 3/3) | ADDRESS |

## Command
\`\`\`
/resolve-review --self --pr=$PR_NUMBER
\`\`\`

## When Done
Return here and say "verify"
```

Display:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEST: resolve-review integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Setting up test fixtures...
  ✓ Created branch: $BRANCH
  ✓ Created test-fixture-file.ts
  ✓ Opened PR #$PR_NUMBER
  ✓ Added 3 review threads
  ✓ Added 2 PR comments

Guide written to: .claude/tmp/test-resolve-review-guide.md

Run: /resolve-review --self --pr=$PR_NUMBER

When done, say "verify" to check results.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for user to complete manual testing and say "verify".

### Phase 2: Verify

When user says "verify", run verification:

```bash
VERIFY_OUTPUT=$(plugins/pr/skills/test-resolve-review/scripts/verify-test-pr.sh --pr="$PR_NUMBER")
PASSED=$(echo "$VERIFY_OUTPUT" | jq -r '.passed')
```

Display results:

```
Verifying test results...
```

For each assertion in output, display:
- `✓` if passed
- `✗` if failed

If all passed:
```
All assertions passed! Cleanup? [Yes / Keep for inspection]
```

If any failed:
```
Some assertions failed. Cleanup? [Yes / Keep for inspection]
```

### Phase 3: Cleanup

If user confirms cleanup:

```bash
plugins/pr/skills/test-resolve-review/scripts/cleanup-test-pr.sh --pr="$PR_NUMBER" --branch="$BRANCH"
```

Display:
```
Cleanup complete. Test session ended.
```

If user wants to keep for inspection:
```
Keeping PR #$PR_NUMBER and branch $BRANCH for inspection.
Run cleanup manually when done:
  gh pr close $PR_NUMBER --delete-branch
```

## Test Fixtures

| # | Type | Content | Expected Action |
|---|------|---------|-----------------|
| 1 | Thread | "Add null check before accessing user.name" | Address |
| 2 | Thread | "Also needs null check here" | Address (group with 1) |
| 3 | Thread | "This needs refactoring - significant rework" | Defer |
| 4 | PR Comment | "Add loading state while fetching" | Address |
| 5 | PR Comment | "Fix error handling. Also add types. And tests." | Address (3 parts) |

## Assertions

- Threads 1, 2: resolved
- Thread 3: still open (deferred)
- Comments 4, 5: minimized
- At least 4 commits created
- Summary comment posted with "Feedback Summary" section
