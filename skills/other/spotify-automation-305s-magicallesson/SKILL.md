---
name: Spotify Automation
description: Automate Spotify music playback, playlist management, and audio analysis workflows
version: 1.0.0
author: Claude Office Skills
category: media
tags:
  - spotify
  - music
  - playlist
  - audio
  - entertainment
department: content
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: media-mcp
  tools:
    - spotify_playback
    - spotify_playlist
    - spotify_search
    - spotify_analysis
capabilities:
  - Playback control
  - Playlist management
  - Music discovery
  - Audio analysis
input:
  - Search queries
  - Playlist configurations
  - Playback commands
  - Analysis parameters
output:
  - Playback status
  - Playlist updates
  - Track recommendations
  - Audio features
languages:
  - en
related_skills:
  - youtube-automation
  - podcast-automation
---

# Spotify Automation

Automate Spotify music playback, playlist management, and discovery workflows.

## Core Capabilities

### Playback Control
```yaml
playback_commands:
  - play_track: "spotify:track:xxx"
  - pause
  - next_track
  - previous_track
  - set_volume: 75
  - set_shuffle: true
  - set_repeat: "context"  # track, context, off
  - seek_position: 30000  # milliseconds
  - transfer_playback:
      device_id: "device_xxx"
```

### Playlist Management
```yaml
playlist_operations:
  create:
    name: "{{playlist_name}}"
    description: "{{description}}"
    public: false
    collaborative: false
    
  add_tracks:
    playlist_id: "xxx"
    tracks:
      - "spotify:track:xxx"
      - "spotify:track:yyy"
    position: 0  # optional
    
  smart_playlist:
    name: "Workout Mix"
    criteria:
      energy: "> 0.8"
      tempo: "> 120"
      genres: ["electronic", "pop"]
    limit: 50
    refresh: weekly
```

### Music Discovery
```yaml
recommendations:
  seed_tracks: ["track_id_1", "track_id_2"]
  seed_artists: ["artist_id"]
  seed_genres: ["pop", "rock"]
  
  target_features:
    energy: 0.8
    danceability: 0.7
    valence: 0.6  # positiveness
    
  limit: 20
```

### Audio Analysis
```yaml
audio_features:
  - acousticness: 0.0-1.0
  - danceability: 0.0-1.0
  - energy: 0.0-1.0
  - instrumentalness: 0.0-1.0
  - liveness: 0.0-1.0
  - loudness: -60 to 0 dB
  - speechiness: 0.0-1.0
  - tempo: BPM
  - valence: 0.0-1.0 (mood)
  - key: 0-11 (C to B)
  - mode: 0 (minor) or 1 (major)
```

## Workflow Examples

### Daily Mix Generator
```yaml
workflow:
  trigger: daily at 6:00 AM
  steps:
    - get_recently_played: 50
    - analyze_mood: based_on_audio_features
    - get_recommendations: 
        based_on: recent_tracks
        mood: current_time_appropriate
    - create_playlist: "Today's Mix - {{date}}"
    - add_tracks: recommended
```

### Party Mode
```yaml
party_playlist:
  trigger: "party mode"
  actions:
    - get_top_tracks:
        time_range: medium_term
        limit: 20
    - get_recommendations:
        seed: top_tracks
        energy: "> 0.8"
        danceability: "> 0.7"
    - shuffle_and_play
    - set_crossfade: 5  # seconds
```

## API Examples

```javascript
// Search and Play
const results = await spotify.search("Bohemian Rhapsody", ["track"]);
await spotify.play({ uris: [results.tracks.items[0].uri] });

// Create Smart Playlist
const recs = await spotify.getRecommendations({
  seed_genres: ["chill"],
  target_energy: 0.4,
  limit: 30
});
const playlist = await spotify.createPlaylist("Chill Vibes", {
  description: "AI-curated relaxation",
  public: false
});
await spotify.addTracksToPlaylist(playlist.id, recs.tracks.map(t => t.uri));
```

## Best Practices

1. **Rate Limits**: Respect Spotify API limits
2. **Caching**: Cache frequently accessed data
3. **User Consent**: Request appropriate scopes
4. **Fallbacks**: Handle unavailable tracks gracefully
