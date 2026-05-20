---
name: review-pr
description: Review a pull request by checking the code changes, PR description, and CI status against the linked Jira ticket requirements. Produces an AC checklist and flags concerns.
---

# Review Pull Request

Comprehensively review a PR by comparing code changes against Jira ticket requirements.

## Requirements

- GitHub CLI (`gh`) configured
- Jira MCP server configured (for ticket lookup)

## Usage

```
/review-pr <PR-NUMBER>
/review-pr 5753
```

If no PR number provided, use the current branch's PR.

## Instructions

### 1. Get PR Details

Fetch comprehensive PR information:

```bash
# Get PR metadata
gh pr view {PR_NUMBER} --json title,body,additions,deletions,changedFiles,files,state,author,baseRefName,headRefName

# Get the full diff
gh pr diff {PR_NUMBER}

# Get CI status
gh pr checks {PR_NUMBER}
```

If no PR number provided:

```bash
gh pr view --json number
```

### 2. Extract Jira Ticket (Optional)

Find the Jira ticket from (in order of preference):

1. PR title (e.g., `feat: AB-841 pii warning`)
2. PR body (e.g., `Jira ticket number? AB-841`)
3. Branch name (e.g., `feat/AB-841-pii-warning`)

Ticket pattern: 2-4 uppercase letters, dash, numbers (e.g., `AB-23`, `SSP-456`, `MAMA-89`)

**If no ticket found:** Continue with the review without Jira comparison. Skip step 3 and 5, and note in the output that no Jira ticket was linked.

### 3. Fetch Jira Ticket Details (If Ticket Found)

Use the Jira MCP tools to get ticket requirements:

```
mcp__jira__jira_get with:
  path: /rest/api/3/issue/{ticketNumber}
  jq: "{key: key, summary: fields.summary, description: fields.description, status: fields.status.name, issuetype: fields.issuetype.name, acceptance: fields.customfield_10040}"
```

Parse the description to extract:

- Overview/context
- Acceptance criteria (look for "AC", "Acceptance Criteria", bullet points)
- Any technical requirements

### 4. Analyze the Code Changes

For each changed file, understand:

- What was added/modified/deleted
- Whether changes align with ticket requirements

For large diffs, save to a file and read in chunks if needed.

**Pay attention to:**

- Deleted code: Is it safe? Are there still imports/usages elsewhere?
- New dependencies: Are they appropriate?
- Test coverage: Are new features tested?
- Security: Any obvious vulnerabilities?

To check if deleted code is used elsewhere:

```bash
# Search for imports of deleted modules
grep -r "from.*{deleted-module}" --include="*.ts" --include="*.tsx"
grep -r "import.*{deleted-module}" --include="*.ts" --include="*.tsx"
```

### 5. Compare PR Against Jira ACs (If Ticket Found)

Create a checklist comparing each acceptance criterion against the implementation:

| AC | Status | Implementation |
|----|--------|----------------|
| {AC from ticket} | {pass/fail/partial} | {How it's implemented or why it fails} |

**If no ticket found:** Skip this step. The review will focus on code quality, CI status, and potential concerns without AC validation.

### 6. Check CI Status

Summarize the CI status:

- All checks passing?
- Any failures or warnings?

### 7. Identify Concerns

Flag any issues:

- **Scope creep**: Changes not related to the ticket
- **Missing ACs**: Requirements not implemented
- **Deleted code**: Large deletions that might break things
- **Missing tests**: New features without test coverage
- **Security**: Potential vulnerabilities
- **Breaking changes**: API changes, removed exports

### 8. Produce Review Summary

Output a structured review:

```markdown
## PR #{number} Review

**Title:** {title}
**Jira:** {ticket} - {summary}  (or "No Jira ticket linked" if none found)
**Status:** {CI status}

### Changes Overview
- {additions} additions, {deletions} deletions across {changedFiles} files
- {Brief summary of what changed}

### AC Checklist (if Jira ticket found)
| AC | Status | Implementation |
|----|--------|----------------|
| ... | ... | ... |

### Concerns
- {List any concerns or none}
- {If no Jira ticket: flag "No Jira ticket linked - cannot verify requirements"}

### Verdict
{Safe to merge / Needs changes / Needs discussion}
```

## Example Output

```
## PR #5753 Review

**Title:** feat: ge-841 pii warning
**Jira:** GE-841 - FE | Unitary AI PII Instructions
**Status:** All checks passing

### Changes Overview
- 136 additions, 1528 deletions across 37 files
- Adds PII redaction instructions to file upload screens
- Removes unused IdVerification component

### AC Checklist
| AC | Status | Implementation |
|----|--------|----------------|
| Prompt users to redact PII | Pass | New `getUploadInstructionText` utility |
| Different messages for Employed/Retired/Volunteer | Pass | Three distinct messages |
| Include data-testid | Pass | `data-testid="upload-instruction-text"` |
| BLC UK only (ok for others) | Pass | Brand check in utility |
| Update request new card journey | Pass | Both screens updated |
| Cleanup is fine if nothing breaks | Pass | Deleted unused code, CI green |

### Concerns
- None. Deleted code was not exported or used externally.

### Verdict
Safe to merge. PR fully implements all acceptance criteria.
```

## Example Output (No Jira Ticket)

```markdown
## PR #5801 Review

**Title:** chore: update dependencies
**Jira:** No Jira ticket linked
**Status:** All checks passing

### Changes Overview
- 45 additions, 32 deletions across 3 files
- Updates npm dependencies to latest versions
- Updates lock file

### Code Review
- package.json: Minor version bumps for react, typescript
- No breaking changes detected
- No new dependencies added

### Concerns
- No Jira ticket linked - cannot verify against requirements
- Consider adding a ticket reference for traceability

### Verdict
Looks safe to merge. Routine dependency update with passing CI. Recommend linking a Jira ticket for audit trail.
```
