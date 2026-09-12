---
name: visual-style
description: >
  Build a persistent visual brand identity for image generation. Defines how
  the brand looks visually — aesthetic, lighting, composition, mood — and writes
  it to brand/creative-kit.md so /image-gen and other creative skills produce
  consistent on-brand visuals. Three modes: Extract (from website/URL), Build
  (interview), Reference (mood board/examples). Use when starting any project
  that needs images, when the user says "visual style", "brand aesthetic",
  "image style", "visual identity", "how should our images look", "build
  visual brand", "define our look", or when /image-gen outputs feel generic
  because no visual style exists yet.
reads:
  - brand/voice-profile.md
  - brand/positioning.md
  - brand/creative-kit.md
writes:
  - brand/creative-kit.md
depends-on:
  - brand-voice
triggers:
  - visual style
  - brand aesthetic
  - image style
  - visual identity
  - how should our images look
  - build visual brand
  - define our look
allowed-tools: []
---

# /visual-style — Visual Brand Identity Builder

Every brand has a voice. This skill gives it eyes.

Voice-profile.md defines how the brand *sounds*. Visual Brand Style defines how it *looks* — the lighting, the composition, the mood that makes someone see an image and know it's yours before reading a word.

---

## On Activation

1. Read `brand/creative-kit.md` if it exists. Check for a `## Visual Brand Style` section.
   - If the section exists and is populated (not template comments): **Refresh mode** — show current style, offer to update or replace.
   - If the section is template/empty: **Create mode** — build from scratch.
   - If `creative-kit.md` doesn't exist: create it first with `mktg init`, then proceed.
2. Read `brand/voice-profile.md` if it exists — personality informs visual tone (e.g., playful voice = warm/bright visuals, authoritative = clean/precise).
3. Read `brand/positioning.md` if it exists — angles inform visual metaphors (e.g., "the simple alternative" = minimalist aesthetic).
4. If no brand files exist, proceed anyway — ask the user directly. Progressive enhancement, not gating.

---

## Mode Selection

Use AskUserQuestion:

"How do you want to define your visual brand style?"

1. **Extract** — I'll analyze your website or existing assets to derive the visual identity
2. **Build** — I'll interview you about your visual preferences (5-7 questions)
3. **Reference** — You provide mood boards, example images, or reference URLs and I'll synthesize a style

---

## Mode 1: Extract

The user provides a URL or set of URLs (website, landing page, social profiles).

1. Use WebFetch to scrape each URL.
2. Analyze for visual patterns:
   - Dominant colors (map to hex codes)
   - Typography (serif vs sans-serif, weight, spacing)
   - Photography style (studio, candid, illustration, none)
   - Layout patterns (dense, airy, grid-heavy, asymmetric)
   - Mood (corporate, playful, premium, technical, warm)
3. Synthesize findings into the Visual Brand Style format.
4. Present to user via AskUserQuestion: "Here's what I extracted from your site. Does this capture your visual brand, or should I adjust?"

**Fallback:** If WebFetch is unavailable, switch to Build mode and tell the user why.

---

## Mode 2: Build

Interview the user. Ask one question at a time via AskUserQuestion.

**Question 1: Aesthetic anchor**
"Pick the closest match to how your brand should look visually:"
- Minimal and clean (Apple, Stripe)
- Warm and human (Mailchimp, Notion)
- Bold and energetic (Figma, Vercel)
- Premium and dark (Linear, Raycast)
- Editorial and photographic (Medium, Substack)
- Something else (describe it)

**Question 2: Lighting and mood**
"What lighting feels right for your brand's images?"
- Warm and golden (golden hour, ambient glow)
- Bright and airy (soft diffused, clean whites)
- Dramatic and contrasty (rim lighting, dark backgrounds)
- Natural and candid (daylight, real environments)
- Neon and digital (glowing screens, dark mode)

**Question 3: Composition**
"How should images be composed?"
- Single focal point with lots of breathing room
- Rich and detailed — fill the frame
- Asymmetric and editorial — off-center subjects
- Geometric and structured — grid-aligned elements

