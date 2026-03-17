---
name: sendgrid
description: Sends transactional and marketing emails with SendGrid API. Use when integrating email delivery in Node.js applications with templates, analytics, and high deliverability.
---

# SendGrid Email API

Email delivery platform with high deliverability, templates, and analytics. Part of Twilio.

## Quick Start

```bash
npm install @sendgrid/mail
```

### Setup

```javascript
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY);
```

### Send Basic Email

```javascript
const msg = {
  to: 'recipient@example.com',
  from: 'sender@example.com',  // Must be verified sender
  subject: 'Hello from SendGrid',
  text: 'Plain text content',
  html: '<strong>HTML content</strong>',
};

await sgMail.send(msg);
```

## Email Options

### Full Message Object

```javascript
const msg = {
  // Recipients
  to: 'single@example.com',
  // Or multiple
  to: ['one@example.com', 'two@example.com'],
  // Or with names
  to: [
    { email: 'one@example.com', name: 'User One' },
    { email: 'two@example.com', name: 'User Two' },
  ],

  // Sender
  from: {
    email: 'sender@example.com',
    name: 'My App',
  },

  // Reply-to (optional)
  replyTo: 'support@example.com',

  // Subject
  subject: 'Your order has shipped',

  // Content
  text: 'Plain text version',
  html: '<h1>HTML version</h1>',

  // CC and BCC
  cc: 'cc@example.com',
  bcc: 'bcc@example.com',

  // Categories for analytics
  categories: ['transactional', 'order-confirmation'],

  // Custom headers
  headers: {
    'X-Custom-Header': 'value',
  },

  // Send at specific time
  sendAt: Math.floor(Date.now() / 1000) + 3600,  // 1 hour from now

  // Attachments
  attachments: [
    {
      content: base64EncodedContent,
      filename: 'invoice.pdf',
      type: 'application/pdf',
      disposition: 'attachment',
    },
  ],
};

await sgMail.send(msg);
```

## Dynamic Templates

Create templates in SendGrid dashboard with handlebars syntax.

```javascript
const msg = {
  to: 'recipient@example.com',
  from: 'sender@example.com',
  templateId: 'd-xxxxxxxxxxxxxxxxxxxxxxxx',
  dynamicTemplateData: {
    name: 'John',
    orderNumber: '12345',
    items: [
      { name: 'Product 1', price: 29.99 },
      { name: 'Product 2', price: 49.99 },
    ],
    total: 79.98,
  },
};

await sgMail.send(msg);
```

### Template Variables

In your SendGrid template:

```handlebars
<h1>Hello {{name}}!</h1>

<p>Your order #{{orderNumber}} has shipped.</p>

<table>
  {{#each items}}
  <tr>
    <td>{{this.name}}</td>
    <td>${{this.price}}</td>
  </tr>
  {{/each}}
  <tr>
    <td><strong>Total</strong></td>
    <td><strong>${{total}}</strong></td>
  </tr>
</table>
```

## Multiple Recipients

### Same Email to Multiple

```javascript
const msg = {
  to: ['user1@example.com', 'user2@example.com'],
  from: 'sender@example.com',
  subject: 'Newsletter',
  html: '<p>Content for all</p>',
};

await sgMail.send(msg);
```

### Personalized Emails (sendMultiple)

```javascript
const msgs = [
  {
    to: 'user1@example.com',
    from: 'sender@example.com',
    subject: 'Hello User 1',
    html: '<p>Content for User 1</p>',
  },
  {
    to: 'user2@example.com',
    from: 'sender@example.com',
    subject: 'Hello User 2',
    html: '<p>Content for User 2</p>',
  },
];

await sgMail.send(msgs);  // Sends in batch
```

### Personalizations (Most Efficient)

```javascript
const msg = {
  from: 'sender@example.com',
  subject: 'Order Update',
  templateId: 'd-xxxxxx',
  personalizations: [
    {
      to: 'user1@example.com',
      dynamicTemplateData: {
        name: 'Alice',
        orderNumber: '001',
      },
    },
    {
      to: 'user2@example.com',
      dynamicTemplateData: {
        name: 'Bob',
        orderNumber: '002',
      },
    },
  ],
};

await sgMail.send(msg);
```

