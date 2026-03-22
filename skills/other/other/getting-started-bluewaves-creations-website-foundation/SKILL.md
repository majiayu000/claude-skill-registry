---
name: getting-started
description: Set up the Website Foundation template from scratch — install dependencies, configure Cloudflare services, set secrets, and deploy. Use when the user says "set up", "get started", "first deploy", "configure cloudflare", "install", "clone", "initial setup", or "how do I start".
---

# Getting Started

Guide users through the complete first-run setup of the Website Foundation template.

## Prerequisites

- Node.js 18+ and [Bun](https://bun.sh) installed
- A Cloudflare account (free tier works)
- Wrangler CLI authenticated (`bunx wrangler login`)

## Setup Steps

1. **Clone and install** — Clone the repository and run `bun install`
2. **Create local env file** — Copy `.dev.vars.example` to `.dev.vars` and fill in values
3. **Start dev server** — Run `bun run dev` to start at `localhost:4321`
4. **Configure wrangler.jsonc** — Set `name` to your project name, change `destination_address` in `send_email` to your verified email
5. **Configure Cloudflare services** — See [Cloudflare setup guide](references/cloudflare-setup.md)
6. **Set production secrets** — Run `bunx wrangler secret put <KEY>` for each secret listed in [secrets reference](references/secrets-reference.md)
7. **Update site URL** — Change `site` in `astro.config.mjs` from `https://example.com` to your actual domain
8. **Deploy** — Run `bun run deploy` (builds then deploys via wrangler)

## Local Development

The dev server uses `platformProxy` to simulate Cloudflare bindings locally. Secrets are read from `.dev.vars` (gitignored). The AI Gateway binding requires a real Cloudflare account even locally.

## Verification

After setup, confirm:
- `bun run dev` starts without errors
- `bun run check` has no TypeScript errors
- `bun run test` passes all 42 tests
- `bun run build` succeeds
