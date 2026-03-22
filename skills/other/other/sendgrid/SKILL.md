---
name: sendgrid
description: >-
  Send transactional and marketing emails with SendGrid. Use when a user asks
  to send emails programmatically, set up transactional email delivery, send
  bulk marketing emails, manage email templates, track email opens and clicks,
  set up email authentication (SPF/DKIM/DMARC), handle bounces and
  unsubscribes, or build email infrastructure. Covers single and bulk sending,
  dynamic templates, email validation, webhooks, and deliverability setup.
license: Apache-2.0
compatibility: 'Node.js 12+, Python 3.6+, any HTTP client'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
    - sendgrid
    - email
    - transactional
    - marketing
    - smtp
    - delivery
---

# SendGrid

## Overview

SendGrid (by Twilio) is the most widely-used transactional email service. It handles email delivery at scale — from single welcome emails to millions of marketing messages. This skill covers sending emails via API and SMTP, dynamic templates, bulk/batch sending, event webhooks (opens, clicks, bounces), email validation, and deliverability configuration (SPF, DKIM, domain authentication).

## Instructions

### Step 1: Setup

```bash
# Node.js
npm install @sendgrid/mail

# Python
pip install sendgrid
```

```typescript
// lib/email.ts — SendGrid client setup
import sgMail from '@sendgrid/mail'

sgMail.setApiKey(process.env.SENDGRID_API_KEY!)
```

### Step 2: Send Single Email

```typescript
// send-email.ts — Send a transactional email
import sgMail from '@sendgrid/mail'

sgMail.setApiKey(process.env.SENDGRID_API_KEY!)

// Simple text/HTML email
await sgMail.send({
  to: 'recipient@example.com',
  from: { email: 'noreply@myapp.com', name: 'My App' },
  subject: 'Welcome to My App',
  text: 'Thanks for signing up!',
  html: '<h1>Welcome!</h1><p>Thanks for signing up.</p>',
})

// With dynamic template (recommended for production)
await sgMail.send({
  to: 'recipient@example.com',
  from: { email: 'noreply@myapp.com', name: 'My App' },
  templateId: 'd-abc123def456',    // template ID from SendGrid dashboard
  dynamicTemplateData: {
    name: 'Alex',
    action_url: 'https://myapp.com/verify?token=xyz',
    company_name: 'My App',
  },
})
```

### Step 3: Bulk Sending

```typescript
// bulk-send.ts — Send to multiple recipients efficiently
// sendMultiple sends individual emails (each recipient only sees their own address)

await sgMail.sendMultiple({
  to: ['user1@example.com', 'user2@example.com', 'user3@example.com'],
  from: { email: 'noreply@myapp.com', name: 'My App' },
  templateId: 'd-abc123def456',
  dynamicTemplateData: { announcement: 'New feature launched!' },
})

// Personalized bulk send (different data per recipient)
const messages = users.map(user => ({
  to: user.email,
  from: { email: 'noreply@myapp.com', name: 'My App' },
  templateId: 'd-abc123def456',
  dynamicTemplateData: {
    name: user.name,
    plan: user.plan,
    usage: user.monthlyUsage,
  },
}))

// Send in batches of 1000 (SendGrid limit per API call)
for (let i = 0; i < messages.length; i += 1000) {
  await sgMail.send(messages.slice(i, i + 1000))
}
```

### Step 4: Event Webhooks

```typescript
// app/api/webhooks/sendgrid/route.ts — Process email events
// SendGrid posts events when emails are delivered, opened, clicked, bounced, etc.

import { NextRequest, NextResponse } from 'next/server'

type SendGridEvent = {
  email: string
  event: 'delivered' | 'open' | 'click' | 'bounce' | 'dropped' | 'spamreport' | 'unsubscribe'
  timestamp: number
  sg_message_id: string
  url?: string           // for click events
  reason?: string        // for bounce/drop events
}

export async function POST(req: NextRequest) {
  const events: SendGridEvent[] = await req.json()

  for (const event of events) {
    switch (event.event) {
      case 'bounce':
        // Mark email as invalid in your database
        await db.users.update({ email: event.email }, { emailBounced: true })
        break
      case 'spamreport':
      case 'unsubscribe':
        // Respect opt-out immediately
        await db.users.update({ email: event.email }, { emailOptOut: true })
        break
      case 'open':
        await db.emailEvents.create({ type: 'open', email: event.email, messageId: event.sg_message_id })
        break
      case 'click':
        await db.emailEvents.create({ type: 'click', email: event.email, url: event.url })
        break
    }
  }

  return NextResponse.json({ received: true })
}
```

### Step 5: Domain Authentication

```bash
# Set up domain authentication for deliverability
# In SendGrid dashboard: Settings → Sender Authentication → Domain Authentication
# This adds DNS records for your domain:

# SPF — tells receiving servers that SendGrid can send on your behalf
# Type: CNAME, Host: em1234.yourdomain.com → u1234.wl.sendgrid.net

# DKIM — cryptographic signature proving email integrity
# Type: CNAME, Host: s1._domainkey.yourdomain.com → s1.domainkey.u1234.wl.sendgrid.net
# Type: CNAME, Host: s2._domainkey.yourdomain.com → s2.domainkey.u1234.wl.sendgrid.net

# After adding DNS records, verify in SendGrid dashboard
# Deliverability improves significantly with proper authentication
```

## Examples

### Example 1: Set up transactional email for a SaaS app
**User prompt:** "I need to send welcome emails, password resets, and invoice receipts. Set up SendGrid with templates and track delivery."

The agent will:
1. Configure SendGrid with domain authentication.
2. Create dynamic templates for each email type in the dashboard.
3. Build a reusable email service module with template-based sending.
4. Set up event webhooks to track delivery, bounces, and opt-outs.
5. Add bounce handling to prevent sending to invalid addresses.

## Guidelines

- Always use dynamic templates instead of inline HTML — they're version-controlled in SendGrid, support A/B testing, and non-engineers can edit them.
- Set up domain authentication (SPF + DKIM) before sending production emails. Without it, your emails will land in spam.
- Handle bounces and unsubscribes immediately via webhooks — continuing to send to bounced addresses damages your sender reputation.
- Use `sendMultiple` (not `send` with multiple `to` addresses) for bulk emails — it sends individual messages so recipients don't see each other's addresses.
- SendGrid's free tier includes 100 emails/day. For production, the Essentials plan starts at $20/month for 50K emails.
- Always include an unsubscribe link in marketing emails — it's required by CAN-SPAM law and improves deliverability.
