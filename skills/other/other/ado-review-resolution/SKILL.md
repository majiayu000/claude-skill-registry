---
name: ado-review-resolution
description: Review a resolved ADO work item to verify the fix is complete and correct
model: sonnet
---

# Resolution Review Skill

Use this skill to review resolved ADO work items that have been assigned to you for verification.

## Process

### 1. Understand the Original Issue
- Read the work item title and description
- Understand what problem was being solved
- Note any acceptance criteria or requirements

### 2. Review the PR Changes
If a GitHub PR URL is provided:
- Fetch the PR diff using `gh pr diff <number>` or review the files changed
- Understand what code changes were made
- Check if the changes align with the issue requirements

### 3. Compare Against Test Notes
The test notes field contains acceptance criteria or testing instructions:
- Verify each criterion is addressed by the changes
- Check for edge cases that might not be covered
- Look for potential regressions

### 4. Code Quality Check
- Review the code for quality issues
- Check for proper error handling
- Verify no security vulnerabilities introduced
- Ensure code follows project conventions

### 5. Provide Verdict

Format your response as:

```markdown
## Resolution Review: [Work Item Title]

### Summary
[Brief summary of what was changed]

### Checklist
- [ ] Changes address the original issue
- [ ] Test notes/acceptance criteria met
- [ ] Code quality acceptable
- [ ] No obvious regressions
- [ ] Error handling adequate

### Findings
[Detailed findings, issues, or concerns]

### Verdict: [APPROVED / NEEDS CHANGES / NEEDS DISCUSSION]

[Explanation of verdict and any required follow-up actions]
```

## Verdict Guidelines

- **APPROVED**: All criteria met, code is good, ready to close
- **NEEDS CHANGES**: Issues found that must be fixed before closing
- **NEEDS DISCUSSION**: Ambiguous requirements or architectural concerns that need team input
