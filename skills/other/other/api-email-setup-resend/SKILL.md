---
name: api-email-setup-resend
description: Resend email setup, domain verification
---

# Resend Email & React Email Setup

> **Quick Guide:** Resend email API with React Email templates. Use the `react` prop to pass components directly to `resend.emails.send()` -- no manual `render()` needed. Keep email templates in a dedicated package for monorepo separation. Verify your sending domain before production. Use `@react-email/render` (not `@react-email/components`) if you need to render to HTML strings manually.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `RESEND_API_KEY` environment variable -- NEVER hardcode API keys)**

**(You MUST verify your sending domain in Resend dashboard before production -- unverified domains only send to your own email)**

**(You MUST use `@react-email/components` for email UI components and `@react-email/render` for HTML rendering -- these are separate packages)**

**(You MUST use `resend.emails.send({ react: MyTemplate(props) })` as the primary sending pattern -- manual `render()` to HTML is only needed for non-Resend senders)**

</critical_requirements>

---

**Auto-detection:** Resend setup, resend install, React Email setup, email templates setup, RESEND_API_KEY, domain verification, SPF DKIM DMARC, transactional email setup, email preview server, @react-email/components, react-email

**When to use:**

- Initial Resend + React Email setup in a project
- Configuring domain verification and DNS records
- Setting up the email preview dev server
- Structuring email templates in a monorepo

**When NOT to use:**

- Marketing email campaigns (use dedicated marketing tools)
- SMS or push notifications (different service)
- Non-JavaScript backends (consider Postmark, SendGrid)
- Need SMTP relay (Resend is API-only)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Client setup, sending patterns, template structure, preview server

---

<philosophy>

## Philosophy

Resend is a **developer-first email API** built by the creators of React Email. React Email brings modern component patterns to email development, replacing legacy table-based HTML.

**Core principles:**

1. **Emails as React components** - Write emails with JSX, Tailwind CSS, and TypeScript
2. **Preview before send** - Local dev server shows exact email rendering
3. **Monorepo separation** - Email templates in dedicated package, not mixed with app code
4. **`react` prop over `render()`** - Resend SDK renders components internally when you pass them via the `react` prop

**When to use Resend:**

- Transactional emails (verification, password reset, notifications)
- React/TypeScript stack wanting best DX
- Need reliable deliverability without managing email infrastructure

**When NOT to use Resend:**

- Marketing campaigns with complex analytics (use Mailchimp, SendGrid Marketing)
- Very high volume (>1M emails/month) without enterprise plan
- Non-JavaScript backend (consider Postmark, SendGrid)
- Need SMTP relay (Resend is API-only)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Sending with the `react` Prop (Preferred)

The Resend SDK accepts React components directly via the `react` prop -- no manual HTML rendering needed.

```typescript
import { Resend } from "resend";
import { WelcomeEmail } from "./templates/welcome-email";

const resend = new Resend(process.env.RESEND_API_KEY);

// Pass the component call directly -- SDK handles rendering
const { data, error } = await resend.emails.send({
  from: "Your App <noreply@yourdomain.com>",
  to: ["user@example.com"],
  subject: "Welcome!",
  react: WelcomeEmail({ userName: "John" }),
});

if (error) {
  console.error("[Email] Send failed:", error);
}
```

**Why good:** No manual `render()` call, SDK handles conversion internally, cleaner code

```typescript
// BAD: Unnecessary manual render step
import { render } from "@react-email/render";

const html = await render(WelcomeEmail({ userName: "John" }));
await resend.emails.send({ html, from, to, subject });
```

**Why bad:** Extra dependency and await when Resend handles it natively

**When to use `render()` instead:** Only when sending via a non-Resend email provider (e.g., Nodemailer, SendGrid) that needs an HTML string. Import from `@react-email/render`, not `@react-email/components`.

---

### Pattern 2: Domain Verification

Verify your domain to send from custom addresses. Unverified accounts can only send to your own email.

1. Go to Resend Dashboard > Domains > Add Domain
2. Add the DNS records Resend provides to your DNS provider:
   - **SPF** (TXT): `v=spf1 include:amazonses.com ~all`
   - **DKIM** (3 CNAME records): Values provided by Resend
   - **DMARC** (TXT, recommended): `v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com`
3. Click Verify -- DNS propagation can take up to 48 hours

