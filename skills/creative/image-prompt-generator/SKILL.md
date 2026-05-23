---
name: image-prompt-generator
description: Generate AI images using Gemini image generation API. Use this skill when content needs images - thumbnails, social posts, blog headers, or creative visuals. Follows an iterative workflow - brainstorm concepts, select direction, generate in multiple styles, then produce via API.
---

# Image Prompt Generator

Generate professional, non-generic images using Google's Gemini API for image generation.

## Prerequisites & Setup

### Getting Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### Configuring the API Key

**Option 1: Environment file (recommended)**

Create a `.env` file in your project root:

```bash
GEMINI_API_KEY=your_api_key_here
```

**Option 2: Direct environment variable**

```bash
export GEMINI_API_KEY=your_api_key_here
```

### Install Dependencies

```bash
pip install google-generativeai python-dotenv pillow
```

### Available Models

| Model | API Name | Best For |
|-------|----------|----------|
| **Flash** | `gemini-2.5-flash-image` | Speed, drafts, iteration |
| **Pro** | `gemini-3-pro-image-preview` | **Final assets, 16:9 aspect ratio, quality** |

### Image Size (CRITICAL for quality)

| Size | Output | Use For |
|------|--------|---------|
| 1K | ~400KB | Drafts, iteration |
| **2K** | ~2MB | **Thumbnails, web assets (default)** |
| 4K | ~7MB | Print, high-resolution needs |

**CRITICAL**: Always specify `--size 2K` or `--size 4K` for final assets. Without this, output defaults to 1K which looks low-quality.

### Skill Stack Thumbnails - MANDATORY SETTINGS

For ANY Skill Stack thumbnail, you MUST use:

```bash
python scripts/images/generate_image.py "YOUR PROMPT" \
  --model pro \
  --size 2K \
  --aspect 16:9 \
  --output public/images/thumbnails \
  --name your-slug
```

And your prompt MUST include risograph style instructions:

```
STYLE: Risograph / screen print aesthetic. Visible halftone dots throughout. 
Slight misregistration between color layers. Indie printmaking quality - warm, tactile, handmade.

COLOR: Warm cream base. Charcoal and gray tones. Terracotta (#D4654A) accent on ONE key element.

TEXTURE: Visible halftone pattern. Paper grain. NOT smooth digital gradients.

AVOID: Empty white borders, photorealism, glossy renders, smooth gradients, clip art aesthetic.
```

**WHY**: Without `--size 2K`, output is ~400KB garbage that looks like it was made with Flash. Without risograph style, output looks generic and AI-generated.

---

## Workflow Overview

1. **Brainstorm Concepts** - Generate 4-6 high-level visual ideas
2. **Select Direction** - User picks the concept they like
3. **Optimize Prompt** - Refine into a strong, detailed prompt
4. **Style Variations** - Adapt to 2-3 different visual styles
5. **Generate Images** - Run via Gemini API

## Step 1: Brainstorm Concepts

When the user provides a topic or use case, generate **3 high-level visual concepts** and indicate your pick. Each concept should be:

- **One sentence** describing the visual idea
- **Concrete and immediate** - you can picture it instantly
- **Conceptual but not abstract** - a clear object/scene with meaning
- **Non-generic** - avoid cliches (no lightbulbs for ideas, no handshakes for partnership)

**Format:**

```
**Concept A:** One sentence description of the visual concept and why it works.

**Concept B:** One sentence description...

**Concept C:** One sentence description...

**My pick: Concept X** — Brief reasoning why this one is strongest.
```

**Example for "newsletter about personal productivity":**

```
**Concept A:** A vintage compass where the needle points toward a coffee ring stain on a map—direction emerges from daily rituals.

**Concept B:** A clock where the 12 hours show seasonal changes—time management over long arcs, not just hours.

**Concept C:** One small key attached to dozens of decorative keychains—we overcomplicate simple solutions.

**My pick: Concept A** — The coffee stain is unexpected and personal, the compass is concrete without being cliché.
```

Wait for user to confirm or redirect before proceeding.

## Step 2: Optimize the Prompt

Once the user selects a concept, develop it into a full prompt. Structure:

```
Create a [style type] illustration of [subject].

CONCEPT: [Expand the one-sentence idea into a clear visual description]

STYLE: [Artistic approach - load from references/styles/ if brand-specific]

COMPOSITION: [Framing, focal point, negative space, balance]

COLORS: [Palette - describe by name, not hex codes which may render as text]

TEXTURE: [Surface qualities, analog/digital feel]

AVOID: [What should NOT appear - be specific]

FORMAT: [Aspect ratio]
```

**Key principles:**
- Natural language, full sentences - no tag soup
- Describe colors by name (burnt orange, sky blue, near-black) not hex codes
- Maximum 2-3 elements - if it feels busy, remove something
- Favor metaphor over literal depiction

