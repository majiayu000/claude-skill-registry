---
name: coverage
description: Run test coverage analysis, identify missed and partial lines, and write tests to improve coverage. Use this when the user asks to check coverage, improve coverage, or write tests for uncovered code. This skill detects both completely missed lines and partially covered lines (executed but missing branch coverage) to match Codecov analysis.
---

# Coverage Analysis and Improvement

This skill guides you through analyzing test coverage and systematically improving it by writing targeted tests.

## Key Concepts

### Coverage Types
- **Missed lines**: Code that was never executed during tests (hits == 0)
- **Partial lines**: Code that executed but didn't take all branch paths (e.g., only the `if` branch was tested, not the `else`)

### Why Partial Lines Matter
Traditional `coverage annotate` cannot detect partial lines. This skill uses XML-based analysis to match what Codecov shows, ensuring agents can target the same gaps that appear in PR reviews.

## Workflow

### Step 1: Run Tests with Coverage

Generate coverage XML report with branch coverage enabled:

```bash
uv run pytest -q --maxfail=1 \
  --cov=sleap_io --cov-branch \
  --cov-report=xml:coverage.xml
```

This creates `coverage.xml` with full branch coverage data.

### Step 2: Analyze Coverage

Use the bundled script to summarize coverage gaps. The script is located at `.claude/skills/coverage/scripts/cov_summary.py` within this skill.

#### Show all uncovered lines (full project)
```bash
uv run python scripts/cov_summary.py --source coverage.xml --format md
```

#### Show only PR-changed lines (recommended)
```bash
uv run python scripts/cov_summary.py --source coverage.xml --only-pr-diff-lines --format md
```

#### Show only changed files vs main
```bash
uv run python scripts/cov_summary.py --source coverage.xml --only-changed --format md
```

### Step 3: Interpret Results

The output shows a table with:
- **File**: Module path
- **Missed**: Line ranges that were never executed
- **Partial**: Line ranges that executed but missed some branches

Example output:
```markdown
| File | Missed | Partial |
| --- | --- | --- |
| io/coco.py | 122-124,518 | 82,84,87,121,279 |
| io/leap.py | — | 105,109,148 |
```

This means:
- `io/coco.py` lines 122-124, 518 were never executed
- `io/coco.py` lines 82, 84, 87, 121, 279 executed but didn't cover all branches
- `io/leap.py` has no missed lines, but lines 105, 109, 148 need branch coverage

### Step 4: Read the Source Code

For each file with gaps:

```bash
# Read the specific file to understand the uncovered code
Read io/coco.py
```

Focus on the line numbers from the coverage report. Look for:
- **Missed lines**: Why wasn't this code executed? Is it an edge case? Error handling?
- **Partial lines**: What branches exist? Usually `if/else`, `and/or`, `try/except`, ternary operators

### Step 5: Write Targeted Tests

For each gap identified:

1. **Determine what conditions trigger the uncovered code**
   - Read the function/method containing the gap
   - Identify what inputs or state would execute that path

2. **Find or create appropriate test fixtures**
   - Check `tests/fixtures/` for existing data
   - Create minimal synthetic data if needed

3. **Write focused tests**
   - One test per distinct code path
   - Use descriptive test names explaining what's being covered
   - Add comments referencing the coverage gap (e.g., `# Covers line 122: error handling for invalid input`)

4. **Verify improvement**
   - Re-run coverage after adding tests
   - Confirm the lines are no longer in the gap report

## Examples

### Example 1: Covering Missed Lines

**Coverage report shows:**
```
io/slp.py | 1134,1244 | —
```

**Action:**
1. Read `io/slp.py` lines around 1134 and 1244
2. Discover they're error handling for corrupt files
3. Write test: `test_load_corrupt_slp_file_raises_error()`
4. Create a minimal corrupt SLP file fixture
5. Re-run coverage to verify

### Example 2: Covering Partial Lines

**Coverage report shows:**
```
model/labels.py | — | 338,376,550
```

**Action:**
1. Read `model/labels.py` line 338:
   ```python
   if video_path and video_path.exists():
   ```
2. Current tests only cover the case where the condition is True
3. Write test: `test_labels_with_missing_video_path()`
4. Ensure `video_path` is None or doesn't exist
5. Re-run coverage to verify

### Example 3: PR-Focused Coverage

When working on a PR, focus only on lines you changed:

```bash
# 1. Run coverage
uv run pytest -q --maxfail=1 --cov=sleap_io --cov-branch --cov-report=xml:coverage.xml

# 2. Filter to PR lines only
uv run python scripts/cov_summary.py --source coverage.xml --only-pr-diff-lines --format md
```

If output shows:
```
✅ No uncovered lines found.
```

Great! Your PR has full coverage of all new/modified lines.

## Best Practices

### Do:
- ✅ Focus on PR-changed lines first (`--only-pr-diff-lines`)
- ✅ Write multiple small focused tests rather than one large test
- ✅ Test both success and failure cases
- ✅ Use existing fixtures when available
- ✅ Add comments linking tests to coverage gaps they address

### Don't:
- ❌ Ignore partial lines—they're as important as missed lines
- ❌ Write tests that mock away the actual behavior (see CLAUDE.md rule #9)
- ❌ Create tests for unreachable defensive code (re-evaluate if it should exist)
- ❌ Batch multiple coverage gaps into one test (makes debugging harder)

## Output Formats

The script supports multiple formats:

- `--format text`: Simple list (default)
- `--format md`: Markdown table (recommended for readability)
- `--format json`: Machine-readable with detailed branch info
- `--format gh-annotations`: GitHub workflow annotations

## Troubleshooting

### "No coverage.xml found"
Run the pytest command with `--cov-report=xml:coverage.xml`

### "GitHub CLI not found" warning
The `--only-pr-diff-lines` option requires `gh` CLI. Install with `brew install gh` or use `--only-changed` instead.

### Paths don't match
Ensure `relative_files = true` is set in `[tool.coverage.run]` section of `pyproject.toml`

## Integration with CI

The coverage workflow is integrated into CI at `.github/workflows/ci.yml`. On PRs, GitHub Actions automatically:
1. Runs tests with coverage XML generation
2. Uploads to Codecov
3. Adds a summary comment showing missed and partial lines for PR-changed files

## References

- Coverage script source: `.claude/skills/coverage/scripts/cov_summary.py`
- Coverage command: `.claude/commands/coverage.md`
- Main script location: `scripts/cov_summary.py`
- Coverage config: `pyproject.toml` `[tool.coverage.*]` sections
