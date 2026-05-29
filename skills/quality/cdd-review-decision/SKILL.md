---
name: cdd-review-decision
description: DECIDED前の設計レビュー（重要な決断に推奨）
allowed-tools: Read, Bash(cdd:*), Glob, Grep
---

# Decision Review (Design Phase)

You are conducting a **design review** for decision ID: `$1`.

This review happens **after decisionStatus is set to DECIDED** but **before implementation starts**.

## Your Task

Review the decision document for consistency with existing architecture, guidelines, and other decisions.

### 1. Load the Decision

- Find and read `CDD/**/*$1*.cdd.md`
- Understand:
  - **Goal**: What they want to achieve
  - **Context**: Background, constraints, and gathered context references
  - **Selection**: Chosen approach
  - **Rejections**: Explicitly rejected alternatives

### 2. Verify Context Section

**IMPORTANT**: Check if the Context section contains `gathered_context` references.

If the Context section has `gathered_context`:
```yaml
gathered_context:
  - path: docs/architecture/overview.md
    summary: ...
    relevance_to_task: ...
```

Then:
1. Read each referenced document
2. Verify the summary and relevance_to_task are accurate
3. Check if any important documents are missing

If the Context section **lacks** `gathered_context`:
- Flag this as NEEDS_REVISION
- Recommend running `/cdd-gather-context` first

### 3. Gather Additional Reference Materials

Beyond the gathered_context, also check:
- `cdd-spec/GUIDE.md` - cdd.md format requirements
- `cdd-spec/WORKFLOW.md` - CDD workflow rules
- Related cdd.md files not in gathered_context (search by phase, keywords, tags)

### 4. Check Consistency

Verify:

#### Context Completeness (NEW)
- [ ] gathered_context is present in Context section
- [ ] All referenced documents actually exist
- [ ] No obviously missing related documents
- [ ] relevance_to_task explanations are accurate

#### Format Compliance
- [ ] YAML frontmatter is valid
- [ ] Required fields present: `id`, `title`, `decisionStatus`, `metadata.assignee`, `metadata.created`
- [ ] ID follows naming convention (#SCOPE-NUMBER)

#### Content Quality
- [ ] Goal is clear and measurable
- [ ] Context provides sufficient background
- [ ] Selection is well-justified
- [ ] Rejections explain why alternatives were rejected
- [ ] No contradictions within the document

#### Architecture Consistency
- [ ] Doesn't violate existing architecture principles
- [ ] Compatible with related decisions (from gathered_context)
- [ ] Follows established patterns and conventions
- [ ] Technical constraints are realistic

#### CDD Workflow Rules
- [ ] decisionStatus is appropriate (DRAFT/REVIEW/DECIDED)
- [ ] No implementation described if status is not DECIDED

### 5. Generate Review Report

Create a concise report:

```markdown
# Decision Review: $1

**Review Date:** {{YYYY-MM-DD}}
**Reviewer:** AI
**Status:** [APPROVED | NEEDS_REVISION]

## Summary

[1-2 sentences: What was reviewed and overall assessment]

## Context Verification

**gathered_context present:** [Yes/No]

[If Yes]
Verified references:
- [x] docs/architecture/overview.md - Accurate
- [x] CDD/tasks/27-xxx.cdd.md - Accurate
- [ ] [Missing: docs/xxx.md - Should be included because...]

[If No]
**Issue:** Context section lacks gathered_context. Run `/cdd-gather-context` first.

## Findings

### Strengths

- [List positive aspects]

### Issues Found

[Only if issues exist]

1. **[Issue Title]**
   - Severity: Critical / High / Medium / Low
   - Description: ...
   - Recommendation: ...

## Consistency Check

- [x] Context completeness
- [x] Format compliance
- [x] Content quality
- [x] Architecture consistency
- [x] CDD workflow rules

## Conclusion

**Status:** [APPROVED | NEEDS_REVISION]

[Final verdict with brief justification]

### Next Steps

[Only if NEEDS_REVISION - specific actions required]
```

### 6. Present Results

Show the user:
1. Review status (APPROVED / NEEDS_REVISION)
2. Context verification results
3. Key findings
4. Recommended next steps

**Important:**
- Be constructive, not critical
- Focus on architectural consistency, not personal preference
- If gathered_context is missing, this is a NEEDS_REVISION issue
- If uncertain, mark as NEEDS_REVISION and explain what needs clarification
- This review does NOT check code - that's done by cdd-review-implementation

## Integration with cdd-gather-context

This skill expects the cdd.md to have been prepared with context gathered by `/cdd-gather-context`.

The gathered_context in the Context section serves as:
1. **Reference list** - Documents that informed this decision
2. **Impact scope** - Documents that may need updates after implementation
3. **Consistency baseline** - What this decision must be consistent with

If the decision lacks this context, the review cannot verify architectural consistency properly.
