# RouterBase Media Generation Notes

Use this reference when building image, video, or audio workflows.

## Source Pages

- https://docs.routerbase.com
- https://docs.routerbase.com/api-reference/images
- https://docs.routerbase.com/overview

## Endpoints

```text
POST https://routerbase.com/v1/images/generations
POST https://routerbase.com/v1/videos/generations
POST https://routerbase.com/v1/audio/speech
POST https://routerbase.com/v1/audio/generations
```

RouterBase docs describe chat and image responses as synchronous. Video and audio generation are asynchronous: the initial request returns an ID and pending status, then the app polls the task endpoint or supplies a callback URL.

## Image Generation

Basic fields:

- `model`: image model ID, required.
- `prompt`: text description, required.
- `n`: number of images, default `1`.
- `aspect_ratio`: example values include `1:1`, `16:9`, `9:16`, `4:3`, `3:4`.
- `resolution`: example values include `1K`, `2K`, `4K`.
- `quality`: example values include `hd`, `standard`.
- `style`: example values include `natural`, `vivid`.
- `negative_prompt`: content to exclude, model-dependent.
- `image_urls`: required for image-to-image, editing, upscale, reframe, or remix models.

Example:

```bash
curl -X POST https://routerbase.com/v1/images/generations \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/imagen-4",
    "prompt": "A red apple on a white table",
    "aspect_ratio": "1:1",
    "resolution": "1K"
  }'
```

Example response shape:

```json
{
  "created": 1776245700,
  "data": [
    { "url": "https://media.routerbase.com/media/<user>/<gen>/0.png" }
  ]
}
```

## Async Task Handling

Persist these fields for video/audio jobs:

- request payload
- task ID
- created timestamp
- model ID
- status
- polling attempt count
- result URLs
- error code/message
- credits or cost fields when returned

Recommended polling behavior:

1. Poll with short initial delay.
2. Use exponential backoff with an upper cap.
3. Stop on terminal success/failure.
4. Surface a user-visible timeout if the job takes too long.
5. Continue background polling where the product supports it.

## Retention

RouterBase docs state generated media files for video and image are retained for 14 days, and log records for 2 months. Download and store generated media on the application side before expiry.

## Model Examples

Verify these against the live catalog before production:

Image:

- `google/imagen-4`
- `blackforestlabs/flux-2-pro`
- `blackforestlabs/flux-2-pro-i2i`
- `ideogram/ideogram-3-0`

Video:

- `google/veo-3-1-fast`
- `google/veo-3-1-quality`
- `xai/grok-imagine`
- `kuaishou/kling-v3-4k-t2v`

Audio:

- `elevenlabs/tts-turbo`
- `elevenlabs/tts-multilingual`
- `suno/suno-v5`
