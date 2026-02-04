---
name: elon-email-templates
description: Use when creating or modifying email templates for Elon AI - welcome emails, role changes, notifications, teacher digests, or QR code invitations. This project uses HTML string templates, NOT React Email components.
---

# Elon AI Email Templates

## Overview

HTML string-based email templates for the Elon AI Classroom Assistant platform. This project does **NOT use React Email components** - all templates are pure HTML strings with TypeScript helper functions.

> **Important:** The global `react-email` skill documents React Email patterns. This project uses a different approach optimized for simplicity and performance. Follow **this skill** for Elon AI email work.

## When to Use

- Creating new transactional email templates
- Modifying existing templates in `email-send.ts`
- Understanding the email queue architecture
- Adding new email types to the system

## Architecture

### Email Flow

```
API/Action → publishJob({jobType: "email:send"})
  → Upstash QStash (queue)
  → emailSendHandler()
  → Template selection (EMAIL_TEMPLATES[templateId])
  → HTML string generation
  → Resend API
  → User inbox
```

### Key Files

| File | Purpose |
|------|---------|
| `lib/jobs/handlers/email-send.ts` | All 12 email templates + handler (916 lines) |
| `lib/email/constants.ts` | Centralized colors, styles, logo URL |
| `lib/email/unsubscribe-token.ts` | HMAC-signed unsubscribe tokens |
| `app/api/email/unsubscribe/route.ts` | Unsubscribe API endpoint |
| `lib/jobs/types.ts` | `EmailSendPayloadSchema` definition |
| `.email-previews/` | HTML preview files for visual testing |

## Template Pattern

All templates use pure HTML strings with helper functions:

```typescript
// Template structure in EMAIL_TEMPLATES object
welcome: (data) => ({
  subject: "Welcome to Elon AI!",
  html: wrapInBaseTemplate({
    headerTitle: `Welcome, ${escapeHtml(data.name)}!`,
    headerSubtitle: "Your AI-powered study companion is ready",
    content: `
      <p style="${STYLES.bodyText}">
        Hey ${escapeHtml(data.name)}, welcome to Elon AI!
      </p>
      ${createButton("Get Started", url)}
    `,
    proTip: "Your conversations are FERPA-protected.",
  }),
}),
```

### Helper Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `wrapInBaseTemplate()` | Header + content + footer wrapper | See above |
| `createButton()` | Primary/secondary CTA buttons | `createButton("Click Me", url, "primary")` |
| `createInfoBox()` | Key-value info cards | `createInfoBox([{label: "Name", value: "John"}])` |
| `escapeHtml()` | XSS protection for user content | `escapeHtml(user.name)` |

### Style Constants

All styles are defined in `STYLES` object at top of `email-send.ts`:

```typescript
const STYLES = {
  container: "...",      // Max-width 600px centered layout
  header: "...",         // Maroon gradient header
  headerTitle: "...",    // White text for header
  body: "...",           // White background body
  bodyText: "...",       // Gray text paragraphs
  button: "...",         // Maroon primary button
  buttonSecondary: "...", // White bordered button
  infoBox: "...",        // Gray background info card
  proTipBox: "...",      // Gold accent tip box
  footer: "...",         // Gray footer
  // ... more
};
```

## Existing Templates (12)

| Template ID | Purpose | Key Data Fields |
|-------------|---------|-----------------|
| `welcome` | New student onboarding | `name` |
| `role_change` | User role changed | `userName`, `oldRole`, `newRole` |
| `assistant_published` | Teacher's assistant goes live | `assistantName`, `courseName`, `joinCode` |
| `budget_warning` | Admin usage alert | `percentUsed`, `currentSpend`, `budgetLimit` |
| `processing_failed` | File upload error | `fileName`, `errorMessage` |
| `new_student_joined` | Admin notification | `studentName`, `studentEmail`, `joinedAt` |
| `role_request` | Admin action needed | `userName`, `userEmail`, `requestedRole` |
| `role_approved` | Role request approved | `name`, `newRole`, `tips[]`, `dashboardUrl` |
| `role_denied` | Role request denied | `name`, `requestedRole`, `reason` |
| `teacher_digest` | Weekly analytics | `totalSessions`, `uniqueStudents`, `satisfactionRate`, `topTopic` |
| `qr_join_code` | QR code invitation | `assistantName`, `courseName`, `joinCode`, `qrCodeUrl` |

