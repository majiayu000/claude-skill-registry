---
name: wiggle
description: Create animated logo files (Lottie JSON, GIF, MP4) from static logo images. This skill should be used when users provide a logo image (PNG/SVG/JPG) and request any kind of logo animation, motion graphics, animated logo effect, waveform animation, bouncing logo, rotating logo, pulsing logo, wiggling logo, or ask to "animate my logo" or "make my logo move". Outputs standalone animation files (not React/HTML artifacts). Generates Lottie JSON with automatic GIF/MP4 rendering, perfect loop validation, and professional motion design patterns.
license: Complete terms in LICENSE.txt
---

# Wiggle Logo Animator

Create professional logo animations using Lottie JSON format. Ingest existing logos (PNG/SVG/JPG) or generate simple text-based logos, then animate them with professionally-crafted motion patterns. Output includes Lottie JSON with automatic GIF preview rendering and optional MP4 export.

## When to Use This Skill

Trigger this skill when users request:
- "Animate my logo" / "Create a logo animation"
- "Make my logo wiggle/bounce/rotate/pulse"
- "Animated waveform effect for my logo"
- "Motion graphics for my brand logo"
- "Lottie animation for my brand"
- Logo entrance, loop, or loading animations
- Any animation effect applied to a provided logo image

**Important**: This skill outputs standalone animation files (Lottie JSON, GIF, MP4), NOT interactive React/HTML artifacts. If user wants an interactive tool or web component, defer to artifacts-builder skill.

---

## Core Workflow

### 1. Define Motion Philosophy (30 seconds - MANDATORY!)

**Before creating any animation**, answer these three questions:

1. **What personality does this brand have?**
   (playful, professional, bold, elegant, innovative, trustworthy)

2. **What emotion should the animation evoke?**
   (excitement, trust, creativity, confidence, curiosity)

3. **What motion metaphor fits?**
   (organic growth, mechanical precision, energetic burst, elegant reveal, rhythmic pulse)

**Example:**
"Canva = Creative tool brand → Playful energy + organic growth → Simultaneous entrance with pulse"

