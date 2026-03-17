---
name: review-standard
description: Systematic code review skill checking documentation quality and promoting code reuse
---

# Review Standard

This skill instructs AI agents on how to perform comprehensive code reviews before merging
changes to the main branch. It ensures quality, consistency, and adherence to project
documentation and code reuse standards.

## Review Philosophy

Effective code review is:
- **Systematic**: Follow a consistent process across all reviews
- **Standards-based**: Enforce documentation standards defined in `document-guideline` skill
- **Reuse-focused**: Prevent reinventing the wheel by identifying existing utilities
- **Actionable**: Provide specific, implementable recommendations
- **Context-aware**: Understand the change within the broader codebase architecture

### Review Objectives

Every review must assess:
1. **Documentation Quality**: Are changes properly documented per `document-guideline` standards?
2. **Code Quality & Reuse**: Does the code follow best practices and leverage existing utilities?
3. **Advanced Code Quality**: Does the code exhibit clarity, type safety, and appropriate scope?
   - **Indirection Analysis**: Question wrappers and unnecessary abstractions
   - **Code Repetition Detection**: Identify duplicate patterns requiring unified interfaces
   - **Module Focus Validation**: Ensure code paths aren't repurposed for unrelated features
   - **Interface Clarity**: Verify clear separation of declaration, usage, and error handling
   - **Type Safety**: Enforce type annotations and eliminate magic numbers
   - **Change Impact Control**: Validate modifications are scoped appropriately

The review process is designed to catch issues before merge, not to block progress. Reviews
provide recommendations - final merge decisions remain with maintainers.

## Review Process Overview

When the `/code-review` command is invoked, agents must:

1. **Gather context**: Get list of changed files and full diff
2. **Phase 1 - Documentation Review**: Validate documentation completeness and quality
3. **Phase 2 - Code Quality Review**: Assess code quality and reuse opportunities
4. **Phase 3 - Advanced Code Quality Review**: Evaluate indirection, type safety, and change scope
5. **Generate report**: Provide structured, actionable feedback

## Phase 1: Documentation Quality Review

This phase validates that all changes comply with the `document-guideline` skill standards.

### Step 1: Identify Changed Files

Get the list of all changed files:

```bash
git diff --name-only main...HEAD
```

Categorize files by type:
- **Source code files**: `.py`, `.c`, `.cpp`, `.cxx`, `.cc`, etc.
- **Documentation files**: `.md` files
- **Test files**: `test_*.sh`, `*_test.py`, etc.
- **Other files**: Configuration, data files, etc.

### Step 2: Validate Folder README.md Files

**Standard**: Every folder (except hidden folders) must have a `README.md` file.

**Check**:
```bash
# Get list of directories with changes
git diff --name-only main...HEAD | xargs -n1 dirname | sort -u

# For each directory, check if README.md exists
```

**Common issues**:
- New folder created without `README.md`
- Existing folder's `README.md` not updated to reflect new files

**Example finding**:
```
❌ Missing folder documentation
   claude/skills/new-skill/ - No README.md found

   Recommendation: Create README.md documenting:
   - Folder purpose (what is this skill for?)
   - Key files and their roles
   - Integration with other skills
```

### Step 3: Validate Source Code Interface Documentation

**Standard**: Every source code file must have a corresponding `.md` file.

**File types requiring documentation**:
- Python: `*.py` → `*.md`
- C/C++: `*.c`, `*.cpp`, `*.cxx`, `*.cc` → `*.md`

**Check**:
```bash
# For each source file in changes, verify .md file exists
git diff --name-only main...HEAD | grep -E '\.(py|c|cpp|cxx|cc)$'

# For each match, check if corresponding .md exists
```

**Review .md content for**:
1. **External Interfaces section**: Documents public APIs
   - Function signatures
   - Expected inputs/outputs
   - Error conditions

2. **Internal Helpers section**: Documents private implementation
   - Internal functions
   - Helper utilities
   - Complex algorithms

**Common issues**:
- Source file exists but `.md` file missing
- `.md` file exists but doesn't document all public functions
- Interface documentation doesn't match actual implementation

