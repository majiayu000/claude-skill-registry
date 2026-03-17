---
name: api-email-resend-react-email
description: Resend + React Email templates
---

# Email Patterns with Resend and React Email

> **Quick Guide:** Use Resend for transactional emails with React Email templates. Server-side sending for reliability, async for non-blocking requests, typed templates for safety. Always await render() before send, handle errors with retry logic, and include unsubscribe links for marketing emails.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST await `render()` before passing HTML to resend.emails.send() - render returns a Promise)**

**(You MUST handle Resend API errors and implement retry logic for transient failures)**

**(You MUST use server-side sending for all emails - never expose RESEND_API_KEY to the client)**

**(You MUST include unsubscribe links in marketing/notification emails - required for CAN-SPAM compliance)**

**(You MUST use typed props interfaces for all email templates - enables compile-time validation)**

</critical_requirements>

---

**Auto-detection:** Resend, React Email, @react-email/components, resend.emails.send, email template, transactional email, verification email, password reset email, notification email, email rendering

**When to use:**

- Sending transactional emails (verification, password reset, receipts)
- Creating React Email templates with Tailwind styling
- Integrating email sending with authentication flows
- Building notification systems with email delivery
- Implementing email tracking and analytics

**When NOT to use:**

- Initial Resend setup (use `setup/resend.md` skill)
- Marketing campaign management (use dedicated marketing tools)
- SMS or push notifications (different services)
- Email list management (use Resend Audiences or marketing tools)

**Key patterns covered:**

- React Email template patterns with Tailwind
- Sending with error handling and retry
- Authentication integration (verification, password reset)
- Async email sending patterns
- Email tracking (opens, clicks)
- Batch sending for notifications
- Type-safe email props
- Testing templates locally
- Unsubscribe and preferences handling
- Scheduled email sending (up to 30 days in advance)
- Idempotency keys for duplicate prevention
- Tags for analytics and campaign tracking

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [core.md](examples/core.md) - Template structure, basic sending (start here)
  - [templates.md](examples/templates.md) - Password Reset, Notification templates
  - [retry.md](examples/retry.md) - Retry logic with exponential backoff
  - [async-batch.md](examples/async-batch.md) - Async sending, batch API
  - [auth-integration.md](examples/auth-integration.md) - Auth system integration
  - [webhooks.md](examples/webhooks.md) - Webhook handler for tracking
  - [preferences.md](examples/preferences.md) - Unsubscribe, email preferences
  - [testing.md](examples/testing.md) - Template testing patterns
  - [advanced-features.md](examples/advanced-features.md) - Scheduled sending, idempotency keys, tags
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Email in modern applications follows a **server-side, template-driven** approach. React Email brings component patterns to email development, while Resend handles reliable delivery.

**Core principles:**

1. **Server-side only** - Never expose API keys to clients
2. **Typed templates** - Props interfaces catch errors at compile time
3. **Reliable delivery** - Error handling with retry logic
4. **Non-blocking** - Async sending for request-response patterns

**When to send emails:**

- User authentication events (verification, password reset, 2FA)
- Transactional confirmations (purchases, signups, invitations)
- Important notifications (security alerts, account changes)
- Team collaboration (invites, mentions, updates)

**When NOT to send emails:**

- Every minor action (creates email fatigue)
- Marketing without consent (spam, illegal)
- Real-time alerts (use push notifications)
- In-app actions (show in-app notifications instead)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Email Template Structure

Create well-structured email templates with proper typing.