See [Animation Philosophy](#animation-philosophy) section below for detailed framework.

---

### 2. Analyze Logo Structure (30 seconds - MANDATORY!)

**Before creating animation**, understand what you're working with:

```bash
# For SVG logos - identify elements
python scripts/extract_svg_elements.py logo.svg --list
```

**Quick decision tree:**

```
Logo has text?
  ├─ YES → Read references/text_animation_guide.md FIRST
  └─ NO  → Continue with standard workflow

Multiple elements (icon + text)?
  ├─ YES → Extract separately, decide timing (simultaneous vs staggered)
  └─ NO  → Animate as single unit

SVG or PNG?
  ├─ SVG → Can extract elements cleanly
  └─ PNG → Limited to single-logo animations
```

---

### 3. Prepare Assets

```bash
# Single logo (simple animation)
python scripts/prepare_logo.py logo.png --max-size 500 --optimize
# Creates: logo_optimized.png (30-50KB) + logo_base64.txt

# Multi-element logo (extract FIRST, then convert)
python scripts/extract_svg_elements.py logo.svg --output-dir ./elements/
python scripts/prepare_logo.py elements/icon.svg --max-size 200
python scripts/prepare_logo.py elements/text.svg --max-size 250
```

**Size guidelines:**
- Full logo (single): 500-600px
- Icon elements: 100-200px
- Text elements: 200-300px

---

### 4. Create Lottie JSON Animation

**Use EXTERNAL references during development:**

```json
{
  "v": "5.7.4",
  "fr": 60,
  "ip": 0,
  "op": 180,
  "w": 800,
  "h": 800,
  "layers": [{
    "ind": 1,
    "ty": 2,
    "nm": "Logo",
    "refId": "logo_image",
    "ks": {
      "o": {
        "a": 1,
        "k": [
          {"t": 0, "s": [0], "e": [100], "i": {"x": [0.42], "y": [1]}, "o": {"x": [0.58], "y": [0]}},
          {"t": 60, "s": [100]}
        ]
      }
    }
  }],
  "assets": [{"id": "logo_image", "w": 512, "h": 512, "p": "logo_optimized.png", "e": 0}]
}
```

**Critical:** Use `"e": 0` (external reference) during development to avoid Cairo memory errors.

See [Animation Patterns](#animation-pattern-quick-reference) below for common effects, or [references/detailed_examples.md](references/detailed_examples.md) for full code examples.

---

### 5. Validate

```bash
# Check Lottie structure (warns about large embedded assets)
python scripts/validate_lottie.py logo_animation.json

# Check loop quality (if creating looping animation)
python scripts/validate_loop.py logo_animation.json
```

---

### 6. Render

```bash
# RECOMMENDED: Preview first (renders only first N frames) - saves time!
python scripts/render_lottie.py logo_animation.json preview.gif --preview-frames 60

# Alternative: Test render mode (200x200, 15fps with confirmation prompt)
python scripts/render_lottie.py logo_animation.json logo.gif --test-render

# If preview looks good → Render full animation
python scripts/render_lottie.py logo_animation.json logo.gif

# Optional: MP4 export (better compression than GIF)
python scripts/render_lottie.py logo_animation.json logo.mp4

# Optional: Batch export all formats
python scripts/batch_export.py logo_animation.json ./output gif,mp4,json
```

**Important notes:**
- Assets are resolved **relative to the Lottie JSON file location** (not current working directory)
- Asset validation runs automatically before rendering
- Output verification detects blank/corrupted files
- Use `--preview-frames N` to render only first N frames for quick validation

---

### 7. Optional: Embed for Distribution

**After successful rendering**, optionally convert to embedded base64 for standalone distribution:

```json
// Replace external reference with base64 from logo_base64.txt
"assets": [{"id": "logo_image", "p": "data:image/png;base64,...", "e": 1}]
```

**Note:** Keep external version for future edits/rendering!

---

## Animation Philosophy

### The Two-Phase Approach

**Phase 1: Define Philosophy** (think before implementing)

1. What personality does this brand have?
2. What emotion should the animation evoke?
3. What motion metaphor fits?

**Phase 2: Express Through Technical Choices**

- **Choose properties** that express philosophy (position/scale/rotation/opacity)
- **Select easing** that matches personality (ease-out=confident, bounce=playful)
- **Set timing** that aligns with emotion (fast=energetic, slow=elegant)

### Philosophy Examples

**"Confident Professionalism"**
- Philosophy: Trustworthy, established, competent
- Expression: Slow ease-out fade (0→100% opacity) + gentle scale (95%→100%)
- Timing: 2s duration, no overshoot
- Example: [references/real-world-examples/slack-hover-pinch.json](references/real-world-examples/slack-hover-pinch.json)

**"Playful Energy"**
- Philosophy: Fun, approachable, memorable
- Expression: Bounce entrance with overshoot
- Timing: 1s duration, back easing (0.6/-0.28)
- Example: [references/real-world-examples/reddit-hover-pinch.json](references/real-world-examples/reddit-hover-pinch.json)

**"Audio/Speech Brand"**
- Philosophy: Sound, rhythm, waveforms, dynamic
- Expression: Vertical waveform with dense keyframes (30-45 keyframes, 60fps)
- Timing: 3s loop, organic easing (0.25/0.75)
- **Critical:** See "Organic/Continuous Motion" in Motion Types section below

More examples in [references/preset_library.md](references/preset_library.md) and [references/animation_theory.md](references/animation_theory.md).

---

## Motion Type Quick Reference

Choose motion type based on brand personality:

### Static/Corporate Motion
Professional brands (B2B, finance, legal)

**Parameters:**
- Keyframes: 8-12 (sparse, deliberate)
- Easing: `0.42/0.58` (standard ease-in-out)
- FPS: 30
- Duration: 1.5-2s

**Use for:** Corporate logos, B2B brands, professional presentations

---

### Organic/Continuous Motion
Audio, music, speech AI, nature brands

**Parameters:**
- Keyframes: 25-45 ← **Critical for smoothness**
- Easing: `0.25/0.75` (softer, more organic)
- FPS: 60 ← **Essential for fluidity**
- Duration: 3s

**Use for:** Audio apps, music platforms, speech AI, organic products

**Example:** Vertical bar waveform pattern in [references/detailed_examples.md](references/detailed_examples.md#7-vertical-bar-waveform-organic-motion)

---

### Bold/Attention-Grabbing
Startups, social media, marketing

**Parameters:**
- Keyframes: 15-25
- Easing: `0.34/1.56` (playful bounce) or `0.6/-0.28` (back overshoot)
- FPS: 60
- Duration: 0.8-1.5s

**Use for:** Startup logos, social media intros, marketing campaigns

---

### Cinematic/Complex
Premium brands, film production

**Parameters:**
- Keyframes: 50-120
- Easing: Custom bezier curves, variable timing
- FPS: 60-120
- Duration: 3-5s

**Use for:** Luxury brands, film intros, high-end agency work

---

## Animation Pattern Quick Reference

### Single-Element Patterns

| Pattern | Duration | Properties | Use Case |
|---------|----------|------------|----------|
| **Fade + Gentle Scale** | 1.5s | Opacity: 0→100%, Scale: 95→100% | Corporate entrances |
| **Bounce Entrance** | 1.2s | Position, Scale, Opacity | Energetic brands |
| **Scale Pulse** | 3s loop | Scale: 100→103→100% | Idle states, CTAs |
| **Smooth Rotation** | 10s loop | Rotation: 0→360° | Loading, tech logos |
| **Wiggle/Jello** | 0.8s | Rotation: ±5° oscillation | Playful notifications |

**Full code examples:** [references/detailed_examples.md](references/detailed_examples.md)

---

### Multi-Element Coordination

**Pattern 1: Simultaneous Entrance**
Both elements appear together (cohesive brand)

```json
Icon: {"t": 0, "s": [0]}, {"t": 60, "s": [100]}
Text: {"t": 0, "s": [0]}, {"t": 60, "s": [100]}
// Both start at t:0 → Synchronized
```

**Pattern 2: Staggered Entrance**
Icon establishes first, text reinforces (storytelling)

```json
Icon: {"t": 0, "s": [0]}, {"t": 45, "s": [100]}
Text: {"t": 30, "s": [0]}, {"t": 75, "s": [100]}
// Text delayed 30 frames (0.5s at 60fps)
```

**Timing guidelines:**
- 15 frames (0.25s): Subtle stagger
- 30 frames (0.5s): Noticeable sequence ← Most common
- 45 frames (0.75s): Dramatic two-act reveal

**Full patterns:** [references/detailed_examples.md#multi-element-coordination](references/detailed_examples.md#multi-element-coordination)

---

## User Intent Classification

Always classify user intent to select appropriate animation style:

| Intent | Keyframes | Easing | FPS | Duration | Motion |
|--------|-----------|--------|-----|----------|--------|
| **Subtle/Professional** | 8-12 | 0.42/0.58 | 30 | 1.5-2s | Slow, controlled, minimal rotation |
| **Bold/Attention** | 15-25 | 0.34/1.56 | 60 | 0.8-1.5s | Medium-fast, dynamic, ±10-20% scale |
| **Playful/Creative** | 12-20 | 0.34/1.56 | 30-60 | 1-2s | Bouncy, exaggerated, wiggle effects |
| **Organic/Continuous** | 25-45 | 0.25/0.75 | 60 | 3s | Waveforms, pulses, flowing rhythms |

**Default:** Provide animation rather than asking questions, unless user explicitly requests options.

---

## Known Limitations

### Asset Path Resolution

**Current behavior:**
- External assets (PNGs/SVGs) are resolved **relative to the Lottie JSON file location**
- The renderer changes the working directory to the JSON file's directory during rendering
- Asset validation runs automatically before rendering begins

**Example:**
```
project/
├── animations/
│   └── logo_animation.json  (references "logo_optimized.png")
└── logo_optimized.png

# This will FAIL - asset not found
```

**Solution:** Place assets in the same directory as the JSON file:
```
project/animations/
├── logo_animation.json
└── logo_optimized.png  # ✅ Correct location
```

### Embedded Base64 vs External References

**Embedded base64** (`"e": 1`):
- **Pros:** Standalone file, easy distribution
- **Cons:** Cairo MemoryError for images >100KB, larger file sizes, not editable

**External references** (`"e": 0`):
- **Pros:** No memory issues, smaller JSON files, easy to update assets
- **Cons:** Requires keeping asset files alongside JSON

**Recommended workflow:**
1. Use external references during development/rendering
2. Optionally embed base64 AFTER successful rendering for distribution
3. Keep external version for future edits

---

## Critical Warnings

### ❌ Common Mistakes to Avoid

1. **Creating animation before defining philosophy** → Random trial-and-error wastes 15-30 minutes
2. **Using PIL ImageDraw to recreate logo text** → Creates DIFFERENT text, not your logo text
3. **Embedding base64 before rendering** → Cairo MemoryError crash (images >100KB)
4. **Using 1000px for small elements** → Huge files (400KB+), memory issues
5. **Skipping logo analysis** → Wrong workflow, have to restart
6. **Forgetting loop validation** → Visible jump when animation loops
7. **Skipping preview renders** → Waste time on full renders before validating concept
8. **Rendering full SVG then cropping** → Fuzzy edges, massive file sizes

**Full list with code examples:** [references/anti_patterns.md](references/anti_patterns.md)

---

### ⚠️ Text in Logos - CRITICAL

**If logo contains text**, you MUST follow specialized workflow:

1. **Extract text from logo SVG** (do NOT recreate with PIL ImageDraw)
2. **Choose appropriate text animation method** (fade/stroke/transform)
3. **Implement proper synchronization** with other elements

**See:** [references/text_animation_guide.md](references/text_animation_guide.md) for complete guide

---

### ⚠️ External References Required

**Always use external file references during development/rendering:**

```json
// ✅ CORRECT: External reference
"assets": [{"id": "logo", "p": "logo_optimized.png", "e": 0}]

// ❌ WRONG: Embedded base64 (causes Cairo crash if >100KB)
"assets": [{"id": "logo", "p": "data:image/png;base64,...", "e": 1}]
```

**Why:** Cairo renderer crashes with embedded images >100KB. Use external during development, optionally embed AFTER successful rendering.

---

## Helper Scripts Quick Reference

| Script | Purpose | Example |
|--------|---------|---------|
| `prepare_logo.py` | Optimize and convert logo images | `python scripts/prepare_logo.py logo.png --max-size 500` |
| `extract_svg_elements.py` | Extract elements from SVG | `python scripts/extract_svg_elements.py logo.svg --list` |
| `validate_lottie.py` | Check Lottie structure | `python scripts/validate_lottie.py animation.json` |
| `validate_loop.py` | Verify perfect loop | `python scripts/validate_loop.py animation.json` |
| `render_lottie.py` | Render to GIF/MP4 (with asset validation) | `python scripts/render_lottie.py animation.json output.gif` |
| `render_lottie.py --preview-frames N` | Quick preview (first N frames) | `python scripts/render_lottie.py animation.json preview.gif --preview-frames 60` |
| `render_lottie.py --test-render` | Test mode with size warnings | `python scripts/render_lottie.py animation.json test.gif --test-render` |
| `batch_export.py` | Export multiple formats | `python scripts/batch_export.py animation.json ./output gif,mp4` |

**New features in render_lottie.py:**
- ✅ Automatic asset validation (checks for missing external files)
- ✅ Asset path resolution (relative to JSON file location)
- ✅ Output verification (detects blank/corrupted files)
- ✅ Preview mode (`--preview-frames N`) - renders only first N frames
- ✅ Test mode (`--test-render`) - small test render with confirmation prompt

**Detailed usage:** [references/script_usage.md](references/script_usage.md)

---

## Lottie JSON Fundamentals

### Basic Structure

```json
{
  "v": "5.7.4",           // Lottie version
  "fr": 60,               // Frame rate
  "ip": 0,                // In point (start frame)
  "op": 180,              // Out point (end frame)
  "w": 800,               // Width
  "h": 800,               // Height
  "layers": [...],        // Animation layers
  "assets": [...]         // Image/asset references
}
```

### Layer Types

- **Type 2 (Image Layer):** Most common - animates PNG/SVG images
- **Type 4 (Shape Layer):** Programmatic geometry (circles, rectangles, paths)

### Animated Properties

- **`o`:** Opacity (0-100)
- **`p`:** Position [x, y]
- **`s`:** Scale [x%, y%]
- **`r`:** Rotation (degrees)
- **`a`:** Anchor point [x, y]

### Keyframe Structure

```json
"o": {
  "a": 1,  // Animated (1) or static (0)
  "k": [
    {"t": 0, "s": [0], "e": [100], "i": {...}, "o": {...}},
    {"t": 60, "s": [100]}
  ]
}
```

- **`t`:** Time (frame number)
- **`s`:** Start value
- **`e`:** End value
- **`i`:** In tangent (ease in)
- **`o`:** Out tangent (ease out)

**Complete specification:** [references/lottie_spec.md](references/lottie_spec.md)

---

## Easing Functions

**Never use linear easing** - always use curves for professional motion.

| Easing | Values | Feel | Use Case |
|--------|--------|------|----------|
| **Ease-in-out (standard)** | `0.42/0.58` | Balanced, professional | Corporate, general use |
| **Organic** | `0.25/0.75` | Soft, natural | Audio brands, waveforms, continuous motion |
| **Bounce** | `0.34/1.56` | Playful, energetic | Startups, playful brands |
| **Back** | `0.6/-0.28` & `0.735/0.045` | Overshoot, dynamic | Bold marketing, attention-grabbing |

**Theory and examples:** [references/animation_theory.md](references/animation_theory.md)

---

## Dependencies

### Required
```bash
pip install lottie[all]    # Lottie manipulation
pip install Pillow         # Image processing
pip install pycairo        # Cairo rendering (for GIF)
```

### Cairo Installation

**macOS:**
```bash
brew install cairo pkg-config
pip install pycairo
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libcairo2-dev pkg-config python3-dev
pip install pycairo
```

**Verify:**
```bash
python3 -c "import cairo; print('Cairo OK')"
```

**Troubleshooting:** [references/troubleshooting.md#cairo-and-dependencies](references/troubleshooting.md#cairo-and-dependencies)

---

## Troubleshooting

### Quick Fixes

**Asset not found errors:**
- **Cause:** Assets not in same directory as Lottie JSON
- **Fix:** Move assets to JSON file's directory, or use absolute paths
- **Validation:** Run `render_lottie.py` - it validates assets before rendering

**Blank/corrupted output:**
- **Cause:** Missing assets, wrong paths, or rendering errors
- **Fix:** Check asset validation messages, verify file sizes (output <1KB indicates failure)
- **Detection:** Output verification runs automatically after rendering

**MemoryError during GIF rendering:**
- **Cause:** Embedded base64 images >100KB
- **Fix:** Use external reference (`"e": 0`) instead

**Loop has visible jump:**
- **Cause:** Last keyframe doesn't match first
- **Fix:** Run `validate_loop.py` and ensure last frame = first frame

**Text looks wrong:**
- **Cause:** Used PIL ImageDraw to recreate text
- **Fix:** Extract text from logo SVG with `extract_svg_elements.py`

**Animation too choppy:**
- **Cause:** Too few keyframes or wrong FPS
- **Fix:** Add keyframes (25-45 for organic motion), use 60fps for continuous motion

**Preview renders save time:**
- **Tip:** Use `--preview-frames 60` to validate concept before full render
- **Tip:** Use `--test-render` for interactive testing with size warnings

**Comprehensive guide:** [references/troubleshooting.md](references/troubleshooting.md)

---

## Advanced References

### Detailed Documentation

- **[references/detailed_examples.md](references/detailed_examples.md)** - Full Lottie JSON code for all patterns
- **[references/animation_theory.md](references/animation_theory.md)** - Motion design principles and easing theory
- **[references/preset_library.md](references/preset_library.md)** - Complete preset collection with real-world examples
- **[references/lottie_spec.md](references/lottie_spec.md)** - Lottie JSON specification details
- **[references/script_usage.md](references/script_usage.md)** - Complete script documentation
- **[references/text_animation_guide.md](references/text_animation_guide.md)** - Specialized text animation workflows
- **[references/anti_patterns.md](references/anti_patterns.md)** - Common mistakes with full code examples
- **[references/troubleshooting.md](references/troubleshooting.md)** - Comprehensive troubleshooting guide
- **[references/real-world-examples/](references/real-world-examples/)** - Production animations from major brands

---

## File Size Guidelines

**Target sizes for different use cases:**

| Use Case | Lottie JSON | GIF | MP4 | Image Assets |
|----------|-------------|-----|-----|--------------|
| Email signature | 20-50KB | 500KB-1MB | 200-500KB | <30KB each |
| Website hero | 30-80KB | 1-3MB | 500KB-1.5MB | <50KB each |
| Social media | 50-150KB | 3-8MB | 1-3MB | <80KB each |
| Splash screen | 30-100KB | 2-5MB | 800KB-2MB | <60KB each |

**Optimization:** Use `scripts/optimize_lottie.py` to reduce file sizes by removing redundant keyframes and rounding values.

---

## Curated Presets

Quick reference to common presets (full code in [references/preset_library.md](references/preset_library.md)):

**Branding Styles:**
- Corporate Subtle - Fade + gentle scale (1.5s)
- Startup Energetic - Bounce + overshoot (1.2s)
- Luxury Elegant - Slow fade + minimal scale (3s)
- Tech Glitch - Digital disruption effect (1s)

**Use Cases:**
- Website Hero - Quick professional entrance (0.8s)
- Email Signature - Subtle loop (3s)
- Social Media Intro - Bold entrance (2s)
- Splash Screen - Brand moment with exit (2.5s)

**Real-World Examples:**
Study hover animations from major brands in [references/real-world-examples/](references/real-world-examples/):
- Reddit - Playful elastic bounce
- Slack - Professional restrained pinch
- Medium - Gentle editorial fade
- Flickr - Camera shutter effect
- Discord - Character wink

---

## Quick Decision Checklist

Before creating animation, verify:

- [ ] Defined motion philosophy (personality + emotion + metaphor)
- [ ] Analyzed logo structure (text? multi-element? SVG or PNG?)
- [ ] Chose correct workflow based on analysis
- [ ] If text present: Read [references/text_animation_guide.md](references/text_animation_guide.md)
- [ ] Using external references (`"e": 0`) during development
- [ ] Element sizes appropriate (500px full logo, 100-250px elements)
- [ ] Selected motion type (Static/Organic/Bold/Cinematic)
- [ ] Chosen timing strategy (simultaneous vs staggered)
- [ ] Will validate with preview render before full render
- [ ] Will run `validate_loop.py` if creating loop

**If all checked → Proceed with confidence ✅**

---

## Tips for Success

1. **Philosophy first** - 30 seconds planning saves 15-30 minutes iteration
2. **Analyze before animating** - Understand logo structure upfront
3. **Preview early, preview often** - Test 30-60 frame versions before full render
4. **External references during development** - Embed base64 only after successful rendering
5. **Match motion to brand** - Corporate ≠ startup ≠ audio brand
6. **Perfect loops matter** - Use `validate_loop.py` to verify
7. **Size elements appropriately** - 100-250px for elements, not 1000px
8. **Extract, don't recreate** - Never use PIL to recreate logo text
9. **Validate before rendering** - Run `validate_lottie.py` and `validate_loop.py`
10. **Read references when stuck** - Detailed docs available for every topic

---

**Remember:** The goal is creating motion that enhances brand identity, not random animation. Philosophy-first workflow ensures alignment from the start.
