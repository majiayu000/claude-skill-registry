---
name: genai-video
description: Generate videos using Google GenAI Veo 3.1 model via CLI. Use when the user asks to create videos, generate animations, make AI video content, do image-to-video transformations, interpolate between frames, or create cinematic shots with camera movement.
---

# GenAI Video Generation Skill

Generate videos using the `genai-cli video` command with Veo 3.1.

**Uses fast mode by default** ($0.15/sec) for quick generation. Use `--quality-mode` for higher quality output ($0.40/sec).

## Quick Start

```bash
# Basic video generation (async - returns job ID)
uv run genai-cli video "sunset over ocean, gentle waves"

# Wait for completion (blocking)
uv run genai-cli video "sunset over ocean" --wait

# Image-to-video (use existing image as starting frame)
uv run genai-cli video "camera pullback revealing the scene" --input ./image.png --wait

# First/last frame interpolation
uv run genai-cli video "smooth morph transition" --input ./start.png --last-frame ./end.png --wait
```

## CLI Reference

```
uv run genai-cli video [OPTIONS] PROMPT

Options:
  --aspect, -a      Aspect ratio: 16:9 or 9:16 (default: 16:9)
  --duration, -d    Duration in seconds: 4, 6, or 8 (default: 8)
  --resolution, -r  Resolution: 720p, 1080p, or 4k (default: 720p)
  --seed, -s        Random seed for reproducibility
  --audio           Generate video with audio
  --wait, -w        Wait for completion (blocking mode)
  --input, -i       First frame image for image-to-video
  --last-frame, -l  Last frame image (requires --input)
  --negative, -n    What NOT to include in video
  --ref             Reference images for style (up to 3, 16:9 only)
  --ref-type        Reference image type: style (aesthetic) or asset (character/object)
  --extend, -e      Video file URI to extend
  --person-gen      Person generation: allow_all or allow_adult
  --quality-mode    Use quality model (slower, higher quality, $0.40/sec)
  --enhance         Auto-improve prompt for better video quality
  --fps             Frames per second (e.g., 24 for cinematic, 60 for smooth)
  --compression     Compression quality: optimized (smaller) or lossless (larger)
  --variations, -v  Number of video variations to generate (1-4)
  --mask, -m        Mask image for targeted editing (requires --input)
  --mask-mode       Mask mode: insert, remove, remove-static, outpaint
  --output, -o      Output directory (default: ./genai_outputs/)
  --json            Output as JSON
```

## Model Modes

### Fast Mode (Default)
Uses `veo-3.1-fast-generate-preview` model at $0.15/second. Optimized for speed and business use cases.

```bash
uv run genai-cli video "sunset over ocean" --wait
```

### Quality Mode
Uses `veo-3.1-generate-preview` model at $0.40/second. Higher quality output for premium content.

```bash
uv run genai-cli video "cinematic sunset scene" --quality-mode --wait
```

## Prompt Enhancement

Auto-improve your prompts for better video quality:

```bash
# Let the model enhance your simple prompt
uv run genai-cli video "sunset" --enhance --wait
```

## Frame Rate Control (FPS)

Control frames per second for different effects:

```bash
# Cinematic 24fps (film-like)
uv run genai-cli video "dramatic scene" --fps 24 --wait

# Standard 30fps
uv run genai-cli video "product demo" --fps 30 --wait

# Smooth 60fps (action/sports)
uv run genai-cli video "slow motion water" --fps 60 --wait
```

## Compression Quality

Control file size vs quality tradeoff:

```bash
# Optimized - smaller file size (default behavior)
uv run genai-cli video "social media clip" --compression optimized --wait

# Lossless - larger file, no quality loss (for archival/editing)
uv run genai-cli video "product demo" --compression lossless --wait
```

## Multiple Variations

Generate multiple video variations from the same prompt:

```bash
# Generate 3 different versions
uv run genai-cli video "abstract animation" --variations 3 --wait

# Generate 4 variations for A/B testing
uv run genai-cli video "hero scene" --variations 4 --wait
```

## Modes

### Async Mode (Default)
Returns immediately with a job ID:
```bash
uv run genai-cli video "flying through clouds"
# Output: Job ID: models/veo-3.1.../operations/abc123
```

### Blocking Mode (--wait)
Waits for video to complete and downloads it:
```bash
uv run genai-cli video "flying through clouds" --wait
# Output: ✓ Saved: genai_outputs/video_20260114_123456_1.mp4 (2.1 MB)
```

## Image-to-Video

Use an existing image as the starting frame for your video:

```bash
# Camera pullback from an image
uv run genai-cli video "Dramatic camera pullback revealing the full scene" \
  --input ./my_image.png \
  --aspect 9:16 \
  --wait

# Animate a still image
uv run genai-cli video "Gentle movement, hair blowing in wind" \
  --input ./portrait.png \
  --wait
```

## First & Last Frame Interpolation

Generate videos by specifying both the starting and ending frames. The model interpolates smooth motion between them:

```bash
# Morph between two images
uv run genai-cli video "Smooth transition with dramatic lighting" \
  --input ./start_frame.png \
  --last-frame ./end_frame.png \
  --wait

# Scene transformation
uv run genai-cli video "Day transforms to night, cinematic transition" \
  --input ./day_scene.png \
  --last-frame ./night_scene.png \
  --aspect 16:9 \
  --wait
```

