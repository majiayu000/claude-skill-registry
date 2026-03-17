---
name: add-backlog-to-prd
description: "Fetch open issues from brave/brave-browser (by label or assignee) and add missing ones to the Brave Core PRD backlog. Triggers on: add backlog to prd, update prd with issues, sync backlog, fetch issues for prd, add intermittent tests."
allowed-tools: Bash, Read, Grep, Glob
---

# PRD Brave Core - Add Backlog Issues

Automatically fetch open issues from the brave/brave-browser repository and add any missing ones to the Brave Core Bot PRD.

---

## The Job

1. Get the configured git user.name (used as the GitHub username)
2. Fetch all open issues with the `bot/type/test` label from brave/brave-browser
3. Fetch all open issues assigned to the git user.name from brave/brave-browser
4. Combine both sets of issues (deduplicated)
5. Compare with existing issues in the PRD (`./prd.json`)
6. Add any missing issues as new user stories
7. Provide a recap of what was added

**Important:** This skill is specifically for the Brave Core Bot PRD format.

---

## Step 1: Get Git Username

Get the configured git user.name to use as the GitHub username for fetching assigned issues:

```bash
git config user.name
```

---

## Step 2: Fetch GitHub Issues

Fetch issues from TWO sources and combine them:

1. **Labeled issues** (bot/type/test):
```bash
gh issue list --repo brave/brave-browser --label "bot/type/test" --state open --json number,title,url,labels --limit 100
```

2. **Assigned issues** (assigned to the git user.name):
```bash
gh issue list --repo brave/brave-browser --assignee "<git_user_name>" --state open --json number,title,url,labels --limit 100
```

3. **Combine and deduplicate** by issue number:
```bash
jq -s '[.[][] | {number, title, url, labels}] | unique_by(.number)' <(gh issue list --repo brave/brave-browser --label "bot/type/test" --state open --json number,title,url,labels --limit 100) <(gh issue list --repo brave/brave-browser --assignee "$(git config user.name)" --state open --json number,title,url,labels --limit 100)
```

---

## Step 3: Process Issues and Update PRD

A single helper script handles both new and existing PRDs:

```bash
jq -s '[.[][] | {number, title, url, labels}] | unique_by(.number)' \
  <(gh issue list --repo brave/brave-browser --label "bot/type/test" --state open --json number,title,url,labels --limit 100) \
  <(gh issue list --repo brave/brave-browser --assignee "$(git config user.name)" --state open --json number,title,url,labels --limit 100) | \
  .claude/skills/add-backlog-to-prd/update_prd_with_issues.py ./prd.json > /tmp/prd_updated.json && \
  mv /tmp/prd_updated.json ./prd.json
```

If `./prd.json` doesn't exist yet, the script creates a new PRD. If it already exists, it only appends missing issues and never modifies existing stories.

### What the script does:

- **Detect issue type**: Issues with "Test failure:" title prefix or `bot/type/test` label are treated as test issues; all others get generic stories
- **For test issues**:
  - Extract test names from issue titles (handles multiple prefixes)
  - Determine test location at generation time by running `git grep` to find if the test is in `src/brave` or `src` (Chromium)
  - Generate test-specific acceptance criteria with correct test binary and filter
  - Include `testType`, `testLocation`, and `testFilter` fields
- **For generic issues**:
  - Use the issue title directly as the story title
  - Generate standard acceptance criteria (fetch issue, analyze, implement, build, format, presubmit, gn_check, find and run relevant tests)
- Generate proper user story structure with sequential US-XXX IDs and priority ordering
- Skip issues already in the PRD
- Safety check verifies existing stories were not modified

---

## Step 4: Provide Recap

Generate a comprehensive recap showing:

1. **New Issues Added**: List each new user story with:
   - US-XXX number
   - Test name
   - Issue number
   - Test type
   - Status

2. **Existing Issues Status Overview**: Summarize existing stories by status:
   - Merged
   - Pushed
   - Pending
   - Skipped
   - Invalid

3. **Total PRD Statistics**:
   - Total count before and after
   - Count by status

---

## Example Output Format

```markdown
# PRD Update Recap

## Summary
Successfully fetched 15 open issues from the `bot/type/test` label and added 7 missing issues to the PRD.

## New Issues Added (US-016 to US-022)

1. **US-016** - Fix test: BraveSearchTestEnabled.DefaultAPIVisibleKnownHost (issue #52439)
   - Type: browser_test
   - Status: pending
   - Priority: 16

[... more entries ...]

## Existing Issues Status Overview

### Merged (6 issues)
- US-001: SolanaProviderTest.AccountChangedEventAndReload (#50022)
[... more entries ...]

### Pushed (1 issue)
[... entries ...]

### Skipped (7 issues)
[... entries ...]

### Invalid (1 issue)
[... entries ...]

### Pending (7 new issues)
[... entries ...]

## Total PRD Statistics
- Total user stories: 22 (was 15, added 7)
- Merged: 6
- Pushed: 1
- Pending: 7
- Skipped: 7
- Invalid: 1
```

---

## Important Notes

- Always preserve the exact structure of existing user stories
- Test issues include the BEST-PRACTICES.md read step in acceptance criteria
- Test type determination is critical for generating correct test commands
- Priority numbers must be sequential and not conflict with existing ones
- All new stories start in "pending" status

---

## Error Handling

- If `gh` CLI is not available, report error and exit
- If `./prd.json` doesn't exist, a new one is created automatically
- If GitHub API rate limit is hit, report error with retry time
- If `jq` is not available, report error and exit