**Example finding**:
```
❌ Missing interface documentation
   src/utils/validator.py - No validator.md found

   Recommendation: Create validator.md with:
   - External Interface: validate_input(), validate_config() signatures
   - Internal Helpers: _check_type(), _sanitize_value() descriptions

❌ Incomplete interface documentation
   src/api/handler.md - Missing documentation for handle_request() function

   Recommendation: Add handle_request() to External Interface section:
   - Parameters: request object structure
   - Return value: response object or error
   - Error conditions: invalid request format, auth failures
```

### Step 4: Validate Test Documentation

**Standard**: Every test file must have documentation explaining what it tests.

**Acceptable formats**:
1. Inline comments within test file (preferred for simple tests)
2. Companion `.md` file (for complex test suites)

**Check**:
```bash
# Get test files from changes
git diff --name-only main...HEAD | grep -E '(^test_|_test\.(py|sh))'

# For bash tests, check for:
# - Inline comments matching pattern: "# Test N:" or "# Test:"
# - OR companion .md file exists

# For Python tests, check for:
# - Docstrings in test functions
# - OR companion .md file exists
```

**Common issues**:
- Test file has no comments or documentation
- Test file has generic comments but doesn't explain what's being tested
- Complex test suite lacks overview documentation

**Example finding**:
```
❌ Missing test documentation
   tests/test_validation.sh - No inline comments or test_validation.md found

   Recommendation: Add inline comments:
   # Test 1: Validator accepts valid input
   # Expected: Exit code 0, no errors
   test_valid_input() { ... }

   # Test 2: Validator rejects malformed input
   # Expected: Exit code 1, error message contains "malformed"
   test_malformed_input() { ... }
```

### Step 5: Check for High-Level Design Documentation

**Standard**: Architectural changes should have design documentation in `docs/`.

**When design docs are expected**:
- New subsystems or major features
- Architectural changes affecting multiple components
- New workflows or processes
- Significant refactoring

**Check**:
```bash
# Look for design doc references in commit messages
git log main...HEAD --format=%B

# Check if docs/ directory has relevant updates
git diff --name-only main...HEAD | grep '^docs/'
```

**Note**: Design docs are not enforced by linting - requires human judgment.

**Common issues**:
- Major architectural change with no design rationale documented
- New subsystem without overview documentation

**Example finding**:
```
⚠️  Consider adding design documentation
   Changes introduce new authentication subsystem across 5 files

   Recommendation: Consider creating docs/authentication.md to document:
   - Architecture overview
   - Authentication flow
   - Integration points with existing code
   - Security considerations
```

### Step 6: Leverage Documentation Linter

**Tool**: `scripts/lint-documentation.sh`

This script validates structural requirements:
- All folders have `README.md`
- All source files have `.md` companions
- All test files have documentation

**Run linter**:
```bash
./scripts/lint-documentation.sh
```

**Note**: On milestone branches, linter may be bypassed with `git commit --no-verify`.
During review, check if bypass was appropriate:
- ✅ Acceptable: Milestone commit, documentation complete, implementation in progress
- ❌ Not acceptable: Delivery commit, documentation incomplete or missing

**Example finding**:
```
❌ Documentation linter would fail
   Running ./scripts/lint-documentation.sh on this branch would fail:
   - Missing: src/utils/parser.md
   - Missing: claude/commands/README.md

   Recommendation: Add missing documentation before final merge
```

## Phase 2: Code Quality & Reuse Review

This phase assesses code quality and identifies opportunities to reuse existing utilities.

### Step 1: Check for Code Duplication

**Objective**: Find duplicate or similar code within the changes.

**Method**:
```bash
# Get the diff content
git diff main...HEAD

# For each new function/class, search for similar patterns
git grep -n "similar_pattern"
```

**Look for**:
- Similar function names or logic patterns
- Repeated code blocks
- Duplicate validation or error handling logic

**Common issues**:
- New function duplicates existing utility
- Similar logic implemented differently in different files
- Copy-pasted code instead of extracting to shared utility

**Example finding**:
```
❌ Code duplication detected
   src/new_feature.py:42 - Function parse_date() duplicates existing logic

   Existing utility: src/utils/date_parser.py:parse_date()

   Recommendation: Import and use existing parse_date() instead of reimplementing
```

### Step 2: Identify Reuse Opportunities (Local Utilities)