## Attachments

```javascript
import fs from 'fs';

const msg = {
  to: 'recipient@example.com',
  from: 'sender@example.com',
  subject: 'Your invoice',
  html: '<p>Please find your invoice attached.</p>',
  attachments: [
    {
      content: fs.readFileSync('./invoice.pdf').toString('base64'),
      filename: 'invoice.pdf',
      type: 'application/pdf',
      disposition: 'attachment',
    },
    {
      content: fs.readFileSync('./logo.png').toString('base64'),
      filename: 'logo.png',
      type: 'image/png',
      disposition: 'inline',
      contentId: 'logo',  // Reference in HTML as <img src="cid:logo">
    },
  ],
};

await sgMail.send(msg);
```

## Error Handling

```javascript
try {
  await sgMail.send(msg);
  console.log('Email sent successfully');
} catch (error) {
  console.error('Error sending email:', error);

  if (error.response) {
    console.error('Status code:', error.code);
    console.error('Body:', error.response.body);
    console.error('Headers:', error.response.headers);
  }
}
```

### Common Errors

| Code | Description |
|------|-------------|
| 400 | Bad request (check payload) |
| 401 | Unauthorized (check API key) |
| 403 | Forbidden (sender not verified) |
| 429 | Rate limit exceeded |
| 500 | SendGrid server error |

## Webhooks (Event Tracking)

Configure in SendGrid dashboard to receive events.

```javascript
// API route to receive webhooks
export async function POST(request) {
  const events = await request.json();

  for (const event of events) {
    switch (event.event) {
      case 'delivered':
        console.log('Email delivered to:', event.email);
        break;
      case 'open':
        console.log('Email opened by:', event.email);
        break;
      case 'click':
        console.log('Link clicked:', event.url);
        break;
      case 'bounce':
        console.log('Bounced:', event.email, event.reason);
        // Remove from mailing list
        break;
      case 'spam_report':
        console.log('Spam report from:', event.email);
        // Unsubscribe user
        break;
    }
  }

  return new Response('OK');
}
```

## Full API Client

For advanced operations beyond sending.

```bash
npm install @sendgrid/client
```

```javascript
import Client from '@sendgrid/client';

const client = new Client();
client.setApiKey(process.env.SENDGRID_API_KEY);

// Get email statistics
const [response, body] = await client.request({
  method: 'GET',
  url: '/v3/stats',
  qs: {
    start_date: '2024-01-01',
    end_date: '2024-01-31',
  },
});

console.log(body);
```

## Next.js API Route

```typescript
// app/api/send-email/route.ts
import { NextResponse } from 'next/server';
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY!);

export async function POST(request: Request) {
  const { to, subject, html } = await request.json();

  try {
    await sgMail.send({
      to,
      from: process.env.SENDGRID_FROM_EMAIL!,
      subject,
      html,
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('SendGrid error:', error);
    return NextResponse.json(
      { error: 'Failed to send email' },
      { status: 500 }
    );
  }
}
```

## With React Email

```typescript
import sgMail from '@sendgrid/mail';
import { render } from '@react-email/components';
import WelcomeEmail from './emails/welcome';

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

async function sendWelcomeEmail(user) {
  const html = await render(WelcomeEmail({
    name: user.name,
    actionUrl: `https://myapp.com/onboarding`,
  }));

  await sgMail.send({
    to: user.email,
    from: 'welcome@myapp.com',
    subject: `Welcome to MyApp, ${user.name}!`,
    html,
  });
}
```

## Environment Variables

```bash
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@yourdomain.com
```

## Sender Verification

Before sending, verify your sender identity:

1. **Single Sender Verification** - Verify individual email addresses
2. **Domain Authentication** - Verify entire domain (recommended for production)

Configure in SendGrid Dashboard > Settings > Sender Authentication.

## Best Practices

1. **Verify your domain** - Improves deliverability
2. **Use templates** - Easier to maintain and update
3. **Handle bounces** - Remove invalid addresses
4. **Monitor events** - Track delivery and engagement
5. **Rate limit** - Don't exceed plan limits
6. **Use categories** - For analytics segmentation
7. **Include unsubscribe** - Required for marketing emails
