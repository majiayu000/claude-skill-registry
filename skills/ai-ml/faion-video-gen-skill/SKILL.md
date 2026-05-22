---
name: faion-video-gen-skill
user-invocable: false
description: ""
---

# AI Video Generation Mastery

**Text-to-Video, Image-to-Video, and Video Editing with AI (2025-2026)**

---

## Quick Reference

| Platform | Best For | Max Duration | API | Cost Range |
|----------|----------|--------------|-----|------------|
| **Sora 2** | Photorealism, complex motion | 20s (Plus), 60s (Pro) | OpenAI | $20-200/mo subscription |
| **Runway Gen-4** | Professional, consistent | 10s | Yes | $0.05-0.10/second |
| **Pika Labs 2.5** | Speed, effects | 5s (extendable) | Yes | $0.20-0.50/video |
| **Kling 2.0** | Alternative, good value | 10s | Limited | Freemium |
| **Luma Dream Machine** | Fast iteration | 5s | Yes | Credits-based |

---

## Platform Comparison

### Feature Matrix

| Feature | Sora 2 | Runway Gen-4 | Pika 2.5 | Kling 2.0 |
|---------|--------|--------------|----------|-----------|
| Text-to-Video | Yes | Yes | Yes | Yes |
| Image-to-Video | Yes | Yes | Yes | Yes |
| Video-to-Video | Yes | Yes | Partial | No |
| Camera Controls | Advanced | Advanced | Basic | Basic |
| Motion Brush | Yes | Yes | No | No |
| Lip Sync | Yes | No | Yes | Yes |
| Audio Generation | Yes | No | Yes (SFX) | No |
| Storyboard Mode | Yes | Multi-shot | No | No |
| Resolution | 1080p | 4K | 1080p | 1080p |
| API Access | OpenAI | Yes | Yes | Limited |

### When to Use Each

| Use Case | Recommended Platform |
|----------|---------------------|
| Cinematic quality, complex scenes | Sora 2 |
| Professional production, API integration | Runway Gen-4 |
| Quick iterations, social content | Pika Labs 2.5 |
| Budget-conscious, testing | Kling 2.0 |
| Rapid prototyping | Luma Dream Machine |

---

## Sora 2 (OpenAI)

### Overview

OpenAI's flagship video generation model. Best for photorealistic output and complex scene understanding.

**Access:** ChatGPT Plus ($20/mo) or Pro ($200/mo)

### Capabilities

| Feature | Description |
|---------|-------------|
| **Text-to-Video** | Generate from detailed prompts |
| **Image-to-Video** | Animate static images |
| **Video-to-Video** | Remix, edit, extend existing videos |
| **Blend Mode** | Combine two video sources |
| **Re-cut** | Edit and re-render existing videos |
| **Storyboard** | Multi-shot timeline planning |

### Prompt Engineering

**Effective Prompt Structure:**

```
[Scene Description] + [Camera Movement] + [Lighting] + [Style] + [Duration Hint]
```

**Example Prompts:**

```
# Cinematic Scene
A woman with dark skin and wavy hair walks through a neon-lit Tokyo alley
at night. Camera follows from behind, tracking shot. Cyberpunk aesthetic,
moody lighting with pink and blue neon reflections on wet pavement.

# Product Shot
A sleek smartphone rotates slowly on a white marble surface. Camera orbits
around the device. Studio lighting with soft shadows, minimalist aesthetic,
commercial quality.

# Nature Documentary
A monarch butterfly emerging from its chrysalis in extreme close-up.
Time-lapse style, macro photography, natural morning light filtering
through leaves.
```

### Best Practices

1. **Be specific about movement** - Describe camera and subject motion explicitly
2. **Specify lighting** - "Golden hour", "studio lighting", "neon", etc.
3. **Reference styles** - "cinematic", "documentary", "commercial", "music video"
4. **Duration awareness** - Shorter prompts = faster, more coherent output
5. **Iterate** - Use re-cut and blend for refinement

### Limitations

