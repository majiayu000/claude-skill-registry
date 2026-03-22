---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: Email Classifier
description: "Automatically categorize emails by type, priority, and required action"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: productivity
tags:
  - email
  - classification
  - organization
department: All

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# Skill Capabilities
capabilities:
  - email_categorization
  - priority_assignment
  - labeling

# Language Support
languages:
  - en
  - zh
---

# Email Classifier

Automatically categorize and prioritize emails to help manage inbox overload.

## Overview

This skill helps you:
- Classify emails by category and type
- Determine priority and urgency
- Identify required actions
- Filter out low-value emails
- Organize for efficient processing

## Classification Categories

### Primary Categories
| Category | Description | Examples |
|----------|-------------|----------|
| **Action Required** | Needs your response/action | Requests, approvals, questions |
| **FYI** | Informational, no action needed | Updates, announcements, reports |
| **Waiting** | You're waiting for others | Follow-ups, pending responses |
| **Delegated** | Forward to someone else | Wrong recipient, team matters |
| **Archive** | Keep but no action | Confirmations, receipts |
| **Delete** | Low value, can remove | Spam, irrelevant promos |

### Email Types
| Type | Description |
|------|-------------|
| **Meeting** | Invites, updates, cancellations |
| **Task/Request** | Someone asking you to do something |
| **Question** | Needs your answer |
| **Update/Report** | Status updates, progress reports |
| **Approval** | Needs your sign-off |
| **Newsletter** | Subscribed content |
| **Marketing** | Promotional content |
| **Alert/Notification** | System alerts, notifications |
| **Personal** | Non-work related |
| **Spam/Phishing** | Unwanted or suspicious |

### Priority Levels
| Priority | Response Time | Indicators |
|----------|---------------|------------|
| 🔴 **Urgent** | Within hours | Deadline today, executive request, blocking issue |
| 🟠 **High** | Within 24h | Important client, time-sensitive, direct request |
| 🟡 **Normal** | Within week | Standard requests, routine matters |
| 🟢 **Low** | When convenient | FYI, newsletters, non-urgent updates |

## How to Use

### Single Email Classification
```
"Classify this email: [paste email content]"
```

### Batch Classification
```
"Classify these emails and organize by priority:
1. [Email 1]
2. [Email 2]
3. [Email 3]"
```

### With Rules
```
"Classify my emails. Treat anything from @client.com as high priority"
```

## Output Format

### Single Email
```markdown
## Email Classification

**From**: sender@example.com
**Subject**: Q1 Budget Approval Needed

| Attribute | Value |
|-----------|-------|
| **Category** | Action Required |
| **Type** | Approval |
| **Priority** | 🔴 Urgent |
| **Deadline** | EOD Friday |
| **Sender Importance** | High (CFO) |

### Recommended Action
Review attached budget and approve/reject by Friday EOD.

### Suggested Response Time
Within 4 hours

### Labels/Tags
`finance`, `approval`, `q1-budget`, `executive`
```

### Batch Results
```markdown
## Email Classification Results

**Total Emails**: 15
**Processing Date**: 2026-01-29

### Summary
| Category | Count | % |
|----------|-------|---|
| Action Required | 4 | 27% |
| FYI | 6 | 40% |
| Delete/Spam | 3 | 20% |
| Waiting | 2 | 13% |

### 🔴 Urgent (2)
1. **[Subject]** from [Sender] - [Action needed]
2. **[Subject]** from [Sender] - [Action needed]

### 🟠 High Priority (3)
1. **[Subject]** from [Sender] - [Type]
2. ...

### 🟡 Normal (5)
1. ...

### 🟢 Low/FYI (5)
1. ...
```

## Custom Rules

### Define Your Rules
```markdown
## My Email Rules

### VIP Senders (Always High Priority)
- CEO, CFO, CTO
- Direct manager
- Key clients: @bigclient.com

### Auto-Archive
- Newsletters (unless from [specific])
- Automated reports (after reading)
- CC-only emails (if no @mention)

### Auto-Delegate
- IT support requests → it-team@
- HR questions → hr@

### Red Flags (Mark Urgent)
- "URGENT" in subject
- Legal/compliance mentions
- Customer complaints
```

## Spam/Phishing Detection

### Warning Signs
```markdown
## Suspicious Email Indicators

**Risk Level**: 🔴 High / 🟠 Medium / 🟢 Low

### Red Flags Detected
- [ ] Sender domain doesn't match display name
- [ ] Urgency pressure tactics
- [ ] Request for credentials/personal info
- [ ] Suspicious links (hover to check)
- [ ] Unexpected attachments
- [ ] Grammar/spelling errors
- [ ] Generic greeting ("Dear Customer")

### Recommendation
[Do not click links / Report as phishing / Safe to proceed]
```

## Workflow Suggestions

### Processing Order
```markdown
## Recommended Processing Order

### Morning (30 min)
1. 🔴 Urgent emails first (2 emails, ~10 min)
2. 🟠 High priority (3 emails, ~15 min)
3. Quick wins under 2 min (5 emails, ~5 min)

### Batch Later
- 🟡 Normal priority - schedule 1 hour block
- 🟢 Newsletters - end of day or weekend

### Delegate Now
- Forward [Email X] to [Person] for handling
```

### Suggested Folder Structure
```
📁 Inbox
├── 📁 Action Required
│   ├── 📁 Today
│   ├── 📁 This Week
│   └── 📁 Waiting For Response
├── 📁 FYI / Read
├── 📁 Reference
│   ├── 📁 Projects
│   ├── 📁 Clients
│   └── 📁 Receipts
└── 📁 Newsletters
```

## Integration Ideas

### Calendar Integration
- Meeting emails → Check/update calendar
- Deadline mentions → Create calendar reminder

### Task Integration
- Action items → Create tasks
- Follow-ups → Set reminder

### CRM Integration
- Client emails → Log in CRM
- Lead inquiries → Create lead record

## Limitations

- Cannot access email accounts directly
- Classification is based on content provided
- May miss context from email threads
- Cannot guarantee phishing detection
- Personal judgment needed for edge cases
