---
name: cloudflare-features
description: Configure and use Cloudflare integrations — Email Routing for the contact form, AI Gateway for media generation, Cloudflare Access for protected pages, and Image Transforms for on-the-fly image optimization. Use when the user mentions "email", "contact form", "AI gateway", "fal.ai", "cloudflare access", "protected pages", "JWT", "authentication", "image transforms", "cdn-cgi", or "cloudflare bindings".
---

# Cloudflare Features

Website Foundation integrates four Cloudflare services, all accessed through Worker bindings.

## Email Routing

Send emails from the contact form using the `SEND_EMAIL` binding. The `sendEmail()` function in `src/lib/email.ts` builds a MIME message and sends via `EmailMessage` from `cloudflare:email`. A honeypot field silently discards bot submissions.

See [email routing reference](references/email-routing.md).

## AI Gateway

Generate images and videos through Cloudflare AI Gateway, which proxies requests to fal.ai. The gateway handles API key management (BYOK — Bring Your Own Key configured in the dashboard). Access the gateway URL with:

```ts
const gatewayUrl = await env.AI.gateway(env.AI_GATEWAY_NAME).getUrl("fal");
```

**Important:** `getUrl()` is async — always `await` it.

See [AI Gateway reference](references/ai-gateway.md).

## Cloudflare Access

Protect pages and API routes with Cloudflare Access JWT verification. The `verifyAccessJwt()` function in `src/lib/access.ts` reads the `Cf-Access-Jwt-Assertion` header and verifies it against Cloudflare's JWKS endpoint using the `jose` library.

See [Access JWT reference](references/access-jwt.md).

## Image Transforms

Optimize images on-the-fly using Cloudflare's `/cdn-cgi/image/` endpoint. The `buildImageUrl()` function in `src/lib/cloudflare-image.ts` constructs transformation URLs with width, height, quality, format, and fit parameters.

**Important:** Image transforms only work on Cloudflare-served domains — they will 404 on localhost or non-CF domains.

## Accessing Bindings

```ts
// In API routes
const env = context.locals.runtime.env;

// In Astro pages
const env = Astro.locals.runtime.env;
```
