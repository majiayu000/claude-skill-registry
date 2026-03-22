---
name: automatic1111
description: |
  Feature-rich Stable Diffusion Web UI for image generation. Supports txt2img, img2img,
  inpainting, outpainting, LoRA, extensions, upscaling, and batch processing. Widely used
  desktop interface with an extensive extension ecosystem and API access.
license: Apache-2.0
compatibility: 'python 3.10+, CUDA 11.8+ / ROCm / CPU, Linux/Windows/macOS'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
    - stable-diffusion
    - image-generation
    - web-ui
    - img2img
    - lora
---

# Automatic1111 (Stable Diffusion WebUI)

## Installation

```bash
# install.sh — Clone and launch Stable Diffusion WebUI
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui

# Download a model (SDXL or SD 1.5)
wget -P models/Stable-diffusion/ \
    "https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors"

# Launch (auto-installs dependencies on first run)
./webui.sh --listen --api --xformers
# Visit http://localhost:7860
```

## API: Text to Image

```python
# txt2img_api.py — Generate images via the built-in REST API
import requests
import base64
from pathlib import Path

API_URL = "http://localhost:7860"

payload = {
    "prompt": "A serene Japanese garden with cherry blossoms, watercolor painting style, detailed",
    "negative_prompt": "blurry, low quality, distorted, text, watermark",
    "steps": 30,
    "cfg_scale": 7.5,
    "width": 1024,
    "height": 1024,
    "sampler_name": "DPM++ 2M Karras",
    "seed": -1,
    "batch_size": 1,
}

response = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload)
data = response.json()

for i, img_b64 in enumerate(data["images"]):
    img_bytes = base64.b64decode(img_b64)
    Path(f"output_{i}.png").write_bytes(img_bytes)
    print(f"Saved output_{i}.png")
```

## API: Image to Image

```python
# img2img_api.py — Transform an existing image with a new prompt
import requests
import base64
from pathlib import Path

API_URL = "http://localhost:7860"

# Read input image as base64
input_image = base64.b64encode(Path("input.png").read_bytes()).decode()

payload = {
    "init_images": [input_image],
    "prompt": "Transform into an oil painting, impressionist style",
    "negative_prompt": "blurry, distorted",
    "steps": 30,
    "cfg_scale": 7,
    "denoising_strength": 0.6,  # 0.0 = no change, 1.0 = full regeneration
    "width": 1024,
    "height": 1024,
    "sampler_name": "DPM++ 2M Karras",
}

response = requests.post(f"{API_URL}/sdapi/v1/img2img", json=payload)
data = response.json()

img_bytes = base64.b64decode(data["images"][0])
Path("output_img2img.png").write_bytes(img_bytes)
```

## API: Inpainting

```python
# inpainting_api.py — Edit specific regions of an image using a mask
import requests
import base64
from pathlib import Path

API_URL = "http://localhost:7860"

input_image = base64.b64encode(Path("photo.png").read_bytes()).decode()
mask_image = base64.b64encode(Path("mask.png").read_bytes()).decode()  # White = edit area

payload = {
    "init_images": [input_image],
    "mask": mask_image,
    "prompt": "A golden retriever puppy sitting on the grass",
    "negative_prompt": "blurry, distorted",
    "steps": 30,
    "cfg_scale": 7,
    "denoising_strength": 0.75,
    "inpainting_fill": 1,  # 0=fill, 1=original, 2=latent noise, 3=latent nothing
    "mask_blur": 4,
    "width": 1024,
    "height": 1024,
}

response = requests.post(f"{API_URL}/sdapi/v1/img2img", json=payload)
img_bytes = base64.b64decode(response.json()["images"][0])
Path("inpainted.png").write_bytes(img_bytes)
```

## Using LoRA Models

```bash
# Place LoRA files in the models directory
# models/Lora/my_style.safetensors
```

```python
# lora_usage.py — Apply LoRA weights in prompts via the API
import requests
import base64
from pathlib import Path

API_URL = "http://localhost:7860"

payload = {
    "prompt": "<lora:my_style:0.8> A portrait in my custom style, detailed, high quality",
    "negative_prompt": "blurry, low quality",
    "steps": 30,
    "cfg_scale": 7,
    "width": 1024,
    "height": 1024,
}

response = requests.post(f"{API_URL}/sdapi/v1/txt2img", json=payload)
img_bytes = base64.b64decode(response.json()["images"][0])
Path("lora_output.png").write_bytes(img_bytes)
```

## Extensions

```bash
# Install popular extensions via git clone into the extensions directory
cd stable-diffusion-webui/extensions

# ControlNet — Guided generation with edge/depth/pose
git clone https://github.com/Mikubill/sd-webui-controlnet.git

# Adetailer — Automatic face/hand detail improvement
git clone https://github.com/Bing-su/adetailer.git

# Regional Prompter — Different prompts for different image regions
git clone https://github.com/hako-mikan/sd-webui-regional-prompter.git

# Restart WebUI to load extensions
```

## Batch Processing

```python
# batch_generate.py — Generate multiple images with different prompts
import requests
import base64
from pathlib import Path

API_URL = "http://localhost:7860"

prompts = [
    "A cyberpunk city at night, neon lights, rain",
    "A cozy cabin in the mountains, snow, warm light",
    "An underwater coral reef, tropical fish, sunlight",
]

for i, prompt in enumerate(prompts):
    response = requests.post(f"{API_URL}/sdapi/v1/txt2img", json={
        "prompt": prompt,
        "negative_prompt": "blurry, low quality",
        "steps": 25,
        "cfg_scale": 7,
        "width": 1024,
        "height": 1024,
    })
    img_bytes = base64.b64decode(response.json()["images"][0])
    Path(f"batch_{i}.png").write_bytes(img_bytes)
    print(f"Generated batch_{i}.png")
```

## Key Concepts

- **txt2img**: Generate images from text prompts — the core feature
- **img2img**: Transform existing images using prompts and denoising strength
- **Inpainting**: Edit specific masked regions while preserving the rest
- **LoRA**: Apply fine-tuned style adapters via `<lora:name:weight>` in prompts
- **Extensions**: Plugin system for ControlNet, Adetailer, regional prompting, and more
- **API**: Full REST API at `/sdapi/v1/` — automate everything the UI can do
- **Samplers**: DPM++ 2M Karras, Euler a, DDIM — different speed/quality tradeoffs
