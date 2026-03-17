---
name: ln-610-code-comments-auditor
description: Audit code comments and docstrings quality across 6 categories (WHY-not-WHAT, Density, Forbidden Content, Docstrings, Actuality, Legacy). Use when code needs comment review, after major refactoring, or as part of ln-100-documents-pipeline. Outputs Compliance Score X/10 per category + Findings + Recommended Actions.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Code Comments Auditor

Audit code comments and docstrings quality. Universal for any tech stack.

## Purpose

- Verify comments explain WHY, not obvious WHAT
- Check comment density (15-20% ratio)
- Detect forbidden content (dates, author names, historical notes)
- Validate docstrings match function signatures
- Ensure comments match current code state
- Identify legacy comments and commented-out code

## Invocation

- **Direct:** User invokes for code comment quality review
- **Pipeline:** Called by ln-100-documents-pipeline (Phase 5, if auditComments=true)

## Workflow

1. **Scan:** Find all source files (auto-detect tech stack)
2. **Extract:** Parse inline comments + docstrings/JSDoc
3. **Audit:** Run 6 category checks (see Audit Categories below)
4. **Score:** Calculate X/10 per category
5. **Context Validation:** Post-filter findings (see below)
6. **Report:** Output findings and recommended actions

## Audit Categories

| # | Category | What to Check |
|---|----------|---------------|
| 1 | **WHY not WHAT** | Comments explain rationale, not obvious code behavior; no restating code |
| 2 | **Density (15-20%)** | Comment-to-code ratio within range; not over/under-commented |
| 3 | **No Forbidden Content** | No dates/authors; no historical notes; no code examples in comments |
| 4 | **Docstrings Quality** | Match function signatures; parameters documented; return types accurate |
| 5 | **Actuality** | Comments match code behavior; no stale references; examples runnable |
| 6 | **Legacy Cleanup** | No TODO without context; no commented-out code; no deprecated notes |

### Context Validation (Post-Filter)

**MANDATORY READ:** Load `shared/references/context_validation.md`

Apply Rule 1 + comment-specific inline filters:
```
FOR EACH finding WHERE severity IN (HIGH, MEDIUM):
  # Rule 1: ADR/Planned Override
  IF finding matches ADR → advisory "[Planned: ADR-XXX]"

  # Comment-specific: Per-category density targets
  IF Cat 2 (Density) finding:
    Classify file by path:
    - test/ or tests/           → target density 2-10%
    - infra/ or config/ or ci/  → target density 5-15%
    - business/domain/services  → target density 15-25%
    Recalculate with per-category target instead of fixed 15-20%.
    If >50% comments are docstrings → calculate inline density separately.

  # Comment-specific: Complexity context for WHY-not-WHAT
  IF Cat 1 (WHY not WHAT) finding:
    - If file McCabe complexity > 15 → WHAT comments acceptable (complex logic)
    - If file in domain/ or business/ → explanatory comments OK (domain knowledge)

Downgraded findings → separate "Advisory" note in report.
```

## Output Format

```markdown
## Code Comments Audit Report - [DATE]

### Compliance Score

| Category | Score | Issues |
|----------|-------|--------|
| WHY not WHAT | X/10 | N obvious comments |
| Density (15-20%) | X/10 | X% actual (target: 15-20%) |
| No Forbidden Content | X/10 | N forbidden items |
| Docstrings Quality | X/10 | N mismatches |
| Actuality | X/10 | N stale comments |
| Legacy Cleanup | X/10 | N legacy items |
| **Overall** | **X/10** | |

### Critical Findings

- [ ] **[Category]** `path/file:line` - Issue description. **Action:** Fix suggestion.

### Recommended Actions

| Priority | Action | Location | Category |
|----------|--------|----------|----------|
| High | Remove author name | src/X:45 | Forbidden |
| Medium | Update stale docstring | lib/Y:120 | Actuality |
```

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

**Severity mapping:**

| Issue Type | Severity |
|------------|----------|
| Author names, dates in comments | CRITICAL |
| Commented-out code blocks | HIGH |
| Stale/outdated comments | HIGH |
| Obvious WHAT comments | MEDIUM |
| Density deviation >5% | MEDIUM |
| Minor density deviation | LOW |

## Reference Files

- Comment rules and patterns: [references/comments_rules.md](references/comments_rules.md)

## Definition of Done

- All source files scanned (tech stack auto-detected)
- Inline comments and docstrings/JSDoc extracted and parsed
- All 6 categories audited with score X/10 each (WHY-not-WHAT, Density, Forbidden, Docstrings, Actuality, Legacy)
- Comment-to-code density ratio calculated and compared against 15-20% target
- Critical Findings listed with file:line, category, and fix suggestion
- Recommended Actions table generated with priority, action, location, category

## Critical Notes

- **Fix code, not rules:** NEVER modify rules files (*_rules.md, *_standards.md) to make violations pass. Always fix the code instead.
- **Code is truth:** When comment contradicts code, flag comment for update
- **WHY > WHAT:** Comments explaining obvious behavior should be removed
- **Task IDs OK:** Task/Story IDs in comments help with code traceability
- **Universal:** Works with any language; detect comment syntax automatically
- **Based on:** Claude Code comment-analyzer agent patterns

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
