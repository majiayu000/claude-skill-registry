---
name: imagerouter
description: Generate AI images with any model using ImageRouter API (requires API key).
homepage: https://imagerouter.io
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["curl"]}}}
---

# ImageRouter Image Generation

Generate images with any model available on ImageRouter using curl commands.

## Available models
The `test/test` model is a free dummy model that is used for testing the API. It is not a real model, therefore you should use other models for image generation.

Get top 10 most popular models:
```bash
curl -X POST 'https://backend.imagerouter.io/operations/get-popular-models'
```

Search available models by name:
```bash
curl "https://api.imagerouter.io/v1/models?type=image&sort=date&name=gemini"
```

Get all available models:
```bash
curl "https://api.imagerouter.io/v1/models?type=image&sort=date&limit=1000"
```

## Quick Start - Text-to-Image

Basic generation with JSON endpoint:
```bash
curl 'https://api.imagerouter.io/v1/openai/images/generations' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  --json '{
    "prompt": "a serene mountain landscape at sunset",
    "model": "test/test",
    "quality": "auto",
    "size": "auto",
    "response_format": "url",
    "output_format": "webp"
  }'
```

## Unified Endpoint (Text-to-Image & Image-to-Image)

### Text-to-Image with multipart/form-data:
```bash
curl 'https://api.imagerouter.io/v1/openai/images/edits' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -F 'prompt=a cyberpunk city at night' \
  -F 'model=test/test' \
  -F 'quality=high' \
  -F 'size=1024x1024' \
  -F 'response_format=url' \
  -F 'output_format=webp'
```

### Image-to-Image (with input images):
```bash
curl 'https://api.imagerouter.io/v1/openai/images/edits' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -F 'prompt=transform this into a watercolor painting' \
  -F 'model=test/test' \
  -F 'quality=auto' \
  -F 'size=auto' \
  -F 'response_format=url' \
  -F 'output_format=webp' \
  -F 'image[]=@/path/to/your/image.webp'
```

### Multiple images (up to 16):
```bash
curl 'https://api.imagerouter.io/v1/openai/images/edits' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -F 'prompt=combine these images' \
  -F 'model=test/test' \
  -F 'image[]=@image1.webp' \
  -F 'image[]=@image2.webp' \
  -F 'image[]=@image3.webp'
```

### With mask (some models require mask for inpainting):
```bash
curl 'https://api.imagerouter.io/v1/openai/images/edits' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -F 'prompt=fill the masked area with flowers' \
  -F 'model=test/test' \
  -F 'image[]=@original.webp' \
  -F 'mask[]=@mask.webp'
```

## Parameters

- **model** (required): Image model to use (see https://imagerouter.io/models)
- **prompt** (optional): Text description for generation. Most models require a text prompt, but not all.
- **quality** (optional): `auto` (default), `low`, `medium`, `high`
- **size** (optional): `auto` (default) or `WIDTHxHEIGHT` (e.g., `1024x1024`).
- **response_format** (optional): 
  - `url` (default) - Returns hosted URL
  - `b64_json` - Returns base64-encoded image
  - `b64_ephemeral` - Base64 without saving to logs
- **output_format** (optional): `webp` (default), `jpeg`, `png`
- **image[]** (optional): Input file for Image-to-Image (multipart only)
- **mask[]** (optional): Editing mask for inpainting (multipart only)

## Response Format

```json
{
  "created": 1769286389027,
  "data": [
    {
      "url": "https://storage.imagerouter.io/fffb4426-efbd-4bcc-87d5-47e6936bf0bb.webp"
    }
  ],
  "latency": 6942,
  "cost": 0.004
}
```

## Endpoint Comparison

| Feature | Unified (/edits) | JSON (/generations) |
|---------|------------------|---------------------|
| Text-to-Image | ✅ | ✅ |
| Image-to-Image | ✅ | ❌ |
| Encoding | multipart/form-data | application/json |

## Tips

- Both `/v1/openai/images/generations` and `/v1/openai/images/edits` are the same for the unified endpoint
- Use JSON endpoint for simple text-to-image when you don't need file uploads
- Use unified endpoint when you need Image-to-Image capabilities
- Check model features at https://imagerouter.io/models (quality support, edit support, etc.)
- Get your API key at https://imagerouter.io/api-keys

## Examples by Use Case

### Quick test generation:
```bash
curl 'https://api.imagerouter.io/v1/openai/images/generations' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  --json '{"prompt":"test image","model":"test/test"}'
```

### Download image directly:
```bash
curl 'https://api.imagerouter.io/v1/openai/images/generations' \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  --json '{"prompt":"abstract art","model":"test/test"}' \
  | jq -r '.data[0].url' \
  | xargs curl -o output.webp
```
