---
name: analyze-coverage
description: Analyze test coverage and identify gaps with actionable recommendations
argument-hint: "[<project-path>] [--spec <spec-path>] [--threshold <percentage>]"
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion
---

# Analyze Coverage Skill

Analyze test coverage for any project by running real coverage tools, parsing results into structured reports, and identifying gaps with actionable recommendations. Optionally maps coverage against spec acceptance criteria to find untested requirements.

**CRITICAL: Complete ALL 6 phases.** The workflow is not complete until Phase 6: Suggest Next Steps is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Core Principles

1. **Real coverage data** -- Run actual coverage tools (pytest-cov, istanbul/c8) via Bash. Never estimate or guess coverage percentages.
2. **Standalone operation** -- This skill works on any project. It does not require the SDD pipeline, specs, or any other skill to function.
3. **Actionable output** -- Every coverage gap should include a specific suggestion for what test to write, not just a percentage.
4. **Graceful degradation** -- If coverage tools are not installed, detect and inform the user with install commands. If a spec is invalid, skip spec mapping and proceed with coverage-only analysis.

## AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Clarifying questions about project structure -> AskUserQuestion
- Framework/tool selection -> AskUserQuestion
- Threshold confirmation -> AskUserQuestion

Text output should only be used for presenting information, summaries, reports, and progress updates.

**NEVER do this** (asking via text output):
```
Which package should I measure coverage for?
1. src/
2. lib/
```

**ALWAYS do this** (using AskUserQuestion tool):
```yaml
AskUserQuestion:
  questions:
    - header: "Coverage Target"
      question: "Which package or directory should coverage be measured for?"
      options:
        - label: "src/"
          description: "Main source directory"
        - label: "lib/"
          description: "Library directory"
      multiSelect: false
```

---

## Phase 1: Detect Environment

**Goal:** Auto-detect the project's test framework, coverage tool, and source package.

### Parse Arguments

Analyze `$ARGUMENTS` to extract optional parameters:

- **Project path**: Directory to analyze (default: current working directory)
- **`--spec <path>`**: Spec file for acceptance criteria mapping
- **`--threshold <percentage>`**: Coverage threshold override (default: 80%)

### Detect Project Type

Determine the project type by checking for language-specific files:

**Python detection (check in order):**
1. `pyproject.toml` exists -> Python project
2. `setup.py` or `setup.cfg` exists -> Python project
3. `requirements.txt` exists -> Python project
4. `*.py` files in source directories -> Python project

**TypeScript/JavaScript detection (check in order):**
1. `package.json` exists -> TypeScript/JavaScript project
2. `tsconfig.json` exists -> TypeScript project
3. `*.ts` or `*.tsx` files in source directories -> TypeScript project

If both Python and TypeScript indicators are found, prefer the one with more signals. If ambiguous, prompt the user:

```yaml
AskUserQuestion:
  questions:
    - header: "Project Type"
      question: "Both Python and TypeScript project files were detected. Which should be analyzed for coverage?"
      options:
        - label: "Python"
          description: "Analyze Python coverage with pytest-cov"
        - label: "TypeScript"
          description: "Analyze TypeScript coverage with istanbul/c8"
      multiSelect: false
```

### Detect Coverage Tool

Read the coverage patterns reference for framework-specific detection:
```
Read: ${CLAUDE_PLUGIN_ROOT}/skills/analyze-coverage/references/coverage-patterns.md
```

**Python: pytest-cov**

Check for `pytest-cov` in the following locations (stop at first match):

1. `pyproject.toml` -> look for "pytest-cov" in dependencies
2. `requirements.txt` / `requirements-dev.txt` -> look for "pytest-cov" line
3. `setup.py` / `setup.cfg` -> look for "pytest-cov" in install_requires or extras_require
4. Run `pip list 2>/dev/null | grep -i pytest-cov`

**TypeScript: istanbul / c8**

Check `package.json` for coverage tool packages:

1. `devDependencies` -> look for `c8`, `@vitest/coverage-v8`, `@vitest/coverage-istanbul`
2. `devDependencies` -> look for `jest` (Jest has built-in istanbul coverage)
3. Check if c8 binary is available: `npx c8 --version 2>/dev/null`