```typescript
// packages/emails/src/templates/welcome-email.tsx
import { Button, Heading, Link, Text } from "@react-email/components";

import { BaseLayout } from "../layouts/base-layout";

const CTA_PADDING_X = 24;
const CTA_PADDING_Y = 12;

// Always define props interface
interface WelcomeEmailProps {
  userName: string;
  loginUrl: string;
  features?: string[];
}

export function WelcomeEmail({
  userName,
  loginUrl,
  features = [],
}: WelcomeEmailProps) {
  return (
    <BaseLayout preview={`Welcome to Your App, ${userName}!`}>
      <Heading className="text-2xl font-bold text-gray-900 mb-4">
        Welcome to Your App!
      </Heading>

      <Text className="text-gray-600 mb-4">Hi {userName},</Text>

      <Text className="text-gray-600 mb-6">
        Thanks for joining! We&apos;re excited to have you on board.
      </Text>

      {features.length > 0 && (
        <>
          <Text className="text-gray-600 mb-2 font-semibold">
            Here&apos;s what you can do:
          </Text>
          <ul className="text-gray-600 mb-6 pl-4">
            {features.map((feature) => (
              <li key={feature} className="mb-1">
                {feature}
              </li>
            ))}
          </ul>
        </>
      )}

      <Button
        href={loginUrl}
        className="bg-blue-600 text-white font-semibold rounded-md"
        style={{
          paddingLeft: CTA_PADDING_X,
          paddingRight: CTA_PADDING_X,
          paddingTop: CTA_PADDING_Y,
          paddingBottom: CTA_PADDING_Y,
        }}
      >
        Get Started
      </Button>
    </BaseLayout>
  );
}

// Preview props for development server
WelcomeEmail.PreviewProps = {
  userName: "John",
  loginUrl: "https://example.com/login",
  features: ["Create projects", "Invite team members", "Track progress"],
} satisfies WelcomeEmailProps;

// Named export with type
export { WelcomeEmail };
export type { WelcomeEmailProps };
```

**Why good:** Typed props catch errors at compile time, PreviewProps enable dev server preview, optional props have defaults, BaseLayout ensures consistency

---

### Pattern 2: Sending Emails with Error Handling

Send emails with proper error handling and logging.

```typescript
// lib/email/send-email.ts
import { render } from "@react-email/components";

import {
  getResendClient,
  DEFAULT_FROM_ADDRESS,
  DEFAULT_FROM_NAME,
} from "@repo/emails";

interface SendEmailOptions {
  to: string | string[];
  subject: string;
  react: React.ReactElement;
  replyTo?: string;
  cc?: string[];
  bcc?: string[];
}

interface SendEmailResult {
  success: boolean;
  id?: string;
  error?: string;
}

export async function sendEmail(
  options: SendEmailOptions,
): Promise<SendEmailResult> {
  const resend = getResendClient();

  try {
    // CRITICAL: Always await render()
    const html = await render(options.react);

    const { data, error } = await resend.emails.send({
      from: `${DEFAULT_FROM_NAME} <${DEFAULT_FROM_ADDRESS}>`,
      to: options.to,
      subject: options.subject,
      html,
      replyTo: options.replyTo,
      cc: options.cc,
      bcc: options.bcc,
    });

    if (error) {
      console.error("[Email] Send failed:", error);
      return {
        success: false,
        error: error.message,
      };
    }

    console.log("[Email] Sent successfully:", data?.id);
    return {
      success: true,
      id: data?.id,
    };
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    console.error("[Email] Unexpected error:", message);
    return {
      success: false,
      error: message,
    };
  }
}

// Named export
export { sendEmail };
export type { SendEmailOptions, SendEmailResult };
```

**Why good:** Wraps Resend client with consistent interface, always awaits render(), returns typed result, logs for debugging

---

### Pattern 3: Retry Logic for Transient Failures

Implement retry logic for temporary API failures.

```typescript
// lib/email/constants.ts
export const MAX_RETRY_ATTEMPTS = 3;
export const INITIAL_RETRY_DELAY_MS = 1000;
export const RETRY_BACKOFF_MULTIPLIER = 2;

// Errors that are safe to retry
const RETRYABLE_ERRORS = [
  "rate_limit_exceeded",
  "internal_server_error",
  "service_unavailable",
];
```

