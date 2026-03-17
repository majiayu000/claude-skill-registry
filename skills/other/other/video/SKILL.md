---
description: Generate AI videos from text prompts or images. Supports Google Veo 3.1 and Pollinations.ai (free). Use when generating video, creating animations, text-to-video, AI video, video generation, make clip, animate.
allowed-tools: Read, Bash, Glob
context: fork
---

# Video Generation Skill

Generate videos from text prompts (or images) using AI models. Video generation is asynchronous - Google Veo requires polling for completion.

## Provider Fallback Chain (Follow This Order)

```
Tier 1: Google Veo 3.1 (PAID, billing required) ─── Best quality, audio ──┐
        ↓ on error                                                         │
Tier 2: Pollinations.ai (FREE, no key) ───────────────────────────────────┘
```

**Note**: Unlike image generation, there are no free Gemini native video models. Veo requires billing. Pollinations provides a free fallback.

## Workflow

### Step 1: Parse User Request

Extract from the user's prompt:
- **Description**: What the video should show
- **Duration**: Desired length (Veo: 5-8 seconds, Pollinations: 4-10 seconds)
- **Style**: Cinematic, animation, documentary, etc.
- **Source image**: Optional image to use as starting frame (image-to-video, Veo only)
- **Output path**: Where to save (default: `./generated-media/`)

### Step 2: Prepare Output Directory

```bash
mkdir -p ./generated-media
```

### Step 3: Load API Key from .env

```bash
# Source .env if it exists (for GEMINI_API_KEY)
if [ -f .env ]; then
  export $(grep -E '^GEMINI_API_KEY=' .env | xargs)
fi

# Also check parent dirs (monorepo support)
if [ -z "$GEMINI_API_KEY" ] && [ -f ../.env ]; then
  export $(grep -E '^GEMINI_API_KEY=' ../.env | xargs)
fi
```

### Step 4: Generate Video (Fallback Chain)

#### Tier 1: Google Veo 3.1 (PAID, requires GEMINI_API_KEY + billing)

Available models:
- `veo-3.1-fast-generate-preview` — Fast, ~$0.15/sec (720p/1080p)
- `veo-3.1-generate-preview` — Standard with audio, ~$0.40/sec (default)

**IMPORTANT**: Veo is asynchronous. You must:
1. Submit the generation request
2. Poll the operation endpoint every 10 seconds
3. Download the video when done

**Cost warning**: Before generating, tell the user the estimated cost (~$0.75-3.20 per clip) and confirm they want to proceed.

```bash
TIMESTAMP=$(date +%s)
MODEL="veo-3.1-generate-preview"
PROMPT="YOUR_PROMPT_HERE"
OUTFILE="generated-media/video-${TIMESTAMP}.mp4"
TMPFILE="/tmp/gemini-vid-response-${TIMESTAMP}.json"
SUCCESS=false

if [ -n "$GEMINI_API_KEY" ]; then
  echo "Starting video generation with $MODEL..."
  echo "Estimated cost: ~$2.00-3.20 for a 5-8 second clip"

  # Step 1: Start generation (returns operation ID)
  curl -s -X POST \
    "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:predictLongRunning" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H "Content-Type: application/json" \
    -o "$TMPFILE" \
    -d "{
      \"instances\": [{
        \"prompt\": \"${PROMPT}\"
      }]
    }"

  # Extract operation name
  OPERATION=$(python3 -c "
import json, sys
with open('$TMPFILE') as f:
    data = json.load(f)
if 'error' in data:
    print(f'Error: {data[\"error\"][\"message\"][:200]}', file=sys.stderr)
    sys.exit(1)
print(data.get('name', ''))
" 2>/dev/null)

  if [ -n "$OPERATION" ] && [ "$OPERATION" != "" ]; then
    echo "Video generation started: $OPERATION"
    echo "Polling for completion (this may take 1-3 minutes)..."

    # Step 2: Poll until done
    MAX_POLLS=30  # 5 minutes max
    POLL_COUNT=0
    while [ $POLL_COUNT -lt $MAX_POLLS ]; do
      sleep 10
      POLL_COUNT=$((POLL_COUNT + 1))

      curl -s \
        "https://generativelanguage.googleapis.com/v1beta/${OPERATION}" \
        -H "x-goog-api-key: $GEMINI_API_KEY" \
        -o "$TMPFILE"

      IS_DONE=$(python3 -c "
import json, sys
with open('$TMPFILE') as f:
    data = json.load(f)
print(data.get('done', False))
" 2>/dev/null)

      if [ "$IS_DONE" = "True" ]; then
        echo "Video generation complete!"

        # Step 3: Extract video URI and download
        VIDEO_URI=$(python3 -c "
import json, sys
with open('$TMPFILE') as f:
    data = json.load(f)
try:
    uri = data['response']['generateVideoResponse']['generatedSamples'][0]['video']['uri']
    print(uri)
except (KeyError, IndexError):
    print('', file=sys.stderr)
    sys.exit(1)
" 2>/dev/null)

        if [ -n "$VIDEO_URI" ]; then
          curl -s -L -o "$OUTFILE" \
            "$VIDEO_URI" \
            -H "x-goog-api-key: $GEMINI_API_KEY"
          SUCCESS=true
          echo "Generated with Veo 3.1 (paid)"
        else
          echo "ERROR: Could not extract video URI from response"
        fi
        break
      fi

      echo "  Still generating... (${POLL_COUNT}/${MAX_POLLS})"
    done

    if [ $POLL_COUNT -ge $MAX_POLLS ]; then
      echo "WARNING: Video generation timed out after 5 minutes"
      echo "Operation: $OPERATION"
      echo "You can check status later with:"
      echo "  curl -s 'https://generativelanguage.googleapis.com/v1beta/${OPERATION}' -H 'x-goog-api-key: \$GEMINI_API_KEY'"
    fi
  else
    echo "Veo failed to start (likely billing not enabled)"
  fi

  rm -f "$TMPFILE"
fi
```

