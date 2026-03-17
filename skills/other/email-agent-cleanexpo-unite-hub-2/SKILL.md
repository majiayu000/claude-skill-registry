---
name: email-agent
description: Processes incoming emails for Unite-Hub. Extracts sender data, identifies communication intents, links to CRM contacts, analyzes sentiment, and updates contact records with AI insights.
---

# Email Agent Skill

## Overview
The Email Agent is responsible for:
1. **Processing unprocessed emails** from a workspace
2. **Extracting sender information** and linking to existing contacts
3. **Analyzing email content** for intents and sentiment
4. **Updating CRM contacts** with interaction data
5. **Creating audit logs** for all actions

## How to Use This Agent

### Trigger
User says: "Process emails for Duncan's workspace" or "Analyze unprocessed emails"

### What the Agent Does

#### 1. Fetch Unprocessed Emails
```
Call: convex query emails.getUnprocessed({
  orgId: "k57akqzf14r07d9q3pbf9kebvn7v7929",
  workspaceId: "kh72b1cng9h88691sx4x7krt2h7v7dehh",
  limit: 50
})
```

Returns array of emails not yet processed (`isProcessed: false`)

#### 2. For Each Email

**Step A: Extract Sender Email**
```
From: "john@techstartup.com"
Extract: sender_email = "john@techstartup.com"
```

**Step B: Link to Contact**
```
Call: convex query contacts.getByEmail({
  orgId: "k57akqzf14r07d9q3pbf9kebvn7v7929",
  workspaceId: "kh72b1cng9h88691sx4x7krt2h7v7dehh",
  email: "john@techstartup.com"
})
```

If exists → `contactId = found_contact._id`
If NOT exists → Create new contact with:
  - email: sender_email
  - name: extracted from email or "Unknown"
  - source: "email"
  - status: "lead"

**Step C: Analyze Email Content**

Extract these intent keywords:
- "interested" / "partnership" / "collaboration" → intent: **inquiry**
- "proposal" / "quote" / "pricing" → intent: **proposal**
- "issue" / "problem" / "help" → intent: **complaint**
- "?" / "how" / "what" / "when" → intent: **question**
- "follow up" / "re:" → intent: **followup**
- "meeting" / "call" / "sync" / "schedule" → intent: **meeting**

Multiple intents can apply to one email.

**Step D: Analyze Sentiment**

Read email tone:
- Positive indicators: "excited", "love", "great", "thank you", "appreciate"
- Negative indicators: "problem", "issue", "concerned", "unhappy", "urgent"
- Neutral: Standard business tone

Classify as: **positive**, **neutral**, or **negative**

**Step E: Generate Summary**

Create 1-2 sentence summary of email intent:
```
Example: "John from TechStartup is inquiring about Q4 marketing services and partnership opportunities."
```

**Step F: Mark as Processed**

Call: convex mutation emails.markProcessed({
  orgId: "k57akqzf14r07d9q3pbf9kebvn7v7929",
  emailId: "email_id_from_step_1",
  contactId: "contact_id_from_step_b",
  intents: ["inquiry", "partnership"],
  sentiment: "positive",
  summary: "John inquiring about Q4 partnership"
})

**Step G: Update Contact**

If this is a NEW interaction, update:
```
Call: convex mutation contacts.updateAiScore({
  orgId: "k57akqzf14r07d9q3pbf9kebvn7v7929",
  contactId: "contact_id",
  score: 75  // Increase score based on engagement
})

Call: convex mutation contacts.addNote({
  orgId: "k57akqzf14r07d9q3pbf9kebvn7v7929",
  contactId: "contact_id",
  note: "Email from John: Inquiring about Q4 partnership. Sentiment: positive. Intents: inquiry, partnership"
})
```

**Step H: Log Audit Event**

Call: convex mutation system.logAudit({
  orgId: "k57akqzf14r07d9q3pbf9kebvn7v7929",
  action: "email_processed",
  resource: "email",
  resourceId: "email_id",
  agent: "email-agent",
  details: JSON.stringify({
    from: "john@techstartup.com",
    intents: ["inquiry", "partnership"],
    sentiment: "positive",
    contactLinked: true
  }),
  status: "success"
})

### Error Handling

If something fails:
```
Call: convex mutation system.logAudit({
  orgId: "k57akqzf14r07d9q3pbf9kebvn7v7929",
  action: "email_processing_error",
  resource: "email",
  resourceId: "email_id",
  agent: "email-agent",
  details: JSON.stringify({ error: "error message" }),
  status: "error",
  errorMessage: "description"
})
```

Then continue to next email (don't stop).

## Summary Output

After processing all emails, provide:
```
✅ Email Processing Complete

Total processed: X
Successfully linked: X
New contacts created: X
Intents extracted: X
Average sentiment: X

Contacts engaged:
- John Smith (TechStartup) - positive, inquiry
- Lisa Johnson (eCommerce) - positive, proposal
- Carlos Rodriguez (Agency) - positive, collaboration

Next steps:
1. Review high-priority contacts (positive sentiment + inquiry)
2. Generate followup emails for warm leads
3. Schedule meetings with decision-makers
```

## Key Points

- **Org isolation**: All operations scoped to `orgId`
- **Workspace scope**: Process only emails from target workspace
- **Contact linking**: Always try to link email to existing contact
- **AI scoring**: Increase contact score when they engage (email received)
- **Audit trail**: Log every action for compliance

---

## Example: Processing One Email

**Input Email:**
```
From: john@techstartup.com
Subject: Interested in your services
Body: Hi Duncan, we're looking to revamp our marketing strategy for Q4. Would love to chat about partnership opportunities.
```

**Agent Process:**

1. ✅ Extract sender: `john@techstartup.com`
2. ✅ Query contact: Found "John Smith" in contacts
3. ✅ Extract intents: `["inquiry", "partnership"]`
4. ✅ Analyze sentiment: `"positive"` (enthusiastic tone)
5. ✅ Generate summary: "John inquiring about Q4 marketing strategy and partnership"
6. ✅ Mark email processed with contact link
7. ✅ Increase contact AI score from 68 → 78
8. ✅ Add note with timestamp and details
9. ✅ Log audit event with full context

**Result:**
- Contact updated with fresh interaction data
- Audit trail shows agent processed email
- Contact now appears in "high-value prospects" due to increased score
