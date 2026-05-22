---
name: review-doc-consistency
description: 'Documentation consistency reviewer that checks alignment between code implementation and documentation. Use when user requests reviewing documentation vs code consistency, checking if README/docs are outdated, verifying API documentation accuracy. Applicable for (1) reviewing README vs implementation consistency (2) checking if docs/ directory content is outdated (3) verifying API/config documentation accuracy (4) generating documentation consistency reports. Trigger words include doc review, documentation consistency, check outdated docs, verify docs.'
---

# Documentation Consistency Reviewer

## Goal

Systematically identify all "outdated" or "inconsistent with implementation" descriptions in README + docs/, outputting ≥30 issue items.

## Core Principles

1. **Code is truth** - When documentation conflicts with code, source code/config/contract files are authoritative
2. **Evidence before conclusions** - Each issue must cite code/config location as evidence
3. **Contracts first** - OpenAPI/proto/schema/TS types are treated as SSOT (Single Source of Truth)
4. **Security default tightening** - Security-related inconsistencies are prioritized as high severity

## Review Process

### 1. Document Enumeration

```bash
# Scan scope
- README.md (root directory)
- docs/**/*.md (all documentation)
- Contract files: OpenAPI/proto/GraphQL schema/TS types
```

### 2. Document-by-Document Review

For each document:
1. List key claims/commitments/configs/interface items
2. Search for corresponding implementation in code
3. Compare differences: missing/renamed/behavior mismatch/default value mismatch
4. Record issues using template

### 3. Cross-Check

- Reverse check documentation from contract files
- Reverse check documentation from config files

See [checklist.md](checklist.md) for detailed review checklist.

## Severity Levels

| Level | Definition | Example |
|-------|------------|---------|
| P0 | Security issue/serious misleading | Docs say sandbox enabled but code doesn't enable it |
| P1 | Core functionality inconsistency | Following docs leads to failure |
| P2 | Incomplete examples/naming inconsistency | Doesn't directly block usage |
| P3 | Wording/formatting/link minor issues | Doesn't affect functionality |
| Pending Evidence | Suspicious but insufficient evidence | Needs further investigation |

## Output Format

See [output-format.md](output-format.md) for detailed templates.

### Single Issue Item

```markdown
### [Title]
- **Severity**: P0/P1/P2/P3/Pending Evidence
- **Location**: `<file_path>:<line_number>`
- **Evidence**:
  - Documentation: [quote]
  - Code: [quote]
- **Impact**: [Misleading consequences]
- **Suggestion**: [Minimal fix]
- **Related Principle**: Code is truth/Contracts first/Security default tightening/...
```

### Review Conclusion

```markdown
## Review Conclusion
- **Verdict**: Pass/Conditional Pass/Fail
- **Summary**: P0:x P1:x P2:x P3:x Pending:x
- **Fix Priority**: P0 → P1 → P2 → P3
```

## Multi-Agent Parallel

For acceleration, split by following dimensions for parallel multi-agent execution:

1. **By document type** - One agent each for README, API docs, development guide
2. **By module** - One agent per functional module's documentation
3. **By check direction** - One checks docs against code, another checks code against docs

Deduplication and unified severity rating needed when aggregating.

## Execution

After review completion, output `doc-consistency.md` report file, and also output `doc-consistency.json` (structured issue list for aggregation/deduplication/statistics).
