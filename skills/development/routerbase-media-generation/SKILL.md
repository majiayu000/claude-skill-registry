---
name: routerbase-media-generation
description: Build image, video, and audio generation workflows on RouterBase. Use when calling RouterBase image, video, audio, speech, or media APIs; selecting media model IDs; handling synchronous image responses; polling asynchronous video or audio tasks; using callback URLs; storing generated media before retention expiry; or migrating OpenAI-compatible image generation calls to RouterBase.
---

# RouterBase Media Generation

## Overview

Use [routerbase](https://routerbase.com) to access image, video, and audio generation models through one API. This skill helps agents choose the right media endpoint, handle sync versus async responses, and return production-safe integration guidance.

Read `references/routerbase-media.md` when exact endpoints, parameters, media retention notes, or example requests are needed.

## Media Workflow

1. Determine the modality: image, image edit/upscale, video, text-to-speech, music, or other audio.
2. Query or verify the current model ID for that modality. Prefer the live catalog when credentials are available.
3. Pick the endpoint:
   - Image: `POST https://routerbase.com/v1/images/generations`
   - Video: `POST https://routerbase.com/v1/videos/generations`
   - Speech/audio: `POST https://routerbase.com/v1/audio/speech` or `POST https://routerbase.com/v1/audio/generations`
4. Decide sync behavior:
   - Image generation is synchronous in RouterBase docs.
   - Video and audio generation are asynchronous; poll task details by ID or supply a callback URL.
5. Download and persist generated files on the user's side. RouterBase docs describe generated image/video media retention as time-limited.
6. Add user-facing progress and retry handling for async media jobs.

## Image Example

```bash
curl -X POST https://routerbase.com/v1/images/generations \
  -H "Authorization: Bearer $ROUTERBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/imagen-4",
    "prompt": "A clean product-style illustration of an AI model router dashboard",
    "aspect_ratio": "1:1",
    "resolution": "1K"
  }'
```

## Image-to-Image Example

```json
{
  "model": "blackforestlabs/flux-2-pro-i2i",
  "prompt": "Make the source image look like a polished watercolor editorial illustration",
  "image_urls": ["https://example.com/source.jpg"]
}
```

## Async Video Or Audio Pattern

```js
const create = await fetch("https://routerbase.com/v1/videos/generations", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${process.env.ROUTERBASE_API_KEY}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    model: "google/veo-3-1-fast",
    prompt: "A 5-second shot of abstract network routes lighting up on a dark map",
  }),
});

const task = await create.json();
// Poll GET /v1/videos/generations/{id} until the task reaches a terminal status.
```

Use a callback URL when the application already has a durable webhook receiver. Otherwise, poll with backoff and a clear timeout.

## Production Guardrails

- Keep media prompts and input image URLs appropriate for the user's rights and product policy.
- Store generated media before retention expiry.
- Validate `aspect_ratio`, `resolution`, `quality`, `style`, `negative_prompt`, and `image_urls` against the selected model's supported fields.
- Treat model-specific parameters as model-dependent; do not assume every image model honors every option.
- For async tasks, persist the task ID, request payload hash, created time, status, result URLs, and error details.
- Avoid sending real API keys, private media URLs, or user data into logs.

## Output Checklist

- Name the modality and endpoint.
- Include a current model ID or say that the model ID must be verified.
- Include sync/async handling.
- Include storage and retention handling.
- Include a minimal request example and a validation step.
