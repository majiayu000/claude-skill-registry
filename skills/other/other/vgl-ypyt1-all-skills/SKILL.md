---
name: vgl
description: Write structured VGL (Visual Generation Language) JSON prompts for Bria's FIBO image generation models. Use this skill when creating detailed image descriptions in JSON format for text-to-image generation, image editing, inpainting, outpainting, background generation, or captioning. Triggers include requests to write structured prompts, create VGL JSON, describe images for AI generation, or work with Bria/FIBO's structured_prompt format. Also use when converting natural language image requests into the deterministic JSON schema required by FIBO models.
---

# Bria VGL Prompt Writing

Generate structured JSON prompts for Bria's FIBO models using Visual Generation Language (VGL).

> **Related Skill**: Use **[bria-ai](../bria-ai/SKILL.md)** to execute these VGL prompts via the Bria API. VGL defines the structured prompt format; bria-ai handles generation, editing, and background removal.

## Core Concept

VGL replaces ambiguous natural language prompts with deterministic JSON that explicitly declares every visual attribute: objects, lighting, camera settings, composition, and style. This ensures reproducible, controllable image generation.

## Operation Modes

| Mode | Input | Output | Use Case |
|------|-------|--------|----------|
| **Generate** | Text prompt | VGL JSON | Create new image from description |
| **Edit** | Image + instruction | VGL JSON | Modify reference image |
| **Edit_with_Mask** | Masked image + instruction | VGL JSON | Fill grey masked regions |
| **Caption** | Image only | VGL JSON | Describe existing image |
| **Refine** | Existing JSON + edit | Updated VGL JSON | Modify existing prompt |

## JSON Schema

Output a single valid JSON object with these required keys:

### 1. `short_description` (String)
Concise summary of image content, max 200 words. Include key subjects, actions, setting, and mood.

### 2. `objects` (Array, max 5 items)
Each object requires:

```json
{
  "description": "Detailed description, max 100 words",
  "location": "center | top-left | bottom-right foreground | etc.",
  "relative_size": "small | medium | large within frame",
  "shape_and_color": "Basic shape and dominant color",
  "texture": "smooth | rough | metallic | furry | fabric | etc.",
  "appearance_details": "Notable visual details",
  "relationship": "Relationship to other objects",
  "orientation": "upright | tilted 45 degrees | facing left | horizontal | etc."
}
```

**Human subjects** add:
```json
{
  "pose": "Body position description",
  "expression": "winking | joyful | serious | surprised | calm",
  "clothing": "Attire description",
  "action": "What the person is doing",
  "gender": "Gender description",
  "skin_tone_and_texture": "Skin appearance"
}
```

**Object clusters** add:
```json
{
  "number_of_objects": 3
}
```

**Size guidance**: If a person is the main subject, use `"medium-to-large"` or `"large within frame"`.

### 3. `background_setting` (String)
Overall environment, setting, and background elements not in `objects`.

### 4. `lighting` (Object)
```json
{
  "conditions": "bright daylight | dim indoor | studio lighting | golden hour | blue hour | overcast",
  "direction": "front-lit | backlit | side-lit from left | top-down",
  "shadows": "long, soft shadows | sharp, defined shadows | minimal shadows"
}
```

### 5. `aesthetics` (Object)
```json
{
  "composition": "rule of thirds | symmetrical | centered | leading lines | medium shot | close-up",
  "color_scheme": "monochromatic blue | warm complementary | high contrast | pastel",
  "mood_atmosphere": "serene | energetic | mysterious | joyful | dramatic | peaceful"
}
```
For people as main subject, specify shot type in composition: `"medium shot"`, `"close-up"`, `"portrait composition"`.

### 6. `photographic_characteristics` (Object)
```json
{
  "depth_of_field": "shallow | deep | bokeh background",
  "focus": "sharp focus on subject | soft focus | motion blur",
  "camera_angle": "eye-level | low angle | high angle | dutch angle | bird's-eye",
  "lens_focal_length": "wide-angle | 50mm standard | 85mm portrait | telephoto | macro"
}
```
**For people**: Prefer `"standard lens (35mm-50mm)"` or `"portrait lens (50mm-85mm)"`. Avoid wide-angle unless specified.

