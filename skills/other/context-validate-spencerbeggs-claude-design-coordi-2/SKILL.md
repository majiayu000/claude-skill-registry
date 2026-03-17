---
name: context-validate
description: Validate CLAUDE.md structure, formatting, and quality. Use when checking context files for compliance, ensuring proper structure, or verifying before commits.
allowed-tools: Read, Glob, Bash
agent: context-doc-agent
---

# LLM Context File Validation

Validates CLAUDE.md files for structure, formatting, and quality compliance
with Claude Code best practices.

## Overview

This skill validates LLM context files by:

1. Reading CLAUDE.md files (root and package-level)
2. Validating markdown structure and formatting
3. Checking for required sections
4. Analyzing content quality and organization
5. Verifying design doc references
6. Checking line limits and organization
7. Reporting issues with severity levels

## Instructions

### 1. Parse Parameters

Extract parameters from the user's request:

**Required:**

- `target`: Path to CLAUDE.md file, or "all" for all context files

**Optional:**

- `strict`: Enable strict mode with additional quality checks (default: false)
- `check-refs`: Validate design doc references exist (default: true)

**Examples:**

- "Validate the root CLAUDE.md"
  - target: `CLAUDE.md`
  - strict: false
  - check-refs: true

- "Validate CLAUDE.md for effect-type-registry"
  - target: `pkgs/effect-type-registry/CLAUDE.md`
  - strict: false
  - check-refs: true

- "Strict validation of all CLAUDE.md files"
  - target: `all`
  - strict: true
  - check-refs: true

### 2. Load Configuration

Read `.claude/design/design.config.json` to understand:

- Context quality standards (`quality.context`)
- Root max lines limit (default: 500)
- Child max lines limit (default: 300)
- Whether design doc pointers are required

**Example config:**

```json
{
  "quality": {
    "context": {
      "rootMaxLines": 500,
      "childMaxLines": 300,
      "requireDesignDocPointers": true
    }
  }
}
```

### 3. Find Context Files

Based on target parameter:

**Specific file:**

```bash
# Validate single file
read {file-path}
```

**All files:**

```bash
# Find all CLAUDE.md files
glob "**/CLAUDE.md" --path="."
```

Typical locations:

- Root: `CLAUDE.md`
- Packages: `pkgs/*/CLAUDE.md`
- Website: `website/CLAUDE.md`

### 4. Validate Each File

For each CLAUDE.md file, perform validation checks:

#### 4.1 Structure Validation

**Required Sections (Root CLAUDE.md):**

- Project Overview
- Commands (or equivalent)
- Architecture (or Development Notes)
- Tooling (or equivalent)

**Required Sections (Package CLAUDE.md):**

- Package Overview (or similar)
- API Documentation (or Key Exports)
- Development Notes (or Architecture)
- Testing (or Quality)

**Validation:**

- All required sections present
- Sections in logical order
- No duplicate sections
- Proper heading hierarchy (H1 → H2 → H3)

#### 4.2 Formatting Validation

**Markdown Quality:**

- Valid markdown syntax
- Proper heading levels (no skipped levels)
- Code blocks have language identifiers
- Lists are properly formatted
- Tables are properly formatted (if present)

**Line Length:**

- Root: ≤ 500 lines (configurable)
- Package: ≤ 300 lines (configurable)
- Flag violations with severity

**Organization:**

- Content is well-structured with clear sections
- Related information grouped together
- No redundant or duplicate content
- Imperative, lean instructions (no fluff)

#### 4.3 Content Quality

**Project/Package Overview:**

- Clearly states purpose
- Brief and focused (1-3 paragraphs)
- Not generic boilerplate
- Actually describes this specific project/package

**Commands Section:**

- Lists actual commands that work
- Includes clear descriptions
- No outdated commands
- Commands are relevant to AI assistant

**Architecture/Development Notes:**

- Provides useful context for development
- Not overly verbose
- Includes relevant file paths
- Mentions key patterns or conventions

**Design Doc References:**

If `requireDesignDocPointers: true`, validate:

- Design docs are referenced when appropriate
- References use correct format: `@./.claude/design/{module}/{doc}.md`
- Referenced files actually exist
- Clear guidance on when to load design docs

#### 4.4 Quality Checks (Strict Mode)

When `strict: true`, perform additional checks:

**Conciseness:**

- No unnecessarily verbose explanations
- Imperative instructions, not prose
- No marketing speak or sales language
- Focused on actionable information

**Relevance:**

- All content is relevant to AI assistant
- No human-only information (unless necessary)
- No outdated information
- Commands and paths are current

**Specificity:**

- Specific file paths, not vague references
- Actual command examples, not pseudocode
- Concrete patterns, not abstract principles
- Real constraints, not hypotheticals

**Design Doc Integration:**

