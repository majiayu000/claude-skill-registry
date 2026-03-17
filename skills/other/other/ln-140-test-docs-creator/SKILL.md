---
name: ln-140-test-docs-creator
description: Creates test documentation (testing-strategy.md + tests/README.md). Establishes testing philosophy and Story-Level Test Task Pattern. L2 Worker in ln-100-documents-pipeline workflow.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Test Documentation Creator

This skill creates and validates test documentation: testing-strategy.md (universal testing philosophy) + tests/README.md (test organization structure and Story-Level Test Task Pattern).

## Purpose

Creates and validates test documentation (testing-strategy.md + tests/README.md) establishing universal testing philosophy, Risk-Based Testing strategy, and Story-Level Test Task Pattern for any project.

## When to Use This Skill

**This skill is a L2 WORKER** invoked by **ln-100-documents-pipeline** orchestrator.

This skill should be used directly when:
- Creating only test documentation (testing-strategy.md + tests/README.md)
- Validating existing test documentation structure and content
- Setting up test philosophy and structure documentation for existing project
- NOT creating full documentation structure (use ln-100-documents-pipeline for complete setup)

## Workflow

The skill follows a 3-phase workflow: **CREATE** → **VALIDATE STRUCTURE** → **VALIDATE CONTENT**. Each phase builds on the previous, ensuring complete structure and semantic validation.

---

### Phase 1: Create Test Documentation

**Objective**: Establish test philosophy and documentation structure.

**Process**:

**1.1 Check & create directories**:
- Check if `docs/reference/guides/` exists → create if missing
- Check if `tests/` exists → create if missing
- Check if `tests/manual/` exists → create if missing
- Check if `tests/manual/results/` exists → create if missing
- Add `tests/manual/results/` to project `.gitignore` if not present
- Log for each: "✓ Created [directory]/" or "✓ [directory]/ already exists"

**1.2 Check & create documentation files**:
- Check if `docs/reference/guides/testing-strategy.md` exists
- If exists:
  - Skip creation
  - Log: "✓ testing-strategy.md already exists, proceeding to validation"
- If NOT exists:
  - Copy template: `ln-114-test-docs-creator/references/testing_strategy_template.md` → `docs/reference/guides/testing-strategy.md`
  - Replace placeholders:
    - `[CURRENT_DATE]` — current date (YYYY-MM-DD)
  - Log: "✓ Created testing-strategy.md from template"

- Check if `tests/README.md` exists
- If exists:
  - Skip creation
  - Log: "✓ tests/README.md already exists, proceeding to validation"
- If NOT exists:
  - Copy template: `ln-114-test-docs-creator/references/tests_readme_template.md` → `tests/README.md`
  - Replace placeholders:
    - `{{DATE}}` — current date (YYYY-MM-DD)
  - Log: "✓ Created tests/README.md from template"

**1.3 Output**:
```
docs/reference/guides/
└── testing-strategy.md           # Created or existing

tests/
├── README.md                     # Created or existing
└── manual/
    └── results/                  # Created, added to .gitignore
```

---

### Phase 2: Validate Structure

**Objective**: Ensure test documentation files comply with structural requirements and auto-fix violations.

**Process**:

**2.1 Check SCOPE tags**:
- Read both files (testing-strategy.md, tests/README.md) - first 5 lines only
- Check for `<!-- SCOPE: ... -->` tag in each
- Expected SCOPE tags:
  - testing-strategy.md: `<!-- SCOPE: Universal testing philosophy (Risk-Based Testing, test pyramid, isolation patterns) -->`
  - tests/README.md: `<!-- SCOPE: Test organization structure (directory layout, Story-Level Test Task Pattern) -->`
- If missing in either file:
  - Use Edit tool to add SCOPE tag at line 1 (before first heading)
  - Track violation: `scope_tags_added += 1`

**2.2 Check required sections**:
- Load expected sections from `references/questions.md`
- For **testing-strategy.md**, required sections:
  - "Testing Philosophy"
  - "Test Levels"
- For **tests/README.md**, required sections:
  - "Test Organization"
  - "Running Tests"
- For each file:
  - Read file content
  - Check if `## [Section Name]` header exists
  - If missing:
    - Use Edit tool to add section with placeholder content from template
    - Track violation: `missing_sections += 1`