**Objective**: Find existing project utilities that could replace new code.

**Method**:
```bash
# Search for common utility patterns
git grep -n "def validate_"
git grep -n "class.*Parser"
git grep -n "def format_"

# Check common utility locations
ls -la src/utils/
ls -la scripts/
```

**Common utility categories to check**:
- **Validation**: Input validation, type checking, format verification
- **Parsing**: File parsing, data transformation, format conversion
- **Formatting**: Output formatting, string manipulation, templating
- **File operations**: Reading, writing, directory management
- **Git operations**: Diff handling, branch management, commit parsing

**Example finding**:
```
❌ Reinventing the wheel - local utility exists
   src/api/handler.py:67 - Manual JSON validation logic

   Existing utility: src/utils/validators.py:validate_json()

   Recommendation: Replace manual validation with:
   from src.utils.validators import validate_json
   result = validate_json(data)

   Benefits: Consistent error handling, tested utility, less code to maintain
```

### Step 3: Identify Reuse Opportunities (External Libraries)

**Objective**: Find standard libraries or external packages that could replace custom code.

**Method**:
```bash
# Check imports in changed files
git diff main...HEAD | grep -E '^[+]import|^[+]from'

# Look for custom implementations of common tasks
# - Date/time manipulation (use datetime, dateutil)
# - HTTP requests (use requests, urllib)
# - JSON/YAML parsing (use json, yaml)
# - Argument parsing (use argparse)
# - File watching (use watchdog)
```

**Common reinvented wheels**:
- Custom argument parsing instead of `argparse`
- Manual HTTP client instead of `requests`
- Custom date parsing instead of `dateutil`
- Manual configuration parsing instead of `configparser` or `yaml`
- Custom logging instead of Python's `logging` module

**Example finding**:
```
❌ Reinventing the wheel - standard library exists
   src/cli.py:23-45 - Custom argument parsing with manual --flag handling

   Standard library: Python's argparse module

   Recommendation: Replace custom parsing with argparse:
   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument('--flag', help='description')
   args = parser.parse_args()

   Benefits: Automatic --help generation, type conversion, error handling
```

### Step 4: Review Imports and Dependencies

**Objective**: Check for redundant or conflicting dependencies.

**Method**:
```bash
# Check all imports in changed files
git diff main...HEAD | grep -E '^[+]import|^[+]from'

# Look for:
# - Multiple libraries for same purpose (requests + urllib3 + httpx)
# - Unused imports
# - Non-standard libraries when standard ones exist
```

**Common issues**:
- Importing entire module when only one function needed
- Multiple libraries imported for similar functionality
- Using third-party library when standard library sufficient

**Example finding**:
```
⚠️  Dependency consideration
   src/fetcher.py:5 - Added import: import httpx

   Note: Project already uses 'requests' library for HTTP

   Recommendation: Use consistent HTTP library across project:
   from requests import get, post

   Unless httpx provides specific required feature, prefer existing dependency
```

### Step 5: Verify Project Conventions and Patterns

**Objective**: Ensure code follows existing project patterns and architecture.

**Method**:
```bash
# Study similar existing code
git grep -l "similar_pattern"

# Compare structure:
# - Error handling approach
# - Function naming conventions
# - Module organization
# - Configuration management
```

**Check for**:
- Consistent error handling patterns
- Naming conventions (snake_case, camelCase, PascalCase)
- Module structure and organization
- Configuration approach (env vars, config files, CLI args)
- Logging patterns

**Example finding**:
```
⚠️  Inconsistent with project patterns
   src/new_module.py - Uses camelCase function names

   Project convention: snake_case for functions (see src/utils/, src/api/)

   Recommendation: Rename functions to match project style:
   - parseInput() → parse_input()
   - validateData() → validate_data()
```

## Phase 3: Advanced Code Quality Review

This phase performs deep analysis of code structure, type safety, and architectural boundaries.

### Step 1: Indirection Analysis

**Objective**: Identify and question unnecessary wrappers and abstractions.

**Method**:
```bash
# Check for wrapper patterns
git diff main...HEAD | grep -E "class.*Wrapper|def.*wrapper|class.*Adapter|def.*adapter"

# Look for delegation-only classes/functions
git diff main...HEAD | grep -E "^\+.*def.*\(.*\):" | head -20
```

