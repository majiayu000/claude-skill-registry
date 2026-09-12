---
name: agent-email-inbox
description: >
  Use when setting up a secure email inbox for any AI agent — configuring inbound
  email via Resend, webhooks, tunneling for local development, and implementing
  security measures to prevent prompt injection attacks. Also use when someone
  mentions 'agent email', 'bot inbox', 'receive emails for agent', 'agent webhook',
  'email security for AI', 'prompt injection via email', 'inbound email for bot',
  or wants their AI agent to receive and respond to emails securely.
---

# AI Agent Email Inbox

Set up a secure email inbox that lets an AI agent receive and respond to emails, with protection against prompt injection and email-based attacks.

**Core principle:** An AI agent's inbox is a potential attack vector. Malicious actors can email instructions that the agent might blindly follow. Security configuration is not optional — it's the first thing you implement, not the last.

This skill is context-independent — it does not use `brand/` files and works identically in any project.

## On Activation

1. Ask the user which agent needs an email inbox and what framework they're using (Next.js, Express, etc.).
2. Determine environment: local development or production deployment.
3. Walk through domain setup (Resend-managed or custom).
4. Set up webhook endpoint with signature verification.
5. If local dev: configure tunneling.
6. Implement security level — read [references/security-levels.md](references/security-levels.md) and present options to the user.
7. Connect webhook to agent processing.

**Output:** A configured webhook handler file, environment variable checklist, and security configuration.

## Architecture

```
Sender → Email → Resend (MX) → Webhook → Your Server → AI Agent
                                              ↓
                                    Security Validation
                                              ↓
                                    Process or Reject
```

## Before You Start: Account & API Key Setup

Ask the user:
- **New account just for the agent?** → Simpler setup, full account access is fine
- **Existing account with other projects?** → Use domain-scoped API keys to limit what the agent can access. Even if the key leaks, it can only send from one domain.

> **Don't paste API keys in chat!** They'll persist in conversation history. Have the user write directly to `.env` or use a secrets manager.

## Domain Setup

### Option 1: Resend-Managed Domain (Recommended for Getting Started)

Use your auto-generated address: `<anything>@<your-id>.resend.app`. No DNS configuration needed.

### Option 2: Custom Domain

The user enables receiving in the Resend dashboard, then adds an MX record:

| Setting | Value |
|---------|-------|
| **Type** | MX |
| **Host** | Your domain or subdomain (e.g., `agent.yourdomain.com`) |
| **Value** | Provided in Resend dashboard |
| **Priority** | 10 (lowest number takes precedence) |

**Use a subdomain** (e.g., `agent.yourdomain.com`) to avoid disrupting existing email services on your root domain — otherwise all email routes to Resend.

## Webhook Setup

The user registers a webhook in Resend dashboard (Webhooks → Add Webhook → select `email.received`). They need the endpoint URL you'll create and the signing secret for verification.

```typescript
// app/api/webhooks/email/route.ts (Next.js App Router)
import { Resend } from 'resend';
import { NextRequest, NextResponse } from 'next/server';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(req: NextRequest) {
  try {
    const payload = await req.text();

    const event = resend.webhooks.verify({
      payload,
      headers: {
        'svix-id': req.headers.get('svix-id'),
        'svix-timestamp': req.headers.get('svix-timestamp'),
        'svix-signature': req.headers.get('svix-signature'),
      },
      secret: process.env.RESEND_WEBHOOK_SECRET,
    });

    if (event.type === 'email.received') {
      const { data: email } = await resend.emails.receiving.get(
        event.data.email_id
      );
      // Security validation happens here (see Security Levels)
      await processEmailForAgent(event.data, email);
    }

    return new NextResponse('OK', { status: 200 });
  } catch (error) {
    console.error('Webhook error:', error);
    return new NextResponse('Error', { status: 400 });
  }
}
```

Resend retries failed deliveries with exponential backoff over ~6 hours. Emails are stored even if webhooks fail.

## Local Development with Tunneling

Your local server isn't accessible from the internet. Use tunneling to expose it:

| Option | Persistent URL? | Cost |
|--------|----------------|------|
| **ngrok (paid)** | Yes (static subdomain) | $8/mo |
| **Cloudflare named tunnel** | Yes (your own domain) | Free |
| **ngrok (free)** | No (changes on restart) | Free |
| **VS Code Port Forwarding** | No (changes per session) | Free |

For webhooks, persistent URLs matter — otherwise you re-register the URL every time the tunnel restarts. See the tunneling docs for each tool for setup instructions.

