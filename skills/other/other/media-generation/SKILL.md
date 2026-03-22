---
name: media-generation
description: Generate images and videos using fal.ai models through Cloudflare AI Gateway — understand the API, craft prompts, and configure options. Use when the user mentions "generate an image", "generate a video", "create media", "AI image", "AI video", "fal.ai", "seedream", "seedance", or "media prompt".
---

# Media Generation

Website Foundation generates images and videos through Cloudflare AI Gateway, proxying requests to fal.ai. No API key is needed in the application code — the gateway handles authentication.

## Library Functions

`src/lib/media.ts` exports two functions:

### `generateImage(env, prompt, options?)`

- **Model**: Seedream v4.5 (ByteDance)
- **Default size**: `auto_2K` (2048x2048)
- **Cost**: ~$0.04 per image
- **Returns**: Raw `Response` from fal.ai with `images[].url`

### `generateVideo(env, prompt, options?)`

- **Model**: Seedance 1.5 Pro (ByteDance)
- **Defaults**: 16:9 aspect ratio, 720p, 5 seconds, with audio
- **Cost**: ~$0.26 per 5s video
- **Returns**: Raw `Response` from fal.ai with `video.url`

## API Routes

Both require Cloudflare Access authentication:

- `POST /api/media/generate-image` — Accepts `{ prompt, imageSize? }`
- `POST /api/media/generate-video` — Accepts `{ prompt, aspectRatio?, resolution?, duration? }`

## Prompt Tips

- Be specific and descriptive — include subject, setting, lighting, style
- For text in images, Seedream supports rendered text: include `The text "..." should appear`
- For video, describe action and camera movement; include audio cues for sound generation
- Keep prompts under 500 characters for best results

## References

- [Seedream API reference](references/seedream-api.md) — Full input/output schema for image generation
- [Seedance API reference](references/seedance-api.md) — Full input/output schema for video generation
