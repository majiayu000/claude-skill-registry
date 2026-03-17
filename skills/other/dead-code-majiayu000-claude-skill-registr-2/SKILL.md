---
name: dead-code-removal
description: Detects and safely removes unused code (imports, functions, classes)
  across multiple languages. Use after refactoring, when removing features, or before
  production deployment. Includes safety checks and validation.
author: Joseph OBrien
status: unpublished
updated: '2025-12-23'
version: 1.0.1
tag: skill
type: skill
---

# Dead Code Removal

This skill safely identifies and removes unused code across multiple programming languages. It includes comprehensive safety checks to prevent removing code that's actually needed.

## When to Use This Skill

- After refactoring code and removing features
- Before production deployment to reduce bundle size
- When cleaning up legacy code
- When removing deprecated functionality
- When optimizing codebase size
- When maintaining code quality standards

## What This Skill Does

1. **Language Detection**: Identifies project languages and structure
2. **Entry Point Mapping**: Maps entry points and critical paths
3. **Dependency Analysis**: Builds dependency graphs and usage patterns
4. **Safe Detection**: Identifies unused elements with safety checks
5. **Incremental Removal**: Removes code incrementally with validation
6. **Backup Creation**: Creates backups before making changes

## Helper Scripts

This skill includes Python helper scripts in `scripts/`:

- **`find_unused_imports.py`**: Uses AST parsing to accurately detect unused imports in Python files. Outputs JSON with unused imports and line numbers.

  ```bash
  python scripts/find_unused_imports.py src/utils.py src/services.py
  ```

## How to Use

### Remove Unused Code

```
Find and remove unused imports and functions in this project
```

```
Clean up dead code in src/ directory, but be conservative
```

### Specific Analysis

```
Check for unused functions in src/utils/ and remove them safely
```

## Analysis Process

### 1. Language Detection

**Identify Project Type:**

- Python: Look for `pyproject.toml`, `setup.py`, `requirements.txt`
- JavaScript/TypeScript: Check `package.json`, `tsconfig.json`
- Java: Look for `pom.xml`, `build.gradle`
- Go: Check `go.mod`
- Rust: Check `Cargo.toml`

**Detect Entry Points:**

- Python: `main.py`, `__main__.py`, `app.py`, `run.py`
- JavaScript: `index.js`, `main.js`, `server.js`, `app.js`
- Java: `Main.java`, `*Application.java`, `*Controller.java`
- Config files: `*.config.*`, `settings.*`, `setup.*`
- Test files: `test_*.py`, `*.test.js`, `*.spec.js`

### 2. Build Dependency Graph

**Cross-File Dependencies:**

- Track imports and requires
- Map function/method calls
- Identify class inheritance
- Track dynamic usage patterns

**Framework Patterns:**

- Preserve framework-specific patterns (Django models, React components, etc.)
- Check for decorators and annotations
- Verify entry point registrations

### 3. Detect Unused Elements

**Using Helper Script:**

The skill includes a Python helper script for finding unused imports:

```bash
# Find unused imports in Python files
python scripts/find_unused_imports.py src/utils.py src/services.py
```

**Unused Imports:**

```python
# Python: AST-based analysis
import ast
# Track: Import statements vs actual usage
# Skip: Dynamic imports (importlib, __import__)
```

```javascript
// JavaScript: Module analysis
// Track: import/require vs references
// Skip: Dynamic imports, lazy loading
```

**Unused Functions/Classes:**

- Define: All declared functions/classes
- Reference: Direct calls, inheritance, callbacks
- Preserve: Entry points, framework hooks, event handlers

### 4. Safety Checks

**Never Remove If:**

- Python: `getattr()`, `eval()`, `globals()` usage detected
- JavaScript: `window[]`, `this[]`, dynamic `import()` usage
- Java: Reflection, annotations (`@Component`, `@Service`)
- Framework patterns: Models, controllers, routes, components
- Entry points: Main functions, app initialization
- Test files: All test-related code

