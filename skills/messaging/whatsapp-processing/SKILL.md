---
name: whatsapp-processing
description: Handles WhatsApp message processing, response drafting, and conversation management. Use when working with WhatsApp messages, drafting responses, or managing WhatsApp communication workflows.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# WhatsApp Processing Skill

This skill provides WhatsApp message handling capabilities for the Personal AI Employee, including message parsing, response drafting, and conversation management.

## Message Types

| Type | Keywords | Priority | Auto-Response |
|------|----------|----------|---------------|
| Urgent | urgent, asap, emergency | Critical | No |
| Business | invoice, payment, quote | High | No |
| Scheduling | meeting, call, available | Medium | Partial |
| General | - | Low | Yes (greetings) |

## Message Format

```markdown
---
type: whatsapp
from: Contact Name
received: 2026-01-07T10:30:00Z
priority: high
keywords: [invoice, payment]
status: pending
---

## Message Content
[Message text]

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Mark as handled
```

## Response Guidelines

- Keep messages concise (WhatsApp style)
- Match sender's formality level
- Use appropriate emoji sparingly
- Respond in sender's language when possible

## Business Hours

- During hours: Normal response
- After hours: Acknowledge + set expectations
- Weekends: Auto-response if configured

## Reference

For detailed patterns, see [reference.md](reference.md)

For examples, see [examples.md](examples.md)