- Max 20 seconds (Plus), 60 seconds (Pro)
- Text rendering still imperfect
- Human hands/fingers can have artifacts
- No direct API (use ChatGPT interface or Sora interface)
- Limited exports per month based on subscription

---

## Runway Gen-3 / Gen-4

### Overview

Industry-standard for professional video production. Best API support and control options.

**Pricing:**
- Standard: $0.05/second generated
- Turbo: $0.02/second (lower quality, faster)
- Unlimited plan: $96/month

### Gen-4 Features

| Feature | Description |
|---------|-------------|
| **Extended Duration** | Up to 40 seconds per generation |
| **Multi-Shot** | Plan and generate connected shots |
| **Camera Controls** | Pan, tilt, zoom, dolly, orbit |
| **Motion Brush** | Paint motion onto specific areas |
| **Structure Reference** | Maintain subject consistency |

### API Integration

```python
# Runway Gen-4 Python SDK
import runwayml

client = runwayml.RunwayML()

# Text-to-Video
text_task = client.text_to_video.create(
    model="gen4",
    prompt="A serene lake at sunrise, mist rising from the water, camera slowly pushes forward",
    duration=10,
    aspect_ratio="16:9",
    resolution="1080p"
)

# Poll for completion
import time
while text_task.status not in ["SUCCEEDED", "FAILED"]:
    text_task = client.tasks.retrieve(text_task.id)
    print(f"Status: {text_task.status}")
    time.sleep(5)

if text_task.status == "SUCCEEDED":
    video_url = text_task.output[0]
    print(f"Video ready: {video_url}")

# Image-to-Video
with open("scene.png", "rb") as f:
    image_data = f.read()

image_task = client.image_to_video.create(
    model="gen4",
    prompt_image=image_data,
    prompt_text="Camera slowly pans right, birds fly across the sky",
    duration=10,
    aspect_ratio="16:9"
)

# With Camera Controls
controlled_task = client.image_to_video.create(
    model="gen4",
    prompt_image=image_data,
    prompt_text="Gentle wind moves the grass",
    camera_motion={
        "horizontal": 0.3,   # Pan right
        "vertical": 0.0,     # No tilt
        "zoom": 0.1,         # Slight zoom in
        "roll": 0.0          # No roll
    },
    duration=10
)
```

### Camera Motion Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| `horizontal` | -1.0 to 1.0 | Pan left/right |
| `vertical` | -1.0 to 1.0 | Tilt up/down |
| `zoom` | -1.0 to 1.0 | Zoom out/in |
| `roll` | -1.0 to 1.0 | Rotate camera |

### Motion Brush Workflow

1. Upload source image
2. Paint mask over areas to animate
3. Describe motion for masked areas
4. Generate with motion applied only to selection

---

## Pika Labs 2.5

### Overview

Fast, cost-effective video generation with unique features like lip sync and sound effects.

**Pricing:**
- Free tier: 250 credits/month
- Pro: $8/month - 700 credits
- Unlimited: $28/month

### Key Features

| Feature | Description |
|---------|-------------|
| **Lip Sync** | Sync character lips to audio |
| **Sound Effects** | AI-generated SFX matching video |
| **Modify Region** | Edit specific parts of video |
| **Expand Canvas** | Outpaint video frames |
| **Pikaffects** | Special effects library |

### API Integration