### Detect Test Runner

**Python:**
- `pyproject.toml` with `[tool.pytest.ini_options]` -> pytest
- `pytest.ini` or `conftest.py` exists -> pytest

**TypeScript:**
- `vitest.config.*` exists -> Vitest
- `jest.config.*` exists -> Jest
- `package.json` with `vitest` in devDependencies -> Vitest
- `package.json` with `jest` in devDependencies -> Jest

### Detect Source Package

Identify the main source package/directory to measure coverage for:

**Python:**
1. Check `pyproject.toml` `[tool.coverage.run] source` setting
2. Check `.coveragerc` `[run] source` setting
3. Look for directories containing `__init__.py`
4. Exclude `tests/`, `test/`, `docs/`, `.venv/`, `venv/`
5. If multiple candidates, prompt the user

**TypeScript:**
1. Check `vitest.config.*` or `jest.config.*` for `collectCoverageFrom` or `coverage.include`
2. Default to `src/` if it exists
3. If `src/` does not exist, look for the main directory from `package.json` `main` or `module` field
4. If ambiguous, prompt the user

### Detect Test Directories

Locate test files and directories:

**Python:**
```bash
# Find test directories
find . -type d -name "tests" -o -name "test" | head -10
# Find test files
find . -name "test_*.py" -o -name "*_test.py" | head -20
```

**TypeScript:**
```bash
# Find test files
find . -name "*.test.ts" -o -name "*.spec.ts" -o -name "*.test.tsx" -o -name "*.spec.tsx" | grep -v node_modules | head -20
```

### Handle Missing Coverage Tool

If the coverage tool is not detected:

**Python -- pytest-cov not found:**
```
Coverage tool not detected.

pytest-cov is not installed. Install it with:

  pip install pytest-cov

Or add "pytest-cov" to your dev dependencies in pyproject.toml:

  [project.optional-dependencies]
  dev = ["pytest-cov"]
```

**TypeScript -- no coverage tool found:**

For Vitest projects:
```
Coverage tool not detected.

Install the Vitest coverage provider:

  npm install -D @vitest/coverage-v8
```

For Jest projects:
```
Jest includes istanbul coverage by default. No additional installation required.
Run with: npx jest --coverage
```

After presenting the install command, stop the workflow. Do not attempt to run coverage without the tool installed.

### Handle No Test Files

If no test files are found in the project:

1. Report: `No test files detected. Coverage: 0%`
2. Recommend: `Use /generate-tests to create an initial test suite based on your source code`
3. If a spec path was provided, report ALL acceptance criteria as **untested**
4. Skip Phase 2 (Run Coverage) and Phase 3 (Parse Results) -- proceed directly to Phase 4 (Analyze Gaps) if spec provided, or Phase 5 (Generate Report) if no spec

### Handle No Source Files

If no source files are found in the project path:

```
ERROR: No source files found in {project-path}.

The directory exists but contains no files matching supported extensions
(.py, .ts, .tsx, .js, .jsx).

Check that the project path is correct, or specify it explicitly:
  /analyze-coverage /path/to/project
```

Stop the workflow after this error.

---

## Phase 2: Run Coverage

**Goal:** Execute the coverage tool and capture output.

### Build Coverage Command

Based on the detected environment, construct the appropriate coverage command.

**Python (pytest-cov):**
```bash
pytest --cov={package} --cov-report=term-missing --cov-report=json --cov-branch
```

If specific test directories were detected:
```bash
pytest {test_dirs} --cov={package} --cov-report=term-missing --cov-report=json --cov-branch
```

**TypeScript (Vitest with coverage):**
```bash
npx vitest run --coverage --coverage.reporter=json --coverage.reporter=text
```

**TypeScript (Jest):**
```bash
npx jest --coverage --coverageReporters=json --coverageReporters=text
```

**TypeScript (standalone c8):**
```bash
npx c8 --reporter=json --reporter=text npx vitest run
```

### Execute Coverage Command

Run the coverage command via Bash:

```bash
cd {project_path} && {coverage_command} 2>&1
```

Capture both stdout and stderr for analysis.

