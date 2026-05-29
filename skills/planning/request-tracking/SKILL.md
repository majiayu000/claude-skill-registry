---
name: request-tracking
description: Request tracking knowledge base. Covers request structure, status tracking, document references, progress management.
allowed-tools: Read, Grep, Glob
context: fork
agent: Explore
---

# Request Tracking Skill

## Trigger

- Keywords: request document, request, progress tracking, status, acceptance criteria, tech spec

## When NOT to Use

- Create new request document (use /create-request)
- Write tech spec (use /tech-spec)
- Code development (use feature-dev)

## Document Hierarchy

```
requests/        Request documents (scope + acceptance)
    ↓ references
planning/        Tech specs (implementation details)
    ↓ references
adr/             Decision records (rationale)
    ↓ references
architecture/    Architecture docs (system design)
```

## File Location

```
docs/features/{feature}/
├── requests/           # Active request documents
│   └── archived/       # Completed
├── planning/           # Tech specs
├── adr/                # Decision records
└── architecture/       # Architecture docs
```

## Naming Convention

**Format**: `YYYY-MM-DD-kebab-case-title.md`

## Status & Priority

| Status   | Description        |
| -------- | ------------------ |
| Pending  | Not started        |
| In Dev   | In progress        |
| Approved | Spec confirmed     |

| Priority | Timeline       |
| -------- | -------------- |
| P0       | Immediate      |
| P1       | This week      |
| P2       | This iteration |

## Verification

- Request document includes: background, requirements, acceptance criteria
- File naming follows convention
- Correctly linked to tech spec

## References

- `references/template.md` - Request document template
- `references/operations.md` - Operations guide

## Examples

```
Input: How to write a request document?
Action: Explain template structure + reference template.md
```

```
Input: How to track progress for this request?
Action: Explain progress table / Phase breakdown approach
```
