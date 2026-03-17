---
name: GitLab Code Review
description: Performs comprehensive code reviews of GitLab merge requests, analyzing code quality, security, performance, and best practices. Use when the user says "review" or "code review" or asks to review merge requests or analyze branch changes before merging.
allowed-tools: gitlab-mcp(get_merge_request), gitlab-mcp(get_merge_request_diffs), gitlab-mcp(list_merge_requests), gitlab-mcp(create_note), gitlab-mcp(create_merge_request_thread), gitlab-mcp(mr_discussions), gitlab-mcp(get_issue), gitlab-mcp(list_commits), gitlab-mcp(get_commit), gitlab-mcp(get_commit_diff), gitlab-mcp(get_branch_diffs), gitlab-mcp(get_file_contents), gitlab-mcp(get_project), gitlab-mcp(list_pipelines), gitlab-mcp(list_pipeline_jobs), gitlab-mcp(get_pipeline), gitlab-mcp(get_pipeline_job_output)
license: MIT
metadata:
  author: Foundation Skills
  version: 1.0.0
  mcp-server: gitlab-mcp
---

# GitLab Code Review

Perform comprehensive code reviews of GitLab merge requests, providing actionable feedback on code quality, security, performance, and best practices.

## GitLab Instance Configuration

This skill is configured for a self-hosted GitLab instance:
- **GitLab URL:** https://gitlab-erp-pas.dedalus.lan
- All project identifiers, URLs, and references should use this self-hosted instance
- Ensure you have appropriate access credentials configured for this GitLab server

## When to Use This Skill

Activate this skill when:
- The user types "review" or "code review" (with or without slash command)
- The user types "review MR-123" or "review !123" to review a specific merge request
- The user types "review ISSUE-ID" (e.g., "review #456") to review the MR associated with a GitLab issue
- The user asks to review a merge request
- Analyzing code changes before merging
- Performing code quality assessments
- Checking for security vulnerabilities or performance issues
- Reviewing merge request diffs

## Critical Rules

**IMPORTANT: Always confirm project_id before reviewing merge requests**

**Always provide constructive feedback framed as questions, not directives**

**Only review changes introduced in the merge request, not unrelated code**

## Workflow

### 1. Identify the Merge Request

#### Merge Request IID Provided

**If a merge request IID is provided** (e.g., "review !123" or "review MR 123"):

1. Extract the MR IID from the user input
2. Verify the project context (ask user if not clear)
3. Fetch merge request details using `gitlab-mcp(get_merge_request)`

#### GitLab Issue ID Provided

**If a GitLab issue ID is provided** (e.g., "review #456"):

1. Fetch issue details using `gitlab-mcp(get_issue)` to understand context
2. Find related merge requests using `gitlab-mcp(list_merge_requests)` with search filter
3. If multiple MRs found, ask user to select the one to review
4. Proceed with the selected MR

#### No Specific MR Provided

**If no MR is specified** (e.g., just "review"):

1. List recent open merge requests using `gitlab-mcp(list_merge_requests)` with `state: "opened"`
2. Present the list to the user
3. Ask user to select which MR to review

### 2. Gather Merge Request Context

**Self-hosted GitLab Instance:** https://gitlab-erp-pas.dedalus.lan

Use `gitlab-mcp(get_merge_request)` to retrieve:

- Title and description
- Source and target branches
- Author information
- State (open, merged, closed)
- Labels and milestones
- Approval status
- Pipeline status
- `diff_refs` (base_sha, head_sha, start_sha) for accurate diff comparison

**Extract key information:**
```
Project: namespace/project
MR: !123 - "Feature: Add user authentication"
Author: @username
Source: feature/auth -> Target: main
Status: Open | Pipeline: Passed | Approvals: 1/2
```

### 3. Analyze the Changes

#### Get File Changes

Use `gitlab-mcp(get_merge_request_diffs)` to retrieve:
- List of changed files
- Additions and deletions per file
- Diff content for each file

**Pagination**: If many files changed, use pagination parameters (`page`, `per_page`) to retrieve all changes.

#### Get Detailed File Content

For complex changes, use `gitlab-mcp(get_file_contents)` to:
- View the complete file context
- Understand surrounding code
- Check for consistency with existing patterns

**Parameters:**
- `project_id`: Project identifier
- `file_path`: Path to the file
- `ref`: Use the source branch or head_sha from diff_refs

#### Analyze Commits

Use `gitlab-mcp(list_commits)` with:
- `project_id`: Project identifier
- `ref_name`: Source branch name

Then use `gitlab-mcp(get_commit)` and `gitlab-mcp(get_commit_diff)` to:
- Understand commit history
- Review individual commit changes
- Check commit message quality

### 4. Check Existing Discussions

Use `gitlab-mcp(mr_discussions)` to:
- Review existing feedback and discussions
- Avoid duplicate comments
- Understand ongoing conversations
- Check for unresolved threads

### 5. Check Pipeline Status

Use `gitlab-mcp(list_pipelines)` and `gitlab-mcp(get_pipeline)` to:
- Verify CI/CD pipeline status
- Check for failed jobs
- Review test results

If pipeline failed, use `gitlab-mcp(get_pipeline_job_output)` to understand failures.

### 6. Perform Comprehensive Code Review

Conduct a thorough review of **only the changes introduced in this merge request**.

#### Code Quality Assessment

