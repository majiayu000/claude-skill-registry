---
name: audit
description: Run comprehensive codebase audit for gaps, deprecated code, TODOs, FIXMEs, architectural anti-patterns, type issues, and code smells. Use when user asks to audit code, find issues, check code quality, or identify architectural problems.
---

# Codebase Audit

## Instructions

Perform a comprehensive, systematic audit of the codebase to identify quality issues, architectural problems, and technical debt.

### Phase 1: Discovery & Planning

1. **Identify scope** - Determine which files/directories to audit based on user request
2. **Create comprehensive file list** - Use Glob to find all relevant files
3. **Initialize todo list** - Create a todo with one item per file to audit
4. **Set up audit report** - Create structured markdown report at `.audit/audit-report-[timestamp].md`

### Phase 2: Automated Analysis

Run automated tools to supplement manual review:
- TypeScript compiler diagnostics
- ESLint (if configured)
- Grep for common patterns: TODO, FIXME, HACK, XXX, @deprecated

### Phase 3: Systematic File Review

For EACH file in the todo list:

1. **Read and analyze** the file thoroughly
2. **Check for issues** in these categories:
   - **Deprecations**: Deprecated APIs, patterns, or code marked for removal
   - **TODOs/FIXMEs**: Unfinished work or known issues
   - **Architectural anti-patterns**:
     - God objects/classes
     - Circular dependencies
     - Tight coupling
     - Violation of SOLID principles
     - Inconsistent patterns
   - **Type issues**:
     - Use of `any` or `unknown`
     - Missing type annotations
     - Incorrect type usage
     - Type casts that hide issues
   - **Code smells**:
     - Duplicated code
     - Long functions/classes
     - Complex conditionals
     - Dead code
     - Magic numbers/strings
     - Poor naming

3. **Assign severity** to each finding:
   - **CRITICAL**: Breaks functionality, security issues, data corruption risks
   - **HIGH**: Architectural violations, major maintainability issues
   - **MEDIUM**: Code smells, minor anti-patterns, missing types
   - **LOW**: Style issues, minor TODOs, cosmetic improvements

4. **Check for cross-file patterns** - As you review, note patterns that appear across multiple files

5. **Update report** - Add findings to the structured report

6. **Mark file as completed** in todo list

### Phase 4: Cross-File Analysis

After reviewing all individual files:

1. **Identify systemic patterns** - Issues that appear across multiple files
2. **Architectural assessment** - Overall system architecture health
3. **Dependency analysis** - Check for circular dependencies or coupling issues
4. **Consistency check** - Verify naming conventions, patterns are followed

### Phase 5: Validation & Summary

1. **Run final checks**:
   - TypeScript type check (`tsc --noEmit` or similar)
   - Linting (`npm run lint` or similar)
   - Build process if applicable

2. **Generate executive summary**:
   - Total issues by category
   - Total issues by severity
   - Top 10 most critical findings

### Audit Report Structure

```markdown
# Audit Report - [Date]

## Executive Summary
- **Files Audited**: X
- **Total Issues Found**: Y
- **Critical**: A | **High**: B | **Medium**: C | **Low**: D

## Top 10 Critical Findings
1. [Issue description] - Severity: CRITICAL - File: path/to/file.ts:line

## Issues by Category

### Deprecations
- [Issue] - Severity - File:line

### TODOs/FIXMEs
- [Issue] - Severity - File:line

### Architectural Anti-Patterns
- [Issue] - Severity - File:line

### Type Issues
- [Issue] - Severity - File:line

### Code Smells
- [Issue] - Severity - File:line

## Cross-File Patterns
- [Pattern description and affected files]

## Automated Tool Results
- TypeScript diagnostics summary
- ESLint results summary
```

## Critical Principles

- **NEVER skip files** - Audit every file in the todo list
- **NEVER edit files during audit** - This is read-only analysis
- **NEVER provide recommendations** - Only identify and report problems
- **NEVER create action plans** - That's a separate responsibility
- **DO use memory/pinboard** - Store context as you discover patterns
- **DO be thorough** - Think critically about each file
- **DO be objective** - Report what you find, not what to do about it
- **DO track progress** - Keep todo list updated in real-time
- **DO find all relevant files** - If you discover new files that should be audited, add them to the todo

## Dynamic File Discovery

If during audit you discover additional files that should be reviewed:
1. Add them to the todo list immediately
2. Continue systematic review
3. Ensure no stone is left unturned