**Check for**:
- Classes that only delegate to another class without adding value
- Functions that wrap existing functions without transformation
- Abstractions created prematurely without clear need
- Wrappers that exist to compensate for poor interface design

**Common issues**:
- Wrapper class adds no functionality, just forwards calls
- Helper function wraps standard library with no value added
- Abstraction layer introduced without concrete use case
- Interface design flaw hidden behind wrapper instead of fixing root cause

**Example finding**:
```
❌ Unnecessary indirection
   src/utils/request_wrapper.py:12 - Class RequestWrapper only delegates to requests.get()

   Code:
   class RequestWrapper:
       def get(self, url):
           return requests.get(url)

   Recommendation: Remove wrapper and use requests.get() directly

   OR if wrapper provides value (retries, logging, auth):
   - Document the added value in docstring
   - Add meaningful functionality, not just delegation
```

### Step 2: Code Repetition Deep Analysis

**Objective**: Identify patterns suggesting need for unified interface or refactoring.

**Method**:
```bash
# Find repeated function name patterns
git diff main...HEAD | grep -E "^\+\s*def (validate_|parse_|format_|handle_)"

# Look for similar code blocks
git diff main...HEAD | grep -E "^\+" | sort | uniq -d
```

**Check for**:
- Multiple similar functions with slight variations (validate_x, validate_y, validate_z)
- Repeated code patterns that could use unified interface
- Copy-pasted logic with minor differences
- Opportunities for generalization vs. over-engineering

**Balance**:
- **Generalize** when pattern appears 3+ times with clear abstraction
- **Flag over-engineering** when premature abstraction adds complexity
- **Clarify intent** when uncertain about appropriate level of abstraction

**Example finding**:
```
⚠️  Code repetition pattern detected
   src/validators.py - Three similar validation functions:
   - validate_email() (line 15)
   - validate_phone() (line 32)
   - validate_url() (line 48)

   Pattern: All follow format:
   1. Regex match against pattern
   2. Return True/False
   3. Optional custom error message

   Recommendation: Consider unified interface:
   def validate_format(value, pattern, error_msg=None):
       if not re.match(pattern, value):
           raise ValueError(error_msg or f"Invalid format: {value}")
       return True

   Then call with:
   validate_format(email, EMAIL_PATTERN, "Invalid email")
   validate_format(phone, PHONE_PATTERN, "Invalid phone")

   Note: Only proceed if this simplifies the codebase. If each validator
   has unique logic beyond pattern matching, keep them separate.
```

### Step 3: Module Focus Validation

**Objective**: Ensure modules maintain single responsibility and don't repurpose code paths.

**Method**:
```bash
# Identify modules being modified
git diff --name-only main...HEAD

# For each module, check if new code aligns with module purpose
# Read existing module content and compare with changes
```

**Check for**:
- Borrowing code paths for unrelated features
- Adding functionality that belongs in different module
- Module scope creep (utils becoming catch-all)
- Private helpers that should be shared utilities

**Differentiate**:
- **Module-specific helpers**: Keep private to module (e.g., `_format_response()` in API handler)
- **Reusable utilities**: Move to shared `utils/` (e.g., `validate_json()` used across modules)

**Example finding**:
```
❌ Module focus violation
   src/api/user_handler.py:67 - Added file parsing logic

   Issue: user_handler.py is responsible for HTTP request handling,
   but now includes CSV parsing functionality unrelated to API handling

   Recommendation: Extract to appropriate location:
   - If CSV parsing is reusable → src/utils/csv_parser.py
   - If specific to user data → src/models/user_csv.py
   - Then import and use in user_handler.py

⚠️  Helper scope consideration
   src/analysis/checker.py:45 - Added _validate_config() helper

   Question: Is this validation specific to checker module or reusable?
   - If checker-specific: Keep as private helper (current location OK)
   - If reusable across analysis modules: Move to src/analysis/utils.py
   - If project-wide: Move to src/utils/validators.py
```

### Step 4: Interface Boundary Clarity

**Objective**: Verify clear separation of declaration, usage, and error handling.

