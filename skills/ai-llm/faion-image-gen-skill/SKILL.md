---
name: faion-image-gen-skill
user-invocable: false
description: ""
---

# AI Image Generation Mastery

**Complete Guide to Text-to-Image, Image Editing, and Prompt Engineering (2025-2026)**

---

## Quick Reference

| Model | Best For | Text in Images | Control Level | API | Cost |
|-------|----------|----------------|---------------|-----|------|
| **DALL-E 3** | Text rendering, commercial | Excellent | Medium | OpenAI | $0.04-0.12/image |
| **Midjourney v6.1** | Artistic, aesthetic | Good | Medium | Discord/API | $10-60/month |
| **FLUX.1 Pro** | Photorealism | Good | High | Replicate/fal.ai | $0.03-0.05/image |
| **SD 3.5 Large** | Maximum control, local | Moderate | Excellent | Self-hosted | Free (GPU costs) |
| **Ideogram 2.0** | Text in images, logos | Excellent | Medium | API | $0.02-0.08/image |

---

## Model Comparison

### Feature Matrix

| Feature | DALL-E 3 | Midjourney | FLUX.1 Pro | SD 3.5 | Ideogram 2 |
|---------|----------|------------|------------|--------|------------|
| Text Rendering | Excellent | Good | Good | Moderate | Excellent |
| Photorealism | Good | Good | Excellent | Good | Good |
| Artistic Styles | Good | Excellent | Good | Excellent | Good |
| ControlNet | No | No | Yes | Yes | No |
| Inpainting | DALL-E 2 | Yes | Yes | Yes | Yes |
| Outpainting | DALL-E 2 | Yes | Yes | Yes | Yes |
| API Access | OpenAI | Official API | Replicate | Local/API | Official |
| Self-hosting | No | No | Yes (Dev) | Yes | No |
| Commercial Use | Yes | Yes | Check license | Check model | Yes |

### When to Use Each

| Use Case | Recommended Model |
|----------|-------------------|
| Text/typography in images | DALL-E 3, Ideogram 2 |
| Photorealistic portraits | FLUX.1 Pro |
| Artistic/stylized images | Midjourney v6.1 |
| Product photography | FLUX.1 Pro, DALL-E 3 |
| Maximum control/customization | Stable Diffusion 3.5 |
| Logo design | Ideogram 2, DALL-E 3 |
| Consistent characters | Midjourney (--cref), SD + LoRA |
| Quick iterations | FLUX.1 Schnell |
| Budget-conscious | SD 3.5 (self-hosted), Ideogram |

---

## DALL-E 3 (OpenAI)

### Overview

OpenAI's flagship image generation model. Best-in-class for text rendering and commercial-safe content.

**Key Strengths:**
- Excellent text rendering in images
- Strong prompt following
- Built-in safety filters
- Automatic prompt enhancement (revised_prompt)

### API Usage

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

# Basic generation
response = client.images.generate(
    model="dall-e-3",
    prompt="A minimalist logo for 'Faion Network' featuring an abstract neural network pattern in deep blue and silver, white background, vector style",
    size="1024x1024",      # "1024x1024" | "1792x1024" | "1024x1792"
    quality="hd",          # "standard" | "hd"
    style="vivid",         # "vivid" | "natural"
    n=1                    # DALL-E 3 supports only n=1
)

image_url = response.data[0].url
revised_prompt = response.data[0].revised_prompt  # What DALL-E actually used
```

### Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| `model` | `dall-e-3`, `dall-e-2` | Model version |
| `size` | 1024x1024, 1792x1024, 1024x1792 | Output resolution |
| `quality` | `standard`, `hd` | Image quality (hd = more detail) |
| `style` | `vivid`, `natural` | Vivid = dramatic, Natural = realistic |
| `response_format` | `url`, `b64_json` | URL expires in 1 hour |
| `n` | 1 (DALL-E 3), 1-10 (DALL-E 2) | Number of images |

### Response Formats

```python
# URL response (default) - expires in 1 hour
response = client.images.generate(
    model="dall-e-3",
    prompt="...",
    response_format="url"
)
url = response.data[0].url

# Base64 response - for immediate use/storage
response = client.images.generate(
    model="dall-e-3",
    prompt="...",
    response_format="b64_json"
)
import base64
image_bytes = base64.b64decode(response.data[0].b64_json)
with open("image.png", "wb") as f:
    f.write(image_bytes)
```

### Image Editing (DALL-E 2 only)

```python
# Inpainting - edit specific regions
response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),  # Transparent areas will be regenerated
    prompt="Add a red sports car in the parking lot",
    size="1024x1024",
    n=1
)

