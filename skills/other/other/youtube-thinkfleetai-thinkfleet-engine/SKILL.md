---
name: youtube
description: "Query YouTube — search videos, get channel stats, list playlists, and manage comments via the Data API v3."
metadata: {"thinkfleetbot":{"emoji":"▶️","requires":{"bins":["curl","jq"],"env":["GOOGLE_ACCESS_TOKEN"]}}}
---

# YouTube

Search videos, get channel stats, and manage playlists via the YouTube Data API v3.

## Environment Variables

- `GOOGLE_ACCESS_TOKEN` - OAuth 2.0 access token with YouTube scope

## Search videos

```bash
curl -s -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  "https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q=SEARCH_QUERY&maxResults=5" | jq '.items[] | {videoId: .id.videoId, title: .snippet.title, channel: .snippet.channelTitle}'
```

## Get video details

```bash
curl -s -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id=VIDEO_ID" | jq '.items[0] | {title: .snippet.title, views: .statistics.viewCount, likes: .statistics.likeCount}'
```

## Get channel stats

```bash
curl -s -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  "https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet&id=CHANNEL_ID" | jq '.items[0] | {title: .snippet.title, subscribers: .statistics.subscriberCount, videos: .statistics.videoCount}'
```

## List playlists

```bash
curl -s -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  "https://www.googleapis.com/youtube/v3/playlists?part=snippet&mine=true&maxResults=10" | jq '.items[] | {id, title: .snippet.title}'
```

## Notes

- Access token must have `https://www.googleapis.com/auth/youtube.readonly` scope.
