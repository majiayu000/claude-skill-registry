---
name: media-transcript-search
description: Extract and search transcripts from multimedia sources (primarily YouTube). Allows finding specific topics within long content without watching the whole video.
---

# Multimedia Transcript Search Skill

This skill turns opaque video content into searchable text data, essential for analyzing speeches, lectures, and news clips.

## Capabilities

1.  **Get Transcript**: Download the full transcript of a YouTube video or **Playlist**.
2.  **Keyword Search**: Find timestamps where specific keywords or phrases are mentioned.
3.  **Metadata**: Automatically fetches Video Title to context script.
4.  **Export**: Dump transcripts as `.txt` or `.srt` for external use.

## Usage

Run the python script `get_transcript.py`.

### Arguments

*   `id` (required): The YouTube Video ID (e.g., `dQw4w9WgXcQ`) or Playlist ID.
*   `--playlist` (optional): Set if the ID is a playlist. Limits to first 10 videos.
*   `--search` (optional): Keyword to find.
*   `--format` (optional): "json" (default), "txt", or "srt".

### Example

```bash
# Find "climate change" in a Playlist
python3 get_transcript.py PLAYLIST_ID --playlist --search "climate change"

# Export a clean text script for a video
python3 get_transcript.py VIDEO_ID --format txt
```

## Tips for the Agent

*   **Playlist Limits**: Playlists are limited to the first 10 videos to ensure speed.
*   **SRT Format**: Use `srt` if you need to re-upload captions or import into a video editor.