**2.3 Check Maintenance section**:
- For each file (testing-strategy.md, tests/README.md):
  - Search for `## Maintenance` header
  - If missing:
    - Use Edit tool to add at end of file:
      ```markdown
      ## Maintenance

      **Last Updated:** [current date]

      **Update Triggers:**
      - Test framework changes
      - Test organization changes
      - New test patterns introduced

      **Verification:**
      - [ ] All test examples follow current framework syntax
      - [ ] Directory structure matches actual tests/
      - [ ] Test runner commands are current
      ```
    - Track violation: `maintenance_added += 1`

**2.4 Check POSIX file endings**:
- For each file:
  - Check if file ends with single blank line (LF)
  - If missing:
    - Use Edit tool to add final newline
    - Track fix: `posix_fixed += 1`

**2.5 Report validation**:
- Log summary:
  ```
  ✅ Structure validation complete:
    - SCOPE tags: [added N / already present]
    - Missing sections: [added N sections]
    - Maintenance sections: [added N / already present]
    - POSIX endings: [fixed N / compliant]
  ```
- If violations found: "⚠️ Auto-fixed [total] structural violations"

---

### Phase 3: Validate Content

**Objective**: Ensure each section answers its questions with meaningful content and populate test-specific sections from auto-discovery.

**Process**:

**3.1 Load validation spec**:
- Read `references/questions.md`
- Parse questions and validation heuristics for 4 sections (2 per file)

**3.2 Validate testing-strategy.md sections**:

For this file, use **standard template content** (no auto-discovery needed):

1. **Testing Philosophy section**:
   - Read section content
   - Check validation heuristics from questions.md:
     - ✅ Mentions "Risk-Based Testing"
     - ✅ Has test pyramid description
     - ✅ Mentions priority threshold (≥15)
     - ✅ References Story-Level Test Task Pattern
     - ✅ Length > 100 words
   - If ANY heuristic passes → content valid
   - If ALL fail → log warning: "⚠️ testing-strategy.md → Testing Philosophy section may need review"

2. **Test Levels section**:
   - Read section content
   - Check validation heuristics from questions.md:
     - ✅ Lists 3 levels (E2E, Integration, Unit)
     - ✅ Has numeric ranges (2-5, 3-8, 5-15)
     - ✅ Explains rationale
     - ✅ Length > 150 words
   - If ANY heuristic passes → content valid
   - If ALL fail → log warning: "⚠️ testing-strategy.md → Test Levels section may need review"

**Note**: testing-strategy.md is **universal philosophy** - no project-specific auto-discovery needed.

**3.3 Validate tests/README.md sections with auto-discovery**:

**Section: Test Organization**

1. **Auto-discover test framework**:
   - Check `package.json` → "devDependencies" and "dependencies":
     - Node.js frameworks: jest, vitest, mocha, ava, tap, jasmine
     - If found: Extract name and version
   - Check `requirements.txt` (if Python project):
     - Python frameworks: pytest, nose2, unittest2
     - If found: Extract name and version
   - Check `go.mod` (if Go project):
     - Go uses built-in testing package
   - If framework detected:
     - Log: "✓ Test framework detected: [framework]@[version]"
     - Track: `framework_detected = "[framework]"`
   - If NOT detected:
     - Log: "⚠️ No test framework detected. Will use generic test organization."
     - Track: `framework_detected = None`

2. **Auto-discover test directory structure**:
   - Use Glob tool to scan tests/ directory:
     - Pattern: `"tests/e2e/**/*.{js,ts,py,go}"`
     - Pattern: `"tests/integration/**/*.{js,ts,py,go}"`
     - Pattern: `"tests/unit/**/*.{js,ts,py,go}"`
   - Count files in each directory:
     - `e2e_count = len(e2e_files)`
     - `integration_count = len(integration_files)`
     - `unit_count = len(unit_files)`
   - If directories exist:
     - Log: "✓ Test structure: [e2e_count] E2E, [integration_count] Integration, [unit_count] Unit tests"
   - If directories DON'T exist:
     - Create placeholder structure:
       ```
       tests/
         e2e/       (empty, ready for E2E tests)
         integration/  (empty, ready for Integration tests)
         unit/      (empty, ready for Unit tests)
       ```
     - Log: "✓ Created test directory structure (will be populated during Story test task execution)"

3. **Auto-discover naming conventions**:
   - For each test file found (from step 2):
     - Extract filename pattern:
       - `*.test.js` → "*.test.js" convention
       - `*.spec.ts` → "*.spec.ts" convention
       - `test_*.py` → "test_*.py" convention
       - `*_test.go` → "*_test.go" convention
   - Count occurrences of each pattern
   - Use most common pattern (majority rule)
   - If pattern detected:
     - Log: "✓ Naming convention: [pattern] (detected from [count] files)"
   - If NO files exist:
     - Use framework default:
       - Jest/Vitest → *.test.js
       - Mocha → *.spec.js
       - Pytest → test_*.py
       - Go → *_test.go
     - Log: "✓ Naming convention: [default_pattern] (framework default)"

