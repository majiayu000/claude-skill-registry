---
name: powerskills-outlook
description: Outlook email and calendar automation via COM. Read inbox, unread, sent items. Search emails. Send, reply, draft. List calendar events and mail folders. Use when needing to check work email, read/send Outlook messages, search mail, or view calendar. Requires Outlook desktop app on Windows.
license: MIT
metadata:
  author: aloth
  cli: powerskills
  parent: powerskills
---

# PowerSkills — Outlook

Outlook COM automation for email and calendar.

## Requirements

- Microsoft Outlook (desktop, COM-enabled)
- Non-admin PowerShell session (admin session cannot access user's Outlook profile)

## Actions

```powershell
.\powerskills.ps1 outlook <action> [--params]
```

| Action | Params | Description |
|--------|--------|-------------|
| `inbox` | `--limit N` | List inbox messages (default: 15) |
| `unread` | `--limit N` | List unread messages (default: 20) |
| `sent` | `--limit N` | List sent items (default: 15) |
| `read` | `--index N --folder inbox\|sent\|drafts` | Read full email by index |
| `search` | `--query "text" --folder inbox\|sent --limit N` | Search by subject/body |
| `calendar` | `--days N` | List upcoming events (default: 7 days) |
| `send` | `--to addr --subject text --body text [--cc addr] [--draft]` | Send or save as draft |
| `reply` | `--index N --body text [--reply-all] [--draft]` | Reply to inbox email |
| `folders` | | List all mail folders with counts |

## Examples

```powershell
# Check unread mail
.\powerskills.ps1 outlook unread --limit 5

# Read a specific email
.\powerskills.ps1 outlook read --index 0 --folder inbox

# Read from sent folder
.\powerskills.ps1 outlook read --index 3 --folder sent

# Search for emails
.\powerskills.ps1 outlook search --query "project update" --limit 10

# Save a reply as draft
.\powerskills.ps1 outlook reply --index 0 --body "Thanks, will review." --draft

# Check calendar for next 3 days
.\powerskills.ps1 outlook calendar --days 3
```

## Output Fields

### List actions (inbox, unread, sent)
`index`, `subject`, `sender`, `sender_email`, `received`, `unread`, `importance`, `has_attachments`

### Read action
`subject`, `sender`, `sender_email`, `to`, `cc`, `received`, `body`, `unread`, `importance`, `attachments`

### Calendar action
`subject`, `start`, `end`, `location`, `organizer`, `is_recurring`, `all_day`, `busy_status`