```python
import requests
import time

PIKA_API_KEY = "your-api-key"
PIKA_BASE_URL = "https://api.pika.art/v1"

headers = {
    "Authorization": f"Bearer {PIKA_API_KEY}",
    "Content-Type": "application/json"
}

# Text-to-Video
response = requests.post(
    f"{PIKA_BASE_URL}/generate",
    headers=headers,
    json={
        "prompt": "A cat playing piano in a jazz club, cinematic lighting",
        "aspect_ratio": "16:9",
        "motion_strength": 3,  # 1-5 scale
        "guidance_scale": 12,
        "negative_prompt": "blurry, distorted, low quality"
    }
)

task_id = response.json()["task_id"]

# Poll for result
while True:
    status_response = requests.get(
        f"{PIKA_BASE_URL}/tasks/{task_id}",
        headers=headers
    )
    status = status_response.json()

    if status["status"] == "completed":
        video_url = status["output"]["video_url"]
        break
    elif status["status"] == "failed":
        raise Exception(f"Generation failed: {status['error']}")

    time.sleep(3)

# Image-to-Video with motion
with open("image.png", "rb") as f:
    files = {"image": f}
    data = {
        "prompt": "The character turns and smiles",
        "motion_strength": 2,
        "fps": 24
    }
    response = requests.post(
        f"{PIKA_BASE_URL}/image-to-video",
        headers={"Authorization": f"Bearer {PIKA_API_KEY}"},
        files=files,
        data=data
    )
```

### Pikaffects (Special Effects)

| Effect | Description |
|--------|-------------|
| Melt | Object melts into liquid |
| Explode | Particle explosion |
| Inflate | Object inflates like balloon |
| Crush | Object gets crushed |
| Cake-ify | Transform into cake |
| Squish | Squeeze and release |

---

## Kling 2.0

### Overview

Chinese-developed alternative with competitive quality and pricing. Good for budget-conscious projects.

**Access:** Web interface, limited API

### Features

| Feature | Description |
|---------|-------------|
| **Motion Templates** | Pre-built motion patterns |
| **Style Transfer** | Apply artistic styles |
| **Character Animation** | Consistent character motion |
| **Inpainting** | Edit specific regions |

### Best For

- Testing and prototyping
- Budget-conscious production
- Simple animations
- Social media content

### Limitations

- API access requires application
- Documentation primarily in Chinese
- Some features geo-restricted
- Processing queue can be slow

---

## Workflows

### Text-to-Video Workflow

```
1. CONCEPT
   ├── Define scene objective
   ├── Write detailed description
   └── Choose platform based on needs

2. PROMPT ENGINEERING
   ├── Subject: Who/what is in the scene
   ├── Action: What happens
   ├── Setting: Where, when
   ├── Camera: Movement, angle
   ├── Style: Aesthetic, mood
   └── Technical: Duration, aspect ratio

3. GENERATION
   ├── Start with shorter duration (5s)
   ├── Iterate on prompt
   ├── Try variations
   └── Select best result

4. REFINEMENT
   ├── Extend if needed
   ├── Apply fixes (inpainting)
   ├── Color grade
   └── Add audio

5. POST-PRODUCTION
   ├── Upscale if needed
   ├── Add music/SFX
   ├── Export in required format
   └── Archive prompts and settings
```

### Image-to-Video Workflow

```
1. IMAGE PREPARATION
   ├── High resolution (min 1024px)
   ├── Clean composition
   ├── Consider what will move
   └── Remove artifacts

2. MOTION PLANNING
   ├── What moves: subject, background, camera
   ├── Direction of movement
   ├── Speed/intensity
   └── Duration needed

3. GENERATION
   ├── Upload image
   ├── Describe motion in prompt
   ├── Set camera controls if available
   └── Generate and review

4. ITERATION
   ├── Adjust motion strength
   ├── Try different angles
   ├── Combine multiple generations
   └── Use motion brush for precision
```

### Multi-Shot Production

```
1. SCRIPT BREAKDOWN
   ├── Write or obtain script
   ├── Break into scenes
   ├── Break scenes into shots
   └── Note required visuals per shot

2. SHOT LIST
   Shot #  | Description      | Duration | Camera      | Platform
   01      | Estab. wide     | 5s       | Static      | Runway
   02      | Subject enters  | 10s      | Track right | Sora
   03      | Close-up face   | 5s       | Push in     | Runway
   04      | POV shot        | 5s       | Handheld    | Pika

3. GENERATION ORDER
   ├── Generate establishing shots first
   ├── Then action sequences
   ├── Finally close-ups and details
   └── Keep consistent style prompts

4. EDITING
   ├── Import all clips to timeline (Premiere, DaVinci)
   ├── Arrange in sequence
   ├── Add transitions
   ├── Color match all clips
   └── Add audio track

5. EXPORT
   ├── Master in highest quality
   ├── Create platform-specific versions
   └── Archive project files
```

