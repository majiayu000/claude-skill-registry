---
name: preflight
description: Run all validation checks without releasing. Use before /release to verify everything is ready.
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
---

# Preflight Checks

Run all validations to confirm the project is ready for release. This does NOT create commits, PRs, tags, or publish anything.

## Step 1: Environment checks

```bash
git branch --show-current
git status --porcelain
gh auth status
```

Report:
- Current branch name
- Whether working tree is clean
- Whether gh is authenticated

## Step 2: Version analysis

```bash
# Current version
node -e "console.log(require('./package.json').version)"

# Last tag
git describe --tags --abbrev=0 2>/dev/null || echo "no tags"

# Commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~50")..HEAD --oneline --no-decorate
```

Analyze commits and suggest:
- Recommended bump type (patch/minor/major)
- Suggested new version
- Summary of changes by category

## Step 3: Run checks

```bash
pnpm format:fix 2>&1   # auto-fix formatting before checking — prevents CI failures on style
pnpm check
```

Report pass/fail for each:
- Typecheck
- Lint
- Tests

## Step 4: Coverage check (optional)

```bash
pnpm test:coverage
```

Report current coverage percentage.

## Step 5: Build verification

```bash
pnpm build
```

Confirm build succeeds and report output size.

## Step 6: CHANGELOG review

Read CHANGELOG.md and check:
- Is there content under `## [Unreleased]`?
- Are there commits that aren't reflected in the changelog?
- Are version comparison links up to date?

## Final report

Print a summary table:

```
## Preflight Report

| Check              | Status | Notes                    |
|--------------------|--------|--------------------------|
| Branch             | ...    | feature/xxx              |
| Working tree       | ...    | clean / N files modified |
| gh auth            | ...    | authenticated as USER    |
| Typecheck          | ...    |                          |
| Lint               | ...    |                          |
| Tests              | ...    | N passed, N failed       |
| Coverage           | ...    | XX%                      |
| Build              | ...    | dist/ XXkb               |
| Changelog          | ...    | up to date / needs update|
| Suggested version  | ...    | X.Y.Z (bump_type)       |

Ready for release: YES / NO
```

If all checks pass, suggest running `/release` with the detected bump type.
If any check fails, list what needs to be fixed first.