### Handle Coverage Tool Failure

If the coverage command exits with a non-zero status:

1. Check the error output for common issues:
   - **Package path not matching**: `No data was collected` -> verify `--cov={package}` matches the importable package name
   - **Module not found**: `Module X was never imported` -> check that the package is importable
   - **Missing dependencies**: Suggest `pip install` or `npm install`
   - **Configuration errors**: Point to the relevant config file

2. Report the error with diagnostic info:
```
Coverage tool failed with exit code {code}.

Error output:
{stderr}

Possible causes:
- {diagnosis based on error pattern}

Suggested fix:
- {actionable fix suggestion}
```

3. If the terminal output still contains a coverage summary (some tools return non-zero when tests fail but still produce coverage), attempt to parse it and proceed with a warning.

---

## Phase 3: Parse Results

**Goal:** Parse the JSON coverage report into structured data.

### Locate Report File

**Python (pytest-cov):**
- Default location: `coverage.json` in the project root
- Custom location: check `--cov-report=json:{path}` if specified

**TypeScript (istanbul/c8):**
- Default location: `coverage/coverage-final.json`
- Custom location: check `coverage.reportsDirectory` in vitest config or `coverageDirectory` in jest config

Read the JSON coverage report file.

### Parse Python Report (coverage.py format)

Extract from `coverage.json`:

1. **Per-file data** from the `files` object:
   - File path (key)
   - `summary.num_statements` -- total executable statements
   - `summary.covered_lines` -- statements executed during tests
   - `summary.missing_lines` -- statements not executed
   - `summary.percent_covered` -- coverage percentage (0-100)
   - `summary.num_branches` -- total branches (if branch coverage enabled)
   - `summary.covered_branches` -- branches taken during tests
   - `missing_lines` -- array of line numbers not covered

2. **Project totals** from the `totals` object:
   - `percent_covered` -- overall coverage percentage
   - `covered_lines` / `num_statements` -- line coverage ratio
   - `covered_branches` / `num_branches` -- branch coverage ratio

### Parse TypeScript Report (istanbul format)

Extract from `coverage-final.json`:

1. **Per-file data** (keys are absolute file paths):
   - Compute statement coverage: `covered = Object.values(s).filter(n => n > 0).length`, `total = Object.keys(s).length`
   - Compute branch coverage: `covered = sum of b[id].filter(n => n > 0).length`, `total = sum of b[id].length`
   - Compute function coverage: `covered = Object.values(f).filter(n => n > 0).length`, `total = Object.keys(f).length`
   - Identify uncovered lines from `statementMap` where `s[id] === 0`
   - Identify uncovered functions from `fnMap` where `f[id] === 0`

2. **Project totals**: Sum across all files

### Group Uncovered Lines into Ranges

For readable reporting, group consecutive uncovered line numbers into ranges:

- `[15, 16, 17, 22, 23]` -> `lines 15-17, 22-23`
- `[5]` -> `line 5`
- `[10, 11, 12, 13, 14, 15]` -> `lines 10-15`

### Check Against Threshold

Compare coverage against the configured threshold:

- **Threshold source (in precedence order)**:
  1. `--threshold` argument
  2. `.claude/agent-alchemy.local.md` `tdd.coverage-threshold`
  3. Default: 80%

- **Per-file check**: Flag files below the threshold, sorted by coverage (lowest first)
- **Project-wide check**: Compare overall percentage against threshold

---

## Phase 4: Analyze Gaps

**Goal:** Identify coverage gaps and, if a spec is provided, map coverage against acceptance criteria.

### Identify Coverage Gaps

From the parsed coverage data, identify:

1. **Completely uncovered files**: Files with 0% coverage -> P0 priority
2. **Uncovered functions/methods**: Functions with 0 execution count -> P1 priority
3. **Uncovered branches**: Branch paths never taken (partial coverage) -> P2 priority
4. **Files below threshold**: Files with coverage below the configured threshold but above 0% -> P3 priority

### Read Source Files for Context

For the top uncovered areas, read the source files to understand what the uncovered code does. This enables specific test suggestions rather than generic ones.

