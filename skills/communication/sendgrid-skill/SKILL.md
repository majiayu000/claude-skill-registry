---
name: sendgrid
slug: sendgrid-integration
version: 1.0.0
category: integration
description: SendGrid email integration with templates and transactional email support
triggers:
  - pattern: "sendgrid|email|send email|transactional|notification"
    confidence: 0.8
    examples:
      - "send email with SendGrid"
      - "setup email notifications"
      - "create email templates"
      - "integrate transactional emails"
      - "send welcome email"
mcp_dependencies:
  - server: sendgrid
    required: false
    capabilities:
      - "send"
      - "templates"
---

# SendGrid Integration Skill

Complete SendGrid email integration template with email client setup, reusable templates, and transactional email functionality.

## Overview

This template includes:
- **SendGrid Client Setup** - Server-side SendGrid SDK configuration
- **Email Templates** - Pre-built welcome and notification templates
- **Type Safety** - Full TypeScript support
- **Error Handling** - Comprehensive email delivery tracking
- **Template System** - Reusable HTML email templates

## When to Use This Template

Use this template when you need:
- Transactional email sending
- Welcome email flows
- Notification emails
- Password reset emails
- Email verification
- Custom email templates

## What's Included

### Code Files

- `code/client.ts` - SendGrid SDK setup and email utilities
- `code/templates/welcome.ts` - Welcome email template
- `code/templates/notification.ts` - Notification email template

### Configuration

- `mcp/config.json` - MCP server configuration for SendGrid
- `env/.env.template` - Required environment variables

### Documentation

- `docs/README.md` - Complete setup and usage guide

## Quick Start

1. **Install Dependencies**
   ```bash
   npm install @sendgrid/mail
   ```

2. **Configure Environment Variables**
   ```bash
   cp templates/sendgrid/env/.env.template .env.local
   # Add your SendGrid API key
   ```

3. **Copy Template Files**
   ```bash
   npx tsx scripts/load-template.ts sendgrid
   ```

4. **Verify Sender Email**
   - Go to SendGrid Dashboard
   - Add and verify sender email address

## Key Features

### 1. Send Transactional Emails

```typescript
import { sendEmail } from '@/lib/sendgrid/client'

await sendEmail({
  to: 'user@example.com',
  subject: 'Welcome to our app!',
  text: 'Thanks for signing up.',
  html: '<strong>Thanks for signing up!</strong>',
})
```

### 2. Use Email Templates

```typescript
import { sendWelcomeEmail } from '@/lib/sendgrid/templates/welcome'

await sendWelcomeEmail({
  to: 'user@example.com',
  name: 'John Doe',
  loginUrl: 'https://app.example.com/login',
})
```

### 3. Send Notifications

```typescript
import { sendNotificationEmail } from '@/lib/sendgrid/templates/notification'

await sendNotificationEmail({
  to: 'user@example.com',
  title: 'New Message',
  message: 'You have received a new message.',
  actionUrl: 'https://app.example.com/messages',
  actionText: 'View Message',
})
```

### 4. Batch Email Sending

```typescript
import { sendBulkEmail } from '@/lib/sendgrid/client'

await sendBulkEmail({
  to: ['user1@example.com', 'user2@example.com'],
  subject: 'Newsletter',
  html: '<p>Monthly newsletter content</p>',
})
```

## Email Templates

### Welcome Email

Professional welcome email with call-to-action button.

### Notification Email

Generic notification template for alerts and updates.

### Custom Templates

Create custom templates following the same pattern:

```typescript
export async function sendCustomEmail(params: {
  to: string
  // ... custom params
}) {
  return sendEmail({
    to: params.to,
    subject: 'Custom Subject',
    html: generateHtmlTemplate(params),
  })
}
```

## Security Best Practices

- Never expose API keys client-side
- Validate recipient email addresses
- Implement rate limiting
- Use unsubscribe links
- Handle bounces and spam reports

## Testing

### Test Mode

SendGrid provides a sandbox mode for testing:

```typescript
const client = sendgrid()
client.setApiKey(process.env.SENDGRID_API_KEY!)
client.setSandboxMode(true) // Enable sandbox
```

### Email Validation

Always validate emails before sending:

```typescript
import { isValidEmail } from '@/lib/sendgrid/utils'

if (!isValidEmail(email)) {
  throw new Error('Invalid email address')
}
```

## Resources

- [SendGrid Documentation](https://docs.sendgrid.com)
- [SendGrid Dashboard](https://app.sendgrid.com)
- [Email Best Practices](https://sendgrid.com/resource/email-marketing-best-practices/)

---

**Template Version:** 1.0.0
**Last Updated:** 2026-01-04
**Maintainer:** Turbocat Agent System
