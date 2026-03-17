---
name: gemini-3-image-generation
description: Generate images with Gemini 3 Pro Image (Nano Banana Pro). Covers 4K generation, text rendering, grounded generation with Google Search, conversational editing, and cost optimization. Use when creating images, generating 4K images, editing images conversationally, fact-verified image generation, or image output tasks.
---

# Gemini 3 Pro Image Generation (Nano Banana Pro)

Comprehensive guide for generating images with Gemini 3 Pro Image (`gemini-3-pro-image-preview`), also known as Nano Banana Pro. This skill focuses on IMAGE OUTPUT (generating images) - see `gemini-3-multimodal` for INPUT (analyzing images).

## Overview

**Gemini 3 Pro Image** (Nano Banana Pro 🍌) is Google's image generation model featuring native 4K support, text rendering within images, grounded generation with Google Search, and conversational editing capabilities.

### Key Capabilities

- **4K Resolution:** Native 4K generation with upscaling to 2K/4K
- **Text Rendering:** High-quality text within images
- **Grounded Generation:** Fact-verified images using Google Search
- **Conversational Editing:** Multi-turn image modification preserving context
- **Aspect Ratios:** Supports 16:9 and custom ratios at 4K
- **Quality Control:** Fine-tuned generation parameters

### When to Use This Skill

- Generating images from text prompts
- Creating 4K resolution images
- Rendering text within images
- Fact-verified image generation (grounded)
- Conversational image editing
- Multi-turn image refinement
- Custom aspect ratio images

---

## Quick Start

### Prerequisites

- **Gemini API setup** (see `gemini-3-pro-api` skill)
- **Model:** `gemini-3-pro-image-preview`

### Python Quick Start

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

# Use the image generation model
model = genai.GenerativeModel("gemini-3-pro-image-preview")

# Generate image
response = model.generate_content("A serene mountain landscape at sunset")

# Save image
if response.parts:
    with open("generated_image.png", "wb") as f:
        f.write(response.parts[0].inline_data.data)
    print("Image saved!")
```

### Node.js Quick Start

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";
import fs from "fs";

const genAI = new GoogleGenerativeAI("YOUR_API_KEY");
const model = genAI.getGenerativeModel({ model: "gemini-3-pro-image-preview" });

const result = await model.generateContent("A serene mountain landscape at sunset");
const imageData = result.response.parts[0].inlineData.data;

fs.writeFileSync("generated_image.png", Buffer.from(imageData, "base64"));
console.log("Image saved!");
```

---

## Core Tasks

### Task 1: Generate Image from Text Prompt

**Goal:** Create high-quality images from text descriptions.

**Python Example:**

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel(
    "gemini-3-pro-image-preview",
    generation_config={
        "thinking_level": "high",  # Best quality
        "temperature": 1.0
    }
)

# Generate image
prompt = """A futuristic cityscape at night with:
- Neon lights and holographic advertisements
- Flying vehicles
- Tall skyscrapers with unique architecture
- Rain-slicked streets reflecting the lights
- Cinematic, detailed, 4K quality"""

response = model.generate_content(prompt)

# Save image
if response.parts and hasattr(response.parts[0], 'inline_data'):
    image_data = response.parts[0].inline_data.data
    with open("futuristic_city.png", "wb") as f:
        f.write(image_data)
    print("Image generated successfully!")
else:
    print("No image generated")
```

**Tips for Better Prompts:**
- Be specific and detailed
- Specify art style (realistic, cartoon, oil painting, etc.)
- Include lighting, mood, and atmosphere
- Mention quality level (4K, detailed, high-quality)
- Describe colors, textures, composition

**See:** `references/generation-guide.md` for comprehensive prompting techniques

---

### Task 2: Generate 4K Images

**Goal:** Create high-resolution 4K images with upscaling.

**Python Example:**

```python
# Generate with 4K quality specification
prompt = """A photorealistic portrait of a scientist in a modern lab:
- 4K ultra-high definition
- Sharp focus on subject
- Soft bokeh background
- Professional studio lighting
- Fine detail in textures
- Cinema-grade quality"""

response = model.generate_content(prompt)

# 4K image will be generated
if response.parts:
    with open("scientist_4k.png", "wb") as f:
        f.write(response.parts[0].inline_data.data)
```

**4K Features:**
- Native 4K resolution support
- Upscaling to 2K/4K
- 16:9 aspect ratio at 4K
- Enhanced detail and clarity

**See:** `references/resolution-guide.md` for resolution control

---

### Task 3: Render Text in Images

**Goal:** Generate images with readable, high-quality text.

**Python Example:**

```python
prompt = """Create a professional business card design with:
- Company name: "TechVision AI"
- Text: "Dr. Sarah Chen"
- Text: "Chief AI Officer"
- Text: "sarah.chen@techvision.ai"
- Text: "+1 (555) 123-4567"
- Modern, clean design
- Professional fonts
- Blue and white color scheme
- All text clearly readable"""

