---
name: environment-configuration
description: Environment variables, setup procedures, API configurations, and security for the omer-akben portfolio. Use when setting up the project, configuring services, or troubleshooting environment issues.
---

# Environment Configuration Skill

## Quick Setup

```bash
# Clone and install
git clone <repo-url>
cd omer-akben
npm install

# Copy environment template
cp .env.example .env

# Configure required environment variables (see below)

# Run development server
npm run dev
```typescript

## Required Environment Variables

### Core Services

```bash
# AI Models (Primary: XAI Grok)
XAI_API_KEY=your-xai-api-key
XAI_REASONING_MODEL=grok-4-fast-reasoning
XAI_NON_REASONING_MODEL=grok-4-fast-non-reasoning

# AI Models (Fallback: OpenAI)
OPENAI_API_KEY=your-openai-api-key
OPENAI_FALLBACK_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```typescript

### Email Service (Resend)

```bash
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=noreply@omerakben.com
```typescript

### Rate Limiting & Caching (Upstash Redis)

```bash
UPSTASH_REDIS_REST_URL=https://your-redis-url.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-redis-token
```typescript

### Episodic Memory (Upstash Vector)

```bash
UPSTASH_VECTOR_REST_URL=https://your-vector-url.upstash.io
UPSTASH_VECTOR_REST_TOKEN=your-vector-token
```typescript

### Analytics (PostHog)

```bash
NEXT_PUBLIC_POSTHOG_KEY=your-posthog-key
NEXT_PUBLIC_POSTHOG_HOST=https://us.i.posthog.com
```typescript

### Error Tracking (Sentry)

```bash
SENTRY_AUTH_TOKEN=your-sentry-auth-token
NEXT_PUBLIC_SENTRY_DSN=your-sentry-dsn
```typescript

### Cron Security (Vercel)

```bash
CRON_SECRET=your-random-secret-key
```typescript

## Service Setup Guides

### XAI Grok Setup

1. Visit <https://console.x.ai/>
2. Create API key
3. Add to `.env` as `XAI_API_KEY`
4. Models: `grok-4-fast-reasoning`, `grok-4-fast-non-reasoning`

**Pricing:** $2/M input tokens, $10/M output tokens

### OpenAI Setup (Fallback)

1. Visit <https://platform.openai.com/>
2. Create API key
3. Add to `.env` as `OPENAI_API_KEY`
4. Models: `gpt-4o-mini`, `text-embedding-3-small`

**Pricing:** $0.15/M input tokens, $0.60/M output tokens

### Upstash Redis Setup

1. Visit <https://console.upstash.com/>
2. Create Redis database
3. Copy REST URL and token to `.env`
4. Used for: Rate limiting, caching

**Free Tier:** 10,000 commands/day

### Upstash Vector Setup

1. Visit <https://console.upstash.com/>
2. Create Vector index (1536 dimensions for OpenAI embeddings)
3. Copy REST URL and token to `.env`
4. Used for: Episodic memory search

**Free Tier:** 10,000 queries/month

### Resend Email Setup

1. Visit <https://resend.com/>
2. Add and verify sending domain
3. Create API key
4. Add to `.env` as `RESEND_API_KEY` and `RESEND_FROM_EMAIL`

**Free Tier:** 3,000 emails/month

### PostHog Analytics Setup

1. Visit <https://posthog.com/>
2. Create project
3. Copy project API key
4. Add to `.env` as `NEXT_PUBLIC_POSTHOG_KEY`

**Free Tier:** 1M events/month

### Sentry Error Tracking Setup

1. Visit <https://sentry.io/>
2. Create Next.js project
3. Copy DSN and auth token
4. Add to `.env`
5. Configure in `sentry.*.config.ts` files

**Free Tier:** 5,000 errors/month

## Environment Validation

### Check Required Variables

```typescript
// Runtime validation
const requiredEnvVars = [
  'XAI_API_KEY',
  'OPENAI_API_KEY',
  'UPSTASH_REDIS_REST_URL',
  'UPSTASH_REDIS_REST_TOKEN',
  'RESEND_API_KEY',
];

requiredEnvVars.forEach((varName) => {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
});
```typescript

### Test Environment Setup

```bash
# Test AI models
curl https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"grok-4-fast-reasoning","messages":[{"role":"user","content":"test"}]}'

# Test Redis connection
curl $UPSTASH_REDIS_REST_URL/ping \
  -H "Authorization: Bearer $UPSTASH_REDIS_REST_TOKEN"

# Test email sending
npm run test:email
```typescript

## Configuration Patterns

### AI Model Configuration

