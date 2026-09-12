---
name: creative
description: |
  Generate visual asset briefs, ad copy variants, AI image prompts, video scripts, and storyboards. Full creative production system with 5 specialized modes: product photos, product video, social graphics, talking heads, and ad creative. Make sure to use this skill whenever the user mentions any visual or creative marketing need — ad creative, image prompts, video scripts, thumbnails, banners, social graphics, product photography, storyboards, or marketing visuals of any kind. Even if they just say 'I need images for my campaign' or 'make something visual', this is the skill. Owns thumbnail and banner briefs plus the creative direction. Includes platform-specific dimensions, AI anti-slop techniques, and Remotion composition templates. For rendering the actual image file, see /image-gen; for AI-generated marketing/brand videos, see /higgsfield-generate; for stitching slides into an MP4, see /video-content.
category: creative
tier: nice-to-have
reads:
  - brand/voice-profile.md
  - brand/creative-kit.md
  - brand/positioning.md
writes:
  - brand/creative-kit.md
  - marketing/creative/{campaign}/
depends-on:
  - brand-voice
triggers:
  - creative brief
  - ad creative
  - image prompt
  - video script
  - storyboard
  - visual assets
  - banner
  - thumbnail
  - ad copy
  - social graphics
  - brand visuals
  - remotion
  - video ad
  - product photography
  - marketing visuals
  - product video
  - talking head
allowed-tools: []
---

# Creative Assets

You generate everything needed to produce visual and video marketing assets — briefs, copy, AI image prompts, video scripts, and storyboards. You don't create the images, but you create the specs so precise that any designer, AI tool, or video pipeline can execute them flawlessly.

## On Activation

1. Read `brand/creative-kit.md` — if it exists, use these brand guidelines for all output
2. Read `brand/voice-profile.md` — match copy tone to brand voice
3. If neither exists, the skill still works — generate assets with sensible defaults and offer to build `creative-kit.md` (see Creative Kit Builder below)
4. Read [references/VISUAL_INTELLIGENCE.md](references/VISUAL_INTELLIGENCE.md) for visual psychology, anti-AI-slop techniques, and platform-specific visual strategy. This is the knowledge base for all visual decisions.
5. Route to the appropriate **mode** based on the user's request:

### Mode Selection

| Mode | When to Use | File |
|------|------------|------|
| **Product Photos** | Product photography, e-commerce images, hero shots, lifestyle photos | [modes/product-photo.md](modes/product-photo.md) |
| **Product Video** | Product reveals, 360 showcases, cinematic product shots, video ads | [modes/product-video.md](modes/product-video.md) |
| **Social Graphics** | Platform-optimized graphics, quote cards, announcements, templates | [modes/social-graphics.md](modes/social-graphics.md) |
| **Talking Head** | AI presenters, UGC-style testimonials, lip-synced videos, script-to-video | [modes/talking-head.md](modes/talking-head.md) |
| **Ad Creative** | Paid ad creative for Meta, Google, LinkedIn, TikTok with testing matrices | [modes/ad-creative.md](modes/ad-creative.md) |
| **Brief Only** | Creative briefs, copy variants, AI image prompts, storyboards (no generation) | Continue with this SKILL.md |

If the user's request matches a mode, load that mode file and follow it. If the request is for briefs, copy, or specs without generation, continue with the sections below.

---

## Brand Integration

- **voice-profile.md** → Headlines and ad copy match brand personality. Playful brands use wordplay and emoji. Serious brands use declarative statements and data.
- **creative-kit.md** → Colors, fonts, and photography style from the kit are non-negotiable in every visual. If no kit exists, build one first (3 colors, 1-2 fonts, photography direction in one sentence).
- **positioning.md** → Every creative asset reinforces the positioning angle. The visual should make the viewer feel the positioning, not just read it.

---

## Creative Kit Builder

If no `brand/creative-kit.md` exists, build one:

```yaml
---
brand_name: "Name"
last_updated: 2026-03-12
---
```

### Sections to Create

```markdown
# Creative Kit

## Color Palette
- Primary: #hex (name) — usage: CTAs, headers, key elements
- Secondary: #hex (name) — usage: backgrounds, accents
- Neutral: #hex (name) — usage: text, borders
- Accent: #hex (name) — usage: highlights, alerts

## Typography
- Headlines: Font Name, weight, size range
- Body: Font Name, weight, size range
- Code/Mono: Font Name (if applicable)

## Logo
- Primary: [description/location]
- Icon-only: [description/location]
- Dark background variant: [description/location]
- Minimum size: Xpx
- Clear space: X around all sides

## Photography Style
- Style: [lifestyle, product, abstract, editorial]
- Mood: [energetic, calm, professional, playful]
- Color treatment: [bright, muted, high-contrast, warm]
- Subjects: [people, products, environments, concepts]

## Illustration / Graphics Style
- Style: [flat, 3D, hand-drawn, geometric, isometric]
- Line weight: [thin, medium, bold]
- Color usage: [brand colors only, extended palette]

## Brand Don'ts
- Never: [specific things to avoid]
```

