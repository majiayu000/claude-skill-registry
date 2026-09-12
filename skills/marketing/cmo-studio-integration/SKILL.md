---
name: cmo-studio-integration
description: When mktg-studio is running on this machine, /cmo proactively narrates work into the dashboard via Bash + curl against the localhost HTTP API. Detect via /api/health, then log every meaningful action — the user sees what /cmo is doing in real time.
---

# /cmo ↔ mktg-studio integration

`mktg-studio` is the local dashboard that visualises everything you do.
When it's running, the user has a browser open at `http://localhost:3000`
showing primary surfaces (Pulse, Signals, Publish, Brand) and an Activity
panel on the right. Trend radar lives inside Signals. Audience summary and
recommended next actions live inside Pulse.

This skill teaches you to drive that dashboard without being asked. No
SDKs. No special tools. Every action is a `curl` you already know how to
write.

## 1. Detect first

On every turn, before doing anything else marketing-y, run:

```bash
STUDIO=${STUDIO_BASE:-http://localhost:3001}
curl -fsS -m 2 "$STUDIO/api/health" >/dev/null 2>&1 && STUDIO_UP=1 || STUDIO_UP=0
```

- `STUDIO_UP=1` → studio is up, follow the rules below
- `STUDIO_UP=0` → studio is down, behave exactly as you would in a
  CLI-only setup. Don't surface the unreachable studio to the user — they
  probably don't have it open.

Cache the result for the rest of the turn — don't hammer health.