4. **Check Test Organization section content**:
   - Read section from tests/README.md
   - Check validation heuristics:
     - ✅ Describes directory structure (e2e/integration/unit)
     - ✅ Mentions naming conventions
     - ✅ References Story-Level Test Task Pattern
     - ✅ Has framework mention
   - If ANY heuristic passes → content valid
   - If ALL fail → log warning: "⚠️ tests/README.md → Test Organization section needs update"

**Section: Running Tests**

1. **Auto-discover test runner command**:
   - Read `package.json` → "scripts" → "test"
   - If found:
     - Extract command value
     - Examples:
       - `"jest"` → Test runner: "npm test" (runs jest)
       - `"vitest"` → Test runner: "npm test" (runs vitest)
       - `"mocha"` → Test runner: "npm test" (runs mocha)
       - Custom script → Test runner: "npm test" (runs [custom])
     - Log: "✓ Test runner: npm test (runs [command])"
   - If NOT found (no package.json or no test script):
     - Use default based on detected framework (from step 3.3.1):
       - Jest → "npm test"
       - Vitest → "npm test"
       - Pytest → "pytest"
       - Go → "go test ./..."
     - Log: "⚠️ No test script found in package.json. Using default '[command]'."

2. **Auto-discover coverage command** (optional):
   - Check `package.json` → "scripts" for:
     - "test:coverage"
     - "coverage"
     - "test:cov"
   - If found:
     - Extract command
     - Log: "✓ Coverage command: npm run [script_name]"
   - If NOT found:
     - Use framework default:
       - Jest → "npm test -- --coverage"
       - Vitest → "npm test -- --coverage"
       - Pytest → "pytest --cov=src"
       - Go → "go test -cover ./..."
     - Log: "✓ Coverage command: [default] (framework default)"

3. **Check Running Tests section content**:
   - Read section from tests/README.md
   - Check validation heuristics:
     - ✅ Has test runner command
     - ✅ Mentions coverage
     - ✅ Shows how to run specific tests
     - ✅ Has command examples
   - If ANY heuristic passes → content valid
   - If ALL fail → log warning: "⚠️ tests/README.md → Running Tests section needs update"

**3.4 Report content validation**:
- Log summary:
  ```
  ✅ Content validation complete:
    - testing-strategy.md: [2 sections checked]
    - tests/README.md: [2 sections checked]
    - Test framework: [detected framework or "Not detected"]
    - Test structure: [e2e/integration/unit counts or "Created placeholder"]
    - Naming convention: [pattern or "Framework default"]
    - Test runner: [command]
    - Coverage command: [command]
  ```

---

## Complete Output Structure

```
docs/reference/guides/
└── testing-strategy.md           # Universal testing philosophy (465 lines)

tests/
└── README.md                     # Test organization + Story-Level Pattern (112 lines)
```

**Note**: Actual test directories (e2e/, integration/, unit/) created during Story test task execution or Phase 3 if missing.

---

## Critical Rules

- **Documentation only:** This skill creates test DOCUMENTATION, NOT actual test code
- **3-phase pipeline:** CREATE → VALIDATE STRUCTURE → VALIDATE CONTENT (no phase skipping)
- **Auto-discovery first:** Scan test frameworks and directory structure before falling back to defaults
- **Idempotent execution:** Checks existence before creation; re-validates on each run without duplication
- **SCOPE tags required:** Both files must have `<!-- SCOPE: ... -->` tag in first 5 lines

---

## Reference Files

- **Risk-based testing methodology:** `shared/references/risk_based_testing_guide.md`

### Templates

**Testing Strategy Template**:
- `references/testing_strategy_template.md` - Universal testing philosophy with:
  - SCOPE tags (testing philosophy, NOT framework-specific)
  - Core Philosophy ("Test YOUR code, not frameworks")
  - Risk-Based Testing Strategy (Priority Matrix, test caps)
  - Story-Level Testing Pattern
  - Test Organization (E2E/Integration/Unit definitions)
  - Isolation Patterns (Data Deletion/Transaction Rollback/DB Recreation)
  - What To Test vs NOT Test (universal examples)
  - Testing Patterns (Arrange-Act-Assert, Mock at the Seam, Test Data Builders)
  - Common Issues (Flaky Tests, Slow Tests, Test Coupling)
  - Coverage Guidelines
  - Verification Checklist