- Code style and formatting consistency
- Variable and function naming conventions
- Code organization and structure
- Adherence to DRY (Don't Repeat Yourself) principles
- Proper abstraction levels

#### Technical Review

- Logic correctness and edge cases
- Error handling and validation
- Performance implications
- Security considerations (input validation, SQL injection, XSS, etc.)
- Resource management (memory leaks, connection handling)
- Concurrency issues if applicable

#### Best Practices Check

- Design patterns usage
- SOLID principles adherence
- Testing coverage implications
- Documentation completeness
- API consistency
- Backwards compatibility

#### Dependencies and Integration

- New dependencies added
- Breaking changes to existing interfaces
- Impact on other parts of the system
- Database migration requirements

### 7. Generate Review Report

Create a structured code review report with:

1. **Executive Summary**: High-level overview of changes and overall assessment

2. **Statistics**:
   - Files changed, lines added/removed
   - Commits reviewed
   - Critical issues found

3. **Strengths**: What was done well

4. **Issues by Priority**:
   - 🔴 **Critical**: Must fix before merging (bugs, security issues)
   - 🟡 **Important**: Should address (performance, maintainability)
   - 🟢 **Suggestions**: Nice to have improvements

5. **Detailed Findings**: For each issue include:
   - File and line reference
   - A question framing the concern
   - Context explaining why you're asking
   - Code example if helpful

6. **Security Review**: Specific security considerations

7. **Performance Review**: Performance implications

8. **Testing Recommendations**: What tests should be added

9. **Documentation Needs**: What documentation should be updated

### 8. Add Comments to Merge Request (Optional)

**CRITICAL: Ask user before adding comments to the MR**

If user wants to add feedback directly to the MR:

#### General Comment

Use `gitlab-mcp(create_note)` to add a general comment:
- `project_id`: Project identifier
- `merge_request_iid`: MR internal ID
- `body`: Comment content in Markdown

#### Line-Specific Discussion

Use `gitlab-mcp(create_merge_request_thread)` for code-specific feedback:
- `project_id`: Project identifier
- `merge_request_iid`: MR internal ID
- `body`: Discussion content
- `position`: Object with diff position details:
  - `base_sha`: From diff_refs
  - `head_sha`: From diff_refs
  - `start_sha`: From diff_refs
  - `new_path`: File path
  - `new_line`: Line number for new code
  - `old_path`: File path (for modifications)
  - `old_line`: Line number for removed code

## Feedback Style: Questions, Not Directives

**Frame all feedback as questions, not commands.** This encourages dialogue and respects the author's context.

### Examples

❌ **Don't write:**
- "You should use early returns here"
- "This needs error handling"
- "Extract this into a separate function"
- "Add a null check"

✅ **Do write:**
- "Could this be simplified with an early return?"
- "What happens if this API call fails? Would error handling help here?"
- "Would it make sense to extract this into its own function for reusability?"
- "Is there a scenario where this could be null? If so, how should we handle it?"

### Why Questions Work Better

- The author may have context you don't have
- Questions invite explanation rather than defensiveness
- They acknowledge uncertainty in the reviewer's understanding
- They create a conversation rather than a checklist

## Review Report Template

```markdown
# Code Review: !{MR_IID} - {MR_TITLE}

## Executive Summary
{Brief overview of changes and overall assessment}

## Merge Request Details
- **Project**: {project_path}
- **Author**: @{author}
- **Source Branch**: {source_branch} → **Target**: {target_branch}
- **Pipeline Status**: {status}
- **Approvals**: {current}/{required}

## Statistics
| Metric | Count |
|--------|-------|
| Files Changed | {count} |
| Lines Added | +{additions} |
| Lines Removed | -{deletions} |
| Commits | {commit_count} |

## Strengths
- {strength_1}
- {strength_2}

## Issues Found

### 🔴 Critical
{critical_issues_or_none}

### 🟡 Important
{important_issues_or_none}

### 🟢 Suggestions
{suggestions_or_none}

## Security Review
{security_findings}

## Performance Review
{performance_findings}

## Testing Recommendations
- {test_recommendation_1}
- {test_recommendation_2}

## Documentation Needs
- {doc_need_1}

## Verdict
{APPROVED | CHANGES_REQUESTED | NEEDS_DISCUSSION}
```

## Examples

### Example 1: Review a Specific Merge Request

```
User: Review !42 in namespace/project

Assistant actions:
1. gitlab-mcp(get_merge_request) with project_id="namespace/project", merge_request_iid=42
2. gitlab-mcp(get_merge_request_diffs) with project_id="namespace/project", merge_request_iid=42
3. gitlab-mcp(mr_discussions) to check existing feedback
4. gitlab-mcp(list_pipelines) to check CI status
5. Analyze changes and generate report
6. Present review to user
7. Ask if user wants comments added to the MR
```

### Example 2: Review MR Related to an Issue

```
User: Review the MR for issue #123

Assistant actions:
1. gitlab-mcp(get_issue) with project_id="namespace/project", issue_iid=123
2. gitlab-mcp(list_merge_requests) with search for "#123" or issue reference
3. Present found MRs and ask user to confirm
4. Proceed with code review workflow
```

### Example 3: List Open MRs for Review

```
User: Show me open merge requests to review

Assistant actions:
1. gitlab-mcp(list_merge_requests) with state="opened"
2. Present list with key details (title, author, pipeline status)
3. Ask user which MR to review
```

## Important Notes

- **Only review changes from THIS merge request** - do not comment on code that wasn't changed
- Frame feedback as questions to encourage dialogue
- Be constructive and specific in feedback
- Provide code examples for suggested improvements
- Acknowledge good practices and improvements
- Prioritize issues clearly (Critical > Important > Suggestions)
- Consider the context and purpose of changes
- Check pipeline status before concluding review
- Review existing discussions to avoid duplicate feedback
- **Always ask before adding comments to the MR**
- Verify the review addresses acceptance criteria if linked to an issue
