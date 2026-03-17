---
name: aget-review-pr
description: Review pull requests for quality and standards
archetype: developer
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# aget-review-pr

Review pull requests for code quality, test coverage, and standards compliance. Produces structured review with categorized comments.

## Instructions

When this skill is invoked:

1. **Gather PR Information**
   ```bash
   gh pr view [number] --json title,body,files,additions,deletions
   gh pr diff [number]
   ```

2. **Analyze Changes**
   - Code correctness
   - Test coverage for changed code
   - Standards compliance
   - Potential issues

3. **Categorize Findings**
   - **Blocking**: Must fix before merge
   - **Suggestion**: Should consider
   - **Nitpick**: Minor observation
   - **Praise**: Positive feedback

4. **Form Recommendation**
   - Approve: No blocking issues
   - Request Changes: Has blocking issues
   - Comment: Questions or suggestions only

## Output Format

```markdown
## PR Review: #[number] - [title]

### Summary

| Metric | Value |
|--------|-------|
| Files Changed | [N] |
| Additions | +[N] |
| Deletions | -[N] |
| Tests Added | [Y/N] |

### Overall Assessment

**Recommendation**: [Approve / Request Changes / Comment]

**Rationale**: [Brief explanation]

---

### Comments

#### Blocking Issues

1. **[file:line]**: [Issue description]
   - Suggestion: [How to fix]

#### Suggestions

1. **[file:line]**: [Suggestion]
   - Rationale: [Why consider this]

#### Nitpicks

1. **[file:line]**: [Minor observation]

#### Positive Observations

1. **[file:line]**: [What was done well]

---

### Test Coverage

- [ ] New code has tests
- [ ] Edge cases covered
- [ ] Integration tests updated (if applicable)

### Standards Check

- [ ] Naming conventions followed
- [ ] Documentation updated
- [ ] No hardcoded values
```

## Constraints

- **C1**: NEVER approve PRs with blocking issues — blocking issues must be resolved
- **C2**: NEVER submit review without user confirmation — user controls GitHub interaction
- **C3**: NEVER focus solely on style issues — correctness and design more important than formatting

## Related

- SKILL-024: aget-review-pr specification
- ONTOLOGY_developer.yaml: Pull_Request, Code_Review concepts
- CAP-DEV-003: PR Review capability
