---
name: fal
description: >
  Generate images, videos, audio, and more using fal.ai AI models.
  Use when user requests: "generate image", "create video", "make a picture",
  "text to image", "image to video", "text to speech", "transcribe audio",
  "edit image", "remove background", "upscale image", "enhance resolution",
  "search models", "fal pricing", "fal usage", "create workflow",
  "chain models", "setup fal", "add API key", or similar media generation tasks.
allowed-tools: Bash(bash:*), Bash(curl:*), Bash(source:*), Bash(echo:*), mcp__fal__SearchFal, WebFetch, WebSearch
metadata:
  author: analyticalmonk
  version: "1.1.0"
---

# fal.ai - Unified Media Generation Skill

Generate images, videos, audio, and more using state-of-the-art AI models on fal.ai.

**References:**
- [Model Reference](references/MODELS.md) - recommended models by category
- [Cinematography Reference](references/CINEMATOGRAPHY.md) - camera movements, shot types, composition, lighting
- [Workflow Reference](references/WORKFLOWS.md) - workflow JSON spec and patterns
- [Platform Reference](references/PLATFORM.md) - pricing, usage, billing APIs

**Script directory:** `scripts/` (all paths below are relative to the skill root)

---

## Authentication

All scripts require `FAL_KEY`. Set it up:

```bash
# Interactive setup
bash scripts/setup.sh --add-fal-key

# Set key directly
bash scripts/setup.sh --add-fal-key "your_key_here"

# Or export directly
export FAL_KEY=your_key_here
```

Scripts auto-load from `.env` if present. Get your key at https://fal.ai/dashboard/keys

---

## Routing Table

| User Intent | Script | Key Args |
|-------------|--------|----------|
| Generate image | `scripts/generate.sh` | `--prompt`, `--model` |
| Generate video | `scripts/generate.sh` | `--prompt`, `--model` (video model) |
| Image-to-video | `scripts/generate.sh` | `--prompt`, `--model`, `--image-url` |
| Upload local file | `scripts/upload.sh` | `--file` |
| Text-to-speech | `scripts/text-to-speech.sh` | `--text`, `--model` |
| Speech-to-text | `scripts/speech-to-text.sh` | `--audio-url` |
| Edit image (style/remove/bg) | `scripts/edit-image.sh` | `--image-url`, `--prompt`, `--operation` |
| Upscale image/video | `scripts/upscale.sh` | `--image-url`, `--model` |
| Search models | `scripts/search-models.sh` | `--query`, `--category` |
| Get model schema | `scripts/get-schema.sh` | `--model` |
| Create workflow | `scripts/create-workflow.sh` | `--name`, `--nodes`, `--outputs` |
| Check pricing | `scripts/pricing.sh` | `--model` |
| Check usage | `scripts/usage.sh` | `--model`, `--timeframe` |
| Estimate cost | `scripts/estimate-cost.sh` | `--model`, `--calls` |
| Manage requests | `scripts/requests.sh` | `--model`, `--delete` |
| Setup API key | `scripts/setup.sh` | `--add-fal-key` |

---

## Generate (Image & Video)

Primary script: `scripts/generate.sh`

### Queue System (Default)

All requests use the queue system for reliability:
```
User Request → Queue Submit → Poll Status → Get Result
```

Benefits: no timeouts for long tasks (video), can check status/cancel anytime, results persist.

### Basic Usage

```bash
# Text-to-image (waits for completion)
bash scripts/generate.sh --prompt "A serene mountain landscape" --model "fal-ai/nano-banana-pro"

# Text-to-video
bash scripts/generate.sh --prompt "Ocean waves crashing" --model "fal-ai/veo3.1"

# Image-to-video (requires --image-url)
bash scripts/generate.sh \
  --prompt "Camera slowly zooms in" \
  --model "fal-ai/kling-video/v2.6/pro/image-to-video" \
  --image-url "https://example.com/image.jpg"
```

### Async Mode (Long Jobs)

For video generation, use `--async` to get request_id immediately:

```bash
# Submit and return immediately
bash scripts/generate.sh --prompt "Epic scene" --model "fal-ai/veo3.1" --async
# → Request ID: abc123-def456

# Check status later
bash scripts/generate.sh --status "abc123-def456" --model "fal-ai/veo3.1"

# Get result when complete
bash scripts/generate.sh --result "abc123-def456" --model "fal-ai/veo3.1"

# Cancel if needed
bash scripts/generate.sh --cancel "abc123-def456" --model "fal-ai/veo3.1"
```

### File Upload

