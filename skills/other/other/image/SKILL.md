---
description: Generate AI images from text prompts. Supports Google Gemini (free) and Pollinations.ai (free). Use when generating images, creating visuals, AI art, text-to-image, image generation, create picture, make illustration, generate photo.
allowed-tools: Read, Bash, Glob
context: fork
---

# Image Generation Skill

Generate images from text prompts using AI models. Uses a 3-tier fallback chain to maximize reliability.

## Provider Fallback Chain (Follow This Order)

```
Tier 1: Gemini Native (FREE) ─── gemini-2.5-flash-image ──┐
        ↓ on error                                         │
        gemini-3-pro-image-preview ────────────────────────┤
        ↓ on error                                         │
Tier 2: Pollinations.ai (FREE, no key) ───────────────────┤
        ↓ on error                                         │
Tier 3: Imagen 4 (PAID, billing required) ────────────────┘
```

**Key**: Gemini native models generate images via the same `generateContent` API used for text - they're FREE with a daily quota. Imagen 4 uses a separate paid `:predict` endpoint.

## Workflow

### Step 1: Parse User Request

Extract from the user's prompt:
- **Subject**: What to generate (e.g., "a sunset over mountains")
- **Style**: Photorealistic, illustration, painting, etc. (default: photorealistic)
- **Output path**: Where to save (default: `./generated-media/`)
- **Count**: How many images (default: 1)

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

### Step 4: Generate Image (Fallback Chain)

**IMPORTANT**: Try each provider in order. On ANY error (quota, billing, network), move to the next tier. Write API responses to temp files to avoid JSON parsing issues with large base64 payloads.

#### Tier 1: Gemini Native Free (requires GEMINI_API_KEY)

Models (try in order):
1. `gemini-2.5-flash-image` - Fast, good quality
2. `gemini-3-pro-image-preview` - Best quality, slower

```bash
TIMESTAMP=$(date +%s)
PROMPT="YOUR_PROMPT_HERE"
OUTFILE="generated-media/image-${TIMESTAMP}.png"
TMPFILE="/tmp/gemini-img-response-${TIMESTAMP}.json"

if [ -n "$GEMINI_API_KEY" ]; then
  # Try gemini-2.5-flash-image first, then gemini-3-pro-image-preview
  for MODEL in "gemini-2.5-flash-image" "gemini-3-pro-image-preview"; do
    echo "Trying $MODEL..."

    curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -o "$TMPFILE" \
      -d "{
        \"contents\": [{
          \"parts\": [{\"text\": \"${PROMPT}\"}]
        }],
        \"generationConfig\": {
          \"responseModalities\": [\"TEXT\", \"IMAGE\"]
        }
      }"

    # Check for error in response
    if python3 -c "
import json, sys, base64
with open('$TMPFILE') as f:
    data = json.load(f)
if 'error' in data:
    print(f'Error: {data[\"error\"][\"message\"][:200]}', file=sys.stderr)
    sys.exit(1)
# Extract image from response parts
for candidate in data.get('candidates', []):
    for part in candidate.get('content', {}).get('parts', []):
        if 'inlineData' in part:
            img_bytes = base64.b64decode(part['inlineData']['data'])
            with open('$OUTFILE', 'wb') as f:
                f.write(img_bytes)
            print(f'Saved: $OUTFILE')
            sys.exit(0)
print('No image in response', file=sys.stderr)
sys.exit(1)
" 2>/dev/null; then
      echo "Generated with $MODEL (free)"
      rm -f "$TMPFILE"
      break 2  # Exit both loops (model loop + provider chain)
    fi

    echo "$MODEL failed, trying next..."
  done
fi
```

If Tier 1 fails (no key, quota exceeded, or model error), continue to Tier 2.

#### Tier 2: Pollinations.ai

Free models: `flux` (best), `gptimage`, `klein`, `klein-large`, `zimage`, `imagen`

