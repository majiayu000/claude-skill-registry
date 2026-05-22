---
name: uni-spotify
description: |
  Spotify control via uni CLI. Use when user wants to control Spotify playback, search music, view playlists, or check what's playing.
  Note: Playback control (play/pause/next/prev/queue/volume) requires Spotify Premium. Search and playlists work for all users.
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# Spotify (uni)

Control Spotify from the terminal. Uses OAuth PKCE (no setup needed - default app embedded).

## Authentication

```bash
uni spotify auth                  # Authenticate (opens browser)
uni spotify auth --status         # Check auth status
uni spotify auth --logout         # Log out
uni spotify auth --setup          # Instructions for custom Spotify app
```

## Now Playing

```bash
uni spotify now                   # Show currently playing
uni spotify np                    # Alias
uni spotify now --watch           # Live updates (5s refresh)
```

## Search

```bash
uni spotify search "Bohemian Rhapsody"        # Search tracks
uni spotify search "Queen" --type artist      # Search artists
uni spotify search "Abbey Road" --type album  # Search albums
uni spotify search "Chill" --type playlist    # Search playlists
uni spotify search "rock" -n 20               # More results
```

## Playback Control (Premium Only)

```bash
uni spotify play                              # Resume playback
uni spotify play "Bohemian Rhapsody"          # Search and play
uni spotify play "Abbey Road" --album         # Play album
uni spotify play "Chill Vibes" --playlist     # Play playlist
uni spotify play "spotify:track:..."          # Play by URI
uni spotify pause                             # Pause
uni spotify next                              # Next track
uni spotify prev                              # Previous track
```

## Queue (Premium Only)

```bash
uni spotify queue "Stairway to Heaven"        # Add to queue
uni spotify queue "spotify:track:..."         # Add by URI
```

## Volume (Premium Only)

```bash
uni spotify volume                # Show current volume
uni spotify volume 50             # Set to 50%
uni spotify vol 75                # Alias
```

## Devices

```bash
uni spotify devices                           # List devices
uni spotify devices --transfer <device-id>    # Switch device
```

## Playlists

```bash
uni spotify playlists                         # List your playlists
uni spotify playlists -n 50                   # More playlists
uni spotify playlists <playlist-id>           # View playlist tracks
```

## Notes

- **Premium Required**: play, pause, next, prev, queue, volume, device transfer
- **Free Users**: search, now (read-only), playlists, devices (view only)
- **IDs**: All commands show IDs in output `[abc123]` for use in subsequent commands
- **URIs**: Spotify URIs like `spotify:track:...` can be used directly
