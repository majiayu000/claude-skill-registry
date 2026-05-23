---
name: controlling-spotify
description: Control Spotify playback and manage playlists via MCP server. Use when user requests playing music, controlling Spotify, creating playlists, searching songs, or managing their Spotify library.
credentials:
- SPOTIFY_CLIENT_ID
- SPOTIFY_CLIENT_SECRET
- SPOTIFY_REFRESH_TOKEN
domains:
- api.spotify.com
- accounts.spotify.com
- raw.githubusercontent.com
- github.com
metadata:
  version: 0.1.0
---

# Controlling Spotify

Control Spotify playback, search for music, and manage playlists using the Spotify MCP Server with full user account access.

## When to Use

Invoke this skill when users request:
- Playing, pausing, or skipping music on Spotify
- Searching for songs, albums, artists, or playlists
- Creating or modifying playlists
- Viewing currently playing track or playback status
- Managing their Spotify library (saved tracks, albums)
- Queuing songs or albums

## Prerequisites

**CRITICAL**: This skill requires user-provided credentials. The user must complete a one-time setup:

### One-Time User Setup

1. **Create Spotify Developer Application**
   - Go to https://developer.spotify.com/dashboard/
   - Create an app and note the Client ID and Client Secret
   - Add redirect URI: `http://127.0.0.1:8888/callback`

2. **Obtain Refresh Token**
   - User must run the helper script locally (see `references/setup-guide.md`)
   - Script exchanges OAuth code for a long-lived refresh token
   - Refresh token is saved as credential in skill configuration

3. **Configure Credentials**
   - Add three credentials to this skill:
     - `SPOTIFY_CLIENT_ID`: From Spotify Developer Dashboard
     - `SPOTIFY_CLIENT_SECRET`: From Spotify Developer Dashboard
     - `SPOTIFY_REFRESH_TOKEN`: From helper script output

   **Alternative**: Credentials can also be provided via a **Project Knowledge** file. Ensure the file contains a `.env` style block with the keys above.

**Without these credentials, the skill cannot function.** If credentials are missing, guide the user through the setup process detailed in `references/setup-guide.md`.

## MCP Server Installation

The Spotify MCP Server must be installed in the compute environment. Use the provided installation script which handles cloning, patching, and building the server.

```bash
# Run the installation script
bash scripts/install-mcp-server.sh
```

### MCP Server Configuration

Configure the MCP client to connect to the Spotify MCP server. Note the logic to support credentials from Project Knowledge.

```python
from mcp import Client
import asyncio
import re

# 1. Try to get credentials from skill configuration
env_vars = {
    "SPOTIFY_CLIENT_ID": credentials.get("SPOTIFY_CLIENT_ID"),
    "SPOTIFY_CLIENT_SECRET": credentials.get("SPOTIFY_CLIENT_SECRET"),
    "SPOTIFY_REFRESH_TOKEN": credentials.get("SPOTIFY_REFRESH_TOKEN")
}

# 2. If missing, look in Project Knowledge / Context for .env style block
if not all(env_vars.values()):
    # Heuristic: Scan context/files for VAR=VALUE patterns
    # (Pseudo-code: Implement based on available context access)
    pass

# Server configuration
mcp_config = {
    "command": "node",
    "args": ["/home/claude/spotify-mcp-server/build/index.js"],
    "env": env_vars
}

# Initialize client
async def initialize_spotify_mcp():
    client = Client()
    await client.connect_stdio(
        mcp_config["command"],
        mcp_config["args"],
        mcp_config["env"]
    )
    return client
```

## Available Tools

### Read Operations

1. **searchSpotify** - Search for tracks, albums, artists, or playlists
   ```python
   result = await client.call_tool("searchSpotify", {
       "query": "bohemian rhapsody",
       "type": "track",
       "limit": 10
   })
   ```

2. **getNowPlaying** - Get currently playing track information
   ```python
   result = await client.call_tool("getNowPlaying", {})
   ```

3. **getMyPlaylists** - List user's playlists
   ```python
   result = await client.call_tool("getMyPlaylists", {
       "limit": 20,
       "offset": 0
   })
   ```

4. **getPlaylistTracks** - Get tracks from a playlist
   ```python
   result = await client.call_tool("getPlaylistTracks", {
       "playlistId": "37i9dQZEVXcJZyENOWUFo7"
   })
   ```

5. **getRecentlyPlayed** - Get recently played tracks
   ```python
   result = await client.call_tool("getRecentlyPlayed", {
       "limit": 10
   })
   ```

6. **getUsersSavedTracks** - Get user's liked songs
   ```python
   result = await client.call_tool("getUsersSavedTracks", {
       "limit": 50,
       "offset": 0
   })
   ```

### Playback Control

1. **playMusic** - Start playing track/album/artist/playlist
   ```python
   # Play by URI
   result = await client.call_tool("playMusic", {
       "uri": "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"
   })

   # Or by type and ID
   result = await client.call_tool("playMusic", {
       "type": "track",
       "id": "6rqhFgbbKwnb9MLmUQDhG6"
   })
   ```

2. **pausePlayback** - Pause current playback
   ```python
   result = await client.call_tool("pausePlayback", {})
   ```

3. **skipToNext** - Skip to next track
   ```python
   result = await client.call_tool("skipToNext", {})
   ```

4. **skipToPrevious** - Skip to previous track
   ```python
   result = await client.call_tool("skipToPrevious", {})
   ```

5. **addToQueue** - Add track/album to playback queue
   ```python
   result = await client.call_tool("addToQueue", {
       "uri": "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"
   })
   ```