**Tests README Template**:
- `references/tests_readme_template.md` - Test organization with:
  - SCOPE tags (test documentation ONLY)
  - Overview (E2E/Integration/Unit test organization)
  - Testing Philosophy (brief, link to testing-strategy.md)
  - Test Structure (directory tree)
  - Story-Level Test Task Pattern (tests in final Story task, NOT scattered)
  - Test Execution (project-specific commands)
  - Quick Navigation (links to testing-strategy.md, kanban_board, guidelines)
  - Maintenance section (Update Triggers, Verification, Last Updated)

**Validation Specification**:
- `references/questions.md` (v1.0.0) - Question-driven validation:
  - Questions each section must answer (4 sections total)
  - Validation heuristics (ANY passes → valid)
  - Auto-discovery hints (test frameworks, directory structure, naming conventions)
  - MCP Ref hints (external research if needed)

---

## Best Practices

- **No premature validation**: Phase 1 creates structure, Phase 2 validates it (no duplicate checks)
- **Parametric validation**: Phase 3 validates 4 sections across 2 files (no code duplication)
- **Auto-discovery first**: Scan test frameworks and directory structure before using defaults
- **Idempotent**: ✅ Can run multiple times safely (checks existence before creation, re-validates on each run)
- **Separation of concerns**: CREATE → VALIDATE STRUCTURE → VALIDATE CONTENT
- **Story-Level Test Task Pattern**: Tests consolidated in final Story task (test planner creates task, test executor implements)
- **Value-Based Testing**: 2-5 E2E, 3-8 Integration, 5-15 Unit per Story (10-28 total max), Priority ≥15 MUST be tested
- **No test code**: This skill creates DOCUMENTATION only, NOT actual tests

### Documentation Standards
- **NO_CODE Rule:** Test docs describe strategy, not test implementations
- **Stack Adaptation:** Framework commands must match project stack
- **Format Priority:** Tables (test levels, counts) > Lists > Text

---

## Prerequisites

**Invoked by**: ln-110-documents-pipeline orchestrator

**Requires**:
- `docs/reference/guides/` directory (created by ln-112-reference-docs-creator or Phase 1 if missing)

**Creates**:
- `docs/reference/guides/testing-strategy.md` (universal testing philosophy)
- `tests/README.md` (test organization structure)
- Validated structure and content (auto-discovery of test frameworks and directory structure)

---

## Definition of Done

Before completing work, verify ALL checkpoints:

**✅ Structure Created (Phase 1):**
- [ ] `docs/reference/guides/` directory exists
- [ ] `tests/` directory exists
- [ ] `tests/manual/` directory exists
- [ ] `tests/manual/results/` directory exists
- [ ] `tests/manual/results/` added to `.gitignore`
- [ ] `testing-strategy.md` exists (created or existing)
- [ ] `tests/README.md` exists (created or existing)

**✅ Structure Validated (Phase 2):**
- [ ] SCOPE tags present in both files (first 5 lines)
- [ ] testing-strategy.md has "Testing Philosophy" and "Test Levels" sections
- [ ] tests/README.md has "Test Organization" and "Running Tests" sections
- [ ] Maintenance sections present in both files at end
- [ ] POSIX file endings compliant (LF, single blank line at EOF)

**✅ Content Validated (Phase 3):**
- [ ] testing-strategy.md → Testing Philosophy section checked (Risk-Based Testing mentioned)
- [ ] testing-strategy.md → Test Levels section checked (2-5 E2E, 3-8 Integration, 5-15 Unit)
- [ ] tests/README.md → Test Organization section checked or auto-discovered
- [ ] tests/README.md → Running Tests section checked or auto-discovered
- [ ] Test framework detected (if applicable) and logged
- [ ] Test directory structure scanned or created
- [ ] Naming conventions detected or defaults used
- [ ] Test runner command identified or defaults used

**✅ Reporting:**
- [ ] Phase 1 logged: creation summary
- [ ] Phase 2 logged: structural fixes (if any)
- [ ] Phase 3 logged: content validation summary with auto-discovery results

---

## Technical Details

**Standards**:
- Story-Level Test Task Pattern
- Value-Based Testing (2-5 E2E, 3-8 Integration, 5-15 Unit, 10-28 total max per Story)
- Risk-Based Testing (Priority ≥15)

**Language**: English only

**Auto-Discovery Support**:
- Node.js: jest, vitest, mocha, ava, tap, jasmine
- Python: pytest, nose2, unittest2
- Go: built-in testing package

---

**Version:** 7.2.0
**Last Updated:** 2026-01-15
