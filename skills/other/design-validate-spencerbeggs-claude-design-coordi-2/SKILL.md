---
name: design-validate
description: Validate design doc structure and frontmatter. Use when checking design docs for compliance, ensuring proper formatting, or verifying metadata before commits.
allowed-tools: Read, Glob, Bash
agent: design-doc-agent
---

# Design Documentation Validation

Validates design documentation files for structure, frontmatter, and quality compliance.

## Overview

This skill validates design documentation by:

1. Reading the design configuration
2. Finding design docs for the specified module
3. Validating YAML frontmatter structure and values
4. Checking for required sections
5. Validating cross-references and links
6. Reporting issues with severity levels
7. Providing actionable fix recommendations

## Quick Start

**Basic validation:**

```bash
/design-validate effect-type-registry
```

**Validate specific file:**

```bash
/design-validate effect-type-registry cache-optimization.md
```

**Strict mode (additional quality checks):**

```bash
/design-validate all --strict
```

## How It Works

### 1. Parse Parameters

- `module`: Module name to validate (or "all" for all modules) [REQUIRED]
- `file`: Specific file to validate (default: all files in module)
- `strict`: Enable strict mode with additional checks (default: false)

### 2. Load Configuration

Read `.claude/design/design.config.json` to get:

- Module configuration and paths
- Quality standards
- Required frontmatter fields
- Minimum section requirements

### 3. Find and Validate Documents

Use Glob to find design docs, then for each file:

**Frontmatter Validation:**

- Validate YAML syntax
- Check all required fields exist
- Verify field values are correct type and format
- Validate dates are in order (created ≤ updated ≤ last-synced)
- Check status matches completeness level

**Structure Validation:**

- Verify required sections exist
- Check TOC matches headings (if required)
- Validate document title

**Cross-Reference Validation:**

- Check paths in `related` array exist
- Check paths in `dependencies` array exist
- Check paths in `implementation-plans` array exist (if present)
- Validate bidirectional plan-design links
- Validate internal markdown links

**Quality Checks (strict mode only):**

- Completeness accuracy
- Status appropriateness
- Documentation quality (section length, content depth)

### 4. Report Results

Generate a validation report with issues categorized by severity:

- **ERROR**: Must be fixed (blocks)
- **WARNING**: Should be fixed
- **INFO**: Nice to have

## Supporting Documentation

When you need detailed information about validation rules or error
messages, load the appropriate supporting file:

### For Frontmatter Rules

See [frontmatter-rules.md](frontmatter-rules.md) for:

- Complete field requirements table
- Status-completeness matrix
- Date validation rules
- Category validation
- Required sections by category

**Load when:** Working with frontmatter validation or debugging field errors

### For Error Messages

See [error-messages.md](error-messages.md) for:

- All error message formats
- Fix instructions for each error type
- Common validation failures

**Load when:** User has validation errors and needs to fix them

### For Usage Examples

See [examples.md](examples.md) for:

- Complete usage scenarios
- Example outputs for different validation states
- Multi-module validation examples

**Load when:** User wants to see concrete examples of validation output

## Validation Flow

```text
1. Parse user parameters
   ↓
2. Load design.config.json
   ↓
3. Find module(s) and design docs
   ↓
4. For each doc:
   - Validate frontmatter
   - Check structure
   - Verify cross-references
   - Run quality checks (if strict)
   ↓
5. Generate report with:
   - Summary stats
   - Issues by file
   - Recommendations
```

## Exit Codes

- ✅ **PASS**: No errors found
- ⚠️  **WARNINGS**: Warnings but no errors
- ❌ **FAIL**: Errors found, must fix

## Plan Link Validation

Design docs can reference implementation plans via the
`implementation-plans` field in frontmatter. This skill validates:

### Plan Reference Validation

- Plans listed in `implementation-plans` array exist in `.claude/plans/`
- Plan paths are relative (e.g., `../plans/my-plan.md`)
- Plans are not archived (warning if in `_archive/`)

### Bidirectional Link Validation

- If a design doc references a plan, verify plan exists
- If a plan references a design doc (via `design-docs` field), verify
  design doc references the plan back
- Warn if links are unidirectional (missing backlink)

**Example validation output:**

```text
✓ Design doc: effect-type-registry/observability.md
  ✓ Plan reference: ../plans/observability-phase-2.md (exists)
  ✓ Bidirectional link: Plan references this design doc

⚠ Design doc: effect-type-registry/cache-optimization.md
  ✓ Plan reference: ../plans/cache-optimization-plan.md (exists)
  ⚠ Unidirectional link: Plan does not reference this design doc
  Fix: Add 'effect-type-registry/cache-optimization.md' to plan's
       design-docs array
```

## Integration

This skill integrates with:

- `/design-init` - Validate newly created docs
- `/design-update` - Validate after updates
- `/design-sync` - Validate after syncing with code
- `/plan-create` - Validate plan-design links when creating plans
- `/plan-validate` - Complementary validation for plans
- CI/CD pipelines - Pre-commit or PR validation

### Standalone Script

A standalone bash validation script is available at:

```bash
.claude/skills/design-validate/scripts/validate.sh [module|all]
```

This script can be:

- Run directly from command line
- Integrated into CI/CD pipelines
- Used in pre-commit hooks
- Called from other automation tools

Exit codes:

- `0` - All validations pass (no errors, no warnings)
- `0` - Pass with warnings (no errors, but warnings present)
- `1` - Validation failed (errors found)

## Success Criteria

A design doc passes validation if:

- ✅ Valid YAML frontmatter with all required fields
- ✅ Field values meet validation rules
- ✅ Required sections present
- ✅ Cross-references exist (related, dependencies, plans)
- ✅ Plan links are bidirectional (if implementation-plans present)
- ✅ Markdown linting passes
- ✅ Status matches completeness level
