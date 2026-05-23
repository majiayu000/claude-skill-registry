---
name: review-pr
description: Review GitHub Pull Request and analyze unresolved review comments. Use when you need to address PR feedback or review outstanding comments.
allowed-tools: Bash(gh:*), mcp__github__*, Read, Edit, Write
argument-hint: [PR-URL]
disable-model-invocation: true
---

# GitHub Pull Request Review Assistant

Review the Pull Request at the provided URL and analyze unresolved review comments to provide comprehensive code review feedback.

## PR Information

**PR URL**: $1

Fetch the PR details using GitHub CLI:

- PR metadata: !gh pr view "$1" --json number,title,author,state,isDraft,files
- Review threads with resolution status: !gh api graphql -F query=@.claude/commands/queries/pr-review-threads.graphql -f owner="$(echo "$1" | sed -E 's#https://github.com/([^/]+)/.*#\1#')" -f repo="$(echo "$1" | sed -E 's#https://github.com/[^/]+/([^/]+)/.*#\1#')" -F number=$(echo "$1" | sed -E 's#._/pull/([0-9]+)._#\1#')

## Task Instructions

1. **Fetch PR Details**
   - Use `gh pr view` to get basic PR information
   - Use `gh api graphql` with external query file to fetch review threads
   - GraphQL query includes `isResolved` field for each thread
   - **Only process threads where `isResolved: false`**
   - Ignore all resolved threads (user intentionally closed them)

2. **Analyze Code Changes**
   - Parse GraphQL response to extract unresolved threads (`isResolved: false`)
   - For each unresolved thread, read the referenced file using Read tool
   - Verify if the issue mentioned in the comment still exists
   - Skip threads where issue was already fixed
   - Focus only on legitimate remaining issues

3. **Review Criteria**

   Apply appropriate coding guidelines based on the project's language and framework.

   Focus on:
   - **Coding Style**: Consistency, readability, naming conventions
   - **Architecture**: Design patterns, separation of concerns, modularity
   - **Side Effects**: Unintended consequences, race conditions, state mutations
   - **Potential Bugs**: Edge cases, error handling, null/undefined checks

4. **Provide Review Feedback & Apply Fixes**

   For each comment that points to a real issue:
   - **Comment Context**: Quote the original review comment
   - **File & Location**: `filepath:line_number`
   - **Code Analysis**: Examine the relevant code section
   - **Assessment**:
     - Is the concern valid?
     - What are the implications?
     - What's the recommended solution?
   - **Decision**:
     - If the concern is valid and the fix is straightforward: **IMMEDIATELY APPLY THE FIX** using Edit/Write tools
     - If the concern requires discussion or design decisions: **ASK USER** for clarification before making changes
   - **Alternative Approaches**: If applicable, suggest better implementations
   - **Guideline References**: Cite relevant coding guidelines when explaining fixes

5. **Summary**

   Provide an overall assessment:
   - Total number of review threads
   - Number of resolved threads (skipped)
   - Number of unresolved threads processed
   - Number of issues automatically fixed
   - Issues requiring user discussion (if any)
   - Overall PR quality assessment

## Output Format

```markdown
# PR Review: [PR Title]

**PR**: [PR URL]
**Status**: [open/draft/closed]
**Files Changed**: [count]

## Review Threads Analysis & Fixes

### 1. [File Path]:[Line]

**Thread Status**: Unresolved
**Comment by @[username]**:

> [quoted comment]

**Current Code Status**:

- ✅ **Already fixed** - [explanation of how it was addressed]
- OR
- ⚠️ **Issue still present** - proceeding with fix

**Analysis** (if issue still present):
[Your detailed analysis based on review criteria]

**Action Taken**:

- ✅ **Fixed automatically**: [description of fix applied]
- OR
- ⏸️ **Requires discussion**: [reason why user input is needed]

**Relevant Guideline**: [Coding guideline reference if applicable]

---

### 2. [File Path]:[Line]

...

## Overall Assessment

- **Total Review Threads**: [count]
- **Resolved Threads (Skipped)**: [count]
- **Unresolved Threads Processed**: [count]
- **Issues Fixed Automatically**: [count]
- **Issues Requiring Discussion**: [count]
- **Overall Status**: [All issues resolved / Partial / Awaiting user input]

## Additional Observations

[Any other observations about the PR quality, architecture, or patterns used]
```

## Important Notes

- **Private Repositories**: Works with `gh` CLI authentication
- **Resolution Filtering**: Uses GraphQL `isResolved` field to skip resolved threads
- **Smart Filtering**: Also verifies if issues still exist in current code
- **Focus**: Only review and fix unresolved threads with real, existing issues
- **Guidelines**: Apply appropriate coding guidelines based on project language/framework
- **Auto-Fix**: Automatically apply fixes for straightforward issues without asking
- **User Consultation**: Only ask user when the fix involves:
  - Architectural or design decisions
  - Multiple valid approaches
  - Potential breaking changes
  - Ambiguous requirements

## Example Usage

```bash
/review-pr https://github.com/owner/repo/pull/123
```

The command will fetch all review threads on PR #123, filter to only unresolved threads (`isResolved: false`), verify which issues still exist in current code, and provide fixes based on the appropriate coding guidelines.
