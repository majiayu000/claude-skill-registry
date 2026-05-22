---
name: email-notifications
description: Expert guide for sending transactional emails, creating templates, scheduling notifications, and email best practices. Use when implementing email functionality, notifications, or campaigns.
---

# Email Notifications Skill

## Overview

This skill helps you implement email notifications in your Next.js application. From transactional emails to scheduled campaigns, this covers everything you need for reliable email delivery.

## Email Providers

### Resend (Recommended for Next.js)

**Install:**
```bash
npm install resend
```

**Setup:**
```typescript
// lib/email.ts
import { Resend } from 'resend'

export const resend = new Resend(process.env.RESEND_API_KEY)
```

**Send Email:**
```typescript
// app/api/email/send/route.ts
import { resend } from '@/lib/email'

export async function POST(request: Request) {
  const { to, subject, html } = await request.json()

  try {
    const { data, error } = await resend.emails.send({
      from: 'noreply@yourdomain.com',
      to,
      subject,
      html,
    })

    if (error) {
      return Response.json({ error }, { status: 400 })
    }

    return Response.json({ data })
  } catch (error) {
    return Response.json({ error }, { status: 500 })
  }
}
```

### SendGrid

**Install:**
```bash
npm install @sendgrid/mail
```

**Setup:**
```typescript
// lib/sendgrid.ts
import sgMail from '@sendgrid/mail'

sgMail.setApiKey(process.env.SENDGRID_API_KEY!)

export async function sendEmail({
  to,
  subject,
  html,
}: {
  to: string
  subject: string
  html: string
}) {
  await sgMail.send({
    from: 'noreply@yourdomain.com',
    to,
    subject,
    html,
  })
}
```

### Nodemailer (SMTP)

**Install:**
```bash
npm install nodemailer
```

**Setup:**
```typescript
// lib/nodemailer.ts
import nodemailer from 'nodemailer'

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: parseInt(process.env.SMTP_PORT!),
  secure: true,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASSWORD,
  },
})

export async function sendEmail({
  to,
  subject,
  html,
}: {
  to: string
  subject: string
  html: string
}) {
  await transporter.sendMail({
    from: process.env.EMAIL_FROM,
    to,
    subject,
    html,
  })
}
```

## React Email (Email Templates)

### Install
```bash
npm install react-email @react-email/components
npm install -D @react-email/tailwind
```

### Create Email Template
```typescript
// emails/welcome.tsx
import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Html,
  Link,
  Preview,
  Section,
  Text,
  Tailwind,
} from '@react-email/components'

interface WelcomeEmailProps {
  name: string
  loginUrl: string
}

export function WelcomeEmail({ name, loginUrl }: WelcomeEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Welcome to our platform, {name}!</Preview>
      <Tailwind>
        <Body className="bg-gray-100 font-sans">
          <Container className="bg-white mx-auto my-8 p-8 rounded-lg shadow-lg max-w-2xl">
            <Heading className="text-2xl font-bold text-gray-900 mb-4">
              Welcome, {name}!
            </Heading>

            <Text className="text-gray-700 mb-4">
              We're excited to have you on board. Get started by logging in to your account.
            </Text>

            <Section className="text-center my-8">
              <Button
                href={loginUrl}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold"
              >
                Log In to Your Account
              </Button>
            </Section>

            <Text className="text-gray-600 text-sm">
              If you didn't create this account, you can safely ignore this email.
            </Text>

            <Text className="text-gray-500 text-xs mt-8">
              © 2024 Your Company. All rights reserved.
              <br />
              <Link href="https://yourcompany.com/unsubscribe">Unsubscribe</Link>
            </Text>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  )
}

export default WelcomeEmail
```

### Render Email Template
```typescript
import { render } from '@react-email/components'
import { WelcomeEmail } from '@/emails/welcome'
import { resend } from '@/lib/email'

export async function sendWelcomeEmail(name: string, email: string) {
  const html = render(
    <WelcomeEmail
      name={name}
      loginUrl={`${process.env.NEXT_PUBLIC_APP_URL}/login`}
    />
  )

  await resend.emails.send({
    from: 'welcome@yourdomain.com',
    to: email,
    subject: `Welcome, ${name}!`,
    html,
  })
}
```

### Preview Emails (Development)
```bash
# Add script to package.json
{
  "scripts": {
    "email:dev": "email dev -p 3001"
  }
}

# Run preview server
npm run email:dev
# Visit http://localhost:3001
```

## Common Email Templates

### Password Reset
```typescript
// emails/password-reset.tsx
import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Html,
  Preview,
  Section,
  Text,
  Tailwind,
} from '@react-email/components'

interface PasswordResetEmailProps {
  name: string
  resetUrl: string
}

export function PasswordResetEmail({ name, resetUrl }: PasswordResetEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Reset your password</Preview>
      <Tailwind>
        <Body className="bg-gray-100 font-sans">
          <Container className="bg-white mx-auto my-8 p-8 rounded-lg max-w-2xl">
            <Heading className="text-2xl font-bold mb-4">
              Reset Your Password
            </Heading>

            <Text className="text-gray-700 mb-4">
              Hi {name}, we received a request to reset your password.
            </Text>

            <Section className="text-center my-8">
              <Button
                href={resetUrl}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg"
              >
                Reset Password
              </Button>
            </Section>

            <Text className="text-gray-600 text-sm">
              This link will expire in 1 hour. If you didn't request this, you can safely ignore this email.
            </Text>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  )
}
```

