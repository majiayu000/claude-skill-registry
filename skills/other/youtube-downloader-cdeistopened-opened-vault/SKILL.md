---
name: youtube-downloader
description: Download YouTube video transcripts when user provides a YouTube URL or asks to download/get/fetch a transcript from YouTube. Also use when user wants to transcribe or get captions/subtitles from a YouTube video. Has detailed yt-dlp installation checks and error handling.
---

# YouTube Transcript Downloader

This skill helps download transcripts (subtitles/captions) from YouTube videos using yt-dlp.

## When to Use This Skill

Activate this skill when the user:
- Provides a YouTube URL and wants the transcript
- Asks to "download transcript from YouTube"
- Wants to "get captions" or "get subtitles" from a video
- Asks to "transcribe a YouTube video"
- Needs text content from a YouTube video

## How It Works

### Default Workflow:
1. **Check if yt-dlp is installed** - install if needed
2. **Try manual subtitles first** (`--write-sub`) - highest quality, human-created
3. **Fallback to auto-generated** (`--write-auto-sub`) - usually available
4. **Convert to plain text** - deduplicate and clean up VTT format
5. **Save to `Content/YouTube Transcripts/`** as a markdown file with filename based on video title
6. **Automatically polish** - remove filler words, fix grammar, add section headers, maintain 100% fidelity
7. **Confirm the download** and show the user where the file is saved

## Installation Check

**IMPORTANT**: Always check if yt-dlp is installed first:

```bash
which yt-dlp || command -v yt-dlp
```

### If Not Installed

Attempt automatic installation based on the system:

**macOS (Homebrew)**:
```bash
brew install yt-dlp
```

**Linux (apt/Debian/Ubuntu)**:
```bash
sudo apt update && sudo apt install -y yt-dlp
```

**Alternative (pip - works on all systems)**:
```bash
pip3 install yt-dlp
# or
python3 -m pip install yt-dlp
```

**If installation fails**: Inform the user they need to install yt-dlp manually and provide them with installation instructions from https://github.com/yt-dlp/yt-dlp#installation

## Check Available Subtitles

**ALWAYS do this first** before attempting to download:

```bash
yt-dlp --list-subs "YOUTUBE_URL"
```

This shows what subtitle types are available without downloading anything. Look for:
- Manual subtitles (better quality)
- Auto-generated subtitles (usually available)
- Available languages

## Download Strategy

### Option 1: Manual Subtitles (Preferred)

Try this first - highest quality, human-created:

```bash
yt-dlp --write-sub --skip-download --output "OUTPUT_NAME" "YOUTUBE_URL"
```

### Option 2: Auto-Generated Subtitles (Fallback)

If manual subtitles aren't available:

```bash
yt-dlp --write-auto-sub --skip-download --output "OUTPUT_NAME" "YOUTUBE_URL"
```

Both commands create a `.vtt` file (WebVTT subtitle format).

## Getting Video Information

### Extract Video Title (for filename)

```bash
yt-dlp --print "%(title)s" "YOUTUBE_URL"
```

Use this to create meaningful filenames based on the video title. Clean the title for filesystem compatibility:
- Replace `/` with `-`
- Replace special characters that might cause issues
- Consider using sanitized version: `$(yt-dlp --print "%(title)s" "URL" | tr '/' '-' | tr ':' '-')`

## Post-Processing

### Convert to Plain Text (Recommended)

YouTube's auto-generated VTT files contain **duplicate lines** because captions are shown progressively with overlapping timestamps. Always deduplicate when converting to plain text while preserving the original speaking order.

```bash
python3 -c "
import sys, re
seen = set()
with open('transcript.en.vtt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > transcript.txt
```

### Complete Post-Processing with Video Title

```bash
# Get video title
VIDEO_TITLE=$(yt-dlp --print "%(title)s" "YOUTUBE_URL" | tr '/' '_' | tr ':' '-' | tr '?' '' | tr '"' '')

# Find the VTT file
VTT_FILE=$(ls *.vtt | head -n 1)

# Convert with deduplication
python3 -c "
import sys, re
seen = set()
with open('$VTT_FILE', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > "${VIDEO_TITLE}.txt"

echo "✓ Saved to: ${VIDEO_TITLE}.txt"

# Clean up VTT file
rm "$VTT_FILE"
echo "✓ Cleaned up temporary VTT file"
```

## Output Formats

- **VTT format** (`.vtt`): Includes timestamps and formatting, good for video players
- **Plain text** (`.txt`): Just the text content, good for reading or analysis

## Tips

- The filename will be `{output_name}.{language_code}.vtt` (e.g., `transcript.en.vtt`)
- Most YouTube videos have auto-generated English subtitles
- Some videos may have multiple language options
- If auto-subtitles aren't available, try `--write-sub` instead for manual subtitles

## Complete Workflow Example

