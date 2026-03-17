---
name: bria-ai
description: Controllable image generation and editing with Bria.ai commercially-safe AI models. Fine-grained control over what gets generated, edited, or removed — edit by text instruction, mask specific regions, add/replace/remove individual objects, control lighting, season, and style independently. Use this skill when building websites, apps, presentations, or documents that need product photos, hero images, icons, illustrations, or backgrounds. Also use for e-commerce product photography, background removal, image upscaling, style transfer, batch generation, and pipeline workflows (generate -> edit -> remove background). Triggers on tasks involving AI image generation, controllable image editing, background removal, or visual asset creation.
license: MIT
metadata:
  author: Bria AI
  version: "1.2.1"
---

# Bria — Controllable Image Generation & Editing

Generate and precisely control visual assets using Bria's commercially-safe AI models (FIBO, RMBG-2.0, GenFill, and more). Unlike black-box generators, Bria gives you fine-grained control: edit by text instruction, mask specific regions, add/replace/remove individual objects, change lighting or season independently, and chain operations in pipelines.

## Setup — API Key Check

Before making any Bria API call, check for the API key and help the user set it up if missing:

### Step 1: Check if the key exists

```bash
echo $BRIA_API_KEY
```

If the output is **not empty**, skip to the next section.

### Step 2: If the key is missing, guide the user

Open the Bria API keys page in the browser:

```bash
open "https://platform.bria.ai/console/account/api-keys?utm_source=skill&utm_campaign=bria_skills&utm_content=adjust_photoshop_for_agent"   # macOS
# xdg-open "https://platform.bria.ai/console/account/api-keys?utm_source=skill&utm_campaign=bria_skills&utm_content=adjust_photoshop_for_agent"  # Linux
```

Then tell the user exactly this:
> I opened the Bria website in your browser. To use image generation, you need a free API key.
>
> 1. Sign up or log in on the page I just opened
> 2. Click **Create API Key**
> 3. Copy the key and **paste it here**

Wait for the user to provide their API key. Do not proceed until they give you the key.

### Step 3: Save the key permanently

Once the user provides the key, save it so it persists across sessions.

**On macOS/Linux**, detect the shell and append to the correct profile:

```bash
# Detect the shell profile
if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = */zsh ]; then
  PROFILE_FILE="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
  PROFILE_FILE="$HOME/.bashrc"
else
  PROFILE_FILE="$HOME/.profile"
fi

# Append the export (only if not already present)
grep -q 'export BRIA_API_KEY=' "$PROFILE_FILE" 2>/dev/null && \
  sed -i.bak '/export BRIA_API_KEY=/d' "$PROFILE_FILE"
echo 'export BRIA_API_KEY="THE_KEY_THE_USER_GAVE_YOU"' >> "$PROFILE_FILE"

# Make it available immediately in this session
export BRIA_API_KEY="THE_KEY_THE_USER_GAVE_YOU"
```

**On Windows (PowerShell)**:

```powershell
[System.Environment]::SetEnvironmentVariable("BRIA_API_KEY", "THE_KEY_THE_USER_GAVE_YOU", "User")
$env:BRIA_API_KEY = "THE_KEY_THE_USER_GAVE_YOU"
```

Replace `THE_KEY_THE_USER_GAVE_YOU` with the actual key the user provided.

### Step 4: Verify

```bash
echo $BRIA_API_KEY
```

Confirm the key is set, then tell the user:
> Your API key is saved and will persist across sessions. You're all set!

**Do not proceed with any image generation or editing until the API key is confirmed set.**

---

## Core Capabilities

