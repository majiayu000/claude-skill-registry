---
name: ln-600-docs-auditor
description: Audit project documentation quality across 6 categories (Hierarchy, SSOT, Compactness, Requirements, Actuality, Legacy). Use when documentation needs quality review, after major doc updates, or as part of ln-100-documents-pipeline. Outputs Compliance Score X/10 per category + Findings + Recommended Actions.
---

# Documentation Auditor

Audit project documentation quality. Universal for any tech stack.

## Purpose

- **Proactively compress** - find all opportunities to reduce size while preserving value
- Eliminate meaningless, redundant, and verbose content
- Convert prose to structured formats (tables, lists)
- Verify documentation hierarchy with CLAUDE.md as root
- Detect duplication and enforce Single Source of Truth
- Ensure docs match current code state

## Invocation

- **Direct:** User invokes for documentation quality review
- **Pipeline:** Called by ln-100-documents-pipeline (Phase 5, if auditDocs=true)

## Workflow

1. **Scan:** Find all .md files in project (CLAUDE.md, README.md, docs/**)
2. **Build Tree:** Construct hierarchy from CLAUDE.md outward links
3. **Audit:** Run 6 category checks (see Audit Categories below)
4. **Score:** Calculate X/10 per category
5. **Report:** Output findings and recommended actions

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
| **Overall** | **X/10** | |

### Critical Findings

- [ ] **[Category]** `path/file.md:line` - Issue description. **Action:** Fix suggestion.

### Recommended Actions

| Priority | Action | Location | Category |
|----------|--------|----------|----------|
| High | Remove duplicate section | docs/X.md | SSOT |
| Medium | Add link to CLAUDE.md | docs/Y.md | Hierarchy |
```

## Scoring Rules

| Score | Meaning |
|-------|---------|
| 10/10 | No issues |
| 8-9/10 | Minor issues (formatting, small redundancies) |
| 6-7/10 | Moderate issues (some duplication, missing links) |
| 4-5/10 | Significant issues (orphaned docs, outdated content) |
| 1-3/10 | Critical issues (major mismatches, broken hierarchy) |

## Reference Files

- Size limits and targets: [references/size_limits.md](references/size_limits.md)
- Detailed checklist: [references/audit_checklist.md](references/audit_checklist.md)

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
- **Delete, don't archive:** Legacy content should be removed, not moved to "archive"
- **No history:** Documents describe current state only; git tracks history

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
