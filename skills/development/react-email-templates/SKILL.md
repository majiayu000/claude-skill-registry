---
name: react-email-templates
description: React Email transactional templates for this project. Node runtime, inline styles, shared components, Resend integration. Triggers on "email", "react-email", "@react-email/components", "transactional", "Resend".
---

# React Email Templates

All transactional emails use React Email components with @convex-dev/resend. Templates run in Node runtime, use inline styles only.

## Directory Structure

```
packages/backend/convex/emails/
├── templates/       # Email templates (.tsx files)
│   ├── apiCreditsExhausted.tsx
│   ├── budgetWarning.tsx
│   ├── byodUpdateRequired.tsx
│   └── feedbackNotification.tsx
├── components/      # Shared email components
│   ├── EmailContainer.tsx
│   ├── EmailButton.tsx
│   └── index.ts
└── utils/          # Sending logic + rate limiting
    ├── send.ts     # Resend integration
    └── mutations.ts # Rate limit checks
```

## Template Pattern

Every template file requires `"use node"` directive and exports a React component:

```typescript
// From emails/templates/apiCreditsExhausted.tsx
"use node";
import { Body, Head, Html, Text } from "@react-email/components";
import { EmailContainer } from "../components";

export function ApiCreditsExhaustedEmail({
  errorMessage,
  modelId,
}: {
  errorMessage: string;
  modelId: string;
}) {
  return (
    <Html>
      <Head />
      <Body style={{ backgroundColor: "#f6f9fc", fontFamily: "sans-serif" }}>
        <EmailContainer>
          <Text
            style={{
              fontSize: "24px",
              fontWeight: "bold",
              color: "#dc2626",
            }}
          >
            🚨 API Credits Exhausted
          </Text>
          <Text style={{ fontSize: "16px", color: "#374151" }}>
            A generation request failed due to exhausted API credits.
          </Text>
          <Text
            style={{
              fontSize: "14px",
              color: "#6b7280",
              fontFamily: "monospace",
              backgroundColor: "#f3f4f6",
              padding: "12px",
              borderRadius: "4px",
            }}
          >
            Model: {modelId}
            <br />
            Error: {errorMessage}
          </Text>
        </EmailContainer>
      </Body>
    </Html>
  );
}
```

## Styling Rules

**CRITICAL**: Email clients don't support CSS classes. Use inline styles only.

```typescript
// ✅ CORRECT - Inline style object
<Text style={{ fontSize: "16px", color: "#374151" }}>
  Budget alert content
</Text>

// ❌ WRONG - CSS classes don't work in emails
<Text className="text-lg text-gray-700">
  Won't render properly
</Text>

// ✅ CORRECT - Multiple style properties
<Text
  style={{
    fontSize: "14px",
    color: "#6b7280",
    fontFamily: "monospace",
    backgroundColor: "#f3f4f6",
    padding: "12px",
    borderRadius: "4px",
  }}
>
  Styled content block
</Text>
```

## Shared Components

Reuse EmailContainer and EmailButton for consistency:

**EmailContainer** - Centered white card:
```typescript
// From emails/components/EmailContainer.tsx
import { Container, Section } from "@react-email/components";

export const EmailContainer = ({ children }: EmailContainerProps) => (
  <Container
    style={{
      margin: "40px auto",
      padding: "20px",
      backgroundColor: "#ffffff",
      borderRadius: "8px",
    }}
  >
    <Section>{children}</Section>
  </Container>
);
```

**EmailButton** - Purple CTA button:
```typescript
// From emails/components/EmailButton.tsx
import { Button } from "@react-email/components";

export const EmailButton = ({ href, children }: EmailButtonProps) => (
  <Button
    href={href}
    style={{
      backgroundColor: "#8b5cf6",
      color: "#ffffff",
      padding: "12px 24px",
      borderRadius: "6px",
      textDecoration: "none",
      display: "inline-block",
      marginTop: "16px",
    }}
  >
    {children}
  </Button>
);
```

Usage in templates:
```typescript
// From emails/templates/budgetWarning.tsx
import { EmailButton, EmailContainer } from "../components";

<EmailContainer>
  <Text style={{ fontSize: "24px", fontWeight: "bold", color: "#e11d48" }}>
    ⚠️ Budget Alert: {percentUsed.toFixed(0)}% Used
  </Text>
  <Text style={{ fontSize: "16px", color: "#374151" }}>
    Your blah.chat AI budget is at <strong>{percentUsed.toFixed(1)}%</strong> usage.
  </Text>
  <EmailButton href="https://blah.chat/admin/settings?tab=limits">
    Adjust Budget Limits
  </EmailButton>
</EmailContainer>
```

## Sending via Resend

Use @convex-dev/resend component in internalAction:

```typescript
// From emails/utils/send.ts
"use node";
import { Resend } from "@convex-dev/resend";
import { render } from "@react-email/render";
import { components, internal } from "../../_generated/api";
import { internalAction } from "../../_generated/server";

export const resend = new Resend(components.resend, {
  testMode: false, // Set to true for testing with delivered@resend.dev
});

export const sendBudgetAlert = internalAction({
  args: {
    percentUsed: v.number(),
    spent: v.number(),
    budget: v.number(),
    isExceeded: v.boolean(),
  },
  handler: async (ctx, args) => {
    // Render React Email template to HTML string
    const html = await render(
      BudgetWarningEmail({
        percentUsed: args.percentUsed,
        spent: args.spent,
        budget: args.budget,
      }),
    );

    // Send via Resend
    await resend.sendEmail(ctx, {
      from: "blah.chat Alerts <alerts@blah.chat>",
      to: recipientEmail,
      subject: args.isExceeded
        ? "🚨 Budget Exceeded - Messages Blocked"
        : `⚠️ Budget Warning - ${args.percentUsed.toFixed(0)}% Used`,
      html,
    });

    logger.info("Sent email", { tag: "Email", type, recipientEmail });
  },
});
```

