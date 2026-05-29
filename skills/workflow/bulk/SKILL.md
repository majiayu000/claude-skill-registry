---
name: bulk
description: Transcribe ALL videos from a TikTok profile. Use when you want to process an entire profile's content.
user_invocable: true
---

# Bulk Video Transcription

This command processes ALL videos from a TikTok profile - scraping URLs, downloading audio, transcribing, and creating organized summaries.

## Workflow

### Step 1: Get Profile URL

Ask the user:
> What TikTok profile do you want to process?
>
> Example: `https://www.tiktok.com/@agentic.james`

### Step 2: Get Limit (Optional)

Ask the user:
> How many videos do you want to process?
>
> Options:
> - **All** - Process every video on the profile
> - **Number** - Process only the first N videos (e.g., "5" or "10")

### Step 3: Verify Environment

Check that the project is set up:

```bash
cd /path/to/project
source .venv/bin/activate
which yt-dlp
```

If not set up, tell user to run `/start` first.

### Step 4: Scrape Video URLs

Run the scraper to discover all videos:

```bash
source .venv/bin/activate && python -c "
from short_form_scraper.scraper.tiktok import TikTokScraper

scraper = TikTokScraper('PROFILE_URL_HERE')
videos = list(scraper.get_video_urls(limit=LIMIT_OR_NONE))

print(f'Found {len(videos)} videos:')
for i, v in enumerate(videos, 1):
    print(f'{i}. {v.title[:60]}...' if len(v.title) > 60 else f'{i}. {v.title}')
    print(f'   URL: {v.url}')
    print()
"
```

Show the user the list and confirm they want to proceed.

### Step 5: Download and Transcribe Each Video

For each video, run:

```bash
source .venv/bin/activate && python -c "
from short_form_scraper.scraper.tiktok import TikTokScraper
from short_form_scraper.downloader.video import VideoDownloader
from short_form_scraper.transcriber.whisper import WhisperTranscriber
from pathlib import Path
import json

# Initialize components
scraper = TikTokScraper('PROFILE_URL_HERE')
downloader = VideoDownloader()
transcriber = WhisperTranscriber()

# Create output directories
Path('transcripts').mkdir(exist_ok=True)
Path('state').mkdir(exist_ok=True)

# Get videos
videos = list(scraper.get_video_urls(limit=LIMIT_OR_NONE))

for i, metadata in enumerate(videos, 1):
    print(f'[{i}/{len(videos)}] Processing: {metadata.title[:50]}...')

    try:
        # Download audio
        audio_path = downloader.download(metadata.url, Path(f'state/audio_{metadata.id}'))
        print(f'  Downloaded: {audio_path}')

        # Transcribe
        transcript = transcriber.transcribe(audio_path)
        print(f'  Transcribed: {len(transcript)} chars')

        # Save transcript with metadata
        transcript_file = Path('transcripts') / f'{metadata.id}.txt'
        content = f'''Video ID: {metadata.id}
Title: {metadata.title}
URL: {metadata.url}
Duration: {metadata.duration}s

--- TRANSCRIPT ---

{transcript}
'''
        transcript_file.write_text(content)
        print(f'  Saved: {transcript_file}')

        # Clean up audio file to save space
        audio_path.unlink()

    except Exception as e:
        print(f'  ERROR: {e}')

    print()

print('Done! Transcripts saved to transcripts/')
"
```

### Step 6: Summarize Transcripts (Claude Code)

After all transcripts are generated, YOU (Claude Code) will:

1. Read each transcript file from `transcripts/` directory
2. For each transcript, analyze and extract:
   - **Topic**: A descriptive 2-4 word kebab-case topic name (e.g., "agentic-engineering", "context-management")
   - **Summary**: One-sentence summary of the main point
   - **Key Tips**: 3-5 actionable bullet points
   - **Details**: Additional context

3. Create organized output in `summaries/` directory:
   ```
   summaries/
   ├── INDEX.md
   ├── {topic-name}/
   │   └── {slugified-title}.md
   ```

   **IMPORTANT: Filename from Video Title**
   - Extract the video title from the yt-dlp metadata (stored in the transcript file header)
   - Convert to kebab-case slug: lowercase, spaces to dashes, remove special chars
   - Example: "How to Use Context Windows" → `how-to-use-context-windows.md`
   - Example: "Claude Code Tips & Tricks!" → `claude-code-tips-tricks.md`

4. Each summary file format:
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

5. Create INDEX.md listing all summaries grouped by topic:
   ```markdown
   # Video Summaries Index

   ## {Topic Name}
   - [{Video Title}](./{topic-name}/{slugified-title}.md)
   ```

### Step 7: Report Results

After completion, report:
- Total videos found
- Successfully transcribed
- Failed (if any)
- Topics identified
- Output locations

## Error Handling

- If a video fails, log the error and continue with the next one
- Save partial progress (transcripts saved immediately)
- User can re-run and existing transcripts won't be re-downloaded
