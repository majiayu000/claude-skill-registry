---
name: af-integrate-sentry
description: Integrate Sentry error tracking into projects with webhook-driven auto-fix agents. Use when setting up the SDK, configuring error alerts, analysing per-project errors, or building error dashboards.

title: Sentry Integration Expertise
created: 2026-03-03
updated: 2026-03-05
last_checked: 2026-03-05
tags: [skill, expertise, sentry, error-tracking, observability, webhooks]
parent: ../README.md
related:
  - ../af-audit-security/SKILL.md
---

# Sentry Integration Expertise

Directive knowledge for integrating Sentry error tracking into GainInsight projects, including SDK setup, webhook-driven auto-fix agent pipelines, and per-project configuration.

## When to Use This Skill

Load this skill when:
- Setting up Sentry SDK in a new project (Next.js, Node, React, Python)
- Configuring webhook integration for auto-fix agents (Holly pipeline)
- Managing Sentry internal integrations via API
- Configuring per-project error thresholds and auto-fix settings
- Troubleshooting webhook delivery, signature verification, or agent spawning
- Querying Sentry errors or issues via API

## Organisation

- **Org**: `gain-insight`
- **Region**: EU (Germany) — `de.sentry.io`
- **Team**: `gain-insight`
- **Dashboard**: `https://gain-insight.sentry.io`

## Rules (FOLLOW THESE)

### API Rules
1. **MUST use `de.sentry.io`** for all API calls — the org is EU-region hosted
2. **MUST use PAT from Doppler** (`doppler secrets get SENTRY_AUTH_TOKEN --project gi --config prd --plain`) — never the MCP token
3. **MUST NOT expose DSNs in logs** — they contain ingest keys
4. **MUST use `sentry.io`** (US endpoint) for internal integration CRUD — this is a Sentry API quirk

### Webhook Rules
5. **MUST verify HMAC-SHA256 signature** using `sentry-hook-signature` header and `crypto.timingSafeEqual()`
6. **MUST fail closed** — reject webhooks when secret is unset in production (`NODE_ENV=production`)
7. **MUST deduplicate** by `sentry_issue_id` — use a unique partial index excluding archived agents
8. **MUST handle race conditions** — catch unique constraint violations (PostgreSQL 23505) gracefully
9. **SHOULD use `async fetch()`** for all HTTP calls in webhook handlers — never `execFileSync('curl')`

### Configuration Rules
10. **MUST add `sentry` config to project's `config_json`** when enabling for a new project
11. **MUST set `enabled: true`** explicitly — missing config means disabled
12. **SHOULD set `min_count: 1`** for new projects to catch errors early
13. **SHOULD default `min_level` to `error`** — only `error` and `fatal` spawn agents
14. **MUST set `auto_fix: false`** for alert-only mode (Linear issue created but no agent spawned)

### SDK Rules
15. **MUST install platform-specific SDK** (e.g., `@sentry/nextjs`, `@sentry/node`, `@sentry/react`)
16. **SHOULD enable Session Replay** on client-side (10% normal, 100% on error)
17. **SHOULD follow the Andon pattern** for Next.js SDK integration (see Workflows)

---

## Quick Reference

### Webhook Pipeline

```
Sentry Issue → Webhook (HMAC-SHA256) → Coordinator → Filter → Linear Issue → Agent Spawn
```

### Severity Levels

| Level | Value | Default Action |
|-------|-------|----------------|
| `debug` | 0 | Ignored |
| `info` | 1 | Ignored |
| `warning` | 2 | Ignored |
| `error` | 3 | Spawn agent (if enabled) |
| `fatal` | 4 | Spawn agent (Urgent priority) |

Unknown levels default to 0 (never trigger unless threshold is `debug`).

### Per-Project Config Schema

```json
{
  "sentry": {
    "enabled": true,
    "project_slug": "my-project",
    "min_level": "error",
    "min_count": 1,
    "auto_fix": true
  }
}
```

Store in `projects.config_json` column.

### Linear Priority Mapping

| Sentry Level | Linear Priority |
|-------------|-----------------|
| `fatal` | 1 (Urgent) |
| `error` | 2 (High) |
| Other | 2 (High) |

### Default Assignee

Sentry-created Linear issues are auto-assigned to **Andy Davidson** (`4ea0cf3c-49f4-42a6-ab7d-01f2c95af853`) by default. This is set via `SENTRY_DEFAULT_ASSIGNEE_ID` in the coordinator's `watcher.ts`. The `createSentryLinearIssue` function accepts an optional `assigneeId` parameter to override per-call.

---

## Workflows

### Workflow: SDK Setup (Next.js)

**When:** Adding Sentry to a new Next.js project

**Steps:**
1. Install SDK: `npm install @sentry/nextjs`
2. Create files:
   - `next.config.ts` — Wrap with `withSentryConfig`
   - `instrumentation.ts` — Server/edge init with DSN
   - `instrumentation-client.ts` — Client init with replay (10% normal, 100% error)
   - `src/app/global-error.tsx` — Error boundary component
3. Get DSN via API:
   ```bash
   curl -s -H "Authorization: Bearer ${SENTRY_TOKEN}" \
     "https://de.sentry.io/api/0/projects/gain-insight/{slug}/keys/"
   ```