For each uncovered function or line range:
1. Read the source file
2. Identify the function name and purpose
3. Identify input parameters and return types
4. Note any error handling paths that are uncovered

### Spec-to-Coverage Mapping (if spec provided)

If `--spec <path>` was provided:

1. **Validate spec path**: Check the file exists. If not:
   ```
   WARNING: Spec file not found at {path}. Skipping spec-to-coverage mapping.
   Proceeding with coverage-only analysis.
   ```
   Skip the remainder of this section and proceed to gap suggestions.

2. **Parse the spec**: Read the spec file and extract acceptance criteria by category:
   - `_Functional:_` criteria
   - `_Edge Cases:_` criteria
   - `_Error Handling:_` criteria
   - `_Performance:_` criteria

3. **Map criteria to code**: For each acceptance criterion:
   - Use Grep to search for keywords from the criterion in the source code
   - Match function/class names that relate to the criterion's subject
   - Check comments or docstrings referencing the criterion

4. **Check coverage for mapped locations**: For each mapped criterion:
   - Look up the file in the coverage report
   - Check if the mapped lines/functions have coverage > 0
   - Classify as:
     - **TESTED**: All mapped locations have coverage > 0
     - **PARTIAL**: Some mapped locations covered, some not
     - **UNTESTED**: No mapped locations have coverage, or no code mapping found

5. **Report untested criteria**: List acceptance criteria where implementing code has no coverage

### Generate Test Suggestions

For each coverage gap, suggest a specific test to write:

- **Uncovered function**: `test_{function_name}_returns_expected_output` -- test with typical inputs
- **Uncovered branch**: `test_{function_name}_when_{condition}` -- test that triggers the untaken branch
- **Uncovered error path**: `test_{function_name}_raises_on_{error_condition}` -- test that triggers the error
- **Uncovered edge case**: `test_{function_name}_handles_{boundary}` -- test with boundary inputs

---

## Phase 5: Generate Report

**Goal:** Produce a structured markdown report summarizing coverage results.

### Report Format

```
## Coverage Analysis Report

**Project**: {project_path}
**Framework**: {pytest-cov | istanbul/c8 | vitest}
**Threshold**: {threshold}%
**Date**: {current date}

### Overall Coverage

| Metric | Value | Status |
|--------|-------|--------|
| Line Coverage | {pct}% ({covered}/{total}) | {PASS or BELOW THRESHOLD} |
| Branch Coverage | {pct}% ({covered}/{total}) | {PASS or BELOW THRESHOLD} |
| Function Coverage | {pct}% ({covered}/{total}) | {PASS or BELOW THRESHOLD or N/A} |

### Coverage by File

| File | Lines | Branches | Status |
|------|-------|----------|--------|
| {file_path} | {pct}% | {pct}% | {PASS or BELOW} |
| ... | ... | ... | ... |

Files are sorted by coverage percentage (lowest first). Only files below threshold are shown by default.

### Coverage Gaps

{For each gap, ordered by priority (P0 first):}

**{P0|P1|P2|P3}**: `{file_path}:{function_name}` ({pct}% covered)
- Uncovered lines: {line_ranges}
- Description: {what the uncovered code does}
- Suggested test: `{test_name}` -- {brief description of what to test}

{If spec provided:}
### Spec Coverage Mapping

**Spec**: {spec_path}

| Category | Criterion | Status | Code Location |
|----------|-----------|--------|---------------|
| Functional | {criterion text} | TESTED/PARTIAL/UNTESTED | {file:function} |
| Edge Cases | {criterion text} | TESTED/PARTIAL/UNTESTED | {file:function} |
| Error Handling | {criterion text} | TESTED/PARTIAL/UNTESTED | {file:function} |

**Tested**: {n}/{total} criteria
**Partially Tested**: {n}/{total} criteria
**Untested**: {n}/{total} criteria

### Summary

- Overall coverage: {pct}% ({PASS or BELOW threshold of {threshold}%})
- Files below threshold: {count}
- Critical gaps (P0): {count}
- High priority gaps (P1): {count}
{If spec:}
- Untested acceptance criteria: {count}
```

### Adapt Report to Results

