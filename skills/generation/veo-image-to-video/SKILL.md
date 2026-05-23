---
name: veo-image-to-video
description: Animate a single image into a video using fal.ai Veo 3.1. Use when the user wants to create a video from a still image, animate a photo, or bring an image to life. Supports up to 8 seconds of video with optional audio.
allowed-tools: Bash, Read, Write
---

# Veo 3.1 Image-to-Video

Animate a single image into a dynamic video using Google DeepMind's Veo 3.1 model via fal.ai.

## Prerequisites

- `FAL_KEY` environment variable must be set (typically in `~/.zshrc`)
- Input image should be 720p or higher resolution

## API Endpoint

`POST https://fal.run/fal-ai/veo3.1/image-to-video`

## Parameters

### Required
- `prompt` (string): Text description of the video motion/action to generate
- `image_url` (string): URL of the input image to animate

### Optional
| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `duration` | string | "8s" | "4s", "6s", "8s" |
| `aspect_ratio` | string | "auto" | "auto", "9:16", "16:9" |
| `resolution` | string | "720p" | "720p", "1080p" |
| `generate_audio` | boolean | true | Uses 50% fewer credits if disabled |

## Usage

### cURL
```bash
curl --request POST \
  --url https://fal.run/fal-ai/veo3.1/image-to-video \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "prompt": "The camera slowly pans across the scene as leaves gently sway in the breeze",
    "image_url": "https://example.com/landscape.jpg",
    "duration": "8s",
    "resolution": "1080p",
    "generate_audio": true
  }'
```

### Python
```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/veo3.1/image-to-video",
    arguments={
        "prompt": "The camera slowly pans across the scene as leaves gently sway in the breeze",
        "image_url": "https://example.com/landscape.jpg",
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

const result = await fal.subscribe("fal-ai/veo3.1/image-to-video", {
  input: {
    prompt: "The camera slowly pans across the scene as leaves gently sway in the breeze",
    image_url: "https://example.com/landscape.jpg",
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

1. **Nature animation**:
   - Image: A forest scene
   - Prompt: "Wind rustles through the trees, birds fly across the sky"

2. **Portrait animation**:
   - Image: A portrait photo
   - Prompt: "The person slowly turns their head and smiles"

3. **Cinematic movement**:
   - Image: A cityscape
   - Prompt: "Slow cinematic zoom out revealing the full city skyline at dusk"

4. **Water animation**:
   - Image: Ocean or lake scene
   - Prompt: "Gentle waves roll onto the shore, water sparkles in sunlight"

## Tips

- Use descriptive motion language (pan, zoom, sway, flow)
- Describe camera movements for cinematic effects
- Higher resolution (1080p) provides better quality but takes longer
- Disable audio generation to save credits when not needed
- Ensure input image is at least 720p for best results

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid FAL_KEY | Verify key at fal.ai dashboard |
| `429 Too Many Requests` | Rate limit exceeded | Wait 60 seconds, retry |
| `400 Bad Request` | Invalid image URL or low resolution | Use 720p+ image |
| `500 Server Error` | API temporary issue | Retry after 30 seconds |
| `Timeout` | Video generation taking too long | Use 720p or shorter duration |