**Centralized Config:** `src/lib/ai/model-config.ts`

```typescript
export const AI_MODEL_CONFIG = {
  primary: {
    provider: "xai",
    models: {
      reasoning: process.env.XAI_REASONING_MODEL || "grok-4-fast-reasoning",
      nonReasoning: process.env.XAI_NON_REASONING_MODEL || "grok-4-fast-non-reasoning",
    },
  },
  fallback: {
    provider: "openai",
    model: process.env.OPENAI_FALLBACK_MODEL || "gpt-4o-mini",
  },
  embedding: {
    provider: "openai",
    model: process.env.OPENAI_EMBEDDING_MODEL || "text-embedding-3-small",
  },
};
```typescript

### Usage

```typescript
import { PRIMARY_REASONING_MODEL } from "@/lib/ai/model-config";

const result = await generateWithFallback({
  model: PRIMARY_REASONING_MODEL,
  messages: [{ role: "user", content: prompt }],
});
```typescript

### Rate Limiting Configuration

**Location:** `src/lib/rate-limit.ts`

```typescript
export const rateLimits = {
  collectContact: {
    limit: 1,           // 1 request
    window: 86400,      // per 24 hours
  },
  chat: {
    limit: 100,         // 100 requests
    window: 3600,       // per hour
  },
};
```typescript

### Feature Flags

```typescript
export const features = {
  episodicMemory: !!process.env.UPSTASH_VECTOR_REST_URL,
  emailNotifications: !!process.env.RESEND_API_KEY,
  analytics: !!process.env.NEXT_PUBLIC_POSTHOG_KEY,
  errorTracking: !!process.env.NEXT_PUBLIC_SENTRY_DSN,
};
```typescript

## Security Best Practices

### API Key Management

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use environment-specific keys** - Different keys for dev/staging/prod
3. **Rotate keys regularly** - Especially after team member changes
4. **Use read-only keys** - When write access not needed

### Server-Side API Calls Only

```typescript
// ✅ GOOD: Server-side API route
export async function POST(request: Request) {
  const apiKey = process.env.XAI_API_KEY; // Secure
  // Make API call
}

// ❌ BAD: Client-side API call
const response = await fetch("/api/external", {
  headers: { "X-API-Key": process.env.XAI_API_KEY }, // Exposed!
});
```typescript

### Input Validation

```typescript
import { z } from "zod";

const inputSchema = z.object({
  email: z.string().email(),
  message: z.string().max(1000),
});

// Validate all inputs
const validated = inputSchema.parse(input);
```typescript

### Rate Limiting

```typescript
import { ratelimit } from "@/lib/rate-limit";

const result = await ratelimit.limit(ip);
if (!result.success) {
  return new Response("Rate limit exceeded", { status: 429 });
}
```typescript

## Vercel Deployment Configuration

### Environment Variables in Vercel

1. Go to Project Settings → Environment Variables
2. Add all variables from `.env.example`
3. Set appropriate scope (Production, Preview, Development)
4. Use Vercel CLI for bulk import: `vercel env pull`

### Vercel Cron Configuration

**File:** `vercel.json`

```json
{
  "crons": [
    {
      "path": "/api/cron/cleanup-memory",
      "schedule": "0 3 * * 0"
    }
  ]
}
```typescript

**Security:** Endpoint validates `CRON_SECRET` header

## Troubleshooting

### Common Issues

**Issue:** "Missing environment variable: XAI_API_KEY"
**Fix:** Ensure `.env` file exists and contains `XAI_API_KEY`

**Issue:** "Redis connection failed"
**Fix:** Check `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` are correct

**Issue:** "Rate limit exceeded"
**Fix:** Redis not configured - add Upstash Redis credentials

**Issue:** "Email sending failed"
**Fix:** Verify `RESEND_API_KEY` and sending domain is verified

### Debug Mode

```bash
# Enable verbose logging
NODE_ENV=development npm run dev

# Check environment variables
node -e "console.log(process.env.XAI_API_KEY ? 'XAI_API_KEY set' : 'XAI_API_KEY missing')"
```typescript

## Local Development Setup

```bash
# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run development server
npm run dev

# In another terminal, run tests
npm test -- --watch
```typescript

## Production Checklist

Before deploying to production:

- [ ] All required environment variables set in Vercel
- [ ] API keys are production keys (not development keys)
- [ ] Rate limiting configured (Redis credentials set)
- [ ] Email sending configured (Resend verified domain)
- [ ] Analytics configured (PostHog project key)
- [ ] Error tracking configured (Sentry DSN)
- [ ] Cron secret set for automated tasks
- [ ] Environment variables match `.env.example` template