If you want to confirm the wire shapes you're about to send, fetch the
schema once per session (it's static):

```bash
curl -fsS "$STUDIO/api/schema" | jq '.routes[].path'
curl -fsS "$STUDIO/api/schema?route=/api/activity/log" | jq
curl -fsS "$STUDIO/api/help" | jq '.data.entryPoints'
```

## 2. The five verbs

Every meaningful action you take should map to one or more of these
endpoints. Skip them when they don't apply — don't be noisy.

| Verb | Endpoint | Call when |
|------|----------|-----------|
| **Log** | `POST /api/activity/log` | After running any skill, writing a brand file, sending a publish, calling out errors. One entry per discrete action. |
| **Note** | `POST /api/brand/note` *or* `POST /api/brand/write` | When you've created or edited a `brand/*.md` file. `/write` is the agent-native path (lock-protected); `/note` is the lightweight "fyi I edited this externally" path. |
| **Push** | `POST /api/opportunities/push` | When your analysis surfaces a recommended next action. Set `priority` 0-100 — be honest about urgency. |
| **Toast** | `POST /api/toast` | Inline confirmations the user should see immediately. `level: "success" \| "info" \| "warn" \| "error"`. |
| **Navigate** | `POST /api/navigate` | When the result of your work lives on a specific surface and you want the user to look there. Valid tabs: `pulse`, `signals`, `publish`, `brand`. Use `{"tab":"signals"}` for Trend radar (`filter.mode` is dropped server-side; do not send it). Example: after `landscape-scan` finishes, switch to Signals/Trend radar; after `brand-voice` or `voice-extraction`, switch to `brand`. |

### Copy-paste recipes

```bash
# Log a skill run
curl -fsS -X POST "$STUDIO/api/activity/log" \
  -H 'content-type: application/json' \
  -d '{"kind":"skill-run","skill":"landscape-scan","summary":"Refreshed landscape, 5 new claims","filesChanged":["brand/landscape.md"]}'

# Note a brand-file write (excerpt is the first ~800 chars)
EXCERPT=$(head -c 800 brand/voice-profile.md | jq -Rs .)
curl -fsS -X POST "$STUDIO/api/brand/note" \
  -H 'content-type: application/json' \
  -d "{\"file\":\"brand/voice-profile.md\",\"excerpt\":$EXCERPT}"

# Push an opportunity
curl -fsS -X POST "$STUDIO/api/opportunities/push" \
  -H 'content-type: application/json' \
  -d '{"skill":"keyword-research","reason":"You have a landscape but no keyword-plan yet — that gates seo-content","priority":80}'

# Toast
curl -fsS -X POST "$STUDIO/api/toast" \
  -H 'content-type: application/json' \
  -d '{"level":"success","message":"Landscape refreshed — see Trend radar"}'

# Navigate
curl -fsS -X POST "$STUDIO/api/navigate" \
  -H 'content-type: application/json' \
  -d '{"tab":"signals"}'
```

## 3. Brand files are first-class

Writing a brand file directly with the Write tool works but doesn't
update the studio. Prefer the HTTP path:

```bash
# 1. Read current content + grab the mtime for optimistic locking
RES=$(curl -fsS "$STUDIO/api/brand/read?file=voice-profile.md")
MTIME=$(echo "$RES" | jq -r '.data.mtime')

# 2. Build new content in-memory (your editing logic here)
CONTENT=$(jq -Rs . < new-voice-profile.md)

# 3. Atomic write — fires brand-file-changed SSE so dependent tabs refresh
curl -fsS -X POST "$STUDIO/api/brand/write" \
  -H 'content-type: application/json' \
  -d "{\"file\":\"voice-profile.md\",\"content\":$CONTENT,\"expectedMtime\":\"$MTIME\"}"

# 4. Log the activity
curl -fsS -X POST "$STUDIO/api/activity/log" \
  -H 'content-type: application/json' \
  -d '{"kind":"brand-write","filesChanged":["brand/voice-profile.md"],"summary":"Made the voice more casual — 3 anchor sentences swapped"}'
```

If the user edited the same file in their text editor while you were
writing, the `expectedMtime` mismatch returns `409 CONFLICT` with a `fix`
hint pointing back to `/api/brand/read` to re-fetch + merge.

If you need to re-research a brand file, queue the owning skill:

```bash
curl -fsS -X POST "$STUDIO/api/brand/regenerate" \
  -H 'content-type: application/json' \
  -d '{"file":"landscape.md"}'
# → { ok: true, data: { jobId, skill, file } }
# poll via curl -fsS "$STUDIO/api/jobs/<jobId>" or watch /api/events
```

## 4. The idiomatic turn

A typical /cmo turn that runs a skill, writes a brand file, and
recommends a next action:

```bash
STUDIO=${STUDIO_BASE:-http://localhost:3001}
curl -fsS -m 2 "$STUDIO/api/health" >/dev/null || exit 0   # 1. detect

curl -fsS -X POST "$STUDIO/api/activity/log" -H 'content-type: application/json' \
  -d '{"kind":"skill-run","skill":"landscape-scan","summary":"Refreshing landscape from 18 sources"}'

# 2. (do the actual work — Exa search, write brand/landscape.md)

EXCERPT=$(head -c 800 brand/landscape.md | jq -Rs .)
curl -fsS -X POST "$STUDIO/api/brand/note" -H 'content-type: application/json' \
  -d "{\"file\":\"brand/landscape.md\",\"excerpt\":$EXCERPT}"

curl -fsS -X POST "$STUDIO/api/activity/log" -H 'content-type: application/json' \
  -d '{"kind":"skill-run","skill":"landscape-scan","summary":"Done — 5 new claims, 2 deprecated","filesChanged":["brand/landscape.md"]}'

curl -fsS -X POST "$STUDIO/api/opportunities/push" -H 'content-type: application/json' \
  -d '{"skill":"competitor-alternatives","reason":"Fresh landscape — write 3 X vs Y pages","priority":75}'

curl -fsS -X POST "$STUDIO/api/navigate" -H 'content-type: application/json' \
  -d '{"tab":"signals"}'

curl -fsS -X POST "$STUDIO/api/toast" -H 'content-type: application/json' \
  -d '{"level":"success","message":"Landscape refreshed — see Trend radar"}'
```

Eight calls. Each one is fire-and-forget, returns under 50ms, and the
dashboard updates in real time via SSE. The user watches the work happen.

## 5. Don't break

- Every endpoint returns `{ok: true, ...}` or `{ok: false, error: {code, message, fix?}}`. Predictable envelope.
- **Three documented exceptions** return bare tab-shaped objects (no `ok`/`data` wrapper): `GET /api/opportunities`, `GET /api/audience/profiles`, `GET /api/briefs`. Treat a 200 with the expected top-level keys (`opportunities`, `profiles`, `briefs`) as success; don't look for `.ok` on these three.
- On connection failure (studio down), proceed as if the dashboard didn't exist. Don't retry.
- On `{ok: false}` with a `fix` field, surface or follow it — it's agent-actionable by design.
- `/api/navigate` and `/api/toast` are SSE-only (no DB write). Spamming them is harmless but ugly. Send one navigate per logical destination change, one toast per user-facing milestone.
- All mutating endpoints accept `?dryRun=true` — append it during development to validate request shape without side effects.

## 6. What NOT to do

- Don't `POST /api/navigate` between every step of a multi-skill playbook — switch tabs once, at the end, when the user should look at the result.
- Don't `POST /api/toast` for routine logs — that's what `/api/activity/log` is for. Toasts are for things the user should drop everything and notice.
- Don't try to `POST /api/brand/write` outside `brand/*.md` — the path validator rejects everything else with `BAD_INPUT`.
- Don't fetch `/api/schema` more than once per session — the wire shape is static within a server boot.

## Reference

- Full HTTP contract with copy-pasteable curls: `docs/cmo-integration.md`
- Endpoint shapes (live, runtime-introspectable): `GET /api/schema`, `GET /api/help`
- 5-minute reproducible demo: `docs/DEMO.md`
