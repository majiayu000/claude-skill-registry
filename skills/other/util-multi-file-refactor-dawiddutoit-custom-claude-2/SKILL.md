---
name: util-multi-file-refactor
description: Optimizes multi-file refactoring workflows by enforcing token-efficient MultiEdit usage (30-50% savings), coordinating changes across files, validating imports/references, and running quality gates. Use when refactoring patterns across codebase, renaming functions/classes/variables, extracting common code, moving functionality, or updating patterns in multiple files. Prevents sequential Edit anti-patterns.
allowed-tools:
  - Read
  - Edit
  - MultiEdit
  - Grep
  - Glob
  - Bash
---

# Multi-File Refactor

## Quick Start

Systematic, token-efficient multi-file refactoring with safety checks. Enforces MultiEdit for 2+ changes per file (30-50% token savings vs sequential Edit).

**Most common use case:**
```
User: "Rename function search_code to find_code across the codebase"

→ Discover all occurrences (Grep)
→ Plan changes (group by file)
→ Execute with MultiEdit (2+ changes per file)
→ Update imports/references
→ Validate (run tests, quality gates)

Result: Clean refactor with no broken references
```

## When to Use This Skill

**Primary triggers:**
- "Rename function/class/variable across codebase"
- "Refactor pattern X to pattern Y"
- "Extract common code to shared module"
- "Move functionality from A to B"
- "Update all usages of X"

**Contextual triggers (agent detection):**
- Multiple files need same change
- Function/class used in 3+ files
- Pattern repeats across modules
- Cross-file dependency changes

**When NOT to use:**
- Single file changes (use Edit directly)
- Simple find-replace (use Edit with replace_all)
- Trivial changes (1-2 total edits)

## What This Skill Does

**Core capabilities:**

1. **Discovery & Analysis** - Find all affected files using Grep/Glob
2. **Change Planning** - Group changes by file, identify dependencies
3. **Token-Efficient Execution** - Use MultiEdit for 2+ changes (30-50% savings)
4. **Import/Reference Updates** - Fix broken imports and references
5. **Validation** - Run tests and quality gates
6. **Reporting** - Document changes and validation results

## Refactoring Workflow

### Phase 1: Discovery & Analysis

**Find all affected files:**
```bash
# Search for function/class usage
grep -r "search_code" src/ --include="*.py"

# Or use Grep tool
pattern: "search_code"
path: src/
output_mode: files_with_matches
```

**Analyze impact:**
- Count occurrences per file
- Identify import statements
- Find documentation references
- Check test files

### Phase 2: Change Planning

**Group changes by file:**
```
File: src/handlers.py (3 changes) - USE MULTIEDIT
File: src/repository.py (2 changes) - USE MULTIEDIT
File: tests/test_search.py (5 changes) - USE MULTIEDIT
File: README.md (1 change) - USE EDIT
```

**Determine execution order:**
1. Core implementation files first
2. Dependent files next
3. Tests last
4. Documentation last

### Phase 3: Execution

**Token optimization rules:**

**Rule 1: ALWAYS Use MultiEdit for 2+ Edits**
```python
# ❌ BAD: Sequential Edit (wastes tokens)
Edit(file="handlers.py", old_string="search_code(query)", new_string="find_code(query)")
Edit(file="handlers.py", old_string="def search_code", new_string="def find_code")
Edit(file="handlers.py", old_string="search_code_handler", new_string="find_code_handler")

# ✅ GOOD: Single MultiEdit (30-50% token savings)
MultiEdit(file="handlers.py", edits=[
    {"old_string": "search_code(query)", "new_string": "find_code(query)"},
    {"old_string": "def search_code", "new_string": "def find_code"},
    {"old_string": "search_code_handler", "new_string": "find_code_handler"}
])
```

**Rule 2: Group Changes by File**
- One MultiEdit call per file
- Include ALL changes for that file
- Read file first to verify changes

