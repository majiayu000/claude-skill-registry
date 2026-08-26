---
name: add-mattermost
description: Add a self-hosted or cloud Mattermost bot channel through the Chat SDK bridge, reusing a local server when available and offering an evaluation server when none exists.
---

# Add Mattermost Channel

Adds Mattermost DMs, channels, threads, files, reactions, and interactive
approval cards. Messages arrive over Mattermost's WebSocket; card clicks return
to NanoClaw over an authenticated HTTP callback. Every step is safe to re-run.

## Discover the server first

Do this before installing the adapter or asking for a URL. The goal is to
reuse a healthy Mattermost the user already has and establish one canonical
base URL.

1. Check an existing `MATTERMOST_BASE_URL` in the current environment and
   NanoClaw env/config files. Do not print tokens or dump whole env files.
2. Probe likely local URLs, at least `http://localhost:8065` and
   `http://127.0.0.1:8065`, using `GET /api/v4/system/ping`. A listening port
   alone is not evidence that the service is Mattermost.
3. Inspect Docker/Compose for Mattermost containers. If a matching container
   exists but is stopped, offer to start it; do not start or recreate it
   without the user's approval.
4. If one healthy server is found, tell the user and use it. If multiple
   distinct servers are found, ask which one to use. Treat localhost and
   127.0.0.1 endpoints for the same container as one server and prefer the
   hostname in its configured Site URL; otherwise prefer `localhost`.
5. If nothing local is found, ask whether the user has a remote Mattermost.
   If not, offer the local evaluation installation in
   [LOCAL_SERVER.md](LOCAL_SERVER.md). Read that file only for local server
   discovery, repair, or installation.

Set `MATTERMOST_BASE_URL` to the chosen canonical URL (scheme included, no
trailing slash), then use that exact hostname in browser/Desktop setup. Do not
silently install Mattermost: it runs containers, binds a port, and persists
data, so show what will be created and get approval first.

## Apply

### 1. Detect the server

Probe a configured URL and the conventional local endpoints. The detector
always returns structured output: `found` binds `base_url`; `none` leaves it
for the guarded prompt below.

```nc:run capture:discovery=.discovery,base_url=.base_url effect:fetch
node .claude/skills/add-mattermost/scripts/discover-server.mjs
```

```nc:operator when:discovery=none
No healthy configured or local Mattermost server was detected. If you have a remote server, provide its URL next. Otherwise install the local evaluation server by following LOCAL_SERVER.md, then provide http://localhost:8065.
```

