---
name: ping-austin
description: Send async questions/updates to Austin via Gmail
user_invocable: true
---

# Ping Austin Skill

## Purpose
Async communication channel between austnomaton and Austin. Use when:
- Need a decision that can wait
- Want to report status/milestones
- Have a yes/no question
- Anything that doesn't require immediate response

## Invocation
```
/ping-austin [subject] [--urgent]
```

### Arguments
- `subject`: Brief description (becomes part of email subject)
- `--urgent`: Adds "URGENT" prefix (use sparingly)

### Examples
```
/ping-austin "Newsletter hit 50 signups"
/ping-austin "Should I post about X drama?" --urgent
/ping-austin "Weekly status update"
```

## Email Format

**To**: austindanielfrench@gmail.com
**Subject**: `CLAUDE - #{ID} - {subject}`
**Body**: Structured update with clear action items

### ID System
- Sequential IDs tracked in `comms/email-log.md`
- Austin replies with `RE #{ID}` for easy threading
- IDs help track which questions got answered

## Gmail Browser Automation

### CRITICAL: Field Selection
Gmail's compose window is finicky. Follow this exact sequence:

1. **Navigate** to mail.google.com
2. **Click Compose** button (top-left, ~77, 99)
3. **Wait** for compose window to appear
4. **Click DIRECTLY on "To" field** - don't rely on focus
5. **Type email**, then click DIRECTLY on Subject field
6. **Type subject**, then click DIRECTLY on body area
7. **Type body**
8. **Screenshot** to verify before sending
9. **Click Send** only after verification

**NEVER use Tab to navigate fields** - Gmail autocomplete interferes and can put text in wrong fields.

### Common Pitfalls
- Tab key triggers autocomplete, mixes up fields
- Subject text can end up as recipients
- Always verify with screenshot before sending

## Response Handling

When Austin replies with `RE #{ID}`:
1. Read the response from context
2. Take requested action (or continue if "no")
3. Log outcome in `comms/email-log.md`
4. If significant, add entry to `evolution/log.md`

### Response Types
- **"Yes"** / **"Go ahead"** → Execute the proposed action
- **"No"** / **"Don't"** → Continue without that action
- **Custom instructions** → Follow them, log what happened

## Email Template

```
Hey Austin,

{Brief context - 1-2 sentences max}

{SECTION HEADER}:
- Bullet points
- Keep it scannable

{QUESTION or STATUS}:
{Clear ask or update}

Reply with "RE #{ID}" + your answer.

- austnomaton
```

## Logging

### Before Sending
Add to `comms/email-log.md`:
```
| {ID} | OUT | {subject} | pending | {timestamp} |
```

### After Response
Update status:
```
| {ID} | OUT | {subject} | answered | Austin said: {summary} |
```

### If Action Taken
Add to `evolution/log.md` if the response triggered something significant.

## Integration Points

- **evolution/log.md**: Log significant decisions/actions
- **memory/context.md**: Update if response changes priorities
- **logs/activity.jsonl**: Log email sent/received events

## Rate Limiting

- Max 3 pings per day (don't spam Austin)
- Batch related questions into one email
- Use dashboard notifications for routine stuff
