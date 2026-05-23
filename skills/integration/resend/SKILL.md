---
name: resend
description: >
  Implement email notifications for PhotoVault using Resend and React Email.
  Use when working with email templates, transactional emails, notification
  triggers, deliverability issues, or styling email content. Includes
  PhotoVault branding and template patterns.
---

# ⚠️ MANDATORY WORKFLOW - DO NOT SKIP

**When this skill activates, you MUST follow the expert workflow before writing any code:**

1. **Spawn Domain Expert** using the Task tool with this prompt:
   ```
   Read the expert prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\resend-expert.md

   Then research the codebase and write an implementation plan to: docs/claude/plans/email-[task-name]-plan.md

   Task: [describe the user's request]
   ```

2. **Spawn QA Critic** after expert returns, using Task tool:
   ```
   Read the QA critic prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\qa-critic-expert.md

   Review the plan at: docs/claude/plans/email-[task-name]-plan.md
   Write critique to: docs/claude/plans/email-[task-name]-critique.md
   ```

3. **Present BOTH plan and critique to user** - wait for approval before implementing

**DO NOT read files and start coding. DO NOT rationalize that "this is simple." Follow the workflow.**

---

# Resend Email Integration

## Core Principles

### Email HTML is NOT Web HTML

Email clients strip `<style>` tags, ignore CSS classes, and render tables differently. Everything must be inline.

```tsx
// ❌ BAD: CSS classes don't work
<div className="button">Click me</div>

// ✅ GOOD: Inline styles
<a href={url} style={{
  backgroundColor: '#f59e0b',
  color: '#000000',
  padding: '12px 24px',
  borderRadius: '8px',
  textDecoration: 'none',
  display: 'inline-block',
}}>
  Click me
</a>
```

### Mobile First (60%+ opens)

Most emails are read on phones. Design for 320px width first.

```tsx
const container = {
  maxWidth: '600px',
  padding: '20px',
  margin: '0 auto',
}
```

### Every Email Needs a Preview

The preview text appears in the inbox next to the subject.

```tsx
import { Preview } from '@react-email/components'
<Preview>Your gallery "Smith Wedding" is ready with 247 photos</Preview>
```

## Anti-Patterns

**Using CSS classes or external stylesheets**
```tsx
// WRONG: Won't render
<style>{`.button { background: blue; }`}</style>
<a className="button">Click</a>

// RIGHT: Inline everything
<a style={{ backgroundColor: 'blue', padding: '12px 24px' }}>Click</a>
```

**Using flexbox or grid**
```tsx
// WRONG: Not supported in most email clients
<div style={{ display: 'flex' }}>

// RIGHT: Use tables for layout
import { Row, Column } from '@react-email/components'
<Row>
  <Column>Left content</Column>
  <Column>Right content</Column>
</Row>
```

**Forgetting alt text on images**
```tsx
// WRONG: Images often blocked
<Img src={url} />

// RIGHT: Always include meaningful alt
<Img src={url} alt="Preview of your wedding photos" />
```

**Generic subject lines**
```typescript
// WRONG: Low open rate
subject: 'Update from PhotoVault'

// RIGHT: Specific and actionable
subject: 'Your "Smith Wedding" gallery is ready - 247 photos inside'
```

**Not handling send failures**
```typescript
// WRONG: Silent failure
await resend.emails.send({ ... })

// RIGHT: Handle errors
const { data, error } = await resend.emails.send({ ... })
if (error) {
  console.error('Email failed:', error)
}
```

## Email Template Pattern

```tsx
// src/lib/email/templates/gallery-ready.tsx
import {
  Body, Container, Head, Heading, Html,
  Img, Link, Preview, Section, Text,
} from '@react-email/components'

interface GalleryReadyEmailProps {
  clientName: string
  galleryName: string
  photoCount: number
  previewImageUrl: string
  galleryUrl: string
}

export function GalleryReadyEmail({
  clientName, galleryName, photoCount, previewImageUrl, galleryUrl,
}: GalleryReadyEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Your "{galleryName}" gallery is ready - {photoCount} photos inside</Preview>
      <Body style={main}>
        <Container style={container}>
          <Img src="https://photovault.photo/logo.png" alt="PhotoVault" width={150} />
          <Heading style={heading}>Hi {clientName}!</Heading>
          <Text style={text}>
            Your photos from <strong>{galleryName}</strong> are ready.
            Your photographer has uploaded {photoCount} photos.
          </Text>
          {previewImageUrl && (
            <Img src={previewImageUrl} alt={`Preview from ${galleryName}`} width={560} />
          )}
          <Section style={{ textAlign: 'center', marginTop: '30px' }}>
            <Link href={galleryUrl} style={button}>View Your Photos</Link>
          </Section>
        </Container>
      </Body>
    </Html>
  )
}

const main = {
  backgroundColor: '#0a0a0a',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
}

const container = { maxWidth: '600px', margin: '0 auto', padding: '40px 20px' }
const heading = { color: '#ffffff', fontSize: '28px', fontWeight: 'bold' }
const text = { color: '#a3a3a3', fontSize: '16px', lineHeight: '26px' }
const button = {
  backgroundColor: '#f59e0b',
  color: '#000000',
  padding: '14px 28px',
  borderRadius: '8px',
  textDecoration: 'none',
  fontWeight: 'bold',
  display: 'inline-block',
}
```

## Email Service

```typescript
// src/lib/email/email-service.ts
import { Resend } from 'resend'

const resend = new Resend(process.env.RESEND_API_KEY)

interface SendEmailParams {
  to: string | string[]
  subject: string
  react: React.ReactElement
  replyTo?: string
}

export async function sendEmail({ to, subject, react, replyTo }: SendEmailParams) {
  try {
    const { data, error } = await resend.emails.send({
      from: 'PhotoVault <noreply@photovault.photo>',
      to: Array.isArray(to) ? to : [to],
      subject,
      react,
      replyTo: replyTo || 'support@photovault.photo',
    })

    if (error) {
      console.error('[Email] Send failed:', error)
      return { success: false, error }
    }

    console.log('[Email] Sent successfully:', data?.id)
    return { success: true, id: data?.id }
  } catch (error) {
    console.error('[Email] Unexpected error:', error)
    return { success: false, error }
  }
}
```

## PhotoVault Configuration

### Templates Needed

| Template | Trigger | Recipient |
|----------|---------|-----------|
| `gallery-ready` | Photographer marks ready | Client |
| `payment-success` | Checkout completed | Client |
| `payment-failed` | Invoice failed | Client |
| `invitation` | Photographer invites client | Client |
| `commission-earned` | Client pays | Photographer |

### Branding

| Element | Value |
|---------|-------|
| Primary color | `#f59e0b` (amber) |
| Background | `#0a0a0a` (near black) |
| Text | `#a3a3a3` (gray) |
| Headings | `#ffffff` (white) |

### Environment Variables

```bash
RESEND_API_KEY=re_...
FROM_EMAIL=PhotoVault <noreply@photovault.photo>
```

## Testing Emails

```bash
# Preview locally
npx react-email dev
```

## Deliverability Checklist

1. ✅ Domain verified in Resend (DKIM, SPF)
2. ✅ FROM address uses verified domain
3. ✅ Subject line is specific, not spammy
4. ✅ Alt text on all images
5. ✅ No URL shorteners
6. ✅ Reply-to address is valid
