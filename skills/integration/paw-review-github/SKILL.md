---
name: paw-review-github
description: Posts finalized review comments to GitHub as a pending review after critique iteration is complete.
metadata:
  type: activity
  artifacts: none
  updates: ReviewComments.md
  stage: output
---

# PAW Review GitHub Skill

Post finalized review comments to GitHub as a pending review. This skill only posts comments marked as ready, filtering out skipped comments while preserving the complete review history in ReviewComments.md.

> **Reference**: Follow Core Review Principles from `paw-review-workflow` skill.

## Prerequisites

Verify `ReviewComments.md` exists in `.paw/reviews/<identifier>/` with:
- Status: `finalized`
- All comments have `**Final**:` markers
- At least one comment marked `**Final**: ✓ Ready for GitHub posting`

Also verify:
- GitHub PR context available (owner, repo, PR number)
- For multi-repo reviews: PR context available for each repository

If ReviewComments.md is not finalized or missing `**Final**:` markers, report blocked status—Critique Response pass must complete first.

**Non-GitHub Context**: If this is not a GitHub PR review (e.g., local branch diff), skip GitHub posting and provide manual posting instructions instead.

## Core Responsibilities

- Read all comments from finalized ReviewComments.md
- Filter to only comments marked `**Final**: ✓ Ready for GitHub posting`
- Create GitHub pending review with filtered comments
- Update ReviewComments.md with posted status and review IDs
- Handle multi-PR scenarios (create pending review per PR)
- Provide manual posting instructions for non-GitHub contexts

## Process Steps

### Step 1: Load ReviewComments.md

Read the finalized ReviewComments.md and verify:
- Status field shows `finalized`
- All comments have `**Final**:` markers
- Extract GitHub PR context (owner, repo, PR number)

If not finalized:
```
Blocked: ReviewComments.md status is not 'finalized'.
Run paw-review-feedback in Critique Response Mode first.
```

### Step 2: Filter Postable Comments

Identify comments to post:

**Include** comments where `**Final**:` contains:
- `✓ Ready for GitHub posting`
- `Ready for GitHub posting`

**Exclude** comments where `**Final**:` contains:
- `Skipped per critique`
- `Skipped`
- Any other status not explicitly "Ready for GitHub posting"

Build list of postable comments with:
- File path
- Line number or range
- Comment text (use `**Updated Comment:**` if present, otherwise original description)
- Suggestion code (use `**Updated Suggestion:**` if present, otherwise original)

### Step 3: Create Pending Review (GitHub PRs)

Use GitHub MCP tools to create pending review:

**3.1 Create Pending Review:**
```
mcp_github_pull_request_review_write(
  owner: "<owner>",
  repo: "<repo>",
  pullNumber: <number>,
  method: "create"
  // Note: event omitted to create pending (draft) review
)
```

Record the pending review ID.

**3.2 Add Comments to Pending Review:**

For EACH postable comment:
```
mcp_github_add_comment_to_pending_review(
  owner: "<owner>",
  repo: "<repo>",
  pullNumber: <number>,
  path: "<file-path>",
  line: <line-number>,  // or startLine/line for multi-line
  body: "<comment-text-and-suggestion>",
  side: "RIGHT",
  subjectType: "LINE"  // or "FILE" for file-level comments
)
```

**Comment Body Construction:**
- Include description text (updated if modified, original otherwise)
- Include code suggestion in markdown code block
- Do NOT include rationale, assessment, or internal markers
- Do NOT include `**Final**:` or other PAW-specific formatting

**Example Posted Comment:**
```markdown
Missing null check before accessing user.profile could cause runtime error.

```suggestion
if (user?.profile) {
  return user.profile.name;
}
return 'Anonymous';
```
```

### Step 4: Update ReviewComments.md

After posting, update each posted comment in ReviewComments.md:

**Add Posted Status:**
```markdown
**Final**: ✓ Ready for GitHub posting
**Posted**: ✓ GitHub pending review (Review ID: 12345678, Comment ID: abc123)
```

**For Skipped Comments:**
```markdown
**Final**: Skipped per critique - stylistic preference
**Posted**: — (not posted per critique)
```

Update the file header:
```markdown
**Status**: Posted to GitHub pending review
**Pending Review ID**: 12345678
**Comments Posted**: 6 of 8 (2 skipped per critique)
```

### Step 5: Multi-PR Pending Reviews

When reviewing PRs across multiple repositories:

**Detection:**
Multi-PR mode applies when:
- Multiple artifact directories exist (`.paw/reviews/PR-<number>-<repo-slug>/`)
- ReviewComments.md files exist in multiple PR directories
- ReviewContext.md contains `related_prs` entries

**Per-PR Processing:**

1. **Iterate PRs**: For each PR in the review set:
   - Read ReviewComments.md from that PR's artifact directory
   - Filter to postable comments for that PR
   - Create separate pending review on that PR
   - Update that PR's ReviewComments.md with posted status

2. **Cross-Reference in Comments**: When posting cross-repo comments:
   - Include cross-reference notation from the comment
   - Example: `(See also: owner/other-repo#456 for related change)`