## Step 3: Style Variations

**MANDATORY for Skill Stack: Risograph style.** Every thumbnail must include risograph style instructions in the prompt. See `references/styles/risograph.md`.

Key risograph elements to ALWAYS include in prompt:
- "Visible halftone dots throughout"
- "Slight misregistration between color layers"
- "Indie printmaking quality - warm, tactile, handmade"
- "NOT smooth digital gradients"

Available styles in `references/styles/` (for non-Skill-Stack projects):

- **risograph.md** - DEFAULT. Halftone dots, misregistration, indie printmaking aesthetic.
- **minimalist-ink.md** - High-contrast black and white, crosshatching.
- **watercolor-line.md** - Ink linework with watercolor washes.
- **editorial-conceptual.md** - Conceptual, sophisticated, editorial wit.

## Step 4: Generate via API

### Running the Script

```bash
# Generate 2K thumbnail (recommended for web)
python scripts/images/generate_image.py "prompt here" --model pro --aspect 16:9 --size 2K

# Generate 4K for print/high-res
python scripts/images/generate_image.py "prompt here" --model pro --size 4K

# Save to specific folder
python scripts/images/generate_image.py "prompt" --output "./images" --name "my_image" --size 2K
```

**Options:**
- `--model pro` (default, higher quality) or `--model flash` (faster)
- `--size 2K` (default), `1K`, or `4K` - **always use 2K or 4K for final assets**
- `--aspect 16:9` (default), `1:1`, `9:16`, `3:4`, `4:3`
- `--variations N` - generate N versions
- `--output ./path` - save location
- `--name prefix` - filename prefix

**Output location:** Save images alongside the content they belong to - not a generic images dump.

## Step 5: Iterate

After user reviews generated images:
- **80% good?** Request specific edits conversationally rather than regenerating
- **Composition off?** Adjust framing or element placement in prompt
- **Wrong style?** Try a different style reference
- **Too busy?** Simplify to fewer elements
- **Colors wrong?** Be more explicit about palette

## Prompting Principles

### Write Like a Creative Director

Brief the model like a human artist. Use proper grammar, full sentences, and descriptive adjectives.

| Don't | Do |
|-------|-----|
| "Cool car, neon, city, night, 8k" | "A cinematic wide shot of a futuristic sports car speeding through a rainy Tokyo street at night. The neon signs reflect off the wet pavement and the car's metallic chassis." |

**Be specific about:**
- **Subject:** Instead of "a woman," say "a sophisticated elderly woman wearing a vintage chanel-style suit"
- **Materiality:** Describe textures - "matte finish," "brushed steel," "soft velvet," "crumpled paper"
- **Setting:** Define location, time of day, weather
- **Lighting:** Specify mood and light source
- **Mood:** Emotional tone of the image

### Provide Context

Context helps the model make logical artistic decisions. Include the "why" or "for whom."

**Example:** "Create an image of a sandwich for a Brazilian high-end gourmet cookbook."
*(Model infers: professional plating, shallow depth of field, perfect lighting)*

### Keep It Simple

- One clear focal point
- Maximum 2-3 elements total
- Generous negative space
- If it feels busy, remove something

### Avoid the Generic

**Hard rules:**
- **NEVER include text in images** - Text renders poorly and looks amateur
- No lightbulbs for "ideas"
- No handshakes for "partnership"
- No audio waveforms for "podcasts" or "audio"
- No gears/cogs for "systems" or "process"
- No happy stock photo poses
- No glossy AI aesthetic
- No puzzle pieces for "connection" or "integration"

### Metaphors That Work

Strong concepts from past generations:
- **Orange cut open revealing neural network** - organic exterior, systematic interior (knowledge systems, RAG)
- **Mail slot with origami bird emerging** - delivery transforms into something alive (newsletters)
- **Exercise club crossed with quill pen** - physical culture meets intellectual work (body + mind)
- **Typewriter key extreme close-up with radiating impact** - decisive action, command (books, authority)
- **Medicine dropper with mandala bloom** - clinical precision meets transcendence (therapy, transformation)
- **Straight razor on leather strop** - precision tool, polishing, refinement (editing, production)
- **Prism dispersing light into distinct beams** - one input, multiple outputs (frameworks)
- **Compass with coffee stain on map** - direction from daily rituals (productivity)

## Resources

### references/styles/
Aesthetic style definitions:
- `risograph.md` - **DEFAULT** - Halftone, misregistration, indie printmaking
- `minimalist-ink.md` - Black and white ink illustration
- `watercolor-line.md` - Ink with watercolor washes
- `editorial-conceptual.md` - Conceptual editorial style

### scripts/
- `generate_image.py` - Gemini API image generation

## Prompt Modifiers Reference