# Variations - create similar images
response = client.images.create_variation(
    model="dall-e-2",
    image=open("source.png", "rb"),
    size="1024x1024",
    n=3
)
```

### Pricing (2025-2026)

| Model | Quality | Size | Price per Image |
|-------|---------|------|-----------------|
| **DALL-E 3** | HD | 1024x1024 | $0.080 |
| **DALL-E 3** | HD | 1792x1024, 1024x1792 | $0.120 |
| **DALL-E 3** | Standard | 1024x1024 | $0.040 |
| **DALL-E 3** | Standard | 1792x1024, 1024x1792 | $0.080 |
| **DALL-E 2** | - | 1024x1024 | $0.020 |
| **DALL-E 2** | - | 512x512 | $0.018 |
| **DALL-E 2** | - | 256x256 | $0.016 |

### curl Example

```bash
source ~/.secrets/openai

curl https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A futuristic AI network visualization, dark blue background with glowing neural connections",
    "n": 1,
    "size": "1024x1024",
    "quality": "hd",
    "style": "vivid"
  }'
```

### Best Practices

1. **Be specific** - More detail = better results
2. **Use revised_prompt** - Check what DALL-E actually generated
3. **Natural style for realism** - Use `style: "natural"` for photos
4. **HD for detail** - Worth the extra cost for final assets
5. **Download immediately** - URLs expire in 1 hour

---

## Midjourney

### Overview

Industry-leading aesthetic quality. Best for artistic, stylized images. Recently launched official API.

**Key Strengths:**
- Exceptional aesthetic quality
- Strong community and style ecosystem
- Character reference (--cref) for consistency
- Style reference (--sref) for consistent aesthetics

### API Access

Midjourney now offers an official API (beta). Previously Discord-only.

```python
import requests
import time

MIDJOURNEY_API_KEY = "your-api-key"
BASE_URL = "https://api.midjourney.com/v1"

headers = {
    "Authorization": f"Bearer {MIDJOURNEY_API_KEY}",
    "Content-Type": "application/json"
}

# Submit generation request
response = requests.post(
    f"{BASE_URL}/imagine",
    headers=headers,
    json={
        "prompt": "portrait of a cyberpunk hacker, neon lights, cinematic --ar 16:9 --style raw --v 6.1",
        "webhook_url": "https://your-webhook.com/callback"  # Optional
    }
)

task_id = response.json()["task_id"]

# Poll for completion
while True:
    status = requests.get(
        f"{BASE_URL}/tasks/{task_id}",
        headers=headers
    ).json()

    if status["status"] == "completed":
        image_urls = status["images"]
        break
    elif status["status"] == "failed":
        raise Exception(f"Generation failed: {status['error']}")

    time.sleep(5)

# Upscale a specific image (U1, U2, U3, U4)
upscale_response = requests.post(
    f"{BASE_URL}/upscale",
    headers=headers,
    json={
        "task_id": task_id,
        "index": 1  # U1
    }
)
```

### Discord Bot Usage

For those without API access:

```
/imagine prompt: portrait of a scientist, dramatic lighting, oil painting style --ar 3:4 --v 6.1

Buttons:
U1-U4: Upscale individual images
V1-V4: Create variations
Re-roll: Generate new images
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--ar` | Aspect ratio | `--ar 16:9`, `--ar 3:4` |
| `--v` | Model version | `--v 6.1` |
| `--style` | Style preset | `--style raw` (less stylized) |
| `--chaos` | Variation (0-100) | `--chaos 50` |
| `--stylize` | Artistic influence (0-1000) | `--stylize 750` |
| `--no` | Negative prompt | `--no blur, watermark` |
| `--cref` | Character reference | `--cref [image_url]` |
| `--sref` | Style reference | `--sref [image_url]` |
| `--cw` | Character weight (0-100) | `--cw 50` |
| `--sw` | Style weight (0-1000) | `--sw 500` |
| `--tile` | Seamless patterns | `--tile` |
| `--seed` | Reproducibility | `--seed 12345` |
| `--q` | Quality (0.25, 0.5, 1) | `--q 1` |
| `--repeat` | Multiple generations | `--repeat 4` |

### Character Consistency (--cref)

```
/imagine portrait of a woman with red hair, business attire --cref https://example.com/character.jpg --cw 100

--cw values:
0: Only face
50: Face + some style
100: Full character reference
```

### Style Reference (--sref)

```
/imagine mountain landscape at sunset --sref https://example.com/style.jpg --sw 500

