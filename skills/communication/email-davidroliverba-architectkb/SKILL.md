---
skill: email
model: haiku
description: Process emails into structured notes and draft responses
tags: [activity/documentation, domain/tooling]
---

# /email - Email Capture and Draft Skill

## Purpose

Capture emails into the vault as structured Email notes, linking them to projects, people, tasks, systems, and data assets. Also supports drafting outbound emails with context from the vault.

## Usage

```
/email                          # Process email from clipboard/pasted content
/email draft <topic>            # Draft a new email using vault context
/email capture                  # Manually capture and process an email
/email thread <subject>         # Find all emails in a conversation thread
```

## Email Direction Types

| Direction  | Description                         | Status Values                 |
| ---------- | ----------------------------------- | ----------------------------- |
| `inbound`  | Email received from someone else    | received, processed, archived |
| `outbound` | Email you sent or plan to send      | draft, sent, archived         |
| `draft`    | Email being composed (not yet sent) | draft                         |

## Email Purpose Categories (GTD-inspired)

| Purpose           | Description                               | Handling                           |
| ----------------- | ----------------------------------------- | ---------------------------------- |
| `action-required` | Requires response or action within 2 mins | Process immediately or create Task |
| `waiting`         | Sent request, awaiting response           | Track in createdTasks              |
| `fyi`             | Informational, no action needed           | Archive after reading              |
| `reference`       | Important info to keep for future         | Store with good keywords           |
| `decision`        | Contains or requests a decision           | Link to relevant ADR/Project       |

## Capture Mode (`/email` or `/email capture`)

### When user pastes email content:

1. **Extract metadata automatically:**
   - Subject line
   - From (sender email/name)
   - To (recipient list)
   - CC (if present)
   - Date and time
   - Thread references (Re:, Fwd:)

2. **Identify relationships:**
   - Search vault for matching Person notes by email address or name
   - Identify project context from keywords or explicit mentions
   - Detect related systems or data assets mentioned
   - Check for existing thread (matching subject line with Re:/Fwd:)

3. **Classify the email:**
   - Determine direction: inbound or outbound
   - Assess purpose: action-required, waiting, fyi, reference, decision
   - Set priority based on urgency indicators

4. **Extract actionable items:**
   - Identify any tasks or action items mentioned
   - Offer to create Task notes linked to this email
   - Note any deadlines mentioned

5. **Create the Email note:**
   - Filename: `Email - <from/to> - <subject>.md` (truncate if too long)
   - Location: Root directory
   - Populate frontmatter with extracted metadata
   - Fill Content section with email body
   - Add Key Points summary
   - Link to identified Person, Project, System, DataAsset notes

### Example Frontmatter Output

```yaml
type: Email
title: "Project Alpha Data Access Request"
created: 2026-01-26
modified: 2026-01-26
tags: [project/alpha, domain/data, activity/communication]

# Email Metadata
subject: "Re: Project Alpha Data Access Request"
from: "[[John Smith]]"
to: ["user@example.com"]
cc: ["[[Jane Doe]]"]
date: 2026-01-24
time: "14:32"

# Direction & Purpose
direction: inbound
purpose: action-required
originalEmailId: null

# Relationships
project: "[[Project - Alpha]]"
person: "[[John Smith]]"
relatedTo: ["[[ADR - Data Integration]]"]
thread: "[[Email - Alex Thompson - Project Alpha Data Access Request]]"
createdTasks: ["[[Task - Respond to data access request]]"]
relatedSystems: ["[[System - Data Platform]]", "[[System - ERP]]"]
relatedDataAssets: []

# Status
status: processed
priority: high

# Quality
summary: "Request for data access credentials to Data Platform staging environment for testing"
keywords: [data-access, staging, credentials]
```

## Draft Mode (`/email draft <topic>`)

### Purpose

Generate draft email content using context from the vault.

### Process

1. **Gather context:**
   - Search vault for notes related to the topic
   - Find relevant ADRs, decisions, project status
   - Identify key stakeholders from Person notes
   - Check recent meetings on the topic

2. **Generate draft:**
   - Create appropriate greeting
   - Structure email with clear purpose statement
   - Include relevant facts from vault context
   - Add clear call-to-action or next steps
   - Professional closing

3. **Create Email note with status: draft:**
   - Pre-populate frontmatter
   - Include generated content in Content section
   - Mark any facts that need verification

