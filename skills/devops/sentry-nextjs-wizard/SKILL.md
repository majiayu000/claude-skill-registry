---
name: sentry-nextjs-wizard
description: Setup Sentry in Next.js using the wizard CLI. Use when asked to add Sentry to Next.js, install @sentry/nextjs, or configure error monitoring for Next.js apps.
---

# Sentry Next.js Wizard

Install and configure Sentry in Next.js projects using the official wizard CLI.

## Invoke This Skill When

- User asks to "add Sentry to Next.js" or "install Sentry" and the project is a Next.js project
- User wants monitoring, logging, metrics, or traces in Next.js
- User mentions using "Sentry wizard" or "@sentry/nextjs" in their project

## Headless Setup (Recommended for Agents)

```bash
npx @sentry/wizard@latest -i nextjs \
  --skip-auth \
  --tracing \
  --replay \
  --logs \
  --ignore-git-changes \
  --disable-telemetry
```

### CLI Flags

| Flag | Description |
|------|-------------|
| `--skip-auth` | Skip authentication, use env var placeholders |
| `--tracing` | Enable performance monitoring |
| `--replay` | Enable Session Replay |
| `--logs` | Enable Sentry Logs |
| `--tunnel-route` | Route requests through Next.js server (ad-blocker bypass) |
| `--example-page` | Create test page at `/sentry-example-page` |
| `--mcp <providers>` | Add MCP config: `cursor`, `vscode`, `claude`, `opencode`, `jetbrains` |
| `--ignore-git-changes` | Skip dirty repo warning |
| `--disable-telemetry` | Don't send telemetry |

### Example with MCP

```bash
npx @sentry/wizard@latest -i nextjs \
  --skip-auth \
  --tracing \
  --replay \
  --logs \
  --mcp opencode \
  --ignore-git-changes \
  --disable-telemetry
```

## Files Created

| File | Purpose |
|------|---------|
| `sentry.server.config.ts` | Server-side init |
| `sentry.edge.config.ts` | Edge runtime init |
| `instrumentation-client.ts` | Client-side init |
| `instrumentation.ts` | Next.js instrumentation hook |
| `next.config.js` | Modified with `withSentryConfig` |
| `global-error.tsx` | App Router error boundary |
| `.env.example` | Required env vars (headless mode) |

## Environment Variables

After headless setup, create `.env.local` from `.env.example`:

```bash
NEXT_PUBLIC_SENTRY_DSN=https://xxx@o123.ingest.sentry.io/456
SENTRY_ORG=my-org
SENTRY_PROJECT=my-project
SENTRY_AUTH_TOKEN=sntrys_xxx
```

**Get credentials from:**
- DSN: Project Settings > Client Keys
- Org/Project slug: URL path on sentry.io
- Auth Token: Organization Settings > Auth Tokens

## Verification

```bash
npm run build  # Check for errors
npm run dev    # Start dev server
# Visit /sentry-example-page (if --example-page used)
# Check Sentry dashboard for test error
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Node version error | Requires Node.js 18.20.0+ |
| Package install hangs | Add `--force-install` |
| Git dirty warning | Add `--ignore-git-changes` |
| Source maps not uploading | Verify `SENTRY_AUTH_TOKEN` is set |

## Post-Setup: Project Configuration via MCP

After wizard completes, check if Sentry MCP can auto-configure the project:

```
mcp: sentry_list_projects
```

**If MCP has create_project capability:**
```
mcp: sentry_create_project
  name: "[project-name]"
  platform: "javascript-nextjs"
```

Then update configuration files with the returned DSN automatically.

**If MCP lacks create_project capability**, advise the user:

> Your Sentry MCP connection doesn't have project creation permissions. You can either:
> 1. **Re-authenticate MCP** with expanded scopes to enable automatic project creation
> 2. **Manually create the project** at sentry.io and update the configuration files below

### Files Requiring DSN/Project Configuration

| File | What to Update |
|------|----------------|
| `.env.local` | Set `NEXT_PUBLIC_SENTRY_DSN`, `SENTRY_ORG`, `SENTRY_PROJECT`, `SENTRY_AUTH_TOKEN` |
| `sentry.server.config.ts` | Verify `dsn` if hardcoded (prefer env var) |
| `sentry.edge.config.ts` | Verify `dsn` if hardcoded (prefer env var) |
| `instrumentation-client.ts` | Verify `dsn` if hardcoded (prefer env var) |

### Manual Project Creation Steps

1. Go to **sentry.io > Create Project**
2. Select **Next.js** platform
3. Copy the DSN from project settings
4. Create `.env.local` with credentials (see Environment Variables above)
