---
name: dead-code-eliminator
description: Identify and analyze unused or redundant code including unused functions/methods, unused variables/imports, unreachable code, and redundant conditions. Use when cleaning up codebases, improving maintainability, reducing technical debt, or conducting code quality audits. Analyzes Python code using AST analysis and produces markdown reports listing dead code locations with line numbers, severity ratings, and recommendations. Triggers when users ask to find dead code, remove unused code, identify unused imports, find unreachable code, or clean up redundant logic.
---

# Dead Code Eliminator

## Overview

Systematically identify unused or redundant code in Python codebases to improve maintainability, reduce confusion, and eliminate technical debt.

## Workflow

### 1. Understand the Scope

Define what to analyze:

**Questions to ask:**
- What directory or files should be analyzed?
- Should test files be included or excluded?
- Are there specific types of dead code to focus on?
- Should external-facing API functions be considered?

**Determine analysis scope:**
```bash
# Check project structure
ls -la

# Count Python files
find . -name "*.py" | wc -l

# Identify test directories
find . -type d -name "*test*"
```

### 2. Identify Dead Code

Use multiple detection strategies to find different types of dead code.

#### Strategy 1: Find Unused Functions

Use the bundled script for AST-based analysis:

```bash
# Scan entire project
python scripts/find_unused_functions.py /path/to/project

# Exclude specific directories
python scripts/find_unused_functions.py /path/to/project tests,venv,docs
```

**What it detects:**
- Functions defined but never called
- Methods that aren't invoked anywhere
- Async functions without callers

**Limitations:**
- Won't detect dynamically called functions (via getattr, decorators)
- May flag public API functions that are used externally
- Doesn't detect pytest fixtures or entry points

#### Strategy 2: Find Unused Imports

Use the bundled script to identify unused imports:

```bash
# Scan single file
python scripts/find_unused_imports.py /path/to/file.py

# Scan entire directory
python scripts/find_unused_imports.py /path/to/project

# Exclude directories
python scripts/find_unused_imports.py /path/to/project venv,.venv,tests
```

**What it detects:**
- Imports that are never referenced
- Unused `from X import Y` statements
- Redundant imports

#### Strategy 3: Use External Tools

Leverage Python ecosystem tools for comprehensive analysis:

**vulture** - Finds unused code:
```bash
# Install
pip install vulture

# Run on project
vulture /path/to/project

# Exclude directories
vulture /path/to/project --exclude venv,tests

# Set minimum confidence (0-100)
vulture /path/to/project --min-confidence 80
```

**autoflake** - Focuses on imports and variables:
```bash
# Install
pip install autoflake

# Check for unused imports
autoflake --check --imports /path/to/file.py

# Check unused imports and variables
autoflake --check --remove-all-unused-imports --remove-unused-variables /path/to/file.py

# Recursive scan
autoflake --check -r /path/to/project
```

**pylint** - General linting including dead code:
```bash
# Install
pip install pylint

# Check for unused variables, imports, functions
pylint /path/to/project --disable=all --enable=unused-import,unused-variable,unreachable
```

#### Strategy 4: Manual Code Review

Read the code to identify patterns:

**Unreachable code:**
- Code after `return` statements
- Code in impossible conditions
- Code after `break`, `continue`, or `raise`

**Redundant conditions:**
- Always-true or always-false checks
- Duplicate conditions
- Unnecessary `else` after `return`

**Look for:**
```bash
# Find code after return statements (basic pattern)
grep -A 3 "return" **/*.py | grep -v "^--$"

# Find functions with "old" or "legacy" in name
grep -r "def.*old\|def.*legacy" .

# Find TODO comments about removal
grep -r "TODO.*remove\|FIXME.*delete" .
```

### 3. Categorize Findings

Organize dead code by type and priority.

See [dead-code-patterns.md](references/dead-code-patterns.md) for comprehensive pattern catalog.

#### Category: Unused Imports

**Priority:** High (easy to remove, low risk)

**Examples:**
- `import os` but os is never used
- `from typing import List, Dict` but only `List` is used
- Duplicate imports

#### Category: Unused Functions/Methods

**Priority:** Medium to High

