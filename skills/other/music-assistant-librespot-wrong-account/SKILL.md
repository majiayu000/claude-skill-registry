---
name: music-assistant-librespot-wrong-account
description: |
  Fix for Music Assistant Spotify playback failing with "librespot does not support free
  accounts" even when the Spotify account has Premium. Use when: (1) Songs load for 1-2
  seconds then auto-pause, (2) Music Assistant logs show "librespot does not support free
  accounts" followed by FFmpeg "Invalid data found when processing input" exit code 183,
  (3) Spotify provider shows "Successfully logged in" but streaming fails. Root cause is
  stale librespot credential cache pointing to a different (free-tier) Spotify account.
author: Claude Code
version: 1.0.0
date: 2026-02-21
---

# Music Assistant Librespot Wrong Account / Stale Credentials

## Problem
Music Assistant (MASS) Spotify playback fails immediately — songs appear to load for 1-2
seconds then auto-pause. Every track is marked "unplayable". The error log shows librespot
rejecting the account as "free" despite the configured Spotify account having Premium.

## Context / Trigger Conditions
- Music Assistant addon on Home Assistant (tested with v2.7.8, addon `d5369777_music_assistant`)
- Symptoms: Song starts loading, pauses after 1-2 seconds, skipped as "unplayable"
- Log pattern (all three appear together on every play attempt):
  ```
  WARNING [music_assistant.spotify] [librespot] librespot does not support "free" accounts.
  WARNING [music_assistant.audio.media_stream] Error opening input: Invalid data found when processing input
  ERROR [music_assistant.streams] AudioError while streaming queue item ... FFMpeg exited with code 183
  ```
- OAuth login succeeds: `Successfully logged in to Spotify as <Name>`
- But librespot streaming fails with the "free" account error

## Root Cause
Music Assistant uses **two separate auth mechanisms** for Spotify:
1. **OAuth (PKCE flow)** — for browsing, search, metadata. Uses access tokens refreshed via
   the Spotify Web API. This is what produces the "Successfully logged in" message.
2. **Librespot** — for actual audio streaming. Uses cached credentials stored in
   `/data/.cache/spotify--<id>/credentials.json` inside the addon container.

The librespot credential cache can become stale or point to a **different Spotify account**
(e.g., if another family member logged in, or credentials were cached from before a Premium
upgrade). Librespot uses these cached credentials to connect to Spotify's internal API, which
returns a `ProductInfo` XML packet containing the account `type`. If the cached account is
"free", librespot calls `exit(1)`, killing the audio pipeline before FFmpeg receives any data.

## How Librespot Determines Account Type
Librespot reads the `type` field from Spotify's `ProductInfo` server packet
(`librespot-org/librespot`, `core/src/session.rs`):
```rust
fn check_catalogue(attributes: &UserAttributes) {
    if let Some(account_type) = attributes.get("type") {
        if account_type != "premium" {
            error!("librespot does not support {account_type:?} accounts.");
            exit(1);
        }
    }
}
```
The check is an exact string match against `"premium"`.

## Solution

### Step 1: Verify the Problem
Check Music Assistant addon logs for the "free accounts" error:
```bash
# Via HA API (from a machine with the HA token)
python3 -c "
import os, json, requests
url = os.environ.get('HOME_ASSISTANT_SOFIA_URL', '').rstrip('/')
token = os.environ.get('HOME_ASSISTANT_SOFIA_TOKEN', '')
headers = {'Authorization': f'Bearer {token}'}
r = requests.get(f'{url}/api/hassio/addons/d5369777_music_assistant/logs', headers=headers)
for line in r.text.split('\n'):
    if 'free' in line.lower() or 'librespot' in line.lower():
        print(line)
"
```

### Step 2: Identify the Music Assistant Container
From the SSH addon (ha-sofia: `ssh vbarzin@192.168.1.8`):
```bash
sudo curl -s --unix-socket /run/docker.sock http://localhost/containers/json | \
  python3 -c "import sys,json; [print(c['Names'][0], c['Id'][:12]) for c in json.load(sys.stdin) if 'music' in c['Names'][0].lower()]"
```

### Step 3: Check Cached Credentials
Exec into the container to read the librespot cache:
```bash
# Create exec
EXEC_ID=$(sudo curl -s --unix-socket /run/docker.sock \
  "http://localhost/containers/<CONTAINER_ID>/exec" \
  -H 'Content-Type: application/json' \
  -d '{"Cmd":["cat","/data/.cache/spotify--5s3mSP8y/credentials.json"],"AttachStdout":true,"AttachStderr":true}' | python3 -c "import sys,json; print(json.load(sys.stdin)['Id'])")

# Run exec
sudo curl -s --unix-socket /run/docker.sock \
  "http://localhost/exec/$EXEC_ID/start" \
  -H 'Content-Type: application/json' -d '{"Detach":false}'
```
Check the `username` field — if it doesn't match the expected Premium account, that's the problem.

### Step 4: Clear the Cache
```bash
# Create exec to delete cache
EXEC_ID=$(sudo curl -s --unix-socket /run/docker.sock \
  "http://localhost/containers/<CONTAINER_ID>/exec" \
  -H 'Content-Type: application/json' \
  -d '{"Cmd":["rm","-rf","/data/.cache/spotify--5s3mSP8y"],"AttachStdout":true,"AttachStderr":true}' | python3 -c "import sys,json; print(json.load(sys.stdin)['Id'])")

# Run exec
sudo curl -s --unix-socket /run/docker.sock \
  "http://localhost/exec/$EXEC_ID/start" \
  -H 'Content-Type: application/json' -d '{"Detach":false}'
```

### Step 5: Restart Music Assistant
```bash
sudo curl -s --unix-socket /run/docker.sock \
  "http://localhost/containers/<CONTAINER_ID>/restart" -X POST
```

### Step 6: Verify
After restart, check logs for:
- `Successfully logged in to Spotify as <Name>` (OAuth OK)
- No "free accounts" error when playing a track
- Optionally re-check `/data/.cache/spotify--5s3mSP8y/credentials.json` to confirm the
  `username` now matches the Premium account

## Verification
1. Play any Spotify track through Music Assistant
2. The track should stream without pausing after 1-2 seconds
3. Logs should show `Start Queue Flow stream` without subsequent `AudioError`

## Notes
- The cache directory name `spotify--5s3mSP8y` is an internal Music Assistant provider ID
  and may differ across installations. Use `find /data -name credentials.json` to locate it.
- The `username` field in the credentials cache is Spotify's internal user ID (numeric for
  newer accounts, text for older ones), not necessarily the display name or email.
- Spotify Family plan **owners** have account type `"premium"`. Family plan **members** also
  report as `"premium"` when their membership is active.
- If the problem recurs, it may indicate that Music Assistant's Spotify provider re-caches
  the wrong credentials — check if multiple Spotify accounts are configured or if another
  user logged in via the Music Assistant UI.
- The SSH addon on HA OS needs `sudo` for Docker socket access (`/run/docker.sock` is owned
  by `root:messagebus`).
- The HA long-lived token typically does NOT have Supervisor API access (hassio endpoints
  return 401), so addon management must go through the Docker socket from the SSH addon.