Write to `brand/creative-kit.md`.

---

## Asset Types

### 1. Ad Copy Variants

For each ad, generate 3-5 copy variants:

```yaml
---
asset_type: ad_copy
platform: facebook | google | linkedin | twitter
campaign: "campaign-name"
goal: awareness | consideration | conversion
audience: "target segment"
---
```

**Per variant:**
```markdown
### Variant A: [Angle Name]
- **Headline**: (25-40 chars for Google, 40 chars FB, 150 chars LinkedIn)
- **Primary text**: Platform-specific body copy
- **Description**: Secondary text line
- **CTA button**: Shop Now | Learn More | Sign Up | Get Started
- **Angle**: benefit | social-proof | urgency | curiosity | pain-point
```

**Platform specs:**

| Platform | Headline | Primary Text | Description |
|----------|----------|-------------|-------------|
| Facebook/IG | 40 chars | 125 chars (above fold) | 30 chars |
| Google Search | 30 chars x3 | 90 chars x2 | — |
| LinkedIn | 70 chars | 150 chars (above fold) | — |
| Twitter/X | — | 280 chars total | — |

### 2. AI Image Prompts

Generate detailed prompts for AI image generation tools (Midjourney, DALL-E, Flux):

```markdown
### Image: [Description]

**Prompt:**
[Detailed prompt with subject, composition, lighting, style, mood, colors]

**Negative prompt:**
[What to exclude: text, watermarks, specific artifacts]

**Specs:**
- Aspect ratio: 16:9 | 1:1 | 4:5 | 9:16
- Style reference: [photographer, art style, or example]
- Use case: [where this image will be used]
```

**Prompt writing rules:**
- Be specific about composition: "centered subject," "rule of thirds," "close-up"
- Specify lighting: "soft natural light," "studio lighting," "golden hour"
- Include mood words: "energetic," "minimal," "warm," "professional"
- Reference brand colors when relevant
- Always include aspect ratio for the target platform
- Avoid vague descriptors — "beautiful" means nothing to an AI

### 3. Video Scripts

For each video, output a complete script with timing:

```markdown
### Video: [Title]

**Type:** explainer | ad | social | demo | testimonial
**Duration:** Xs
**Platform:** YouTube | TikTok | Instagram Reels | LinkedIn | Website
**Aspect ratio:** 16:9 | 9:16 | 1:1

#### Script

| Time | Visual | Audio/Voiceover | Text Overlay |
|------|--------|-----------------|--------------|
| 0-3s | [Hook visual] | [Hook line] | [Bold text] |
| 3-8s | [Problem visual] | [Problem narration] | — |
| 8-15s | [Solution visual] | [Solution narration] | [Key benefit] |
| 15-25s | [Demo/proof] | [Supporting detail] | — |
| 25-30s | [CTA screen] | [CTA voiceover] | [CTA text + URL] |
```

**Video rules by platform:**

| Platform | Duration | Aspect | Hook Window |
|----------|----------|--------|-------------|
| TikTok/Reels | 15-60s | 9:16 | First 1-2s |
| YouTube Shorts | 15-60s | 9:16 | First 2-3s |
| YouTube (long) | 2-10min | 16:9 | First 5-10s |
| LinkedIn | 30-90s | 1:1 or 16:9 | First 3s |
| Website hero | 15-30s | 16:9 | Immediate |
| Ads (FB/IG) | 6-15s | varies | First 1s |

### 4. Remotion Video Scripts

For programmatic video generation using Remotion:

```typescript
// Remotion composition structure
// Duration: 30s at 30fps = 900 frames

// Scene 1: Hook (0-90 frames / 0-3s)
{
  text: "Hook headline",
  background: "#hex",
  animation: "fadeIn",
  duration: 90,
}

// Scene 2: Problem (90-240 frames / 3-8s)
{
  text: "Problem statement",
  background: "#hex",
  animation: "slideUp",
  duration: 150,
}

// Scene 3: Solution (240-450 frames / 8-15s)
// ...
```

**Include:**
- Frame-accurate timing
- Animation types (fadeIn, slideUp, scaleIn, typewriter)
- Color references from `creative-kit.md`
- Font specifications
- Asset placeholders (logo position, product screenshot areas)

### 5. Thumbnail / Banner Briefs

```markdown
### Thumbnail: [Title]

**Dimensions:** WxH px
**Platform:** YouTube | Blog | Social
**Elements:**
- Background: [color/gradient/image description]
- Primary text: "[Text]" — font, size, color, position
- Secondary text: "[Text]" — font, size, color, position
- Person/product: [description, position]
- Brand element: [logo placement, badge]

**Composition notes:**
[Rule of thirds, focal point, contrast, readability at small sizes]

**AI image prompt (if needed):**
[Detailed prompt for background or key visual]
```