## Rate Limiting

Prevent email spam with rate limit checks before sending:

**Global rate limit** (1 per hour for alert type):
```typescript
// From emails/utils/send.ts
const type = "api_credits_exhausted";

// Check rate limit
const canSend = await ctx.runMutation(
  internal.emails.utils.mutations.checkCanSend,
  { type },
);
if (!canSend) {
  logger.info("Skipping email - sent within last hour", { tag: "Email", type });
  return;
}

// Send email...

// Record sent
await ctx.runMutation(internal.emails.utils.mutations.recordSent, {
  type,
  recipientEmail,
  metadata: { errorMessage, modelId },
});
```

**Per-user rate limit** (one-time per user per type):
```typescript
// From emails/utils/send.ts - BYOD update notification
const type = `byod_update_${args.latestVersion}`;

// Check rate limit - one email per version update per user
const canSend = await ctx.runMutation(
  internal.emails.utils.mutations.checkCanSendToUser,
  { type, userId: args.userId },
);
if (!canSend) {
  logger.info("Skipping email - already sent", { tag: "Email", type, userId });
  return;
}
```

**No rate limiting** (send every time):
```typescript
// From emails/utils/send.ts - feedback notifications
// NO rate limiting check - send every time
await resend.sendEmail(ctx, {
  from: "blah.chat Feedback <feedback@blah.chat>",
  to: recipientEmail,
  subject,
  html,
});
```

Rate limit implementation uses `emailAlerts` table with indexes:
```typescript
// From emails/utils/mutations.ts
async function canSendEmail(ctx: any, type: string): Promise<boolean> {
  const oneHourAgo = Date.now() - 60 * 60 * 1000;

  const recentEmail = await ctx.db
    .query("emailAlerts")
    .withIndex("by_type_sent", (q: any) =>
      q.eq("type", type).gt("sentAt", oneHourAgo),
    )
    .first();

  return recentEmail === null;
}
```

## Testing Pattern

Set `testMode: true` to use Resend's test address:

```typescript
// In emails/utils/send.ts
export const resend = new Resend(components.resend, {
  testMode: true, // Sends to delivered@resend.dev instead of real addresses
});
```

Test mode bypasses real email sending:
- All emails go to `delivered@resend.dev`
- Check Resend dashboard for delivery confirmation
- Switch to `testMode: false` for production

## Anti-Patterns

**NEVER use plain text or raw HTML strings:**
```typescript
// ❌ WRONG - Plain text string
await resend.sendEmail(ctx, {
  from: "alerts@blah.chat",
  to: recipientEmail,
  subject: "Alert",
  text: "Your budget is at 80%", // Don't use plain text
});

// ❌ WRONG - Raw HTML string
const html = `
  <html>
    <body style="background: #f6f9fc;">
      <h1>Budget Alert</h1>
    </body>
  </html>
`;

// ✅ CORRECT - React Email template
const html = await render(BudgetWarningEmail({ percentUsed, spent, budget }));
```

**NEVER forget "use node" directive:**
```typescript
// ❌ WRONG - Missing directive causes runtime error
import { Body, Head, Html } from "@react-email/components";

export function MyEmail() { ... }

// ✅ CORRECT - Node runtime required for @react-email/render
"use node";
import { Body, Head, Html } from "@react-email/components";

export function MyEmail() { ... }
```

**NEVER use CSS classes:**
```typescript
// ❌ WRONG - Classes don't work in email clients
<div className="bg-white rounded-lg p-4">
  <p className="text-gray-700">Content</p>
</div>

// ✅ CORRECT - Inline styles only
<Container
  style={{
    backgroundColor: "#ffffff",
    borderRadius: "8px",
    padding: "16px",
  }}
>
  <Text style={{ color: "#374151" }}>Content</Text>
</Container>
```

## Key Files

- `packages/backend/convex/emails/templates/` - All email templates
- `packages/backend/convex/emails/components/` - Shared components (EmailContainer, EmailButton)
- `packages/backend/convex/emails/utils/send.ts` - Resend integration, internalActions
- `packages/backend/convex/emails/utils/mutations.ts` - Rate limiting logic
- `packages/backend/convex/_generated/api.ts` - Import `components.resend` from here

## Common Patterns

**Subject line with emojis:**
```typescript
subject: `🚨 API Credits Exhausted`
subject: `⚠️ Budget Warning - ${percentUsed.toFixed(0)}% Used`
subject: `🔄 Database Update Available (v${latestVersion})`
```

**Dynamic "from" addresses by category:**
```typescript
from: "blah.chat Alerts <alerts@blah.chat>"      // System alerts
from: "blah.chat Feedback <feedback@blah.chat>"  // User feedback
from: "blah.chat <updates@blah.chat>"            // Update notices
```

**Error handling (best-effort):**
```typescript
try {
  await resend.sendEmail(ctx, { ... });
  logger.info("Sent email", { tag: "Email", feedbackId });
} catch (error) {
  logger.error("Email failed", { tag: "Email", error: String(error) });
  // Don't throw - email is best-effort, continue execution
}
```
