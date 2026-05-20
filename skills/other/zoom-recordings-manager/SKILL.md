---
name: zoom-recordings-manager
description: List, download, and delete Zoom recordings via the API (OAuth). Use when you need to manage recordings at scale.
---

# Zoom recordings manager

## Goal
Generic operations on recordings:
- list
- download
- delete (by meeting or by file)

## Requirements
- Zoom OAuth credentials (Server-to-Server recommended)
- Environment variables:
  - ZOOM_ACCOUNT_ID
  - ZOOM_CLIENT_ID
  - ZOOM_CLIENT_SECRET

## Key notes
- Recurring meetings: use the **meeting UUID** for a specific instance.
- Deletion: use `trash` by default; `delete` is permanent.
- Downloads: use `download_url` and add the access_token.

## Quick script
File: `scripts/zoom_recordings.py`

List:
```
python scripts/zoom_recordings.py list --from 2025-11-01 --to 2025-12-31
```

List upcoming meetings (join_url for attendees):
```
python scripts/zoom_meetings.py --user me --type upcoming --from 2026-01-14 --to 2026-03-31
```

List by user:
```
python scripts/zoom_recordings.py list --user me --from 2025-11-01 --to 2025-12-31
```

Download:
```
python scripts/zoom_recordings.py download --url "<download_url>" --out /path/file.mp4
```

Download MP4 of LIVE/Q&A (renamed):
```
python scripts/zoom_recordings.py download-mp4 --user me --from 2025-11-01 --to 2025-12-31 --out-dir /path/zoom
```

Delete (entire meeting):
```
python scripts/zoom_recordings.py delete --meeting-id <meeting_id> --action trash
```

Delete a specific file:
```
python scripts/zoom_recordings.py delete --meeting-id <meeting_id> --recording-id <recording_id> --action trash
```

## If it fails
- Verify scopes (recording:read / recording:write) in the OAuth app.
- If the account endpoint fails, use `--user`.
- Zoom limits listings to ~30-day windows; the script already chunks requests.
