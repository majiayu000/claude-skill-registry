---
name: file-name-wizard
description: Audit all filename and naming conventions in the codebase against CLAUDE.md standards and common patterns. Use when user asks to check naming conventions, audit filenames, find naming inconsistencies, or validate file naming patterns.
---

# Filename & Naming Convention Audit

## Instructions

Perform systematic audit of all filenames and naming conventions in the codebase to identify inconsistencies, anti-patterns, and violations of naming standards.

### Phase 1: Discovery & Standard Extraction

#### Step 1: Find All Files
Use Glob to identify all files in the codebase:
- Source files (`.ts`, `.tsx`, `.js`, `.jsx`, etc.)
- Config files
- Documentation files
- Test files

Create comprehensive todo list of all files to audit.

#### Step 2: Extract Naming Standards

Read all `CLAUDE.md` files in the repository:
- Root `CLAUDE.md` if exists
- Directory-specific `CLAUDE.md` files

Extract naming conventions:
- File naming patterns (kebab-case, PascalCase, etc.)
- Directory structure rules
- Component naming rules
- Utility/helper naming rules
- Test file naming rules
- Config file naming rules
- Constant/enum file naming rules

#### Step 3: Identify Implicit Patterns

Even without explicit CLAUDE.md rules, identify patterns:
- Most common naming convention in each directory
- Grouping patterns (e.g., `*.service.ts`, `*.controller.ts`)
- Organizational patterns (e.g., `components/`, `utils/`, `lib/`)

### Phase 2: Systematic File Audit

For EACH file in the todo list:

#### Step 1: Analyze Filename
- What is the current filename?
- What naming convention does it use?
- Is it descriptive and clear?
- Does it match its purpose/content?

#### Step 2: Check Against Standards

Compare to:
- Explicit CLAUDE.md rules for this directory
- Implicit patterns in the same directory
- Common naming conventions for file type
- Best practices for the framework/language

#### Step 3: Identify Issues

**Naming Convention Violations**:
- Wrong case (e.g., PascalCase when should be kebab-case)
- Mixed conventions (e.g., `userAuth.service.ts` mixing camelCase and dot notation)
- Inconsistent with directory pattern

