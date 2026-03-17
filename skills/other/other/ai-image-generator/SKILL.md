---
name: ai-image-generator
description: "Generate AI images using Gemini or GPT APIs directly. Covers model selection (Gemini for scenes, GPT for transparent icons), the 5-part prompting framework, API calling patterns, multi-turn editing, and quality assurance. Produces photorealistic scenes, icons, illustrations, OG images, and product shots. Use when building websites that need images, creating marketing assets, or generating visual content. Triggers: 'generate image', 'ai image', 'create hero image', 'make an icon', 'generate illustration', 'create og image', 'ai art', 'image generation'."
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
compatibility: claude-code-only
---

# AI Image Generator

Generate images using AI APIs (Google Gemini and OpenAI GPT). This skill teaches the prompting patterns and API mechanics for producing professional images directly from Claude Code.

> **Managed alternative**: If you don't want to manage API keys, [ImageBot](https://imagebot.au) provides a managed image generation service with album templates and brand kit support.

## Model Selection

Choose the right model for the job:

| Need | Model | Why |
|------|-------|-----|
| **Scenes / stock photos** | Gemini 3.1 Flash Image | Best depth, complexity, environmental context |
| **Transparent icons / logos** | GPT Image 1.5 | Native RGBA alpha channel (`background: "transparent"`) |
| **Text on images** | GPT Image 1.5 | 90% accurate text rendering |
| **Drafts / iteration** | Gemini 2.5 Flash Image | Free tier (~500/day) |
| **Final client assets** | Gemini 3 Pro Image | Higher detail, better style consistency |

### Model IDs

| Model | API ID | Provider |
|-------|--------|----------|
| Gemini 3.1 Flash Image | `gemini-3.1-flash-image-preview` | Google AI |
| Gemini 3 Pro Image | `gemini-3-pro-image-preview` | Google AI |
| Gemini 2.5 Flash Image | `gemini-2.5-flash-image` | Google AI |
| GPT Image 1.5 | `gpt-image-1.5` | OpenAI |

**Verify model IDs before use** — they change frequently:
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY" | python3 -c "import sys,json; [print(m['name']) for m in json.load(sys.stdin)['models'] if 'image' in m['name'].lower()]"
```

## The 5-Part Prompting Framework

Build prompts in this order for consistent results:

### 1. Image Type
Set the genre: "A photorealistic photograph", "An isometric illustration", "A flat vector icon"

### 2. Subject
Who or what, with specific details: "of a warm, approachable Australian woman in her early 30s, smiling naturally"

### 3. Environment
Setting and spatial relationships: "in a bright modern home with terracotta decor on wooden shelves behind her"

### 4. Technical Specs
Camera and lighting: "Shot at 85mm f/2.0, natural window light, head and shoulders framing"

### 5. Constraints
What to exclude: "Photorealistic, no text, no watermarks, no logos"

### Example (Good vs Bad)

```
BAD — keyword soup:
"professional woman, spa, warm lighting, high quality, 4K"

GOOD — narrative direction:
"A professional skin treatment scene in a warm clinical setting.
A practitioner wearing blue medical gloves uses a microneedling pen
on the client's forehead. The client lies on a white treatment bed,
eyes closed, relaxed. Warm golden-hour light from a window to the
left. Terracotta-toned wall visible in the background. Shot at
85mm f/2.0, shallow depth of field. No text, no watermarks."
```

## Workflow

### 1. Determine Image Need

| Purpose | Aspect Ratio | Model |
|---------|-------------|-------|
| Hero banner | 16:9 or 21:9 | Gemini |
| Service card | 4:3 or 3:4 | Gemini |
| Profile / avatar | 1:1 | Gemini |
| Icon / badge | 1:1 | GPT (transparent) |
| OG / social share | 1.91:1 | Gemini |
| Instagram post | 1:1 or 4:5 | Gemini |
| Mobile hero | 9:16 | Gemini |

### 2. Build the Prompt

Use the 5-part framework. Refer to `references/prompting-guide.md` for detailed photography parameters.

### 3. Generate via API

#### Gemini (Python — handles shell escaping correctly)

```python
python3 << 'PYEOF'
import json, base64, urllib.request, os, sys

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Set GEMINI_API_KEY environment variable"); sys.exit(1)

model = "gemini-3.1-flash-image-preview"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"

prompt = """A professional photograph of a modern co-working space in
Newcastle, Australia. Natural light floods through floor-to-ceiling
windows. Three people collaborate at a standing desk — one pointing
at a laptop screen. Exposed brick wall, potted fiddle-leaf fig,
coffee cups on the desk. Shot at 35mm f/4.0, environmental portrait
style. No text, no watermarks, no logos."""