4. **Present to user for review:**
   - Show the draft
   - Highlight sources used
   - Ask for any modifications

### Example Draft Command

```
/email draft Project Alpha status update to Sarah Chen
```

Would:

1. Search for Project - Alpha notes
2. Find recent meetings and decisions
3. Look up Sarah Chen in People
4. Generate professional status update email
5. Create `Email - Alex Thompson - Project Alpha Status Update.md`

## Thread Mode (`/email thread <subject>`)

### Purpose

Find and display all emails in a conversation thread.

### Process

1. Search for Email notes matching subject (with/without Re:/Fwd: prefix)
2. Order chronologically
3. Display thread summary with key points from each
4. Offer to create a Page summarising the thread

## File Naming Convention

| Direction | Pattern                              | Example                                  |
| --------- | ------------------------------------ | ---------------------------------------- |
| Inbound   | `Email - <sender> - <subject>.md`    | `Email - John Smith - Data Request.md`   |
| Outbound  | `Email - <recipient> - <subject>.md` | `Email - Sarah Chen - Status Update.md`  |
| Draft     | `Email - Draft - <subject>.md`       | `Email - Draft - Architecture Review.md` |

If subject is too long, truncate to 50 characters.

## Tags to Apply

Always include:

- At least one `project/` or `domain/` tag
- `activity/communication`

Optional:

- `status/action-required` (if urgent)
- `audience/executive` (if to senior leadership)

## Integration with Outlook MCP

If Outlook MCP is available, the skill can:

- Read emails directly from inbox
- Send drafted emails after user approval
- Search for related emails in Outlook

### Using Outlook MCP

```javascript
// Read recent unread emails
mcp__outlook - mcp__outlook_mail({ operation: "unread", limit: 10 });

// Search for emails about a topic
mcp__outlook - mcp__outlook_mail({ operation: "search", searchTerm: "Alpha" });

// Send after approval
mcp__outlook -
  mcp__outlook_mail({
    operation: "send",
    to: "recipient@example.com",
    subject: "Subject",
    body: "Email content",
  });
```

## Two-Minute Rule Implementation

When processing emails:

1. **Can it be handled in < 2 minutes?**
   - YES: Handle immediately, archive email
   - NO: Create Task note linked to email

2. **Is it waiting for someone else?**
   - YES: Set purpose to `waiting`, create follow-up Task with due date
   - NO: Continue processing

3. **Is it just for reference?**
   - YES: Set purpose to `reference`, ensure good keywords for search
   - NO: Determine specific action required

## Archive Pattern

When archiving processed emails:

```yaml
archived: true
archivedDate: 2026-01-26
archivedReason: "Processed and no longer active"
```

Move to: `Archive/Emails/` (create folder if needed)

## Example Workflow

### User pastes:

```
From: john.smith@example.com
To: user@example.com
Date: 24 Jan 2026 14:32
Subject: Re: Project Alpha Data Access Request

Hi,

Following our meeting yesterday, I need access to the Data Platform staging environment to begin testing the data integration. Could you raise a request with the data platform team?

The specific datasets we need are:
- Maintenance history (last 12 months)
- Parts inventory current state

Timeline: We need this by end of next week for sprint planning.

Thanks,
John
```

### Claude processes and creates:

**File**: `Email - John Smith - Project Alpha Data Access Request.md`

**Actions offered**:

1. Create Task: "Raise Data Platform staging access request for Alpha"
2. Link to existing: [[Project - Alpha]], [[John Smith]], [[System - Data Platform]]
3. Set priority: high (due to deadline)
4. Add to thread if previous email exists

## Quality Checklist

Before completing email capture:

- [ ] Subject extracted correctly
- [ ] Sender linked to Person note (or created)
- [ ] Project identified and linked
- [ ] Purpose category assigned
- [ ] Action items extracted
- [ ] Keywords populated for search
- [ ] Summary written

## Error Handling

- **No sender found**: Prompt for name, offer to create Person note
- **No project match**: Ask user to specify or leave null
- **Ambiguous thread**: Present options to user
- **Long email**: Summarise key points, store full text in Content

## Related Skills

- `/meeting` - For meeting notes (emails may reference meetings)
- `/task` - For creating tasks from email action items
- `/person` - For creating person notes from new contacts
