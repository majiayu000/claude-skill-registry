---
name: nodemailer
description: Sends emails from Node.js applications using SMTP or other transports with Nodemailer. Use when implementing email functionality with full control over transport configuration.
---

# Nodemailer

Node.js email sending library. Works with SMTP, Amazon SES, and other transports. Zero dependencies, full Unicode support.

## Quick Start

```bash
npm install nodemailer
```

### Basic SMTP Setup

```javascript
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: 'smtp.example.com',
  port: 587,
  secure: false,  // true for 465, false for 587
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

// Send email
await transporter.sendMail({
  from: '"My App" <noreply@example.com>',
  to: 'user@example.com',
  subject: 'Hello',
  text: 'Plain text content',
  html: '<b>HTML content</b>',
});
```

## Transport Configuration

### Gmail

```javascript
// Use App Password (not regular password)
// Enable 2FA, then generate App Password in Google Account settings

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'your-email@gmail.com',
    pass: 'your-app-password',  // 16-character app password
  },
});
```

### Gmail with OAuth2

```javascript
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    type: 'OAuth2',
    user: 'your-email@gmail.com',
    clientId: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    refreshToken: process.env.GOOGLE_REFRESH_TOKEN,
  },
});
```

### Outlook/Office365

```javascript
const transporter = nodemailer.createTransport({
  host: 'smtp.office365.com',
  port: 587,
  secure: false,
  auth: {
    user: 'your-email@outlook.com',
    pass: 'your-password',
  },
});
```

### Amazon SES

```javascript
import { SES } from '@aws-sdk/client-ses';

const transporter = nodemailer.createTransport({
  SES: {
    ses: new SES({
      region: 'us-east-1',
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
      },
    }),
    aws: { SendRawEmailCommand },
  },
});
```

### Resend SMTP

```javascript
const transporter = nodemailer.createTransport({
  host: 'smtp.resend.com',
  port: 465,
  secure: true,
  auth: {
    user: 'resend',
    pass: process.env.RESEND_API_KEY,
  },
});
```

### SendGrid SMTP

```javascript
const transporter = nodemailer.createTransport({
  host: 'smtp.sendgrid.net',
  port: 587,
  secure: false,
  auth: {
    user: 'apikey',
    pass: process.env.SENDGRID_API_KEY,
  },
});
```

## Message Options

```javascript
const message = {
  // Sender
  from: '"Sender Name" <sender@example.com>',

  // Recipients
  to: 'recipient@example.com',
  // Or multiple
  to: 'one@example.com, two@example.com',
  // Or with names
  to: '"User One" <one@example.com>, "User Two" <two@example.com>',

  // CC and BCC
  cc: 'cc@example.com',
  bcc: 'bcc@example.com',

  // Reply-to
  replyTo: 'reply@example.com',

  // Subject
  subject: 'Hello World',

  // Content
  text: 'Plain text body',
  html: '<h1>HTML body</h1>',

  // Priority
  priority: 'high',  // 'high', 'normal', 'low'

  // Custom headers
  headers: {
    'X-Custom-Header': 'value',
  },

  // Message-ID
  messageId: '<unique-id@example.com>',

  // References (for threading)
  references: '<previous-message-id@example.com>',
  inReplyTo: '<previous-message-id@example.com>',
};

await transporter.sendMail(message);
```

## Attachments

```javascript
const message = {
  from: 'sender@example.com',
  to: 'recipient@example.com',
  subject: 'With attachments',
  text: 'See attachments',
  attachments: [
    // From file
    {
      filename: 'document.pdf',
      path: './files/document.pdf',
    },
    // From buffer
    {
      filename: 'data.json',
      content: Buffer.from(JSON.stringify({ hello: 'world' })),
    },
    // From string
    {
      filename: 'text.txt',
      content: 'Hello World',
    },
    // From URL
    {
      filename: 'image.png',
      path: 'https://example.com/image.png',
    },
    // Embedded image (for HTML)
    {
      filename: 'logo.png',
      path: './logo.png',
      cid: 'logo@myapp',  // Reference in HTML as <img src="cid:logo@myapp">
    },
  ],
};

await transporter.sendMail(message);
```

### Embedded Images

