---
name: loom
description: Manage Loom video recordings - list, share, and get analytics via Loom API.
metadata: {"clawdbot":{"emoji":"🎥","requires":{"env":["LOOM_API_KEY"]}}}
---

# Loom

Video messaging platform.

## Environment

```bash
export LOOM_API_KEY="xxxxxxxxxx"
```

## List Videos

```bash
curl "https://api.loom.com/v1/videos" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## Get Video Details

```bash
curl "https://api.loom.com/v1/videos/{video_id}" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## Get Video Transcript

```bash
curl "https://api.loom.com/v1/videos/{video_id}/transcript" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## Update Video

```bash
curl -X PATCH "https://api.loom.com/v1/videos/{video_id}" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "privacy": "public"}'
```

## Delete Video

```bash
curl -X DELETE "https://api.loom.com/v1/videos/{video_id}" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## Get Analytics

```bash
curl "https://api.loom.com/v1/videos/{video_id}/insights" \
  -H "Authorization: Bearer $LOOM_API_KEY"
```

## Links
- Dashboard: https://www.loom.com/looms
- Docs: https://dev.loom.com
