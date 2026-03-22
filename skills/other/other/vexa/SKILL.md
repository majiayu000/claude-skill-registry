---
name: vexa
description: "Send bots to Zoom, Google Meet, and Microsoft Teams meetings. Get live transcripts, recordings, and reports. Works with Vexa Cloud or your own self-hosted instance."
---

## Chat-oriented interactions

Speak **directly to the user** as in a natural chat. Do not output internal reasoning, plan summaries, or procedural notes ("I need to...", "According to the skill...", "I will inform..."). Reply with only what you would say to the user — conversational, warm, and to the point.

## Plain text formatting for meeting chat

When sending messages to meeting chat (Google Meet, Teams, etc.), **always use plain text** — no markdown. These chat surfaces do not render markdown, so asterisks, hash headers, backticks, and bullet dashes appear as ugly raw characters. Use line breaks and spacing for structure instead.

Use the bundled CLI:
- `node skills/vexa/scripts/vexa.mjs ...`
- `node skills/vexa/scripts/onboard.mjs ...`
- `node skills/vexa/scripts/ingest.mjs ...`
- `node skills/vexa/scripts/audit.mjs`

## Environment

**Required:** `VEXA_API_KEY` — get yours from https://vexa.ai/dashboard/api-keys

Set `VEXA_API_KEY` in your environment or create `skills/vexa/secrets/vexa.env` manually with:
```
VEXA_API_KEY=your_key_here
```

Optional: `VEXA_BASE_URL` (env override — takes priority over endpoint config)

### Endpoint switching (prod / local dev)