--sw values:
0-100: Subtle influence
100-500: Moderate influence
500-1000: Strong influence
```

### Pricing

| Plan | Monthly Cost | Fast Hours | Relax Mode |
|------|-------------|------------|------------|
| Basic | $10 | 3.3 hours | No |
| Standard | $30 | 15 hours | Yes |
| Pro | $60 | 30 hours | Yes |
| Mega | $120 | 60 hours | Yes |

---

## FLUX (Black Forest Labs)

### Overview

Open-source photorealistic image generation. Three variants for different use cases.

**Models:**
- **FLUX.1 Pro**: Highest quality, API only
- **FLUX.1 Dev**: Open-source, non-commercial
- **FLUX.1 Schnell**: Fast, 4 steps, Apache 2.0 license

### FLUX.1 Pro via Replicate

```python
import replicate

# FLUX.1 Pro - best quality
output = replicate.run(
    "black-forest-labs/flux-1.1-pro",
    input={
        "prompt": "Professional headshot of a CEO, studio lighting, neutral background, sharp focus",
        "aspect_ratio": "1:1",
        "output_format": "webp",
        "output_quality": 90,
        "safety_tolerance": 2,
        "prompt_upsampling": True
    }
)

image_url = output
print(f"Generated: {image_url}")
```

### FLUX.1 Dev via Replicate

```python
# FLUX.1 Dev - open weights, good quality
output = replicate.run(
    "black-forest-labs/flux-dev",
    input={
        "prompt": "Serene Japanese garden with cherry blossoms, koi pond, photorealistic",
        "guidance": 3.5,
        "num_inference_steps": 50,
        "aspect_ratio": "16:9",
        "output_format": "png"
    }
)
```

### FLUX.1 Schnell - Fast Generation

```python
# FLUX.1 Schnell - 4 steps, fastest
output = replicate.run(
    "black-forest-labs/flux-schnell",
    input={
        "prompt": "A golden retriever playing in autumn leaves",
        "num_inference_steps": 4,
        "aspect_ratio": "1:1"
    }
)
```

### FLUX via fal.ai

```python
import fal_client

# Text-to-Image
result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1",
    arguments={
        "prompt": "Minimalist product shot of wireless earbuds on marble surface",
        "image_size": "landscape_16_9",
        "num_images": 1,
        "enable_safety_checker": True
    }
)

image_url = result["images"][0]["url"]

# Image-to-Image with FLUX
result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1/redux",
    arguments={
        "image_url": "https://example.com/source.jpg",
        "prompt": "Same scene but at sunset with warm golden lighting",
        "strength": 0.7
    }
)
```

### ControlNet with FLUX

```python
# FLUX with Canny edge control
result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1/canny",
    arguments={
        "image_url": "https://example.com/pose_reference.jpg",
        "prompt": "Fashion model in designer outfit, studio photography",
        "control_strength": 0.8
    }
)

# FLUX with Depth control
result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1/depth",
    arguments={
        "image_url": "https://example.com/scene.jpg",
        "prompt": "Same composition but in watercolor painting style",
        "control_strength": 0.7
    }
)
```

### Pricing (API Providers)

| Provider | FLUX Pro | FLUX Dev | FLUX Schnell |
|----------|----------|----------|--------------|
| Replicate | ~$0.03-0.05/image | ~$0.02/image | ~$0.003/image |
| fal.ai | ~$0.03-0.05/image | ~$0.02/image | ~$0.003/image |
| BFL API | ~$0.04/image | - | - |

---

## Stable Diffusion 3.5

### Overview

Open-weights model offering maximum control. Best for local deployment and custom workflows.

**Variants:**
- **SD 3.5 Large**: 8B parameters, highest quality
- **SD 3.5 Large Turbo**: 8B, distilled for speed
- **SD 3.5 Medium**: 2.5B parameters, balanced

### Local Installation

```bash
# Using ComfyUI (recommended)
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
pip install -r requirements.txt

# Download SD 3.5 Large model
# Place in ComfyUI/models/checkpoints/
# Get from huggingface.co/stabilityai/stable-diffusion-3.5-large

# Run ComfyUI
python main.py
```

### Python with diffusers

```python
from diffusers import StableDiffusion3Pipeline
import torch

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large",
    torch_dtype=torch.float16
)
pipe.to("cuda")

# Basic generation
image = pipe(
    prompt="A majestic lion in the savanna at golden hour, photorealistic, 8K",
    negative_prompt="blurry, low quality, distorted",
    num_inference_steps=28,
    guidance_scale=4.5,
    height=1024,
    width=1024
).images[0]

