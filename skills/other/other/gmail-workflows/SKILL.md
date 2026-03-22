---
name: gmail-workflows
description: "Automate Gmail with intelligent workflows - attachment management, email organization, auto-archiving, and Google Drive integration"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: productivity
tags:
  - gmail
  - google-drive
  - email-automation
  - workflow
  - n8n
department: Operations

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - gpt-4
    - gpt-4o

mcp:
  server: google-workspace-mcp
  tools:
    - gmail_search
    - gmail_get_attachments
    - gmail_apply_label
    - gmail_archive
    - gdrive_upload
    - gdrive_create_folder

capabilities:
  - email_attachment_extraction
  - automatic_file_organization
  - email_filtering_rules
  - drive_synchronization
  - notification_setup

languages:
  - en
  - zh

related_skills:
  - email-drafter
  - email-classifier
  - file-organizer
---

# Gmail Workflows

Automate Gmail with intelligent workflows for attachment management, email organization, and Google Drive integration. Based on n8n's 7,800+ workflow templates.

## Overview

This skill helps you design and implement Gmail automation workflows that:
- Automatically save attachments to Google Drive
- Organize emails with smart labeling
- Archive processed emails
- Send notifications via Slack/Email
- Track email metrics

## Core Workflow Templates

### 1. Gmail Attachment Manager

**Purpose**: Automatically extract attachments from emails and save to Google Drive

**Workflow Steps**:
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Gmail       │───▶│ Filter by   │───▶│ Extract     │───▶│ Upload to   │
│ Trigger     │    │ Criteria    │    │ Attachments │    │ Google Drive│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                │
                         ┌─────────────┐    ┌─────────────┐    │
                         │ Send        │◀───│ Apply Label │◀───┘
                         │ Notification│    │ & Archive   │
                         └─────────────┘    └─────────────┘
```

**Configuration**:
```yaml
trigger:
  type: gmail_new_email
  filters:
    has_attachment: true
    from: ["*@company.com", "*@vendor.com"]
    subject_contains: ["invoice", "report", "contract"]

actions:
  - extract_attachments:
      file_types: [pdf, xlsx, docx, csv]
      max_size_mb: 25
  
  - upload_to_drive:
      folder_path: "/Attachments/{year}/{month}"
      naming_pattern: "{filename}_{sender}_{date}"
      create_folder_if_missing: true
  
  - organize_email:
      apply_label: "Processed/Attachments"
      mark_as_read: true
      archive: true
  
  - notify:
      channel: slack
      message: "New attachment saved: {filename} from {sender}"
```

**Best Practices**:
- Use specific sender filters to avoid processing spam
- Set file size limits to prevent storage issues
- Use date-based folder structure for easy retrieval
- Enable duplicate detection to avoid redundant uploads

---

### 2. Invoice Auto-Archiver

**Purpose**: Automatically collect and organize invoices from email

**Workflow Steps**:
```
Gmail Trigger → Detect Invoice → Extract PDF → OCR/Parse → Save to Drive → Update Spreadsheet → Archive Email
```

**Configuration**:
```yaml
trigger:
  subject_patterns:
    - "invoice"
    - "bill"
    - "statement"
    - "付款"
    - "发票"

