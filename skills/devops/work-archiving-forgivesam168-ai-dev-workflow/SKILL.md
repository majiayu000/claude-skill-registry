---
name: work-archiving
description: Finalize and archive completed change packages. Use when asked to "archive changes", "finalize work", "close change package", or after code review approval. Handles Git commits, changelog generation, branch cleanup, and documentation updates.
license: See LICENSE.txt in repository root
---

# Work Archiving Skill

## When to Use This Skill

Use this skill at **Stage 6 (Archive)** of the workflow when:
- Code review is approved and all changes are merged
- Need to finalize and document completed work
- Time to close out the change package
- Asked to "archive", "finalize", "close out this work"
- Completing the 6-stage workflow cycle

## Prerequisites

Before archiving:
- [ ] Code review completed (05-review.md exists with approval)
- [ ] All changes committed and pushed
- [ ] Tests passing (if applicable)
- [ ] Documentation updated

## Archiving Workflow

### Step 1: Review Change Package Status

Check the change package folder (`changes/<YYYY-MM-DD>-<slug>/`) for completeness:
- `01-brainstorm.md` — Initial requirements and risk assessment
- `02-decision-log.md` — Key decisions made
- `03-spec.md` — Specification (if standard path)
- `04-plan.md` — Implementation plan
- `05-review.md` — Code review results

### Step 2: Create Archive Summary

Create `changes/<YYYY-MM-DD>-<slug>/99-archive.md`:

```markdown
# Archive: [Feature Name]

**Date Completed**: YYYY-MM-DD
**Status**: ✅ Completed / ⚠️ Completed with Known Issues

## Summary
Brief description of what was implemented.

## Key Outcomes
- Outcome 1
- Outcome 2

## Commits
- [commit-hash] commit message
- [commit-hash] commit message

## Related Issues/PRs
- Closes #123
- Related to #456

## Known Issues / Technical Debt
- Issue 1 (tracked in #789)
- Issue 2 (documented in decision log)

## Lessons Learned
- What went well
- What could be improved
- Recommendations for future work
```

### Step 3: Update CHANGELOG

If `CHANGELOG.md` exists, add entry:

```markdown
## [Version] - YYYY-MM-DD

### Added
- Feature description

### Changed
- Change description

### Fixed
- Fix description

### Security
- Security improvement description
```

If no CHANGELOG exists, consider creating one following [Keep a Changelog](https://keepachangelog.com/) format.

### Step 4: Commit and Tag (if applicable)

```bash
# Commit archive document
git add changes/<YYYY-MM-DD>-<slug>/99-archive.md
git commit -m "docs: archive change package for <feature-name>"

# Optional: Create release tag
git tag -a v1.2.3 -m "Release version 1.2.3"
git push origin v1.2.3
```

### Step 5: Close Related Issues/PRs

If using GitHub:
- Close related issues with reference to commits
- Update project boards
- Link PRs to completed work

### Step 6: Clean Up (Optional)

- [ ] Remove temporary files or branches
- [ ] Archive old change packages (if many exist)
- [ ] Update team documentation

## Output Format

### Archive Document (`99-archive.md`)

| Section | Required | Description |
|---------|----------|-------------|
| Summary | Yes | Brief description of completed work |
| Key Outcomes | Yes | Bullet list of deliverables |
| Commits | Yes | List of Git commits with hashes |
| Related Issues/PRs | If applicable | References to GitHub issues/PRs |
| Known Issues | If applicable | Technical debt or limitations |
| Lessons Learned | Recommended | Retrospective notes |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Change package incomplete | Review missing files and complete them before archiving |
| Commits not yet pushed | Push changes to remote before finalizing |
| Review not approved | Return to Stage 5 (Review) to address feedback |
| No CHANGELOG exists | Create one or document in 99-archive.md |

## Integration with Workflow

This skill completes the 6-stage workflow:
1. Brainstorm → 2. Specification → 3. Planning → 4. Implementation → 5. Review → **6. Archive**

After archiving, the change package serves as:
- **Audit trail** for regulatory/compliance needs
- **Knowledge base** for future similar work
- **Onboarding material** for new team members
- **Reference** for technical decisions

## Related Resources

- [WORKFLOW.md](../../WORKFLOW.md) — Complete workflow documentation
- [Specification Skill](../specification/SKILL.md) — Stage 2
- [Implementation Planning Skill](../implementation-planning/SKILL.md) — Stage 3
- [TDD Workflow Skill](../tdd-workflow/SKILL.md) — Stage 4
- [Code & Security Review Skill](../code-security-review/SKILL.md) — Stage 5

## Security Considerations

- Never commit secrets, credentials, or sensitive data in archive documents
- Redact customer/user information from examples
- If archiving includes security fixes, coordinate disclosure timing
- Ensure compliance with data retention policies
