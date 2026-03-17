---
name: api-email-setup-resend
description: Resend email setup, domain verification
---

# Resend Email & React Email Setup

> **Quick Guide:** One-time setup for Resend email API with React Email templates in a Next.js App Router monorepo. Covers package installation, environment variables, domain verification, React Email project structure, preview server, and Better Auth integration.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `RESEND_API_KEY` environment variable for the server-side API key - NEVER hardcode secrets)**

**(You MUST verify your sending domain in Resend dashboard before production emails - unverified domains only allow sending to your own email)**

**(You MUST create email templates in a dedicated `packages/emails/` directory for monorepo - not inside the Next.js app)**

**(You MUST use `@react-email/components` for email components - external UI libraries like Material UI are NOT supported)**

**(You MUST configure the Resend SDK with appropriate region for your users - reduces delivery latency)**

</critical_requirements>

---

**Auto-detection:** Resend setup, resend install, React Email setup, email templates setup, RESEND_API_KEY, domain verification, SPF DKIM DMARC, transactional email setup, email preview server

**When to use:**

- Initial Resend setup in a new project
- Setting up React Email templates package in monorepo
- Configuring domain verification and DNS records
- Setting up email preview server for development
- Integrating email sending with Better Auth

**When NOT to use:**

- Sending individual emails (use `backend/email.md` for patterns)
- Email template design patterns (use `backend/email.md` for patterns)
- Marketing email campaigns (use dedicated marketing tools)
- SMS or push notifications (different service)

**Key patterns covered:**

- Resend account and API key setup
- Domain verification (SPF, DKIM, DMARC)
- React Email package structure for monorepo
- Email preview server configuration
- Next.js App Router API route setup
- Better Auth email callbacks integration
- Environment variables configuration
- Vercel deployment setup

**Detailed Resources:**

- For code examples, see [examples/](examples/):
  - [core.md](examples/core.md) - Client setup, constants, package exports
  - [templates.md](examples/templates.md) - Base layout, components, email templates
  - [integrations.md](examples/integrations.md) - Better Auth, Next.js API routes
  - [deployment.md](examples/deployment.md) - Preview server, Vercel config, checklist
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Resend is a **developer-first email API** built by the creators of React Email. It provides a simple API for sending transactional emails with excellent deliverability. React Email brings modern component patterns to email development, replacing legacy table-based HTML.

**Core principles:**

1. **Emails as React components** - Write emails with JSX, Tailwind CSS, and TypeScript
2. **Preview before send** - Local development server shows exact email rendering
3. **Monorepo separation** - Email templates in dedicated package, not mixed with app code
4. **Type-safe sending** - Full TypeScript support from template to API call

**React Email 5.0 (Current):**

- Requires Tailwind 4 (compatibility checker only supports Tailwind 4)
- Supports React 19.2 and Next.js 16
- Dark mode theming support with tested email client compatibility
- Templates can be uploaded directly to Resend dashboard via CLI

**When to use Resend:**

- Transactional emails (verification, password reset, notifications)
- Developer experience priority (best DX in the space)
- React/TypeScript stack
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

### Pattern 1: Resend Account and API Key Setup

Create a Resend account and get your API key for development.

#### Account Setup

