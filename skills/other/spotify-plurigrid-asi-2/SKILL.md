---
name: spotify
description: Control Spotify playback and manage playlists. Play music, pause, skip tracks, search for songs/albums/artists, create playlists, add tracks, check what's playing, and manage your library. Requires Spotify Premium.
compatibility: Requires Node.js, Spotify Premium account, and OAuth tokens configured in spotify-config.json.
---

# Spotify Control

Control Spotify playback and manage playlists via MCP.

## When to Use

- Play specific songs, albums, artists, or playlists
- Control playback (pause, skip, previous)
- Search Spotify catalog
- Create and manage playlists
- Check what's currently playing
- Add tracks to queue

## Setup

MCP server configured in `~/.mcp.json`:
```json
{
  "spotify": {
    "command": "node",
    "args": ["/Users/alice/Projects/spotify-mcp-server/build/index.js"]
  }
}
```

OAuth config in `/Users/alice/Projects/spotify-mcp-server/spotify-config.json`.

## Available Tools

### Read Operations
| Tool | Description |
|------|-------------|
| `searchSpotify` | Search tracks, albums, artists, playlists |
| `getNowPlaying` | Get currently playing track |
| `getMyPlaylists` | List user's playlists |
| `getPlaylistTracks` | Get tracks in a playlist |
| `getRecentlyPlayed` | Recently played tracks |
| `getUsersSavedTracks` | Liked songs library |

### Playback Control
| Tool | Description |
|------|-------------|
| `playMusic` | Play track/album/artist/playlist |
| `pausePlayback` | Pause current playback |
| `skipToNext` | Skip to next track |
| `skipToPrevious` | Skip to previous track |
| `addToQueue` | Add item to queue |

### Playlist Management
| Tool | Description |
|------|-------------|
| `createPlaylist` | Create new playlist |
| `addTracksToPlaylist` | Add tracks to playlist |

### Album Operations
| Tool | Description |
|------|-------------|
| `getAlbums` | Get album details |
| `getAlbumTracks` | Get tracks from album |
| `saveOrRemoveAlbumForUser` | Save/remove albums |
| `checkUsersSavedAlbums` | Check if albums saved |

## Example Usage

### Play a Song
```
searchSpotify(query="bohemian rhapsody", type="track", limit=5)
playMusic(uri="spotify:track:6rqhFgbbKwnb9MLmUQDhG6")
```

### Check What's Playing
```
getNowPlaying()
```

### Create a Playlist
```
createPlaylist(name="Workout Mix", description="Pump up songs", public=false)
addTracksToPlaylist(playlistId="...", trackUris=["spotify:track:..."])
```

### Add to Queue
```
addToQueue(type="track", id="6rqhFgbbKwnb9MLmUQDhG6")
```

## Notes

- Requires Spotify Premium for playback control
- Run `npm run auth` in spotify-mcp-server to set up OAuth if tokens expired
- Active Spotify device required for playback (phone, desktop app, etc.)
