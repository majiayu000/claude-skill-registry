---
name: create-pr-from-spec
description: "Create GitHub Pull Request from specification using pull_request_template.md. Use when: spec needs to be converted to PR, spec is ready for review/merge, need to automate PR creation from specification file with template-based body and title."
allowed-tools: Read, Grep, Glob, Bash
---

# Create Pull Request from Specification

Create a GitHub Pull Request for a specification using the pull_request_template.md template located at `${workspaceFolder}/.github/pull_request_template.md`.

## Overview

This skill automates the creation of GitHub Pull Requests directly from specifications. It follows a structured process:

1. Analyzes the specification template requirements
2. Creates a draft PR with the target branch
3. Verifies no duplicate PRs exist
4. Updates PR body and title with template-compliant content
5. Marks PR as ready for review
6. Automatically assigns to the creator
7. Returns PR URL to user

**Key Benefits:**
- ✅ Automated PR creation from specifications
- ✅ Template-compliant PR body and title
- ✅ Duplicate PR prevention
- ✅ Auto-assignment to creator
- ✅ Streamlined spec-to-PR workflow

## When to Use

Use this skill when:

1. **Specification is ready to merge** - Convert finalized spec to PR
2. **Need automated PR creation** - Avoid manual PR drafting
3. **Template compliance required** - Ensure PR follows pull_request_template.md
4. **Multiple PRs from specs** - Batch process specifications into PRs
5. **Team collaboration** - Share specs as PRs for review

**Trigger phrases:**
- "Create pull request from spec"
- "Convert spec to PR"
- "Open PR for specification"
- "Submit spec as pull request"
- "Automate PR creation"

## Instructions

### Prerequisites

Before using this skill, ensure:
- Specification file is finalized and ready for review
- Target branch is specified (e.g., `main`, `develop`)
- `.github/pull_request_template.md` exists in the repository
- You have write access to create PRs

### Step-by-Step Process

**1. Analyze specification template**
- Extract requirements from `${workspaceFolder}/.github/pull_request_template.md`
- Use search tool to parse template sections and placeholders

**2. Create pull request draft**
- Use `create_pull_request` tool to create draft PR to target branch
- First verify no existing PR exists using `get_pull_request` to prevent duplicates
- If PR already exists, stop and report to user

**3. Get pull request changes**
- Use `get_pull_request_diff` tool to analyze differences
- Verify code changes are correct before updating

**4. Update pull request**
- Use `update_pull_request` tool to populate PR body and title
- Incorporate template sections from step 1
- Ensure all required fields are filled

**5. Mark ready for review**
- Use `update_pull_request` tool to change state from draft to ready for review
- Verify PR is no longer in draft mode

**6. Assign pull request**
- Use `get_me` to retrieve current user information
- Use `update_issue` tool to assign PR to creator

**7. Return pull request URL**
- Provide user with clickable PR URL
- Include summary of PR contents

## Examples

### Example 1: Basic PR Creation

```bash
Input: Create PR from spec to main branch
Process:
  1. Analyze pull_request_template.md
  2. Create draft PR to main
  3. Check for existing PRs
  4. Update PR title: "feat: [Feature Name from Spec]"
  5. Update PR body with template sections
  6. Mark as ready for review
  7. Assign to creator
Output: https://github.com/user/repo/pull/123
```

### Example 2: Template-Compliant PR

```markdown
PR Title: feat: Implement user authentication system

PR Body:
## Description
Implements JWT-based authentication with token refresh mechanism

## Related Issue
Closes #456

## Changes
- Added JWT middleware
- Implemented token validation
- Added refresh token endpoint

## Testing
- Unit tests for auth middleware
- Integration tests for token endpoints

## Checklist
- [x] Tests pass
- [x] Documentation updated
- [x] No breaking changes
```

### Example 3: Duplicate Prevention

```bash
Input: Create PR from spec
Check: PR for current branch already exists?
  → Yes: Report error, don't create duplicate
  → No: Proceed with PR creation
Output: "PR already exists at https://github.com/user/repo/pull/789"
```

## Requirements

- Single pull request for the complete specification
- Clear title and body identifying the specification/feature
- Pull request body follows pull_request_template.md structure
- Verification that no duplicate pull requests exist
- PR automatically assigned to creator
- No draft PRs left behind

## Success Criteria

- ✅ PR created without errors
- ✅ PR body follows pull_request_template.md structure
- ✅ PR title clearly identifies the specification/feature
- ✅ No duplicate PRs exist for the branch
- ✅ PR assigned to creator
- ✅ PR URL returned to user
- ✅ PR is ready for review (not in draft)

## Constraints and Warnings

⚠️ **Important:**
- PR creation requires write access to repository
- Target branch must exist before PR creation
- Template file must exist at `.github/pull_request_template.md`
- Cannot create PR without valid branch target
- Duplicate PRs will be detected and rejected
- PR assignment requires valid GitHub user

🚫 **Limitations:**
- Does not perform code review automatically
- Does not trigger CI/CD pipelines
- Does not merge PRs automatically
- Cannot modify existing code, only PR metadata

## Best Practices

1. **Verify before creating** - Always review specification before converting to PR
2. **Use descriptive titles** - PR titles should clearly indicate feature/fix purpose
3. **Complete template** - Ensure all required template sections are filled
4. **Link related issues** - Include issue references in PR body
5. **Test first** - Ensure all tests pass before creating PR
6. **Team review** - Get team approval before marking ready for review
7. **Clean git history** - Ensure commits are clean and well-documented

## Tools Used

- `search` - Analyze specification template requirements
- `create_pull_request` - Create new PR in draft mode
- `get_pull_request` - Check for existing PRs before creation
- `get_pull_request_diff` - Analyze PR changes
- `update_pull_request` - Update PR title, body, and state
- `update_issue` - Assign PR to creator
- `get_me` - Retrieve current user information
