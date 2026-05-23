---
name: veo-frames-to-video
description: Generate video from first and last frame images using fal.ai Veo 3.1. Use when the user wants to create a video transition between two images, morph between scenes, or generate smooth video connecting a starting and ending frame.
allowed-tools: Bash, Read, Write
---

# Veo 3.1 First-Last-Frame-to-Video

Generate smooth video transitions between two frames using Google DeepMind's Veo 3.1 model via fal.ai.

## Prerequisites

- `FAL_KEY` environment variable must be set (typically in `~/.zshrc`)

## API Endpoint

`POST https://fal.run/fal-ai/veo3.1/first-last-frame-to-video`

## Parameters

### Required
- `prompt` (string): Text description of how the video should transition between frames
- `first_frame_url` (string): URL of the first/starting frame
- `last_frame_url` (string): URL of the last/ending frame

### Optional
| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `duration` | string | "8s" | "4s", "6s", "8s" |
| `aspect_ratio` | string | "auto" | "auto", "9:16", "16:9" |
| `resolution` | string | "720p" | "720p", "1080p" |
| `generate_audio` | boolean | true | Enable/disable audio generation |

## Usage

### cURL
```bash
curl --request POST \
  --url https://fal.run/fal-ai/veo3.1/first-last-frame-to-video \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "prompt": "Smooth time-lapse transition from day to night as the sun sets",
    "first_frame_url": "https://example.com/daytime-scene.jpg",
    "last_frame_url": "https://example.com/nighttime-scene.jpg",
    "duration": "8s",
    "resolution": "1080p",
    "generate_audio": true
  }'
```

### Python
```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/veo3.1/first-last-frame-to-video",
    arguments={
        "prompt": "Smooth time-lapse transition from day to night as the sun sets",
        "first_frame_url": "https://example.com/daytime-scene.jpg",
        "last_frame_url": "https://example.com/nighttime-scene.jpg",
        "duration": "8s",
        "resolution": "1080p",
        "generate_audio": True
    }
)

# Access the generated video URL
video_url = result["video"]["url"]
print(f"Generated video: {video_url}")
```

### JavaScript
```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/veo3.1/first-last-frame-to-video", {
  input: {
    prompt: "Smooth time-lapse transition from day to night as the sun sets",
    first_frame_url: "https://example.com/daytime-scene.jpg",
    last_frame_url: "https://example.com/nighttime-scene.jpg",
    duration: "8s",
    resolution: "1080p",
    generate_audio: true
  }
});

console.log("Generated video:", result.video.url);
```

## Response Format

```json
{
  "video": {
    "url": "https://storage.googleapis.com/.../output.mp4"
  }
}
```

## Examples

1. **Time-lapse transition**:
   - First frame: Morning cityscape
   - Last frame: Same cityscape at night
   - Prompt: "Time-lapse of the city from morning to night, lights gradually turning on"

2. **Seasonal change**:
   - First frame: Summer landscape
   - Last frame: Winter landscape (same location)
   - Prompt: "Seasons change from summer to winter, leaves fall and snow covers the ground"

3. **Transformation**:
   - First frame: Empty room
   - Last frame: Furnished room
   - Prompt: "Furniture magically appears and arranges itself in the room"

4. **Growth animation**:
   - First frame: Seed in soil
   - Last frame: Full-grown plant
   - Prompt: "Plant grows from seed, stem emerges and leaves unfold"

5. **Scene morphing**:
   - First frame: Photo of a person
   - Last frame: Artistic painting of the same person
   - Prompt: "Realistic photo gradually transforms into an impressionist painting"

## Tips

- Ensure both frames have similar composition for smooth transitions
- Describe the transition motion/action in the prompt
- Works best when both frames share similar subjects or scenes
- Use longer duration (8s) for complex transitions
- The AI will interpolate the motion between the two frames

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid FAL_KEY | Verify key at fal.ai dashboard |
| `429 Too Many Requests` | Rate limit exceeded | Wait 60 seconds, retry |
| `400 Bad Request` | Invalid frame URLs or mismatch | Use similar composition frames |
| `500 Server Error` | API temporary issue | Retry after 30 seconds |
| `Timeout` | Video generation taking too long | Use 720p or 4s duration |