The CLI supports named endpoints stored in `secrets/vexa-endpoints.json`. Default endpoints: `prod` (https://api.cloud.vexa.ai) and `local` (http://localhost:8000).

- List endpoints & active env: `node skills/vexa/scripts/vexa.mjs env:list`
- Switch to local dev: `node skills/vexa/scripts/vexa.mjs env:use local`
- Switch to prod: `node skills/vexa/scripts/vexa.mjs env:use prod`
- Add custom endpoint: `node skills/vexa/scripts/vexa.mjs env:set staging --url https://staging.vexa.ai`
- Remove endpoint: `node skills/vexa/scripts/vexa.mjs env:remove staging`

Priority: `VEXA_BASE_URL` env var > `vexa-endpoints.json` active endpoint > default prod URL.

## Secrets-first check (before any onboarding)

**Always check first:** `node skills/vexa/scripts/onboard.mjs --check-secrets`

- If output is `{"secrets_ok": true}` → secrets exist. Skip onboarding. Use normal flows.
- If output is `{"secrets_ok": false}` → run onboarding. Load `references/onboarding-flow.md`.

**Webhook — proactive setup:** Whenever secrets exist and you're working with Vexa, run `node skills/vexa/scripts/onboard.mjs --check-webhook`. If `webhook_configured` is false, advise adding the vexa mapping (see `references/webhook-setup.md`). For onboarding-only details (webhook requirements, pipeline validation, mock webhook), load `references/onboarding-flow.md`.

**When secrets are missing:** Direct the user to get their key from https://vexa.ai/dashboard/api-keys and set it up themselves. They should either set `VEXA_API_KEY` in their environment or create `skills/vexa/secrets/vexa.env` manually with `VEXA_API_KEY=their_key_here`. Do not ask users to paste API keys in chat.

**Secrets location:** `skills/vexa/secrets/` holds env files and `vexa-state.json`. This dir is gitignored. When publishing the skill to ClawHub, ensure `secrets/` is excluded.

**Per-endpoint API keys:** The CLI supports separate env files per endpoint: `vexa-prod.env`, `vexa-local.env`, etc. When switching endpoints with `env:use`, the matching `vexa-<name>.env` is loaded automatically. Falls back to `vexa.env` if no endpoint-specific file exists.

Non-interactive (for scripting): `onboard.mjs --api_key <key> --persist yes --meeting_url "<url>" --language en --wait_seconds 60 --poll_every_seconds 10`

## Quick workflows

### 1) User drops a meeting link → send bot

- After successfully sending the bot, **proactively** run `--check-webhook`. If not configured, offer to set it up so finished meetings auto-trigger reports.
- Parse/normalize link (or pass explicit ID):
  - `node skills/vexa/scripts/vexa.mjs parse:meeting-url --meeting_url "https://meet.google.com/abc-defg-hij"`
- Start bot directly from URL:
  - `node skills/vexa/scripts/vexa.mjs bots:start --meeting_url "https://meet.google.com/abc-defg-hij" --bot_name "Claw" --language en`
  - `node skills/vexa/scripts/vexa.mjs bots:start --meeting_url "https://teams.live.com/meet/9387167464734?p=qxJanYOcdjN4d6UlGa" --bot_name "Claw" --language en`

### 2) Start bot from calendar meeting links

If a calendar tool/skill is available (for example `gog`):
1. Fetch upcoming events.
2. Extract meeting links (Google Meet/Teams).
3. For each selected event, call `bots:start --meeting_url ...`.
4. Optionally save event title into Vexa metadata:
   - `meetings:update --name "<calendar title>" --notes "source: calendar"`

### 3) Read transcript during meeting or after meeting

- Poll current transcript:
  - `node skills/vexa/scripts/vexa.mjs transcripts:get --platform google_meet --native_meeting_id abc-defg-hij`
- For near real-time streaming, use Vexa WebSocket API (see `references/user-api-guide-notes.md` for endpoints and notes).
- After transcript is available, summarize and store key updates.

### 4) Stop bot

- `node skills/vexa/scripts/vexa.mjs bots:stop --meeting_url "<url>"`

### 5) Create meeting report (after meeting finished)

After stopping the bot (or once the meeting has ended and transcript is finalized), create a basic meeting report:

- `node skills/vexa/scripts/vexa.mjs report --meeting_url "https://meet.google.com/abc-defg-hij"`
- or `node skills/vexa/scripts/ingest.mjs --meeting_url "<url>"`

Writes to `memory/meetings/YYYY-MM-DD-<slug>.md` with: meeting info, summary placeholders, key decisions, action items, and full transcript.

### 6) Get or update the Ultravox voice agent system prompt

The voice agent system prompt controls how the Vexa bot behaves in meetings (personality, language, what it does when triggered). It is stored per-user and applied when the next bot starts.

- Get current prompt (null = using service default):
  - `node skills/vexa/scripts/vexa.mjs voice-agent:config:get`
- Set a custom prompt:
  - `node skills/vexa/scripts/vexa.mjs voice-agent:config:set --prompt "You are Vexa, a concise meeting assistant..."`
- Reset to service default:
  - `node skills/vexa/scripts/vexa.mjs voice-agent:config:reset`

**Note:** The updated prompt takes effect on the **next bot started** — it does not affect bots already in a meeting.

## Core commands

- Bot status:
  - `node skills/vexa/scripts/vexa.mjs bots:status`
- Request bot (explicit fields):
  - `node skills/vexa/scripts/vexa.mjs bots:start --platform google_meet --native_meeting_id abc-defg-hij --bot_name "Claw" --language en`
- Update active bot language:
  - `node skills/vexa/scripts/vexa.mjs bots:config:update --platform google_meet --native_meeting_id abc-defg-hij --language es`
- List meetings:
  - `node skills/vexa/scripts/vexa.mjs meetings:list`
- Update metadata (title/participants/languages/notes):
  - `node skills/vexa/scripts/vexa.mjs meetings:update --platform google_meet --native_meeting_id abc-defg-hij --name "Weekly Product Sync" --participants "Alice,Bob" --languages "en" --notes "Action items captured"`
- Generate share URL:
  - `node skills/vexa/scripts/vexa.mjs transcripts:share --platform google_meet --native_meeting_id abc-defg-hij --ttl_seconds 3600`
- Set Vexa user webhook URL:
  - `node skills/vexa/scripts/vexa.mjs user:webhook:set --webhook_url https://your-public-url/hooks/vexa`

## Recordings

- List recordings:
  - `node skills/vexa/scripts/vexa.mjs recordings:list [--limit 50] [--offset 0] [--meeting_id <db_id>]`
- Get a single recording:
  - `node skills/vexa/scripts/vexa.mjs recordings:get <recording_id>`
- Delete a recording (destructive):
  - `node skills/vexa/scripts/vexa.mjs recordings:delete <recording_id> --confirm DELETE`
- Get download URL for a media file:
  - `node skills/vexa/scripts/vexa.mjs recordings:download <recording_id> <media_file_id>`
- Get recording config:
  - `node skills/vexa/scripts/vexa.mjs recordings:config:get`
- Update recording config:
  - `node skills/vexa/scripts/vexa.mjs recordings:config:update --enabled true --capture_modes audio,video`

## Meeting bundle (post-meeting)

Get everything about a meeting in one call — transcript, recordings, share link:
- `node skills/vexa/scripts/vexa.mjs meetings:bundle --meeting_url "https://meet.google.com/abc-defg-hij"`
- `node skills/vexa/scripts/vexa.mjs meetings:bundle --platform zoom --native_meeting_id 1234567890`

Options:
- `--segments` — include transcript segments (omitted by default to keep output small)
- `--no-share` — skip creating a share link
- `--no-recordings` — skip recordings metadata
- `--download-urls` — resolve download URLs for each recording media file
- `--ttl_seconds 3600` — share link TTL

## Webhook (meeting finished → report) — optional

Optionally, Vexa can POST a "meeting finished" webhook to trigger automatic report creation. This requires the user to manually configure their `openclaw.json` — see `references/webhook-setup.md` for the hooks mapping config. The skill does NOT modify `openclaw.json` automatically. Users who want this feature add `hooks.transformsDir` and the vexa mapping to their config themselves.

## OpenClaw ingestion helpers

- Create basic meeting report (meeting info, transcript, placeholders for summary/decisions/actions):
  - `node skills/vexa/scripts/vexa.mjs report --meeting_url "<url>"`
  - `node skills/vexa/scripts/ingest.mjs --meeting_url "<url>"` (or `--platform` + `--native_meeting_id`)
- Audit meetings for likely test calls / cleanup candidates:
  - `node skills/vexa/scripts/audit.mjs`

## Platform rules

- Supported: `google_meet`, `teams`, `zoom`
- Teams `native_meeting_id` must be numeric ID only.
- Teams bot join requires passcode (from `?p=` in Teams URL).
- Zoom `native_meeting_id` is 10-11 digit numeric ID. Passcode (`?pwd=`) is optional.

## Deletion safety (strict)

`DELETE /meetings/{platform}/{native_meeting_id}` purges transcripts and anonymizes data.

Rules:
1. Never call delete without explicit user request for that exact meeting.
2. Verify `platform` + `native_meeting_id` first.
3. Prefer non-destructive cleanup (`meetings:update`) whenever possible.
4. Require guard flag:
   - `node skills/vexa/scripts/vexa.mjs meetings:delete --platform google_meet --native_meeting_id abc-defg-hij --confirm DELETE`
