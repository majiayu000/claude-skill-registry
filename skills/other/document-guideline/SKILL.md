---
name: document-guideline
description: Instructs AI agents on documentation standards for design docs, folder READMEs, source code interfaces, and test cases
---

# Document Guideline

This skill instructs AI agents on how to maintain comprehensive documentation throughout
the development lifecycle. It defines documentation standards that are enforced via
pre-commit linting for structural requirements, while providing guidance on content
quality and workflow integration.

## Documentation Philosophy

Good documentation is:
- **Comprehensive**: Covers all code files, folders, and high-level designs
- **Enforced**: Structural requirements validated automatically via pre-commit linting
- **Design-first**: Documentation written before implementation (following TDD approach)
- **Milestone-friendly**: Documentation-code inconsistency acceptable during incremental development
- **Self-descriptive**: Each file, folder, and component documents its purpose and interfaces

### Documentation Types

This project maintains three levels of documentation:

1. **High-level design documents** (`docs/*`) - Architecture and design decisions
2. **Folder organization** (folder `README.md` files) - Purpose and file organization
3. **Code interface documentation** (`.md` companions to source files) - External and internal APIs

## High-Level Design Documentation

**Location**: `docs/*` directory

**Purpose**: Document architectural decisions, design rationale, and high-level project structure.

**When to create/update**:
- During planning phase (before implementation)
- When making architectural decisions
- When introducing new subsystems or major features
- When documenting workflows or processes

**Not enforced by linting**: Creating design documents requires human judgment about
what constitutes a "high-level design" versus implementation details.

**Content guidelines**:
- Focus on the "why" (design rationale) not just the "what"
- Document alternatives considered and trade-offs
- Include diagrams, workflows, or examples where helpful
- Keep design docs synchronized with actual implementation

**Examples of good design documents**:
- `docs/git-msg-tags.md` - Documents commit message tag standards
- `docs/developer.md` - Developer workflow and contribution guidelines
- `docs/options.md` - SDK configuration options and usage

**When NOT to create design docs**:
- For simple implementation details (put in code `.md` files instead)
- For temporary decisions or experiments
- For information that duplicates existing documentation

## Folder Organization Documentation

**Requirement**: Every folder (except hidden folders like `.git`) **MUST** have a `README.md` file.

**Enforced by**: Pre-commit linting (`scripts/lint-documentation.sh`)

**Purpose**: Document folder purpose and file organization so developers can quickly understand
the codebase structure.

**When to create**:
- When creating a new folder in the project
- Before committing any code that introduces a new directory

**Required content**:
1. **Folder purpose**: What is this folder for? (1-2 sentences)
2. **File organization**: What types of files are in this folder?
3. **Key files**: Brief description of important files (optional)

**Examples of good folder README.md**:

```markdown
# Skills Directory

This directory contains all Claude Code skills that define AI agent behavior.

## Organization

Each skill is in its own subdirectory with a `SKILL.md` file:
- `commit-msg/` - Skill for creating meaningful git commits
- `fork-dev-branch/` - Skill for creating development branches
- `milestone/` - Skill for incremental implementation with milestone commits

## Adding New Skills

Create a new subdirectory and add a `SKILL.md` file with frontmatter defining
the skill name and description.
```

**Format flexibility**:
- Can be brief (3-5 lines) for simple folders
- Can be detailed for complex subsystems
- Should reference key files if there are many files

## Source Code Interface Documentation

**Requirement**: Every source code file **MUST** have a corresponding `.md` file documenting its interfaces.

**File types requiring documentation** (enforced by linting):
- Python: `*.py` → `*.md`
- C/C++: `*.c`, `*.cpp`, `*.cxx`, `*.cc` → `*.md`

**Enforced by**: Pre-commit linting (`scripts/lint-documentation.sh`)

**Naming convention**: Same prefix as source file
- `foo.py` → `foo.md`
- `bar.cpp` → `bar.md`
- `baz.c` → `baz.md`

**Required sections**:

### 1. External Interfaces (Public APIs)

Document all interfaces exposed to external callers:
- Public functions/methods with signatures
- Public classes/structures with key attributes
- Module-level exports or entry points
- Expected inputs and outputs
- Error conditions and exceptions

### 2. Internal Helpers (Private APIs)

Document internal implementation details:
- Private functions and their purpose
- Internal data structures
- Helper utilities
- Algorithms or complex logic explanations

**Example interface documentation**:

```markdown
# validate_target_dir.sh

Script for validating target directories before SDK initialization.

## External Interface

### Command-line usage
```bash
./validate_target_dir.sh <target_dir> <mode>
```

**Parameters**:
- `target_dir`: Path to directory to validate
- `mode`: Either "init" or "update"

**Exit codes**:
- 0: Validation passed
- 1: Validation failed (directory issues)
- 2: Invalid arguments

**Output**: Error messages to stderr listing validation failures

## Internal Helpers

### check_directory_exists()
Validates that the target directory exists.

### check_write_permissions()
Validates that the user has write access to the directory.

### check_conflicting_files()
Scans for files that would conflict with SDK initialization.
Returns list of conflicting file paths.

### validate_init_mode()
Specific validation for "init" mode (directory must be empty or non-existent).

### validate_update_mode()
Specific validation for "update" mode (directory must have existing SDK structure).
```

