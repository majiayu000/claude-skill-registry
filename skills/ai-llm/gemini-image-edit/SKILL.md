---
name: gemini-image-edit
description: Edit existing images with text prompts using fal.ai Gemini 3 Pro. Use when the user wants to modify, edit, transform, or change an existing image based on a text description. Supports multiple input images for context.
allowed-tools: Bash, Read, Write
---

# Gemini Image Editing

Edit and transform existing images using text prompts with Google's Gemini 3 Pro model via fal.ai.

## Prerequisites

- `FAL_KEY` environment variable must be set (typically in `~/.zshrc`)

## API Endpoint

`POST https://fal.run/fal-ai/gemini-3-pro-image-preview/edit`

## Parameters

### Required
- `prompt` (string): The editing instruction describing what changes to make
- `image_urls` (array of strings): URLs of the images to edit

### Optional
| Parameter | Type | Default | Options |
|-----------|------|---------|---------|
| `num_images` | integer | 1 | 1-4 |
| `aspect_ratio` | string | "auto" | "auto", "21:9", "16:9", "3:2", "4:3", "5:4", "1:1", "4:5", "3:4", "2:3", "9:16" |
| `output_format` | string | "png" | "jpeg", "png", "webp" |
| `resolution` | string | "1K" | "1K", "2K", "4K" |
| `sync_mode` | boolean | false | Returns data URI when true |
| `enable_web_search` | boolean | false | Uses current web data for generation |
| `limit_generations` | boolean | false | Restricts to 1 image per prompt round |

## Usage

### cURL
```bash
curl --request POST \
  --url https://fal.run/fal-ai/gemini-3-pro-image-preview/edit \
  --header "Authorization: Key $FAL_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "prompt": "Add snow to this mountain scene and make it winter",
    "image_urls": ["https://example.com/mountain.jpg"],
    "num_images": 1,
    "output_format": "png"
  }'
```

### Python
```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/gemini-3-pro-image-preview/edit",
    arguments={
        "prompt": "Add snow to this mountain scene and make it winter",
        "image_urls": ["https://example.com/mountain.jpg"],
        "num_images": 1
    }
)

# Access the edited image URL
edited_url = result["images"][0]["url"]
print(f"Edited image: {edited_url}")
```

### JavaScript
```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/gemini-3-pro-image-preview/edit", {
  input: {
    prompt: "Add snow to this mountain scene and make it winter",
    image_urls: ["https://example.com/mountain.jpg"],
    num_images: 1
  }
});

console.log("Edited image:", result.images[0].url);
```

## Response Format

```json
{
  "images": [
    {
      "file_name": "edited_image.png",
      "content_type": "image/png",
      "url": "https://storage.googleapis.com/..."
    }
  ],
  "description": "A description of the edited image"
}
```

## Examples

1. **Style transformation**:
   - Prompt: "Convert this photo to a watercolor painting style"

2. **Object addition**:
   - Prompt: "Add a rainbow in the sky"

3. **Scene modification**:
   - Prompt: "Change the time of day to sunset with golden hour lighting"

4. **Multiple reference images**:
   - Prompt: "Combine elements from these images into a cohesive scene"
   - Provide multiple URLs in `image_urls` array

## Tips

- Be specific about what changes you want
- Use descriptive language for style changes
- Multiple images can be provided for context or combining elements
- The `auto` aspect ratio preserves the original image proportions

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid FAL_KEY | Verify key at fal.ai dashboard |
| `429 Too Many Requests` | Rate limit exceeded | Wait 60 seconds, retry |
| `400 Bad Request` | Invalid image URL or parameters | Ensure image URLs are accessible |
| `500 Server Error` | API temporary issue | Retry after 30 seconds |
| `Timeout` | Generation taking too long | Reduce resolution or simplify edit |