image.save("lion.png")
```

### ControlNet with SD 3.5

```python
from diffusers import StableDiffusion3ControlNetPipeline, SD3ControlNetModel
from diffusers.utils import load_image
import torch

# Load ControlNet model
controlnet = SD3ControlNetModel.from_pretrained(
    "stabilityai/stable-diffusion-3.5-controlnet-canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusion3ControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large",
    controlnet=controlnet,
    torch_dtype=torch.float16
)
pipe.to("cuda")

# Load control image
control_image = load_image("https://example.com/canny_edges.png")

# Generate with control
image = pipe(
    prompt="Modern architecture building, glass and steel, sunny day",
    control_image=control_image,
    controlnet_conditioning_scale=0.8,
    num_inference_steps=28
).images[0]
```

### LoRA Fine-tuning

```python
# Load base model with LoRA
from diffusers import StableDiffusion3Pipeline
import torch

pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large",
    torch_dtype=torch.float16
)

# Load custom LoRA
pipe.load_lora_weights("path/to/custom_style.safetensors")
pipe.to("cuda")

# Generate with LoRA style
image = pipe(
    prompt="portrait of a person in custom_style",
    num_inference_steps=28
).images[0]
```

### ComfyUI Workflow Export

```json
{
  "workflow": {
    "nodes": [
      {
        "id": 1,
        "type": "CheckpointLoaderSimple",
        "inputs": {"ckpt_name": "sd3.5_large.safetensors"}
      },
      {
        "id": 2,
        "type": "CLIPTextEncode",
        "inputs": {"text": "beautiful landscape, mountains, sunset"}
      },
      {
        "id": 3,
        "type": "KSampler",
        "inputs": {
          "seed": 42,
          "steps": 28,
          "cfg": 4.5,
          "sampler_name": "euler",
          "scheduler": "normal"
        }
      },
      {
        "id": 4,
        "type": "VAEDecode",
        "inputs": {}
      },
      {
        "id": 5,
        "type": "SaveImage",
        "inputs": {"filename_prefix": "output"}
      }
    ]
  }
}
```

### Hardware Requirements

| Model | VRAM Required | Recommended GPU |
|-------|---------------|-----------------|
| SD 3.5 Large | 24GB+ | RTX 4090, A100 |
| SD 3.5 Large (fp8) | 12GB | RTX 4080, RTX 3090 |
| SD 3.5 Medium | 8GB | RTX 4070, RTX 3080 |
| SD 3.5 Large Turbo | 16GB | RTX 4080 |

---

## Ideogram 2.0

### Overview

Specialized for text rendering in images. Excellent for logos, posters, and graphics with text.

**Key Strengths:**
- Best-in-class text rendering
- Good for logos and branding
- Clean, commercial-ready output

### API Usage

```python
import requests

IDEOGRAM_API_KEY = "your-api-key"

response = requests.post(
    "https://api.ideogram.ai/generate",
    headers={
        "Api-Key": IDEOGRAM_API_KEY,
        "Content-Type": "application/json"
    },
    json={
        "image_request": {
            "prompt": "A modern tech startup logo with the text 'FAION' in bold geometric font, blue and silver gradient, white background, vector style",
            "aspect_ratio": "ASPECT_1_1",
            "model": "V_2",
            "magic_prompt_option": "AUTO",
            "style_type": "DESIGN"
        }
    }
)