- **High coverage (above threshold)**: Emphasize what is well-tested, briefly note any remaining gaps
- **Low coverage (below threshold)**: Lead with the critical gaps and prioritize recommendations
- **Zero coverage (no tests)**: Short report emphasizing the need for test creation
- **With spec mapping**: Include the Spec Coverage Mapping section
- **Without spec**: Omit the Spec Coverage Mapping section

---

## Phase 6: Suggest Next Steps

**Goal:** Provide actionable next steps based on the coverage analysis.

### Generate Recommendations

Based on the coverage analysis results, recommend specific actions:

**If coverage is below threshold:**
```
### Next Steps

1. **Generate tests for critical gaps**: Run `/generate-tests {source_file}` to auto-generate tests for uncovered areas
2. **Focus on P0 gaps first**: The following files have 0% coverage and need tests immediately:
   {list of P0 files}
3. **Run TDD cycle for new features**: Use `/tdd-cycle {feature}` to build new features test-first
```

**If coverage is above threshold:**
```
### Next Steps

1. **Coverage target met** -- {pct}% exceeds the {threshold}% threshold
2. **Optional improvements**: Consider adding tests for the remaining {count} uncovered branches
3. **Maintain coverage**: Run `/analyze-coverage` after significant changes to catch regressions
```

**If spec mapping found untested criteria:**
```
### Untested Acceptance Criteria

The following acceptance criteria from {spec_path} have no test coverage:

{For each untested criterion:}
- **{criterion}**: Generate tests with `/generate-tests {spec_path}`
```

### Cross-Skill Recommendations

Recommend other TDD tools skills when appropriate:

- **Low coverage + spec available**: `/generate-tests {spec_path}` to generate criteria-driven tests
- **Low coverage + no spec**: `/generate-tests {source_file}` to generate code-analysis tests
- **Building new features**: `/tdd-cycle {feature}` to follow RED-GREEN-REFACTOR
- **Re-analyze after changes**: `/analyze-coverage {project_path}` to verify improvements

---

## Error Handling

### Coverage Tool Not Installed

Detect the missing tool, identify the project type, and suggest the appropriate installation command. Do not attempt to run coverage without the tool installed.

### Coverage Tool Fails

If the coverage command returns a non-zero exit code:
1. Parse the error output for known patterns (see `references/coverage-patterns.md` Common Issues tables)
2. Report the error with the full output and a specific diagnosis
3. If partial results are available (terminal output contains a summary), parse and use them with a warning

### Invalid Spec Path

If `--spec` points to a file that does not exist:
1. Log a warning: `Spec file not found at {path}. Skipping spec-to-coverage mapping.`
2. Skip the spec mapping in Phase 4
3. Proceed with coverage-only analysis in Phase 5

### No Source Files Found

If the project path contains no recognizable source files:
1. Report a clear error message with the path searched
2. List the supported file extensions
3. Suggest verifying the project path

### Coverage Report File Not Found

If the JSON report file is not generated after running the coverage command:
1. Check if the terminal output contains inline coverage data
2. If terminal data exists, parse the terminal output as a fallback
3. If no data at all, report the error and suggest checking coverage tool configuration

---

## Settings

The following settings in `.claude/agent-alchemy.local.md` affect coverage analysis:

```yaml
tdd:
  framework: auto                    # auto | pytest | jest | vitest
  coverage-threshold: 80             # Minimum coverage percentage (0-100)
```

| Setting | Default | Used In |
|---------|---------|---------|
| `tdd.framework` | `auto` | Phase 1 (coverage tool selection) |
| `tdd.coverage-threshold` | `80` | Phase 3 (threshold comparison) |

The `--threshold` argument overrides the `tdd.coverage-threshold` setting.

**Error handling:**
- If the settings file does not exist, use defaults for all settings.
- If the YAML frontmatter is malformed, use defaults and log a warning.
- If `tdd.framework` is set to an unrecognized value, fall back to auto-detection.
- If `tdd.coverage-threshold` is out of range, clamp to 0-100.

See `tdd-tools/README.md` for the full settings reference.

---

## Reference Files

- `references/coverage-patterns.md` -- Framework-specific coverage tool integration: detection, commands, JSON parsing, gap analysis, spec mapping
