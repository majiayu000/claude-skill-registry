---
name: quality-fixer
description: Automatically apply safe quality fixes including formatting (Black, isort), linting (Ruff auto-fixes), and resolve formatter conflicts. Use when quality checks fail or before committing code.
---

# Quality Fix Applier

## ⚠️ MANDATORY: Read Project Documentation First

**BEFORE applying quality fixes, you MUST read and understand the following project documentation:**

### Core Project Documentation

1. **README.md** - Project overview, features, and getting started
2. **AI_DOCS/project-context.md** - Tech stack, architecture, development workflow
3. **AI_DOCS/code-conventions.md** - Code style, formatting, best practices
4. **AI_DOCS/tdd-workflow.md** - TDD process, testing standards, coverage requirements

### Session Context (if available)

5. **.ai-context/ACTIVE_TASKS.md** - Current tasks and priorities
6. **.ai-context/CONVENTIONS.md** - Project-specific conventions
7. **.ai-context/RECENT_DECISIONS.md** - Recent architectural decisions
8. **.ai-context/LAST_SESSION_SUMMARY.md** - Previous session summary

### Additional AI Documentation

9. **AI_DOCS/ai-tools.md** - Session management workflow
10. **AI_DOCS/ai-skills.md** - Other specialized skills/agents available

### Why This Matters

- **Tool Configuration**: Understand which formatters and linters are configured
- **Code Standards**: Apply fixes that align with project conventions
- **Safety Rules**: Know which auto-fixes are safe vs. require manual review
- **Integration**: Coordinate with other quality tools (Black, Ruff, isort)

**After reading these files, proceed with your quality fixing task below.**

---

## Overview

Automatically apply safe quality fixes to Python code, resolving formatting issues, linting problems, and formatter conflicts.

## When to Use

- After writing code, before running `make check`
- When `make lint` or `make format` reports fixable issues
- To resolve Black vs Ruff formatter conflicts
- Before committing code to ensure quality gates pass
- When you want to apply all safe, automatic fixes

## What This Skill Fixes

✅ **Formatting Issues**
- Black code formatting
- isort import sorting
- Line length adjustments
- Whitespace normalization

✅ **Linting Issues (Safe Auto-Fixes)**
- Unused imports removal
- Unused variables (when safe)
- F-string conversion
- Simplifiable if statements
- List/dict comprehension improvements

✅ **Type Hint Issues (Safe Cases)**
- Add `-> None` to functions without return
- Add obvious type hints (str, int, bool literals)
- Fix Ellipsis in stub signatures

✅ **Formatter Conflicts**
- Black vs Ruff disagreements
- Message variable extraction for long strings
- Line break adjustments

## Usage Examples

### Fix All Issues in Project

```bash
# Run comprehensive quality fixes
apply quality fixes to the entire project
```

**Actions:**
1. Run `make format` (Black + isort)
2. Run Ruff with `--fix` flag
3. Check for and resolve formatter conflicts
4. Report what was fixed

### Fix Specific File

```bash
# Fix a single file
fix quality issues in src/{{ package_name }}/validators.py
```

**Actions:**
1. Format the specific file
2. Apply Ruff fixes to that file
3. Verify no conflicts introduced
4. Show diff of changes

### Resolve Formatter Conflicts Only

```bash
# Focus on conflicts
resolve Black and Ruff formatter conflicts
```

**Actions:**
1. Run both formatters
2. Identify lines where they disagree
3. Apply conflict resolution strategies
4. Verify both are satisfied

### Preview Mode (Dry Run)

```bash
# See what would be fixed without applying
preview quality fixes for src/
```

**Actions:**
1. Run all checks in dry-run mode
2. Show what would be changed
3. Ask for confirmation before applying

## Step-by-Step Process

### Step 1: Run Formatting

```bash
# Apply Black formatting
make format

# This runs:
# - black src/ tests/
# - isort src/ tests/
```

**What gets fixed:**
- Code style (spacing, indentation, quotes)
- Import organization and grouping
- Line length compliance (88 characters)

### Step 2: Apply Ruff Auto-Fixes