| Category | Examples |
|----------|----------|
| **Lighting** | golden hour, dramatic shadows, soft diffused light, neon glow, overcast |
| **Style** | cinematic, editorial, technical diagram, hand-drawn, photorealistic |
| **Texture** | matte finish, brushed steel, soft velvet, crumpled paper, weathered wood |
| **Composition** | wide shot, close-up, bird's eye view, dutch angle, symmetrical |
| **Mood** | energetic, serene, dramatic, playful, sophisticated |
| **Quality** | 4K, high-fidelity, pixel-perfect, professional grade |

## Advanced Capabilities

### Text Rendering & Infographics

Put exact text in quotes. Specify style: "polished editorial," "technical diagram," or "hand-drawn whiteboard."

**Example prompts:**

```
Earnings Report Infographic:
"Generate a clean, modern infographic summarizing the key financial highlights from this earnings report. Include charts for 'Revenue Growth' and 'Net Income', and highlight the CEO's key quote in a stylized pull-quote box."
```

```
Whiteboard Summary:
"Summarize the concept of 'Transformer Neural Network Architecture' as a hand-drawn whiteboard diagram suitable for a university lecture. Use different colored markers for the Encoder and Decoder blocks, and include legible labels for 'Self-Attention' and 'Feed Forward'."
```

### Character Consistency & Thumbnails

Use reference images and state "Keep the person's facial features exactly the same as Image 1." Describe expression/action changes while maintaining identity.

**Example prompt:**

```
Viral Thumbnail:
"Design a viral video thumbnail using the person from Image 1.
Face Consistency: Keep the person's facial features exactly the same as Image 1, but change their expression to look excited and surprised.
Action: Pose the person on the left side, pointing their finger towards the right side of the frame.
Subject: On the right side, place a high-quality image of a delicious avocado toast.
Graphics: Add a bold yellow arrow connecting the person's finger to the toast.
Text: Overlay massive, pop-style text in the middle: 'Done in 3 mins!'. Use a thick white outline and drop shadow.
Background: A blurred, bright kitchen background. High saturation and contrast."
```

### Image Reworking (Edit Existing Images)

The `--input` flag enables "rework mode" - pass an existing image to Gemini and describe the changes you want.

**Key use cases:**
- **Small tweaks** - Adjust colors, add/remove elements, change lighting
- **Style transfer** - Keep composition but change artistic style
- **Object manipulation** - Remove, add, or modify specific objects
- **Seasonal/temporal changes** - Same scene, different time/season

**Running in rework mode:**

```bash
# Basic edit - add something
python scripts/generate_image.py "Add snow to the roof and yard" \
  --input ./house.png \
  --model pro

# Color adjustment
python scripts/generate_image.py "Change the accent color from red to teal, keep everything else identical" \
  --input ./thumbnail.png \
  --model pro

# Style transfer - keep composition, change aesthetic
python scripts/generate_image.py "Convert this to risograph style with halftone dots and slight color misregistration" \
  --input ./photo.png \
  --model pro

# Generate variations of an edit
python scripts/generate_image.py "Make the lighting warmer, like golden hour" \
  --input ./portrait.png \
  --variations 3 \
  --model pro
```

**Prompting tips for rework mode:**

1. **Be specific about what to preserve:**
   - "Keep the person's facial features exactly the same"
   - "Maintain the composition and framing"
   - "Don't change the background"

2. **Be explicit about what to change:**
   - "Change ONLY the color of the shirt from blue to red"
   - "Add snow to the roof and nothing else"
   - "Remove the text overlay"

3. **Use comparative language:**
   - "Make the colors more vibrant"
   - "Increase the contrast slightly"
   - "Make the lighting softer and more diffused"

**Output naming:** Files from rework mode are named `{prefix}_{timestamp}_edit_{model}.png` to distinguish from generated images (`_gen_`).

### Advanced Editing Examples

**Object Removal:**
```bash
python scripts/generate_image.py \
  "Remove the tourists from the background and fill with matching cobblestones and storefronts" \
  --input ./street-photo.png \
  --model pro
```

**Seasonal Control:**
```bash
python scripts/generate_image.py \
  "Turn this into winter. Add snow to the roof and yard. Change lighting to cold, overcast afternoon. Keep architecture identical." \
  --input ./house-summer.png \
  --model pro
```

**Character Consistency (thumbnail series):**
```bash
python scripts/generate_image.py \
  "Keep the person's face exactly the same. Change expression to surprised. Add a pointing gesture toward the right side of the frame." \
  --input ./person-reference.png \
  --model pro
```

---

## Related Skills

- **youtube-title-creator** - Pair generated images with optimized titles
- **social-content-creation** - Use images in platform-optimized posts

---

*For custom brand styles, create new style files in references/styles/ following the existing format*
