---
name: ln-600-docs-auditor
description: Audit project documentation quality across 8 categories (Hierarchy, SSOT, Compactness, Requirements, Actuality, Legacy, Stack Adaptation, Semantic Content). Delegates to ln-601 for deep semantic verification of project documents. Use when documentation needs quality review, after major doc updates, or as part of ln-100-documents-pipeline. Outputs Compliance Score X/10 per category + Findings + Recommended Actions.
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Documentation Auditor

Audit project documentation quality. Universal for any tech stack.

## Purpose

- **Proactively compress** - find all opportunities to reduce size while preserving value
- Eliminate meaningless, redundant, and verbose content
- Convert prose to structured formats (tables, lists)
- Verify documentation hierarchy with CLAUDE.md as root
- Detect duplication and enforce Single Source of Truth
- Ensure docs match current code state
- **Semantic verification** - delegate to ln-601 to verify content matches SCOPE and codebase reality

## Invocation

- **Direct:** User invokes for documentation quality review
- **Pipeline:** Called by ln-100-documents-pipeline (Phase 5, if auditDocs=true)

## Workflow

1. **Scan:** Find all .md files in project (CLAUDE.md, README.md, docs/**)
2. **Build Tree:** Construct hierarchy from CLAUDE.md outward links
3. **Audit Categories 1-7:** Run structural checks (see Audit Categories below)
4. **Semantic Audit (Category 8):** For each project document, delegate to ln-601-semantic-content-auditor
5. **Score:** Calculate X/10 per category (including semantic scores from ln-601)
6. **Context Validation:** Post-filter findings (see below)
7. **Report:** Output findings and recommended actions

### Phase 4: Semantic Audit Delegation

For each project document (excluding tasks/, reference/, presentation/):

```
FOR doc IN [CLAUDE.md, docs/README.md, docs/project/*.md]:
    result = DELEGATE ln-601-semantic-content-auditor {
        doc_path: doc,
        project_root: project_root,
        tech_stack: detected_stack
    }
    semantic_findings.append(result.findings)
    semantic_scores[doc] = result.scores
```

**Target documents:** CLAUDE.md, docs/README.md, docs/documentation_standards.md, docs/principles.md, docs/project/*.md

**Excluded:** docs/tasks/, docs/reference/, docs/presentation/, tests/

## Audit Categories

| # | Category | What to Check |
|---|----------|---------------|
| 1 | **Hierarchy & Links** | CLAUDE.md is root; all docs reachable via links; no orphaned files; no broken links |
| 2 | **Single Source of Truth** | No content duplication; duplicates replaced with links to source; clear ownership |
| 3 | **Proactive Compression** | Eliminate verbose/redundant content; prose→tables; remove meaningless info; compress even under-limit files; see [size_limits.md](references/size_limits.md) |
| 4 | **Requirements Compliance** | Correct sections; within size limits; **no code blocks** (tables/ASCII diagrams/text only); stack-appropriate doc links |
| 5 | **Actuality (CRITICAL)** | **Verify facts against code:** paths exist, functions match, APIs work, configs valid; outdated docs are worse than none |
| 6 | **Legacy Cleanup** | No history sections; no "was changed" notes; no deprecated info; current state only |
| 7 | **Stack Adaptation** | Links/refs match project stack; no Python examples in .NET project; official docs for correct platform |
| 8 | **Semantic Content** | **Delegated to ln-601:** Content matches SCOPE; serves project goals; descriptions match actual code behavior; architecture/API docs reflect reality |

### Context Validation (Post-Filter)

**MANDATORY READ:** Load `shared/references/context_validation.md`

Apply Rule 1 + doc-specific inline filters:
```
FOR EACH finding WHERE severity IN (HIGH, MEDIUM):
  # Rule 1: ADR/Planned Override
  IF finding matches ADR → advisory "[Planned: ADR-XXX]"

  # Doc-specific: Compression context
  IF Cat 3 (Compression) finding:
    - Skip if path in references/ or templates/ (reference docs = naturally large)
    - Skip if filename contains architecture/design/api_spec
    - Skip if tables+lists > 50% of content (already structured, not verbose prose)

  # Doc-specific: Actuality severity calibration
  IF Cat 5 (Actuality) finding:
    - Path/function COMPLETELY missing → CRITICAL (broken docs)
    - Path exists but deprecated/renamed → HIGH (not CRITICAL)
    - Example code outdated but concept valid → MEDIUM

Downgraded findings → "Advisory Findings" section in report.
```

## Output Format

```markdown
## Documentation Audit Report - [DATE]

### Compliance Score

| Category | Score | Issues |
|----------|-------|--------|
| Hierarchy & Links | X/10 | N issues found |
| Single Source of Truth | X/10 | N duplications |
| Proactive Compression | X/10 | N compression opportunities |
| Requirements Compliance | X/10 | N violations |
| Actuality | X/10 | N mismatches with code |
| Legacy Cleanup | X/10 | N legacy items |
| Stack Adaptation | X/10 | N stack mismatches |
| Semantic Content | X/10 | N semantic issues (via ln-601) |
| **Overall** | **X/10** | |

### Critical Findings

- [ ] **[Category]** `path/file.md:line` - Issue description. **Action:** Fix suggestion.

### Recommended Actions

| Priority | Action | Location | Category |
|----------|--------|----------|----------|
| High | Remove duplicate section | docs/X.md | SSOT |
| Medium | Add link to CLAUDE.md | docs/Y.md | Hierarchy |
```

## Scoring Algorithm

**MANDATORY READ:** Load `shared/references/audit_scoring.md` for unified scoring formula.

**Severity mapping:**

| Issue Type | Severity |
|------------|----------|
| Outdated content (code mismatch) | CRITICAL |
| Broken links, orphaned docs | HIGH |
| Semantic mismatch (via ln-601) | HIGH |
| Content duplication | MEDIUM |
| Missing compression opportunity | LOW |

## Reference Files

- Size limits and targets: [references/size_limits.md](references/size_limits.md)
- Detailed checklist: [references/audit_checklist.md](references/audit_checklist.md)

## Definition of Done

- All .md files in project scanned and hierarchy tree built from CLAUDE.md
- Categories 1-7 (structural) audited with score X/10 each
- Category 8 (semantic) delegated to ln-601 for each target document; scores collected
- Overall Compliance Score calculated (average of 8 categories)
- Critical Findings listed with file:line, category, and fix suggestion
- Recommended Actions table generated with priority, action, location, category

## Critical Notes

- **Fix content, not rules:** NEVER modify standards/rules files (*_standards.md, *_rules.md, *_limits.md) to make violations pass. Always fix the violating files instead.
- **Verify facts against code:** Actively check every path, function name, API, config mentioned in docs. Run commands. Outdated docs mislead - they're worse than no docs.
- **Compress always:** Size limits are upper bounds, not targets. A 100-line file instead of 300 is a win. Always look for compression opportunities.
- **Meaningless content:** Remove filler words, obvious statements, over-explanations. If it doesn't add value, delete it.
- **No code in docs:** Documents describe algorithms in tables or ASCII diagrams. Code belongs in codebase.
  - **Forbidden:** Code blocks, implementation snippets
  - **Allowed:** Tables, ASCII diagrams, Mermaid, method signatures (1 line)
  - **Instead of code:** "See [Official docs](url)" or "See [src/file.cs:42](path#L42)"
- **Format Priority:** Tables/ASCII > Lists (enumerations only) > Text (last resort)
- **Stack adaptation:** Verify all documentation references match project stack. .NET project must not have Python examples. Check official doc links point to correct platform (Microsoft docs for C#, MDN for JS, etc.)
- **Code is truth:** When docs contradict code, always update docs. Never "fix" code to match documentation.
- **SSOT re-verification after fixes:** After making ANY documentation change, re-check that the fix maintains Single Source of Truth. If content exists in multiple files, keep it in the canonical source only and replace other occurrences with a link to that source (e.g., `See [section](path#anchor)`). Never duplicate content inline — always link. Canonical source hierarchy: CLAUDE.md → docs/README.md → docs/project/*.md → docs/reference/*.md.
- **Delete, don't archive:** Legacy content should be removed, not moved to "archive"
- **No history:** Documents describe current state only; git tracks history

---
**Version:** 4.0.0
**Last Updated:** 2026-01-28
