---
name: bria-ai
description: AI image generation, editing, and background removal API via Bria.ai — remove backgrounds to get transparent PNGs and cutouts, generate images from text prompts, and edit photos with natural language instructions. Also create product photography and lifestyle shots, replace or blur backgrounds, upscale resolution, restyle, and batch-generate visual assets. Use this skill whenever the user wants to remove a background, create transparent PNGs, generate, edit, modify, or transform any image — including hero images, banners, social media visuals, product photos, illustrations, icons, thumbnails, ad creatives, or marketing materials. Also triggers on cutout, inpainting, outpainting, object removal or addition, photo restoration, style transfer, image enhancement, relight, reseason, sketch-to-photo, or any visual content creation. Commercially safe, royalty-free. 20+ specialized endpoints for e-commerce, web design, and content pipelines.
license: MIT
metadata:
  author: Bria AI
  version: "1.2.7"
  dependencies:
    - type: env
      name: BRIA_API_KEY
      description: "Bria AI API key (get one at https://platform.bria.ai/console/account/api-keys)"
---

# Bria — AI Image Generation, Editing & Background Removal

Commercially safe, royalty-free image generation and editing through 20+ API endpoints. Generate from text, edit with natural language, remove backgrounds, create product shots, and build automated image pipelines.

## When to Use This Skill

Use this skill when the user wants to:
- **Generate images** — "create an image of...", "make me a banner", "generate a hero image", "I need a product photo"
- **Edit images** — "change the background", "make it look like winter", "add a vase to the table", "remove the person"
- **Remove/replace backgrounds** — "make the background transparent", "cut out the product", "replace with a studio background"
- **Product photography** — "create a lifestyle shot", "place this product in a kitchen scene", "e-commerce packshot"
- **Enhance/transform** — "upscale this image", "make it higher resolution", "restyle as oil painting", "change the lighting"
- **Batch/pipeline** — "generate 10 product images", "process all these images", "remove backgrounds in bulk"

This skill handles the full spectrum of AI image operations. If the user mentions images, photos, visuals, or any visual content creation — use this skill.

---

## What You Can Build

- **E-commerce product catalog** — Generate product photos, remove backgrounds for transparent PNGs, place products in lifestyle scenes (kitchen, office, outdoor), create packshots with consistent style
- **Landing page visuals** — Generate hero images, abstract tech backgrounds, team photos, and section illustrations — all matching your brand aesthetic
- **Social media content** — Instagram posts (1:1), Stories/Reels (9:16), LinkedIn banners (16:9), ad creatives — batch-generate variants for A/B testing
- **Marketing campaign assets** — Seasonal transformations (summer→winter), restyle product shots for different markets, create localized visuals at scale
- **Photo restoration pipeline** — Restore old damaged photos, colorize black & white images, upscale low-res photos to 4x, enhance quality automatically
- **Brand asset toolkit** — Remove backgrounds from logos, blend artwork onto products (t-shirts, mugs), create consistent product photography across your entire catalog
- **AI-powered design workflows** — Chain operations: generate→edit→remove background→place in scene→upscale — all automated through API pipelines

---

## Setup — API Key Check

Before making any Bria API call, check for the API key and help the user set it up if missing:

### Step 1: Check if the key exists (without printing the key)

```bash
if [ -z "$BRIA_API_KEY" ]; then
  echo "BRIA_API_KEY is not set"
else
  echo "BRIA_API_KEY is set"
fi
```

If the output says **BRIA_API_KEY is set**, skip to the next section.

### Step 2: If the key is missing, guide the user

Tell the user exactly this:
> To use image generation, you need a free Bria API key.
>
> 1. Go to https://platform.bria.ai/console/account/api-keys
> 2. Sign up or log in
> 3. Click **Create API Key**

Wait for the user to provide their API key. Do not proceed until they give you the key.

**Do not proceed with any image generation or editing until the API key is confirmed set.**

---

## Core Capabilities

| Need | Capability | Use Case |
|------|------------|----------|
| Generate images from text | FIBO Generate | Hero images, product shots, illustrations, social media images, banners |
| Edit images by text instruction | FIBO-Edit | Change colors, modify objects, transform scenes |
| Edit image region with mask | GenFill/Erase | Precise inpainting, add/replace specific regions |
| Add/Replace/Remove objects | Text-based editing | Add vase, replace apple with pear, remove table |
| Remove background (transparent PNG) | RMBG-2.0 | Extract subjects for overlays, logos, cutouts |
| Replace/blur/erase background | Background ops | Change, blur, or remove backgrounds |
| Expand/outpaint images | Outpainting | Extend boundaries, change aspect ratios |
| Upscale image resolution | Super Resolution | Increase resolution 2x or 4x |
| Enhance image quality | Enhancement | Improve lighting, colors, details |
| Restyle images | Restyle | Oil painting, anime, cartoon, 3D render |
| Change lighting | Relight | Golden hour, spotlight, dramatic lighting |
| Change season | Reseason | Spring, summer, autumn, winter |
| Composite/blend images | Image Blending | Apply textures, logos, merge images |
| Restore old photos | Restoration | Fix old/damaged photos |
| Colorize images | Colorization | Add color to B&W, or convert to B&W |
| Sketch to photo | Sketch2Image | Convert drawings to realistic photos |
| Create product lifestyle shots | Lifestyle Shot | Place products in scenes for e-commerce |
| Integrate products into scenes | Product Integrate | Embed products at exact coordinates |

