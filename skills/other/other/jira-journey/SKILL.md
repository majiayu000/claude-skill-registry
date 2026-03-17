---
name: jira-journey
description: "Parse a JIRA ticket's Validation Journey section, execute the verification steps using appropriate tools (curl, test commands, database queries), capture evidence, and post to JIRA + GitHub PR using the jira-evidence skill."
allowed-tools: ["Bash", "Read", "Glob", "Grep", "Skill", "mcp__atlassian__getJiraIssue", "mcp__atlassian__updateJiraIssue"]
---

# JIRA Validation Journey (TypeScript)

Parse a JIRA ticket's Validation Journey, execute the verification steps using the appropriate tools for the change type, capture evidence at each `[EVIDENCE: name]` marker, and post to JIRA + GitHub PR.

## Arguments

`$ARGUMENTS`: `<TICKET_ID> [PR_NUMBER]`

- `TICKET_ID` (required): JIRA ticket key (e.g., `PROJ-123`)
- `PR_NUMBER` (optional): GitHub PR number to update description

## Prerequisites

- `JIRA_API_TOKEN` environment variable set
- `jira-cli` configured (`~/.config/.jira/.config.yml`)
- `gh` CLI authenticated
- Appropriate services running for the verification type (dev server, database, etc.)

## Workflow

### Step 1: Parse the Validation Journey

Run the parser script to extract the Validation Journey from the JIRA ticket description:

```bash
python3 .claude/skills/jira-journey/scripts/parse-plan.py <TICKET_ID>
```

The script outputs JSON with: `ticket`, `prerequisites`, `steps`, `viewports`, `assertions`.

Note: `viewports` may be empty for TypeScript tickets — that is expected.

### Step 2: Satisfy Prerequisites

Before starting the journey, verify each prerequisite:

1. Check if required services are running
2. Verify database connectivity if needed
3. Ensure environment variables are set
4. Run any setup commands mentioned in prerequisites

### Step 3: Execute Steps and Capture Evidence

Execute each step sequentially. For each step, determine the verification approach based on the step text and change type:

- **API endpoints** → Run curl commands, capture HTTP response to `evidence/NN-name.txt`
- **Database changes** → Run psql/migration commands, capture schema output to `evidence/NN-name.txt`
- **Background jobs** → Trigger the job, check queue/state, capture logs to `evidence/NN-name.txt`
- **Library/utility changes** → Run tests, capture output to `evidence/NN-name.txt`
- **Security fixes** → Reproduce exploit attempt, verify fix, capture output to `evidence/NN-name.txt`

At each `[EVIDENCE: name]` marker, capture stdout/stderr to a numbered file:

#### Evidence Naming Convention

Evidence files are named: `{NN}-{evidence-name}.txt` (or `.json` for structured data)

- `NN`: zero-padded sequential number (01, 02, 03...)
- `evidence-name`: the value from `[EVIDENCE: name]` in the JIRA step

Example:

```text
evidence/
  01-health-check.json
  02-schema-after-migration.txt
  03-rate-limit-response.txt
  comment.txt
  comment.md
```

### Step 4: Generate Evidence Templates

After capturing all evidence, run the template generator:

```bash
python3 .claude/skills/jira-journey/scripts/generate-templates.py \
  <TICKET_ID> \
  <PR_NUMBER> \
  <BRANCH_NAME> \
  ./evidence
```

This generates `evidence/comment.txt` (JIRA wiki markup) and `evidence/comment.md` (GitHub markdown) with evidence formatted as code blocks.

### Step 5: Post Evidence

Use the jira-evidence skill to post everything:

```bash
bash .claude/skills/jira-evidence/scripts/post-evidence.sh <TICKET_ID> ./evidence <PR_NUMBER>
```

### Step 6: Verify

Confirm evidence is posted to both the JIRA ticket and GitHub PR.

## Verification Patterns Reference

The agent should use patterns from the project's `verfication.md` when executing steps:

| Change Type | Verification Method | Evidence Format |
|---|---|---|
| API endpoint | `curl -s localhost:PORT/endpoint` | JSON response |
| Database migration | `psql -c "\d table"` or migration output | Schema text |
| Background job | Trigger + check state | Log output |
| Library/utility | `bun run test -- path/to/test` | Test output |
| Security fix | Reproduce + verify fix | Request/response |
| Auth/authz | Multi-role verification | Status codes per role |

## Troubleshooting

### Evidence file is empty

Ensure the command succeeded and produced output. Use `2>&1` to capture both stdout and stderr.

### Parser returns no steps

The ticket may not have a Validation Journey section. Use `/jira-add-journey <TICKET_ID>` to add one.