**Rule 3: Read Before Modifying**
```python
# Always read first
Read(file_path="src/handlers.py")

# Then modify
MultiEdit(file="src/handlers.py", edits=[...])
```

**Rule 4: Batch Independent Operations**
- Run Read calls in parallel
- Run MultiEdit calls in parallel (if files independent)
- Run validation commands sequentially

### Phase 4: Import & Reference Updates

**Update import statements:**
```python
# If function moved or renamed
# OLD: from src.handlers import search_code
# NEW: from src.handlers import find_code

MultiEdit(file="src/app.py", edits=[
    {"old_string": "from src.handlers import search_code",
     "new_string": "from src.handlers import find_code"}
])
```

**Check for broken references:**
```bash
# Verify old name doesn't exist
grep -r "search_code" src/ --include="*.py"

# Should return empty or only comments/strings
```

### Phase 5: Validation

**Run quality gates:**
```bash
# Type checking
mypy src/

# Linting
ruff check src/

# Tests
pytest tests/

# All must pass before considering refactor complete
```

**Manual verification:**
- Test in running application
- Check logs for errors
- Verify documentation updated

### Phase 6: Reporting

**Generate refactor report:**
```
## Refactor Report: search_code → find_code

### Files Modified: 8
- src/handlers.py (3 changes)
- src/repository.py (2 changes)
- src/models.py (1 change)
- tests/test_search.py (5 changes)
- tests/test_repository.py (2 changes)
- tests/conftest.py (1 change)
- README.md (1 change)
- docs/API.md (1 change)

### Changes Made:
- Function renamed: search_code → find_code
- Imports updated: 6 files
- Tests updated: 3 files
- Documentation updated: 2 files

### Validation:
✅ mypy: 0 type errors
✅ ruff: 0 linting errors
✅ pytest: 42/42 tests passing
✅ grep verification: No old references found

Status: COMPLETE
```

## Common Refactoring Patterns

### Pattern 1: Function/Method Rename

```python
# 1. Find all usages
grep -r "old_function_name" src/

# 2. Plan changes (group by file)
# 3. Execute with MultiEdit per file
# 4. Update imports
# 5. Run tests
```

### Pattern 2: Class Rename

```python
# Additional considerations:
# - Update class definition
# - Update all instantiations
# - Update type hints
# - Update docstrings
# - Update imports
```

### Pattern 3: Module/File Move

```python
# 1. Move file: mv old/path.py new/path.py
# 2. Update all imports referencing old path
# 3. Update relative imports in moved file
# 4. Run tests
```

### Pattern 4: Extract Common Code

```python
# 1. Create new shared module
# 2. Move common code to new module
# 3. Update original files to import from new module
# 4. Remove duplicate code
# 5. Run tests
```

### Pattern 5: API Signature Change

```python
# Example: Add parameter to function
# 1. Update function definition
# 2. Update all call sites (add new parameter)
# 3. Update tests
# 4. Update documentation
```

## Language-Specific Guidance

### Python
- Update `__init__.py` imports
- Fix relative imports (from . import X)
- Update type hints
- Check for dynamic imports (importlib)

### JavaScript/TypeScript
- Update named imports: `import { oldName } from 'module'`
- Update default imports: `import oldName from 'module'`
- Update require statements: `const oldName = require('module')`
- Update type definitions (.d.ts files)

### Java
- Update package imports
- Update fully qualified names
- Rebuild project (Maven/Gradle)
- Update XML configuration files

### Go
- Update package imports
- Run `go mod tidy`
- Update interface implementations
- Run `go build`

## Validation Checklist

After refactoring, verify:

- [ ] All quality gates passing (mypy, ruff, pytest)
- [ ] No grep results for old name (except comments/strings if intended)
- [ ] All imports updated
- [ ] Tests passing (unit, integration, E2E)
- [ ] Documentation updated (README, API docs)
- [ ] No broken references in other files
- [ ] Application runs without errors
- [ ] Logs show no warnings/errors