## Quick Reference

### Generate an Image (FIBO)

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/generate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.7" \
  -d '{
    "prompt": "your description",
    "aspect_ratio": "16:9",
    "resolution": "1MP",
    "sync": true
  }'
```

**Aspect ratios**: `1:1` (square), `16:9` (hero/banner), `4:3` (presentation), `9:16` (mobile/story), `3:4` (portrait)

**Resolution**: `1MP` (default) or `4MP` (improved details for photorealism, adds ~30s latency)

**Sync mode**: Pass `"sync": true` in the request body for single image generation to get the result directly in the response. For batch/multiple image generation, omit `sync` (or set `false`) and use polling instead.

> **Advanced**: For precise, deterministic control over generation, use **[VGL structured prompts](../vgl/SKILL.md)** instead of natural language. VGL defines every visual attribute (objects, lighting, composition) as explicit JSON.

### Remove Background (RMBG-2.0)

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/remove_background" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.7" \
  -d '{"image": "https://..."}'
```

Returns PNG with transparency.

### Edit Image (FIBO-Edit) - No Mask Required

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.7" \
  -d '{
    "images": ["https://..."],
    "instruction": "change the mug to red"
  }'
```

### Edit Image Region with Mask (GenFill)

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/gen_fill" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.7" \
  -d '{
    "image": "https://...",
    "mask": "https://...",
    "prompt": "what to generate in masked area"
  }'
```

### Expand Image (Outpainting)

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/expand" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.7" \
  -d '{
    "image": "base64-or-url",
    "aspect_ratio": "16:9",
    "prompt": "coffee shop background, wooden table"
  }'
```

### Upscale Image

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/increase_resolution" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.7" \
  -d '{"image": "https://...", "scale": 2}'
```

### Create Product Lifestyle Shot

```bash
curl -X POST "https://engine.prod.bria-api.com/v1/product/lifestyle_shot_by_text" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.7" \
  -d '{
    "image": "https://product-with-transparent-bg.png",
    "prompt": "modern kitchen countertop, natural morning light"
  }'
```

### Integrate Products into Scene

Place one or more products at exact coordinates in a scene. Products are automatically cut out and matched to the scene's lighting and perspective.

```bash
curl -X POST "https://engine.prod.bria-api.com/image/edit/product/integrate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: BriaSkills/1.2.7" \
  -d '{
    "scene": "https://scene-image-url",
    "products": [
      {
        "image": "https://product-image-url",
        "coordinates": {"x": 100, "y": 200, "width": 300, "height": 400}
      }
    ]
  }'
```

---

## Response Handling

### Sync (single image generation)

For single image requests, pass `"sync": true` in the request body. The response returns the result directly — no polling needed.

### Async with polling (batch generation)

For batch or multiple image generation, omit `sync` (or set `"sync": false`). The response returns a status URL to poll:

```json
{
  "request_id": "uuid",
  "status_url": "https://engine.prod.bria-api.com/v2/status/uuid"
}
```

Poll the status_url until `status: "COMPLETED"`, then get `result.image_url`.

```python
import requests, time

def get_result(status_url, api_key):
    while True:
        r = requests.get(status_url, headers={"api_token": api_key, "User-Agent": "BriaSkills/1.2.7"})
        data = r.json()
        if data["status"] == "COMPLETED":
            return data["result"]["image_url"]
        if data["status"] == "FAILED":
            raise Exception(data.get("error"))
        time.sleep(2)
```

---

## Prompt Engineering Tips

- **Style**: "professional product photography" vs "casual snapshot", "flat design illustration" vs "3D rendered"
- **Lighting**: "soft natural light", "studio lighting", "dramatic shadows"
- **Background**: "white studio", "gradient", "blurred office", "transparent"
- **Composition**: "centered", "rule of thirds", "negative space on left for text"
- **Quality keywords**: "high quality", "professional", "commercial grade", "4K", "sharp focus"
- **Negative prompts**: "blurry, low quality, pixelated", "text, watermark, logo"

---

## API Reference

See `references/api-endpoints.md` for complete endpoint documentation with request/response formats for all 20+ endpoints.

### Authentication

All requests need these headers:
```
api_token: YOUR_BRIA_API_KEY
Content-Type: application/json
User-Agent: BriaSkills/1.2.7
```

---

## Additional Resources

- **[API Endpoints Reference](references/api-endpoints.md)** — Complete endpoint documentation with request/response formats
- **[Workflows & Pipelines](references/workflows.md)** — Batch generation, parallel pipelines, integration examples
- **[Python Client](references/code-examples/bria_client.py)** — Full-featured async Python client
- **[TypeScript Client](references/code-examples/bria_client.ts)** — Typed Node.js client
- **[Bash/curl Reference](references/code-examples/bria_client.sh)** — Shell functions for all endpoints

## Related Skills

- **[vgl](../vgl/SKILL.md)** — Write structured VGL JSON prompts for precise, deterministic control over FIBO image generation
- **[image-utils](../image-utils/SKILL.md)** — Classic image manipulation (resize, crop, composite, watermarks) for post-processing
