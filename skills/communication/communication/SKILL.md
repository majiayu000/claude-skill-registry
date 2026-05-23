---
description: View cross-role communication guidelines and message templates
triggers:
  - how to communicate
  - send message
  - message template
  - communication guide
  - who do I contact
---

# Communication Guide Skill

Reference for cross-role communication in the INAV project.

## Full Documentation

Read the complete guide:
```bash
cat claude/COMMUNICATION.md
```

## Quick Reference

### Role Contacts

| Need | Contact |
|------|---------|
| Task assignment | Manager |
| Implementation help | Developer |
| Build/release issues | Release Manager |
| Project status | Manager |

### Message Flow

**To send a message:**
1. Create file in `claude/{your-role}/sent/`
2. Copy to `claude/{recipient-role}/inbox/`

**File naming:** `YYYY-MM-DD-HHMM-{type}-{description}.md`

### Message Types

- `task` - Task assignment
- `completed` - Completion report
- `status` - Status update
- `question` - Question needing answer
- `response` - Response to question
- `reminder` - Future action reminder
- `guidance` - Direction or decision

### Basic Template

```markdown
# {Type}: {Title}

**Date:** YYYY-MM-DD HH:MM
**From:** {Your Role}
**To:** {Recipient Role}

## Content

{Your message}

---
**{Your Role}**
```

## Folder Structure

Each role has:
- `inbox/` - Incoming messages
- `inbox-archive/` - Processed messages
- `sent/` - Sent message copies
- `outbox/` - Drafts awaiting delivery

---

## Related Skills

- **email** - Read and manage your inbox messages
- **projects** - Query project status (often referenced in communications)