response = model.generate_content(prompt)

if response.parts:
    with open("business_card.png", "wb") as f:
        f.write(response.parts[0].inline_data.data)
```

**Text Rendering Best Practices:**
- Explicitly specify text content in quotes
- Request "readable" or "clearly visible" text
- Keep text short and simple
- Specify font style if desired
- Use high contrast backgrounds

**See:** `references/generation-guide.md` for text rendering techniques

---

### Task 4: Grounded Generation (Fact-Verified Images)

**Goal:** Generate factually accurate images using Google Search grounding.

**Python Example:**

```python
# Enable Google Search grounding for factual accuracy
model_grounded = genai.GenerativeModel(
    "gemini-3-pro-image-preview",
    tools=[{"google_search_retrieval": {}}]  # Enable grounding
)

prompt = """Generate an accurate image of the International Space Station
with Earth in the background. Use current ISS configuration."""

response = model_grounded.generate_content(prompt)

if response.parts:
    with open("iss_grounded.png", "wb") as f:
        f.write(response.parts[0].inline_data.data)

    # Check if grounding was used
    if hasattr(response, 'grounding_metadata'):
        print(f"Grounding sources used: {len(response.grounding_metadata.grounding_chunks)}")
```

**Grounded Generation Use Cases:**
- Historical scenes (accurate to period)
- Scientific visualizations
- Current events
- Famous landmarks
- Product representations

**Benefits:**
- Factual accuracy
- Real-world grounding
- Reduced hallucination
- Up-to-date information

**Note:** Uses free Google Search quota (1,500 queries/day)

**See:** `references/grounded-generation.md` for comprehensive guide

---

### Task 5: Conversational Image Editing

**Goal:** Iteratively refine images through multi-turn conversation.

**Python Example:**

```python
model = genai.GenerativeModel("gemini-3-pro-image-preview")

# Start a chat session for conversational editing
chat = model.start_chat()

# First generation
response1 = chat.send_message("Create a cozy coffee shop interior")

if response1.parts:
    with open("coffee_shop_v1.png", "wb") as f:
        f.write(response1.parts[0].inline_data.data)

# Refine the image
response2 = chat.send_message("Add more plants and warm lighting")

if response2.parts:
    with open("coffee_shop_v2.png", "wb") as f:
        f.write(response2.parts[0].inline_data.data)

# Further refinement
response3 = chat.send_message("Make it more minimalist, remove some decorations")

if response3.parts:
    with open("coffee_shop_v3.png", "wb") as f:
        f.write(response3.parts[0].inline_data.data)
```

**Conversational Editing Features:**
- Preserves visual context across turns
- Incremental modifications
- Natural language instructions
- Multi-turn refinement
- Context-aware changes

**Example Editing Commands:**
- "Make it darker/lighter"
- "Add more [element]"
- "Change the color scheme to [colors]"
- "Make it more realistic/artistic"
- "Remove [element]"

**See:** `references/conversational-editing.md` for advanced patterns

---

### Task 6: Custom Aspect Ratios

**Goal:** Generate images in specific aspect ratios.

**Python Example:**

```python
# 16:9 aspect ratio (4K supported)
prompt_169 = "A cinematic landscape in 16:9 aspect ratio, 4K quality"

# Square aspect ratio
prompt_square = "A square logo design for a tech company"

# Portrait orientation
prompt_portrait = "A portrait-oriented movie poster"

response = model.generate_content(prompt_169)
# Image will be generated in specified ratio
```

**Supported Ratios:**
- **16:9** - Wide, cinematic (4K supported)
- **1:1** - Square
- **4:3** - Standard
- **9:16** - Vertical/portrait

---

### Task 7: Optimize Image Generation Costs

**Goal:** Balance quality and cost for image generation.

**Pricing:**
- **Text Input:** $1-2 per 1M tokens
- **Text Output:** $6-9 per 1M tokens
- **Image Output:** $0.134 per image (varies by resolution)

**Python Cost Optimization:**

```python
def generate_with_cost_tracking(prompt):
    """Generate image and track costs"""

    response = model.generate_content(prompt)

    # Calculate cost
    usage = response.usage_metadata
    input_cost = (usage.prompt_token_count / 1_000_000) * 2.00
    output_cost = (usage.candidates_token_count / 1_000_000) * 9.00
    image_cost = 0.134  # Per image

    total_cost = input_cost + output_cost + image_cost

    print(f"Input tokens: {usage.prompt_token_count} (${input_cost:.6f})")
    print(f"Output tokens: {usage.candidates_token_count} (${output_cost:.6f})")
    print(f"Image cost: ${image_cost:.6f}")
    print(f"Total: ${total_cost:.6f}")

    return response

