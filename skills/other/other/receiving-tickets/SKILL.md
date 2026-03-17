---
name: receiving-tickets
description: |
  Fetches a Jira ticket with all linked tickets and Confluence pages, then
  creates a standardized project workspace folder with documentation files.
  Use when a QA engineer receives a new Jira ticket to work on, wants to
  start a project, trace a ticket, set up a project folder, or begin a
  QA project from a Jira issue.
disable-model-invocation: true
tools:
  - mcp-atlassian:jira_get_issue
  - mcp-atlassian:jira_search
  - mcp-atlassian:confluence_get_page
---

# receiving-tickets

Fetches a Jira ticket with all linked tickets and Confluence pages, then creates a standardized project workspace.

## Progress Checklist

Copy and track your progress:

```
- [ ] Step 1: Collect ticket data (main + related + Confluence)
- [ ] Step 2: Create folder structure
- [ ] Step 3: Download raw documentation files
- [ ] Step 4: Validate and generate summary files
- [ ] (Optional) Step 5: Initialize test scaffolding
```

## Steps

### Step 1: Collect Ticket Data

Run `/jr-trace-fetch` to fetch the main Jira ticket with all fields, comments, remote links, parent/child tickets, linked issues, and Confluence pages.

**MCP tools:** `mcp-atlassian:jira_get_issue`, `mcp-atlassian:jira_search`, `mcp-atlassian:confluence_get_page`

### Step 2: Create Folder Structure

Run `/jr-trace-structure` to create `active/[TICKET]_[Short_Description]/` with:
- `confluence/` subfolder only if Confluence links were found
- No empty folders

### Step 3: Download Raw Documentation Files

Run `/jr-trace-docs` to create these files from collected data:
1. `00_Main_Task_[TICKET].md` — main ticket details + comments
2. `01_[Description]_[TICKET].md` — one file per related ticket
3. `confluence/[Title].md` — one file per Confluence page

### Step 4: Validate and Generate Summaries

Run `/jr-trace-verify` to review created files and generate:
1. `confluence/confluence_links.md` — Confluence index with document summaries
2. `README.md` — project overview with key insights
3. `Ticket_Relationship_Diagram.md` — ticket hierarchy with progress summary
4. Validation report — file count and completeness check

### Step 5 (Optional): Initialize Test Scaffolding

If user requests project initialization, run `/pm-init` to scaffold `test_plan/` and `test_cases/` folders with README templates.

## Expected Input

Jira issue key: `PROJ-12345`

## Next Step

After receiving tickets, run `/planning-tests` to detect the ticket type and start test planning.