- Design docs mentioned where they add value
- Not mentioned for trivial details
- Clear when-to-load guidance
- Pointers are up-to-date

#### 4.5 Cross-Reference Validation

If `check-refs: true`, validate:

**Design Doc References:**

- Extract all `@./.claude/design/...` references
- Verify each referenced file exists
- Check for broken paths
- Warn if design doc not in module's config

**File Path References:**

- Extract references to source files (e.g., `src/foo.ts`)
- Spot-check that paths exist
- Warn about likely outdated paths

**Command References:**

- Extract command examples
- Basic validation (no obvious typos)
- Check for deprecated commands

#### 4.6 Markdown Linting

Run markdown linter:

```bash
pnpm lint:md -- {file-path}
```

Report any linting errors with line numbers.

### 5. Report Validation Results

Generate validation report:

**Report Format:**

```markdown
# CLAUDE.md Validation Report

**Target:** {file-path|all}
**Files Validated:** {count}
**Status:** ✅ PASS / ⚠️  WARNINGS / ❌ FAIL

## Summary

- Errors: {count}
- Warnings: {count}
- Info: {count}

## Issues by File

### {file-path}

**Status:** ✅ PASS / ⚠️  WARNINGS / ❌ FAIL
**Lines:** {count} / {limit}
**Type:** Root / Package

#### Errors

- [Line X] Missing required section: {section}
- [Structure] Heading level skipped (H1 → H3)
- [References] Broken design doc reference: {path}

#### Warnings

- [Line X] Line limit exceeded ({actual} > {limit})
- [Content] Overview is verbose (350 words, recommend <200)
- [References] Design doc not referenced (observability.md exists)

#### Info

- Consider splitting into child CLAUDE.md files
- Add design doc pointer for {topic}
- Update command examples to use latest syntax

## Recommendations

1. {actionable fix recommendation}
2. {actionable fix recommendation}
```

### 6. Validation Rules Reference

#### Root CLAUDE.md Rules

| Rule | Validation |
| :--- | :--------- |
| Max lines | 500 (configurable) |
| Required sections | Project Overview, Commands, Architecture, Tooling |
| Design doc refs | Optional but recommended |
| Heading level | Must start with H1 |
| Organization | Logical section order |

#### Package CLAUDE.md Rules

| Rule | Validation |
| :--- | :--------- |
| Max lines | 300 (configurable) |
| Required sections | Package Overview, API/Exports, Development, Testing |
| Design doc refs | Required if design docs exist |
| File paths | Should reference package-relative paths |
| Scope | Package-specific, not general project info |

#### Severity Levels

- **ERROR**: Must be fixed (missing sections, broken refs, invalid markdown)
- **WARNING**: Should be fixed (line limit, quality issues, missing refs)
- **INFO**: Nice to have (optimization suggestions, style improvements)

## Error Messages

### Missing Required Section

```text
ERROR: Missing required section: {section}
- Expected: ## {section}
- File type: {Root|Package}
- Fix: Add section following CLAUDE.md template
```

### Line Limit Exceeded

```text
WARNING: File exceeds line limit
- Limit: {limit} lines
- Actual: {actual} lines
- Overage: {actual - limit} lines
- Fix: Split into child CLAUDE.md files or remove redundant content
```

### Broken Design Doc Reference

```text
ERROR: Referenced design doc does not exist
- Reference: @./.claude/design/{path}
- Fix: Create the design doc or fix the reference path
```

### Missing Design Doc Pointer

```text
WARNING: Design doc exists but not referenced in CLAUDE.md
- Design doc: .claude/design/{module}/{doc}.md
- Category: {category}
- Fix: Add reference in relevant section with when-to-load guidance
```

### Invalid Heading Hierarchy

```text
ERROR: Heading level skipped
- Line: {line}
- Found: H3
- Expected: H2 (after H1)
- Fix: Use proper heading progression (H1 → H2 → H3)
```

### Verbose Content

```text
WARNING: Section is verbose
- Section: {section}
- Word count: {count}
- Recommended: <{limit}
- Fix: Make content more concise and imperative
```

## Examples

### Example 1: Validate root CLAUDE.md

**User request:**

> Validate the root CLAUDE.md

**Execution:**

1. Load config for quality standards
2. Read CLAUDE.md
3. Check structure, formatting, content
4. Validate design doc references
5. Run markdown linter
6. Generate report

**Output:**

```markdown
# CLAUDE.md Validation Report

**Target:** CLAUDE.md
**Files Validated:** 1
**Status:** ⚠️  WARNINGS

## Summary

- Errors: 0
- Warnings: 2
- Info: 1

## Issues by File

### CLAUDE.md

**Status:** ⚠️  WARNINGS
**Lines:** 487 / 500
**Type:** Root

#### Errors

None found.

#### Warnings

- [Line 234] Design doc exists but not referenced (performance-observability.md)
- [Content] Commands section verbose (280 words, recommend <150)

#### Info

- Consider adding design doc pointer for build architecture

## Recommendations

1. Add reference to performance-observability.md in relevant section
2. Condense Commands section to focus on essentials
3. Add pointer to build-architecture.md with when-to-load guidance
```