---

## Style Consistency

### Maintaining Visual Coherence

| Technique | Description |
|-----------|-------------|
| **Style Prompt Base** | Use consistent style descriptors across all shots |
| **Reference Image** | Use same source image for related shots |
| **Character Sheets** | Generate reference images first, use for all videos |
| **Color Palette** | Specify exact colors in prompts |
| **Lighting Consistency** | Same lighting description across shots |

### Style Prompt Template

```
Base Style Prompt (prepend to all shots):
"[Shot description], cinematic film grain, color graded in teal and orange,
professional lighting, 24fps motion blur, shallow depth of field,
shot on RED camera --style [consistent_style_id]"
```

### Character Consistency

1. **Generate Character Reference**
   - Create detailed character image first
   - Document exact appearance details
   - Save as reference for all shots

2. **Description Template**
   ```
   [Character: young woman, dark curly hair, brown eyes, wearing
   olive green jacket and white t-shirt] + [action/scene]
   ```

3. **Use Image-to-Video**
   - Keep character image as starting frame
   - Describe motion, not appearance
   - Maintain same source across shots

---

## Video Editing Automation

### Bulk Generation Scripts

```python
# Batch video generation with Runway
import runwayml
import json
import time

client = runwayml.RunwayML()

# Load shot list
with open("shot_list.json") as f:
    shots = json.load(f)

# Example shot_list.json:
# [
#   {"id": "01", "prompt": "...", "duration": 5, "image": "shot01.png"},
#   {"id": "02", "prompt": "...", "duration": 10, "image": null}
# ]

results = []

for shot in shots:
    if shot.get("image"):
        # Image-to-video
        with open(shot["image"], "rb") as f:
            task = client.image_to_video.create(
                model="gen4",
                prompt_image=f.read(),
                prompt_text=shot["prompt"],
                duration=shot["duration"]
            )
    else:
        # Text-to-video
        task = client.text_to_video.create(
            model="gen4",
            prompt=shot["prompt"],
            duration=shot["duration"]
        )

    results.append({
        "shot_id": shot["id"],
        "task_id": task.id
    })

    print(f"Started shot {shot['id']}: {task.id}")
    time.sleep(2)  # Rate limiting

# Poll all tasks
completed = []
while len(completed) < len(results):
    for result in results:
        if result["shot_id"] in [c["shot_id"] for c in completed]:
            continue

        task = client.tasks.retrieve(result["task_id"])
        if task.status == "SUCCEEDED":
            completed.append({
                "shot_id": result["shot_id"],
                "url": task.output[0]
            })
            print(f"Completed shot {result['shot_id']}")
        elif task.status == "FAILED":
            print(f"Failed shot {result['shot_id']}: {task.error}")
            completed.append({"shot_id": result["shot_id"], "url": None})

    time.sleep(10)

# Save results
with open("generated_videos.json", "w") as f:
    json.dump(completed, f, indent=2)
```

### FFmpeg Post-Processing

```bash
# Concatenate multiple clips
ffmpeg -f concat -safe 0 -i clips.txt -c copy output.mp4

# clips.txt format:
# file 'shot01.mp4'
# file 'shot02.mp4'
# file 'shot03.mp4'

# Upscale to 4K
ffmpeg -i input.mp4 -vf "scale=3840:2160:flags=lanczos" -c:v libx264 -crf 18 output_4k.mp4

# Add audio track
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest output.mp4

# Create loop
ffmpeg -stream_loop 3 -i input.mp4 -c copy output_looped.mp4

# Adjust speed (2x faster)
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output_fast.mp4

# Add fade in/out (1 second each)
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=4:d=1" output.mp4

# Convert to GIF (for previews)
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos" -c:v gif output.gif
```