processing:
  - detect_invoice:
      methods: [subject_keywords, attachment_name, sender_domain]
  
  - extract_data:
      fields: [invoice_number, amount, date, vendor, due_date]
      use_ocr: true
  
  - save_to_drive:
      folder: "/Finance/Invoices/{year}/{vendor}"
      naming: "{date}_{vendor}_{amount}"
  
  - update_tracker:
      spreadsheet: "Invoice Tracker"
      columns: [Date, Vendor, Amount, Invoice#, Status, File_Link]
  
  - archive:
      label: "Finance/Invoices"
      star: true
```

---

### 3. Client Communication Organizer

**Purpose**: Automatically organize client emails by project/client

**Configuration**:
```yaml
rules:
  - name: "Client A Emails"
    condition:
      from_domain: "clienta.com"
    actions:
      - apply_label: "Clients/Client A"
      - forward_to: "team-a@company.com"
      - save_attachments: "/Clients/Client A/{subject}"

  - name: "Project X Updates"
    condition:
      subject_contains: ["Project X", "PX-"]
    actions:
      - apply_label: "Projects/Project X"
      - add_to_task: "Project X Board"
      - notify_slack: "#project-x"

  - name: "Urgent Requests"
    condition:
      subject_contains: ["URGENT", "ASAP", "紧急"]
      is_unread: true
    actions:
      - apply_label: "Priority/Urgent"
      - send_sms: "+1234567890"
      - move_to_inbox: true
```

---

### 4. Email Analytics Dashboard

**Purpose**: Track email metrics and generate reports

**Metrics to Track**:
```yaml
daily_metrics:
  - emails_received: count(inbox)
  - emails_sent: count(sent)
  - response_time_avg: avg(reply_time)
  - unread_count: count(unread)
  - attachment_count: count(has_attachment)

weekly_report:
  - top_senders: group_by(from, count)
  - busiest_hours: group_by(hour, count)
  - label_distribution: group_by(label, count)
  - response_rate: sent / received

automation:
  - schedule: "every Monday 9am"
  - output: Google Sheets
  - notify: Slack #email-metrics
```

---

## Implementation Guide

### Using n8n

```javascript
// n8n Workflow: Gmail to Google Drive
{
  "nodes": [
    {
      "name": "Gmail Trigger",
      "type": "n8n-nodes-base.gmailTrigger",
      "parameters": {
        "pollTimes": { "item": [{ "mode": "everyMinute" }] },
        "filters": { "labelIds": ["INBOX"] }
      }
    },
    {
      "name": "Filter Attachments",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "boolean": [{
            "value1": "={{ $json.hasAttachment }}",
            "value2": true
          }]
        }
      }
    },
    {
      "name": "Get Attachments",
      "type": "n8n-nodes-base.gmail",
      "parameters": {
        "operation": "getAttachments",
        "messageId": "={{ $json.id }}"
      }
    },
    {
      "name": "Upload to Drive",
      "type": "n8n-nodes-base.googleDrive",
      "parameters": {
        "operation": "upload",
        "folderId": "your-folder-id",
        "name": "={{ $json.filename }}"
      }
    }
  ]
}
```

### Using Google Apps Script

```javascript
// Gmail to Drive Automation
function processNewEmails() {
  const threads = GmailApp.search('has:attachment is:unread');
  const targetFolder = DriveApp.getFolderById('FOLDER_ID');
  
  threads.forEach(thread => {
    const messages = thread.getMessages();
    messages.forEach(message => {
      const attachments = message.getAttachments();
      attachments.forEach(attachment => {
        // Save to Drive
        const file = targetFolder.createFile(attachment);
        
        // Rename with date and sender
        const newName = `${Utilities.formatDate(message.getDate(), 'GMT', 'yyyy-MM-dd')}_${message.getFrom()}_${attachment.getName()}`;
        file.setName(newName);
      });
      
      // Mark as processed
      message.markRead();
      thread.addLabel(GmailApp.getUserLabelByName('Processed'));
    });
  });
}

// Set up trigger
function setupTrigger() {
  ScriptApp.newTrigger('processNewEmails')
    .timeBased()
    .everyMinutes(5)
    .create();
}
```

---

## Common Workflow Patterns

### Pattern 1: Filter → Process → Organize → Notify

```
Email arrives
    │
    ▼
┌─────────────────┐
│ Apply Filters   │ → Skip if doesn't match
│ (sender, subject│
│  attachment)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Process Content │ → Extract data, attachments
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Organize        │ → Save files, apply labels
│                 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Notify          │ → Slack, email, SMS
│                 │
└─────────────────┘
```

### Pattern 2: Batch Processing

```yaml
schedule: "daily at 6am"
steps:
  1. Collect all unprocessed emails from last 24h
  2. Group by category (invoices, reports, misc)
  3. Batch upload to respective Drive folders
  4. Generate summary report
  5. Send daily digest to stakeholders
```

### Pattern 3: Conditional Routing

```yaml
conditions:
  - if: attachment_type == "pdf" AND subject contains "invoice"
    then: route_to_finance_folder
  
  - if: from_domain in ["important-client.com"]
    then: priority_handling + immediate_notification
  
  - if: attachment_size > 10MB
    then: save_to_large_files_folder + skip_backup
  
  - default:
    then: standard_processing
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Attachments not detected | Check MIME type filters, increase trigger frequency |
| Duplicate files | Enable deduplication by hash or filename |
| Rate limits | Reduce trigger frequency, use batch processing |
| Permission errors | Re-authorize OAuth credentials |
| Large files failing | Set size limits, use chunked upload |

---

## Security Considerations

1. **OAuth Scopes**: Request minimal permissions
   - `gmail.readonly` for reading
   - `gmail.modify` for labels/archive
   - `drive.file` for Drive access

2. **Data Privacy**: 
   - Don't log email content
   - Use secure storage for credentials
   - Implement retention policies

3. **Access Control**:
   - Limit who can modify workflows
   - Audit automation activities
   - Use separate service accounts

---

## Output Example

**Daily Email Report**:
```markdown
# Email Activity Report - 2026-01-30

## Summary
- Emails Received: 47
- Emails Sent: 23
- Attachments Processed: 12
- Average Response Time: 2.3 hours

## Attachment Processing
| File | Sender | Saved To | Time |
|------|--------|----------|------|
| Invoice_Jan.pdf | vendor@co.com | /Finance/Invoices | 09:15 |
| Report_Q4.xlsx | team@company.com | /Reports/Q4 | 10:30 |
| Contract_v2.docx | legal@client.com | /Contracts | 14:22 |

## Labels Applied
- Finance/Invoices: 5 emails
- Projects/Active: 12 emails
- Clients/Priority: 8 emails

## Pending Actions
- 3 emails require manual review
- 2 large attachments need approval
```

---

*Gmail Workflows Skill - Part of Claude Office Skills*
