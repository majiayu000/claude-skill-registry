---
name: review-test-coverage
description: "Analyze code for test coverage gaps, untested functions, and missing edge cases. Returns structured findings without writing tests. Use when the user asks to \"review test coverage\", \"check test coverage\", \"find untested code\", \"analyze coverage gaps\", or \"what needs tests\"."
---

# Review Test Coverage

Analyze code for test coverage gaps. Identify untested functions, missing edge cases, and areas where test quality is insufficient. Return structured findings.

## Step 1: Determine the Scope

Determine what to analyze:

- If a specific **diff command** was provided (e.g., `git diff --cached`), run it to identify changed code that needs coverage analysis.
- If a **file list or directory** was provided, analyze those files directly.
- If **neither** was provided, default to diffing against the repository's default branch (detect via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`).

## Step 2: Identify Coverage Gaps

1. For each file in scope, skip non-testable code (config, documentation, CI files, SKILL.md files, markdown)
2. Search for existing test files covering the target code
3. Identify the project's test framework and conventions by reading existing test files
4. Analyze each function/module for:
   - **No test coverage**: functions or modules with no corresponding tests
   - **Missing edge cases**: tests exist but miss critical paths (error handling, boundary conditions, empty inputs, concurrent access)
   - **Risk-level mismatch**: high-risk code (auth, data handling, financial logic) with only basic happy-path tests
   - **Convention gaps**: tests not following the project's established testing patterns

## Output Format

Return findings as a numbered list. For each finding:

```
### [P<N>] <title (imperative, <=80 chars)>

**File:** `<file path>` (lines <start>-<end>)

<one paragraph describing the coverage gap and why it matters>
```

After all findings, add:

```
## Overall Verdict

**Test Coverage:** <adequate | gaps found>

<1-3 sentence summary>
```

If nothing needs tests, report that and explain briefly.

## Priority Levels

- **P0** — Critical code with no tests (auth, data mutation, payment processing)
- **P1** — Important code with no tests or high-risk code with only happy-path tests
- **P2** — Code with tests but missing significant edge cases
- **P3** — Minor coverage gaps or convention mismatches