### 7. `style_medium` (String)
`"photograph"` | `"oil painting"` | `"watercolor"` | `"3D render"` | `"digital illustration"` | `"pencil sketch"`

Default to `"photograph"` unless explicitly requested otherwise.

### 8. `artistic_style` (String)
If not photograph, describe characteristics in max 3 words: `"impressionistic, vibrant, textured"`

For photographs, use `"realistic"` or similar.

### 9. `context` (String)
Describe the image type/purpose:
- `"High-fashion editorial photograph for magazine spread"`
- `"Concept art for fantasy video game"`
- `"Commercial product photography for e-commerce"`

### 10. `text_render` (Array)
**Default: empty array `[]`**

Only populate if user explicitly provides exact text content:
```json
{
  "text": "Exact text from user (never placeholder)",
  "location": "center | top-left | bottom",
  "size": "small | medium | large",
  "color": "white | red | blue",
  "font": "serif typeface | sans-serif | handwritten | bold impact",
  "appearance_details": "Metallic finish | 3D effect | etc."
}
```
Exception: Universal text integral to objects (e.g., "STOP" on stop sign).

### 11. `edit_instruction` (String)
Single imperative command describing the edit/generation.

## Edit Instruction Formats

### For Standard Edits (no mask)
Start with action verb, describe changes, never reference "original image":

| Category | Rewritten Instruction |
|----------|----------------------|
| Style change | `Turn the image into the cartoon style.` |
| Object attribute | `Change the dog's color to black and white.` |
| Add element | `Add a wide-brimmed felt hat to the subject.` |
| Remove object | `Remove the book from the subject's hands.` |
| Replace object | `Change the rose to a bright yellow sunflower.` |
| Lighting | `Change the lighting from dark and moody to bright and vibrant.` |
| Composition | `Change the perspective to a wider shot.` |
| Text change | `Change the text "Happy Anniversary" to "Hello".` |
| Quality | `Refine the image to obtain increased clarity and sharpness.` |

### For Masked Region Edits
Reference "masked regions" or "masked area" as target:

| Intent | Rewritten Instruction |
|--------|----------------------|
| Object generation | `Generate a white rose with a blue center in the masked region.` |
| Extension | `Extend the image into the masked region to create a scene featuring...` |
| Background fill | `Create the following background in the masked region: A vast ocean extending to horizon.` |
| Atmospheric fill | `Fill the background masked area with a clear, bright blue sky with wispy clouds.` |
| Subject restoration | `Restore the area in the mask with a young woman.` |
| Environment infill | `Create inside the masked area: a greenhouse with rows of plants under glass ceiling.` |

## Fidelity Rules

### Standard Edit Mode
Preserve ALL visual properties unless explicitly changed by instruction:
- Subject identity, pose, appearance
- Object existence, location, size, orientation
- Composition, camera angle, lens characteristics
- Style/medium

Only change what the edit strictly requires.

### Masked Edit Mode
- Preserve all visible (non-masked) portions exactly
- Fill grey masked regions to blend seamlessly with unmasked areas
- Match existing style, lighting, and subject matter
- Never describe grey masks—describe content that fills them

## Example Output