**GitHub Tool Calls for Multiple PRs:**
```
# PR 1: repo-a
mcp_github_pull_request_review_write(owner, "repo-a", 123, method="create")
mcp_github_add_comment_to_pending_review(...)  # postable comments for PR-123

# PR 2: repo-b  
mcp_github_pull_request_review_write(owner, "repo-b", 456, method="create")
mcp_github_add_comment_to_pending_review(...)  # postable comments for PR-456
```

**Error Handling:**
If pending review creation fails for one PR:
- Document the failure in that PR's ReviewComments.md
- Continue with other PRs
- Provide manual posting instructions for failed PR
- Report partial success in completion response

### Step 6: Non-GitHub Context

For non-GitHub workflows (local branch review):

**Skip GitHub Posting:**
- Do not attempt to call GitHub MCP tools
- Update ReviewComments.md status to `finalized (non-GitHub)`

**Provide Manual Posting Instructions:**

Append to ReviewComments.md:
```markdown
---

## Manual Posting Instructions

This review was conducted on a non-GitHub context. To post comments manually:

### Comments Ready for Posting (X total)

1. **File: auth.ts, Lines 45-50**
   > Missing null check before accessing user.profile could cause runtime error.
   
   Suggestion:
   ```typescript
   if (user?.profile) {
     return user.profile.name;
   }
   return 'Anonymous';
   ```

2. **File: db.ts, Lines 120-125**
   > [Comment text...]

### Skipped Comments (Y total)
These comments were evaluated as low-value by the critique process and are not recommended for posting:
- File: api.ts L88 - Skipped: stylistic preference
```

## Guardrails

**Post Only Finalized Comments:**
- NEVER post comments without `**Final**: ✓ Ready for GitHub posting`
- Comments marked Skip must NOT be posted
- Respect critique recommendations

**Pending Review Only:**
- NEVER submit the pending review automatically
- Use `method: "create"` without event parameter
- Human reviewer must explicitly submit

**No Rationale in Posted Comments:**
- Posted comments contain only description and suggestion
- Rationale, assessment, and internal markers stay in ReviewComments.md
- PAW artifacts never referenced in posted comments

**Preserve History:**
- Do not modify original comment text when adding Posted status
- Keep all history: original → assessment → updated → posted
- Skipped comments remain in artifact for documentation

**Human Control:**
- Pending review is a draft—reviewer can edit/delete before submitting
- Reviewer can manually add skipped comments if they disagree with critique
- Final submission decision rests with human reviewer

## Validation Checklist

Before completing, verify:

- [ ] ReviewComments.md was finalized (had `**Final**:` markers on all comments)
- [ ] Only comments marked "Ready for GitHub posting" were posted
- [ ] Skipped comments NOT posted to GitHub
- [ ] Pending review created (not submitted)
- [ ] All posted comments have `**Posted**:` status in ReviewComments.md
- [ ] ReviewComments.md header updated with Pending Review ID and counts
- [ ] Posted comment bodies contain only description + suggestion (no rationale)
- [ ] Multi-PR: Each PR has its own pending review
- [ ] Non-GitHub: Manual posting instructions provided

## Completion Response

**GitHub PRs (Success):**
```
Activity complete.
Artifact updated: .paw/reviews/<identifier>/ReviewComments.md

GitHub Posting Summary:
- Pending Review Created: Review ID 12345678
- Comments Posted: 6 of 8 (2 skipped per critique)
- Status: Pending review awaiting human submission

Posted comments:
| Comment | GitHub ID |
|---------|-----------|
| auth.ts L45-50 | comment-abc |
| db.ts L120-125 | comment-def |
| ... | ... |

Skipped (not posted):
- api.ts L88 - stylistic preference
- utils.ts L200 - already addressed

NOTE: The pending review is ready for your review in GitHub.
Edit or delete any comments, then submit when satisfied.
```

**Multi-PR (Success):**
```
Activity complete.

GitHub Posting Summary:
- PR repo-a#123: Pending review created (Review ID: 111), 4 comments posted
- PR repo-b#456: Pending review created (Review ID: 222), 3 comments posted
- Total: 7 comments posted, 2 skipped

Artifacts updated:
- .paw/reviews/PR-123-repo-a/ReviewComments.md
- .paw/reviews/PR-456-repo-b/ReviewComments.md

NOTE: Review pending reviews in GitHub for each PR before submitting.
```

**Non-GitHub:**
```
Activity complete.
Artifact updated: .paw/reviews/<identifier>/ReviewComments.md

Non-GitHub Context - Manual Posting Required:
- Comments ready for posting: 6
- Comments skipped per critique: 2
- Manual posting instructions added to ReviewComments.md

Review the Manual Posting Instructions section to post comments to your review platform.
```

**Partial Failure:**
```
Activity complete with errors.

GitHub Posting Summary:
- PR repo-a#123: ✓ Success (Review ID: 111, 4 comments)
- PR repo-b#456: ✗ Failed - permission denied

Partial success: 1 of 2 PRs posted.
Manual posting instructions added for failed PR.
```
