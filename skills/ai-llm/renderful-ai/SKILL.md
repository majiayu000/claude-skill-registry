---
name: renderful-ai
description: |
  Generate images and videos via renderful.ai API (FLUX, Kling, Sora, WAN, etc.) with crypto payments.
  Use when the user wants to create AI images, videos, or needs a crypto-friendly generation service.
  Triggers: renderful, renderful.ai, generate image, generate video, crypto payment generation
allowed-tools: Bash(curl), Web(fetch)
---

# Renderful AI

Generate AI images and videos using the renderful.ai API. Pay with crypto (Base/Polygon/Solana).

## API Base URL

```
https://api.renderful.ai/v1
```

## Authentication

Get API key from https://renderful.ai/dashboard

```bash
# Set as environment variable
export RENDERFUL_API_KEY="rf_your_api_key"
```

## Quick Start

### Generate an Image

```bash
curl -X POST https://api.renderful.ai/v1/generate \
  -H "Authorization: Bearer $RENDERFUL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flux-dev",
    "prompt": "a cat astronaut floating in space, cinematic lighting",
    "width": 1024,
    "height": 1024,
    "steps": 28
  }'
```

### Generate a Video

```bash
curl -X POST https://api.renderful.ai/v1/generate \
  -H "Authorization: Bearer $RENDERFUL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kling-1.6",
    "prompt": "a serene mountain landscape at sunset, camera slowly panning",
    "duration": 5,
    "width": 1280,
    "height": 720
  }'
```

## Available Models

### Image Models

| Model | Description | Best For |
|-------|-------------|----------|
| `flux-dev` | FLUX.1 Dev | General purpose, high quality |
| `flux-schnell` | FLUX.1 Schnell | Fast generation |
| `flux-pro` | FLUX.1 Pro | Highest quality |
| `sdxl` | Stable Diffusion XL | Classic diffusion |
| `gemini-3` | Gemini 3 Pro Image | Google image gen |
| `grok-imagine` | Grok Imagine | X/Twitter integration |
| `seedream` | Seedream 4.5 | Asian aesthetic |
| `reve` | Reve Image | Artistic styles |

### Video Models

| Model | Description | Duration |
|-------|-------------|----------|
| `kling-1.6` | Kling 1.6 | Up to 10s |
| `kling-1.5` | Kling 1.5 | Up to 10s |
| `veo-3` | Google Veo 3 | Up to 8s |
| `veo-2` | Google Veo 2 | Up to 8s |
| `seedance` | Seedance 1.5 | Up to 10s |
| `wan-2.5` | Wan 2.5 | Up to 10s |
| `ltx` | LTX Video | Up to 10s |
| `omnihuman` | OmniHuman | Portrait videos |

## Image Generation Options

```json
{
  "model": "flux-dev",
  "prompt": "required - your image description",
  "negative_prompt": "optional - what to avoid",
  "width": 1024,
  "height": 1024,
  "steps": 28,
  "seed": 42,
  "format": "png"
}
```

## Video Generation Options

```json
{
  "model": "kling-1.6",
  "prompt": "required - your video description",
  "duration": 5,
  "width": 1280,
  "height": 720,
  "fps": 24,
  "seed": 42
}
```

## Check Generation Status

```bash
curl https://api.renderful.ai/v1/status/{task_id} \
  -H "Authorization: Bearer $RENDERFUL_API_KEY"
```

## Response Format

```json
{
  "task_id": "rf_abc123",
  "status": "completed",
  "url": "https://cdn.renderful.ai/generated/abc123.png",
  "expires_at": "2026-02-02T12:00:00Z"
}
```

## Pricing

Pay with USDC on Base, Polygon, or Solana. Check current rates at https://renderful.ai/pricing

## x402 Integration

Renderful supports x402 payments for agent autonomy:

```bash
# Agent can pay directly without human approval
export RENDERFUL_X402_WALLET="your_agent_wallet"
export RENDERFUL_PREFER_X402="true"
```

## Error Handling

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 402 | Payment required (x402 flow) |
| 429 | Rate limit |
| 500 | Generation failed |

## Examples

### Simple Image
```bash
curl -X POST https://api.renderful.ai/v1/generate \
  -H "Authorization: Bearer $RENDERFUL_API_KEY" \
  -d '{"model":"flux-dev","prompt":"a cute cat","width":512,"height":512}'
```

### Video with Specific Settings
```bash
curl -X POST https://api.renderful.ai/v1/generate \
  -H "Authorization: Bearer $RENDERFUL_API_KEY" \
  -d '{
    "model": "kling-1.6",
    "prompt": "underwater coral reef, fish swimming, sunlight rays",
    "duration": 5,
    "width": 1920,
    "height": 1080
  }'
```

## Tips

- Use detailed prompts for better results
- Include style descriptors ("cinematic", "photorealistic", "anime")
- Negative prompts help avoid unwanted elements
- Check status for video generation (takes 30-120s)