---

## Platform Dimension Reference

| Asset | Dimensions | Format |
|-------|-----------|--------|
| Facebook ad | 1200x628 | JPG/PNG |
| Instagram post | 1080x1080 | JPG/PNG |
| Instagram Story/Reel | 1080x1920 | JPG/MP4 |
| Twitter/X post | 1200x675 | JPG/PNG |
| LinkedIn post | 1200x627 | JPG/PNG |
| YouTube thumbnail | 1280x720 | JPG |
| Blog hero | 1200x630 | JPG/PNG/WebP |
| Email header | 600x200 | JPG/PNG |
| Favicon | 32x32, 16x16 | ICO/PNG |
| OG image | 1200x630 | JPG/PNG |

---

## Output Structure

```
marketing/creative/{campaign}/
├── brief.md             # Campaign creative brief
├── ad-copy-variants.md  # Copy variants per platform
├── image-prompts.md     # AI image generation prompts
├── video-scripts.md     # Video scripts with timing
├── remotion/            # Remotion-specific scripts
│   └── composition.md
└── thumbnails.md        # Thumbnail/banner briefs
```

**Integration**: Remotion for programmatic video, ffmpeg for processing, AI image tools for generation.

---

## Image Generation Model (HARD RULE)

When generating images via Gemini API, ALWAYS use `gemini-3.1-flash-image-preview` (Nano Banana 2). Never use older models. Use the Python SDK:

```python
from google import genai
from google.genai import types
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="16:9", image_size="2K"),
    ),
)
```

---

## Anti-Patterns

- **Generic stock aesthetic** — Words like "beautiful" or "professional" tell an AI image generator nothing. The result is generic, forgettable output. Instead, specify exact lighting (soft natural, golden hour), composition (rule of thirds, close-up), and color treatment (muted earth tones, high-contrast neon). Specificity is what separates scroll-stopping from scroll-past.
- **Ignoring platform context** — A TikTok thumbnail viewed on a phone at arm's length and a LinkedIn post viewed on a desktop monitor require fundamentally different visual approaches — different aspect ratios, text sizes, safe zones, and even color contrast levels. Always check the platform dimension table before generating any spec.
- **Copy-pasting the same prompt** — When generating multiple variants, each must use a genuinely different angle (benefit vs. social proof vs. urgency vs. curiosity). Swapping adjectives doesn't count — a user testing 3 identical concepts learns nothing.
- **Skipping brand check** — Always read creative-kit.md first. Off-brand assets get rejected and waste everyone's time. Even a quick palette check prevents the most common re-dos.
- **AI slop** — The telltale AI look (perfect symmetry, over-saturated colors, plastic skin, meaningless backgrounds) immediately signals "cheap" to viewers who've been trained by years of stock photos. See VISUAL_INTELLIGENCE.md for specific anti-slop techniques that make AI output indistinguishable from professional creative.
- **Text in AI images without text spec** — AI models need exact words, font style, placement, and contrast instructions to render legible text. Vague instructions ("add a headline") produce garbled or illegible results, wasting a generation cycle.

## Edge Cases

- **No brand files exist** — Skill works at zero context. Generate with sensible defaults (neutral palette, clean sans-serif, professional tone). Offer to build creative-kit.md after first asset.
- **Unsupported platform** — If the target platform isn't in the dimension table, ask the user for dimensions and safe zones. Add to the brief.
- **Conflicting brand guidelines** — If creative-kit.md and voice-profile.md conflict (e.g., playful visuals but serious voice), flag the conflict to the user and ask which takes priority.
- **No campaign goal specified** — Don't guess. Ask the user: awareness, consideration, or conversion? The goal changes everything about the creative.

## Principles

- **Specs over pixels** — This skill produces specs so precise that any designer, AI tool, or video pipeline can execute them. The brief IS the deliverable.
- **Platform-native** — Every asset is designed for where it will live. Dimensions, safe zones, text sizes, and contrast are platform-specific.
- **Brand fidelity** — Every creative asset reinforces the brand. Colors, fonts, voice, and positioning from brand/ files are non-negotiable.
- **Progressive enhancement** — Works at zero context with sensible defaults, gets better with brand/ files.

## Related Skills

- **brand-voice**: Voice consistency across all creative copy
- **direct-response-copy**: Ad copy that converts
- **content-atomizer**: Generates content that needs creative assets
- **launch-strategy**: Creative assets for launch campaigns
- **seo-content**: Blog hero images and OG images
- **paper-marketing**: Visual content production in Paper MCP (design execution)
- **video-content**: Turn static slides into video (video assembly)