```bash
# Option 1: Auto-upload with --file
bash scripts/generate.sh \
  --file "/path/to/photo.jpg" \
  --model "fal-ai/kling-video/v2.6/pro/image-to-video" \
  --prompt "Camera zooms in slowly"

# Option 2: Manual upload first
URL=$(bash scripts/upload.sh --file "/path/to/photo.jpg")
bash scripts/generate.sh --image-url "$URL" --model "..." --prompt "..."

# Option 3: Use any public URL directly
bash scripts/generate.sh --image-url "https://example.com/image.jpg" ...
```

Supported types: jpg, jpeg, png, gif, webp (images), mp4, mov, webm (video), mp3, wav, flac (audio). Max 100MB.

### Generate Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--prompt`, `-p` | Text description | (required) |
| `--model`, `-m` | Model ID | `fal-ai/flux/dev` |
| `--image-url` | Input image URL for I2V | - |
| `--file`, `--image` | Local file (auto-uploads) | - |
| `--size` | `square`, `portrait`, `landscape` | `landscape_4_3` |
| `--num-images` | Number of images | 1 |
| `--async` | Return request_id immediately | - |
| `--sync` | Synchronous (not recommended for video) | - |
| `--logs` | Show generation logs while polling | - |
| `--status ID` | Check queued request status | - |
| `--result ID` | Get completed request result | - |
| `--cancel ID` | Cancel queued request | - |
| `--poll-interval` | Seconds between status checks | 2 |
| `--timeout` | Max seconds to wait | 600 |
| `--lifecycle N` | Object expiration in seconds | - |
| `--schema [MODEL]` | Get OpenAPI schema | - |

### Recommended Models

**Text-to-Image:** `fal-ai/nano-banana-pro` (best overall), `fal-ai/flux/dev` (default), `fal-ai/flux/schnell` (fastest), `fal-ai/ideogram/v3` (best text rendering)

**Text-to-Video:** `fal-ai/veo3.1` (high quality), `fal-ai/bytedance/seedance/v1/pro` (fast)

**Image-to-Video:** `fal-ai/kling-video/v2.6/pro/image-to-video` (best), `fal-ai/bytedance/seedance/v1.5/pro/image-to-video` (smooth motion)

See [references/MODELS.md](references/MODELS.md) for full list.

### Prompt Crafting

When writing prompts for image or video generation, apply cinematography and storytelling techniques from the [Cinematography Reference](references/CINEMATOGRAPHY.md). Key rules:

- **Structure prompts as:** `[shot type + angle], [subject], [action], [camera movement], [lighting], [style]`
- **One camera movement per short clip** (under 6s) - don't combine pan + dolly + zoom
- **Match camera style to content:** handheld for UGC, steadicam for cinematic, drone for landscapes, orbit for products
- **Specify lighting to set mood:** golden hour for warmth, low-key for drama, natural for authenticity
- **Lead with the subject**, then describe action, then environment
- **For images:** focus on composition (rule of thirds, depth of field, leading lines) and lighting over motion

---

## Audio

### Text-to-Speech

```bash
# Default (fast, good quality)
bash scripts/text-to-speech.sh --text "Hello, welcome to the future."

# High quality
bash scripts/text-to-speech.sh --text "Premium speech." --model "fal-ai/minimax/speech-2.6-hd"

# With specific voice
bash scripts/text-to-speech.sh --text "Hello" --model "fal-ai/elevenlabs/eleven-v3" --voice "Aria"
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--text` | Text to convert (required) | - |
| `--model` | TTS model | `fal-ai/minimax/speech-2.6-turbo` |
| `--voice` | Voice ID (model-specific) | - |

**Models:** `fal-ai/minimax/speech-2.6-hd` (best), `fal-ai/minimax/speech-2.6-turbo` (fast), `fal-ai/elevenlabs/eleven-v3` (natural), `fal-ai/chatterbox/multilingual` (multi-language)

### Speech-to-Text

```bash
# Transcribe with Whisper
bash scripts/speech-to-text.sh --audio-url "https://example.com/audio.mp3"

# With speaker diarization
bash scripts/speech-to-text.sh --audio-url "https://..." --model "fal-ai/elevenlabs/scribe"

# Specific language
bash scripts/speech-to-text.sh --audio-url "https://..." --language "es"
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--audio-url` | Audio URL to transcribe (required) | - |
| `--model` | STT model | `fal-ai/whisper` |
| `--language` | Language code (auto-detected) | - |

---

## Image Editing

```bash
bash scripts/edit-image.sh --image-url URL --prompt "..." --operation OP
```

| Operation | Description | Model Used |
|-----------|-------------|------------|
| `style` | Style transfer (default) | `fal-ai/flux/dev/image-to-image` |
| `remove` | Object removal | `bria/fibo-edit` |
| `background` | Background change | `fal-ai/flux-kontext` |
| `inpaint` | Masked inpainting (needs `--mask-url`) | `fal-ai/flux/dev/inpainting` |