If Tier 1 fails (no key, billing not enabled, or generation error), continue to Tier 2.

#### Tier 2: Pollinations.ai

Free video models: `seedance` (best quality), `wan` (image-to-video with audio), `grok-video`
Paid video models: `veo` (Google Veo 3.1 Fast)

**Note**: `gen.pollinations.ai` requires a free API key (register at https://pollinations.ai). Video uses the same `/image/` endpoint but returns `video/mp4` for video models.

```bash
if [ "$SUCCESS" != "true" ]; then
  echo "Trying Pollinations.ai video..."
  ENCODED_PROMPT=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''${PROMPT}'''))")
  POLL_MODEL="seedance"  # Free, good quality

  # Try authenticated endpoint first
  if [ -n "${POLLINATIONS_API_KEY:-}" ]; then
    curl -s -L --max-time 180 \
      -H "Authorization: Bearer $POLLINATIONS_API_KEY" \
      -o "$OUTFILE" \
      "https://gen.pollinations.ai/image/${ENCODED_PROMPT}?model=${POLL_MODEL}"
  else
    # Anonymous endpoint (may be unreliable)
    curl -s -L --max-time 180 \
      -o "$OUTFILE" \
      "https://image.pollinations.ai/prompt/${ENCODED_PROMPT}?model=${POLL_MODEL}"
  fi

  # Verify it's actually a video file
  if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
    FILETYPE=$(file -b "$OUTFILE" | head -1)
    if echo "$FILETYPE" | grep -qiE "video|MP4|MPEG|ISO Media|QuickTime"; then
      SUCCESS=true
      echo "Generated with Pollinations.ai (free)"
    else
      echo "Pollinations returned non-video: $FILETYPE"
      rm -f "$OUTFILE"
    fi
  fi
fi
```

### Step 5: Verify Output

```bash
if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
  file "$OUTFILE"
  SIZE=$(du -h "$OUTFILE" | cut -f1)
  echo "Video generated successfully: $OUTFILE ($SIZE)"
  echo "Play with: open '$OUTFILE'"
else
  echo "ERROR: All providers failed. Possible causes:"
  echo "  - Veo: Billing not enabled or quota exceeded"
  echo "  - Pollinations: Service temporarily down"
  echo ""
  echo "Solutions:"
  echo "  1. Enable billing at https://aistudio.google.com/ for Veo"
  echo "  2. Try again in a few minutes (Pollinations may recover)"
  echo "  3. Consider /sw-media:remotion for programmatic video (no AI, no API key)"
fi
```

### Step 6: Report Result

Tell the user:
- File path to the generated video
- Which provider/model was used
- Video duration (if known)
- Cost: estimate (Veo: ~$0.75-3.20) or "free" (Pollinations)
- Playback: `open file.mp4` (macOS), `xdg-open file.mp4` (Linux)

## Image-to-Video (Google Veo Only)

If the user provides a source image, use image-to-video mode:

```bash
# Convert image to base64
IMAGE_B64=$(base64 -i source-image.png)

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-generate-preview:predictLongRunning" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -o "$TMPFILE" \
  -d "{
    \"instances\": [{
      \"prompt\": \"${PROMPT}\",
      \"image\": {
        \"bytesBase64Encoded\": \"${IMAGE_B64}\"
      }
    }]
  }"
# Then poll as above
```

## Error Handling

| Error | Action |
|-------|--------|
| `GEMINI_API_KEY` not set | Skip Veo, use Pollinations only |
| Veo billing not enabled | Auto-fallback to Pollinations |
| Generation timed out | Report operation ID so user can check later |
| Pollinations 502/timeout | Report all providers failed, suggest Remotion |
| Content policy block | Report prompt was blocked, suggest rewording |

## Cost Awareness

**IMPORTANT**: Video generation costs money with Google Veo. Always inform the user before generating:

| Model | Cost | Duration |
|-------|------|----------|
| Veo 3.1 Fast (720p) | ~$0.15/sec = ~$0.75-1.20 per video | 5-8 sec |
| Veo 3.1 Standard | ~$0.40/sec = ~$2.00-3.20 per video | 5-8 sec |
| Pollinations | Free | 4-10 sec |

Before generating with Google Veo, confirm: "This will cost approximately $X. Proceed?"

## Setup Instructions (Show When No API Key Found)

If no `GEMINI_API_KEY` is set, inform the user:

> **Using free Pollinations.ai provider** (rate limited, shorter clips).
>
> For higher quality video with audio, set up Google Veo 3.1:
> 1. Go to https://aistudio.google.com/
> 2. Create or select a project with billing enabled
> 3. Generate an API key
> 4. Add to your `.env` file: `GEMINI_API_KEY=your-key-here`
>
> The same key works for both image AND video generation.
> Video costs ~$0.75-3.20 per clip depending on model/resolution.
>
> For programmatic video (no AI, no API key), try `/sw-media:remotion`.

## Activation Keywords

generate video, create video, make video, AI video, text-to-video, video generation, create animation, make clip, generate clip, animate, create movie, video from text, video from image