### Playlist Management

1. **createPlaylist** - Create new playlist
   ```python
   result = await client.call_tool("createPlaylist", {
       "name": "My Workout Mix",
       "description": "High energy tracks",
       "public": False
   })
   ```

2. **addTracksToPlaylist** - Add tracks to existing playlist
   ```python
   result = await client.call_tool("addTracksToPlaylist", {
       "playlistId": "3cEYpjA9oz9GiPac4AsH4n",
       "trackUris": [
           "spotify:track:4iV5W9uYEdYUVa79Axb7Rh",
           "spotify:track:6rqhFgbbKwnb9MLmUQDhG6"
       ]
   })
   ```

### Album Operations

1. **getAlbums** - Get album details
   ```python
   result = await client.call_tool("getAlbums", {
       "albumIds": ["4aawyAB9vmqN3uQ7FjRGTy"]
   })
   ```

2. **getAlbumTracks** - Get tracks from album
   ```python
   result = await client.call_tool("getAlbumTracks", {
       "albumId": "4aawyAB9vmqN3uQ7FjRGTy"
   })
   ```

3. **saveOrRemoveAlbumForUser** - Save/remove albums
   ```python
   result = await client.call_tool("saveOrRemoveAlbumForUser", {
       "albumIds": ["4aawyAB9vmqN3uQ7FjRGTy"],
       "action": "save"
   })
   ```

## Workflow Examples

### Example 1: Play User's Favorite Song

```python
# 1. Search for the song
search_result = await client.call_tool("searchSpotify", {
    "query": "user's favorite song name",
    "type": "track",
    "limit": 1
})

# 2. Extract track URI from results
track_uri = search_result["tracks"][0]["uri"]

# 3. Play the track
await client.call_tool("playMusic", {
    "uri": track_uri
})
```

### Example 2: Create Playlist from Genre

```python
# 1. Search for tracks in genre
search_result = await client.call_tool("searchSpotify", {
    "query": "genre:rock year:2020-2024",
    "type": "track",
    "limit": 20
})

# 2. Create new playlist
playlist_result = await client.call_tool("createPlaylist", {
    "name": "Modern Rock Mix",
    "description": "Recent rock tracks",
    "public": False
})

# 3. Extract track URIs
track_uris = [track["uri"] for track in search_result["tracks"]]

# 4. Add tracks to playlist
await client.call_tool("addTracksToPlaylist", {
    "playlistId": playlist_result["id"],
    "trackUris": track_uris
})
```

### Example 3: Show What's Playing

```python
# Get current playback state
now_playing = await client.call_tool("getNowPlaying", {})

# Format and display
print(f"Now Playing: {now_playing['track']['name']}")
print(f"Artist: {now_playing['track']['artists'][0]['name']}")
print(f"Album: {now_playing['track']['album']['name']}")
print(f"Progress: {now_playing['progress_ms']} / {now_playing['duration_ms']} ms")
```

## Important Notes

### Spotify Premium Required

Playback control operations (play, pause, skip, queue) **require Spotify Premium**. Read operations (search, get playlists, view tracks) work with free accounts.

### Active Device Required

For playback commands to work, the user must have an active Spotify session (web player, desktop app, mobile app) with a device available. If no active device, playback commands will fail.

### Rate Limits

Spotify API has rate limits (typically 180 requests per minute). For bulk operations, implement appropriate delays or batching.

### Token Security

- Refresh tokens grant **full access** to user's Spotify account
- **Never** log or expose refresh tokens
- Treat them with the same security as passwords
- Users can revoke tokens from https://www.spotify.com/account/apps/

### URI Format

Spotify uses URIs in the format:
- Track: `spotify:track:ID`
- Album: `spotify:album:ID`
- Artist: `spotify:artist:ID`
- Playlist: `spotify:playlist:ID`

Most tools accept either URIs or separate `type` + `id` parameters.

## Troubleshooting

### "Spotify configuration not found"

**Cause**: Missing environment variables

**Solution**: Verify credentials are properly configured:
```python
import os
print(os.getenv("SPOTIFY_CLIENT_ID"))  # Should not be None
print(os.getenv("SPOTIFY_CLIENT_SECRET"))  # Should not be None
print(os.getenv("SPOTIFY_REFRESH_TOKEN"))  # Should not be None
```

### "No active device"

**Cause**: No Spotify client is currently running/active

**Solution**: Guide user to:
1. Open Spotify on any device (web, desktop, mobile)
2. Start playing something (can pause immediately)
3. Try the playback command again

### "Premium required"

**Cause**: User has Spotify Free account

**Solution**: Playback control requires Spotify Premium. Only search and read operations available for free accounts.

### MCP Server Won't Start

**Cause**: Missing dependencies or incorrect installation

**Solution**:
```bash
# Re-run installation script
bash scripts/install-mcp-server.sh
```

## Best Practices

1. **Always search before playing** - Don't assume URIs, search for content first
2. **Check playback state** - Use `getNowPlaying` to verify device availability
3. **Handle errors gracefully** - Provide helpful messages when operations fail
4. **Batch operations** - When adding multiple tracks, use single call with array
5. **Respect rate limits** - Add delays for bulk operations

## References

- Setup Guide: `references/setup-guide.md`
- API Documentation: https://developer.spotify.com/documentation/web-api/
- MCP Specification: https://modelcontextprotocol.io/

## Security

This skill requires sensitive credentials. Ensure:
- Credentials are stored securely in skill configuration
- Never expose credentials in responses to users
- Never log credentials
- Users understand they can revoke access anytime

See `references/setup-guide.md` for detailed security best practices.