## Anti-Patterns to Avoid

1. **Sequential Edit on Same File** - Use MultiEdit for 2+ changes (30-50% token savings)
2. **Blind Editing Without Reading** - Always Read file first to verify context
3. **Skipping Tests** - Tests catch broken references immediately
4. **Ignoring Quality Gates** - Type errors indicate missed references
5. **Forgetting Imports** - Broken imports cause runtime errors
6. **Incomplete Refactoring** - Leaving old name in some files creates confusion
7. **Wrong Dependency Order** - Update core files before dependent files

## Edge Cases & Troubleshooting

### Pattern in Strings/Comments

**Issue:** Grep finds occurrences in strings/comments that shouldn't be changed

**Solution:**
- Review grep results manually
- Exclude string/comment matches from changes
- Use more specific search patterns (e.g., `def search_code` instead of just `search_code`)

### Partial Matches

**Issue:** "search_code" also matches "search_code_advanced"

**Solution:**
- Use word boundaries in grep: `\bsearch_code\b`
- Review all matches before changing
- Use more specific old_string in Edit/MultiEdit

### Tests Failing After Refactor

**Issue:** Tests fail with "NameError" or "ImportError"

**Diagnosis:**
```bash
# Check for old references
grep -r "old_name" tests/

# Check import statements
grep -r "from.*import.*old_name" tests/
```

**Solution:**
- Update test imports
- Update test fixture names
- Update mock/patch references

### MultiEdit Conflicts

**Issue:** MultiEdit fails with "overlapping edits" or "string not found"

**Diagnosis:**
- Edits are in wrong order
- String changed between Read and MultiEdit
- old_string not unique

**Solution:**
- Ensure old_strings are unique
- Order edits top-to-bottom in file
- Re-read file if it changed

## Expected Outcomes

### Successful Refactor

```
## Refactor Complete

Files Modified: 12
Total Changes: 37
Token Efficiency: 45% savings (MultiEdit vs Edit)

Validation:
✅ Type checking: 0 errors
✅ Linting: 0 issues
✅ Tests: 87/87 passing
✅ Verification: No old references

Status: READY TO COMMIT
```

### Failed Validation

```
## Refactor Failed Validation

Files Modified: 12
Total Changes: 37

Validation:
❌ Tests: 3 failures
  - test_search_handler: ImportError: cannot import 'search_code'
  - test_repository: NameError: 'search_code' not defined
❌ Grep verification: 2 old references found
  - src/cache.py:45: search_code_cache
  - tests/conftest.py:12: mock_search_code

Action Required:
1. Fix remaining imports in test files
2. Update cache.py reference
3. Update conftest.py fixture
4. Re-run validation

Status: BLOCKED
```

## Supporting Files

- **[references/refactoring-patterns.md](references/refactoring-patterns.md)** - Comprehensive guidance:
  - Detailed refactoring patterns (10+ scenarios)
  - Language-specific best practices (Python, JS/TS, Java, Go, Rust)
  - Token optimization calculations and examples
  - Advanced edge cases and solutions
  - Quality gate configuration details

## Red Flags to Avoid

1. **Using Edit for 2+ changes** - Wastes 30-50% tokens
2. **Skipping Read before Edit** - Causes edit failures
3. **Incomplete refactoring** - Partial changes break codebase
4. **Ignoring test failures** - Broken references in production
5. **Not verifying old references gone** - grep should return empty
6. **Forgetting documentation** - README/API docs out of sync
7. **Skipping quality gates** - Type errors indicate missed updates
8. **Wrong execution order** - Dependencies before dependents causes failures

---

**Key principle:** Token-efficient refactoring uses MultiEdit for 2+ changes (30-50% savings) while maintaining safety through validation.

**Remember:** 10 minutes of systematic refactoring prevents hours of debugging broken references.