**Note**: `gen.pollinations.ai` requires a free API key (register at https://pollinations.ai). The old `image.pollinations.ai` endpoint works anonymously but may be unreliable.

```bash
if [ ! -f "$OUTFILE" ] || [ ! -s "$OUTFILE" ]; then
  echo "Trying Pollinations.ai..."
  ENCODED_PROMPT=$(python3 -c "import urllib.parse; print(urllib.parse.quote('''${PROMPT}'''))")
  POLL_MODEL="flux"
  POLL_OK=false

  # Try authenticated endpoint first (gen.pollinations.ai)
  if [ -n "${POLLINATIONS_API_KEY:-}" ]; then
    curl -s -L --max-time 120 \
      -H "Authorization: Bearer $POLLINATIONS_API_KEY" \
      -o "$OUTFILE" \
      "https://gen.pollinations.ai/image/${ENCODED_PROMPT}?model=${POLL_MODEL}&width=1024&height=1024&nologo=true"

    if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
      FILETYPE=$(file -b "$OUTFILE" | head -1)
      if echo "$FILETYPE" | grep -qiE "image|PNG|JPEG|GIF|WebP"; then
        POLL_OK=true
      else
        rm -f "$OUTFILE"
      fi
    fi
  fi

  # Fall back to anonymous endpoint (image.pollinations.ai)
  if [ "$POLL_OK" != "true" ]; then
    curl -s -L --max-time 120 \
      -o "$OUTFILE" \
      "https://image.pollinations.ai/prompt/${ENCODED_PROMPT}?model=${POLL_MODEL}&width=1024&height=1024&nologo=true"

    if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
      FILETYPE=$(file -b "$OUTFILE" | head -1)
      if echo "$FILETYPE" | grep -qiE "image|PNG|JPEG|GIF|WebP"; then
        POLL_OK=true
      else
        echo "Pollinations returned non-image: $FILETYPE"
        rm -f "$OUTFILE"
      fi
    fi
  fi

  [ "$POLL_OK" = "true" ] && echo "Generated with Pollinations.ai (free)"
fi
```

If Tier 2 also fails (502, auth required, non-image response), continue to Tier 3.

#### Tier 3: Imagen 4 (PAID, requires billing)

Only attempt if GEMINI_API_KEY exists and user has billing enabled.

```bash
if [ ! -f "$OUTFILE" ] || [ ! -s "$OUTFILE" ]; then
  if [ -n "$GEMINI_API_KEY" ]; then
    echo "Trying Imagen 4 (paid)..."
    IMAGEN_MODEL="imagen-4.0-generate-001"

    curl -s -X POST \
      "https://generativelanguage.googleapis.com/v1beta/models/${IMAGEN_MODEL}:predict" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H "Content-Type: application/json" \
      -o "$TMPFILE" \
      -d "{
        \"instances\": [{\"prompt\": \"${PROMPT}\"}],
        \"parameters\": {\"sampleCount\": 1}
      }"

    python3 -c "
import json, sys, base64
with open('$TMPFILE') as f:
    data = json.load(f)
if 'predictions' in data:
    img = base64.b64decode(data['predictions'][0]['bytesBase64Encoded'])
    with open('$OUTFILE', 'wb') as f:
        f.write(img)
    print(f'Saved: $OUTFILE')
elif 'error' in data:
    print(f'Imagen error: {data[\"error\"][\"message\"][:200]}', file=sys.stderr)
    sys.exit(1)
" 2>/dev/null && echo "Generated with Imagen 4 (paid)"

    rm -f "$TMPFILE"
  fi
fi
```

### Step 5: Verify Output

```bash
if [ -f "$OUTFILE" ] && [ -s "$OUTFILE" ]; then
  file "$OUTFILE"
  SIZE=$(du -h "$OUTFILE" | cut -f1)
  echo "Image generated successfully: $OUTFILE ($SIZE)"
else
  echo "ERROR: All providers failed. Possible causes:"
  echo "  - Gemini: Daily quota exceeded (resets at midnight PT)"
  echo "  - Pollinations: Service temporarily down"
  echo "  - Imagen 4: Billing not enabled"
  echo ""
  echo "Solutions:"
  echo "  1. Wait for Gemini quota reset (check https://ai.dev/rate-limit)"
  echo "  2. Try again in a few minutes (Pollinations may recover)"
  echo "  3. Enable billing at https://aistudio.google.com/ for Imagen 4"
fi
```

### Step 6: Report Result

Tell the user:
- File path to the generated image
- Which provider/model was used
- Cost: "free" (Gemini native / Pollinations) or cost estimate (Imagen 4: ~$0.04/image)

## Error Handling

| Error | Action |
|-------|--------|
| Gemini quota exceeded | Auto-fallback to Pollinations, then Imagen 4 |
| Pollinations 502/timeout | Auto-fallback to Imagen 4 |
| Imagen billing not enabled | Report all providers failed, suggest enabling billing |
| `GEMINI_API_KEY` not set | Skip Gemini tiers, use Pollinations only |
| Content policy block | Report prompt was blocked, suggest rewording |
| All providers fail | Show diagnostic with links to check quota/status |

## Setup Instructions (Show When No API Key Found)

If `GEMINI_API_KEY` is not set, inform the user:

> **Using Pollinations.ai only** (free, but may be unreliable).
>
> For better reliability, set up a free Google Gemini API key:
> 1. Go to https://aistudio.google.com/
> 2. Click "Get API key" → Create API key
> 3. Add to your `.env` file: `GEMINI_API_KEY=your-key-here`
>
> The free tier includes image generation with `gemini-2.5-flash-image`.
> The same key also works for video generation (Veo models require billing).

## Activation Keywords

generate image, create image, make image, AI image, text-to-image, image generation, create picture, make illustration, generate photo, AI art, create visual, generate artwork, make a picture of
