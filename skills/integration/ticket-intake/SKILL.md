---
name: ticket-intake
description: 'Parse Notion ticket URL, extract all data, initialize pipeline run. Use when starting work on a new ticket or when asked to pick up a ticket.'
---

# Ticket Intake

Parses a Notion ticket URL, extracts all relevant information, and initializes a pipeline run directory for tracking work.

## Quick Start

When given a Notion ticket URL:

1. Parse the URL to extract page ID
2. Fetch ticket content via Notion MCP
3. Extract all relevant properties
4. Create pipeline run directory with artifacts
5. Update Notion ticket status
6. Output summary and next steps

## Prerequisites

- Notion MCP connected and authenticated
- If not setup: `claude mcp add --transport http notion https://mcp.notion.com/mcp`
- Authenticate via `/mcp` command if prompted

## Workflow

### Step 1: Parse Notion URL

Extract page ID from URL formats:

```
https://www.notion.so/workspace/Page-Title-abc123def456...
https://notion.so/Page-Title-abc123def456...
https://www.notion.so/abc123def456...
```

Page ID is the 32-character hex string (with or without hyphens).

### Step 2: Fetch Ticket Content

Use `Notion:notion-fetch` with the page URL or ID:

```
Fetch the full page content including all properties
```

### Step 3: Extract Ticket Data

Extract these properties (names may vary):

| Property      | Expected Name             | Type         |
| ------------- | ------------------------- | ------------ |
| Title         | Name / Title              | Title        |
| Status        | Status                    | Select       |
| Assignee      | Assignee / Assigned To    | Person       |
| Description   | -                         | Page content |
| Slack Link    | Slack Link / Slack Thread | URL          |
| GitHub PR     | GitHub PR / PR Link       | URL          |
| Priority      | Priority                  | Select       |
| Area          | Area / Category           | Select       |
| Related Tasks | Related Tasks             | Relation     |

**If properties are missing**: Note what's unavailable and continue with available data.

### Step 4: Create Pipeline Run Directory

Create directory structure at:

```
$HOME/repos/ticket-to-pr-pipeline/runs/{ticket-id}/
├── status.json          # Current pipeline status
├── ticket.json          # Extracted ticket data
├── research-report.md   # (created later)
├── plan.md              # (created later)
├── tasks.md             # (created later)
└── review-comments.md   # (created later)
```

**Generate ticket-id**: Use short form of page ID (first 8 characters) or sanitized title.

**Initialize status.json**:

```json
{
  "ticketId": "abc12345",
  "ticketUrl": "https://notion.so/...",
  "status": "research",
  "startedAt": "2024-01-15T10:30:00Z",
  "lastUpdated": "2024-01-15T10:30:00Z"
}
```

**Initialize ticket.json**:

```json
{
  "id": "abc12345",
  "url": "https://notion.so/...",
  "title": "Ticket title",
  "status": "Not Started",
  "assignee": "Name",
  "priority": "High",
  "area": "UI",
  "description": "Full description text",
  "acceptanceCriteria": ["Criterion 1", "Criterion 2"],
  "slackLink": "https://slack.com/...",
  "githubPR": null,
  "relatedTasks": [],
  "fetchedAt": "2024-01-15T10:30:00Z"
}
```

### Step 5: Update Notion Ticket (REQUIRED)

**⚠️ DO NOT SKIP THIS STEP. This is a required action, not optional.**

**⚠️ Follow [Notion Write Safety](docs/notion-write-safety.md) rules.**

Use `Notion:notion-update-page` to update the ticket:

1. **Status**: Set to "In Progress" (only valid from "Not Started")
2. **Assignee**: Assign to pipeline owner (Notion ID: `175d872b-594c-81d4-ba5a-0002911c5966`)

```json
{
  "page_id": "{page_id_from_ticket}",
  "command": "update_properties",
  "properties": {
    "Status": "In Progress",
    "Assignee": "175d872b-594c-81d4-ba5a-0002911c5966"
  }
}
```

**After the update succeeds**, log the write to `status.json`:

```json
{
  "notionWrites": [
    {
      "field": "Status",
      "value": "In Progress",
      "previousValue": "Not Started",
      "at": "2024-01-15T10:30:00Z",
      "skill": "ticket-intake",
      "success": true
    }
  ]
}
```