```bash
# ngrok (paid - recommended for persistent dev)
ngrok http --domain=myagent.ngrok.io 3000

# Cloudflare named tunnel (free but more setup)
cloudflared tunnel run my-agent-webhook
```

## Production Deployment

For a reliable agent inbox, deploy to production rather than relying on tunnels:

- **Serverless** (Vercel, Netlify, Cloudflare Workers) — zero server management, automatic HTTPS
- **VPS/cloud** — webhook handler runs alongside your agent, use nginx/caddy for HTTPS
- **Existing infrastructure** — add webhook route to your agent's existing web server

## Security Levels

This is the most critical part of the setup. An AI agent that processes emails without security is dangerous.

There are 5 graduated security levels. Read [references/security-levels.md](references/security-levels.md) for complete code examples and implementation details. Present the options to the user and help them choose:

| Level | Approach | Best For |
|-------|----------|----------|
| **1. Strict Allowlist** | Only process emails from approved addresses | Personal assistant agents |
| **2. Domain Allowlist** | Allow any address at approved domains | Team/org internal agents |
| **3. Content Filtering** | Accept from anyone, filter injection patterns | Customer support agents |
| **4. Sandboxed Processing** | Accept all, restrict agent capabilities | Public-facing agents |
| **5. Human-in-the-Loop** | Require human approval for untrusted senders | High-stakes agents |

Levels can be combined (e.g., Domain Allowlist + Content Filtering).

### Security Best Practices

| Practice | Why |
|----------|-----|
| Verify webhook signatures | Spoofed events let attackers control your agent |
| Log all rejected emails | Audit trail reveals attack patterns |
| Use allowlists where possible | Explicit trust is safer than trying to filter bad input |
| Rate limit email processing | A flood of emails can overwhelm your agent or exhaust API quotas |
| Separate trusted/untrusted handling | Different risk levels need different agent capabilities |

### What to Avoid

| Anti-Pattern | Risk |
|--------------|------|
| Processing emails without validation | Anyone can control your agent by sending an email |
| Trusting email headers for authentication | "From:" headers are trivially spoofed — use webhook verification instead |
| Executing code from email content | Remote code execution — the most dangerous vulnerability |
| Storing email content in prompts verbatim | Prompt injection attacks bypass your security layer entirely |
| Giving untrusted emails full agent access | One malicious email could compromise your entire system |

## Agent Integration

Connect your webhook to your AI agent:

```typescript
async function processWithAgent(email: ProcessedEmail) {
  const message = `New Email\nFrom: ${email.from}\nSubject: ${email.subject}\n\n${email.body}`.trim();
  await sendToAgent(message);
}
```

Alternatively, the agent can poll the Resend API during heartbeats instead of using webhooks — simpler architecture but less immediate.

## Complete Example

See [references/security-levels.md](references/security-levels.md) for the complete secure agent inbox implementation with configurable security levels, rate limiting, content truncation, and rejection logging.

## Environment Variables

```bash
RESEND_API_KEY=re_xxxxxxxxx
RESEND_WEBHOOK_SECRET=whsec_xxxxxxxxx
SECURITY_LEVEL=strict                    # strict | domain | filtered | sandboxed
ALLOWED_SENDERS=you@example.com,trusted@example.com
ALLOWED_DOMAINS=yourcompany.com
OWNER_EMAIL=you@example.com             # For security notifications
```

## Common Mistakes

| Mistake | Why It's a Problem | Fix |
|---------|-------------------|-----|
| No sender verification | Anyone can control your agent | Implement a security level (start with Level 1) |
| Trusting email headers | Headers are trivially spoofed | Rely on webhook signature verification only |
| Same treatment for all emails | Trusted and untrusted senders have different risk profiles | Use capability-based access control |
| Using ephemeral tunnel URLs | URL changes on restart, breaking webhook delivery | Use paid ngrok or Cloudflare named tunnels |
| No rate limiting | Flooding attacks can overwhelm the agent | Implement per-sender rate limits |
| Processing HTML directly | HTML can contain hidden injection content | Strip to plain text before processing |

## Testing

- `delivered@resend.dev` — simulates successful delivery
- `bounced@resend.dev` — simulates hard bounce
- Send from non-allowlisted addresses to verify rejection works

## Related Skills

- `send-email` — sending emails from your agent
- `resend-inbound` — detailed inbound email processing (domain setup, content retrieval, attachments)