**When implementation changes**:
- Update interface documentation to match
- During milestones, temporary doc-code mismatch is acceptable (see below)
- Before final delivery, all documentation must match implementation

## Test Documentation

**Requirement**: Every test case **MUST** have documentation explaining what it tests.

**Enforced by**: Pre-commit linting (`scripts/lint-documentation.sh`)

**Format options**:
1. **Inline comments** within the test file (preferred for simple tests)
2. **Companion `.md` file** (for complex test suites)

**Required content**:
- What is being tested (feature or behavior)
- Expected outcome
- Any setup or preconditions

**Example with inline comments**:

```bash
#!/bin/bash
# Test suite for documentation linting
# Tests that the linter correctly identifies missing documentation

set -e

# Test 1: Linter passes with complete documentation
# Expected: Exit code 0, no errors
test_complete_documentation() {
    # Setup: Create temporary directory with all docs present
    ...
}

# Test 2: Linter fails when folder missing README.md
# Expected: Exit code 1, error message lists folder
test_missing_folder_readme() {
    ...
}
```

**Example with companion .md file**:

For `test_documentation_lint.sh`, create `test_documentation_lint.md`:

```markdown
# Documentation Linter Test Suite

Tests for `scripts/lint-documentation.sh` to verify it correctly validates
documentation completeness.

## Test Cases

### test_complete_documentation
**Purpose**: Verify linter passes when all documentation is present
**Setup**: Temporary directory with source files and corresponding .md files
**Expected**: Exit code 0, no error output

### test_missing_folder_readme
**Purpose**: Verify linter catches folders without README.md
**Setup**: Create folder without README.md
**Expected**: Exit code 1, error message listing the folder

...
```

**Linting check**:
- For bash test files (`test_*.sh`), linter checks for either:
  - Inline comments following pattern `# Test N:` or `# Test:` or function comments
  - Companion `.md` file with same prefix

## Documentation-Code Consistency During Milestones

### Design-First TDD Workflow

This project follows strict design-first test-driven development:

1. **Phase 1: Documentation** - Update all relevant documentation first
2. **Phase 2: Tests** - Write test cases based on documentation
3. **Phase 3: Implementation** - Write code to make tests pass

### Acceptable Documentation-Code Inconsistency

During milestone commits, documentation and code may be temporarily inconsistent:

**Why this happens**:
- Documentation describes the **final intended state**
- Implementation is **incrementally catching up** to match documentation
- Tests are written based on documentation (may not all pass yet)

**When it's acceptable**:
- **During milestone commits**: Documentation complete, implementation in progress
- **On development branches**: Work is ongoing, not ready for final delivery
- **With explicit test status**: Milestone commits show `N/M tests passed`

**When it's NOT acceptable**:
- **Final delivery commits**: All tests must pass, docs must match code
- **Merging to main branch**: Complete consistency required
- **Production releases**: Documentation must accurately reflect implementation

### Pre-commit Linting and Milestones

The documentation linter (`scripts/lint-documentation.sh`) runs as part of the
pre-commit hook and validates:
- All folders have `README.md`
- All source files have corresponding `.md` files
- All test files have documentation

**Bypassing the linter**:

For milestone commits where documentation is complete but implementation is incomplete:

```bash
git commit --no-verify -m "milestone: ..."
```

The `--no-verify` flag bypasses **all** pre-commit hooks, including:
- Documentation linting
- Test execution

**IMPORTANT**: Only bypass for milestone commits on development branches. Never bypass
for final delivery commits or commits to main branch.

**Milestone progression example**:

```
Milestone 1: Documentation complete (bypass linting OK)
- All .md files created and document final interfaces
- Implementation: 0% complete
- Tests: 0/10 passed (expected, no implementation yet)
- Commit with: --no-verify

Milestone 2: Partial implementation (bypass linting OK)
- Documentation: Still accurate for final state
- Implementation: 60% complete
- Tests: 6/10 passed
- Commit with: --no-verify

Delivery: All tests pass (NO bypass)
- Documentation: Matches implementation exactly
- Implementation: 100% complete
- Tests: 10/10 passed
- Commit without: --no-verify (linter must pass)
```

## Integration with Other Skills

This documentation guideline integrates with other project skills:

### Integration with `plan-guideline` skill

When creating implementation plans, the `plan-guideline` skill references these
documentation standards:

- Step 1 in plans should always be documentation updates
- Plans should list specific `.md` files to create/update
- Plans should note which documentation is enforced by linting

### Integration with `milestone` skill

The `milestone` skill uses these guidelines for incremental development:

- Milestone 1 always creates documentation first
- `--no-verify` bypass acceptable for milestone commits
- Milestone commits track test progress (N/M tests passed)
- Final delivery requires all linting to pass

### Integration with `commit-msg` skill

The `commit-msg` skill considers documentation standards:

- Commits updating only documentation use `[docs]` tag
- Milestone commits note test status in message
- Delivery commits confirm all lints pass

## Summary

**Enforced by linting** (structural requirements):
- ✅ Folder `README.md` existence
- ✅ Source code `.md` file correspondence
- ✅ Test documentation presence

**Guided by skill** (content quality):
- High-level design document creation
- Interface documentation completeness
- Explanation clarity and usefulness

**Workflow integration**:
- Documentation written first (design-first TDD)
- Temporary doc-code mismatch OK during milestones
- All documentation must match code at delivery
