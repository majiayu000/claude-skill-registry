---
name: ado-review
description: Use when reviewing code changes for an Azure DevOps ticket. Fetches ticket context, finds the linked PR, and performs a code review. Triggers on "review ticket", "check ticket", or ticket number mentions with review intent.
model: opus
---

# Review ADO Ticket Code Changes

Fetch ADO ticket for context → find linked PR → review the code changes against ticket requirements.

> **Read `~/.claude/skills/_ado-shared.md`** for auth, env vars, and Windows/MSYS2 patterns.

## Workflow

1. **Fetch ticket** with `$expand=all` to get description, acceptance criteria, test notes, and relations
2. **Extract PR URL** from `Microsoft.VSTS.Common.Resolution` field (HTML — parse `<a href="...">` links) or from relations (`ArtifactLink` with `vstfs:///Git/PullRequestId/...`)
3. **Extract ticket context**: description (stripped HTML), acceptance criteria, repro steps (bugs), test notes
4. **Get PR number + repo** from the PR URL (e.g. `bluebillywig/ovp6/pull/6183` → repo=`bluebillywig/ovp6`, PR=`6183`)
5. **Fetch PR diff** via `gh pr diff <number> --repo <owner/repo>`
6. **Fetch PR files** via `gh pr view <number> --repo <owner/repo> --json files`
7. **Review the code changes** using the `pr-review-toolkit:review-pr` skill or manual review, considering:
   - Does the fix address the ticket description / repro steps?
   - Are the acceptance criteria met?
   - Are there edge cases the test notes don't cover?
   - Code quality, patterns, potential regressions
8. **Output structured review** to user

## Fetch Ticket

```bash
source ~/.env && B64=$(printf ':%s' "$ADO_PAT" | base64 -w0)
curl -s -H "Authorization: Basic $B64" \
  "https://dev.azure.com/bluebillywig/BBNew/_apis/wit/workitems/<ID>?api-version=7.0&\$expand=all"
```

## Extract PR URL

The PR link is typically in `Microsoft.VSTS.Common.Resolution` as an `<a href="...">` tag. Parse it:

```bash
node -e "const html='RESOLUTION_HTML'; const m=html.match(/href=\"(https:\/\/github\.com\/[^\"]+)\"/); console.log(m?m[1]:'NO_PR_FOUND')"
```

Also check relations array for `ArtifactLink` entries containing `vstfs:///Git/PullRequestId/`.

If no PR found, ask the user for the PR URL or number.

## Fetch PR Details

```bash
# PR diff
gh pr diff <NUMBER> --repo <OWNER/REPO>

# PR metadata + files
gh pr view <NUMBER> --repo <OWNER/REPO> --json title,body,files,additions,deletions,changedFiles

# PR review comments (existing reviews)
gh pr view <NUMBER> --repo <OWNER/REPO> --json reviews
```

## Review Checklist

When reviewing, evaluate against the ticket context:

### Correctness
- Does the change fix the described bug / implement the requested feature?
- Are repro steps addressed? (for bugs)
- Are acceptance criteria met? (for stories/tasks)

### Completeness
- Are all scenarios from test notes covered?
- Are edge cases handled?
- Are related areas potentially affected?

### Code Quality
- Follows project patterns and conventions?
- No regressions introduced?
- No security issues (XSS, injection, etc)?
- Proper error handling?

## Output Format

```markdown
## Review: ADO #<ID> — <Title>

**PR**: <PR_URL>
**Status**: <ticket state>

### Ticket Context
<brief description of what the ticket asks for>

### Code Changes Summary
<list of files changed and what each change does>

### Findings
- ✅ <what looks good>
- ⚠️ <concerns or suggestions>
- ❌ <issues that should be fixed>

### Verdict
<LGTM / Needs changes / Questions>
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Reviewing without ticket context | Always fetch ticket first — context drives the review |
| Missing PR link | Check both Resolution field and relations array |
| Reviewing only the diff | Also check PR description, test notes, and acceptance criteria |
| Not checking test coverage | Compare test notes against actual code changes |
