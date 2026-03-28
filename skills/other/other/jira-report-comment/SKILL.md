---
name: jira-report-comment
description: >-
  This skill should be used when the user asks to "jira report", "post update to jira",
  "summarize commits for jira", "report to jira", "update the ticket", "comment on the ticket",
  "generate implementation report", "write a jira comment", "summarize my changes",
  or wants to notify PM/QA about completed work on a Jira ticket.
  Generates a business-friendly implementation report from git commits and saves it as a local markdown report.
allowed-tools: Read, Write, Bash, mcp__atlassian__getJiraIssue, AskUserQuestion
user-invocable: true
---

# Jira Report Comment

Generate a non-technical, business-focused summary of git changes for a Jira issue and save it as a markdown report.

**Announce at start:** "Using the jira-report-comment skill to generate an implementation report."

## Step 1: Resolve the Issue Key

Determine the Jira issue key using this priority:

1. If the user provided an issue key (e.g., "CX-4328"), use it directly.
2. Otherwise, extract from the current branch name:
   ```bash
   git branch --show-current
   ```
   Parse the ticket ID using the pattern `[A-Z]+-[0-9]+` (e.g., `feature/ABC-1234-description` yields `ABC-1234`).
3. If no key can be determined, ask the user.

**Always confirm** the resolved key with the user before proceeding: "I detected **CX-4328** from your branch. Use this issue key?"

### Reserve the Report File

Immediately after confirming the issue key, reserve the output file. This locks the filename for the entire session — all subsequent writes go to this same file.

```bash
mkdir -p docs/jira-reports
touch "docs/jira-reports/$(date +%Y-%m-%d)-$(date +%s)-<ISSUE_KEY>.md"
```

Store the full file path in conversation context (e.g., `docs/jira-reports/2026-03-27-1743091200-ABC-123.md`). This is the only file you will write to for the rest of this session. If the skill is invoked again in the same session for the same issue, reuse this path — do not create a new file.

## Step 2: Fetch Jira Issue Context

Retrieve the issue to understand what was requested. Try the Atlassian MCP tool first:

```
mcp__atlassian__getJiraIssue
  issueIdOrKey: "<ISSUE_KEY>"
```

If the MCP tool is unavailable or fails, ask the user to provide the issue context manually: "Atlassian MCP is not available. Please paste the issue text (title, description, acceptance criteria) or provide an XML export."

Extract and note:
- **Issue title** — what the ticket is about
- **Description** — acceptance criteria, requirements, business context
- **Issue type** — bug, story, task (shapes the report tone)
- **Status** — current workflow state

This context is essential. The report must map code changes back to what was actually requested in the ticket.

## Step 3: Gather Commits and Diffs

Find all commits referencing the issue key:

```bash
git log --grep="<ISSUE_KEY>" --format="%H %s" --reverse
```

If no commits found, widen the search:

```bash
git log --all --grep="<ISSUE_KEY>" --format="%H %s" --reverse
```

If still no commits, fall back to diffing the current branch against its base:

```bash
git merge-base HEAD main
git diff $(git merge-base HEAD main)..HEAD --stat
git diff $(git merge-base HEAD main)..HEAD
```

Try `main`, then `master`, then `develop` as the base branch. If no meaningful diff is found, inform the user and stop.

For the aggregate diff across all found commits (first commit's parent to last commit):

```bash
git diff <FIRST_COMMIT>^..<LAST_COMMIT> --stat
git diff <FIRST_COMMIT>^..<LAST_COMMIT>
```

If the first commit is the initial repository commit (no parent), use `git diff $(git hash-object -t tree /dev/null)..<LAST_COMMIT>` instead.

This shows the **net result** across all commits, not incremental progress. The aggregate diff reveals what actually changed, while individual commits often contain scaffolding and refinements.

If the diff is very large (50+ files), focus on the stat summary and read only the most significant files. Configuration files, test files, and migration files often reveal intent better than implementation details.

## Step 4: Analyze and Generate the Report

Load the reference template:
- **`references/report-template.md`** — read this now for the output structure

Analyze the diffs with a **business lens**. Map every code change to a user-facing or system-facing outcome.

### Analysis Checklist

- What new capabilities were added?
- What existing behavior was changed or fixed?
- What was removed or deprecated?
- Which parts of the application are affected (API endpoints, UI screens, background jobs, database)?
- Are there new dependencies, configurations, or environment requirements?
- What are the testing considerations for QA?
- Are there any risks, limitations, or known issues?

### Tone and Language

- Write for a PM, QA engineer, or architect who has not read the code
- Describe outcomes, not implementation: "Medical credential verification now checks the NPI Registry" not "Added NpiRegistryService class with HTTP client"
- Load **`references/formatting-rules.md`** and follow all rules strictly
- If the `humanizer` skill is available, run the final report through it before presenting to the user

## Step 5: Save the Report

Write the report content to the reserved file path (overwriting the empty placeholder):

```
Write tool -> file_path: <RESERVED_FILE_PATH>
              content: <REPORT_CONTENT>
```

Present the report to the user in the conversation and confirm: "Report saved to `<RESERVED_FILE_PATH>`."

If the user requests changes, revise and overwrite the same file again.

## Error Handling

- **Jira issue not found:** Tell the user the key appears invalid. Ask to double-check.
- **No commits found:** Report clearly. Suggest checking the branch or that commits may use a different key format.
- **MCP tool unavailable:** Inform the user that Atlassian MCP tools are not connected. Ask the user to provide issue context manually.
- **File write fails:** Show the error. Check directory permissions and retry.

## Constraints

- NEVER commit or stage the report file — just write it and leave it untracked
- NEVER include raw code snippets, file paths, or class names in the report unless necessary to describe an API endpoint, configuration change, or other technical detail that requires exact values
- NEVER fabricate changes not evidenced by the diffs
- ALWAYS map back to the Jira issue's stated requirements when possible
- ALWAYS write to the reserved file path from Step 1 — never create additional report files
- Keep report length between 300-800 words

## Additional Resources

### Reference Files

- **`references/report-template.md`** — Structured template for the Jira comment output. Load when generating the report in Step 4.
- **`references/formatting-rules.md`** — Tone, style, and formatting constraints for the report. Load alongside the template in Step 4.