## Adding a New Template

### Step 1: Add to EMAIL_TEMPLATES object

```typescript
// In lib/jobs/handlers/email-send.ts

const EMAIL_TEMPLATES = {
  // ... existing templates

  // Your new template
  my_new_template: (data) => ({
    subject: `Your subject with ${escapeHtml(data.dynamicValue)}`,
    html: wrapInBaseTemplate({
      headerTitle: "Header Title",
      headerSubtitle: "Optional subtitle",
      content: `
        <p style="${STYLES.bodyText}">
          ${escapeHtml(data.message)}
        </p>
        ${createButton("Action", data.actionUrl)}
      `,
      proTip: "Optional helpful tip",
    }),
  }),
};
```

### Step 2: Add payload schema (if needed)

If your template needs specific data validation, update `lib/jobs/types.ts`:

```typescript
export const EmailSendPayloadSchema = z.object({
  tenantId: z.string().uuid(),
  templateId: z.string(), // Template ID
  to: z.string().email(),
  subject: z.string().optional(), // Override template subject
  data: z.record(z.unknown()), // Template-specific data
});
```

### Step 3: Trigger the email

```typescript
import { publishJob } from "@/lib/jobs/publisher";

await publishJob({
  jobType: "email:send",
  payload: {
    tenantId: user.tenantId,
    templateId: "my_new_template",
    to: user.email,
    data: {
      message: "Hello world!",
      actionUrl: "https://elon-ai.app/action",
    },
  },
});
```

### Step 4: Generate preview

Add test data and regenerate previews:

```bash
pnpm email:preview
```

## Security Requirements

### XSS Protection

**ALWAYS** use `escapeHtml()` on user-controlled content:

```typescript
// CORRECT - escaped
<p>${escapeHtml(data.userName)}</p>

// WRONG - XSS vulnerability!
<p>${data.userName}</p>
```

### FERPA Compliance

- Include `tenantId` in all email payloads
- All sends are logged to `audit_logs` table
- Don't include student PII in email subjects
- Unsubscribe tokens use HMAC-SHA256 signing

### Multi-Tenant Scoping

- Emails are always scoped to a tenant
- Job queue handles tenant isolation
- Audit logs record tenant context

## Email Client Compatibility

### DO

- Use **PNG/JPG images** with absolute URLs
- Use inline CSS styles (no classes)
- Use table-based layouts for columns
- Keep emails under 102KB
- Test in Gmail, Outlook, Apple Mail

### DON'T

- Use SVG images (Gmail strips them)
- Use CSS Grid or Flexbox
- Use media queries (limited support)
- Use external CSS files
- Use JavaScript

### Logo

The logo is a hosted PNG at `public/email-assets/elon-ai-logo.png`:

```typescript
// Defined in lib/jobs/handlers/email-send.ts
const EMAIL_LOGO_URL = "https://elon-ai.app/email-assets/elon-ai-logo.png";
const LOGO_IMG = `<img src="${EMAIL_LOGO_URL}" alt="Elon AI" width="48" height="48" />`;
```

To regenerate the logo PNG:
```bash
pnpm tsx scripts/generate-email-logo.ts
```

## Testing

### Visual Previews

Open `.email-previews/index.html` to browse all templates visually.

### Unit Tests

```bash
pnpm test tests/unit/email/
```

### Integration Tests

```bash
pnpm test tests/integration/api/unsubscribe.test.ts
```

### Development Mode

When `RESEND_API_KEY` is not set, emails are logged to console instead of sent.

## Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Maroon | `#73000a` | Headers, buttons, primary text |
| Gold | `#b59a57` | Accents, pro tips, highlights |
| White | `#ffffff` | Body backgrounds, button text |
| Gray-50 | `#f9fafb` | Footer, info box backgrounds |
| Gray-700 | `#374151` | Body text |

## Common Patterns

### Teacher Analytics Email

The `teacher_digest` template demonstrates advanced patterns:
- Dynamic headlines based on metrics
- Conditional content based on activity level
- Unsubscribe link with HMAC token
- Color-coded metric changes

### QR Code Email

The `qr_join_code` template shows how to include images:
- Hosted QR code image URL
- Fallback text if image fails
- Clear call-to-action
