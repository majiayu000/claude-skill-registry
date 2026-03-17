---
name: create-image
description: >
  Create images using AI generation (FLUX.1-schnell, Ollama), Mermaid diagrams,
  or placeholders. Supports multiple backends with automatic fallback.
allowed-tools: Bash, Read, Write
triggers:
  - create image
  - generate image
  - make image
  - ai image
  - create diagram
  - generate diagram
  - mermaid diagram
  - flowchart image
metadata:
  short-description: "Create images (AI-generated, Mermaid, placeholders)"

provides:
  - create-image
composes:
  - memory
  - dogpile
  - create-movie
  - task-monitor
---

# create-image

Generate images using FREE AI image generation backends.

## Features

- **Ollama (local)** - Z-Image Turbo or FLUX2-Klein via Ollama (FREE, no internet)
- **Gemini 2.5 Flash Image** - AI-generated images via Google gemini-2.5-flash-image (FREE with API key)
- **FLUX.1-schnell** - AI-generated images via HuggingFace (FREE remote)
- **Mermaid diagrams** - Flowcharts and architecture diagrams (FREE)
- **Placeholder images** - Random grayscale from picsum.photos (FREE)
- **Solid color** - Gray box with text label (always works)
- **Size control** - Specify dimensions for PDF embedding (auto-resized)

## Quick Start

```bash
cd .pi/skills/create-image

# Generate an AI image (uses Gemini or FLUX)
uv run --script generate.py "hardware verification flowchart for microprocessor" \
  --output test_figure.png \
  --size 400x600

# Generate with specific backend
uv run --script generate.py "network security architecture" \
  --output security_arch.png \
  --size 800x600 \
  --backend flux

# Use placeholder fallback
uv run --script generate.py "placeholder" \
  --output placeholder.png \
  --size 400x300 \
  --backend placeholder
```

## Commands

### `generate` - Create an image

```bash
uv run --script generate.py "<prompt>" [options]
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `prompt` | Description of the image to generate |

**Options:**
| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file path | `fixture_image.png` |
| `--size` | `-s` | Image dimensions (WxH) | `512x512` |
| `--backend` | `-b` | Generation backend | `auto` |

### Backends

| Backend       | Description                    | Requires                             | Cost              |
| ------------- | ------------------------------ | ------------------------------------ | ----------------- |
| `gemini`      | Gemini 2.5 Flash Image         | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | **FREE**          |
| `google`      | Alias for gemini               | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | **FREE**          |
| `ollama`      | Z-Image/FLUX2 local generation | Ollama + model                       | **FREE (local)**  |
| `flux`        | FLUX.1-schnell AI generation   | `HF_TOKEN`                           | **FREE (remote)** |
| `mermaid`     | Flowchart/diagram generation   | `mmdc` CLI                           | **FREE**          |
| `placeholder` | picsum.photos (grayscale)      | Nothing                              | **FREE**          |
| `solid`       | Gray box with text label       | Pillow                               | **FREE**          |
| `auto`        | Try backends in order          | Any available                        | -                 |

## Setup

### Option 1: Ollama (macOS only - MLX framework)

**Note:** Ollama image generation currently only works on macOS (Apple Silicon). Linux/NVIDIA support is "coming soon" per [Ollama docs](https://ollama.com/blog).

```bash
# macOS only
ollama pull x/z-image-turbo
# or
ollama pull x/flux2-klein
```

### Option 2: Google Gemini 2.5 Flash Image (Nano Banana) (FREE API)

Get a FREE API key from [aistudio.google.com](https://aistudio.google.com/):

```bash
export GEMINI_API_KEY="your_api_key_here"
# or
export GOOGLE_API_KEY="your_api_key_here"
```

**Note:** This uses the `gemini-2.5-flash-image` model (aka "nano-banana") via the REST API. No special SDK installation required (uses `requests`). Image generation counts against your daily Pro quota (~1000 images/day). Either `GEMINI_API_KEY` or `GOOGLE_API_KEY` will work.

### Option 3: HuggingFace Token (FREE Remote)

Get a FREE HuggingFace token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens):

```bash
export HF_TOKEN="hf_your_token_here"
```

### Option 4: Mermaid (for Diagrams)

```bash
npm install -g @mermaid-js/mermaid-cli
```

## Example Prompts

### Security Documents

```bash
"APT attack kill chain diagram with reconnaissance, weaponization, delivery, exploitation phases"
"network intrusion detection system architecture"
"malware analysis workflow flowchart"
```

### Engineering Documents

```bash
"hardware verification flow for microprocessor with RTL, synthesis, and timing analysis"
"FPGA design pipeline from HDL to bitstream"
"embedded systems boot sequence diagram"
```

### Scientific Documents

```bash
"machine learning pipeline with data preprocessing, training, and inference stages"
"experimental methodology flowchart"
"system architecture diagram with numbered components"
```

## Cached Images (Reuse Before Generating)

Pre-generated images are available in `cached_images/` - **use these first** to avoid unnecessary API calls:

| File               | Description                            | Size    |
| ------------------ | -------------------------------------- | ------- |
| `decorative.png`   | Abstract cover/decorative illustration | 512x512 |
| `flowchart.png`    | Technical workflow/process diagram     | 512x512 |
| `network_arch.png` | Network/system architecture diagram    | 512x512 |

```bash
# Copy cached image instead of generating
cp cached_images/flowchart.png /path/to/output.png
```

## Integration with PDF Generation

After generating images, embed them in PDFs:

```python
import fitz  # PyMuPDF

doc = fitz.open()
page = doc.new_page()

# Insert generated image
img_rect = fitz.Rect(50, 200, 450, 500)  # x0, y0, x1, y1
page.insert_image(img_rect, filename="test_figure.png")

doc.save("fixture_with_figure.pdf")
```

## Dependencies

```toml
dependencies = [
    "huggingface_hub>=0.26.0",
    "httpx",
    "typer",
    "pillow",
]
```
