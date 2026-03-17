---
name: dev-workflow-review-pr
description: Review GitHub pull requests using the gh CLI. Fetches PR diff and details, optional Jira or GitHub issue context from branch, analyzes for code quality, security, tests, and style, then posts inline comments. Use when the user asks to review a PR, check a pull request, or mentions a PR URL or number.
---

# GitHub PR Review

Review pull requests using the GitHub CLI (`gh`), analyzing changes and posting inline comments.

## Prerequisites

- GitHub CLI installed and authenticated (`gh auth status`)
- Repository must be a GitHub repo

## Workflow

### Step 1: Identify the PR

If the user provides:

- **PR URL**: Extract owner/repo and PR number from the URL
- **PR number**: Use current repo context
- **Nothing specific**: **ALWAYS use the AskQuestion tool:**
  - Title: "Which PR?"
  - Question: "Which pull request would you like to review?"
  - Options:
    - id: "number", label: "Specify PR number"
    - id: "url", label: "Provide PR URL"
    - id: "current", label: "Review current branch's PR"

  After the user selects, ask conversationally for the PR number or URL if needed.

### Step 2: Fetch PR Information

Run these commands to gather context:

```bash
# Get PR metadata (title, body, author, base branch)
gh pr view <PR_NUMBER> --json title,body,author,baseRefName,headRefName,additions,deletions,files

# Get the full diff
gh pr diff <PR_NUMBER>

# Get existing review comments (to avoid duplicates)
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments --jq '.[].body'
```

### Step 3: Fetch Ticket or Issue Context

Extract the ticket or issue identifier from the PR's head branch name (`headRefName` from Step 2).

- **Jira:** Pattern `[A-Z]+-[0-9]+` (e.g. RNDCORE-1234, RETIRE-5678). Fetch via Jira MCP (getJiraIssue) with fields summary, description, issuetype, acceptanceCriteria. Use to understand intent, verify the PR addresses requirements, and check acceptance criteria.
- **GitHub:** Pattern `issue-(\d+)` or leading `(\d+)-` (e.g. issue-1, 1-add-feature). Fetch via `gh issue view N --repo owner/repo --json title,body,state,number` (use PR base repo if not in branch). Use title and body to understand intent and verify the PR addresses the issue.

**If no ticket/issue pattern is found**: Skip this step and proceed to Step 4.

### Step 4: Analyze Changes

Review each file in the diff for:

#### Code Quality

- Logic correctness and edge case handling
- Function size and single responsibility
- Code duplication
- Appropriate error handling
- Clear naming and readability

#### Security

- Input validation
- SQL injection, XSS, or injection vulnerabilities
- Hardcoded secrets or credentials
- Insecure dependencies
- Authentication/authorization issues

#### Testing

- Test coverage for new functionality
- Edge cases covered in tests
- Test quality and maintainability

#### Style

- Consistency with codebase conventions
- Proper formatting (defer to linters when present)
- Documentation for public APIs

### Step 5: Post Inline Comments

For each issue found, post an inline comment:

```bash
gh api repos/{owner}/{repo}/pulls/<PR_NUMBER>/comments \
  --method POST \
  -f body="<COMMENT>" \
  -f commit_id="$(gh pr view <PR_NUMBER> --json headRefOid --jq '.headRefOid')" \
  -f path="<FILE_PATH>" \
  -F line=<LINE_NUMBER> \
  -f side="RIGHT"
```

#### Comment Format

Prefix your comments with one of the following:

- **blocking**: This means you will not approve this PR because you view this as a required change. Leave this as a comment and in general, do NOT use GitHub's "Request Changes" functionality as that will block the PR author from moving forward. You may be out sick or have PTO and then you're unnecessarily blocking a PR while out that could have already addressed your concerns.

  If two other reviewers choose to approve this PR despite the blocking comment, it is up to the PR author to decide whether or not to update the PR and address the blocking comment, or merge anyways.

- **follow-up**: This means you feel strongly about updating the code, but understanding timelines and efficiency, it's ok to make these changes in a follow-up PR or another story.

- **nit**: This means you would consider doing this a different way, or this is optional.

- **info**: This is just an FYI or education you want to pass on, but they don't need to change anything.

- **check**: You see a potential issue here but you're not sure, this should be looked at further before merging.

- **question**: You don't see a potential issue, you just want to learn more about this.

**Important**: NEVER approve PRs. Only leave comments. Approvals should come from human reviewers, not automated agents.

Example comments:

```
blocking: This SQL query is vulnerable to injection. User input must be parameterized.

follow-up: This function is getting long. Consider splitting it in a future PR.

nit: I'd name this `getUserById` instead of `getUser` for clarity.

info: FYI, we have a utility function in `utils/format.ts` that does this same thing.

check: This looks like it might cause a race condition, but I'm not certain. Worth investigating.

question: Why did you choose to use a Map here instead of an object?
```

### Step 6: Submit Review Summary

After posting inline comments, submit the review as a comment (NEVER approve):

```bash
# If blocking issues found
gh pr review <PR_NUMBER> --comment --body "Left some blocking feedback that should be addressed before merge. See inline comments."

# If no blocking issues found
gh pr review <PR_NUMBER> --comment --body "Review complete. Left some feedback - see inline comments."

# If no issues found at all
gh pr review <PR_NUMBER> --comment --body "Review complete. No issues found. LGTM from an automated review perspective - awaiting human approval."
```

**Important**:

- NEVER use `--approve` - approvals must come from human reviewers only
- NEVER use `--request-changes` as this blocks the PR author from merging
- Always use `--comment` to leave feedback without blocking

## Review Checklist

Copy and track progress:

```
PR Review Progress:
- [ ] Fetched PR metadata and diff
- [ ] Fetched Jira or GitHub issue context (if available)
- [ ] Reviewed for code quality issues
- [ ] Checked for security vulnerabilities
- [ ] Verified test coverage
- [ ] Verified PR addresses ticket/issue requirements
- [ ] Checked style consistency
- [ ] Posted inline comments
- [ ] Submitted review summary
```

## Common Patterns

### Reviewing a PR by Number

```bash
# In the repo directory
gh pr diff 123
gh pr view 123 --json title,body,files
```

### Reviewing a PR by URL

```bash
# Extract from URL: https://github.com/owner/repo/pull/123
gh pr diff 123 --repo owner/repo
```

### Checking Out PR Locally (if needed)

```bash
gh pr checkout 123
# Run tests, linters, etc.
npm test
```

## Notes

- Always check existing comments before posting to avoid duplicates
- For large PRs (>500 lines), focus on the most impactful changes first
- If the PR description is unclear, ask clarifying questions before diving deep
- When unsure about project conventions, check similar files in the codebase