**Framework Preservation:**

**Python:**

- Django: Models, migrations, admin registrations
- Flask: Routes, blueprints, app factories
- FastAPI: Endpoints, dependencies

**JavaScript:**

- React: Components, hooks, context providers
- Vue: Components, directives, mixins
- Angular: Decorators, services, modules

**Java:**

- Spring: Beans, controllers, repositories
- JPA: Entities, repositories

### 5. Safe Removal Process

**Backup Creation:**

```bash
backup_dir="./unused_code_backup_$(date +%Y%m%d_%H%M%S)"
cp -r . "$backup_dir" 2>/dev/null || mkdir -p "$backup_dir" && rsync -a . "$backup_dir"
```

**Incremental Removal:**

1. Create temp file with change
2. Validate syntax
3. Run tests if available
4. Apply or rollback

**Validation:**

```bash
# Python
python -m py_compile file.py
python -m pytest

# JavaScript
npx eslint file.js
npm test

# Java
javac -Xlint file.java
mvn test
```

## Examples

### Example 1: Remove Unused Imports

**Input**: Clean up unused imports in `src/utils/helpers.py`

**Output**:

```markdown
## Dead Code Removal: src/utils/helpers.py

### Analysis
- **File**: `src/utils/helpers.py`
- **Total imports**: 8
- **Unused imports**: 3

### Unused Imports Found
1. `import os` - Line 2 (not used anywhere)
2. `import json` - Line 3 (not used anywhere)
3. `from datetime import timedelta` - Line 5 (not used anywhere)

### Safe to Remove
✅ All 3 imports are safe to remove (no dynamic usage detected)

### Changes
```python
# Before
import os
import json
from datetime import datetime, timedelta
import requests

# After
from datetime import datetime
import requests
```

### Validation

- ✅ Syntax check passed
- ✅ Tests pass
- ✅ No dynamic imports detected

```

### Example 2: Remove Unused Functions

**Input**: Find unused functions in `src/services/`

**Output**:
```markdown
## Dead Code Removal: src/services/

### Analysis
- **Files analyzed**: 12
- **Functions found**: 45
- **Unused functions**: 2

### Unused Functions

**1. `formatOldDate()` in `src/services/utils.js`**
- **Location**: Line 34-42
- **Status**: ✅ Safe to remove
- **Reason**: No references found, not exported, not used in tests

**2. `legacyAuth()` in `src/services/auth.js`**
- **Location**: Line 78-95
- **Status**: ⚠️ Preserved (framework pattern)
- **Reason**: Referenced in route configuration (line 12)

### Summary
- **Removed**: 1 function (`formatOldDate`)
- **Preserved**: 1 function (framework usage)
- **Lines removed**: 9
- **Size reduction**: ~300 bytes
```

## Best Practices

### Safety Guidelines

**Do:**

- Run tests after each removal
- Preserve framework patterns
- Check string references in templates
- Validate syntax continuously
- Create comprehensive backups
- Remove incrementally

**Don't:**

- Remove without understanding purpose
- Batch remove without testing
- Ignore dynamic usage patterns
- Skip configuration files
- Remove from migrations
- Remove exported/public APIs

### Detection Patterns

**Static Analysis:**

- Use AST parsing for accurate detection
- Track cross-file references
- Check for dynamic usage patterns
- Verify framework-specific patterns

**Validation:**

- Always run syntax checks
- Run tests after removal
- Verify build still works
- Check for runtime errors

### Reporting

**Report Should Include:**

- Files analyzed (count and types)
- Unused detected (imports, functions, classes)
- Safely removed (with validation status)
- Preserved (reason for keeping)
- Impact metrics (lines removed, size reduction)

## Related Use Cases

- Code cleanup before release
- Reducing bundle size
- Removing deprecated code
- Maintaining code quality
- Refactoring legacy codebases
- Optimizing build times