**Subcategories:**
- **Orphaned helpers:** Utility functions never called
- **Refactoring leftovers:** Old implementations not removed
- **Test helpers:** Test utilities not used by any test

**Caution - May be intentional:**
- Public API functions (used externally)
- Plugin/hook functions (called dynamically)
- CLI entry points (called from command line)

#### Category: Unreachable Code

**Priority:** High (indicates bugs or confusion)

**Examples:**
- Code after `return`
- Code in impossible conditions
- Code after `raise`

#### Category: Redundant Code

**Priority:** Medium

**Examples:**
- Redundant boolean checks
- Unnecessary `else` after `return`
- Duplicate logic in multiple places

#### Category: Unused Variables

**Priority:** Low to Medium

**Examples:**
- Assigned but never read
- Function parameters never used
- Loop variables never referenced

### 4. Verify Findings

Before reporting, verify that identified code is truly dead.

**Check for dynamic usage:**
```python
# Code may appear unused but is called dynamically
handlers = {
    'process': process_handler,  # Looks unused but isn't
}

# Or via getattr
handler = getattr(module, function_name)
```

**Check for external usage:**
- Is this a public API function?
- Is it documented in README or API docs?
- Is it an entry point in setup.py?

**Check for framework conventions:**
```python
# Django signal handlers
@receiver(post_save, sender=User)
def user_saved(sender, instance, **kwargs):  # May appear unused
    pass

# Pytest fixtures
@pytest.fixture
def sample_data():  # Used by tests but not "called" directly
    return {"key": "value"}
```

**Verify with grep:**
```bash
# Search for function name in entire codebase
grep -r "function_name" .

# Search in quotes (dynamic calls)
grep -r "'function_name'\|\"function_name\"" .

# Search in setup.py or config files
grep -r "function_name" setup.py pyproject.toml
```

### 5. Generate Report

Create a structured markdown report of findings.

## Dead Code Analysis Report

**Project:** [Project Name]
**Analyzed:** [Date]
**Scope:** [Directories analyzed]
**Excluded:** [Excluded directories]

---

## Summary

- **Unused imports:** X findings across Y files
- **Unused functions:** A findings across B files
- **Unreachable code:** M findings
- **Redundant code:** N findings

**Total:** Z dead code instances found

---

## 🔴 High Priority Issues

### Unreachable Code

Code that can never execute - should be removed immediately.

#### Issue 1: Code After Return

**Location:** `src/utils.py:45-47`

**Code:**
```python
def process_data(data):
    if not data:
        return None
        logging.warning("Empty data")  # UNREACHABLE
        validate(data)  # UNREACHABLE
```

**Recommendation:** Remove lines 46-47 (unreachable after return).

**Impact:** Misleading code that suggests validation happens but doesn't.

---

### Unused Imports

#### File: `src/main.py`

**Lines:**
- Line 3: `import os` (unused)
- Line 5: `from typing import Dict, Tuple` (only `Dict` is used)
- Line 12: `import re` (unused)

**Recommendation:** Remove unused imports. Update line 5 to `from typing import Dict`.

---

## 🟡 Medium Priority Issues

### Unused Functions

Functions that appear unused but should be verified before removal.

#### Issue 3: Orphaned Helper Function

**Location:** `src/helpers.py:89`

**Function:** `format_timestamp(ts: int) -> str`

**Analysis:**
- Defined but never called in codebase
- Not in public API documentation
- Not an entry point

**Verification needed:**
- ✅ Checked: Not in setup.py entry_points
- ✅ Checked: Not mentioned in README
- ✅ Checked: No string references in codebase
- ❌ **Need to verify:** Could this be used by external code?

**Recommendation:** If not part of public API, remove. Otherwise, document it.

---

#### Issue 4: Duplicate Logic

**Locations:**
- `src/processor_a.py:45-52`
- `src/processor_b.py:78-85`

**Code:** Both files contain identical validation logic.

**Recommendation:** Extract common logic into shared utility function.

**Impact:** Maintenance burden - changes must be duplicated.

---

## 🔵 Low Priority Issues

### Redundant Code

#### Issue 5: Unnecessary Else After Return

**Location:** `src/validator.py:123-127`

**Code:**
```python
def check_status(value):
    if value > 0:
        return "positive"
    else:  # Unnecessary
        return "negative"
```

