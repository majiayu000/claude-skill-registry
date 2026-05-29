---
name: jira-journey
description: "Parse a JIRA ticket's Validation Journey section, execute the verification steps, capture evidence, and post to JIRA + GitHub PR using the jira-evidence skill."
---

# JIRA Validation Journey

Parse a JIRA ticket's Validation Journey, execute the verification steps using the project's appropriate tools, capture evidence at each marker, and post to JIRA + GitHub PR.

## Arguments

`$ARGUMENTS`: `<TICKET_ID> [PR_NUMBER]`

- `TICKET_ID` (required): JIRA ticket key (e.g., `PROJ-123`)
- `PR_NUMBER` (optional): GitHub PR number to update description

## Prerequisites

- `JIRA_API_TOKEN` environment variable set
- `jira-cli` configured (`~/.config/.jira/.config.yml`)
- `gh` CLI authenticated

## Workflow

### Step 1: Parse the Validation Journey

Run the parser script to extract the Validation Journey from the JIRA ticket description:

```bash
python3 .claude/skills/jira-journey/scripts/parse-plan.py <TICKET_ID>
```

The script outputs JSON with: `ticket`, `prerequisites`, `steps`, `viewports`, `assertions`.

### Step 2: Satisfy Prerequisites

Before starting the journey, verify each prerequisite listed in the parsed output.

### Step 3: Execute Steps

Execute each step sequentially. At each step with an evidence marker (`[SCREENSHOT: name]` or `[EVIDENCE: name]`), capture the appropriate evidence.

The execution method depends on the project type:
- **UI projects**: Use Playwright MCP browser tools, capture screenshots at each viewport
- **API projects**: Use curl or test commands, capture stdout/stderr
- **Library projects**: Run tests, capture output

Stack-specific overrides provide the actual execution implementation.

### Step 4: Generate Evidence Templates

After capturing all evidence, run the template generator to format evidence for JIRA and GitHub.

### Step 5: Post Evidence

Use the `/jira-evidence` skill to post everything:

```bash
bash .claude/skills/jira-evidence/scripts/post-evidence.sh <TICKET_ID> ./evidence <PR_NUMBER>
```

### Step 6: Verify

Confirm evidence renders at both the JIRA ticket and GitHub PR.