### Order Confirmation
```typescript
// emails/order-confirmation.tsx
interface OrderConfirmationEmailProps {
  name: string
  orderId: string
  items: Array<{ name: string; price: number; quantity: number }>
  total: number
}

export function OrderConfirmationEmail({
  name,
  orderId,
  items,
  total,
}: OrderConfirmationEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Order confirmation #{orderId}</Preview>
      <Tailwind>
        <Body className="bg-gray-100 font-sans">
          <Container className="bg-white mx-auto my-8 p-8 rounded-lg max-w-2xl">
            <Heading className="text-2xl font-bold mb-4">
              Order Confirmed!
            </Heading>

            <Text>Hi {name}, thanks for your order!</Text>
            <Text className="text-gray-600">Order #{orderId}</Text>

            <Section className="my-8">
              {items.map((item, index) => (
                <div key={index} className="flex justify-between py-2 border-b">
                  <Text>
                    {item.quantity}x {item.name}
                  </Text>
                  <Text>${item.price.toFixed(2)}</Text>
                </div>
              ))}
              <div className="flex justify-between py-4 font-bold">
                <Text>Total</Text>
                <Text>${total.toFixed(2)}</Text>
              </div>
            </Section>

            <Button href={`${process.env.NEXT_PUBLIC_APP_URL}/orders/${orderId}`}>
              View Order Details
            </Button>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  )
}
```

## Email Triggers

### Welcome Email on Signup
```typescript
// app/api/auth/signup/route.ts
import { sendWelcomeEmail } from '@/lib/emails/send'

export async function POST(request: Request) {
  const { email, name } = await request.json()

  // Create user
  const user = await createUser({ email, name })

  // Send welcome email (async, don't await)
  sendWelcomeEmail(name, email).catch((error) => {
    console.error('Failed to send welcome email:', error)
  })

  return Response.json({ user })
}
```

### Order Confirmation
```typescript
// lib/emails/send.ts
import { render } from '@react-email/components'
import { OrderConfirmationEmail } from '@/emails/order-confirmation'
import { resend } from '@/lib/email'

export async function sendOrderConfirmation(order: Order) {
  const html = render(
    <OrderConfirmationEmail
      name={order.customerName}
      orderId={order.id}
      items={order.items}
      total={order.total}
    />
  )

  await resend.emails.send({
    from: 'orders@yourdomain.com',
    to: order.customerEmail,
    subject: `Order Confirmation #${order.id}`,
    html,
  })
}
```

## Scheduled Emails

### Daily Digest
```typescript
// app/api/cron/daily-digest/route.ts
import { sendDailyDigest } from '@/lib/emails/send'

export async function GET(request: Request) {
  // Verify cron secret
  const authHeader = request.headers.get('authorization')
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 })
  }

  // Get users who opted in for daily digest
  const users = await db.users.findMany({
    where: { emailPreferences: { dailyDigest: true } },
  })

  // Send emails in batches
  for (const user of users) {
    await sendDailyDigest(user)
  }

  return Response.json({ sent: users.length })
}
```

### Vercel Cron Configuration
```json
// vercel.json
{
  "crons": [
    {
      "path": "/api/cron/daily-digest",
      "schedule": "0 9 * * *"
    },
    {
      "path": "/api/cron/weekly-summary",
      "schedule": "0 9 * * 1"
    }
  ]
}
```

## Email Queue (Background Jobs)

### Using Supabase Edge Functions
```typescript
// supabase/functions/send-email/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { Resend } from 'npm:resend'

const resend = new Resend(Deno.env.get('RESEND_API_KEY'))

