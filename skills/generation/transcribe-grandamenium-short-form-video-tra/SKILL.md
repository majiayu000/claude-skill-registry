---
name: transcribe
description: Transcribe specific video URL(s). Use when you have one or more TikTok video URLs to process.
user_invocable: true
---

# Transcribe Specific Videos

This command processes specific TikTok videos by URL - no need to scrape an entire profile.

## Workflow

### Step 1: Get Video URLs

Ask the user:
> Paste the TikTok video URL(s) you want to transcribe.
>
> You can paste one URL or multiple URLs (one per line):
> ```
> https://www.tiktok.com/@username/video/123456789
> https://www.tiktok.com/@username/video/987654321
> ```

Parse the URLs from the user's message. Extract any URLs that match TikTok video patterns:
- `https://www.tiktok.com/@username/video/ID`
- `https://tiktok.com/@username/video/ID`
- `https://vm.tiktok.com/SHORTCODE`

### Step 2: Verify Environment

Check that the project is set up:

```bash
cd /path/to/project
source .venv/bin/activate 2>/dev/null || echo "venv not found"
```

If venv doesn't exist, tell user to run `/start` first.

### Step 3: Process Each Video

For each URL provided, run:

```bash
source .venv/bin/activate && python -c "
from short_form_scraper.scraper.tiktok import TikTokScraper
from short_form_scraper.downloader.video import VideoDownloader
from short_form_scraper.transcriber.whisper import WhisperTranscriber
from pathlib import Path

# Initialize
scraper = TikTokScraper('https://www.tiktok.com/@placeholder')  # Just for metadata fetching
downloader = VideoDownloader()
transcriber = WhisperTranscriber()

# Create directories
Path('transcripts').mkdir(exist_ok=True)
Path('state').mkdir(exist_ok=True)

# Video URL
video_url = 'VIDEO_URL_HERE'

print(f'Processing: {video_url}')

# Get metadata
metadata = scraper.get_single_video_metadata(video_url)
print(f'Title: {metadata.title}')
print(f'Duration: {metadata.duration}s')

# Download
audio_path = downloader.download(metadata.url, Path(f'state/audio_{metadata.id}'))
print(f'Downloaded audio: {audio_path}')

# Transcribe
transcript = transcriber.transcribe(audio_path)
print(f'Transcribed: {len(transcript)} characters')

# Save
transcript_file = Path('transcripts') / f'{metadata.id}.txt'
content = f'''Video ID: {metadata.id}
Title: {metadata.title}
URL: {metadata.url}
Duration: {metadata.duration}s

--- TRANSCRIPT ---

{transcript}
'''
transcript_file.write_text(content)
print(f'Saved: {transcript_file}')

# Cleanup audio
audio_path.unlink()
print('Done!')
"
```

Run this for each URL the user provided.

### Step 4: Summarize Transcripts (Claude Code)

After transcripts are generated, YOU (Claude Code) will:

1. Read each new transcript file from `transcripts/`
2. Analyze and extract:
   - **Topic**: 2-4 word kebab-case topic name
   - **Summary**: One-sentence summary
   - **Key Tips**: 3-5 actionable bullet points
   - **Details**: Additional context

3. Create summary files in `summaries/{topic}/{slugified-title}.md`:

   **IMPORTANT: Filename from Video Title**
   - Extract the video title from the yt-dlp metadata (stored in transcript header as "Title: ...")
   - Convert to kebab-case slug: lowercase, spaces to dashes, remove special chars
   - Example: "How to Use Context Windows" → `how-to-use-context-windows.md`
   - Example: "Claude Code Tips & Tricks!" → `claude-code-tips-tricks.md`
   ```markdown
   ---
   video_id: {id}
   title: {title}
   url: {url}
   topic: {topic}
   ---

   # {Title}

   ## Summary
   {one-sentence summary}

   ## Key Tips
   - {tip 1}
   - {tip 2}
   - {tip 3}

   ## Details
   {additional context}

   ## Full Transcript
   {original transcript}
   ```

4. Update INDEX.md with the new summaries

### Step 5: Show Results

Display:
- Video title and URL
- Transcript location
- Summary location
- Key tips extracted

## Example

User: `/transcribe`

Claude: What TikTok video URLs would you like to transcribe?

User:
```
https://www.tiktok.com/@agentic.james/video/7597629199486029070
https://www.tiktok.com/@agentic.james/video/7597614123362323767
```

Claude: [Processes each video, creates transcripts and summaries]

## Handling Multiple URLs

When multiple URLs are provided:
1. Process them sequentially
2. Report progress: "[1/3] Processing..."
3. Continue even if one fails
4. At the end, report success/failure for each
