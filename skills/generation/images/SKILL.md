---
name: skill-stack-thumbnails
description: Generate blog post thumbnails for Skill Stack using the brand aesthetic. Follows an iterative workflow - brainstorm concepts, get approval, generate with Gemini API.
---

# Skill Stack Thumbnail Generator

Generate on-brand thumbnails for Skill Stack blog posts using Google's Gemini API.

## Brand Identity

**Skill Stack** is a curated repository of SKILL.md files for content creators. The aesthetic is:
- **Clean and minimal** - Anthropic-adjacent sophistication
- **Paper/document metaphor** - Skills as stackable knowledge artifacts
- **Terracotta accent** - Single warm pop of color
- **Editorial quality** - Think publishing meets productivity

### Logo Reference

The logo is 4 stacked paper documents:
- 3 gray layers (light → medium → darker)
- 1 terracotta top layer with folded corner
- Warm cream background
- Subtle shadows for depth

## Color Palette

| Role | Color | Hex |
|------|-------|-----|
| **Primary Accent** | Terracotta/Coral | `#D4654A` |
| **Background** | Warm Cream | `#F5F3EE` |
| **Paper Light** | Light Gray | `#E8E6E1` |
| **Paper Medium** | Medium Gray | `#DEDBD5` |
| **Paper Dark** | Darker Gray | `#D4D1CB` |
| **Text/Line** | Near-Black | `#2D2D2D` |

**Rule**: Terracotta appears on ONE element only per image.

---

## Workflow

### Step 1: Understand the Post

Read the post title and content to understand:
- What's the core concept?
- What metaphor would resonate?
- What visual would make someone click?

### Step 2: Brainstorm Concepts (APPROVAL REQUIRED)

Generate 4-5 visual concepts. Each should be:
- **One sentence** describing the visual
- **Concrete** - you can picture it instantly
- **Non-generic** - no lightbulbs, handshakes, arrows
- **On-brand** - fits the paper/document aesthetic

**Format for presenting concepts:**

```
## Thumbnail Concepts for "[Post Title]"

1. **[Short label]** - One sentence visual description. Why it works.

2. **[Short label]** - Description...

3. **[Short label]** - Description...

4. **[Short label]** - Description...

Which direction resonates? I can refine from there.
```

**Wait for user approval before proceeding.**

### Step 3: Develop the Prompt

Once user selects a concept, expand into full prompt:

```
Create a minimal editorial thumbnail for a blog post about [TOPIC].

CONCEPT: [Expand the selected concept into 2-3 sentences]

STYLE: Clean, flat editorial illustration with paper-like shapes and subtle shadows.
Think Anthropic brand guidelines meets publishing design - sophisticated, minimal, intentional.
NOT photorealistic. NOT glossy AI aesthetic. NOT busy.

COMPOSITION:
- Focal element offset to [left/right third]
- Generous negative space (40%+ of frame empty)
- Single clear focal point
- Asymmetrical balance

COLOR PALETTE:
- Background: warm cream, almost off-white (like #F5F3EE)
- Primary accent: terracotta/burnt coral (like #D4654A) on ONE key element only
- Supporting: light gray and medium gray tones for layered paper shapes
- Shadows: soft, subtle, not harsh drop shadows

TEXTURE: Matte paper quality. Flat shapes with slight edge shadows.
No glossy renders. No gradients. No photorealism.

AVOID:
- Busy compositions
- More than 2-3 distinct elements
- Photorealistic rendering
- Cliche imagery (lightbulbs, gears, arrows)
- Neon or saturated colors
- Gradients
- Glossy AI aesthetic
- Text or words in the image

FORMAT: 16:9 landscape aspect ratio for blog thumbnails
```

### Step 4: Generate

Run via Gemini API:

```bash
cd scripts/images
export GEMINI_API_KEY=$(grep GEMINI_API_KEY ../../.env.local | cut -d= -f2)
python3 generate_image.py "PROMPT" --output ../../public/images/thumbnails --name "post-slug"
```

Or use the `/gemini-imagegen` skill if available.

### Step 5: Review & Iterate

After generation:
- **80% good?** Request specific edits
- **Composition off?** Adjust framing language
- **Wrong vibe?** Simplify further or try different concept
- **Too busy?** Remove elements

---

## Concept Templates by Post Type

### Framework Posts (CODER, 4S, etc.)
- Stacked/layered shapes representing steps
- Flow diagrams with paper elements
- Numbered paper cards in sequence

### Philosophy/Thesis Posts
- Transformation metaphors (rough → polished)
- Contrast/juxtaposition of two elements
- Single powerful symbol

### Tool/Technical Posts
- Tool icon + paper document interaction
- Simple geometric representation
- Integration/connection visual

### How-To/Practical Posts
- Action in progress (folding, stacking, organizing)
- Before/after implied through arrangement
- Single focused action

---

## Example Concepts

**For "The 4S Framework":**
1. **Four stacked squares** - Four paper squares arranged diagonally ascending, each labeled S1-S4, top one terracotta
2. **Funnel of papers** - Four documents funneling into one polished output
3. **Compass with 4 points** - Vintage compass where N/E/S/W are replaced by the 4 S's
4. **Building blocks** - Four cube shapes stacking, architectural quality

**For "Transform Don't Generate":**
1. **Crumpled to crisp** - Crumpled paper ball on left, crisp folded document on right, terracotta accent on the crisp one
2. **Rough cut to gem** - Raw stone transforming into faceted shape
3. **Sketch to blueprint** - Messy sketch evolving into clean technical drawing

---

## Output Location

Save thumbnails to: `public/images/thumbnails/[post-slug].png`

Reference in frontmatter: `image: "/images/thumbnails/[post-slug].png"`

---

*Always get concept approval before generating. The thinking is as important as the image.*
