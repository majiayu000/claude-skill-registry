---
name: email-processing
description: Handles Gmail integration, email parsing, drafting, and sending workflows. Use when processing emails, composing responses, managing email threads, or integrating with Gmail API.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Email Processing Skill

This skill provides comprehensive email handling capabilities for the Personal AI Employee, including Gmail API integration, email parsing, and response drafting.

## Capabilities

1. **Email Parsing** - Extract and structure email content
2. **Response Drafting** - Generate contextual email responses
3. **Thread Management** - Handle email conversations
4. **Gmail API Integration** - Connect with Gmail for send/receive

## Email File Format

Emails captured by watchers follow this format:

```markdown
---
type: email
from: sender@example.com
to: recipient@example.com
subject: Email Subject Line
received: 2026-01-07T10:30:00Z
message_id: abc123
thread_id: thread_xyz
priority: high
status: pending
---

## Email Content
[Body of the email]

## Attachments
- filename.pdf (150KB)

## Suggested Actions
- [ ] Reply to sender
- [ ] Forward to relevant party
- [ ] Archive after processing
```

## Response Templates

### Professional Reply
```markdown
Dear [Name],

Thank you for your email regarding [subject].

[Body of response]

Best regards,
[Signature]
```

### Invoice Response
```markdown
Dear [Name],

Please find attached the invoice for [description].

Invoice Details:
- Invoice #: [number]
- Amount: $[amount]
- Due Date: [date]

Payment can be made via [payment methods].

Best regards,
[Signature]
```

## Integration

- Works with Gmail MCP server for sending
- Coordinates with approval-workflow for HITL
- Updates vault-management for file operations

## Reference

For detailed API documentation, see [reference.md](reference.md)

For usage examples, see [examples.md](examples.md)
