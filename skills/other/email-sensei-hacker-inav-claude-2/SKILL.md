---
description: Read and manage internal email messages between project roles
triggers:
  - read your email
  - check your email
  - read your inbox
  - check your inbox
  - read your messages
  - check your messages
  - check inbox
  - any new messages
  - any new email
---

# Internal Email System

This project uses an internal email system for communication between roles (Manager, Developer, Release Manager, Tester, etc.).

## Directory Structure

Each role has its own email folder under `claude/{role}/email/`:

- Inbox: `claude/{role}/email/inbox/`
- Inbox Archive: `claude/{role}/email/inbox-archive/`
- Sent: `claude/{role}/email/sent/`
- Outbox (pending delivery): `claude/{role}/email/outbox/`

**Current roles:**
- `manager/email/`
- `developer/email/`
- `release-manager/email/`
- `security-analyst/email/`
- `tester/email/` (future)

## Reading Email

1. First, determine your role by checking CLAUDE.local.md
2. List all files in your inbox directory:
   ```bash
   ls -lt claude/{role}/email/inbox/
   ```
3. You always have permission to read claude/{role}/email/inbox/ and all files within. Do not request permission to read this directory.
4. Read each message file to display contents
5. Summarize messages in a table format showing:
   - Date
   - Type (Task Assignment, Completion Report, Reminder, Question, etc.)
   - Subject/Summary
   - Action needed (if any)

## Processing Email

**For completion reports:**
- Review the report
- If work is verified complete, archive to `email/inbox-archive/`
- Update INDEX.md if needed

**For reminders:**
- Keep in inbox until the remind-on date
- Take action when due

**For questions:**
- Respond by creating a file in `email/sent/` and copying to the sender's `email/inbox/`

## Sending Email

1. Create message file in your `email/sent/` folder with naming convention:
   `YYYY-MM-DD-HHMM-{type}-{brief-description}.md`

2. Copy the file to the recipient's inbox:
   ```bash
   cp claude/{your-role}/email/sent/{filename}.md claude/{recipient-role}/email/inbox/
   ```

## Email Templates

**Task Assignment:**
```markdown
# Task Assignment: <Title>

**Date:** YYYY-MM-DD HH:MM
**Project:** <project-name>
**Priority:** High | Medium | Low
**Estimated Effort:** X-Y hours

## Task
<Description>

## What to Do
1. Step 1
2. Step 2

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

---
**{Role}**
```

**Completion Report:**
```markdown
# Task Completed: <Title>

**Date:** YYYY-MM-DD
**From:** {Role}
**Type:** Completion Report

## Status: COMPLETED

## Summary
<What was done>

## Branch
**Branch:** `branch-name`
**Commit:** `hash`

## Changes
<Files modified>

---
**{Role}**
```

## Checking for Undelivered Mail

Also check outbox folders for messages waiting to be delivered:
```bash
ls claude/*/email/outbox/
```

If messages exist, they need to be moved to the recipient's `email/inbox/`.

---

## Related Skills

- **communication** - Communication guidelines and message templates
- **projects** - Query project status (tasks often arrive via email)