**Clarity Issues**:
- Vague names (e.g., `utils.ts`, `helpers.ts`, `stuff.ts`)
- Overly verbose names
- Misleading names (content doesn't match name)
- Abbreviations without context

**Anti-Patterns**:
- Temporary names (e.g., `temp.ts`, `test.ts`, `new-*.ts`, `*-v2.ts`)
- Generic names (e.g., `index2.ts`, `common.ts`)
- Dated names (e.g., `old-*.ts`, `legacy-*.ts`)
- Feature flag names (e.g., `*-new.ts`, `*-enhanced.ts`)

**Organizational Issues**:
- File in wrong directory
- Missing grouping suffix (e.g., should be `*.service.ts`)
- Inconsistent with sibling files

#### Step 4: Check File Contents
Read the file to verify:
- Does filename accurately describe contents?
- Would a better name exist based on what's inside?
- Are there naming conventions violations inside (class names, etc.)?

#### Step 5: Record Findings

Store in memory:
```
File: path/to/filename.ts
Convention Used: camelCase
Should Be: kebab-case
Pattern: Violates directory convention
Issues:
- [Specific issue]
Suggested Name: [better-name.ts]
Severity: [HIGH|MEDIUM|LOW]
```

#### Step 6: Update Todo
Mark file as audited in todo list.

### Phase 3: Pattern Analysis

After auditing all files:

#### Step 1: Identify Systemic Issues
- Which directories have most inconsistencies?
- What naming patterns are most violated?
- Are there clusters of similar violations?

#### Step 2: Find Outliers
- Files that don't match any pattern
- One-off naming schemes
- Orphaned file types

#### Step 3: Detect Missing Standards
- Directories lacking clear naming conventions
- File types without established patterns
- Areas needing CLAUDE.md documentation

### Phase 4: Generate Report

Create report at `.audits/naming-audit-[timestamp].md`:

```markdown
# Filename & Naming Convention Audit
**Date**: [timestamp]
**Files Audited**: X
**Issues Found**: Y

---

## Executive Summary
- **Critical Issues**: X (blocks consistency)
- **High Priority**: Y (major violations)
- **Medium Priority**: Z (minor inconsistencies)
- **Low Priority**: W (suggestions)

**Most Problematic Directory**: [path] (X issues)

---

## Issues by Severity

### CRITICAL: Convention Violations

#### Temporary/Migration Filenames
- `src/services/auth-v2.ts` - Migration file still in use
  - **Violates**: No version suffixes rule
  - **Suggested**: `src/services/auth.ts` (replace old one)

- `src/utils/new-logger.ts` - Temporary naming
  - **Violates**: No "new-" prefix rule
  - **Suggested**: `src/utils/logger.ts`

#### Wrong Case Convention
- `src/components/UserProfile.tsx` - PascalCase
  - **Directory Standard**: kebab-case
  - **Suggested**: `src/components/user-profile.tsx`

### HIGH: Consistency Violations

#### Inconsistent with Directory Pattern
- `src/services/database.ts` - Missing `.service.ts` suffix
  - **Pattern**: All files in directory use `*.service.ts`
  - **Suggested**: `src/services/database.service.ts`

#### Vague/Generic Names
- `src/utils/helpers.ts` - Too generic
  - **Contains**: String manipulation functions
  - **Suggested**: `src/utils/string-helpers.ts`

### MEDIUM: Clarity Issues

#### Misleading Names
- `src/lib/validator.ts` - Named as single purpose
  - **Contains**: Multiple validators and formatters
  - **Suggested**: Split or rename to `validators.ts`

### LOW: Suggestions

#### Verbose Names
- `src/components/user-authentication-form-component.tsx`
  - **Redundant**: "component" suffix in components dir
  - **Suggested**: `src/components/user-auth-form.tsx`

---

## Issues by Directory

### src/services/ (12 issues)
- **Pattern**: Should use `*.service.ts` suffix
- **Violations**:
  - `database.ts` (missing suffix)
  - `auth-helper.ts` (wrong suffix)
  - `userService.ts` (wrong case)

### src/components/ (8 issues)
- **Pattern**: kebab-case without suffix
- **Violations**:
  - `UserProfile.tsx` (PascalCase)
  - `button-component.tsx` (redundant suffix)

[Continue for all directories]

---

## Pattern Analysis

### Most Common Violations
1. **Mixed case conventions** - 15 files
2. **Missing pattern suffixes** - 12 files
3. **Generic names** - 8 files
4. **Temporary names** - 5 files

### Directories Lacking Standards
- `src/lib/` - No clear convention (mix of all patterns)
- `src/shared/` - Inconsistent organization
- `tools/` - No established pattern

### Emerging Anti-Patterns
- Version suffixes appearing (`*-v2`, `*-new`)
- Component files with "component" in name
- Service files without `.service.ts` suffix

---

## CLAUDE.md Coverage

### Documented Standards
- ✅ `src/components/` - Documented in `src/CLAUDE.md`
- ✅ `src/services/` - Documented in `src/CLAUDE.md`
- ❌ `src/lib/` - No documentation
- ❌ `src/utils/` - No documentation
- ❌ `tools/` - No documentation

### Missing Documentation Needed
- File naming conventions for `src/lib/`
- Grouping patterns for utilities
- Test file naming standards
- Config file organization rules

---

## Statistics

**By Issue Type**:
- Case Violations: X
- Pattern Violations: Y
- Generic Names: Z
- Temporary Names: W
- Misleading Names: V

**By Severity**:
- Critical: X
- High: Y
- Medium: Z
- Low: W

**By File Type**:
- TypeScript: X issues
- React Components: Y issues
- Test Files: Z issues
- Config Files: W issues

---

## Detailed File List

### Critical Issues
| File | Issue | Suggested Name | Reason |
|------|-------|----------------|--------|
| `src/auth-v2.ts` | Version suffix | `src/auth.ts` | Migration files not allowed |
| `src/UserProfile.tsx` | Wrong case | `src/user-profile.tsx` | Directory uses kebab-case |

### High Priority Issues
[Similar table]

### Medium Priority Issues
[Similar table]

### Low Priority Issues
[Similar table]
```

### Phase 5: Summary for User

Provide concise summary:

```markdown
# Naming Convention Audit Complete

## Overview
- **Files Audited**: X
- **Issues Found**: Y
- **Directories with Issues**: Z

## Critical Issues (Immediate Action)
- X files with version/migration suffixes (`*-v2`, `*-new`)
- Y files with wrong case convention
- Z files in wrong locations

## Most Problematic Areas
1. **src/services/** - 12 issues (missing `.service.ts` suffix)
2. **src/components/** - 8 issues (case convention mix)
3. **src/lib/** - 6 issues (no clear standard)

## Top Violations
- Mixed case conventions: 15 files
- Missing pattern suffixes: 12 files
- Generic names: 8 files

## Missing Standards
- `src/lib/` lacks naming documentation
- `src/utils/` needs pattern definition
- Test files need naming standard

**Full Report**: `.audits/naming-audit-[timestamp].md`
```

## Critical Principles

- **NEVER EDIT FILES** - This is audit only, not renaming
- **NEVER SKIP FILES** - Audit every file in todo list
- **DO READ CLAUDE.MD** - Extract explicit standards first
- **DO IDENTIFY PATTERNS** - Find implicit conventions
- **DO BE CONSISTENT** - Apply same standards across similar files
- **DO CHECK CONTENTS** - Verify name matches file contents
- **DO TRACK PROGRESS** - Update todo list as you audit
- **DO FLAG ANTI-PATTERNS** - Especially temporary/migration names

## Success Criteria

A complete naming audit includes:
- All files in codebase audited
- All CLAUDE.md standards extracted and applied
- Implicit patterns identified for each directory
- Violations categorized by severity
- Systemic issues identified
- Missing standards documented
- Structured report generated
- Statistics and trends analyzed