**Method**:
```bash
# Check for dynamic attribute access
git diff main...HEAD | grep -E "getattr|setattr|hasattr"

# Look for dataclass usage (preferred for structured data)
git diff main...HEAD | grep -E "@dataclass|class.*\(.*\):"

# Find None-handling patterns
git diff main...HEAD | grep -E "is None|if.*None|== None"
```

**Prefer `@dataclass` for structured data**:
- Pre-declares all attributes explicitly
- Provides type safety
- Generates `__init__`, `__repr__` automatically
- Avoids dynamic attribute assignment

**Check for**:
- Use of `getattr`/`setattr` instead of explicit attributes
- None-handling scattered at usage sites instead of accessor level
- Mixing mandatory vs. optional attributes without clear contract
- Dynamic attribute assignment hiding interface contract

**Example finding**:
```
❌ Dynamic attribute access reduces clarity
   src/models/config.py:23 - Uses getattr(obj, 'field', default)

   Code:
   value = getattr(config, 'timeout', 30)

   Issue: Unclear whether 'timeout' is:
   - Mandatory attribute (should error if missing)
   - Optional attribute (default is intentional)

   Recommendation: Use @dataclass with explicit declaration:
   from dataclasses import dataclass

   @dataclass
   class Config:
       timeout: int = 30  # Optional with default
       host: str          # Mandatory, no default

   Benefits:
   - Clear interface contract
   - Type safety
   - IDE autocomplete support

⚠️  None-handling at usage site
   src/api/handler.py:45 - None check at usage:

   Code:
   if user.email is not None:
       send_email(user.email)

   Recommendation: Handle at accessor level instead:
   - If email is mandatory: Ensure user.email is never None (validation at creation)
   - If email is optional: Provide method has_email() or email property with default

   Example:
   @property
   def has_email(self) -> bool:
       return self.email is not None
```

### Step 5: Type Safety & Magic Numbers

**Objective**: Enforce type annotations and eliminate unnamed literal constants.

**Method**:
```bash
# Find magic numbers (2+ digit literals)
git diff main...HEAD | grep -E "^\+.*[^a-zA-Z_0-9][0-9]{2,}[^a-zA-Z_0-9]"

# Check for type annotations on new functions
git diff main...HEAD | grep -E "^\+\s*def\s+[a-zA-Z_]+" | grep -v " -> "

# Look for string-based type annotations (avoid these)
git diff main...HEAD | grep -E ":\s*['\"].*['\"]"

# Check for TYPE_CHECKING usage (good for circular imports)
git diff main...HEAD | grep -E "from typing import TYPE_CHECKING|if TYPE_CHECKING:"
```

**Type annotation requirements**:
- All function signatures must have parameter and return type annotations
- Use `typing.TYPE_CHECKING` for types that cause circular dependencies
- Avoid string-based type annotations (use actual types)
- Import types properly at module level

**Magic number detection**:
- Flag literal constants embedded in code (86400, 3600, 1024, etc.)
- Suggest named constants or enums
- Allow well-known literals (0, 1, 2, -1) without flags

**Example finding**:
```
❌ Magic number detected
   src/cache.py:34 - Literal constant 86400

   Code:
   cache.set(key, value, 86400)

   Issue: Unclear what 86400 represents

   Recommendation: Extract to named constant:
   SECONDS_PER_DAY = 86400
   cache.set(key, value, SECONDS_PER_DAY)

   OR use more readable calculation:
   CACHE_TTL = 24 * 60 * 60  # 24 hours in seconds

❌ Missing type annotations
   src/utils/parser.py:15 - Function lacks return type

   Code:
   def parse_input(data):
       return json.loads(data)

   Recommendation: Add type annotations:
   def parse_input(data: str) -> dict:
       return json.loads(data)

   OR with more specific return type:
   from typing import Dict, Any

   def parse_input(data: str) -> Dict[str, Any]:
       return json.loads(data)

⚠️  Circular import handled well
   src/models/user.py:5 - Uses TYPE_CHECKING for type imports

   Code:
   from typing import TYPE_CHECKING
   if TYPE_CHECKING:
       from src.services.auth import AuthService

   def validate_auth(self, auth: 'AuthService') -> bool:

   This is acceptable pattern, but could be improved to:
   def validate_auth(self, auth: AuthService) -> bool:

   Since AuthService is imported under TYPE_CHECKING guard
```