**Requirements:**
- Both images must match the video's aspect ratio
- `--last-frame` requires `--input` (first frame) to be set
- Duration defaults to 8 seconds for interpolation

## Reference Images for Style/Assets

Use up to 3 reference images to guide the video. Two reference types are available:

### Style References (Default)
Transfer aesthetic elements like colors, lighting, and visual style:

```bash
# Style-guided generation (default)
uv run genai-cli video "A person walking through a forest" \
  --ref ./style1.png --ref ./style2.png \
  --ref-type style \
  --aspect 16:9 \
  --wait
```

### Asset References
Maintain character or object consistency across scenes:

```bash
# Character consistency
uv run genai-cli video "The character walks through a city" \
  --ref ./character_front.png --ref ./character_side.png \
  --ref-type asset \
  --aspect 16:9 \
  --wait

# Object consistency
uv run genai-cli video "The product rotates on display" \
  --ref ./product_view1.png --ref ./product_view2.png \
  --ref-type asset \
  --aspect 16:9 \
  --wait
```

**Note:** Reference images only work with 16:9 aspect ratio and require duration of 8 seconds.

## Video Extension

Extend a previously generated Veo video:

```bash
# Extend an existing video
uv run genai-cli video "Continue the scene with more action" \
  --extend "files/video-file-id" \
  --wait
```

**Note:** Extension requires duration of 8 seconds.

## Negative Prompts

Specify what NOT to include in your video:

```bash
uv run genai-cli video "A serene beach scene" \
  --negative "people, crowds, text, watermarks" \
  --wait
```

## Person Generation Control

Control how people are generated in videos:

```bash
# Allow all person generation (text/extension mode)
uv run genai-cli video "People walking in park" \
  --person-gen allow_all \
  --wait

# Allow adult-only generation (image/interpolation/references)
uv run genai-cli video "Professional meeting" \
  --input ./office.png \
  --person-gen allow_adult \
  --wait
```

## Audio Generation

Generate videos with synchronized audio:

```bash
uv run genai-cli video "Ocean waves crashing on beach with seagulls" \
  --audio \
  --wait
```

## Resolution & Duration

### High Resolution (1080p/4K)
```bash
# 1080p requires 8s duration
uv run genai-cli video "Cinematic landscape" \
  --resolution 1080p \
  --duration 8 \
  --wait

# 4K also requires 8s duration
uv run genai-cli video "Ultra HD nature scene" \
  --resolution 4k \
  --duration 8 \
  --wait
```

### Duration Options
```bash
# 4 seconds
uv run genai-cli video "Quick action shot" --duration 4 --wait

# 6 seconds
uv run genai-cli video "Medium scene" --duration 6 --wait

# 8 seconds (default, required for 1080p/4K/extension/references)
uv run genai-cli video "Full scene" --duration 8 --wait
```

## Camera Movement Prompts

For image-to-video, describe the camera movement:

| Movement | Prompt Example |
|----------|----------------|
| Pullback | "Camera slowly pulls back to reveal the scene" |
| Push in | "Camera pushes in toward the subject" |
| Pan | "Camera pans left across the scene" |
| Tilt | "Camera tilts up to show the sky" |
| Dolly | "Smooth dolly shot moving parallel to subject" |
| Crane | "Crane shot rising above the scene" |
| Static | "Subtle movement, subject remains still" |

## Video Masking (Targeted Editing)

Use masks to edit specific regions of videos:

### Insert Mode
Add new objects into a masked region:

```bash
uv run genai-cli video "add a butterfly flying" \
  --input ./scene.png \
  --mask ./butterfly_area_mask.png \
  --mask-mode insert \
  --wait
```

### Remove Mode
Remove tracked objects from video (tracks object through frames):

```bash
uv run genai-cli video "remove the car smoothly" \
  --input ./street_scene.png \
  --mask ./car_mask.png \
  --mask-mode remove \
  --wait
```

### Remove-Static Mode
Remove static objects (watermarks, logos, fixed elements):

```bash
uv run genai-cli video "clean background" \
  --input ./video_frame.png \
  --mask ./watermark_mask.png \
  --mask-mode remove-static \
  --wait
```

### Outpaint Mode
Expand the video beyond its original frame:

```bash
uv run genai-cli video "expand the landscape view" \
  --input ./cropped_scene.png \
  --mask ./outpaint_mask.png \
  --mask-mode outpaint \
  --wait
```

**Mask Requirements:**
- Mask must be same dimensions as input image
- White areas (255) = region to modify
- Black areas (0) = region to preserve
- `--mask` requires `--input` (first frame image)

## Output

Videos are saved to `./genai_outputs/` by default:
- `video_YYYYMMDD_HHMMSS_1.mp4`

## Prompt Tips

1. **Describe movement**: "Camera slowly pulls back", "Gentle zoom in"
2. **Include atmosphere**: "Moody lighting", "Dust particles in air"
3. **Use audio cues**: With `--audio`, describe sounds in prompt
4. **Be cinematic**: "Dramatic", "Cinematic", "Film-like"
5. **Use negative prompts**: Exclude unwanted elements with `--negative`

## API Constraints

| Feature | Constraint |
|---------|------------|
| 1080p/4K resolution | Requires duration = 8 |
| Reference images | Requires 16:9 aspect, duration = 8 |
| Video extension | Requires duration = 8 |
| Reference images | Max 3 images |

## Prerequisites

API key must be configured:
```bash
uv run genai-cli auth set-key
```