| Argument | Description | Default |
|----------|-------------|---------|
| `--image-url` | Image to edit (required) | - |
| `--prompt` | Edit description (required) | - |
| `--operation` | `style`, `remove`, `background`, `inpaint` | `style` |
| `--mask-url` | Mask image (for inpaint) | - |
| `--strength` | Edit strength 0.0-1.0 | 0.75 |

```bash
# Style transfer
bash scripts/edit-image.sh --image-url "https://..." --prompt "Convert to anime style"

# Remove object
bash scripts/edit-image.sh --image-url "https://..." --prompt "Remove the car" --operation remove

# Change background
bash scripts/edit-image.sh --image-url "https://..." --prompt "Tropical beach" --operation background
```

---

## Upscale

```bash
# Image upscale (4x, fast)
bash scripts/upscale.sh --image-url "https://example.com/image.jpg"

# With specific model and scale
bash scripts/upscale.sh --image-url "https://..." --model "fal-ai/clarity-upscaler" --scale 2
```

| Argument | Description | Default |
|----------|-------------|---------|
| `--image-url` | Image to upscale (required) | - |
| `--model` | Upscale model | `fal-ai/aura-sr` |
| `--scale` | Scale factor (2 or 4) | 4 |

**Image models:** `fal-ai/aura-sr` (fast 4x), `fal-ai/clarity-upscaler` (detail), `fal-ai/creative-upscaler` (artistic)

**Video models:** `fal-ai/topaz/upscale/video` (premium), `fal-ai/video-upscaler` (general)

---

## Workflows

Chain multiple AI models into pipelines. See [references/WORKFLOWS.md](references/WORKFLOWS.md) for full spec.

```bash
bash scripts/create-workflow.sh \
  --name "my-workflow" \
  --title "My Workflow" \
  --nodes '[{"nodeId":"node-image","modelId":"fal-ai/flux/dev","input":{"prompt":"$input.prompt"}}]' \
  --outputs '{"image":"$node-image.images.0.url"}'
```

Key rules: only `"run"` and `"display"` node types, no string interpolation (variable must be entire value), dependencies must match references.

---

## Model Discovery

### Search Models

```bash
bash scripts/search-models.sh --query "flux"
bash scripts/search-models.sh --category "text-to-video"
bash scripts/search-models.sh --query "upscale" --limit 5
```

Categories: `text-to-image`, `image-to-image`, `text-to-video`, `image-to-video`, `text-to-speech`, `speech-to-text`

### Get Model Schema (OpenAPI)

Fetch exact parameters for any model before using it:

```bash
bash scripts/get-schema.sh --model "fal-ai/nano-banana-pro"
bash scripts/get-schema.sh --model "fal-ai/kling-video/v2.6/pro/image-to-video" --input
```

---

## Platform

See [references/PLATFORM.md](references/PLATFORM.md) for full API reference.

```bash
# Pricing
bash scripts/pricing.sh --model "fal-ai/flux/dev"

# Usage
bash scripts/usage.sh --timeframe "day"

# Cost estimation
bash scripts/estimate-cost.sh --model "fal-ai/flux/dev" --calls 100

# Request management
bash scripts/requests.sh --model "fal-ai/flux/dev" --limit 10
```

---

## MCP Integration

The fal MCP server provides a `SearchFal` tool for documentation and model discovery.

**When to use SearchFal (MCP):**
- Discovering what models exist and their capabilities
- Reading documentation and guides
- Understanding model parameters and features

**When to use scripts:**
- Actually generating media (images, video, audio)
- Uploading files to fal CDN
- Checking pricing, usage, and billing
- Getting exact OpenAPI schemas (`get-schema.sh`)

They complement each other: SearchFal for discovery/docs, scripts for execution.

---

## Output Presentation

### Images
```
![Generated Image](https://v3.fal.media/files/...)
- 1024x768 | Generated in 2.2s
```

### Videos
```
[Click to view video](https://v3.fal.media/files/.../video.mp4)
- Duration: 5s | Generated in 45s
```

### Audio (TTS)
```
[Download audio](https://v3.fal.media/files/.../speech.mp3)
- Duration: 5.2s | Model: MiniMax Speech 2.6 Turbo
```

### Async Submission
```
Request submitted to queue.
- Request ID: abc123-def456
- Model: fal-ai/veo3
- Check status: bash scripts/generate.sh --status "abc123-def456" --model "fal-ai/veo3"
```

---

## Troubleshooting

### FAL_KEY not set
Run `bash scripts/setup.sh --add-fal-key` or `export FAL_KEY=your_key`.

### Timeout
Use `--status` and `--result` to check manually, or increase `--timeout`.

### Unknown model parameters
Fetch the schema first: `bash scripts/get-schema.sh --model "model-id" --input`
