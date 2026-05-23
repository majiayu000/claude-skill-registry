---
name: veo-reference-video
description: Generate video with consistent subject appearance using reference images via fal.ai Veo 3.1. Use when the user wants to create a video featuring specific people, objects, or characters that should look consistent throughout. Supports multiple reference images for better subject consistency.
allowed-tools: Bash, Read, Write
---

# Veo 3.1 Reference-to-Video

Generate videos with consistent subject appearance using reference images via Google DeepMind's Veo 3.1 model on fal.ai.

## Prerequisites

- `FAL_KEY` environment variable must be set (typically in `~/.zshrc`)

## API Endpoint

`POST https://fal.run/fal-ai/veo3.1/reference-to-video`

## Parameters

### Required
- `prompt` (string): Text description of the video scene and action
- `image_urls` (array of strings): URLs of reference images for consistent subject appearance

### Optional
| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `duration` | string | "8s" | "8s" |
| `resolution` | string | "720p" | "720p", "1080p" |
| `generate_audio` | boolean | true | Enable/disable audio generation |

## Usage

### cURL
```bash
curl --request POST \
  --url https://fal.run/fal-ai/veo3.1/reference-to-video \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "prompt": "The character walks through a sunny park, looking around curiously",
    "image_urls": [
      "https://example.com/character-front.jpg",
      "https://example.com/character-side.jpg"
    ],
    "duration": "8s",
    "resolution": "1080p",
    "generate_audio": true
  }'
```

### Python
```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/veo3.1/reference-to-video",
    arguments={
        "prompt": "The character walks through a sunny park, looking around curiously",
        "image_urls": [
            "https://example.com/character-front.jpg",
            "https://example.com/character-side.jpg"
        ],
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

const result = await fal.subscribe("fal-ai/veo3.1/reference-to-video", {
  input: {
    prompt: "The character walks through a sunny park, looking around curiously",
    image_urls: [
      "https://example.com/character-front.jpg",
      "https://example.com/character-side.jpg"
    ],
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

1. **Character video**:
   - References: Multiple angles of a character
   - Prompt: "The character runs through a forest, jumping over fallen logs"

2. **Product showcase**:
   - References: Product photos from different angles
   - Prompt: "The product rotates on a display stand with dramatic lighting"

3. **Pet video**:
   - References: Photos of a pet from various angles
   - Prompt: "The dog plays fetch in a backyard, running and jumping"

4. **Avatar animation**:
   - References: Avatar/character design images
   - Prompt: "The avatar waves hello and then starts dancing"

## Tips

- Provide multiple reference images from different angles for better consistency
- Use clear, well-lit reference images
- Describe both the scene and the subject's actions in the prompt
- More reference images generally lead to better subject consistency
- Works best with distinct, recognizable subjects

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid FAL_KEY | Verify key at fal.ai dashboard |
| `429 Too Many Requests` | Rate limit exceeded | Wait 60 seconds, retry |
| `400 Bad Request` | Invalid image URLs | Ensure all reference URLs are accessible |
| `500 Server Error` | API temporary issue | Retry after 30 seconds |
| `Timeout` | Video generation taking too long | Use 720p or fewer references |
