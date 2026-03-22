---
name: vercel-env-sync
description: >
  Sync environment variables from local .env to a Vercel project and trigger redeploy.
  Use this skill whenever the user wants to update Vercel env vars, fix a missing API key on
  production, sync .env to Vercel, redeploy after env changes, or says something like
  "update Vercel env", "add key to Vercel", "env not working on prod", "redeploy Vercel".
---

# Vercel Env Sync

Sync env vars from local `.env` to a Vercel project via the Vercel REST API, then trigger a redeploy.

## Step 1 — Find the working Vercel token

Read `.env` and extract all tokens starting with `vcp_`. Try each until one works:

```bash
curl -s -H "Authorization: Bearer <token>" "https://api.vercel.com/v9/projects?limit=5"
```

A working token returns `{"projects": [...]}`. An invalid one returns `{"error": {"invalidToken": true}}`.

> The .env may have multiple `vcp_` tokens (e.g. `VERCEL_TOKEN`, `vcp_...` raw lines). Try all of them.

## Step 2 — Find the project ID

From the projects list, match by `name` (e.g. `keyway-construction`). Save `project.id` (format: `prj_...`).

```bash
curl -s -H "Authorization: Bearer <TOKEN>" "https://api.vercel.com/v9/projects?limit=20" \
  | python3 -c "import sys,json; [print(p['id'], p['name']) for p in json.load(sys.stdin).get('projects',[])]"
```

Ask the user which project if ambiguous.

## Step 3 — List current Vercel env vars

```bash
curl -s "https://api.vercel.com/v9/projects/<PROJECT_ID>/env" \
  -H "Authorization: Bearer <TOKEN>" \
  | python3 -c "import sys,json; [print(e['id'], e['key']) for e in json.load(sys.stdin).get('envs',[])]"
```

This returns a list of `{id, key, value (encrypted)}`. Build a map of `key → [list of env ids]`.

## Step 4 — Parse .env and decide what to sync

Read `.env`. For each line matching `KEY=VALUE`:
- Skip keys that are git tokens or clearly not needed on Vercel:
  - `GIT_ACC_*`, `X_USERNAME`, `X_PASSWORD`, `X_AUTH_TOKEN`, `X_CT0`
  - `DATAIMPULSE_*`, `DATAFORSEO_*` (unless user says otherwise)
- Sync everything else: `RESEND_API_KEY`, `STRIPE_*`, `NEXT_PUBLIC_*`, `VERCEL_TOKEN`, `FIRECRAWL_*`, etc.

Show the user the list of keys you're about to sync and confirm before proceeding.

## Step 5 — Update or create each env var

**If key already exists (one entry):** PATCH to update the value:
```bash
curl -s -X PATCH \
  "https://api.vercel.com/v9/projects/<PROJECT_ID>/env/<ENV_ID>" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"value": "<VALUE>"}'
```

**If key has duplicates:** DELETE all but the first, then PATCH the remaining one:
```bash
# Delete duplicate
curl -s -X DELETE \
  "https://api.vercel.com/v9/projects/<PROJECT_ID>/env/<DUPLICATE_ID>" \
  -H "Authorization: Bearer <TOKEN>"

# Update the kept one
curl -s -X PATCH \
  "https://api.vercel.com/v9/projects/<PROJECT_ID>/env/<KEPT_ID>" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"value": "<VALUE>"}'
```

**If key doesn't exist yet:** POST to create:
```bash
curl -s -X POST \
  "https://api.vercel.com/v10/projects/<PROJECT_ID>/env" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"key":"<KEY>","value":"<VALUE>","type":"encrypted","target":["production","preview","development"]}'
```

> PATCH body only needs `{"value": "..."}` — do NOT include `target` in PATCH or you'll get a conflict error.

## Step 6 — Trigger redeploy

Get the latest deployment ID:
```bash
curl -s "https://api.vercel.com/v6/deployments?projectId=<PROJECT_ID>&limit=1" \
  -H "Authorization: Bearer <TOKEN>" \
  | python3 -c "import sys,json; d=json.load(sys.stdin)['deployments'][0]; print(d['uid'], d['url'])"
```

Trigger redeploy from that deployment:
```bash
curl -s -X POST \
  "https://api.vercel.com/v13/deployments?forceNew=1" \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"deploymentId":"<DEPLOYMENT_ID>","name":"<PROJECT_NAME>","target":"production"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('url','?'), d.get('state','?'))"
```

## Common errors

| Error | Fix |
|---|---|
| `invalidToken` | Try the next `vcp_` token from .env |
| `ENV_CONFLICT` | Key already exists with that target — use PATCH not POST |
| `bad_request: should NOT have additional property projectId` | Remove `projectId` from POST /deployments body |
| PATCH returns conflict | Don't include `target` in PATCH body, only `value` |

## Summary output

After completing, report:
- How many keys were synced (updated / created / skipped)
- Redeploy URL (e.g. `keyway-construction-xxx.vercel.app`)
- Whether the deployment is BUILDING or READY