### Example 2: Strict validation with errors

**User request:**

> Strict validation of pkgs/effect-type-registry/CLAUDE.md

**Execution:**

1. Load config
2. Read package CLAUDE.md
3. Perform strict validation
4. Check all references
5. Generate report

**Output:**

```markdown
# CLAUDE.md Validation Report

**Target:** pkgs/effect-type-registry/CLAUDE.md
**Files Validated:** 1
**Status:** ❌ FAIL

## Summary

- Errors: 3
- Warnings: 2
- Info: 1

## Issues by File

### pkgs/effect-type-registry/CLAUDE.md

**Status:** ❌ FAIL
**Lines:** 245 / 300
**Type:** Package

#### Errors

- [Line 12] Missing required section: Testing
- [Line 89] Broken design doc reference:
  @./.claude/design/effect-type-registry/caching.md
- [Structure] Heading level skipped (H1 → H3 at line 45)

#### Warnings

- [References] Design doc exists but not referenced (observability.md)
- [Content] Package Overview is generic boilerplate

#### Info

- Add when-to-load guidance for design doc references

## Recommendations

1. Add Testing section documenting test strategy
2. Fix broken reference: create caching.md or update reference
3. Fix heading hierarchy at line 45 (use H2 instead of H3)
4. Reference observability.md in Development Notes
5. Customize Package Overview with specific purpose and features
```

### Example 3: Validate all CLAUDE.md files

**User request:**

> Validate all CLAUDE.md files

**Execution:**

1. Find all CLAUDE.md files
2. Validate each file
3. Generate comprehensive report

**Output:**

```markdown
# CLAUDE.md Validation Report

**Target:** all
**Files Validated:** 4
**Status:** ⚠️  WARNINGS

## Summary

- Errors: 1
- Warnings: 5
- Info: 3

## Files by Status

- ✅ PASS: 2 files
- ⚠️  WARNINGS: 1 file
- ❌ FAIL: 1 file

## Issues by File

### CLAUDE.md (Root)

**Status:** ⚠️  WARNINGS
**Lines:** 487 / 500
**Type:** Root

#### Warnings

- [References] 2 design docs not referenced
- [Content] Commands section verbose

### pkgs/effect-type-registry/CLAUDE.md

**Status:** ❌ FAIL
**Lines:** 245 / 300
**Type:** Package

#### Errors

- [Line 12] Missing required section: Testing

### pkgs/rspress-plugin-api-extractor/CLAUDE.md

**Status:** ✅ PASS
**Lines:** 278 / 300
**Type:** Package

No issues found.

### website/CLAUDE.md

**Status:** ✅ PASS
**Lines:** 156 / 300
**Type:** Package

No issues found.

## Recommendations

1. Fix missing Testing section in effect-type-registry/CLAUDE.md
2. Add design doc references to root CLAUDE.md
3. Condense Commands section in root CLAUDE.md
```

## Special Cases

### New Packages

Packages without existing CLAUDE.md:

```text
INFO: No CLAUDE.md found for package
- Package: {package-name}
- Expected location: {path}/CLAUDE.md
- Recommendation: Create CLAUDE.md using package template
```

### Child CLAUDE.md Files

Some packages may have CLAUDE.local.md or other child files:

- Validate against package rules (not root rules)
- Check that parent CLAUDE.md references child
- Ensure child doesn't duplicate parent content

### Archived Modules

Modules marked as archived in config:

- Don't require up-to-date content
- Don't penalize for missing design doc refs
- Validate structure only
- Should have archival notice

## Success Criteria

A valid CLAUDE.md file has:

- ✅ All required sections present
- ✅ Proper markdown structure
- ✅ Within line limit
- ✅ Valid design doc references
- ✅ No markdown linting errors
- ✅ Concise, imperative content
- ✅ Up-to-date commands and paths

## Integration with Other Skills

Works well with:

- `/context-review` - Fix issues before validation
- `/context-update` - Update files based on validation
- `/context-split` - Split overlimit files
- `/design-validate` - Ensure referenced design docs are valid
- `/design-review` - Check design doc health

## CI/CD Integration

Can be integrated into workflows:

```bash
# Pre-commit hook
claude code --skill context-validate --args "all"

# CI pipeline
- name: Validate CLAUDE.md files
  run: claude code --skill context-validate --args "all --strict"
```

Exit codes:

- 0: All validations pass
- 1: Warnings present
- 2: Errors found
