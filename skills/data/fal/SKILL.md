---
name: fal
description: Search, explore, and run fal.ai generative AI models (image generation, video, audio, 3D). Use when user wants to generate images, videos, or other media with AI models.
allowed-tools: Bash(curl *), Bash(jq *), Bash(mkdir *), Read, Write
argument-hint: "<command> [model_id] [--param value]"
---

# fal.ai Model API Skill

Run 600+ generative AI models on fal.ai.

## Arguments

- **Command:** `$0` (search | schema | run | status | result | upload)
- **Arg 1:** `$1` (model_id, search query, or file path)
- **Arg 2+:** `$2`, `$3`, etc. (additional parameters)
- **All args:** `$ARGUMENTS`

## Session Output

Save generated files to session folder:
```bash
mkdir -p ~/.fal/sessions/${CLAUDE_SESSION_ID}
```

Downloaded images/videos go to: `~/.fal/sessions/${CLAUDE_SESSION_ID}/`

---

## Authentication

Requires `FAL_KEY` environment variable. If requests fail with 401, tell user:
```
Get an API key from https://fal.ai/dashboard/keys
Then: export FAL_KEY="your-key-here"
```

---

## Command: `$0`

### If $0 = "search"

Search for models matching `$1`:

```bash
curl -s "https://api.fal.ai/v1/models?q=$1&limit=15" \
  -H "Authorization: Key $FAL_KEY" | jq -r '.models[] | "• \(.endpoint_id) — \(.metadata.display_name) [\(.metadata.category)]"'
```

For category search, use:
```bash
curl -s "https://api.fal.ai/v1/models?category=$1&limit=15" \
  -H "Authorization: Key $FAL_KEY" | jq -r '.models[] | "• \(.endpoint_id) — \(.metadata.display_name)"'
```

Categories: `text-to-image`, `image-to-video`, `text-to-video`, `image-to-3d`, `training`, `speech-to-text`, `text-to-speech`

---

### If $0 = "schema"

Get input schema for model `$1`:

```bash
curl -s "https://api.fal.ai/v1/models?endpoint_id=$1&expand=openapi-3.0" \
  -H "Authorization: Key $FAL_KEY" | jq '.models[0].openapi.components.schemas.Input.properties'
```

Show required vs optional fields to help user understand what inputs are needed.

---

### If $0 = "run"

Run model `$1` with parameters from remaining arguments.

**Step 1: Parse parameters**
Extract `--key value` pairs from `$ARGUMENTS` after the model_id to build JSON payload.

Example: `/fal run fal-ai/flux-2 --prompt "a cat" --image_size landscape_16_9`
→ Model: `fal-ai/flux-2`
→ Payload: `{"prompt": "a cat", "image_size": "landscape_16_9"}`

**Step 2: Submit to queue**
```bash
curl -s -X POST "https://queue.fal.run/$1" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '<JSON_PAYLOAD>'
```

**Step 3: Poll until complete**
```bash
# Get request_id from response, then poll:
while true; do
  STATUS=$(curl -s "https://queue.fal.run/$1/requests/$REQUEST_ID/status" \
    -H "Authorization: Key $FAL_KEY" | jq -r '.status')
  echo "Status: $STATUS"
  if [ "$STATUS" = "COMPLETED" ]; then break; fi
  if [ "$STATUS" = "FAILED" ]; then echo "Job failed"; break; fi
  sleep 3
done
```

**Step 4: Get result and save**
```bash
# Fetch result
RESULT=$(curl -s "https://queue.fal.run/$1/requests/$REQUEST_ID" \
  -H "Authorization: Key $FAL_KEY")

# Create session output folder
mkdir -p ~/.fal/sessions/${CLAUDE_SESSION_ID}

# Download images/videos
# For images: jq -r '.images[0].url' and curl to download
# Save as: ~/.fal/sessions/${CLAUDE_SESSION_ID}/<timestamp>_<model>.png
```

---

### If $0 = "status"

Check status of request `$2` for model `$1`:

```bash
curl -s "https://queue.fal.run/$1/requests/$2/status?logs=1" \
  -H "Authorization: Key $FAL_KEY" | jq '{status: .status, queue_position: .queue_position, logs: .logs}'
```

---

### If $0 = "result"

Get result of completed request `$2` for model `$1`:

```bash
curl -s "https://queue.fal.run/$1/requests/$2" \
  -H "Authorization: Key $FAL_KEY" | jq '.'
```

---

### If $0 = "upload"

Upload file `$1` to fal CDN:

```bash
curl -s -X POST "https://fal.run/fal-ai/storage/upload" \
  -H "Authorization: Key $FAL_KEY" \
  -F "file=@$1"
```

Returns URL to use in model requests.

---

## Quick Reference

**Popular models:**
- `fal-ai/flux-2` — Fast text-to-image
- `fal-ai/flux-2-pro` — High quality text-to-image
- `fal-ai/kling-video/v2/image-to-video` — Image to video
- `fal-ai/minimax/video-01/image-to-video` — Image to video
- `fal-ai/whisper` — Speech to text

**Common parameters for text-to-image:**
- `--prompt "description"` — What to generate
- `--image_size landscape_16_9` — Aspect ratio (square, portrait_4_3, landscape_16_9)
- `--num_images 1` — Number of images

**Example invocations:**
- `/fal search video` — Find video models
- `/fal schema fal-ai/flux-2` — See input options
- `/fal run fal-ai/flux-2 --prompt "a sunset over mountains"`
- `/fal status fal-ai/flux-2 abc-123`
- `/fal upload ./photo.png`
