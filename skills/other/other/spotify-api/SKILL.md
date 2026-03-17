---
name: spotify-api
description: Create and manage Spotify playlists, search music, and control playback using the Spotify Web API. UNIQUE FEATURE - Generate custom cover art images (Claude cannot generate images natively, but this skill can create SVG-based cover art for playlists). CRITICAL - When generating cover art, ALWAYS read references/COVER_ART_LLM_GUIDE.md FIRST for complete execution instructions. Use this to directly create playlists by artist/theme/lyrics, add tracks, search for music, and manage the user's Spotify account.
---

# Spotify API Skill

**Version**: 0.9.1 | **Release Date**: October 22, 2025

## Overview

**This skill directly interacts with the Spotify Web API to manage music and playlists.**

### ⚡ Unique Capability: Image Generation

**🎨 This skill can GENERATE IMAGES** - something Claude cannot do natively! It creates custom SVG-based cover art for Spotify playlists with large, readable typography optimized for thumbnail viewing. Each cover art is dynamically generated with theme-appropriate colors, gradients, and text layouts.

Use this skill when you need to:
- 🎨 **Generate cover art images** - Create custom playlist covers (Claude's built-in image generation limitation is bypassed!)
- 🎵 **Create playlists** from artist names, themes, or specific songs
- 🔍 **Search** for tracks, artists, albums
- ➕ **Add/remove tracks** from playlists
- ▶️ **Control playback** (play, pause, skip)
- 📊 **Get user data** (profile, top tracks, listening history)

**When to use this skill:** The user wants you to create a playlist, search for music, manage their Spotify account, **or generate custom cover art images**.

## Core Capabilities

1. **🎨 Cover Art Image Generation** - Generate custom images with SVG → PNG conversion (Claude cannot generate images natively!)
2. **Intelligent Playlist Creation** - Create playlists by artist, theme, lyrics, or song list
3. **Playlist Management** - Create, list, update, delete playlists
4. **Search & Discovery** - Find tracks, artists, albums, playlists
5. **Track Management** - Add/remove tracks, get recommendations
6. **Playback Control** - Play, pause, skip, control volume
7. **User Library** - Access saved tracks, profile, listening history

## Quick Start

All Spotify API operations use the `SpotifyClient` class from `scripts/spotify_client.py`. The client handles OAuth authentication and provides methods for all operations.

### Prerequisites

**1. Enable Network Access (REQUIRED)**

⚠️ **This skill requires network access to reach api.spotify.com**

In Claude Desktop, you must enable network egress:
- Go to **Settings** → **Developer** → **Allow network egress**
- Toggle it **ON** (blue)
- Under "Domain allowlist", choose either:
  - **"All domains"** (easiest), OR
  - **"Specified domains"** and add `api.spotify.com` (more secure/restricted)
- This allows the skill to make API calls to Spotify's servers

Without network access enabled, API calls will fail with connection errors.

**2. Install Dependencies**

```bash
pip install -r requirements.txt
```

Required packages:
- `requests>=2.31.0` - HTTP requests for Spotify Web API
- `python-dotenv>=1.0.0` - Environment variable management
- `cairosvg>=2.7.0` - SVG to PNG conversion for **image generation**
- `pillow>=10.0.0` - Image processing for **cover art creation**

> **💡 Note:** The `cairosvg` and `pillow` packages enable **image generation** - allowing this skill to create cover art images even though Claude cannot generate images natively!

### Basic Setup

The easiest way to initialize the client is using credentials from environment variables (loaded from `.env` file):

```python
from spotify_client import create_client_from_env

# Initialize client from environment variables (.env file)
client = create_client_from_env()

# If you have a refresh token, refresh the access token
if client.refresh_token:
    client.refresh_access_token()
```

Alternatively, you can manually provide credentials:

```python
from spotify_client import SpotifyClient

# Initialize with credentials directly
client = SpotifyClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    refresh_token="YOUR_REFRESH_TOKEN"  # if available
)

# Refresh to get current access token
if client.refresh_token:
    client.refresh_access_token()
```

### Common Operations

**List ALL user playlists (with pagination):**
```python
# Get all playlists - handles pagination automatically
all_playlists = []
offset = 0
limit = 50  # Max allowed per request

while True:
    playlists = client.get_user_playlists(limit=limit, offset=offset)
    if not playlists:
        break  # No more playlists
    all_playlists.extend(playlists)
    offset += limit
    if len(playlists) < limit:
        break  # Last page (fewer than limit returned)

print(f"Total playlists: {len(all_playlists)}")
for playlist in all_playlists:
    print(f"- {playlist['name']} ({playlist['tracks']['total']} tracks)")
```

**Create a new playlist:**
```python
playlist = client.create_playlist(
    name="My Awesome Playlist",
    description="A curated collection",
    public=True
)
```

**Search for tracks:**
```python
results = client.search_tracks(query="artist:The Beatles", limit=20)
```

**Add tracks to playlist:**
```python
client.add_tracks_to_playlist(
    playlist_id="playlist_123",
    track_ids=["track_1", "track_2", "track_3"]
)
```

## Playlist Management Workflows

### List All User Playlists

**Important:** Users may have more than 50 playlists. Always use pagination to get ALL playlists:

```python
# Get ALL playlists using pagination
all_playlists = []
offset = 0
limit = 50  # Spotify's max per request

while True:
    batch = client.get_user_playlists(limit=limit, offset=offset)
    if not batch:
        break  # No more playlists to fetch

    all_playlists.extend(batch)
    print(f"Fetched {len(batch)} playlists (total so far: {len(all_playlists)})")

    offset += limit
    if len(batch) < limit:
        break  # Last page - fewer results than limit means we're done

print(f"\n✓ Total playlists found: {len(all_playlists)}")

# Display all playlists with details
for i, playlist in enumerate(all_playlists, 1):
    print(f"{i}. {playlist['name']}")
    print(f"   Tracks: {playlist['tracks']['total']}")
    print(f"   Public: {playlist['public']}")
    print(f"   ID: {playlist['id']}")
```

## Playlist Creation Workflows

### By Artist/Band Name

Create a playlist containing all or most popular tracks by a specific artist:

```python
# STEP 1: Search for the artist by name
artists = client.search_artists(query="The Beatles", limit=1)
if not artists:
    print("Artist not found")
    # Handle error: artist doesn't exist or name is misspelled
else:
    artist_id = artists[0]['id']  # Get Spotify ID of first result

    # STEP 2: Get the artist's most popular tracks
    # Note: Spotify API returns up to 10 top tracks per artist
    tracks = client.get_artist_top_tracks(artist_id=artist_id)
    track_ids = [t['id'] for t in tracks]  # Extract just the track IDs

    # STEP 3: Create a new playlist and add the tracks
    playlist = client.create_playlist(name="The Beatles Collection")
    client.add_tracks_to_playlist(playlist['id'], track_ids)
    print(f"Created playlist with {len(track_ids)} tracks")
```

### By Theme/Mood

Create thematic playlists by searching for tracks matching mood keywords:

```python
# STEP 1: Define search queries for your theme
# Spotify search syntax: "genre:indie mood:chill" or "genre:indie year:2020-2024"
theme_queries = [
    "genre:indie mood:chill",      # Search for chill indie tracks
    "genre:indie year:2020-2024"   # Search for recent indie tracks
]

# STEP 2: Search for tracks matching each query
all_tracks = []
for query in theme_queries:
    results = client.search_tracks(query=query, limit=50)  # Get up to 50 per query
    all_tracks.extend(results)  # Combine results from all queries

# STEP 3: Remove duplicates (same track may match multiple queries)
# Use set() with track IDs to keep only unique tracks
unique_track_ids = list(set(t['id'] for t in all_tracks))

# STEP 4: Create playlist with unique tracks (limit to 100 for reasonable size)
playlist = client.create_playlist(name="Chill Indie Evening")
client.add_tracks_to_playlist(playlist['id'], unique_track_ids[:100])
print(f"Created playlist with {len(unique_track_ids[:100])} tracks")
```

### By Lyrics Content

Search for tracks with specific lyrical themes using Spotify's search:

```python
# STEP 1: Define keywords related to lyrical content
# Note: Spotify search indexes track/artist names and some metadata,
# not full lyrics, so results are based on title/description matching
queries = ["love", "heartbreak", "summer", "midnight"]

# STEP 2: Search for tracks matching each keyword
all_tracks = []
for keyword in queries:
    results = client.search_tracks(query=keyword, limit=20)  # 20 tracks per keyword
    all_tracks.extend(results)

# STEP 3: Remove duplicates (same track may match multiple keywords)
# Use set() with track IDs to keep only unique tracks
unique_track_ids = list(set(t['id'] for t in all_tracks))
print(f"Found {len(all_tracks)} total matches, {len(unique_track_ids)} unique tracks")

# STEP 4: Create playlist (limit to 100 tracks for reasonable size)
playlist = client.create_playlist(name="Love & Heartbreak")
client.add_tracks_to_playlist(playlist['id'], unique_track_ids[:100])
print(f"Created playlist with {len(unique_track_ids[:100])} unique tracks")
```

### From Specific Song List

Create a playlist from a user-provided list of track URIs or search terms:

```python
# STEP 1: Get the list of songs from the user
# User provides song names (can also use Spotify URIs like "spotify:track:...")
song_list = ["Shape of You", "Blinding Lights", "As It Was"]

# STEP 2: Search for each song and collect track IDs
track_ids = []
for song_name in song_list:
    results = client.search_tracks(query=song_name, limit=1)  # Get best match
    if results:
        track_ids.append(results[0]['id'])  # Add first result's ID
        print(f"✓ Found: {results[0]['name']} by {results[0]['artists'][0]['name']}")
    else:
        print(f"✗ Not found: {song_name}")  # Song doesn't exist or name is wrong

# STEP 3: Create playlist with found tracks
playlist = client.create_playlist(name="My Favorites")
if track_ids:
    client.add_tracks_to_playlist(playlist['id'], track_ids)
    print(f"Created playlist with {len(track_ids)}/{len(song_list)} tracks")
else:
    print("No tracks found - playlist is empty")
```

## 🎨 Cover Art Image Generation

> **⚡ UNIQUE CAPABILITY: This skill can generate images!**
>
> Claude cannot generate images natively, but this skill bypasses that limitation by creating custom SVG graphics and converting them to PNG images for Spotify playlist covers.

> **🚨 MANDATORY: USE THE COVER ART LLM GUIDE**
>
> **⚠️ DO NOT attempt to generate cover art without first reading the complete execution guide.**
>
> **➡️ READ THIS FILE FIRST: [references/COVER_ART_LLM_GUIDE.md](references/COVER_ART_LLM_GUIDE.md)**
>
> **This guide is REQUIRED and contains:**
> - Complete step-by-step execution instructions
> - How to analyze playlist content to determine appropriate colors
> - Genre-to-color and mood-to-color mapping tables
> - Typography rules and accessibility requirements
> - Edge case handling and quality checklist
>
> **Do not proceed with cover art generation without consulting this guide first.**

### ⚠️ Required Scope for Upload

**To upload cover art to Spotify, you MUST have the `ugc-image-upload` scope enabled:**

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Select your app
3. Ensure `ugc-image-upload` scope is included in your authorization
4. Re-run OAuth flow to get a new refresh token with this scope: `python get_refresh_token.py`
5. Update your `.env` file with the new refresh token

**Without this scope:** You'll get a 401 error when trying to upload. However, you can still **generate cover art images locally** and upload them manually via Spotify's web/mobile app.

**📖 Having trouble?** See [COVER_ART_TROUBLESHOOTING.md](COVER_ART_TROUBLESHOOTING.md) for detailed solutions.

### Basic Usage Example

**⚠️ Remember: Read [references/COVER_ART_LLM_GUIDE.md](references/COVER_ART_LLM_GUIDE.md) before generating cover art!**

```python
from cover_art_generator import CoverArtGenerator

# Initialize generator (uses same credentials as SpotifyClient)
art_gen = CoverArtGenerator(client_id, client_secret, access_token)

# Generate and upload cover art
# (Follow the LLM guide for how to determine appropriate colors)
art_gen.create_and_upload_cover(
    playlist_id=playlist['id'],
    title="Beast Mode",           # Main title (large text)
    subtitle="Gym",                # Optional subtitle
    gradient_start="#E63946",      # Colors determined from guide
    gradient_end="#1D1D1D",
    text_color="#FFFFFF"
)
```

**All cover art generation workflows, color selection guidance, and advanced features are documented in [references/COVER_ART_LLM_GUIDE.md](references/COVER_ART_LLM_GUIDE.md).**

## Advanced Operations

### Get Recommendations

```python
# Get AI-powered music recommendations based on seed artists/tracks/genres
recommendations = client.get_recommendations(
    seed_artists=["artist_id_1"],  # Spotify IDs of artists
    seed_tracks=["track_id_1"],    # Spotify IDs of tracks
    limit=50                       # Number of recommendations to get
)
# Returns: List of recommended tracks similar to the seeds
```

### Access User Profile

```python
# Get information about the current authenticated user
profile = client.get_current_user()
# Returns: user_id, display_name, email, followers, images, country, etc.
print(f"Logged in as: {profile['display_name']}")
print(f"User ID: {profile['id']}")
```

### Get User's Top Items

```python
# Get user's most played artists over different time periods
top_artists = client.get_top_items(
    item_type="artists",
    limit=20,
    time_range="medium_term"  # Options: short_term (~4 weeks), medium_term (~6 months), long_term (~years)
)
print(f"Top artist: {top_artists[0]['name']}")

# Get user's most played tracks
top_tracks = client.get_top_items(
    item_type="tracks",
    limit=20,
    time_range="short_term"  # Recent listening (last ~4 weeks)
)
print(f"Most played track: {top_tracks[0]['name']} by {top_tracks[0]['artists'][0]['name']}")
```

### Playback Control

```python
# STEP 1: Start playback of a playlist or album
client.start_playback(
    device_id="device_123",                      # Optional: specific device
    context_uri="spotify:playlist:playlist_id",  # What to play (playlist/album/artist URI)
    offset=0                                     # Optional: start at track 0
)

# STEP 2: Pause playback
client.pause_playback(device_id="device_123")

# STEP 3: Skip to next track
client.next_track(device_id="device_123")

# STEP 4: Check what's currently playing
current = client.get_currently_playing()
if current and current.get('item'):
    track = current['item']
    print(f"Now playing: {track['name']} by {track['artists'][0]['name']}")
else:
    print("Nothing is currently playing")
```

## Authentication & Credentials

See `references/authentication_guide.md` for detailed OAuth flow setup and credential management. Ensure credentials are available in environment variables or passed at initialization:

- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_REDIRECT_URI`
- `SPOTIFY_ACCESS_TOKEN` (optional, can use refresh token)
- `SPOTIFY_REFRESH_TOKEN` (for token refresh)

## API Reference

See `references/api_reference.md` for complete Spotify API endpoint documentation, rate limits, response formats, and error handling patterns.

## Scripts

### spotify_client.py

Comprehensive Python wrapper for all Spotify Web API operations. Handles authentication, token management, rate limiting, and provides methods for:
- Authentication and token refresh
- Playlist CRUD operations
- Search (tracks, artists, albums, playlists)
- Track/URI management
- User data access
- Playback control
- Recommendations engine

### playlist_creator.py

High-level utility for intelligent playlist creation from various sources (artist, theme, lyrics, song list). Encapsulates common workflows and handles track deduplication and limit management.

---

## For Developers Building Apps (Advanced)

**Note:** The features below are for developers building web applications, NOT for direct playlist creation tasks.

If the user is asking you to **build an application** or **export data**, see:
- `ADVANCED_USAGE.md` - Application development patterns
- `scripts/export_data.py` - Export Spotify data as JSON
- `SpotifyAPIWrapper` class - Error handling for production apps

**For playlist creation and music management, use the workflows above.**