### Step 6: Change Impact Analysis

**Objective**: Validate changes are appropriately scoped and justify cross-module impact.

**Method**:
```bash
# Count affected modules
git diff --name-only main...HEAD | cut -d'/' -f1-2 | sort -u | wc -l

# List affected modules
git diff --name-only main...HEAD | cut -d'/' -f1-2 | sort -u

# Check for broad refactoring across many files
git diff --stat main...HEAD
```

**Check for**:
- Changes limited to target module vs. widespread modification
- Cross-module impact with explicit justification
- Refactoring scope appropriate for stated intent
- Unintended side effects from broad changes

**Scope expectations**:
- **Feature addition**: Should touch 1-3 modules (implementation + tests)
- **Bug fix**: Ideally 1-2 files (bug location + test)
- **Refactoring**: Broad impact acceptable if explicitly stated
- **API change**: Multiple files expected, should be documented

**Example finding**:
```
⚠️  Broad change impact
   Changes affect 8 modules across 3 subsystems:
   - src/api/ (4 files)
   - src/models/ (3 files)
   - src/utils/ (2 files)

   Issue: PR title suggests "Add email validation to User model"
   but changes span multiple subsystems

   Question: Is this scope appropriate?
   - If refactoring email validation project-wide: ✅ Appropriate, document in PR
   - If just adding User.email field: ⚠️  Scope too broad, should be limited

   Recommendation: Clarify intent in PR description and justify cross-module changes

❌ Uncontrolled change scope
   src/config.py:23 - Changed constant value

   Code change:
   - MAX_RETRIES = 3
   + MAX_RETRIES = 5

   Impact: Affects all modules using MAX_RETRIES:
   - src/api/client.py
   - src/services/fetcher.py
   - tests/integration/test_retry.py

   Recommendation: Verify this is intended behavior change, not accidental:
   1. Document reason for change in commit message
   2. Update related tests to reflect new retry count
   3. Consider adding migration notes if breaking external expectations
```

## Workflow and Integration

### When to Use Review-Standard

Use the `/code-review` command:
- **Before creating a pull request**: Catch issues early
- **Before final merge to main**: Ensure quality standards
- **After milestone commits**: Validate incremental progress
- **On request**: When explicit review needed

### Integration with Document-Guideline

The `document-guideline` skill defines the standards; `review-standard` enforces them:

**document-guideline provides**:
- Documentation requirements (folder READMEs, source .md files, test docs)
- Content guidelines (what to document, how to structure)
- Workflow integration (design-first TDD, milestone flexibility)

**review-standard enforces**:
- Validates changes comply with documentation standards
- Checks for missing or incomplete documentation
- Leverages `scripts/lint-documentation.sh` for validation
- Provides specific remediation recommendations

### Integration with Milestone Workflow

**Milestone commits** (in-progress implementation):
- May bypass documentation linter with `--no-verify`
- Documentation-code inconsistency is acceptable
- Review should note progress toward completion

**Delivery commits** (final implementation):
- Must pass all linting without bypass
- Documentation must match implementation
- All tests must pass
- Review should confirm delivery readiness

**Example milestone review**:
```
✅ Milestone commit review
   Status: Milestone 2/3 (6/10 tests passing)

   Documentation: Complete and accurate for final state
   Code: 60% implemented, matches documented interfaces

   Notes:
   - Appropriate use of --no-verify for milestone commit
   - Documentation correctly describes intended final behavior
   - Partial implementation progressing as expected

   Recommendation: Continue implementation following documented design
```

### Command Invocation

The `/code-review` command invokes this skill automatically:

```bash
/code-review
```

The command handles:
1. Verifying current branch is not main
2. Getting changed files: `git diff --name-only main...HEAD`
3. Getting full diff: `git diff main...HEAD`
4. Invoking review-standard skill with context
5. Displaying formatted review report

## Review Report Format

Every review must produce a structured report with actionable feedback.

### Report Structure