4. Hardcode DSN in instrumentation files (not env var — it's public and baked at build time)
5. Set webpack config: `org: "gain-insight"`, `project: "{slug}"`
6. Test: throw a test error, verify it appears in Sentry dashboard

**Success criteria:**
- Errors appear in Sentry dashboard within 30 seconds
- Source maps upload correctly
- Session replay captures user interactions

---

### Workflow: Enable Webhook Auto-Fix for a Project

**When:** Connecting an existing Sentry project to the Holly auto-fix pipeline

**Steps:**
1. Ensure Sentry internal integration exists with correct webhook URL
2. Update project config in database:
   ```sql
   UPDATE projects SET config_json = jsonb_set(
     COALESCE(config_json, '{}'),
     '{sentry}',
     '{"enabled": true, "project_slug": "my-slug", "min_level": "error", "min_count": 1, "auto_fix": true}'
   ) WHERE project_key = 'my-project';
   ```
3. Verify via dashboard status endpoint: `GET /api/sentry/status`
4. Test with dry-run: `POST /api/sentry/test-webhook` with project slug
5. Verify test creates Linear issue and spawns agent (or dry-run passes all checks)

**Success criteria:**
- Status endpoint shows project with `enabled: true`
- Test webhook creates Linear issue with correct priority
- Agent spawns with `workflow_type: 'sentry-fix'`

---

### Workflow: Create Internal Integration (API)

**When:** Setting up the webhook receiver for the first time or rotating secrets

**Steps:**
1. Create integration via US endpoint (Sentry API quirk):
   ```bash
   SENTRY_TOKEN=$(doppler secrets get SENTRY_AUTH_TOKEN --project gi --config prd --plain)
   curl -s -X POST \
     -H "Authorization: Bearer ${SENTRY_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Holly Agent Integration",
       "scopes": ["event:read"],
       "events": ["issue"],
       "webhookUrl": "https://{coordinator-host}/webhooks/sentry",
       "isInternal": true,
       "verifyInstall": false
     }' \
     "https://sentry.io/api/0/sentry-apps/"
   ```
2. Save `clientSecret` from response as `SENTRY_WEBHOOK_SECRET`
3. Store secret in Doppler and AWS Secrets Manager
4. Force-redeploy coordinator to pick up new secret
5. Verify: send test webhook, expect 200 (not 401)

**Success criteria:**
- Integration appears in Sentry Settings > Developer Settings
- Webhook receives valid HMAC signatures
- Coordinator verifies signatures and processes events

---

### Workflow: Troubleshoot Webhook Delivery

**When:** Webhooks are not being processed or returning errors

**Steps:**
1. Check integration exists: `GET https://de.sentry.io/api/0/sentry-apps/`
2. Check webhook URL is correct in integration settings
3. Verify ALB/proxy routing: webhook path (`/webhooks/sentry`) must route to coordinator port (not API server)
4. Verify secret matches: compare Doppler/Secrets Manager value with integration's `clientSecret`
5. Check coordinator logs for signature verification errors
6. Send manual test with valid HMAC:
   ```bash
   SECRET="..."; BODY='{"action":"created","data":{...}}'
   SIG=$(echo -n "$BODY" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')
   curl -X POST -H "Content-Type: application/json" \
     -H "sentry-hook-signature: $SIG" \
     -d "$BODY" "https://{coordinator-host}/webhooks/sentry"
   ```
7. Check response: 200 = processed, 401 = bad signature, 500 = handler error

**Success criteria:**
- Webhook returns 200 with `{"handled": true}` or `{"handled": false, "reason": "..."}`
- Reason messages explain filtering decisions clearly

---

## Database Schema

### Required Columns (tasks table)

```sql
ALTER TABLE tasks ADD COLUMN sentry_issue_id TEXT;
ALTER TABLE tasks ADD COLUMN sentry_event_id TEXT;
```

### Dedup Index

```sql
CREATE UNIQUE INDEX idx_tasks_sentry_dedup
  ON tasks (sentry_issue_id)
  WHERE sentry_issue_id IS NOT NULL
    AND agent_status NOT IN ('archived');
```

Prevents duplicate active agents for the same Sentry issue. Archived agents don't count.

---

## Environment Variables

| Variable | Location | Purpose |
|----------|----------|---------|
| `SENTRY_AUTH_TOKEN` | Doppler `gi/prd` | Full-access PAT for API operations |
| `SENTRY_DSN` | Per-project Doppler | Error tracking ingest endpoint |
| `SENTRY_WEBHOOK_SECRET` | Doppler + AWS SM | HMAC signature verification |

---

## Essential Reading

- [Sentry Developer Docs: Internal Integrations](https://docs.sentry.io/organization/integrations/integration-platform/internal-integration/)
- [Sentry Webhook Events](https://docs.sentry.io/organization/integrations/integration-platform/webhooks/)
- [af-audit-security](../af-audit-security/SKILL.md) — Related security patterns

---

**Remember:**
1. EU region = `de.sentry.io` for API, but `sentry.io` for integration CRUD
2. Webhook secret comes from integration's `clientSecret`, not a separate API key
3. Always verify HMAC with `timingSafeEqual` — never string comparison
4. Fatal = Urgent priority, everything else = High
5. Unknown severity levels default to 0 (safest default)
6. Dedup by `sentry_issue_id` with partial unique index excluding archived agents
