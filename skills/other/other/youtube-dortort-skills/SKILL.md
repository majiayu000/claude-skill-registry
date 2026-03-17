---
name: youtube
description: Manages YouTube channels and videos using the YouTube Data API v3. Handles OAuth2 authentication, video uploads with resumable transfer, metadata updates, thumbnail setting, playlist management, comment moderation, channel-wide search, and bulk CSV workflows. Use when the user wants to upload a video, manage their YouTube channel, update video titles or descriptions, create or manage playlists, list channel videos, search their content, export a video catalogue, or bulk-edit metadata. Trigger phrases include "youtube", "upload video", "channel manager", "my videos", "YouTube playlist", "YouTube API", "update metadata".
user-invocable: true
disable-model-invocation: true
argument-hint: "<intent>"
---

# YouTube — Creator & Channel Manager

Manages YouTube channels and videos via the YouTube Data API v3, using the `scripts/yt.py` helper and the official `google-api-python-client` SDK. All operations are authenticated with OAuth2 and credentials are cached after the first authorisation.

**User request:** $ARGUMENTS

---

## Step 1 — Check prerequisites

Run this first and act on the result:

```bash
python3 scripts/yt.py whoami 2>&1
```

- **Channel name printed** → authenticated, go to Step 2
- **"Missing dependencies"** → run `bash scripts/setup.sh`, then re-check
- **"No OAuth credentials found"** → guide the user through one-time setup below

### One-time setup (only when needed)

**Install Python dependencies:**

```bash
bash scripts/setup.sh
```

**Create Google Cloud credentials (manual — guide the user):**

1. Go to [https://console.cloud.google.com](https://console.cloud.google.com) and create or select a project
2. **APIs & Services → Library** → search for **YouTube Data API v3** → Enable
3. **APIs & Services → Credentials** → Create Credentials → OAuth 2.0 Client ID → Desktop app
4. Download JSON → save as `~/.youtube-skill/client_secrets.json`

**Authorise (opens a browser window):**

```bash
python3 scripts/yt.py auth
```

Credentials are cached at `~/.youtube-skill/credentials.json` and silently refreshed on all subsequent runs. To force a fresh login: `rm ~/.youtube-skill/credentials.json && python3 scripts/yt.py auth`.

---

## Step 2 — Parse $ARGUMENTS and run the right command

Interpret the user's intent and run the matching `yt.py` command. See [reference.md](reference.md) for the full flag reference.

| User intent | Command |
|---|---|
| Show channel / who am I | `python3 scripts/yt.py whoami` |
| List videos | `python3 scripts/yt.py videos list [--limit N] [--status public\|private\|unlisted]` |
| Get video details | `python3 scripts/yt.py videos get <VIDEO_ID>` |
| Upload a video | `python3 scripts/yt.py videos upload <FILE> --title "..." --privacy private` |
| Update title / description / tags / category | `python3 scripts/yt.py videos update <VIDEO_ID> --title "..." [--description "..."] [--tags "a,b"]` |
| Change privacy / publish now | `python3 scripts/yt.py videos update <VIDEO_ID> --privacy public` |
| Schedule publish | `python3 scripts/yt.py videos update <VIDEO_ID> --publish-at "2025-12-31T18:00:00Z"` |
| Set thumbnail | `python3 scripts/yt.py videos thumbnail <VIDEO_ID> <IMAGE>` |
| Delete a video | `python3 scripts/yt.py videos delete <VIDEO_ID>` |
| List playlists | `python3 scripts/yt.py playlists list` |
| Create playlist | `python3 scripts/yt.py playlists create "Title" [--privacy public]` |
| List videos in a playlist | `python3 scripts/yt.py playlists items <PLAYLIST_ID>` |
| Add video to playlist | `python3 scripts/yt.py playlists add <PLAYLIST_ID> <VIDEO_ID>` |
| Remove video from playlist | `python3 scripts/yt.py playlists remove <PLAYLIST_ID> <VIDEO_ID>` |
| Delete playlist | `python3 scripts/yt.py playlists delete <PLAYLIST_ID>` |
| List comments | `python3 scripts/yt.py comments list <VIDEO_ID> [--limit N] [--order relevance\|time]` |
| Reply to a comment | `python3 scripts/yt.py comments reply <COMMENT_THREAD_ID> "reply text"` |
| Search channel content | `python3 scripts/yt.py search "query" [--type video\|playlist]` |
| Export full catalogue | `python3 scripts/yt.py export > channel.csv` |
| Bulk-update from CSV | `python3 scripts/yt.py bulk-update updates.csv` |

**Safety defaults — always apply:**

- Uploads default to `--privacy private`. Never upload as public unless the user explicitly asks.
- Do **not** add `--yes` to delete commands. Always let the script prompt for confirmation.
- For `comments reply`, confirm the reply text with the user before posting.

---

## Step 3 — Report results and suggest next steps

After each command:

1. Show the output (video ID, URL, status).
2. Offer logical next steps. Examples:
   - After upload → set thumbnail, add to playlist, schedule or publish
   - After export → offer to open in spreadsheet or run bulk-update
   - After creating a playlist → offer to add videos
3. If an API error occurs, explain it and suggest the fix. See the error table in [reference.md](reference.md).