**Why this matters:** Unverified domains are limited to sending to your account email only. Production sending requires verification. Proper DNS records prevent emails from landing in spam.

---

### Pattern 3: Monorepo Package Structure

Keep email templates in a dedicated package, separate from your application code.

```
packages/emails/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts              # Re-export all templates
│   ├── client.ts             # Resend client singleton
│   ├── layouts/
│   │   └── base-layout.tsx   # Shared layout wrapper
│   ├── components/
│   │   ├── button.tsx        # Reusable email button
│   │   └── footer.tsx        # Email footer
│   └── templates/
│       ├── verification-email.tsx
│       ├── password-reset.tsx
│       └── welcome-email.tsx
└── emails/                   # For react-email dev server
```

**Why good:** Reusable across apps, prevents bundling issues, clean separation of concerns

See [examples/core.md](examples/core.md) for full client setup and template examples.

---

### Pattern 4: Email Error Handling

Resend returns `{ data, error }` -- always check the error.

```typescript
const { data, error } = await resend.emails.send(emailOptions);

if (error) {
  console.error("[Email] Send failed:", error.name, error.message);
  return { success: false, error: error.message };
}

return { success: true, id: data?.id };
```

**Why good:** Explicit error checking, structured logging, returns typed result

```typescript
// BAD: Ignoring the error response
await resend.emails.send(emailOptions);
return { success: true }; // May have silently failed!
```

**Why bad:** No error detection, reports success even on failure, no debugging info

---

### Pattern 5: Webhook Verification

Always verify webhook signatures before processing events. The `verify()` method **throws** on invalid signatures.

```typescript
const payload = await request.text(); // Raw body, NOT parsed JSON

try {
  const event = resend.webhooks.verify({
    payload,
    headers: {
      id: request.headers.get("svix-id") ?? "",
      timestamp: request.headers.get("svix-timestamp") ?? "",
      signature: request.headers.get("svix-signature") ?? "",
    },
    webhookSecret: process.env.RESEND_WEBHOOK_SECRET!,
  });

  // event.type: "email.sent" | "email.delivered" | "email.bounced" | etc.
} catch {
  return new Response("Invalid webhook signature", { status: 400 });
}
```

**Why good:** SDK's built-in verification, uses raw body (not parsed JSON which breaks signature), try/catch handles invalid signatures

**Gotcha:** You MUST use `request.text()` not `request.json()` -- parsing as JSON before verification breaks the cryptographic signature. The `verify()` method throws on failure (unlike `emails.send()` which returns `{ data, error }`).

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority:**

- Hardcoded `RESEND_API_KEY` in source code (security vulnerability, visible in git)
- Sending from unverified domain in production (emails fail or go to spam)
- Importing `render` from `@react-email/components` (wrong package -- use `@react-email/render`)
- Not awaiting `render()` when using it (returns Promise, email body becomes `[object Promise]`)

**Medium Priority:**

- No error handling on `resend.emails.send()` (silent failures)
- Email templates inside app directory instead of dedicated package (bundling issues in monorepo)
- Using `request.json()` instead of `request.text()` for webhook payload (breaks signature verification)

**Gotchas & Edge Cases:**

- Resend free tier: 100 emails/day, 3000 emails/month
- Unverified domains can only send to your account's email address
- DNS propagation takes up to 48 hours for domain verification
- React Email dev server creates a `.react-email` folder in your project
- Using Grid, Flexbox, or `box-shadow` in email templates does not work in Gmail/Outlook
- Use `px` units in emails -- `rem` renders inconsistently across email clients
- In Resend SDK v6.1.0+, some bundlers may error on `@react-email/render` -- add `resend` to your bundler's external packages config if you see resolution errors
- `@react-email/components` is for UI components (Body, Button, etc.); `@react-email/render` is for the `render()` utility -- they are separate packages

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

**(You MUST use `RESEND_API_KEY` environment variable -- NEVER hardcode API keys)**

**(You MUST verify your sending domain in Resend dashboard before production -- unverified domains only send to your own email)**

**(You MUST use `@react-email/components` for email UI components and `@react-email/render` for HTML rendering -- these are separate packages)**

**(You MUST use `resend.emails.send({ react: MyTemplate(props) })` as the primary sending pattern -- manual `render()` to HTML is only needed for non-Resend senders)**

**Failure to follow these rules will cause email delivery failures or security vulnerabilities.**

</critical_reminders>