result = response.json()
image_url = result["data"][0]["url"]
```

### Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| `model` | `V_2`, `V_2_TURBO` | Model version |
| `aspect_ratio` | `ASPECT_1_1`, `ASPECT_16_9`, `ASPECT_9_16`, etc. | Output ratio |
| `style_type` | `GENERAL`, `REALISTIC`, `DESIGN`, `RENDER_3D`, `ANIME` | Style preset |
| `magic_prompt_option` | `AUTO`, `ON`, `OFF` | Prompt enhancement |
| `seed` | Integer | Reproducibility |
| `negative_prompt` | String | What to avoid |

### Style Types

| Style | Best For |
|-------|----------|
| `GENERAL` | Mixed content |
| `REALISTIC` | Photos, product shots |
| `DESIGN` | Logos, graphics, flat design |
| `RENDER_3D` | 3D renders, product visualization |
| `ANIME` | Anime/manga style |

### Pricing

| Plan | Images/Month | Cost |
|------|--------------|------|
| Free | 100 | $0 |
| Basic | 400 | $7/month |
| Plus | 1000 | $16/month |
| Pro | 3000 | $48/month |

API pricing: ~$0.02-0.08 per image depending on model and resolution.

---

## Prompt Engineering for Images

### Prompt Structure

```
[Subject] + [Setting/Environment] + [Style] + [Lighting] + [Composition] + [Technical]
```

**Example:**
```
A professional businesswoman | in a modern glass office | corporate photography style |
soft natural window light | medium shot, shallow depth of field | 8K, sharp focus
```

### Subject Keywords

| Category | Keywords |
|----------|----------|
| **People** | portrait, headshot, full body, group, candid |
| **Objects** | product shot, floating, isolated, arrangement |
| **Animals** | wildlife, pet portrait, action shot |
| **Landscapes** | panoramic, aerial view, close-up detail |
| **Abstract** | patterns, textures, geometric shapes |

### Style Keywords

| Style | Keywords |
|-------|----------|
| **Photorealistic** | photorealistic, hyperrealistic, RAW photo, 8K UHD |
| **Artistic** | oil painting, watercolor, digital art, illustration |
| **Commercial** | product photography, advertising, editorial |
| **Cinematic** | cinematic, movie still, film grain, anamorphic |
| **Minimalist** | minimalist, clean, simple, white space |
| **Vintage** | retro, vintage, film photography, polaroid |
| **3D** | 3D render, CGI, octane render, unreal engine |

### Lighting Keywords

| Lighting | Effect |
|----------|--------|
| **Natural** | golden hour, blue hour, overcast, harsh sunlight |
| **Studio** | softbox, rim light, key light, fill light |
| **Dramatic** | chiaroscuro, low-key, high contrast, silhouette |
| **Ambient** | neon glow, bioluminescent, candlelight, moonlight |
| **Technical** | backlit, side-lit, front-lit, diffused |

### Composition Keywords

| Composition | Description |
|-------------|-------------|
| **Framing** | close-up, medium shot, wide shot, extreme close-up |
| **Angle** | eye level, bird's eye, worm's eye, Dutch angle |
| **Rule of thirds** | subject positioned at intersection points |
| **Symmetry** | balanced, mirrored, centered |
| **Depth** | shallow DOF, bokeh, layered, foreground interest |

### Technical Quality Keywords

```
High quality: 8K, UHD, high resolution, sharp focus, detailed
Camera: shot on Sony A7R IV, Canon EOS R5, Hasselblad
Lens: 85mm f/1.4, 35mm wide angle, macro lens
Post-processing: color graded, professionally retouched
```

### Negative Prompts

Common elements to exclude:

```
blurry, low quality, distorted, deformed, ugly, duplicate,
watermark, text, signature, cropped, out of frame,
extra limbs, bad anatomy, bad proportions, gross proportions,
mutation, disfigured, poorly drawn, jpeg artifacts
```

### Model-Specific Tips

**DALL-E 3:**
- Natural language works best
- System adds detail automatically
- Check `revised_prompt` to understand changes
- Use "natural" style for realism

**Midjourney:**
- Use `--style raw` for less stylization
- Stack style references with `--sref`
- Lower `--stylize` for more prompt adherence
- Separate concepts with `::`

**FLUX:**
- More literal prompt following
- Good with technical photography terms
- Supports longer prompts well
- Use `prompt_upsampling` for enhancement

**Stable Diffusion:**
- Use LoRAs for consistent styles
- CFG scale 4-7 for SD 3.5
- Negative prompts are important
- ComfyUI for complex workflows

---

## Image-to-Image

### Style Transfer

Transform existing images while preserving structure.

```python
# FLUX Redux for style transfer
import fal_client

result = fal_client.subscribe(
    "fal-ai/flux-pro/v1.1/redux",
    arguments={
        "image_url": "https://example.com/photo.jpg",
        "prompt": "Same scene in impressionist painting style, vibrant colors",
        "strength": 0.6  # 0.3-0.8 typical range
    }
)

# Stable Diffusion img2img
from diffusers import StableDiffusion3Img2ImgPipeline
from diffusers.utils import load_image

pipe = StableDiffusion3Img2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large",
    torch_dtype=torch.float16
)
pipe.to("cuda")

init_image = load_image("photo.png").resize((1024, 1024))

image = pipe(
    prompt="oil painting style, impressionist brush strokes",
    image=init_image,
    strength=0.7,  # How much to change (0-1)
    num_inference_steps=28
).images[0]
```

### Strength Parameter

| Strength | Effect |
|----------|--------|
| 0.3-0.4 | Subtle changes, preserve most details |
| 0.5-0.6 | Moderate transformation |
| 0.7-0.8 | Significant changes, keep composition |
| 0.9+ | Almost complete regeneration |

### Upscaling

```python
# Using Real-ESRGAN via Replicate
import replicate

