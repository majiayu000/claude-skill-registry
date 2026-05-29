---
name: cdd-review-implementation
description: IN_REVIEW実装をレビュー（APPROVED→DONE）
allowed-tools: Read, Edit, Write, Bash(cdd:*, git:*), Glob, Grep
---

# Implementation Review (Code Phase)

You are conducting an **implementation review** for decision ID: `$1`.

This review happens **after implementation is complete** (implementationStatus: IN_REVIEW).

## Your Task

Review the implementation code to verify it matches the decision requirements.

### 1. Read the Decision Document

First, read `CDD/**/*$1*.cdd.md` to understand:
- **Goal**: What was supposed to be achieved
- **Selection**: What approach was chosen and why
- **Rejections**: What alternatives were explicitly rejected (should NOT be in the implementation)
- **Review Criteria**: Any specific review points mentioned in the document

### 2. Check for Review Criteria Section

If the cdd.md contains a `## Review Criteria` section:
- Read any referenced documents (e.g., "参照: docs/SECURITY.md")
- Apply the criteria specified in that section
- Document your findings in the review report

### 3. Locate Implementation

**Two methods to find implementation files**:

#### Method 1: Git commit search (Primary)
Use the Bash tool to search for commits related to this decision:
```bash
git log --all --grep="CDD: $1" --name-only --pretty=format:"%H %s"
```

This will show:
- Commit hashes and messages containing `CDD: $1`
- Files changed in those commits

Extract the file list from the commits for review.

#### Method 2: Code marker search (Fallback for older implementations)
If no commits are found, search for `@cdd #$1` markers (deprecated but may exist in older code):
```bash
grep -r "@cdd #$1" --include="*.ts" --include="*.js" --include="*.tsx" --include="*.jsx"
```

**Prefer Method 1** - Git commits are the source of truth for recent implementations.

### 4. Conduct the Review

Check the following:

#### Decision Alignment
- [ ] All items in the **Selection** section are implemented correctly
- [ ] None of the **Rejections** section items are present in the implementation
- [ ] Implementation follows the constraints and guidelines in the **Context** section

#### Code Quality
- [ ] Code follows project conventions and style
- [ ] Appropriate error handling
- [ ] Adequate test coverage

#### Architecture & Security (if applicable)
- [ ] Follows architectural principles
- [ ] Security best practices applied
- [ ] No security vulnerabilities introduced

### 5. Generate Review File

Create a review file at: `CDD/.logs/review/$1-{{YYYYMMDD}}-{{sequence}}.md`

Use this structure:

```yaml
---
reviewId: $1-{{YYYYMMDD}}-{{sequence}}
decisionId: $1
decisionFile: {{path to cdd.md}}
reviewDate: '{{YYYY-MM-DDTHH:mm}}'
reviewer: AI
status: [APPROVED|REJECTED|NEEDS_REVISION]
---

## Summary

[Brief overview of the review - 2-3 sentences describing what was reviewed and the outcome]

## Implementation Check

### Decision Alignment

- [x] Selection section items are implemented
  - [Detail what was checked and found]
- [x] Rejections section items are NOT implemented
  - [Detail what was verified]
- [x] Context constraints are followed
  - [Detail compliance]

### Code Quality

- [x] Code follows project conventions
- [x] Error handling is appropriate
- [x] Tests are adequate

## Review Criteria Check

[If Review Criteria section exists in cdd.md, document findings here]

### [Criterion 1]
- Finding: ...
- Status: ✅ Pass / ❌ Fail / ⚠️ Needs attention

### [Criterion 2]
- Finding: ...
- Status: ✅ Pass / ❌ Fail / ⚠️ Needs attention

## Issues Found

[List any issues discovered - omit this section if no issues]

1. **[Issue Title]**
   - Location: file:line
   - Description: ...
   - Severity: Critical / High / Medium / Low
   - Recommendation: ...

## Conclusion

**Status:** [APPROVED|REJECTED|NEEDS_REVISION]

[Final verdict with brief justification]

### Next Steps

[Only if REJECTED or NEEDS_REVISION]
- Action 1
- Action 2
```

### 6. Update cdd.md (IMPORTANT)

After creating the review file, you MUST update the cdd.md file to add the review to its `reviewHistory` in the YAML frontmatter:

```yaml
reviewHistory:
  - date: '{{YYYY-MM-DDTHH:mm}}'
    file: 'CDD/.logs/review/$1-{{YYYYMMDD}}-{{sequence}}.md'
    status: '[APPROVED|REJECTED|NEEDS_REVISION]'
```

Append this to the existing `reviewHistory` array if it exists, or create the field if it doesn't.

### 7. Present Results and Update Status

Show the user:
1. Review status (APPROVED/REJECTED/NEEDS_REVISION)
2. Key findings (if any issues)
3. Path to the review file
4. Confirmation that cdd.md was updated

### If Review Status is APPROVED

**Use AskUserQuestion tool** to confirm:
- Question: "レビューがAPPROVEDになりました。implementationStatusをDONEに変更しますか？"
- Options: "はい" / "いいえ"

**If "はい":**
- Update the cdd.md file to change `implementationStatus: DONE`
- Use the Edit tool to update the frontmatter
- Show confirmation: "✓ Updated implementationStatus to DONE"

**If "いいえ":**
- Keep current implementationStatus unchanged
- Show confirmation: "implementationStatus kept as-is"

**Important:**
- Only use AskUserQuestion if the review status is `APPROVED`
- Do not ask for `REJECTED` or `NEEDS_REVISION` reviews

## File Naming Convention

- Format: `$1-{{YYYYMMDD}}-{{sequence}}.md`
- Example: `PHASE1.1-A-20260120-1.md`
- Sequence number differentiates multiple reviews on the same day
- Check existing files to determine the next sequence number

## Important Notes

- Be thorough but concise
- Focus on objective findings, not opinions
- If uncertain about something, investigate further before making a judgment
- Use checkboxes ([x] / [ ]) to make findings scannable
- Always reference specific file locations when mentioning issues
- The review should be constructive and actionable
