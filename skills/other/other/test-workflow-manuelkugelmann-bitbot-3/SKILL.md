---
name: test-workflow
description: Run BitBot's iterative test workflow (implement → test → fix → commit → push). Use PROACTIVELY during development to ensure quality before committing.
---

Running BitBot test workflow...

This workflow supports the full development cycle:
1. **Implement** - Write/modify code
2. **Test** - Fix line endings, check syntax, run tests
3. **Fix** - Address failures iteratively
4. **Commit** - Once all tests pass
5. **Push** - Share your work

## Usage

**Single file check** (basic mode):
```bash
.claude/skills/test-workflow/scripts/test-workflow.sh <file>
```

**Implementation loop** (use this in practice):
1. Make changes to implementation file
2. Run workflow on implementation + test file
3. If tests fail, fix issues and repeat from step 2
4. Once tests pass, commit and push

## What It Does

**Step 1: Fix Line Endings & Check Syntax**
- Converts CRLF → LF
- Validates bash syntax
- Reports any syntax errors

**Step 2: Run Tests (if test file)**
- Executes with 60-second timeout
- Prevents hanging tests
- Shows pass/fail results

**Step 3: Report Status**
- Shows success/failure
- Next steps if errors found

## When to Use Proactively

**During iterative development (recommended):**
```bash
# 1. Implement feature
vim core/util/feature.sh

# 2. Test implementation
.claude/skills/test-workflow/scripts/test-workflow.sh core/util/feature.sh

# 3. Create/update tests
vim dev/tests/test-feature.sh

# 4. Run test suite
.claude/skills/test-workflow/scripts/test-workflow.sh dev/tests/test-feature.sh

# 5. If tests fail, fix and repeat steps 2-4
# 6. Once all tests pass, commit
git add core/util/feature.sh dev/tests/test-feature.sh
git commit -m "Add feature with tests (all passing)"
git push
```

**Quick single-file checks:**
```bash
# After creating/modifying shell script
.claude/skills/test-workflow/scripts/test-workflow.sh core/util/new-script.sh

# After updating test file
.claude/skills/test-workflow/scripts/test-workflow.sh dev/tests/test-feature.sh
```

## See Also

- `sparc/0-research/TESTING_PROCESS.md` - Full testing guidelines
- `.claude/skills/fix-line-endings-check-bash/` - Individual fix+check
- `.claude/skills/run-with-timeout/` - Timeout wrapper
