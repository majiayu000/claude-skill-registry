---
name: review-code
description: >-
  Perform systematic code review following project standards.
  Use when reviewing pull requests, analyzing code quality, checking for
  patterns compliance, or auditing code changes.
  Invoked by: "code review", "review PR", "review changes", "audit code".
---

# Code Review Process SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

---

## Overview

### Purpose
Systematic analysis of branch/feature changes to identify gaps, inconsistencies, and architectural violations. Ensures code quality, pattern compliance, and cross-layer completeness before merge.

### When to Use
**ALWAYS**: Branch refactorings, feature completions, pre-merge quality gates, architectural changes
**SKIP**: Simple typo fixes, doc-only changes, emergency hotfixes

---

## Process Workflow

### Flow Diagram
```
[Commit History Analysis] --> [Review Planning] --> [Detailed Review] --> [Report Generation]
        |                           |                      |                     |
   15-30 min                   10-20 min              30-60 min             15-30 min
```

### Phase Summary
| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Commit History Analysis | 15-30 min | Commit analysis summary |
| 2. Review Planning | 10-20 min | Review plan with checklist |
| 3. Detailed Code Review | 30-60 min | Findings log |
| 4. Report Generation | 15-30 min | Final review report |

**Total Duration**: 60-120 minutes

---

## Key Principles

1. **Systematic Analysis** - Methodical commit-by-commit review, document all findings
2. **Context-Aware** - Understand intent, review changes in relation to each other
3. **React Native Best Practices** - Verify mobile patterns, performance, platform compatibility
4. **Completeness Verification** - Check all layers updated (components, screens, Redux, navigation, tests)
5. **Pattern Consistency** - Follow established codebase patterns
6. **Constructive Feedback** - Actionable findings with context and examples
7. **Platform Awareness** - Verify iOS and Android compatibility

---

## Phase 1: Commit History Analysis

**Objective**: Understand change progression
**Duration**: 15-30 minutes

### Commands
```bash
# View commit history
git log --oneline --graph main..HEAD
git log --stat main..HEAD

# View affected files
git diff --name-only main...HEAD
git diff --stat main...HEAD
```

### Steps
1. **Review git log** - Analyze commits, identify patterns
2. **Map affected components** - Group by layer
3. **Identify change relationships** - Find cascading changes, potential gaps

### Change Relationship Checklist
- Component changed --> Tests updated?
- Redux slice modified --> Selectors updated?
- Screen added --> Navigation updated?
- Type changed --> All usages updated?

---

## Phase 2: Review Planning

**Objective**: Create structured review plan
**Duration**: 10-20 minutes

### Priority Levels
- **High**: Redux state, navigation, core components
- **Medium**: Screens, utils
- **Low**: Docs, styles

### Review Order
```
Types --> Redux --> Components --> Screens --> Navigation --> Utils --> Tests
```

### Quick Checklist

See [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md) for detailed checklist.

| Layer | Key Checks |
|-------|------------|
| Types | Correct definitions, no `any`, proper interfaces |
| Redux | State structure, actions/reducers patterns, selectors, migrations |
| Components | Props typed, patterns followed, accessibility |
| Screens | Navigation props, safe area, platform-specific code |
| Navigation | Routes defined, params typed, deep linking |
| Utils | Functions typed, error handling, edge cases |
| Tests | New/modified tests present, edge cases, both platforms |

---

## Phase 3: Detailed Code Review

**Objective**: Execute review, identify gaps/issues
**Duration**: 30-60 minutes

### Review Commands
```bash
# Type definitions
git diff main...HEAD -- src/types/

# Redux state
git diff main...HEAD -- src/store/

# Components
git diff main...HEAD -- src/components-next/

# Screens
git diff main...HEAD -- src/screens/

# Navigation
git diff main...HEAD -- src/navigation/

# Tests
git diff main...HEAD -- __tests__/ src/**/*.test.ts src/**/*.test.tsx
```

### Severity Levels

| Icon | Severity | Action |
|------|----------|--------|
| :rotating_light: | **Critical** | Must fix before merge |
| :warning: | **Major** | Should fix before merge |
| :bulb: | **Minor** | Can defer |

### Cross-Layer Completeness

For each change, verify:
- Type change --> All usages updated
- Redux change --> Components using it updated
- Component change --> Tests updated
- Screen change --> Navigation updated

---

## Phase 4: Report Generation

**Objective**: Compile actionable final report
**Duration**: 15-30 minutes

### Report Structure

Use template: [REVIEW_REPORT_TEMPLATE.md](REVIEW_REPORT_TEMPLATE.md)

```markdown
# Code Review Report: <Branch>

## Executive Summary
- Overall: PASS / CONDITIONAL PASS / FAIL
- Strengths: [list]
- Critical issues: [count]
- Recommendation: [go/no-go]

## Findings Summary
- Total: X (Y critical, Z major, W minor)

## Detailed Findings
### Critical (must fix)
### Major (should fix)
### Minor (can defer)

## Action Items
- Must Do: [tasks]
- Should Do: [tasks]
- Can Defer: [tasks]
```

---

## Quick Reference

### Git Commands
```bash
# Commit analysis
git log --oneline --graph main..HEAD
git log --stat main..HEAD

# File changes
git diff --name-only main...HEAD
git diff --stat main...HEAD

# Diffs
git diff main...HEAD -- path/to/file.tsx
git show <commit-sha>

# Search
git log -p -S "search_term" main..HEAD
git log --grep="pattern" main..HEAD
```

### Search Patterns
```bash
# Types
Glob: "src/types/**/*.ts"
Grep: "interface|type"

# Redux
Glob: "src/store/**/*.ts"
Grep: "createSlice|createAction"

# Components
Glob: "src/components-next/**/*.tsx"
Grep: "export.*Component"

# Screens
Glob: "src/screens/**/*.tsx"
Grep: "Screen.*="

# Tests
Glob: "**/*.test.ts*"
Grep: "describe|it|test"
```

### Minimum Review Time (30 min)
| Layer | Time |
|-------|------|
| Types | 5 min |
| Redux | 5 min |
| Components | 5 min |
| Screens | 5 min |
| Navigation | 5 min |
| Tests | 5 min |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Too many commits | Group by theme, focus on key commits, request squashing |
| Unclear commit messages | Read diffs (`git show <sha>`), ask author |
| Missing cross-layer changes | Use systematic checklist, search with Grep |
| Review fatigue | Take breaks (45-min chunks), split sessions |
| Platform-specific issues | Verify both iOS and Android tested |

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/dev-feature` | Feature workflow | During Phase 6 validation |
| `/test` | Mobile testing | After code review |
| `/git-pr` | Create PR | After review passes |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
