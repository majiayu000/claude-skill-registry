---
name: dl
description: Download Video/Music from YouTube/Bilibili/X/etc.
author: guoqiao
metadata: {"openclaw":{"always":false,"emoji":"🦞","homepage":"https://clawhub.ai/guoqiao/dl","os":["darwin","linux","win32"],"requires":{"bins":["uv"]}}}
triggers:
- "/dl <url>"
- "Download this video ..."
- "Download this music ..."
---

# Media Downloader

Smartly download media (Video/Music) from URLs (YouTube, Bilibili, X, etc.) to the appropriate local folders.

- **Video:** Save into `~/Movies/` or `~/Videos/`.
- **Music:** Save into `~/Music/`.
- **Playlists:** Saves items into a subdirectory (e.g., `~/Music/<playlist_name>/`).

Designed to work with a local Media Server (e.g., Universal Media Server, Jellyfin) for instant playback on TV/devices.

## Agent Procedure

When the user provides a URL or asks to download media, **you MUST follow this exact sequence:**

1. **Acknowledge:**
   - Immediately reply to the user: "Downloading with dl skill..."

2. **Execute:**
   - Run the script:
     ```bash
     uv run --script ${baseDir}/dl.py "<url>"
     ```

3. **Capture Path:**
   - Read the script output, a path will be printed to stdout at the end, points to either a single file or a folder contains the playlist items.

4. **Upload (Telegram Only):**
   - If the user is on Telegram (check context or session) AND the file is audio (mp3/m4a):
   - Use the `message` tool to send the file to the user:
     ```json
     {
       "action": "send",
       "filePath": "<filepath>",
       "caption": "Here is your music."
     }
     ```

## Usage

Run `dl.py` as a uv script:
```bash
# save into default dirs ~/Music or ~/Movies or ~/Videos
uv run --script ${baseDir}/dl.py <url>

# specify your own output dir
uv run --script ${baseDir}/dl.py <url> -o <out_dir>
```
The script will print output path, either a file or a folder.

A optional cookies file could be provided to make yt-dlp more reliable, with which ever of these detected first:

- `${baseDir}/.cookies.txt`
- `$DL_COOKIES_FILE`
- `$COOKIES_FILE`
- `~/.cookies.txt`

## Setup (User)

This skill will be much more useful if you setup a media server on same machine to share the downloaded media in your LAN:

1. Install a DLNA/UPnP Media Server (Universal Media Server, miniDLNA, Jellyfin).
2. Share `~/Music` and `~/Movies` (or `~/Videos`) folders.
3. Downloaded media will appear automatically on your TV, with apps support DLNA/UPnP, such as VLC.

See [example script](https://github.com/guoqiao/skills/blob/main/dl/ums/ums_install.sh) to setup Universal Media Server on Mac.