output = replicate.run(
    "nightmareai/real-esrgan:350d32041630ffbe63c8352783a26d94126809164e54085352f8571e3d4edd3b",
    input={
        "image": open("low_res.png", "rb"),
        "scale": 4,  # 2x or 4x
        "face_enhance": True
    }
)

# Using FLUX for creative upscaling
output = replicate.run(
    "black-forest-labs/flux-1.1-pro-ultra",
    input={
        "image": open("source.png", "rb"),
        "prompt": "enhance details, sharp focus, 4K resolution",
        "aspect_ratio": "1:1",
        "output_quality": 100
    }
)
```

### Background Removal

```python
# Using remove.bg API
import requests

response = requests.post(
    "https://api.remove.bg/v1.0/removebg",
    files={"image_file": open("photo.png", "rb")},
    data={"size": "auto"},
    headers={"X-Api-Key": "YOUR_API_KEY"}
)

with open("no_bg.png", "wb") as f:
    f.write(response.content)

# Using Replicate
output = replicate.run(
    "lucataco/remove-bg:95fcc2a26d3899cd6c2691c900465aaeff466285a65c14638cc5f36f34befaf1",
    input={"image": open("photo.png", "rb")}
)
```

---

## Inpainting and Outpainting

### Inpainting (Edit Regions)

Edit specific parts of an image while keeping the rest.

```python
# DALL-E 2 Inpainting
from openai import OpenAI
client = OpenAI()

response = client.images.edit(
    model="dall-e-2",
    image=open("scene.png", "rb"),
    mask=open("mask.png", "rb"),  # White = keep, Transparent = edit
    prompt="A golden retriever sitting on the grass",
    size="1024x1024"
)

# Stable Diffusion Inpainting
from diffusers import StableDiffusionInpaintPipeline
from diffusers.utils import load_image

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-inpainting",
    torch_dtype=torch.float16
)
pipe.to("cuda")

init_image = load_image("scene.png").resize((512, 512))
mask_image = load_image("mask.png").resize((512, 512))

image = pipe(
    prompt="a beautiful flower garden",
    image=init_image,
    mask_image=mask_image,
    num_inference_steps=50
).images[0]
```

### Creating Masks

```python
# Automatic mask with Segment Anything
from segment_anything import SamPredictor, sam_model_registry
import numpy as np
from PIL import Image

sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h.pth")
predictor = SamPredictor(sam)

image = np.array(Image.open("photo.png"))
predictor.set_image(image)

# Point-based segmentation
masks, scores, _ = predictor.predict(
    point_coords=np.array([[500, 300]]),  # Click point
    point_labels=np.array([1]),  # 1 = foreground
    multimask_output=True
)

# Save best mask
best_mask = masks[np.argmax(scores)]
mask_image = Image.fromarray((best_mask * 255).astype(np.uint8))
mask_image.save("mask.png")
```

### Outpainting (Expand Canvas)

```python
# DALL-E 2 Outpainting
from PIL import Image
import numpy as np

# Create expanded canvas with transparent edges
original = Image.open("original.png")
expanded = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))

# Center original in expanded canvas
x_offset = (1024 - original.width) // 2
y_offset = (1024 - original.height) // 2
expanded.paste(original, (x_offset, y_offset))

# Create mask (white = keep, transparent = generate)
mask = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
mask.paste(Image.new("RGB", original.size, (255, 255, 255)), (x_offset, y_offset))

# Save for API
expanded.save("expanded.png")
mask.save("outpaint_mask.png")

# Use with DALL-E 2 edit endpoint
response = client.images.edit(
    model="dall-e-2",
    image=open("expanded.png", "rb"),
    mask=open("outpaint_mask.png", "rb"),
    prompt="continuation of the landscape scene, same style",
    size="1024x1024"
)
```

---

## Cost Comparison

### Per-Image Cost

| Model | Low Quality | Standard | High Quality |
|-------|-------------|----------|--------------|
| **DALL-E 3** | $0.040 | $0.040 | $0.080-0.120 |
| **DALL-E 2** | $0.016 | $0.018 | $0.020 |
| **Midjourney** | ~$0.02* | ~$0.02* | ~$0.02* |
| **FLUX Pro** | - | $0.03-0.05 | - |
| **FLUX Schnell** | $0.003 | - | - |
| **Ideogram** | $0.02 | $0.04 | $0.08 |
| **SD 3.5** | Free** | Free** | Free** |

*Midjourney based on subscription divided by fast hours
**Self-hosted, only GPU/compute costs

### Monthly Cost Scenarios

| Use Case | Volume | Recommended | Est. Monthly Cost |
|----------|--------|-------------|-------------------|
| **Hobbyist** | ~100/month | FLUX Schnell, Free tiers | $0-10 |
| **Content Creator** | ~500/month | Midjourney Standard, FLUX | $30-50 |
| **Agency** | ~2000/month | Mix of services | $100-200 |
| **Enterprise** | ~10000/month | SD self-hosted + APIs | $200-500 |

### Cost Optimization Tips

1. **Prototype with cheap models** - Use FLUX Schnell or Ideogram free tier
2. **Batch similar requests** - Reduce API overhead
3. **Self-host for volume** - SD 3.5 is free (compute only)
4. **Use appropriate quality** - Standard often sufficient
5. **Cache results** - Don't regenerate identical prompts
6. **Choose right model** - Text in images? Use DALL-E/Ideogram, not FLUX

---

## Production Workflows

### Asset Generation Pipeline

```python
import os
import json
import hashlib
from datetime import datetime

