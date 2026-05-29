---
name: whole-reviewer
description: |
  Post-editing validation for Whole documentation. Use when: (1) After completing edits,
  (2) Before marking task complete, (3) Validating cross-reference updates,
  (4) Verifying bilingual consistency, (5) Final quality check.
version: 2.1.0
license: MIT
allowed-tools:
  - Grep
  - Read
  - Bash
  - Task
metadata:
  author: "Whole Project"
  category: "documentation"
  updated: "2026-01-02"
---

# Whole Content Reviewer

## Purpose
Validate all changes meet quality standards before completion.

## Integration with Agents

### When to Invoke Agents
Use Task tool to invoke specialized validation agents:

```javascript
// For comprehensive content validation
Task(subagent_type: 'whole-content-validator', prompt: 'Validate CF[N] content structure and compliance')

// For cross-reference deep analysis
Task(subagent_type: 'whole-cross-reference', prompt: 'Validate cross-references in CF[N] and build reference graph')

// For complex translation validation
Task(subagent_type: 'whole-translator', prompt: 'Review bilingual consistency and cultural adaptation in CF[N]')
```

### When NOT to Use Agents
- Simple format checks → Use validation scripts in `scripts/`
- Basic concept counting → Use Grep directly
- Quick structure validation → Run scripts first (faster)
- Single cross-reference check → Manual verification

## Review Checklist

### Content Integrity
- [ ] No content deleted without approval
- [ ] All additions follow 4-point structure (minimum 4, can have more)
- [ ] Bilingual format consistent (`#### **[num]. English - Tiếng Việt**`)
- [ ] Use **whole-content-validator** agent for automated checks

### Cross-Reference Integrity
- [ ] All refs updated bidirectionally (A→B requires B→A)
- [ ] No orphaned refs
- [ ] Correct format used (`→ **Liên kết:**`)
- [ ] Use **whole-cross-reference** agent for graph analysis

### Quality Standards
- [ ] Vietnamese culturally authentic (not literal translation)
- [ ] English conceptually precise
- [ ] Examples relevant and clear
- [ ] Use **whole-translator** agent for terminology consistency

## Verification Protocol

### Phase 1: Automated Validation
Run validation scripts:
```bash
# Comprehensive validation (recommended first)
node .claude/skills/whole-regrouper/scripts/validate-regroup.js [funcNum]

# Detailed validation suite
node .claude/skills/whole-editor/scripts/validate-structure.js [funcNum]
node .claude/skills/whole-editor/scripts/bilingual-check.js [funcNum]
node .claude/skills/whole-editor/scripts/check-cross-refs.js [funcNum]
```

### Phase 2: Agent-Based Deep Analysis
For complex validations or after major edits:
1. **Invoke whole-content-validator** - Get comprehensive validation report
2. **Invoke whole-cross-reference** - Analyze reference graph and connectivity
3. **Invoke whole-translator** (if needed) - Review terminology consistency

### Phase 3: Manual Review
1. Compare before/after sections
2. Validate each change type
3. Check cross-ref consistency
4. Verify bilingual alignment
5. Confirm structure preservation

## Report Format

```markdown
# Review Report: CHỨC NĂNG [N]

## Changes Applied
- Additions: [N] concepts
- Modifications: [N] concepts
- Cross-ref updates: [N] links
- Groups reorganized: [N] groups

## Automated Validation Results

### Scripts Executed:
- ✅ validate-regroup.js: PASS (0 issues)
- ✅ validate-structure.js: PASS (0 issues)
- ✅ bilingual-check.js: PASS (0 issues)
- ⚠️ check-cross-refs.js: WARNING (2 orphaned refs)

### Agent Validation:
- ✅ **whole-content-validator**: PASS
  - 15 concepts validated
  - 23 cross-references checked
  - 0 critical issues, 2 warnings

- ⚠️ **whole-cross-reference**: WARNINGS
  - 5 orphaned references (fix recommended)
  - Reference graph: 3 high-connectivity concepts identified
  - No broken links

## Manual Validation Results
- ✅ Content integrity preserved
- ✅ Cross-ref format correct
- ✅ Quality standards met

## Issues Found

### Critical (Must fix before commit):
*None*

### Warnings (Fix recommended):
1. CF[N] Concept 5 → CF12 Concept 3 missing reciprocal link
2. CF[N] Concept 8 → CF25 Concept 1 missing reciprocal link

### Info:
- 3 high-connectivity concepts could benefit from additional cross-domain links

## Recommendations
1. Add reciprocal cross-references for orphaned links
2. Consider strategic link additions suggested by whole-cross-reference agent
3. Review terminology consistency in next editing session

## Approval Status
✅ **APPROVED** (with warnings - fix in next session)

---
**Reviewer**: whole-reviewer v2.1.0
**Validation Scripts**: v1.0.0
**Agents Invoked**: whole-content-validator, whole-cross-reference
**Date**: [timestamp]
```

## Agent Integration Guide

### whole-content-validator
**When to use**: After any edit to validate structure, bilingual format, and compliance
**Command**: `Task(subagent_type='whole-content-validator', prompt='Validate CF[N]')`
**Expected output**: Comprehensive validation report with PASS/FAIL status

### whole-cross-reference
**When to use**: When editing cross-references or need reference graph analysis
**Command**: `Task(subagent_type='whole-cross-reference', prompt='Analyze cross-references in CF[N]')`
**Expected output**: Reference graph, orphaned links, strategic suggestions

### whole-translator
**When to use**: When reviewing bilingual consistency or complex translations
**Command**: `Task(subagent_type='whole-translator', prompt='Review terminology consistency in CF[N]')`
**Expected output**: Translation report, terminology glossary, consistency analysis

## Critical Rules

### ✅ MUST
- Run validation scripts before invoking agents (scripts are faster)
- Use agents for deep analysis, not simple checks
- Document agent findings in review report
- Fix critical issues before approval
- Use shared utilities from `.claude/skills/shared`

### ❌ NEVER
- Skip validation scripts
- Approve with critical issues
- Modify content (review only)
- Invoke agents unnecessarily (prefer scripts for simple checks)
