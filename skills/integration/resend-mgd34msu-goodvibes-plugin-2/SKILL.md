---
name: resend
description: Sends transactional emails with Resend including React Email templates, API integration, and Next.js setup. Use when sending emails, creating email templates, or integrating transactional email in applications.
---

# Resend

Modern email API for developers with React Email support.

## Quick Start

**Install:**
```bash
npm install resend
```

**Environment variable:**
```bash
# .env.local
RESEND_API_KEY=re_...
```

## Basic Usage

### Send Simple Email

```typescript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send({
  from: 'Acme <noreply@acme.com>',
  to: ['user@example.com'],
  subject: 'Hello World',
  html: '<p>Welcome to our app!</p>',
});
```

### API Route (Next.js App Router)

```typescript
// app/api/send/route.ts
import { Resend } from 'resend';
import { NextResponse } from 'next/server';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(req: Request) {
  const { to, subject, message } = await req.json();

  try {
    const { data, error } = await resend.emails.send({
      from: 'Acme <noreply@acme.com>',
      to: [to],
      subject,
      html: `<p>${message}</p>`,
    });

    if (error) {
      return NextResponse.json({ error }, { status: 400 });
    }

    return NextResponse.json({ data });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to send email' },
      { status: 500 }
    );
  }
}
```

## React Email Templates

### Install React Email

```bash
npm install @react-email/components
```

### Create Template

```tsx
// emails/welcome.tsx
import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Html,
  Img,
  Link,
  Preview,
  Section,
  Text,
} from '@react-email/components';

interface WelcomeEmailProps {
  username: string;
  loginUrl: string;
}

export function WelcomeEmail({ username, loginUrl }: WelcomeEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Welcome to Acme - Your account is ready!</Preview>
      <Body style={main}>
        <Container style={container}>
          <Img
            src="https://acme.com/logo.png"
            width={48}
            height={48}
            alt="Acme"
          />
          <Heading style={h1}>Welcome, {username}!</Heading>
          <Text style={text}>
            Thanks for signing up for Acme. We're excited to have you on board.
          </Text>
          <Section style={buttonContainer}>
            <Button style={button} href={loginUrl}>
              Get Started
            </Button>
          </Section>
          <Text style={footer}>
            If you didn't create an account, you can safely ignore this email.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const main = {
  backgroundColor: '#f6f9fc',
  fontFamily:
    '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Ubuntu,sans-serif',
};

const container = {
  backgroundColor: '#ffffff',
  margin: '0 auto',
  padding: '40px 20px',
  borderRadius: '5px',
  maxWidth: '465px',
};

const h1 = {
  color: '#1f2937',
  fontSize: '24px',
  fontWeight: '600',
  lineHeight: '40px',
  margin: '0 0 20px',
};

const text = {
  color: '#4b5563',
  fontSize: '14px',
  lineHeight: '24px',
  margin: '0 0 20px',
};

const buttonContainer = {
  textAlign: 'center' as const,
  margin: '30px 0',
};

const button = {
  backgroundColor: '#3b82f6',
  borderRadius: '5px',
  color: '#fff',
  fontSize: '14px',
  fontWeight: '600',
  textDecoration: 'none',
  textAlign: 'center' as const,
  display: 'inline-block',
  padding: '12px 30px',
};

const footer = {
  color: '#9ca3af',
  fontSize: '12px',
  lineHeight: '16px',
  margin: '20px 0 0',
};

export default WelcomeEmail;
```

### Send with Template

```typescript
// app/api/send-welcome/route.ts
import { Resend } from 'resend';
import { WelcomeEmail } from '@/emails/welcome';
import { NextResponse } from 'next/server';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(req: Request) {
  const { email, username } = await req.json();

  try {
    const { data, error } = await resend.emails.send({
      from: 'Acme <noreply@acme.com>',
      to: [email],
      subject: 'Welcome to Acme!',
      react: WelcomeEmail({
        username,
        loginUrl: `${process.env.NEXT_PUBLIC_APP_URL}/login`,
      }),
    });

    if (error) {
      return NextResponse.json({ error }, { status: 400 });
    }

    return NextResponse.json({ data });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to send email' },
      { status: 500 }
    );
  }
}
```

## Common Email Templates

### Password Reset

```tsx
// emails/password-reset.tsx
import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Html,
  Preview,
  Text,
} from '@react-email/components';

interface PasswordResetProps {
  resetUrl: string;
  expiresIn: string;
}

export function PasswordResetEmail({ resetUrl, expiresIn }: PasswordResetProps) {
  return (
    <Html>
      <Head />
      <Preview>Reset your password</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={h1}>Reset Your Password</Heading>
          <Text style={text}>
            We received a request to reset your password. Click the button below
            to create a new password.
          </Text>
          <Button style={button} href={resetUrl}>
            Reset Password
          </Button>
          <Text style={text}>
            This link will expire in {expiresIn}. If you didn't request a
            password reset, you can safely ignore this email.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}
```

### Order Confirmation

