---
name: media-generation
description: 'Generate images, videos, and audio using Google''s Gemini APIs. Use
  for image generation/editing (Gemini 3 Pro Image), video generation (Veo 3), and
  speech (TBD). Trigger words - images: generate, crea'
---

---
name: media-generation
description: Generate images, videos, and audio using Google's Gemini APIs. Use for image generation/editing (Gemini 3 Pro Image), video generation (Veo 3), and speech (TBD). Trigger words - images: generate, create, draw, design, make, edit, modify image/picture. Video: generate video, create video, animate, make a video. Supports text-to-image, image-to-image editing, text-to-video, and image-to-video.
---

# Media Generation

## Image Generation

```bash
uv run ~/.claude/skills/media-generation/scripts/generate_image.py \
  --prompt "description or editing instructions" \
  --filename "output.png" \
  [--input-image "source.png"] \
  [--resolution 1K|2K|4K]
```

### Resolution
- `1K` (default) — also for: "low res", "1080p"
- `2K` — also for: "medium", "2048"
- `4K` — also for: "high res", "hi-res", "ultra"

## Video Generation

```bash
uv run ~/.claude/skills/media-generation/scripts/generate_video.py \
  --prompt "video description" \
  --filename "output.mp4" \
  [--model veo-3.0-generate-preview] \
  [--negative "things to avoid"] \
  [--input-image "first-frame.png"]
```

### Models
- `veo-3.0-generate-001` (default) — stable, video only
- `veo-3.0-fast-generate-001` — faster, lower cost
- `veo-3.1-generate-preview` — supports video extend, audio sync
- `veo-3.1-fast-generate-preview` — fast with extend support

### Prompting Tips
- Specify camera movements: `"slow zoom in", "pan left", "close-up"`
- Add `"no talking, no dialogue"` if character shouldn't speak
- Describe atmosphere: `"rain outside", "purple mystical energy"`

**Note:** Veo requires paid tier. ~$0.40/sec standard, ~$0.15/sec fast.

## Music Video from Image + Audio

### Overview
1. Start with character image + audio track (e.g., from Suno)
2. Transcribe audio to get timestamps
3. Generate clip 1 from image (veo-3.1)
4. Extend each subsequent clip from previous (maintains continuity)
5. Stitch clips + overlay audio with ffmpeg

### Step 1: Transcribe audio for timing
```bash
whisper-ctranslate2 "song.mp3" --model large-v3 --output_dir /tmp --output_format srt
```

### Step 2: Generate first clip from image
```python
# Use veo-3.1 (required for extend feature)
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    image=types.Image(image_bytes=img_data, mime_type="image/jpeg"),
    prompt="character description, scene action, no talking",
)
video1 = operation.result.generated_videos[0]
```

### Step 3: Extend from previous clip
```python
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    video=previous_video.video,  # Pass previous video object
    prompt="next scene description, continuous action, no talking",
)
```

### Step 4: Stitch clips + add audio
```bash
# Create concat list
printf "file 'clip_01.mp4'\nfile 'clip_02.mp4'\n..." > concat.txt

# Stitch video clips
ffmpeg -f concat -safe 0 -i concat.txt -c copy combined.mp4

# Add audio track
ffmpeg -i combined.mp4 -i song.mp3 -c:v copy -c:a aac -map 0:v -map 1:a final.mp4
```

### Cost estimate
- ~8 sec per clip × $0.40/sec = $3.20/clip
- 4-min song ≈ 30 clips ≈ $96

## Audio Generation

- **Music:** Use Suno (external service)
- **Speech:** Gemini 2.5 TTS (Flash or Pro) - TBD script

## API Key

Uses `GEMINI_API_KEY` env var, or pass `--api-key KEY`.