payload = json.dumps({
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "responseModalities": ["TEXT", "IMAGE"],
        "temperature": 0.8
    }
}).encode()

req = urllib.request.Request(url, data=payload, headers={
    "Content-Type": "application/json",
    "User-Agent": "ImageGen/1.0"
})

resp = urllib.request.urlopen(req, timeout=120)
result = json.loads(resp.read())

# Extract image from response
for part in result["candidates"][0]["content"]["parts"]:
    if "inlineData" in part:
        img_data = base64.b64decode(part["inlineData"]["data"])
        output_path = "hero-image.png"
        with open(output_path, "wb") as f:
            f.write(img_data)
        print(f"Saved: {output_path} ({len(img_data):,} bytes)")
        break
PYEOF
```

#### GPT (Transparent Icons)

```python
python3 << 'PYEOF'
import json, base64, urllib.request, os, sys

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Set OPENAI_API_KEY environment variable"); sys.exit(1)

url = "https://api.openai.com/v1/images/generations"

payload = json.dumps({
    "model": "gpt-image-1.5",
    "prompt": "A minimal, clean plumbing wrench icon. Flat design, single consistent stroke weight, modern style. On a transparent background.",
    "n": 1,
    "size": "1024x1024",
    "background": "transparent",
    "output_format": "png"
}).encode()

req = urllib.request.Request(url, data=payload, headers={
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
})

resp = urllib.request.urlopen(req, timeout=120)
result = json.loads(resp.read())

img_data = base64.b64decode(result["data"][0]["b64_json"])
with open("icon-wrench.png", "wb") as f:
    f.write(img_data)
print(f"Saved: icon-wrench.png ({len(img_data):,} bytes)")
PYEOF
```

### 4. Save and Optimise

Save generated images to `.jez/artifacts/` or the user's specified path.

Post-processing (optional):
```bash
# Convert to WebP for web use
python3 -c "
from PIL import Image
img = Image.open('hero-image.png')
img.save('hero-image.webp', 'WEBP', quality=85)
print(f'WebP: {img.size[0]}x{img.size[1]}')
"

# Trim whitespace from transparent icons
python3 -c "
from PIL import Image
img = Image.open('icon.png')
trimmed = img.crop(img.getbbox())
trimmed.save('icon-trimmed.png')
"
```

### 5. Quality Check (Optional)

Send the generated image back to a vision model for QA:

```python
# Send to Gemini Flash for critique
critique_prompt = """Review this image for:
1. AI artifacts (extra fingers, floating objects, text errors)
2. Technical accuracy (wrong equipment, unsafe positioning)
3. Composition issues (awkward cropping, cluttered background)
4. Style consistency with a professional stock photo

List any issues found, or say 'PASS' if the image is production-ready."""
```

If issues are found, append them as negative guidance to the original prompt and regenerate.

## Multi-Turn Editing

Gemini supports editing a generated image across conversation turns. The key requirement: **preserve thought signatures** from model responses.

```python
# Turn 1: Generate base image
contents = [{"role": "user", "parts": [{"text": "Scene prompt..."}]}]

# The response includes thoughtSignature on parts — preserve them ALL

# Turn 2: Edit the image
contents = [
    {"role": "user", "parts": [{"text": "Original prompt"}]},
    {"role": "model", "parts": response_parts_with_signatures},  # Keep intact
    {"role": "user", "parts": [{"text": "Edit: change the wall colour to blue. Keep everything else exactly the same."}]}
]
```

**Edit prompt pattern**: Always specify what to KEEP unchanged, not just what to change. The model treats unlisted elements as free to modify.

```
GOOD: "Edit this image: keep the people, desk, and window unchanged.
Only change: wall colour from terracotta to ocean blue."

BAD: "Now make the wall blue."
(Model may change everything else too)
```

## API Key Setup

| Provider | Get key at | Env variable |
|----------|-----------|-------------|
| Google Gemini | [aistudio.google.com](https://aistudio.google.com/apikey) | `GEMINI_API_KEY` |
| OpenAI | [platform.openai.com](https://platform.openai.com/api-keys) | `OPENAI_API_KEY` |

```bash
export GEMINI_API_KEY="your-key-here"
export OPENAI_API_KEY="your-key-here"
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using curl for Gemini prompts | Use Python — shell escaping breaks on apostrophes |
| "Beautiful, professional, high quality" | Use concrete specs: "85mm f/1.8, golden hour light" |
| Not specifying what to exclude | Always end with "No text, no watermarks, no logos" |
| Requesting transparent PNG from Gemini | Gemini cannot do transparency — use GPT with `background: "transparent"` |
| American defaults for AU businesses | Explicitly specify "Australian" + local architecture, vegetation |
| Generic data for model ID | Verify current model IDs — they change frequently |