**Question 4: What to avoid**
"What should your images NEVER look like?"
(Free text — the user's avoidances are often more revealing than their preferences)

**Question 5: Reference**
"Name a brand, website, or aesthetic that captures what you're going for — even if it's in a completely different industry."

**Optional Question 6: Existing assets**
"Do you have any images that already feel on-brand? Describe them or share URLs."

Synthesize answers into the Visual Brand Style format.

---

## Mode 3: Reference

The user provides mood boards, image URLs, or descriptions of their ideal visual style.

1. If URLs: use WebFetch or Read to analyze the images/pages.
2. If descriptions: extract the key visual patterns.
3. Synthesize into Visual Brand Style format.
4. Present for confirmation.

---

## Output Format

Write the `## Visual Brand Style` section into `brand/creative-kit.md`. Preserve all existing sections (Brand Colors, Typography, Visual Style). Only add/update the Visual Brand Style section.

```markdown
## Visual Brand Style

- **Primary Aesthetic:** [derived aesthetic, e.g., "warm tech minimalism with editorial photography"]
- **Lighting:** [specific lighting direction, e.g., "soft diffused with rim lighting accents, warm color temperature"]
- **Backgrounds:** [background treatment, e.g., "dark slate (#0F172A) with warm accent gradients"]
- **Composition:** [layout approach, e.g., "single focal point, generous negative space for text overlay"]
- **Mood:** [emotional tone, e.g., "calm empowerment — powerful but approachable, like a quiet expert"]
- **Avoid:** [explicit exclusions, e.g., "generic stock photos, cold blue tech grids, floating 3D cubes, busy compositions"]
- **Reference Prompts:**
  1. [A proven prompt that captures the brand look — ready to paste into image gen]
  2. [A second prompt showing a different use case in the same style]
  3. [Optional third prompt for edge cases]
```

**Reference Prompts are critical.** These are the style anchors that `/image-gen` uses when generating on-brand images. They should be complete, narrative prompts (not keywords) that produce images distinctly *this brand*.

---

## Refresh Mode

When `## Visual Brand Style` already exists:

1. Present the current style summary.
2. AskUserQuestion: "Your visual brand style was last defined [date]. What would you like to do?"
   - Update specific fields (which ones?)
   - Rebuild from scratch
   - Add new reference prompts
   - Keep it as-is

---

## Progressive Enhancement

| Level | Context | Output quality |
|-------|---------|---------------|
| L0 | No brand files | Generic but functional — asks user directly, writes style from scratch |
| L1 | voice-profile.md exists | Personality-aligned — playful voice gets warm visuals |
| L2 | + creative-kit.md colors/typography | Color-constrained — prompts incorporate brand palette |
| L3 | + positioning.md | Full alignment — visual metaphors match positioning angles |

---

## Anti-Patterns

| Anti-pattern | Why it fails | Instead |
|-------------|-------------|---------|
| Locking into one rigid style | Brands need versatility — a blog header and an error page shouldn't look identical | Define the core aesthetic but include "also works for: [alternative moods]" in reference prompts |
| Ignoring existing creative-kit.md sections | Overwriting colors/typography the user already defined breaks trust and loses work | Read and preserve existing sections, only add/update Visual Brand Style |
| Generic descriptions like "modern and clean" | Every brand says this — it gives image-gen nothing to work with | Be specific: "warm rim lighting on dark backgrounds, single subject, f/2.0 bokeh" |
| Skipping the Avoid list | What to avoid is often more distinctive than what to include — it prevents the generic | Always ask what the brand should NEVER look like |
| Writing keyword prompts instead of narrative | Image gen models produce better results from flowing descriptions than comma-separated terms | Reference prompts should read like a scene description, not a tag list |

---

## Related Skills

- **/image-gen** — reads the Visual Brand Style this skill creates to generate on-brand images
- **/brand-voice** — builds the verbal identity; visual-style builds the visual identity
- **/creative** — produces multi-mode creative briefs that reference creative-kit.md
- **/paper-marketing** — designs in Paper MCP using creative-kit.md for design system