### DaVinci Resolve Automation

```python
# DaVinci Resolve script (run inside Resolve)
import DaVinciResolveScript as dvr

resolve = dvr.scriptapp("Resolve")
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()

# Create timeline
media_pool = project.GetMediaPool()
timeline = media_pool.CreateTimelineFromClips(
    "AI Generated Sequence",
    clips_list  # List of imported clips
)

# Add transitions
for i, clip in enumerate(timeline.GetItemListInTrack("video", 1)):
    if i > 0:
        timeline.AddTransition(
            clip,
            "Cross Dissolve",
            duration=24  # frames
        )

# Color match
project.SetCurrentTimeline(timeline)
timeline.ApplyGradeFromDRX(0, "color_grade.drx")

# Render
project.SetCurrentRenderFormatAndCodec("mp4", "H265_NVIDIA")
project.SetRenderSettings({
    "TargetDir": "/output/",
    "CustomName": "final_output"
})
project.AddRenderJob()
project.StartRendering()
```

---

## Storyboarding

### Pre-Production Planning

```markdown
# Storyboard Template

## Project: [Title]
## Total Duration: [X seconds/minutes]
## Platform: [Sora/Runway/Pika]

---

### Shot 01
- **Duration:** 5s
- **Visual:** Wide establishing shot of city at dawn
- **Camera:** Slow push forward
- **Motion:** Cars moving on streets below
- **Audio:** Ambient city sounds
- **Prompt:** "Aerial view of Manhattan at dawn, golden hour lighting,
  camera slowly pushes forward toward the skyline, cars visible on
  streets below, cinematic, 4K quality"
- **Reference:** [image link]

---

### Shot 02
- **Duration:** 3s
- **Visual:** Close-up of protagonist's eyes opening
- **Camera:** Static, then slight push in
- **Motion:** Eyes open, blink
- **Audio:** Alarm clock sound
- **Prompt:** "Extreme close-up of human eyes opening, morning light
  falling across face, eyes blink twice, photorealistic, shallow DOF"
- **Reference:** [image link]
```

### Sora Storyboard Mode

1. **Access Storyboard**
   - Open Sora interface
   - Select "Storyboard" mode
   - Define timeline length

2. **Add Shots**
   - Click to add shot markers
   - Write prompt for each shot
   - Upload reference images

3. **Connect Shots**
   - Define transitions between shots
   - Set camera continuity
   - Preview full sequence

4. **Generate**
   - Generate all shots in sequence
   - Review and regenerate as needed
   - Export final video

---

## Resolution and Export

### Supported Resolutions

| Platform | Max Resolution | Aspect Ratios |
|----------|---------------|---------------|
| Sora 2 | 1920x1080 | 16:9, 9:16, 1:1 |
| Runway Gen-4 | 4096x2160 | 16:9, 9:16, 1:1, 4:5, 21:9 |
| Pika 2.5 | 1920x1080 | 16:9, 9:16, 1:1 |
| Kling 2.0 | 1920x1080 | 16:9, 9:16 |

### Platform-Specific Exports

| Platform | Resolution | Aspect | Duration | Notes |
|----------|------------|--------|----------|-------|
| YouTube | 1920x1080+ | 16:9 | Any | Include 2s intro/outro |
| TikTok | 1080x1920 | 9:16 | 15-60s | Vertical, fast-paced |
| Instagram Reels | 1080x1920 | 9:16 | 15-90s | Vertical |
| Instagram Post | 1080x1350 | 4:5 | 3-60s | Square or tall |
| Twitter/X | 1280x720 | 16:9 | 2:20 max | Keep under 512MB |
| LinkedIn | 1920x1080 | 16:9 | 3-10min | Professional content |

### Upscaling

For higher resolution output:

```python
# Using Topaz Video AI (via CLI)
import subprocess

subprocess.run([
    "tvai",
    "--input", "generated_1080p.mp4",
    "--output", "upscaled_4k.mp4",
    "--model", "proteus-3",
    "--scale", "2",
    "--format", "mp4"
])

# Using Real-ESRGAN for frames
# 1. Extract frames
subprocess.run([
    "ffmpeg", "-i", "input.mp4",
    "-vf", "fps=24",
    "frames/frame_%04d.png"
])

# 2. Upscale frames
subprocess.run([
    "realesrgan-ncnn-vulkan",
    "-i", "frames/",
    "-o", "upscaled_frames/",
    "-n", "realesrgan-x4plus"
])

# 3. Reassemble video
subprocess.run([
    "ffmpeg", "-framerate", "24",
    "-i", "upscaled_frames/frame_%04d.png",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "upscaled_video.mp4"
])
```

---

## Cost Comparison

### Monthly Subscription Comparison

| Platform | Free Tier | Basic | Pro | Unlimited |
|----------|-----------|-------|-----|-----------|
| Sora 2 | - | $20/mo (Plus) | $200/mo (Pro) | - |
| Runway | 125 credits | $15/mo | $35/mo | $96/mo |
| Pika | 250 credits | $8/mo | $28/mo | $58/mo |
| Kling | Yes | $5/mo | $10/mo | - |

### Per-Video Cost Estimate

| Video Type | Duration | Sora | Runway | Pika |
|------------|----------|------|--------|------|
| Social clip | 5s | ~$1 | $0.25 | $0.20 |
| Product demo | 30s | ~$5 | $1.50 | $1.00 |
| Short film | 2min | ~$20 | $6.00 | $4.00 |

### Cost Optimization Tips

1. **Prototype cheap, produce premium**
   - Use Pika/Kling for concept testing
   - Generate final in Sora/Runway

2. **Optimize duration**
   - Shorter clips = lower cost
   - Combine clips in post-production

3. **Batch processing**
   - Generate during off-peak hours
   - Use API for bulk discounts

4. **Cache and reuse**
   - Save successful prompts
   - Extend existing clips vs. generating new

---

## Common Issues and Solutions

### Quality Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Blurry output | Low motion, poor prompt | Increase motion strength, add detail |
| Morphing faces | Complex motion, profile views | Use front-facing shots, shorter duration |
| Flickering | Frame inconsistency | Reduce motion, use image-to-video |
| Artifacts | Complex scene, hands/text | Simplify scene, avoid text generation |
| Wrong style | Vague prompt | Add explicit style references |

### Motion Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No movement | Motion strength too low | Increase motion parameter |
| Chaotic motion | Too many moving elements | Focus on one subject |
| Unnatural motion | Over-prompting | Simplify motion description |
| Camera drift | Default behavior | Specify "static camera" |

### Consistency Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Character changes | No reference | Use same source image |
| Color mismatch | Different generations | Add color palette to prompt |
| Style drift | Inconsistent prompts | Create base style prompt |

---

## Integration with Other Skills

| Skill | Integration Point |
|-------|------------------|
| **faion-image-gen-skill** | Generate source images for image-to-video |
| **faion-audio-skill** | Add voiceover, music, sound effects |
| **faion-langchain-skill** | Automate video generation pipelines |
| **faion-openai-api-skill** | Access Sora API when available |

---

## Tools and Resources

| Tool | Purpose | Link |
|------|---------|------|
| FFmpeg | Video processing CLI | ffmpeg.org |
| DaVinci Resolve | Professional editing | blackmagicdesign.com |
| Topaz Video AI | Upscaling | topazlabs.com |
| Runway API | Programmatic access | docs.runwayml.com |
| Pika API | Programmatic access | pika.art/api |

---

## References

- [Runway Documentation](https://docs.runwayml.com)
- [Pika Labs API](https://pika.art/api)
- [Sora User Guide](https://openai.com/sora)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Video Encoding Best Practices](https://developer.apple.com/documentation/avfoundation)

---

*Skill Version: 1.0*
*Last Updated: 2026-01-18*
*Part of Faion Network AI/LLM Skills*
