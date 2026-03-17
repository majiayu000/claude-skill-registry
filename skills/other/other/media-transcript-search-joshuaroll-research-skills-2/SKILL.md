---
name: media-transcript-search
description: Extract and search transcripts from multimedia sources (primarily YouTube). Allows finding specific topics within long content without watching the whole video.
---

# Multimedia Transcript Search Skill

This skill turns opaque video content into searchable text data, essential for analyzing speeches, lectures, and news clips.

## Capabilities

1.  **Get Transcript**: Download the full transcript of a YouTube video.
2.  **Keyword Search**: Find timestamps where specific keywords or phrases are mentioned.
3.  **Context Window**: Return surrounding text to understand the context of the mention.

## Usage

Run the python script `get_transcript.py`.

### Arguments

*   `video_id` (required): The YouTube Video ID (e.g., `dQw4w9WgXcQ`).
*   `--search` (optional): Keyword to find.
*   `--lang` (optional): Language code (default 'en').

### Example

```bash
# Get full transcript for a video
python3 get_transcript.py dQw4w9WgXcQ

# Find where "climate change" is discussed
python3 get_transcript.py dQw4w9WgXcQ --search "climate change"
```

## Dependencies

This skill requires the `youtube-transcript-api` library.
```bash
pip install youtube-transcript-api
```

## Output Format

A JSON object containing:
*   `video_id`
*   `transcript`: Full list of segments (if no search) OR
*   `matches`: List of segments matching the search term:
    *   `text`: The text segment.
    *   `start`: Start time (seconds).
    *   `duration`: Duration of segment.
    *   `url`: Direct URL to timestamp (e.g., `https://youtu.be/ID?t=123`).

## Tips for the Agent

*   **Fuzzy Matching**: The search is simple case-insensitive matching.
*   **Timestamps**: Always provide the `url` with the timestamp so the user can verify the context immediately.