```nc:prompt base_url when:discovery=none normalize:rstrip-slash validate:^https?://[A-Za-z0-9._~:%/?#\[\]@!&()*+,;=-]+$
Mattermost base URL including the scheme, such as `https://mattermost.example.com`.
```

### 2. Copy and register the channel

Copy the canonical adapter and registration test from the `channels` branch.

```nc:copy from-branch:channels
src/channels/mattermost.ts
src/channels/mattermost-registration.test.ts
src/channels/mattermost-adapter/adapter.ts
src/channels/mattermost-adapter/format.ts
src/channels/mattermost-adapter/index.ts
src/channels/mattermost-adapter/rest.ts
src/channels/mattermost-adapter/thread-id.ts
src/channels/mattermost-adapter/types.ts
src/channels/mattermost-adapter/websocket.ts
```

Append the channel's single reach-in to the barrel, skipping it if present.

```nc:append to:src/channels/index.ts
import './mattermost.js';
```

Remove the unscoped `chat-adapter-mattermost` package when it is installed.
Nothing in this repository imports it: it is typosquat-shaped against the
scoped `@chat-adapter` family, so any copy in `package.json` is stale or
mistaken and would sit beside the audited implementation copied from the
`channels` branch.

```nc:run
if node -e "const p=require('./package.json'); process.exit(p.dependencies?.['chat-adapter-mattermost'] ? 0 : 1)"; then pnpm remove chat-adapter-mattermost; fi
```

Install the vendored adapter's direct WebSocket dependencies at the exact
supported versions.

```nc:dep
ws@8.21.3
@types/ws@8.18.1
```

### 3. Create and authenticate the bot

Tell the operator:

```nc:operator
Create a dedicated Mattermost bot:
1. As a System Admin, open System Console → Integrations → Bot Accounts and enable bot-account creation.
2. Create a bot such as `nanoclaw`, then copy the access token shown after creation.
3. Add the bot to every team and channel where it should receive messages. Bots do not join channels automatically.
4. Keep the token private. If it is lost, create a new token and deactivate the obsolete one after replacement.
```

```nc:prompt bot_token secret normalize:trim validate:^[A-Za-z0-9_-]{20,}$
Mattermost bot access token (20 or more letters, digits, underscores, or hyphens).
```

Confirm the credential and capture the bot identity. A failure means the URL,
token, or bot-account status is wrong.

```nc:run capture:bot_user_id=.id,bot_username=.username effect:fetch
curl -sf "{{base_url}}/api/v4/users/me" -H "Authorization: Bearer {{bot_token}}"
```

### 4. Configure authenticated card callbacks

Approvals require Mattermost itself—not the browser—to reach NanoClaw. Ask for
a URL routable from the Mattermost server. It may be NanoClaw's base URL or the
full `/webhook/mattermost` route; the adapter normalizes either form.

```nc:prompt callback_url normalize:rstrip-slash validate:^https?://.+
Callback URL reachable from Mattermost, such as `https://nanoclaw.example.com` or `http://host.docker.internal:3000/webhook/mattermost`.
```

Mattermost does not sign action callbacks. Generate a random shared secret for
the server-only callback context.

```nc:run capture:callback_secret effect:external validate:^[a-f0-9]{64}$
openssl rand -hex 32
```

Store the channel configuration. Existing keys remain unchanged on a re-run.

```nc:env-set
MATTERMOST_BASE_URL={{base_url}}
MATTERMOST_BOT_TOKEN={{bot_token}}
MATTERMOST_CALLBACK_URL={{callback_url}}
MATTERMOST_CALLBACK_SECRET={{callback_secret}}
```

Tell the operator:

```nc:operator
From the Mattermost server, verify the callback host is reachable. For a private host or Docker bridge name, add that hostname or IP under System Console → Environment → Developer → Allow untrusted internal connections. Use a publicly trusted HTTPS certificate in production.
```

### 5. Resolve the owner's DM

Ask for the Mattermost username that will own this NanoClaw installation.

```nc:prompt owner_username normalize:lower validate:^[a-z0-9][a-z0-9._-]{0,63}$
Your Mattermost username, without `@`.
```

Resolve that user and open the DM shared with the bot.

```nc:run capture:owner_user_id=.id effect:fetch
curl -sf "{{base_url}}/api/v4/users/username/{{owner_username}}" -H "Authorization: Bearer {{bot_token}}"
```

```nc:run capture:platform_id effect:fetch validate:^mattermost:[a-z0-9]{26}$
curl -sf -X POST "{{base_url}}/api/v4/channels/direct" -H "Authorization: Bearer {{bot_token}}" -H "Content-Type: application/json" -d '["{{owner_user_id}}","{{bot_user_id}}"]' | jq -er '"mattermost:" + .id'
```

The resolved `platform_id` and `owner_username` are used by
`/init-first-agent`. If an owner exists, use `/manage-channels` instead.

### 6. Build, test, and restart

Build the composed host to guard the typed Chat SDK bridge call and dependency.

```nc:run effect:build
pnpm run build
```

Run the registration test through the real channel barrel.

```nc:run effect:test
pnpm exec vitest run src/channels/mattermost-registration.test.ts
```

Restart NanoClaw so the channel and credentials load.

```nc:run effect:restart
bash setup/lib/restart.sh
```

## Next steps

For a first channel, continue with `/init-first-agent` using `mattermost`,
`{{platform_id}}`, and `{{owner_username}}`. Otherwise run `/manage-channels`.

Send the bot a DM and mention it in a joined channel. The first mention in an
unwired channel sends an approval card to the owner's bot DM. Approve it there;
NanoClaw replays the held message after creating the wiring.

Click a real approval card to verify callbacks. Success replaces the buttons
with the chosen result. An unsigned probe must return `401`:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' -X POST \
  -H 'content-type: application/json' -d '{}' \
  http://<nanoclaw-host>:3000/webhook/mattermost
```

## Channel information

- **type:** `mattermost`
- **platform ID:** `mattermost:<channel-id>` for channels and DMs
- **threads:** channel posts use optional Mattermost reply roots
- **group trigger:** mention-sticky, scoped per thread
- **DM trigger:** every message
- **unknown channels:** request owner approval
- **transport:** WebSocket inbound, REST outbound, HTTP action callbacks

## Troubleshooting

**The token check returns 401.** The token is stale, belongs to a deactivated
bot, or was pasted incorrectly. Create a replacement token and deactivate the
old token after the replacement works.

**The bot ignores a channel.** Add it to that team and channel. Membership
changes are observed, but restarting NanoClaw forces a fresh subscription.

**A new channel gets no immediate reply.** Check the owner's DM with the bot.
NanoClaw holds the first message behind a channel-approval card and deduplicates
later mentions until that card is resolved.

**Desktop messages appear only after a manual refresh.** This is usually the
Desktop client's WebSocket origin being rejected. Keep the Desktop server URL,
`MATTERMOST_BASE_URL`, and Mattermost `ServiceSettings.SiteURL` on the same
canonical hostname. Check server logs for `request origin not allowed`, and
verify `/api/v4/websocket` returns `101 Switching Protocols` for that Origin.
For a local server that genuinely needs both hostnames, persist a space-separated
`ServiceSettings.AllowCorsFrom` containing `http://localhost:8065` and
`http://127.0.0.1:8065`; do not use `*`. Preview images may regenerate
`config.json` on restart, so make the setting part of container startup rather
than relying on an in-container edit.

**Cards render but clicks do nothing.** From the Mattermost server, POST to the
callback URL. A `401` proves the path reaches NanoClaw; timeout or refusal means
routing or firewall failure. Mattermost logs report blocked hosts and TLS errors.

**The adapter repeatedly reconnects.** Confirm `/api/v4/websocket` supports
WebSocket upgrades through every reverse proxy and that idle connections live
longer than the adapter heartbeat.

**Messages arrive but no agent runs.** Inspect `ncl dropped-messages list` and
`ncl wirings list`. `no_agent_wired` means approval is pending or no wiring was
created; it is not an adapter failure.
