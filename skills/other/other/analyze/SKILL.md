---
name: analyze
description: "Analyze consistency across spec, plan, tasks, and checklist. Use before implementation. Triggers on: analyze consistency, check artifacts, validate feature."
---

# Cross-Artifact Consistency Analyzer

Validate consistency across feature artifacts before implementation.

---

## SpecKit Workflow

This skill is **Step 5 of 6** in the Relentless workflow:

specify → plan → tasks → convert → **analyze** → implement

Prerequisites (ALL must exist):
- `spec.md` - Feature specification
- `plan.md` - Technical implementation plan
- `tasks.md` - User stories and tasks
- `prd.json` - Converted PRD with routing metadata (run convert first)
- `checklist.md` - Quality validation checklist (recommended)

Purpose:
- Validate consistency across ALL artifacts
- Catch gaps before implementation begins
- **Ensure TDD and routing compliance**
- **Verify quality gates are defined**

---

## The Job

1. Read all feature artifacts
2. Check for consistency issues
3. **Validate TDD compliance**
4. **Validate routing metadata**
5. **Validate quality gates**
6. Validate against constitution
7. Generate analysis report

---

## Files to Analyze

Required:
- `relentless/constitution.md`
- `relentless/features/NNN-feature/spec.md`
- `relentless/features/NNN-feature/plan.md`
- `relentless/features/NNN-feature/tasks.md`
- `relentless/features/NNN-feature/prd.json`
- `relentless/features/NNN-feature/checklist.md`

Optional:
- `relentless/features/NNN-feature/progress.txt`

---

## Validation Checks

### 1. Completeness
- [ ] All functional requirements from spec have tasks
- [ ] All tasks reference spec requirements
- [ ] Plan addresses all spec requirements
- [ ] Checklist covers all tasks

### 2. TDD Compliance Validation (MANDATORY)

Verify that:
- [ ] Every story in tasks.md has test acceptance criteria
- [ ] Test specifications exist in plan.md
- [ ] Checklist includes test validation items
- [ ] No stories marked "tests optional"
- [ ] Given/When/Then format used in acceptance criteria

**Flag as CRITICAL if TDD requirements are missing.**

### 3. Routing Metadata Validation (MANDATORY)

Verify that prd.json contains for EVERY story:
- [ ] `routing.complexity` - simple/medium/complex/expert
- [ ] `routing.harness` - claude/gemini/codex/opencode/amp/droid
- [ ] `routing.model` - specific model name
- [ ] `routing.mode` - free/cheap/good/genius
- [ ] `routing.estimatedCost` - cost in USD

Also verify:
- [ ] Routing preference in spec.md matches prd.json routing mode
- [ ] Complexity classifications are reasonable for story scope

**Flag as CRITICAL if routing metadata is missing.**

### 4. Quality Gates Validation (MANDATORY)

Verify that ALL THREE quality gates are present in acceptance criteria:
- [ ] Typecheck requirement (`bun run typecheck` passes with 0 errors)
- [ ] Lint requirement (`bun run lint` passes with 0 errors AND 0 warnings)
- [ ] Test requirement (`bun test` passes)

**Flag as CRITICAL if any quality gate is missing.**

### 5. Constitution Compliance
- [ ] Plan follows MUST rules
- [ ] Tasks include required quality checks
- [ ] Testing requirements met
- [ ] Security requirements addressed
- [ ] No `any` types planned

### 6. Dependency Consistency
- [ ] Task dependencies are valid (no circular refs)
- [ ] Referenced dependencies exist
- [ ] Dependency order makes sense

### 7. Scope Consistency
- [ ] Plan doesn't include out-of-scope items
- [ ] Tasks match plan scope
- [ ] No scope creep in checklist

### 8. Data Model Consistency
- [ ] Entities mentioned in spec are in plan
- [ ] Plan data models match spec requirements
- [ ] Tasks create required entities

### 9. API Consistency
- [ ] Endpoints in plan match spec scenarios
- [ ] Tasks implement all planned endpoints
- [ ] Checklist validates all endpoints

### 10. Testing Coverage
- [ ] Each task has test acceptance criteria
- [ ] Checklist includes test validation
- [ ] Test types match constitution requirements

---

## Issue Severity

**CRITICAL:** Blocks implementation - MUST fix before proceeding
- Constitution MUST rule violations
- **Missing TDD requirements**
- **Missing routing metadata in prd.json**
- **Missing quality gate requirements**
- Circular dependencies
- Missing required artifacts

**WARNING:** Should fix before implementation
- Incomplete coverage of requirements
- Ambiguous acceptance criteria
- Missing test criteria for some stories
- Routing preference mismatch (spec vs prd.json)

**INFO:** Nice to have
- Style inconsistencies
- Minor gaps in checklist
- Optimization opportunities

---

## Report Format

Use the template at `templates/analysis-report.md`:

```markdown
# Consistency Analysis Report

**Feature:** [feature-name]
**Date:** [date]
**Status:** [PASS | FAIL | WARNINGS]

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Completeness | ✅/❌ | [count] |
| TDD Compliance | ✅/❌ | [count] |
| Routing Validation | ✅/❌ | [count] |
| Quality Gates | ✅/❌ | [count] |
| Constitution | ✅/❌ | [count] |
| Dependencies | ✅/❌ | [count] |

## Critical Issues

### CRIT-001: [Issue Title]
**Location:** [file]
**Details:** [description]
**Fix:** [required action]

## Recommendations

1. [Action item 1]
2. [Action item 2]

**Next Step:** /relentless.implement (if PASS) or fix issues (if FAIL)
```

---

## Output

1. Save analysis report to `relentless/features/NNN-feature/analysis-report.md`
2. Update progress.txt with analysis results
3. Report:
   - Overall status: PASS/FAIL/WARNINGS
   - Critical issues count
   - TDD compliance: PASS/FAIL
   - Routing validation: PASS/FAIL
   - Quality gates: PASS/FAIL
   - Next step: `/relentless.implement` or fix issues

---

## Notes

- Run before starting implementation
- Constitution compliance is non-negotiable
- **TDD compliance is non-negotiable**
- **Routing metadata is required for all stories**
- **Quality gates (typecheck, lint, test) are mandatory**
- Fix critical issues immediately
- Warnings can sometimes be deferred
- Re-run after making fixes