```markdown
# Code Review Report

**Branch**: issue-42-feature-name
**Changed files**: 8 files (+450, -120 lines)
**Review date**: 2025-01-15

---

## Phase 1: Documentation Quality

### ✅ Passed
- All folders have README.md files
- Test files have inline documentation

### ❌ Issues Found

#### Missing source interface documentation
- `src/utils/parser.py` - No parser.md found

  **Recommendation**: Create parser.md documenting:
  - External Interface: parse_input(data) signature and behavior
  - Internal Helpers: _tokenize(), _validate_syntax() descriptions

### ⚠️  Warnings

#### Consider design documentation
- New authentication subsystem spans 5 files

  **Recommendation**: Consider docs/authentication.md to document architecture

---

## Phase 2: Code Quality & Reuse

### ✅ Passed
- No code duplication detected
- Imports follow project conventions

### ❌ Issues Found

#### Reinventing the wheel - local utility exists
- `src/api/handler.py:67` - Manual JSON validation

  **Existing utility**: src/utils/validators.py:validate_json()

  **Recommendation**: Replace with:
  ```python
  from src.utils.validators import validate_json
  result = validate_json(data)
  ```

### ⚠️  Warnings

#### Dependency consideration
- Added httpx library when requests already used

  **Recommendation**: Use consistent HTTP library (requests) unless httpx feature required

---

## Phase 3: Advanced Code Quality

### ✅ Passed
- No unnecessary indirection detected
- Change scope appropriate for feature

### ❌ Issues Found

#### Magic number detected
- `src/cache.py:34` - Literal constant 86400

  **Recommendation**: Extract to named constant:
  ```python
  SECONDS_PER_DAY = 86400
  cache.set(key, value, SECONDS_PER_DAY)
  ```

### ⚠️  Warnings

#### Missing type annotations
- `src/utils/parser.py:15` - Function lacks return type

  **Recommendation**: Add type annotations:
  ```python
  def parse_input(data: str) -> dict:
      return json.loads(data)
  ```

---

## Overall Assessment

**Status**: ⚠️  NEEDS CHANGES

**Summary**:
- 3 critical issues: missing documentation, code reuse opportunity, magic number
- 3 warnings: design doc consideration, dependency consistency, type annotations

**Recommended actions before merge**:
1. Create parser.md documenting interfaces
2. Replace manual JSON validation with existing utility
3. Extract magic number to named constant
4. Add type annotations to parse_input()
5. Consider design doc for authentication subsystem
6. Evaluate httpx vs requests for HTTP client

**Merge readiness**: Not ready - address critical issues first
```

### Assessment Categories

**✅ APPROVED**:
- All documentation complete and accurate
- No code quality issues found
- All reuse opportunities identified and addressed
- No unnecessary indirection or magic numbers
- Type annotations present and correct
- Change scope appropriate for intent
- Ready for merge

**⚠️  NEEDS CHANGES**:
- Minor documentation gaps
- Code reuse opportunities exist
- Non-critical improvements recommended
- Missing type annotations on some functions
- Minor magic numbers or scope considerations
- Can merge after addressing issues

**❌ CRITICAL ISSUES**:
- Missing required documentation
- Significant code quality problems
- Major reuse opportunities ignored
- Unnecessary wrappers hiding design flaws
- Module responsibility violations
- Uncontrolled change scope
- Security or correctness concerns
- Must address before merge

### Providing Actionable Feedback

Every issue must include:
1. **Specific location**: File path and line number
2. **Clear problem**: What's wrong and why it matters
3. **Concrete recommendation**: Exact steps to fix
4. **Example**: Code sample or specific implementation

**Bad feedback**:
```
❌ Documentation needs improvement
   Some files are missing docs
```

**Good feedback**:
```
❌ Missing interface documentation
   src/utils/parser.py - No parser.md found

   Recommendation: Create parser.md with:

   ## External Interface

   ### parse_input(data: str) -> dict
   Parses input string and returns structured data.

   **Parameters**: data (str) - Input string to parse
   **Returns**: dict - Parsed data structure
   **Raises**: ValueError - If data format invalid
```

## Summary

The review-standard skill provides a systematic approach to code review that:

1. **Validates documentation**: Ensures compliance with `document-guideline` standards
2. **Promotes code reuse**: Identifies existing utilities and prevents duplication
3. **Enforces quality**: Checks conventions, patterns, and best practices
4. **Provides actionable feedback**: Specific, implementable recommendations

Reviews are recommendations to help maintain quality - final merge decisions remain
with project maintainers.