**Recommendation:** Remove `else` clause (implicit after return).

**Impact:** Minor - slightly less readable but no functional impact.

---

#### Issue 6: Unused Variable

**Location:** `src/calculator.py:56`

**Code:**
```python
def compute(a, b):
    total = a + b  # Assigned but never used
    return a * b
```

**Recommendation:** Remove unused `total` variable.

---

## ⚪ Needs Verification

### Potentially Used Dynamically

These appear unused but may be called dynamically. Manual verification needed.

#### Function: `handle_create()`

**Location:** `src/handlers.py:34`

**Reason for caution:** File contains handler registry suggesting dynamic dispatch.

**Code pattern:**
```python
HANDLERS = {
    'create': handle_create,
    'update': handle_update,
}
```

**Recommendation:** Verify this is registered and used. If confirmed unused, remove.

---

## Recommendations

### Immediate Actions (High Priority)

1. Remove unreachable code (Issue 1)
2. Clean up unused imports across all files
3. Verify and remove orphaned helper functions

### Short-term Actions (Medium Priority)

4. Extract duplicate logic into shared utilities
5. Verify dynamically-called functions
6. Remove confirmed unused functions

### Long-term Actions (Low Priority)

7. Simplify redundant conditions
8. Remove unused variables
9. Establish linting rules to prevent future dead code

### Prevention

**Add to CI/CD pipeline:**
```bash
# Add to pre-commit hook or CI
vulture src/ --min-confidence 80
autoflake --check -r src/
```

**Configure IDE:**
- Enable unused import warnings
- Configure pylint/flake8 for dead code detection

**Code review checklist:**
- [ ] No unused imports?
- [ ] No unreachable code?
- [ ] No unused variables?
- [ ] Functions have callers?

---

## Detailed Findings

[If needed, include full lists of all findings organized by file]

---

### 6. Present Findings

Share the report with the team and get feedback.

**Present clearly:**
- Start with summary statistics
- Highlight high-priority issues first
- Provide specific locations and recommendations
- Separate definite dead code from "needs verification"

**Be cautious about:**
- Public API functions that may be used externally
- Dynamic dispatch patterns
- Framework-specific code (decorators, fixtures, signals)
- CLI entry points
- Plugin systems

**Request feedback:**
- "Are these functions part of the public API?"
- "Is this code used by external tools or scripts?"
- "Should we keep this for planned features?"

## Tips for Effective Dead Code Analysis

**Start conservatively:**
- Focus on obvious cases first (unused imports, unreachable code)
- Be cautious with unused functions (may be called externally)
- Verify before removing

**Use multiple detection methods:**
- AST-based analysis (bundled scripts)
- External tools (vulture, autoflake, pylint)
- Manual code review
- Coverage analysis (find untested code)

**Prioritize by risk:**
- **Low risk:** Unused imports, unused variables
- **Medium risk:** Unused internal functions, redundant code
- **Higher risk:** Functions that might be public API

**Consider the context:**
- Age of code (old = more likely truly dead)
- Recent refactoring (may be leftovers)
- Project type (library vs application)
- Team size (more people = more likely to have external usage)

**Prevention is better than cure:**
- Enable linting in CI/CD
- Configure IDE warnings
- Code review checklist
- Regular dead code audits

## Common False Positives

Be aware of code that appears dead but isn't:

**1. Dynamic dispatch:**
```python
handler = getattr(module, f"handle_{action}")
```

**2. Entry points:**
```python
# setup.py
entry_points={
    'console_scripts': ['tool=module:main_function']
}
```

**3. Pytest fixtures:**
```python
@pytest.fixture
def sample_data():  # Used by tests implicitly
    return data
```

**4. Django signals:**
```python
@receiver(post_save, sender=Model)
def handle_save(sender, instance, **kwargs):  # Called by framework
    pass
```

**5. Decorators and metaclasses:**
```python
class Meta:
    def __init_subclass__(cls):  # Called implicitly
        register(cls)
```

**6. Public API functions:**
```python
# In library code - may be used by external code
def public_function():  # Appears unused internally
    pass
```

## Reference

For comprehensive dead code patterns and detection strategies, see [dead-code-patterns.md](references/dead-code-patterns.md).