```bash
# Run Ruff with auto-fix
uv run ruff check --fix src/ tests/

# Safe fixes include:
# - Remove unused imports
# - Remove unused variables (when safe)
# - F-string conversion
# - Simplify expressions
```

**What gets fixed:**
- Import cleanup
- Code simplification
- Modern Python idioms

### Step 3: Detect Formatter Conflicts

```bash
# Check if Black and Ruff agree
make format && make lint
```

**Common conflicts:**
- Long string literals exceeding line length
- Complex expressions needing line breaks
- Comment placement differences

### Step 4: Resolve Conflicts

**Strategy 1: Extract Message Variables**

```python
# Before (conflict - too long)
logger.error("This is a very long error message that exceeds the line length limit")

# After (resolved)
msg = "This is a very long error message that exceeds the line length limit"
logger.error(msg)
```

**Strategy 2: Use Parentheses for Line Breaks**

```python
# Before (conflict)
result = some_function(arg1, arg2, arg3, arg4, arg5, arg6)

# After (resolved)
result = some_function(
    arg1, arg2, arg3, arg4, arg5, arg6
)
```

**Strategy 3: Split Long Strings**

```python
# Before (conflict)
text = "This is a very long string that should be split across multiple lines for readability"

# After (resolved)
text = (
    "This is a very long string that should be "
    "split across multiple lines for readability"
)
```

### Step 5: Verify Fixes

```bash
# Run complete quality check
make check
```

**Must pass:**
- ✅ Format (Black + isort)
- ✅ Lint (Ruff + Pylint + mypy)
- ✅ Tests (pytest)
- ✅ Security (Bandit)

## Conflict Resolution Strategies

### Identifying Conflicts

Run both tools and compare:

```bash
# Apply Black
black src/{{ package_name }}/module.py

# Check Ruff
ruff check src/{{ package_name }}/module.py

# If Ruff still complains about formatting, there's a conflict
```

### Resolution Decision Tree

1. **Long String Literals**
   → Extract to variable or split across lines

2. **Complex Expressions**
   → Add parentheses and line breaks

3. **Long Function Calls**
   → Break arguments to multiple lines

4. **Comment Placement**
   → Move comments above the line

5. **Type Annotation Complexity**
   → Split to multiple lines with proper indentation

### Example: Resolving Long String Conflict

**Problem:**

```python
# Black formats this way:
raise ValueError("The email address provided is not valid because it does not contain the required @ symbol")

# Ruff complains: E501 Line too long (92 > 88)
```

**Solution:**

```python
# Extract message variable
error_msg = (
    "The email address provided is not valid because it "
    "does not contain the required @ symbol"
)
raise ValueError(error_msg)

# Both Black and Ruff are satisfied!
```

## What This Skill Does NOT Fix

❌ **Complex Logic Issues**
- Algorithm problems
- Business logic errors
- Design flaws

❌ **Non-Obvious Type Hints**
- Complex generic types
- Union types requiring domain knowledge
- Custom type aliases

❌ **Docstring Content**
- Will format docstrings
- Won't write missing docstrings
- Won't improve docstring quality

❌ **Test Failures**
- Only fixes code style
- Doesn't fix failing tests
- Doesn't add missing tests

❌ **Breaking Changes**
- Only applies safe, non-breaking fixes
- Won't remove used variables
- Won't change semantics

## Output Format

After applying fixes, provide a report:

```markdown
## Quality Fixes Applied

**Files Modified:** X
**Total Changes:** X lines

### Formatting Fixes
- ✅ Applied Black formatting to X files
- ✅ Sorted imports with isort in X files
- ✅ Fixed line length issues: X lines

### Linting Fixes
- ✅ Removed X unused imports
- ✅ Converted X strings to f-strings
- ✅ Simplified X expressions
- ✅ Fixed X Ruff issues

### Conflicts Resolved
- ✅ Extracted X message variables
- ✅ Split X long strings
- ✅ Reformatted X function calls

### Quality Check Results
```bash
make check
```
[Show output]

### Files Changed
1. src/{{ package_name }}/module1.py (+12, -8)
2. src/{{ package_name }}/module2.py (+5, -3)
3. tests/test_module.py (+3, -2)

### Next Steps
- Review changes with `git diff`
- Run tests to ensure no breaking changes: `make test`
- Commit changes if satisfied
```

