---
name: rules-doctor
description: Scan .claude/rules/ for broken paths, coverage gaps, and cross-reference issues
user-invocable: true
disable-model-invocation: true
---

# /rules-doctor — Rules Health Scanner

Audit `.claude/rules/` for integrity issues.

## Checks

### 1. Broken File Paths
For every file path referenced in `.claude/rules/*.md`:
- Verify the target file exists
- Flag broken references

### 2. Anti-Pattern Coverage
Read `.claude/rules/anti-patterns.md` (the index file):
- Verify all domain files listed in the table exist
- Check each domain file has at least one DO/DON'T table
- Compare technologies in stack (CLAUDE.md line 3) against covered technologies

### 3. Hook Cross-References
For each hook in `.claude/settings.json`:
- Verify the `.sh` file exists
- Check the hook script references relevant rules files (if applicable)
- Flag hooks without corresponding documentation

### 4. Skill-Rules Alignment
For skills that enforce rules (e.g., tdd-workflow references conventions):
- Verify referenced rules files exist
- Check for stale version-specific mentions (e.g., "tRPC v10" when we use v11)

### 5. Duplicate/Conflicting Rules
Search for contradictory guidance across rules files:
- Same topic covered in multiple files with different advice
- Overlapping DO/DON'T entries

## Output

```
## Rules Doctor Report

### Broken References (X)
- anti-patterns.md:15 → `anti-patterns-payments.md` (MISSING)

### Coverage Gaps
- Stack includes "Stripe" but no anti-patterns-stripe.md

### Hook Issues (X)
- settings.json references `check-foo.sh` (MISSING)

### Stale Versions (X)
- conventions.md mentions "tRPC v10" (should be v11)

### Status: HEALTHY / NEEDS ATTENTION
```
