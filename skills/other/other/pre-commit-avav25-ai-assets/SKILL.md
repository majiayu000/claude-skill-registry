---
name: pre-commit
description: Pre-commit quality gate — lint, format, test, validate before committing. Runs automated checks and fixes issues. Use before git commit to ensure code quality.
disable-model-invocation: true
---

# Pre-Commit

Automated quality gate before committing code. Runs linting, formatting, tests, and validation checks. Fixes auto-fixable issues and reports blockers.

## 1. Detect Project Stack

Read `CLAUDE.md` and project config files to determine:

- **Language(s)**: TypeScript, Java, Python, Go, etc.
- **Package manager**: npm/pnpm/yarn, maven/gradle, pip/poetry, go mod
- **Linter**: ESLint, Checkstyle, ruff/flake8, golangci-lint
- **Formatter**: Prettier, google-java-format, black/ruff, gofmt
- **Test runner**: Vitest/Jest, JUnit/Maven, pytest, go test

## 2. Check Staged Changes

```
// turbo
git status --short
```

Identify which files are staged. If no files are staged:

```
⚠️ No staged changes found. Stage your changes first:
  git add <files>
```

Stop and inform the user.

## 3. Run Linter

Run the project's linter on staged files:

| Stack | Command |
|---|---|
| TypeScript/JS | `npx eslint --fix <files>` |
| Python | `ruff check --fix <files>` or `flake8 <files>` |
| Java | `mvn checkstyle:check` or `gradle checkstyleMain` |
| Go | `golangci-lint run <files>` |

**Completion**: If exit code 0 after auto-fix → proceed. If errors remain → report and STOP:

```
## Lint Issues (must fix)
- [file:line] [rule] description
```

## 4. Run Formatter

Run the project's formatter:

| Stack | Command |
|---|---|
| TypeScript/JS | `npx prettier --write <files>` |
| Python | `ruff format <files>` or `black <files>` |
| Java | `mvn spotless:apply` or `google-java-format <files>` |
| Go | `gofmt -w <files>` |

Re-stage any auto-formatted files:
```
git add <formatted-files>
```

**Completion**: Files formatted and re-staged → proceed.

## 5. Run Type Checker (if applicable)

| Stack | Command |
|---|---|
| TypeScript | `npx tsc --noEmit` |
| Python | `mypy <files>` or `pyright <files>` |

**Completion**: If exit code 0 → proceed. If type errors → report and STOP.

## 6. Run Tests

Run the project's test suite (unit tests at minimum):

| Stack | Command |
|---|---|
| TypeScript/JS | `npx vitest run` or `npx jest` |
| Python | `pytest -x -q` |
| Java | `mvn test -q` or `gradle test` |
| Go | `go test ./...` |

If tests fail:
1. Analyze the failure
2. Attempt auto-fix if the fix is obvious and safe
3. Re-run tests to verify
4. If still failing — report and STOP

**Completion**: All tests pass → proceed. Any failure after auto-fix attempt → STOP.

## 7. Validate Build (if applicable)

| Stack | Command |
|---|---|
| TypeScript/JS | `npm run build` or `npx tsc --noEmit` |
| Java | `mvn compile -q` |
| Go | `go build ./...` |

## 8. Summary

```
## Pre-Commit Results

| Check      | Status | Details |
|------------|--------|---------|
| Lint       | ✅/❌  | [issues found/fixed] |
| Format     | ✅/❌  | [files formatted] |
| Type check | ✅/❌/⏭️ | [errors or N/A] |
| Tests      | ✅/❌  | [passed/failed count] |
| Build      | ✅/❌/⏭️ | [success or N/A] |

Ready to commit: [YES / NO — fix issues above first]
```

If all checks pass, suggest the commit command:
```
git commit -m "<type>(<scope>): <description>"
```

Follow Conventional Commits format.

## Integration

- **Called by**: `/feature-dev`, `/bugfix` (before commit)
- **Calls**: `/run-tests`
- **Followed by**: `/create-pr`
