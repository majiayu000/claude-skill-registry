---
name: twitch
description: "Query Twitch — streams, users, games, and clips via the Helix API."
metadata: {"thinkfleetbot":{"emoji":"🎮","requires":{"bins":["curl","jq"],"env":["TWITCH_CLIENT_ID","TWITCH_ACCESS_TOKEN"]}}}
---

# Twitch

Query streams, users, games, and clips via the Twitch Helix API.

## Environment Variables

- `TWITCH_CLIENT_ID` - Client ID
- `TWITCH_ACCESS_TOKEN` - OAuth access token

## Get user

```bash
curl -s -H "Client-ID: $TWITCH_CLIENT_ID" -H "Authorization: Bearer $TWITCH_ACCESS_TOKEN" \
  "https://api.twitch.tv/helix/users?login=USERNAME" | jq '.data[0] | {id, login, display_name, view_count}'
```

## Get streams

```bash
curl -s -H "Client-ID: $TWITCH_CLIENT_ID" -H "Authorization: Bearer $TWITCH_ACCESS_TOKEN" \
  "https://api.twitch.tv/helix/streams?first=10" | jq '.data[] | {user_name, game_name, viewer_count, title}'
```

## Get top games

```bash
curl -s -H "Client-ID: $TWITCH_CLIENT_ID" -H "Authorization: Bearer $TWITCH_ACCESS_TOKEN" \
  "https://api.twitch.tv/helix/games/top?first=10" | jq '.data[] | {id, name}'
```

## Get clips

```bash
curl -s -H "Client-ID: $TWITCH_CLIENT_ID" -H "Authorization: Bearer $TWITCH_ACCESS_TOKEN" \
  "https://api.twitch.tv/helix/clips?broadcaster_id=BROADCASTER_ID&first=5" | jq '.data[] | {id, title, view_count, url}'
```

## Notes

- Read-only operations. No confirmation needed for queries.