class ImageGenerationPipeline:
    def __init__(self, output_dir: str = "generated_assets"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.manifest = []

    def generate_dall_e(self, prompt: str, **kwargs) -> dict:
        from openai import OpenAI
        client = OpenAI()

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=kwargs.get("size", "1024x1024"),
            quality=kwargs.get("quality", "hd"),
            style=kwargs.get("style", "vivid"),
            response_format="b64_json"
        )

        # Save image
        import base64
        image_data = base64.b64decode(response.data[0].b64_json)
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        filename = f"dalle3_{prompt_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(image_data)

        # Record metadata
        metadata = {
            "model": "dall-e-3",
            "prompt": prompt,
            "revised_prompt": response.data[0].revised_prompt,
            "filepath": filepath,
            "timestamp": datetime.now().isoformat(),
            "params": kwargs
        }
        self.manifest.append(metadata)

        return metadata

    def generate_flux(self, prompt: str, **kwargs) -> dict:
        import replicate

        model = kwargs.get("model", "black-forest-labs/flux-1.1-pro")
        output = replicate.run(
            model,
            input={
                "prompt": prompt,
                "aspect_ratio": kwargs.get("aspect_ratio", "1:1"),
                "output_format": kwargs.get("format", "png")
            }
        )

        # Download image
        import requests
        response = requests.get(output)
        prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
        filename = f"flux_{prompt_hash}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        metadata = {
            "model": model,
            "prompt": prompt,
            "filepath": filepath,
            "timestamp": datetime.now().isoformat(),
            "params": kwargs
        }
        self.manifest.append(metadata)

        return metadata

    def save_manifest(self):
        manifest_path = os.path.join(self.output_dir, "manifest.json")
        with open(manifest_path, "w") as f:
            json.dump(self.manifest, f, indent=2)

# Usage
pipeline = ImageGenerationPipeline("project_assets")

# Generate hero images
for style in ["professional", "creative", "minimalist"]:
    pipeline.generate_dall_e(
        f"Hero image for tech startup, {style} style, abstract neural network pattern",
        quality="hd",
        size="1792x1024"
    )

pipeline.save_manifest()
```

### Batch Generation

```python
import asyncio
from typing import List, Dict