If update fails, log with `success: false` and continue.

### Step 6: Verify Completion

**Before outputting summary, confirm:**

- [ ] Run directory created at `runs/{ticket-id}/`
- [ ] `ticket.json` saved with extracted data
- [ ] `status.json` initialized
- [ ] **Notion Status updated to "In Progress"**
- [ ] **Notion Assignee set to pipeline owner**
- [ ] `notionWrites` array in status.json has entries

If any Notion updates were skipped, go back and complete Step 5 now.

### Step 7: Output Summary

Print a clear summary:

```markdown
## Ticket Intake Complete

**Title:** [Ticket title]
**ID:** abc12345
**Status:** In Progress (updated)
**Priority:** High
**Area:** UI

### Description

[Brief description or first 200 chars]

### Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

### Links

- **Ticket:** [Notion link]
- **Slack:** [Slack link] ← Copy thread content manually if needed

### Pipeline Run

- **Directory:** $HOME/repos/ticket-to-pr-pipeline/runs/abc12345/
- **Status:** Research phase initialized

---

**Next Step:** Load the `research-orchestrator` skill to begin research phase.
```

## Error Handling

### Invalid URL

```
❌ Invalid Notion URL format.
Expected: https://notion.so/... or https://www.notion.so/...
Received: [provided URL]
```

### Authentication Error

```
⚠️ Notion authentication required.
Run: claude mcp add --transport http notion https://mcp.notion.com/mcp
Then authenticate via /mcp command.
```

### Missing Properties

Continue with available data and note what's missing:

```
⚠️ Some properties unavailable:
- Slack Link: not found
- Related Tasks: not found

Proceeding with available data...
```

### Page Not Found

```
❌ Notion page not found or inaccessible.
- Check the URL is correct
- Ensure you have access to this page
- Try re-authenticating via /mcp
```

## Database Reference: Comfy Tasks

The "Comfy Tasks" database has these properties (verify via `notion-search`):

- **Status values**: Not Started, In Progress, In Review, Done
- **Team assignment**: "Frontend Team" for unassigned tickets
- **Filtering note**: Team filtering in Notion may have quirks - handle gracefully

### Pipeline Owner Details

When assigning tickets, use these identifiers:

| Platform        | Identifier                             |
| --------------- | -------------------------------------- |
| Notion User ID  | `175d872b-594c-81d4-ba5a-0002911c5966` |
| Notion Name     | Christian Byrne                        |
| Notion Email    | cbyrne@comfy.org                       |
| Slack User ID   | U087MJCDHHC                            |
| GitHub Username | christian-byrne                        |

**To update Assignee**, use the Notion User ID (not name):

```
properties: {"Assignee": "175d872b-594c-81d4-ba5a-0002911c5966"}
```

### Finding Active Tickets

To list your active tickets:

```
Use Notion:notion-search for "Comfy Tasks"
Filter by Assignee = current user OR Team = "Frontend Team"
```

## Slack Thread Handling

If a Slack link exists:

1. Convert to browser-friendly URL format
2. Print the link prominently
3. Instruct user to manually copy thread content
4. Thread content can be pasted into research phase

### Slack URL Conversion

Notion stores Slack links in `slackMessage://` format:

```
slackMessage://comfy-organization.slack.com/CHANNEL_ID/THREAD_TS/MESSAGE_TS
```

Convert to browser-clickable format:

```
https://comfy-organization.slack.com/archives/CHANNEL_ID/pMESSAGE_TS_NO_DOT
```

**Example:**

- Input: `slackMessage://comfy-organization.slack.com/C075ANWQ8KS/1766022478.450909/1764772881.854829`
- Output: `https://comfy-organization.slack.com/archives/C075ANWQ8KS/p1764772881854829`

(Remove the dot from the last timestamp and prefix with `p`)

### Output Format

```
📋 **Manual Action Required:**
Slack MCP not available. Please copy the thread content from:
https://comfy-organization.slack.com/archives/{CHANNEL_ID}/p{MESSAGE_TS}

Paste into the research phase when prompted.
```

## Notes

- This skill focuses ONLY on intake - it does not do research
- Always create the run directory even if some data is missing
- Pipeline status tracks progress through phases: research → planning → implementation → review → QA → done
- The `runs/` directory is gitignored - artifacts stay local