```javascript
const message = {
  from: 'sender@example.com',
  to: 'recipient@example.com',
  subject: 'With embedded image',
  html: `
    <h1>Hello</h1>
    <img src="cid:logo@myapp" alt="Logo" />
  `,
  attachments: [
    {
      filename: 'logo.png',
      path: './logo.png',
      cid: 'logo@myapp',
    },
  ],
};
```

## Verify Connection

Test configuration before sending.

```javascript
try {
  await transporter.verify();
  console.log('SMTP connection successful');
} catch (error) {
  console.error('SMTP connection failed:', error);
}
```

## Error Handling

```javascript
try {
  const info = await transporter.sendMail(message);
  console.log('Message sent:', info.messageId);
} catch (error) {
  if (error.responseCode === 550) {
    console.error('Recipient rejected');
  } else if (error.code === 'ECONNECTION') {
    console.error('Connection failed');
  } else if (error.code === 'EAUTH') {
    console.error('Authentication failed');
  } else {
    console.error('Error:', error.message);
  }
}
```

## Pooled Connections

For high-volume sending, reuse connections.

```javascript
const transporter = nodemailer.createTransport({
  pool: true,
  host: 'smtp.example.com',
  port: 587,
  secure: false,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
  maxConnections: 5,
  maxMessages: 100,
});

// Close pool when done
transporter.close();
```

## With React Email

```javascript
import nodemailer from 'nodemailer';
import { render } from '@react-email/components';
import WelcomeEmail from './emails/welcome';

const transporter = nodemailer.createTransport({
  host: 'smtp.example.com',
  port: 587,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

async function sendWelcomeEmail(user) {
  const html = await render(WelcomeEmail({
    name: user.name,
    actionUrl: 'https://myapp.com/start',
  }));

  await transporter.sendMail({
    from: '"MyApp" <hello@myapp.com>',
    to: user.email,
    subject: `Welcome, ${user.name}!`,
    html,
  });
}
```

## Next.js API Route

```typescript
// app/api/contact/route.ts
import { NextResponse } from 'next/server';
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT || '587'),
  secure: false,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

export async function POST(request: Request) {
  const { name, email, message } = await request.json();

  try {
    await transporter.sendMail({
      from: process.env.SMTP_FROM,
      to: process.env.CONTACT_EMAIL,
      replyTo: email,
      subject: `Contact form: ${name}`,
      text: `From: ${name} <${email}>\n\n${message}`,
      html: `
        <p><strong>From:</strong> ${name} &lt;${email}&gt;</p>
        <p>${message.replace(/\n/g, '<br>')}</p>
      `,
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Email error:', error);
    return NextResponse.json(
      { error: 'Failed to send email' },
      { status: 500 }
    );
  }
}
```

## Testing with Ethereal

Free fake SMTP for testing - no emails actually sent.

```javascript
// Create test account
const testAccount = await nodemailer.createTestAccount();

const transporter = nodemailer.createTransport({
  host: 'smtp.ethereal.email',
  port: 587,
  secure: false,
  auth: {
    user: testAccount.user,
    pass: testAccount.pass,
  },
});

const info = await transporter.sendMail({
  from: 'test@example.com',
  to: 'recipient@example.com',
  subject: 'Test',
  text: 'Test email',
});

// Preview URL
console.log('Preview:', nodemailer.getTestMessageUrl(info));
```

## Environment Variables

```bash
# SMTP Configuration
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-username
SMTP_PASS=your-password
SMTP_FROM="My App" <noreply@example.com>

# Or for Gmail
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
```

## Common Transports

| Provider | Host | Port | Secure |
|----------|------|------|--------|
| Gmail | smtp.gmail.com | 465 | true |
| Outlook | smtp.office365.com | 587 | false |
| Yahoo | smtp.mail.yahoo.com | 465 | true |
| SendGrid | smtp.sendgrid.net | 587 | false |
| Mailgun | smtp.mailgun.org | 587 | false |
| Amazon SES | email-smtp.{region}.amazonaws.com | 465 | true |

## Best Practices

1. **Use environment variables** - Never hardcode credentials
2. **Verify connection** - Test before sending in production
3. **Use pooling** - For high-volume sending
4. **Handle errors** - Implement proper error handling
5. **Use OAuth2** - More secure than passwords for Gmail
6. **Test with Ethereal** - Free testing without sending real emails
7. **Set proper From** - Use verified sender addresses
