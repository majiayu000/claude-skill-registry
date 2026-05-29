---
name: review-rfc
description: >-
  Review an architecture RFC against project architecture standards and best practices.
  Use when an RFC document needs design review, when evaluating a technical proposal,
  or when assessing architecture decision readiness.
argument-hint: "<path-to-rfc>"
disable-model-invocation: true
---

# Review RFC

Review the architecture RFC at `$0` against the project's architecture standards.

If `$0` is empty, ask the user for the RFC path. Suggest globbing `docs/rfcs/*.md` and `docs/20-architecture/rfcs/*.md` to find candidates.

## Context Loading

1. Read the RFC document at `$0`
2. Discover architecture standards (check in order, use first found):
   - `.arkhe/roadmap/architecture.md` (arkhe convention)
   - `docs/20-architecture/` directory (jd-docs convention)
   - `docs/architecture.md` or `docs/architecture/` (generic)
   - If none found, review against general architecture best practices
3. Scan referenced modules/packages in the RFC to verify feasibility

## Review Dimensions

Evaluate each dimension, noting concerns with severity (Critical/Major/Minor):

### 1. Problem Definition
Is the problem clearly stated? Are goals and non-goals explicit? Is the motivation compelling?

### 2. Architecture Quality
Does the design respect module boundaries? Is dependency direction correct? Does it follow established patterns from `architecture.md`?

### 3. Scalability
Will this scale with user growth? Are there bottlenecks? Does it handle multi-tenant scenarios?

### 4. Data Architecture
Is the data model sound? Are migrations safe? Are queries efficient? Does it maintain data integrity?

### 5. Infrastructure
Is the deployment strategy clear? Are there new infrastructure requirements? Is rollback possible?

### 6. Security
Are auth flows correct? Is input validated? Are there data privacy implications? Does it follow OWASP guidelines?

### 7. Project Fit
Does it align with the project's domain and existing patterns? Does it integrate well with the current architecture?

## Output Format

```markdown
# RFC Review: [RFC Title]
**Reviewer**: Claude | **Date**: [date] | **RFC**: [path]

## Verdict: [Approve | Approve with changes | Needs redesign]

## Summary
[2-3 sentence assessment]

## Strengths
- [strength with reference to RFC section]

## Concerns

### Critical
- [concern] — Section: [ref] | Impact: [description]

### Major
- [concern] — Section: [ref] | Impact: [description]

### Minor
- [concern] — Section: [ref] | Suggestion: [fix]

## Suggested Improvements
1. [improvement with rationale]

## Verdict Rationale
[Why this verdict was chosen. What must change before approval (if applicable).]
```

## Verdict Criteria

- **Approve**: No critical concerns, minor issues only
- **Approve with changes**: No critical concerns, has major concerns with clear fixes
- **Needs redesign**: Has critical concerns or fundamental architecture issues

## Notes

- Flag missing sections from the standard RFC template as Minor concerns
- After review, suggest related skills: `create-rfc` to draft new RFCs, `list-rfcs` to check the pipeline