```json
{
  "short_description": "A professional businesswoman in a navy blazer stands confidently in a modern glass office, holding a tablet. Natural daylight streams through floor-to-ceiling windows, creating a warm, productive atmosphere.",
  "objects": [
    {
      "description": "A confident businesswoman in her 30s with shoulder-length dark hair, wearing a tailored navy blazer over a white blouse. She holds a tablet in her left hand while gesturing naturally with her right.",
      "location": "center-right",
      "relative_size": "large within frame",
      "shape_and_color": "Human figure, navy and white clothing",
      "texture": "smooth fabric, professional attire",
      "appearance_details": "Minimal jewelry, well-groomed professional appearance",
      "relationship": "Main subject, interacting with tablet",
      "orientation": "facing slightly left, three-quarter view",
      "pose": "Standing upright, relaxed professional stance",
      "expression": "confident, approachable smile",
      "clothing": "Tailored navy blazer, white silk blouse, dark trousers",
      "action": "Presenting or reviewing information on tablet",
      "gender": "female",
      "skin_tone_and_texture": "Medium warm skin tone, healthy smooth complexion"
    },
    {
      "description": "A modern tablet device with a bright display showing charts and graphs",
      "location": "center, held by subject",
      "relative_size": "small",
      "shape_and_color": "Rectangular, silver frame with illuminated screen",
      "texture": "smooth glass and metal",
      "appearance_details": "Thin profile, business application visible on screen",
      "relationship": "Held by businesswoman, focus of her attention",
      "orientation": "vertical, screen facing viewer at slight angle",
      "pose": null,
      "expression": null,
      "clothing": null,
      "action": null,
      "gender": null,
      "skin_tone_and_texture": null,
      "number_of_objects": null
    }
  ],
  "background_setting": "Modern corporate office interior with floor-to-ceiling windows overlooking a city skyline. Minimalist furniture in neutral tones, potted plants adding touches of green.",
  "lighting": {
    "conditions": "bright natural daylight",
    "direction": "side-lit from left through windows",
    "shadows": "soft, natural shadows"
  },
  "aesthetics": {
    "composition": "rule of thirds, medium shot",
    "color_scheme": "professional blues and neutral whites with warm accents",
    "mood_atmosphere": "confident, professional, welcoming"
  },
  "photographic_characteristics": {
    "depth_of_field": "shallow, background slightly soft",
    "focus": "sharp focus on subject's face and upper body",
    "camera_angle": "eye-level",
    "lens_focal_length": "portrait lens (85mm)"
  },
  "style_medium": "photograph",
  "artistic_style": "realistic",
  "context": "Corporate portrait photography for company website or LinkedIn professional profile.",
  "text_render": [],
  "edit_instruction": "Generate a professional businesswoman in a modern office environment holding a tablet."
}
```

## Common Pitfalls

1. **Don't invent text** - Keep `text_render` empty unless user provides exact text
2. **Don't over-describe** - Max 5 objects, prioritize most important
3. **Match the mode** - Use correct `edit_instruction` format for masked vs standard edits
4. **Preserve fidelity** - Only change what's explicitly requested
5. **Be specific** - Use concrete values ("85mm portrait lens") not vague terms ("nice camera")
6. **Null for irrelevant** - Human-specific fields should be `null` for non-human objects

---

## Using VGL with Bria API

### Generate Image with Structured Prompt

Pass VGL JSON to the `structured_prompt` parameter:

```python
from bria_client import BriaClient

client = BriaClient()

vgl_prompt = {
    "short_description": "Professional businesswoman in modern office...",
    "objects": [...],
    # ... full VGL JSON
}

# Use structured_prompt for deterministic generation
result = client.refine(
    structured_prompt=json.dumps(vgl_prompt),
    instruction="Generate this scene",
    aspect_ratio="16:9"
)
print(result['result']['image_url'])
```

### Refine Existing Generation

After generation, Bria returns a `structured_prompt` you can modify and regenerate:

```python
# Initial generation
result = client.generate("A cozy coffee shop interior")
structured = result['result']['structured_prompt']

# Modify and regenerate
result = client.refine(
    structured_prompt=structured,
    instruction="Change the lighting to golden hour"
)
```

### curl Example

```bash
curl -X POST "https://engine.prod.bria-api.com/v2/image/generate" \
  -H "api_token: $BRIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "structured_prompt": "{\"short_description\": \"...\", ...}",
    "prompt": "Generate this scene",
    "aspect_ratio": "16:9"
  }'
```

---

## References

- **[Schema Reference](references/schema-reference.md)** - Complete JSON schema with all parameter values
- **[bria-ai](../bria-ai/SKILL.md)** - API client and endpoint documentation for executing VGL prompts