async def batch_generate(prompts: List[str], model: str = "flux") -> List[Dict]:
    """Generate multiple images concurrently."""
    import aiohttp
    import replicate

    async def generate_one(prompt: str) -> Dict:
        output = await asyncio.to_thread(
            replicate.run,
            "black-forest-labs/flux-1.1-pro",
            input={"prompt": prompt, "aspect_ratio": "1:1"}
        )
        return {"prompt": prompt, "url": output}

    tasks = [generate_one(p) for p in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return [r for r in results if not isinstance(r, Exception)]

# Usage
prompts = [
    "Product shot of wireless earbuds on marble",
    "Product shot of smartwatch on wooden desk",
    "Product shot of laptop in modern office",
]

results = asyncio.run(batch_generate(prompts))
```

### A/B Testing Images

```python
def generate_variants(base_prompt: str, variations: List[str], model: str = "dall-e-3") -> List[Dict]:
    """Generate prompt variations for A/B testing."""
    from openai import OpenAI
    client = OpenAI()

    results = []
    for variation in variations:
        full_prompt = f"{base_prompt}, {variation}"
        response = client.images.generate(
            model="dall-e-3",
            prompt=full_prompt,
            size="1024x1024",
            quality="standard"
        )
        results.append({
            "variation": variation,
            "prompt": full_prompt,
            "revised_prompt": response.data[0].revised_prompt,
            "url": response.data[0].url
        })

    return results

# Test different styles
variants = generate_variants(
    base_prompt="Landing page hero image for AI productivity app",
    variations=[
        "minimalist design, blue gradient",
        "vibrant colors, abstract shapes",
        "dark theme, neon accents",
        "natural lighting, workspace setting"
    ]
)
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| **faion-video-gen-skill** | Generate source images for image-to-video |
| **faion-openai-api-skill** | DALL-E API details |
| **faion-langchain-skill** | Build image generation chains |
| **faion-marketing-domain-skill** | Social media and ad visuals |

---

## Ethical Considerations

### Content Guidelines

1. **Consent** - Don't generate images of real people without permission
2. **Deepfakes** - Avoid creating misleading content
3. **Copyright** - Don't replicate copyrighted characters/art
4. **NSFW** - Follow platform content policies
5. **Attribution** - Credit AI generation when required

### Safety Filters

All major platforms have content safety filters:

| Platform | Safety Level |
|----------|--------------|
| DALL-E 3 | Strict, built-in |
| Midjourney | Strict, terms enforced |
| FLUX Pro | Configurable (1-6) |
| SD 3.5 | Local = user responsibility |

### Licensing

| Model | Commercial Use |
|-------|----------------|
| DALL-E 3 | Yes |
| Midjourney | Yes (paid plans) |
| FLUX Pro | Yes |
| FLUX Dev | Non-commercial only |
| FLUX Schnell | Yes (Apache 2.0) |
| SD 3.5 | Check specific license |

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Blurry output | Low resolution, wrong model | Use HD quality, larger size |
| Wrong subject | Ambiguous prompt | Be more specific, use negative prompts |
| Distorted faces | Model limitation | Use portrait-specific models |
| Wrong text | Model weakness | Use DALL-E 3 or Ideogram |
| Inconsistent style | Prompt drift | Use style references, seed values |
| API timeout | Long generation | Increase timeout, use async |
| Rate limited | Too many requests | Implement backoff, queue requests |

### Quality Checklist

Before using generated images:

- [ ] Resolution appropriate for use case
- [ ] No visible artifacts or distortions
- [ ] Text renders correctly (if applicable)
- [ ] Composition matches requirements
- [ ] Style consistent with brand
- [ ] No copyright/trademark issues
- [ ] Suitable for target audience

---

## References

- [OpenAI DALL-E Documentation](https://platform.openai.com/docs/guides/images)
- [Midjourney Documentation](https://docs.midjourney.com)
- [Black Forest Labs FLUX](https://blackforestlabs.ai)
- [Stability AI SD 3.5](https://stability.ai/stable-diffusion-3-5)
- [Ideogram Documentation](https://ideogram.ai/docs)
- [Replicate Model Library](https://replicate.com/models)
- [ComfyUI Workflows](https://github.com/comfyanonymous/ComfyUI)

---

*Skill Version: 1.0*
*Last Updated: 2026-01-18*
*Part of Faion Network AI/LLM Skills*


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-GEN-001-image-prompting | M-GEN-001-image-prompting | [methodologies/M-GEN-001-image-prompting.md](methodologies/M-GEN-001-image-prompting.md) |
| M-GEN-002-video-generation-workflow | M-GEN-002-video-generation-workflow | [methodologies/M-GEN-002-video-generation-workflow.md](methodologies/M-GEN-002-video-generation-workflow.md) |
| M-GEN-003-voice-synthesis | M-GEN-003-voice-synthesis | [methodologies/M-GEN-003-voice-synthesis.md](methodologies/M-GEN-003-voice-synthesis.md) |
| M-GEN-004-audio-transcription | M-GEN-004-audio-transcription | [methodologies/M-GEN-004-audio-transcription.md](methodologies/M-GEN-004-audio-transcription.md) |
| M-GEN-005-multimodal-pipelines | M-GEN-005-multimodal-pipelines | [methodologies/M-GEN-005-multimodal-pipelines.md](methodologies/M-GEN-005-multimodal-pipelines.md) |
| M-GEN-006-finetuning-workflow | M-GEN-006-finetuning-workflow | [methodologies/M-GEN-006-finetuning-workflow.md](methodologies/M-GEN-006-finetuning-workflow.md) |
| M-GEN-007-content-moderation | M-GEN-007-content-moderation | [methodologies/M-GEN-007-content-moderation.md](methodologies/M-GEN-007-content-moderation.md) |
| M-GEN-008-asset-management | M-GEN-008-asset-management | [methodologies/M-GEN-008-asset-management.md](methodologies/M-GEN-008-asset-management.md) |