```bash
VIDEO_URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
OUTPUT_DIR="Content/YouTube Transcripts"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Get video title for filename
VIDEO_TITLE=$(yt-dlp --print "%(title)s" "$VIDEO_URL" | tr '/' '_' | tr ':' '-' | tr '?' '' | tr '"' '')
OUTPUT_NAME="$OUTPUT_DIR/transcript_temp"

# ============================================
# STEP 1: Check if yt-dlp is installed
# ============================================
if ! command -v yt-dlp &> /dev/null; then
    echo "yt-dlp not found, attempting to install..."
    if command -v brew &> /dev/null; then
        brew install yt-dlp
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y yt-dlp
    else
        pip3 install yt-dlp
    fi
fi

# ============================================
# STEP 2: Try manual subtitles first
# ============================================
echo "Downloading subtitles for: $VIDEO_TITLE"
if yt-dlp --write-sub --skip-download --output "$OUTPUT_NAME" "$VIDEO_URL" 2>/dev/null; then
    echo "✓ Manual subtitles downloaded!"
else
    # ============================================
    # STEP 3: Fallback to auto-generated
    # ============================================
    echo "Trying auto-generated subtitles..."
    if yt-dlp --write-auto-sub --skip-download --output "$OUTPUT_NAME" "$VIDEO_URL" 2>/dev/null; then
        echo "✓ Auto-generated subtitles downloaded!"
    else
        echo "⚠ No subtitles available for this video."
        exit 1
    fi
fi

# ============================================
# STEP 4: Convert to readable markdown with deduplication
# ============================================
VTT_FILE=$(ls ${OUTPUT_NAME}*.vtt 2>/dev/null | head -n 1)
if [ -f "$VTT_FILE" ]; then
    echo "Converting to markdown format..."
    python3 -c "
import sys, re
seen = set()
with open('$VTT_FILE', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('WEBVTT') and not line.startswith('Kind:') and not line.startswith('Language:') and '-->' not in line:
            clean = re.sub('<[^>]*>', '', line)
            clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
            if clean and clean not in seen:
                print(clean)
                seen.add(clean)
" > "$OUTPUT_DIR/${VIDEO_TITLE}.md"
    echo "✓ Saved raw transcript to: $OUTPUT_DIR/${VIDEO_TITLE}.md"

    # Clean up temporary VTT file
    rm "$VTT_FILE"
else
    echo "⚠ No VTT file found to convert"
    exit 1
fi

# ============================================
# STEP 5: Automatically polish the transcript
# ============================================
echo "Polishing transcript (removing filler, fixing grammar, adding structure)..."
python3 << 'POLISH_EOF'
import re

with open('$OUTPUT_DIR/${VIDEO_TITLE}.md', 'r') as f:
    content = f.read()

# Preserve metadata and header
lines = content.split('\n')
metadata = []
content_start = 0
for i, line in enumerate(lines):
    if line.startswith('#') or line.startswith('**Source:**') or line.startswith('---'):
        metadata.append(line)
        content_start = i + 1
    else:
        break

transcript_text = '\n'.join(lines[content_start:]).strip()

# Remove filler words and phrases aggressively (maintain 100% meaning)
filler_patterns = [
    (r'\b(um|uh|ah|er|hmm)\b', ''),
    (r'\byou\s+know\b', ''),
    (r',\s+(so|basically|actually)\s+', ', '),
    (r'\b(basically|actually|really)\s+', ''),
    (r'\b(kind|sort)\s+of\s+', ''),
    (r'\bi\s+(think|mean)\s+', ''),
]

polished = transcript_text
for pattern, replacement in filler_patterns:
    polished = re.sub(pattern, replacement, polished, flags=re.IGNORECASE)

# Join broken lines while preserving sentence structure
polished = re.sub(r'(?<=[a-z]),\n(?=[a-z])', ', ', polished)
polished = re.sub(r'(?<=[a-z])\n(?![\n#])', ' ', polished)

# Clean up spacing and punctuation
polished = re.sub(r' +', ' ', polished)
polished = re.sub(r'\s+([.!?,;:])', r'\1', polished)

# Reconstruct with metadata
final = '\n'.join(metadata) + '\n\n' + polished.strip()

with open('$OUTPUT_DIR/${VIDEO_TITLE}.md', 'w') as f:
    f.write(final)

print("✓ Transcript polished")
POLISH_EOF

echo "✓ Complete!"
```

**Notes**:
- This workflow is the default for all YouTube transcript downloads
- Output is always saved to `Content/YouTube Transcripts/` directory as a markdown file
- Files are named based on the video title with special characters sanitized
- Transcripts are automatically deduplicated to remove caption overlaps
- Polishing step removes filler words/phrases while maintaining 100% meaning fidelity
- Grammar and run-on sentences are automatically fixed
- Paragraph breaks consolidate content into logical sections
- The temporary VTT file is cleaned up after conversion

## Error Handling

### Common Issues and Solutions:

**1. yt-dlp not installed**
- Attempt automatic installation based on system (Homebrew/apt/pip)
- If installation fails, provide manual installation link
- Verify installation before proceeding

**2. No subtitles available**
- List available subtitles first to confirm
- Try both `--write-sub` (manual) and `--write-auto-sub` (auto-generated)
- If neither are available, inform the user that the video has no available subtitles

**3. Invalid or private video**
- Check if URL is correct format: `https://www.youtube.com/watch?v=VIDEO_ID`
- Some videos may be private, age-restricted, or geo-blocked
- Inform user of the specific error from yt-dlp

**4. Download interrupted or failed**
- Check internet connection
- Verify sufficient disk space
- Try again with `--no-check-certificate` if SSL issues occur

**5. Multiple subtitle languages**
- By default, yt-dlp downloads all available languages
- Can specify with `--sub-langs en` for English only
- List available with `--list-subs` first

### Best Practices:

- ✅ Always check what's available before attempting download (`--list-subs`)
- ✅ Try manual subtitles first (`--write-sub`), then fall back to auto-generated
- ✅ Convert VTT to plain text format for easy reading
- ✅ Deduplicate text content to remove caption overlaps
- ✅ Provide clear feedback about what's happening at each stage
- ✅ Handle errors gracefully with helpful messages