## Safety Features

### Dry Run Mode

Always available for preview:

```bash
# Format preview
black --check --diff src/

# Ruff preview
ruff check --fix --diff src/
```

### Git Integration

Verify changes before committing:

```bash
# See what changed
git diff

# Stage specific changes
git add -p
```

### Backup Strategy

For large fixes, create a commit first:

```bash
# Commit current state
git commit -m "Before quality fixes"

# Apply fixes
[quality-fixer runs]

# Review changes
git diff HEAD~1

# Undo if needed
git reset --hard HEAD~1
```

## Integration with Project Tools

### Makefile Integration

```bash
# Just formatting
make format

# Just linting (with fixes)
make lint

# Complete check (no auto-fix)
make check
```

### Pre-Commit Integration

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: quality-fixer
      name: Quality Fixer
      entry: python .claude/skills/quality-fixer/scripts/auto_fix.py
      language: system
      types: [python]
```

### CI Integration

Run in CI with `--check` mode:

```bash
# CI should verify, not fix
make check

# If it fails, developers run:
[quality-fixer to fix locally]
```

## Advanced Features

### Selective Fixing

Fix only specific types of issues:

```bash
# Only formatting
[quality-fixer] --format-only

# Only import cleanup
[quality-fixer] --imports-only

# Only conflicts
[quality-fixer] --conflicts-only
```

### Ignore Patterns

Respect configuration in `pyproject.toml`:

```toml
[tool.ruff.lint]
ignore = ["E501"]  # Don't auto-fix line length in specific cases

[tool.black]
extend-exclude = '''
/(
  | generated
)/
'''
```

### Custom Rules

Define project-specific fixes:

```python
# .claude/skills/quality-fixer/scripts/custom_rules.py

def fix_common_typos(code: str) -> str:
    """Fix project-specific common mistakes."""
    fixes = {
        "recieve": "receive",
        "seperator": "separator",
    }
    for typo, correction in fixes.items():
        code = code.replace(typo, correction)
    return code
```

## Best Practices

1. **Run before committing** - Always clean up code before commits
2. **Review changes** - Don't blindly accept all fixes, use `git diff`
3. **Test after fixing** - Run `make test` to ensure no breaking changes
4. **Fix iteratively** - Start with formatting, then linting, then conflicts
5. **Understand the changes** - Learn from fixes to avoid future issues

## Common Scenarios

### Scenario 1: Before Committing

```bash
# 1. Apply fixes
[quality-fixer]

# 2. Review changes
git diff

# 3. Test
make test

# 4. Commit
git add .
git commit -m "feat: add new feature"
```

### Scenario 2: After Code Review

```bash
# Code reviewer says: "Fix formatting and linting"

# 1. Apply fixes
[quality-fixer]

# 2. Verify all issues resolved
make check

# 3. Push
git push
```

### Scenario 3: CI Failure

```bash
# CI reports quality issues

# 1. Pull latest
git pull

# 2. Apply fixes
[quality-fixer]

# 3. Verify locally
make check

# 4. Push fix
git commit -am "fix: resolve quality issues"
git push
```

## Troubleshooting

### "Black and Ruff still conflict after fix"

**Solution:** Manually review the conflicting lines and apply advanced strategies:
- Extract complex expressions to variables
- Restructure the code for better formatting
- Use `# noqa` comments sparingly for unavoidable cases

### "Auto-fix broke my tests"

**Solution:**
- Revert with `git checkout -- <file>`
- Review what was changed with `git diff`
- Apply fixes more selectively
- Report if a fix is unsafe (should not be applied)

### "Pylint still reports issues"

**Note:** This skill only applies auto-fixable issues. Pylint often requires manual fixes:
- Unused arguments → Use `_` prefix or remove
- Too many arguments → Refactor function
- Too complex → Simplify logic

## Remember

**Quality fixes are TOOLS, not SUBSTITUTES for good code:**
- Write clean code from the start
- Understand why formatters want changes
- Learn from the fixes applied
- Don't rely on auto-fix for everything

This skill helps you maintain code quality efficiently, but **good coding practices are still essential**!