```typescript
// lib/email/send-with-retry.ts
export async function sendEmailWithRetry(
  options: SendWithRetryOptions,
): Promise<{ success: boolean; id?: string; error?: string }> {
  const resend = getResendClient();
  const maxRetries = options.maxRetries ?? MAX_RETRY_ATTEMPTS;

  let lastError: string | undefined;
  let attempt = 0;

  while (attempt < maxRetries) {
    attempt++;

    try {
      const html = await render(options.react);

      const { data, error } = await resend.emails.send({
        from: `${DEFAULT_FROM_NAME} <${DEFAULT_FROM_ADDRESS}>`,
        to: options.to,
        subject: options.subject,
        html,
      });

      if (error) {
        lastError = error.message;

        // Check if error is retryable
        const isRetryable = RETRYABLE_ERRORS.some((e) =>
          error.name?.toLowerCase().includes(e),
        );

        if (isRetryable && attempt < maxRetries) {
          const delay =
            INITIAL_RETRY_DELAY_MS *
            Math.pow(RETRY_BACKOFF_MULTIPLIER, attempt - 1);
          console.log(
            `[Email] Retry ${attempt}/${maxRetries} after ${delay}ms`,
          );
          await sleep(delay);
          continue;
        }

        return { success: false, error: error.message };
      }

      return { success: true, id: data?.id };
    } catch (err) {
      lastError = err instanceof Error ? err.message : "Unknown error";

      if (attempt < maxRetries) {
        const delay =
          INITIAL_RETRY_DELAY_MS *
          Math.pow(RETRY_BACKOFF_MULTIPLIER, attempt - 1);
        await sleep(delay);
        continue;
      }
    }
  }

  return { success: false, error: lastError ?? "Max retries exceeded" };
}
```

**Why good:** Exponential backoff prevents overwhelming the API, only retries transient errors, configurable retry count, logs retry attempts

</patterns>

---

<performance>

## Performance Optimization

### Parallel Template Rendering

```typescript
// Render multiple templates in parallel
const [verificationHtml, welcomeHtml] = await Promise.all([
  render(VerificationEmail({ userName, verificationUrl })),
  render(WelcomeEmail({ userName, loginUrl })),
]);
```

### Async Sending for Fast Responses

```typescript
// Don't await non-critical emails
sendEmailAsync({ to, subject, react });
return NextResponse.json({ success: true }); // Returns immediately
```

### Batch API for Multiple Recipients

```typescript
// Use batch API instead of loop
await resend.batch.send(emails); // Single API call for up to 100 emails
```

### Connection Reuse

```typescript
// Singleton client reuses connections
const resend = getResendClient(); // Same instance across requests
```

</performance>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST await `render()` before passing HTML to resend.emails.send() - render returns a Promise)**

**(You MUST handle Resend API errors and implement retry logic for transient failures)**

**(You MUST use server-side sending for all emails - never expose RESEND_API_KEY to the client)**

**(You MUST include unsubscribe links in marketing/notification emails - required for CAN-SPAM compliance)**

**(You MUST use typed props interfaces for all email templates - enables compile-time validation)**

**Failure to follow these rules will cause email delivery failures, security vulnerabilities, or legal compliance issues.**

</critical_reminders>

---

## Sources

- [Resend Node.js SDK](https://resend.com/docs/send-with-nodejs)
- [Resend Send Email API](https://resend.com/docs/api-reference/emails/send-email)
- [Resend Batch API](https://resend.com/docs/api-reference/emails/send-batch-emails)
- [Resend Webhooks Verification](https://resend.com/docs/dashboard/webhooks/verify-webhooks-requests)
- [Resend Idempotency Keys](https://resend.com/blog/engineering-idempotency-keys)
- [Resend Extended Scheduling](https://resend.com/changelog/extended-email-scheduling)
- [Resend Error Handling](https://resend.com/docs/api-reference/errors)
- [React Email Components](https://react.email/docs/components)
- [React Email 5.0 Release](https://resend.com/blog/react-email-5)
- [React Email Changelog](https://react.email/docs/changelog)
- [CAN-SPAM Compliance](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business)