response = generate_with_cost_tracking("A beautiful sunset over mountains")
```

**Cost Optimization Strategies:**
1. **Batch Requests:** Generate multiple images in one session
2. **Reuse Chat Sessions:** Conversational editing is more efficient
3. **Specific Prompts:** Clear prompts reduce regeneration needs
4. **Monitor Usage:** Track costs per project
5. **Use Appropriate Quality:** Not all images need 4K

**See:** `references/pricing-optimization.md` for detailed strategies

---

## Batch Image Generation

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-3-pro-image-preview")

prompts = [
    "A serene mountain lake at dawn",
    "A bustling market in Morocco",
    "A futuristic robot assistant",
    "An abstract geometric pattern"
]

for i, prompt in enumerate(prompts):
    print(f"Generating image {i+1}/{len(prompts)}: {prompt}")

    response = model.generate_content(prompt)

    if response.parts:
        with open(f"generated_{i+1}.png", "wb") as f:
            f.write(response.parts[0].inline_data.data)
        print(f"  Saved: generated_{i+1}.png")
```

---

## Error Handling

```python
from google.api_core import exceptions

def safe_image_generation(prompt):
    """Generate image with error handling"""

    try:
        response = model.generate_content(prompt)

        if not response.parts:
            return {"success": False, "error": "No image generated"}

        if not hasattr(response.parts[0], 'inline_data'):
            return {"success": False, "error": "Invalid response format"}

        return {
            "success": True,
            "image_data": response.parts[0].inline_data.data,
            "mime_type": response.parts[0].inline_data.mime_type
        }

    except exceptions.InvalidArgument as e:
        return {"success": False, "error": f"Invalid prompt: {e}"}
    except exceptions.ResourceExhausted as e:
        return {"success": False, "error": f"Rate limit exceeded: {e}"}
    except Exception as e:
        return {"success": False, "error": f"Error: {e}"}
```

---

## References

**Core Guides**
- [Model Setup](references/model-setup.md) - Nano Banana Pro configuration
- [Generation Guide](references/generation-guide.md) - Comprehensive prompting techniques
- [Grounded Generation](references/grounded-generation.md) - Fact-verified image creation
- [Conversational Editing](references/conversational-editing.md) - Multi-turn refinement

**Optimization**
- [Resolution Guide](references/resolution-guide.md) - 4K and quality control
- [Pricing Optimization](references/pricing-optimization.md) - Cost management

**Scripts**
- [Generate Image Script](scripts/generate-image.py) - Production-ready generation
- [Grounded Generation Script](scripts/grounded-gen.py) - Fact-verified images
- [Edit Image Script](scripts/edit-image.py) - Conversational editing

**Official Resources**
- [Imagen 3 Documentation](https://ai.google.dev/gemini-api/docs/imagen)
- [Image Generation Guide](https://ai.google.dev/gemini-api/docs/image-generation)
- [Pricing](https://ai.google.dev/pricing)

---

## Related Skills

- **gemini-3-pro-api** - Basic setup, authentication, text generation
- **gemini-3-multimodal** - Image INPUT (analyzing images)
- **gemini-3-advanced** - Advanced features (caching, batch, tools)

---

## Best Practices

1. **Be Specific:** Detailed prompts produce better results
2. **Specify Quality:** Request 4K or high quality explicitly
3. **Use Grounding:** Enable for factual accuracy
4. **Iterate Conversationally:** Use chat for refinements
5. **Monitor Costs:** Track usage, especially for 4K
6. **Handle Errors:** Implement retry logic
7. **Save Images Properly:** Use binary mode for writing

---

## Troubleshooting

### Issue: No image generated
**Solution:** Check `response.parts` exists and has `inline_data` attribute

### Issue: Low quality images
**Solution:** Add "4K", "high quality", "detailed" to prompt

### Issue: Text in images unreadable
**Solution:** Specify text explicitly in quotes, request "readable text"

### Issue: Images not factually accurate
**Solution:** Enable grounded generation with Google Search

### Issue: High costs
**Solution:** Optimize prompts, batch requests, monitor usage

---

## Summary

This skill provides complete image generation capabilities:

✅ Text-to-image generation
✅ Native 4K support
✅ Text rendering in images
✅ Grounded generation (fact-verified)
✅ Conversational editing
✅ Custom aspect ratios
✅ Cost optimization
✅ Production-ready examples

**Ready to generate images?** Start with Task 1: Generate Image from Text Prompt above!