1. Sign up at [resend.com](https://resend.com)
2. Navigate to API Keys section
3. Create a new API key with appropriate permissions

```bash
# API key format
re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Environment Variables

```bash
# apps/client-next/.env.local

# Resend Configuration
RESEND_API_KEY=re_your_api_key_here

# Optional: Specify sending region for lower latency
# Options: us-east-1 (default), eu-west-1, sa-east-1, ap-northeast-1
RESEND_REGION=us-east-1

# Email "from" address (must be verified domain or onboarding@resend.dev for testing)
EMAIL_FROM_ADDRESS=noreply@yourdomain.com
EMAIL_FROM_NAME="Your App"
```

**Why good:** Environment variables protect secrets, region setting reduces latency, separate FROM variables enable easy updates

---

### Pattern 2: Domain Verification (Production Required)

Verify your domain to send from custom addresses. Unverified accounts can only send to your own email.

#### DNS Records Required

Add these records in your domain's DNS settings (Cloudflare, Route 53, etc.):

```markdown
## Required DNS Records

### SPF Record (TXT)

Host: @
Type: TXT
Value: v=spf1 include:amazonses.com ~all

### DKIM Records (CNAME) - Resend provides 3 records

Host: resend.\_domainkey
Type: CNAME
Value: (provided by Resend dashboard)

Host: resend2.\_domainkey
Type: CNAME
Value: (provided by Resend dashboard)

Host: resend3.\_domainkey
Type: CNAME
Value: (provided by Resend dashboard)

### DMARC Record (TXT) - Recommended

Host: \_dmarc
Type: TXT
Value: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

#### Verification Process

1. Go to Resend Dashboard > Domains
2. Click "Add Domain"
3. Enter your domain (e.g., `yourdomain.com`)
4. Copy the provided DNS records
5. Add records to your DNS provider
6. Click "Verify" - may take up to 48 hours for DNS propagation

**Why good:** Domain verification improves deliverability, prevents emails from landing in spam, required for production sending

---

### Pattern 3: React Email Package Structure (Monorepo)

Create a dedicated package for email templates in your monorepo.

#### Package Setup

```bash
# Create the emails package
mkdir -p packages/emails
cd packages/emails

# Initialize package
bun init

# Install dependencies
bun add @react-email/components resend
bun add -D react-email typescript @types/react
```

#### Package Configuration

```json
// packages/emails/package.json
{
  "name": "@repo/emails",
  "version": "0.1.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": {
    "dev": "email dev --port 3001",
    "preview": "email preview",
    "export": "email export --outDir dist"
  },
  "dependencies": {
    "@react-email/components": "^1.0.4",
    "resend": "^6.7.0"
  },
  "devDependencies": {
    "@types/react": "^19.0.0",
    "react-email": "^5.0.0",
    "typescript": "^5.0.0"
  }
}
```

**Why good:** Dedicated package enables reuse across apps, dev script starts preview server, separate from app code prevents bundling issues

#### Directory Structure

```
packages/emails/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts              # Export all templates
│   ├── client.ts             # Resend client singleton
│   ├── layouts/
│   │   └── base-layout.tsx   # Shared layout wrapper
│   ├── components/
│   │   ├── button.tsx        # Reusable button
│   │   ├── footer.tsx        # Email footer
│   │   └── header.tsx        # Email header
│   └── templates/
│       ├── verification-email.tsx
│       ├── password-reset.tsx
│       ├── welcome-email.tsx
│       └── notification.tsx
└── emails/                   # For react-email dev server
    └── (symlink to src/templates or copy)
```

</patterns>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `RESEND_API_KEY` environment variable for the server-side API key - NEVER hardcode secrets)**

**(You MUST verify your sending domain in Resend dashboard before production emails - unverified domains only allow sending to your own email)**

**(You MUST create email templates in a dedicated `packages/emails/` directory for monorepo - not inside the Next.js app)**

**(You MUST use `@react-email/components` for email components - external UI libraries like Material UI are NOT supported)**

**(You MUST configure the Resend SDK with appropriate region for your users - reduces delivery latency)**

**Failure to follow these rules will cause email delivery failures, security vulnerabilities, or bundling issues.**

</critical_reminders>

---

## Sources

- [Resend Next.js Documentation](https://resend.com/docs/send-with-nextjs)
- [React Email Documentation](https://react.email/docs)
- [React Email Monorepo Setup](https://react.email/docs/getting-started/monorepo-setup/npm)
- [React Email Tailwind Component](https://react.email/docs/components/tailwind)
- [Better Auth Email Configuration](https://www.better-auth.com/docs/concepts/email)
- [Resend + Better Auth Integration](https://resend.com/customers/better-auth)
- [Resend Error Handling](https://resend.com/docs/api-reference/errors)

---

**VERIFY ALL CRITICAL REQUIREMENTS BEFORE IMPLEMENTATION. RE-READ FILES AFTER EDITING TO CONFIRM CHANGES.**
