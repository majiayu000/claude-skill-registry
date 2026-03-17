---
name: youtube-full
cluster: community
description: "YouTube: video management, transcript extraction, channel analytics, comments, playlists, upload"
tags: ["youtube","video","transcripts","google"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "youtube video transcript channel analytics comment playlist upload"
---

## youtube-full

## Purpose
This skill provides tools for interacting with YouTube's API to handle video management, transcript extraction, channel analytics, comments, playlists, and uploads, enabling automation in scripts or applications.

## When to Use
Use this skill for tasks involving YouTube data, such as fetching video transcripts in content analysis, uploading user-generated videos, analyzing channel performance for reports, or managing playlists in media apps. Apply it when Google API access is available and tasks require real-time data extraction or manipulation.

## Key Capabilities
- Video management: Retrieve, search, or delete videos using YouTube Data API v3 endpoints like /youtube/v3/videos.
- Transcript extraction: Fetch captions for videos via the /youtube/v3/captions endpoint, supporting languages like English or auto-generated transcripts.
- Channel analytics: Access metrics such as view counts and subscriber data from /youtube/v3/channels, including parameters for date ranges.
- Comments: Read or post thread comments using /youtube/v3/commentThreads, with moderation flags for spam handling.
- Playlists: Create, update, or delete playlists via /youtube/v3/playlists, including adding video items.
- Upload: Handle video uploads with multipart POST to /youtube/v3/videos, requiring resumable sessions for large files.

## Usage Patterns
Invoke this skill via function calls in your AI agent's code, passing required parameters like video IDs or API keys. Always check for authentication first by setting $YOUTUBE_API_KEY as an environment variable. For example, structure requests in a loop for batch operations, like processing multiple video transcripts. Use JSON payloads for POST requests and query parameters for GET requests. Handle rate limits by adding delays between API calls, e.g., sleep for 1 second after every 10 requests.

## Common Commands/API
- To list videos: Use GET https://www.googleapis.com/youtube/v3/search?part=snippet&q=query&key=$YOUTUBE_API_KEY with query string parameters.
- For transcript extraction: GET https://www.googleapis.com/youtube/v3/captions?videoId=VIDEO_ID&key=$YOUTUBE_API_KEY, then parse the JSON response for text.
- Code snippet for fetching video details:
  ```python
  import requests; import os
  api_key = os.environ.get('YOUTUBE_API_KEY')
  response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=VIDEO_ID&key={api_key}')
  data = response.json()
  ```
- To upload a video: POST https://www.googleapis.com/upload/youtube/v3/videos?part=snippet,status with multipart/form-data, including fields like title and file.
- For channel analytics: GET https://www.googleapis.com/youtube/v3/channels?part=statistics&id=CHANNEL_ID&key=$YOUTUBE_API_KEY, returning JSON with metrics like viewCount.
- Playlist management: POST https://www.googleapis.com/youtube/v3/playlists?part=snippet with JSON body {"snippet": {"title": "New Playlist"}}.

## Integration Notes
Integrate by importing the skill in your AI agent's codebase and ensuring $YOUTUBE_API_KEY is set in the environment for OAuth or API key authentication. Use a config file like JSON for storing endpoint defaults, e.g., {"base_url": "https://www.googleapis.com/youtube/v3"}. For secure handling, avoid hardcoding keys; instead, use libraries like google-auth in Python. If using OAuth, redirect users for token exchange, but for simple API access, $YOUTUBE_API_KEY suffices. Test integrations in a sandbox environment to avoid quota exceedance.

## Error Handling
Check HTTP status codes in responses; for example, if status == 403, log "Quota exceeded" and retry after a delay. Handle specific YouTube errors like invalid video IDs (error code 404) by validating inputs before requests. Use try-except blocks in code for network issues:
```python
try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"Error: {err} - Check API key or parameters")
```
Implement exponential backoff for rate limit errors (e.g., 403 with quota message), waiting 2^x seconds before retrying up to 3 times. Log all errors with context, such as the API endpoint and parameters used.

## Usage Examples
1. Extract transcript for a specific video: First, set $YOUTUBE_API_KEY. Then, call the API with GET https://www.googleapis.com/youtube/v3/captions?videoId=VIDEO_ID&key=$YOUTUBE_API_KEY. In code, parse the response to extract text: import json; transcript = [item['text'] for item in response.json()['items']]. Save the output to a file for further processing.
2. Upload a video to a channel: Ensure $YOUTUBE_API_KEY is set and you have upload permissions. Use POST https://www.googleapis.com/upload/youtube/v3/videos with multipart data including the video file and JSON metadata like {"snippet": {"title": "Uploaded Video"}}. After upload, retrieve the video ID from the response and update its status if needed.

## Graph Relationships
- Relates to: google-api (for shared authentication and endpoints)
- Depends on: authentication-service (for handling $YOUTUBE_API_KEY)
- Connects to: video-processing skills (for post-extraction analysis)
- Integrates with: storage-services (for managing uploaded files)