serve(async (req) => {
  const { to, subject, html } = await req.json()

  const { data, error } = await resend.emails.send({
    from: 'noreply@yourdomain.com',
    to,
    subject,
    html,
  })

  return new Response(JSON.stringify({ data, error }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

### Queue Email for Sending
```typescript
import { createClient } from '@/lib/supabase/server'

export async function queueEmail({
  to,
  subject,
  html,
}: {
  to: string
  subject: string
  html: string
}) {
  const supabase = createClient()

  await supabase.from('email_queue').insert({
    to,
    subject,
    html,
    status: 'pending',
    created_at: new Date().toISOString(),
  })
}

// Process queue with cron
export async function processEmailQueue() {
  const supabase = createClient()

  const { data: emails } = await supabase
    .from('email_queue')
    .select('*')
    .eq('status', 'pending')
    .limit(10)

  for (const email of emails || []) {
    try {
      await resend.emails.send({
        from: 'noreply@yourdomain.com',
        to: email.to,
        subject: email.subject,
        html: email.html,
      })

      await supabase
        .from('email_queue')
        .update({ status: 'sent', sent_at: new Date().toISOString() })
        .eq('id', email.id)
    } catch (error) {
      await supabase
        .from('email_queue')
        .update({
          status: 'failed',
          error: error.message,
          attempts: email.attempts + 1,
        })
        .eq('id', email.id)
    }
  }
}
```

## Email Preferences

### User Email Settings
```typescript
// Database schema
type EmailPreferences = {
  marketing: boolean
  productUpdates: boolean
  weeklyDigest: boolean
  orderUpdates: boolean
}

// Update preferences
export async function updateEmailPreferences(
  userId: string,
  preferences: Partial<EmailPreferences>
) {
  await db.users.update({
    where: { id: userId },
    data: { emailPreferences: preferences },
  })
}

// Check before sending
export async function canSendEmail(
  userId: string,
  emailType: keyof EmailPreferences
): Promise<boolean> {
  const user = await db.users.findUnique({
    where: { id: userId },
    select: { emailPreferences: true },
  })

  return user?.emailPreferences[emailType] ?? false
}
```

### Unsubscribe Link
```typescript
// app/api/unsubscribe/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const token = searchParams.get('token')

  // Verify token and get user
  const userId = await verifyUnsubscribeToken(token)

  // Unsubscribe from all marketing emails
  await db.users.update({
    where: { id: userId },
    data: {
      emailPreferences: {
        marketing: false,
        productUpdates: false,
      },
    },
  })

  return new Response('You have been unsubscribed', { status: 200 })
}

// Generate unsubscribe link
function getUnsubscribeUrl(userId: string): string {
  const token = generateUnsubscribeToken(userId)
  return `${process.env.NEXT_PUBLIC_APP_URL}/api/unsubscribe?token=${token}`
}
```

## Email Testing

### Test Email Locally
```typescript
// lib/email-test.ts
import { sendWelcomeEmail } from '@/lib/emails/send'

async function testEmail() {
  await sendWelcomeEmail('Test User', 'test@example.com')
  console.log('Test email sent!')
}

testEmail()
```

### Email Preview in Browser
```typescript
// app/email-preview/[template]/page.tsx
import { WelcomeEmail } from '@/emails/welcome'

export default function EmailPreview({
  params,
}: {
  params: { template: string }
}) {
  const templates = {
    welcome: <WelcomeEmail name="John Doe" loginUrl="/login" />,
    // Add more templates
  }

  return (
    <div className="p-8">
      {templates[params.template]}
    </div>
  )
}
```

## Email Analytics

### Track Email Opens
```typescript
// emails/welcome.tsx
export function WelcomeEmail({ name, userId }: { name: string; userId: string }) {
  const trackingPixel = `${process.env.NEXT_PUBLIC_APP_URL}/api/email/track/open?userId=${userId}&email=welcome`

  return (
    <Html>
      {/* Email content */}
      <img src={trackingPixel} width="1" height="1" alt="" />
    </Html>
  )
}

// app/api/email/track/open/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const userId = searchParams.get('userId')
  const emailType = searchParams.get('email')

  // Track email open
  await db.emailEvents.create({
    data: {
      userId,
      emailType,
      event: 'open',
      timestamp: new Date(),
    },
  })

  // Return 1x1 transparent pixel
  const pixel = Buffer.from(
    'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
    'base64'
  )

  return new Response(pixel, {
    headers: {
      'Content-Type': 'image/gif',
      'Cache-Control': 'no-store',
    },
  })
}
```

### Track Link Clicks
```typescript
// Create tracked link
function createTrackedLink(url: string, userId: string, emailType: string): string {
  return `${process.env.NEXT_PUBLIC_APP_URL}/api/email/track/click?url=${encodeURIComponent(url)}&userId=${userId}&email=${emailType}`
}

// Handle click tracking
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const url = searchParams.get('url')
  const userId = searchParams.get('userId')
  const emailType = searchParams.get('email')

  // Track click
  await db.emailEvents.create({
    data: {
      userId,
      emailType,
      event: 'click',
      metadata: { url },
      timestamp: new Date(),
    },
  })

  // Redirect to actual URL
  return Response.redirect(url!, 302)
}
```

## Best Practices Checklist

- [ ] Use transactional email provider (Resend/SendGrid)
- [ ] Create email templates with React Email
- [ ] Implement unsubscribe links
- [ ] Respect user email preferences
- [ ] Queue emails for background processing
- [ ] Add email tracking (opens, clicks)
- [ ] Test emails before sending
- [ ] Use proper from addresses
- [ ] Include plain text version
- [ ] Handle bounces and complaints
- [ ] Add retry logic for failures
- [ ] Monitor email delivery rates
- [ ] Comply with email regulations (CAN-SPAM, GDPR)
- [ ] Use email authentication (SPF, DKIM, DMARC)

## When to Use This Skill

Invoke this skill when:
- Setting up email notifications
- Creating email templates
- Implementing transactional emails
- Building email campaigns
- Setting up scheduled emails
- Implementing email preferences
- Debugging email delivery
- Adding email tracking
- Creating unsubscribe flows
- Testing email templates