```tsx
// emails/order-confirmation.tsx
import {
  Body,
  Column,
  Container,
  Head,
  Heading,
  Hr,
  Html,
  Preview,
  Row,
  Section,
  Text,
} from '@react-email/components';

interface OrderItem {
  name: string;
  quantity: number;
  price: number;
}

interface OrderConfirmationProps {
  orderNumber: string;
  items: OrderItem[];
  total: number;
  shippingAddress: string;
}

export function OrderConfirmationEmail({
  orderNumber,
  items,
  total,
  shippingAddress,
}: OrderConfirmationProps) {
  return (
    <Html>
      <Head />
      <Preview>Order {orderNumber} confirmed</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={h1}>Order Confirmed</Heading>
          <Text style={text}>
            Thanks for your order! Your order number is{' '}
            <strong>{orderNumber}</strong>.
          </Text>

          <Section style={orderSection}>
            <Heading as="h2" style={h2}>
              Order Summary
            </Heading>
            {items.map((item, index) => (
              <Row key={index} style={itemRow}>
                <Column>
                  <Text style={itemName}>{item.name}</Text>
                  <Text style={itemQuantity}>Qty: {item.quantity}</Text>
                </Column>
                <Column style={priceColumn}>
                  <Text style={itemPrice}>${item.price.toFixed(2)}</Text>
                </Column>
              </Row>
            ))}
            <Hr style={hr} />
            <Row>
              <Column>
                <Text style={totalLabel}>Total</Text>
              </Column>
              <Column style={priceColumn}>
                <Text style={totalPrice}>${total.toFixed(2)}</Text>
              </Column>
            </Row>
          </Section>

          <Section>
            <Heading as="h2" style={h2}>
              Shipping Address
            </Heading>
            <Text style={text}>{shippingAddress}</Text>
          </Section>
        </Container>
      </Body>
    </Html>
  );
}
```

## Email Options

### Full Options

```typescript
const { data, error } = await resend.emails.send({
  // Required
  from: 'Acme <noreply@acme.com>',
  to: ['user@example.com'],
  subject: 'Hello',

  // Content (one of these)
  html: '<p>Hello</p>',
  text: 'Hello',
  react: EmailTemplate({ props }),

  // Optional
  cc: ['cc@example.com'],
  bcc: ['bcc@example.com'],
  replyTo: 'support@acme.com',
  headers: {
    'X-Custom-Header': 'value',
  },
  attachments: [
    {
      filename: 'invoice.pdf',
      content: Buffer.from(pdfContent),
    },
  ],
  tags: [
    { name: 'category', value: 'transactional' },
  ],
});
```

### Multiple Recipients

```typescript
// To multiple addresses
await resend.emails.send({
  from: 'Acme <noreply@acme.com>',
  to: ['user1@example.com', 'user2@example.com'],
  subject: 'Team Update',
  html: '<p>Hello team!</p>',
});

// Batch send (different emails)
const { data, error } = await resend.batch.send([
  {
    from: 'Acme <noreply@acme.com>',
    to: ['user1@example.com'],
    subject: 'Welcome User 1',
    html: '<p>Hello User 1!</p>',
  },
  {
    from: 'Acme <noreply@acme.com>',
    to: ['user2@example.com'],
    subject: 'Welcome User 2',
    html: '<p>Hello User 2!</p>',
  },
]);
```

## Attachments

```typescript
import { readFileSync } from 'fs';

// From file
const attachment = readFileSync('./invoice.pdf');

await resend.emails.send({
  from: 'Acme <noreply@acme.com>',
  to: ['user@example.com'],
  subject: 'Your Invoice',
  html: '<p>Please find your invoice attached.</p>',
  attachments: [
    {
      filename: 'invoice.pdf',
      content: attachment,
    },
  ],
});

// From URL
await resend.emails.send({
  from: 'Acme <noreply@acme.com>',
  to: ['user@example.com'],
  subject: 'Your Report',
  html: '<p>Please find your report attached.</p>',
  attachments: [
    {
      filename: 'report.pdf',
      path: 'https://example.com/reports/report.pdf',
    },
  ],
});
```

## Preview Emails

### Development Server

```bash
npm install react-email -D
```

```json
{
  "scripts": {
    "email": "email dev --dir emails"
  }
}
```

```bash
npm run email
```

Opens at `http://localhost:3000` to preview templates.

## Server Actions

```typescript
// app/actions/email.ts
'use server';

import { Resend } from 'resend';
import { WelcomeEmail } from '@/emails/welcome';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function sendWelcomeEmail(email: string, username: string) {
  try {
    const { data, error } = await resend.emails.send({
      from: 'Acme <noreply@acme.com>',
      to: [email],
      subject: 'Welcome to Acme!',
      react: WelcomeEmail({ username, loginUrl: '/login' }),
    });

    if (error) {
      return { success: false, error: error.message };
    }

    return { success: true, messageId: data?.id };
  } catch (error) {
    return { success: false, error: 'Failed to send email' };
  }
}
```

## Webhooks

```typescript
// app/api/webhooks/resend/route.ts
import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  const payload = await req.json();

  switch (payload.type) {
    case 'email.sent':
      console.log('Email sent:', payload.data.email_id);
      break;
    case 'email.delivered':
      console.log('Email delivered:', payload.data.email_id);
      break;
    case 'email.bounced':
      console.log('Email bounced:', payload.data.email_id);
      // Handle bounce - update user record
      break;
    case 'email.complained':
      console.log('Spam complaint:', payload.data.email_id);
      // Handle complaint - unsubscribe user
      break;
  }

  return NextResponse.json({ received: true });
}
```

## Best Practices

1. **Use React Email** - Type-safe, reusable templates
2. **Verify domain** - Better deliverability
3. **Handle errors** - Check for error response
4. **Use batch for bulk** - More efficient
5. **Preview before sending** - Use email dev server

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Unverified domain | Verify in Resend dashboard |
| Missing from address | Use verified domain email |
| Not handling errors | Check error response |
| Inline styles missing | Use style objects in React Email |
| Large attachments | Keep under 40MB |

## Reference Files

- [references/templates.md](references/templates.md) - More template examples
- [references/webhooks.md](references/webhooks.md) - Webhook events
- [references/domains.md](references/domains.md) - Domain verification
