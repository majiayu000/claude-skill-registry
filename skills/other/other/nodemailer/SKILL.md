---
name: nodemailer
description: 从Node.js应用发送邮件。最流行的邮件发送模块，支持SMTP、OAuth2、附件和HTML模板。
metadata:
  short-description: Node.js邮件发送
source:
  repository: https://github.com/nodemailer/nodemailer
  license: MIT
  stars: 17k+
---

# Nodemailer Tool

## Description
Send emails from Node.js with SMTP, OAuth2, attachments, and HTML templates.

## Source
- Repository: [nodemailer/nodemailer](https://github.com/nodemailer/nodemailer)
- License: MIT

## Installation

```bash
npm install nodemailer
```

## Usage Examples

### Basic Email

```typescript
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  host: 'smtp.gmail.com',
  port: 587,
  secure: false,
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS,
  },
});

async function sendEmail() {
  const info = await transporter.sendMail({
    from: '"My App" <noreply@myapp.com>',
    to: 'user@example.com',
    subject: 'Welcome to My App',
    text: 'Hello, welcome to our platform!',
    html: '<h1>Hello</h1><p>Welcome to our platform!</p>',
  });
  
  console.log('Message sent:', info.messageId);
}
```

### HTML Email with Template

```typescript
async function sendWelcomeEmail(user: { name: string; email: string }) {
  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <style>
          .container { max-width: 600px; margin: 0 auto; font-family: Arial; }
          .header { background: #4F46E5; color: white; padding: 20px; }
          .content { padding: 20px; }
          .button { background: #4F46E5; color: white; padding: 12px 24px; 
                    text-decoration: none; border-radius: 4px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>Welcome, ${user.name}!</h1>
          </div>
          <div class="content">
            <p>Thank you for joining our platform.</p>
            <a href="https://myapp.com/dashboard" class="button">Get Started</a>
          </div>
        </div>
      </body>
    </html>
  `;
  
  await transporter.sendMail({
    from: '"My App" <noreply@myapp.com>',
    to: user.email,
    subject: `Welcome, ${user.name}!`,
    html,
  });
}
```

### Email with Attachments

```typescript
async function sendEmailWithAttachment() {
  await transporter.sendMail({
    from: '"Reports" <reports@myapp.com>',
    to: 'manager@company.com',
    subject: 'Monthly Report',
    text: 'Please find the monthly report attached.',
    attachments: [
      {
        filename: 'report.pdf',
        path: './reports/monthly-report.pdf',
      },
      {
        filename: 'data.xlsx',
        content: Buffer.from('...'), // Buffer content
      },
      {
        filename: 'logo.png',
        path: './assets/logo.png',
        cid: 'logo@myapp', // For embedding in HTML
      },
    ],
    html: '<img src="cid:logo@myapp" /><p>See attached report.</p>',
  });
}
```

### OAuth2 Authentication (Gmail)

```typescript
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    type: 'OAuth2',
    user: process.env.GMAIL_USER,
    clientId: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    refreshToken: process.env.GOOGLE_REFRESH_TOKEN,
  },
});
```

### Email Queue with Rate Limiting

```typescript
class EmailQueue {
  private queue: Array<() => Promise<void>> = [];
  private processing = false;
  
  async add(emailFn: () => Promise<void>) {
    this.queue.push(emailFn);
    this.process();
  }
  
  private async process() {
    if (this.processing) return;
    this.processing = true;
    
    while (this.queue.length > 0) {
      const emailFn = this.queue.shift()!;
      await emailFn();
      await new Promise(r => setTimeout(r, 1000)); // Rate limit
    }
    
    this.processing = false;
  }
}
```

## Tags
`email`, `smtp`, `notification`, `communication`, `automation`

## Compatibility
- Codex: ✅
- Claude Code: ✅