| Need | Capability | Use Case |
|------|------------|----------|
| Create new images | FIBO Generate | Hero images, product shots, illustrations |
| Edit by text | FIBO-Edit | Change colors, modify objects, transform scenes |
| Edit with mask | GenFill/Erase | Precise inpainting, add/replace specific regions |
| Add/Replace/Remove objects | Text-based editing | Add vase, replace apple with pear, remove table |
| Transparent backgrounds | RMBG-2.0 | Extract subjects for overlays, logos, cutouts |
| Background operations | Replace/Blur/Erase | Change, blur, or remove backgrounds |
| Expand images | Outpainting | Extend boundaries, change aspect ratios |
| Upscale images | Super Resolution | Increase resolution 2x or 4x |
| Enhance quality | Enhancement | Improve lighting, colors, details |
| Transform style | Restyle | Oil painting, anime, cartoon, 3D render |
| Change lighting | Relight | Golden hour, spotlight, dramatic lighting |
| Change season | Reseason | Spring, summer, autumn, winter |
| Blend/composite | Image Blending | Apply textures, logos, merge images |
| Restore photos | Restoration | Fix old/damaged photos |
| Colorize | Colorization | Add color to B&W, or convert to B&W |
| Sketch to photo | Sketch2Image | Convert drawings to realistic photos |
| Product photography | Lifestyle Shot | Place products in scenes |
| Product integration | Product Integrate | Embed products into scenes at exact coordinates |

## Quick Reference

### Generate an Image (FIBO)

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/generate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "your description",
    "aspect_ratio": "16:9",
    "resolution": "1MP"
  }'
```

**Aspect ratios**: `1:1` (square), `16:9` (hero/banner), `4:3` (presentation), `9:16` (mobile/story), `3:4` (portrait)

**Resolution**: `1MP` (default) or `4MP` (improved details for photorealism, adds ~30s latency)

> **Advanced**: For precise, deterministic control over generation, use **[VGL structured prompts](../vgl/SKILL.md)** instead of natural language. VGL defines every visual attribute (objects, lighting, composition) as explicit JSON.

### Remove Background (RMBG-2.0)

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit/remove_background" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image": "https://..."}'
```

Returns PNG with transparency.

### Edit Image (FIBO-Edit) - No Mask Required

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/edit" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
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
  -d '{"image": "https://...", "scale": 2}'
```

### Product Lifestyle Shot

```bash
curl -X POST "https://engine.prod.bria-api.com/v1/product/lifestyle_shot_by_text" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
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

## Async Response Handling

All endpoints return async responses:

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
        r = requests.get(status_url, headers={"api_token": api_key})
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

See `references/api-endpoints.md` for complete endpoint documentation.

### Key Endpoints

**Generation**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/generate` | Generate images from text (FIBO) |

**Edit by Text (No Mask)**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit` | Edit image with natural language instruction |
| `POST /v2/image/edit/add_object_by_text` | Add objects to image |
| `POST /v2/image/edit/replace_object_by_text` | Replace objects in image |
| `POST /v2/image/edit/erase_by_text` | Remove objects by name |

**Edit with Mask**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/gen_fill` | Inpaint/generate in masked region |
| `POST /v2/image/edit/erase` | Erase masked region |

**Background Operations**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/remove_background` | Remove background (RMBG-2.0) |
| `POST /v2/image/edit/replace_background` | Replace with AI-generated background |
| `POST /v2/image/edit/blur_background` | Apply blur to background |
| `POST /v2/image/edit/erase_foreground` | Remove foreground, fill background |
| `POST /v2/image/edit/crop_foreground` | Crop tightly around subject |

**Image Transformation**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/expand` | Outpaint to new aspect ratio |
| `POST /v2/image/edit/enhance` | Enhance quality and details |
| `POST /v2/image/edit/increase_resolution` | Upscale 2x or 4x |
| `POST /v2/image/edit/blend` | Blend/merge images or textures |
| `POST /v2/image/edit/reseason` | Change season/weather |
| `POST /v2/image/edit/restyle` | Transform artistic style |
| `POST /v2/image/edit/relight` | Modify lighting |

**Restoration**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/image/edit/sketch_to_colored_image` | Convert sketch to photo |
| `POST /v2/image/edit/restore` | Restore old/damaged photos |
| `POST /v2/image/edit/colorize` | Colorize B&W or convert to B&W |

**Product Photography**
| Endpoint | Purpose |
|----------|---------|
| `POST /v1/product/lifestyle_shot_by_text` | Place product in scene by text |
| `POST /image/edit/product/integrate` | Integrate products into scene at exact coordinates |

**Utilities**
| Endpoint | Purpose |
|----------|---------|
| `POST /v2/structured_instruction/generate` | Generate JSON instruction (no image) |
| `GET /v2/status/{id}` | Check async request status |

### Authentication

All requests need `api_token` header:
```
api_token: YOUR_BRIA_API_KEY
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
