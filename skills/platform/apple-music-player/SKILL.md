---
name: apple-music-player
description: Play random songs or specific tracks in Music.app from the local Music library. Use when a user asks to play a random song by artist, random track from an album, random track from a playlist, or a specific track by name (optionally with artist).
---

# Apple Music Player

## Overview
Play a random track from the Music app's local library by artist, album, or playlist, using a bundled script that wraps AppleScript and handles errors.

## Quick Start
- Artist: `scripts/play_random_music.sh --artist "JAY-Z"`
- Album: `scripts/play_random_music.sh --album "TRON: Ares"`
- Playlist: `scripts/play_random_music.sh --playlist "My Favorites"`
- Track: `scripts/play_random_music.sh --track "Rock the Boat" --artist "XG"`
- Foreground (optional): append `--foreground` to bring Music to front.

## Behavior Notes
- Operates on the local Music library only; it does not search Apple Music.
- Artist, album, and track matching use "contains" so partial names work.
- Playlist matching requires an exact playlist name.
- Performance path keeps Music in background by default; use `--foreground` only when needed.

## Workflow
1. Prefer using the script in `scripts/` rather than retyping AppleScript.
2. If no matches are found, surface the script's error message to the user.
3. If the user needs Apple Music search/playback, ask them to add the album or track to the Library first.

## Resources
### scripts/
- `scripts/play_random_music.sh`: performance-optimized AppleScript runner to play by artist/album/playlist/track with optional foreground activation.
