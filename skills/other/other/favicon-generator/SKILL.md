---
name: favicon-generator
description: >
  Generate professional-quality favicons that rival the best app icons. Uses a
  multi-layer effects engine with drop shadows, inner glows, highlights, gradients,
  and noise textures. Includes 8 curated design templates and 18 Lucide icons.
  Produces complete favicon suites with proper ICO, SVG, PNG formats and framework
  integration. Trigger when users need favicons, app icons, or browser tab icons.
---

# Pro-Grade Favicon Generator

Create stunning, professional-quality favicons that stand alongside icons from Linear, Notion, Figma, and other polished apps.

## Philosophy: Favicons Are Miniature Design Artifacts

The difference between a mediocre favicon and a great one isn't complexity—it's **polish**. Great favicons have:

- **Depth**: Subtle shadows that lift the icon off the surface
- **Lighting**: Highlights and gradients that create dimensionality  
- **Texture**: Optional noise/grain that adds organic feel
- **Precision**: Optical centering, proper padding, crisp edges

**Before generating, ask yourself**:
1. What's the app's personality? (Playful, professional, technical, creative)
2. What colors define the brand? (Extract from tailwind config, CSS, or ask)
3. What level of polish is needed? (Quick prototype vs. production launch)

---

## Workflow: Discover Existing Icons First

**CRITICAL**: Before generating a favicon, always check what icons are already used in the codebase. The favicon should match your existing brand identity.

### Step 1: Search for Icon Usage

Search the codebase for icon imports and usage:

```bash
# Find lucide-react imports
rg "from.*lucide-react" --type tsx --type ts

# Find icon component usage
rg "PackagePlus|Package|Icon" --type tsx --type ts

# Check Header/Nav components (common icon locations)
rg "Header|Nav|Logo" --type tsx
```

### Step 2: Identify Primary Brand Icons

Look for:
- **Logo icons**: Used in Header, navigation, or branding components
- **Most frequently used icons**: Appear in multiple places
- **Icon libraries**: lucide-react, react-icons, custom SVG components

Example discovery:
```
Found in Header.tsx: PackagePlus from lucide-react
Found in HomePage.tsx: PackagePlus, Package
Primary brand icon: PackagePlus (used in logo/branding)
```

### Step 3: Extract Icon Paths

If using lucide-react or similar libraries:

1. **Locate icon definition**:
   ```bash
   cat node_modules/lucide-react/dist/esm/icons/package-plus.js
   ```

2. **Extract SVG paths** from the icon definition:
   - Lucide icons use 24x24 viewBox
   - Paths are defined as arrays: `["path", { d: "M..." }]`
   - Copy the exact `d` attributes from each path

3. **Use cairosvg for accurate rendering** (recommended):
   ```bash
   pip install cairosvg
   brew install cairo  # macOS - required native library
   ```
   
   **Why cairosvg?** Pillow cannot render SVG bezier curves and arcs. Lucide icons
   use arc commands (`a2 2 0 0 0...`) that only a proper SVG renderer can draw.

### Step 4: Match Favicon to Brand Icon

- **Same icon**: Use the exact icon from your brand (e.g., PackagePlus → PackagePlus favicon)
- **Same colors**: Extract brand colors from Tailwind config or CSS variables
- **Same style**: Match the visual style (minimal, vibrant, etc.)

### Example: PackagePlus Favicon with cairosvg

```python
import cairosvg
from PIL import Image
from io import BytesIO

# Actual Lucide PackagePlus paths (from node_modules/lucide-react/dist/esm/icons/package-plus.js)
SVG_TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f97316"/>
      <stop offset="100%" stop-color="#ef4444"/>
    </linearGradient>
  </defs>
  <rect width="{size}" height="{size}" rx="{radius}" fill="url(#bg)"/>
  <g transform="translate({offset}, {offset}) scale({scale})" 
     stroke="#ffffff" stroke-width="2" fill="none" 
     stroke-linecap="round" stroke-linejoin="round">
    <!-- Exact Lucide PackagePlus paths -->
    <path d="M16 16h6"/>
    <path d="M19 13v6"/>
    <path d="M21 10V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l2-1.14"/>
    <path d="m7.5 4.27 9 5.15"/>
    <polyline points="3.29 7 12 12 20.71 7"/>
    <line x1="12" x2="12" y1="22" y2="12"/>
  </g>
</svg>"""

def render_lucide_icon(size):
    # Lucide uses 24x24, scale to fit in favicon with padding
    scale = (size * 0.7) / 24
    offset = size * 0.15
    radius = int(size * 0.22)
    
    svg = SVG_TEMPLATE.format(size=size, scale=scale, offset=offset, radius=radius)
    png_data = cairosvg.svg2png(bytestring=svg.encode('utf-8'))
    return Image.open(BytesIO(png_data)).convert('RGBA')
```

### Why This Matters

- **Consistency**: Favicon matches your app's visual identity
- **Brand recognition**: Users recognize your icon across contexts
- **Professionalism**: Shows attention to detail and design coherence
- **Avoids mismatch**: Prevents generating a favicon that doesn't match your actual logo

---

### The Effects Stack

Professional favicons are built in **layers**, not drawn flat:

```
┌─────────────────────────────────────┐
│  Layer 6: Content (letter/icon)    │ ← With its own shadow
│  Layer 5: Noise texture            │ ← Subtle grain for organic feel
│  Layer 4: Highlight gradient       │ ← Top-lit shine effect
│  Layer 3: Inner glow               │ ← Ambient light/shadow
│  Layer 2: Background               │ ← Gradient or solid
│  Layer 1: Drop shadow              │ ← Depth and lift
└─────────────────────────────────────┘
```

Each layer is subtle. Combined, they create polish that's felt rather than seen.

---

## Generation Tools

This skill provides two complementary tools:

### Tool 1: Interactive HTML Generator
**File**: `scripts/generate_favicon_pro.html`

Open in browser for real-time preview and customization:
- 8 professional design templates
- 18 Lucide icons + letter/emoji modes
- Live effect adjustment (shadow, glow, highlight, noise)
- All sizes preview (16px to 512px)
- Context preview (browser tab, bookmarks)
- Bulk download

**Best for**: Quick iteration, visual exploration, client demos

### Tool 2: Python CLI Pipeline  
**File**: `scripts/generate_favicon.py`

Command-line generation with Pillow:
```bash
# Using a template
python generate_favicon.py --letter A --style vibrant --output ./public/

# Custom colors
python generate_favicon.py --letter T --bg "#22c55e" --bg2 "#14b8a6" --output ./favicons/

# Full control
python generate_favicon.py --letter N --bg "#0f172a" --fg "#22d3ee" \
  --shadow 0.6 --glow 0.5 --noise 0.04 --output ./icons/
```

**Best for**: CI/CD integration, batch generation, precise control

---

## Design Templates

Choose a template that matches the app's personality:

| Template | Colors | Character | Best For |
|----------|--------|-----------|----------|
| **Modern** | Indigo → Purple | Clean, trustworthy | SaaS, productivity |
| **Vibrant** | Pink → Orange | Energetic, bold | Consumer apps, social |
| **Minimal** | Near-black | Understated, technical | Dev tools, utilities |
| **Glass** | Blue → Cyan | Airy, modern | Dashboards, analytics |
| **Neon** | Dark + Cyan glow | Futuristic, edgy | Gaming, creative tools |
| **Warm** | Amber → Red | Friendly, approachable | Food, lifestyle, community |
| **Forest** | Green → Teal | Natural, sustainable | Health, environment, finance |
| **Mono** | White + Black | Minimal, adaptable | Any (works in any context) |

### Template Selection Guide

```
App personality assessment:
├── Professional/Enterprise → Minimal, Modern, Mono
├── Consumer/Fun → Vibrant, Warm, Neon
├── Technical/Developer → Minimal, Glass, Neon
├── Health/Wellness → Forest, Warm
└── Creative/Design → Vibrant, Glass, Modern
```

---

## Content Types

### 1. Letter/Monogram (Default)
Single letter or two-letter combination from app name.

```
"TaskFlow" → "T" or "TF"
"Acme Corp" → "A" or "AC"
```

**Typography considerations**:
- Single letters work better at small sizes
- Choose distinctive letters (avoid O, I which lack character)
- Font weight matters—bold reads better at 16px

### 2. Icons (Lucide Integration)
18 curated Lucide icons for common app types:

| Icon | Use Case |
|------|----------|
| `rocket` | Startups, launch, speed |
| `zap` | Performance, automation |
| `star` | Favorites, ratings, premium |
| `heart` | Health, favorites, social |
| `code` | Developer tools, IDEs |
| `box` | Packages, containers, storage |
| `compass` | Navigation, exploration |
| `flame` | Trending, hot, energy |
| `globe` | International, web, browser |
| `layers` | Design, stacks, organization |
| `music` | Audio, media, entertainment |
| `send` | Messaging, communication |
| `shield` | Security, protection, trust |
| `sparkles` | AI, magic, premium |
| `sun` | Light mode, energy, positivity |
| `target` | Goals, focus, precision |
| `terminal` | CLI, developer, technical |
| `wand` | Magic, automation, creative |

### 3. Emoji
Native emoji for playful, informal apps.

```
🚀 → Launch, speed, startups
💡 → Ideas, innovation
🔥 → Trending, hot
✨ → Premium, magic
```

**Note**: Emoji rendering varies by OS—test on multiple platforms.

---

## Effects Reference

### Drop Shadow
Creates depth and lift. Essential for polished look.

| Intensity | Effect | Use When |
|-----------|--------|----------|
| 0.2–0.3 | Subtle | Minimal designs, light backgrounds |
| 0.4–0.5 | Balanced | Most apps (default) |
| 0.6+ | Strong | Dark backgrounds, high contrast |

### Highlight
Top-lit gradient that adds dimensionality.

| Intensity | Effect | Use When |
|-----------|--------|----------|
| 0.15–0.25 | Gentle | Subtle polish |
| 0.3–0.4 | Pronounced | Glass, vibrant styles |
| 0.5+ | Strong | Glossy, skeuomorphic look |

### Inner Glow
Radial lighting from center, creates depth.

| Intensity | Effect | Use When |
|-----------|--------|----------|
| 0.2–0.3 | Soft ambient | Glass style |
| 0.4–0.5 | Noticeable | Neon, futuristic |
| 0.6+ | Strong | Glowing effect |

### Noise/Grain
Subtle texture that prevents banding and adds organic feel.

| Intensity | Effect | Use When |
|-----------|--------|----------|
| 0.03–0.05 | Barely visible | Anti-banding only |
| 0.06–0.08 | Subtle texture | Organic, natural feel |
| 0.1+ | Visible grain | Vintage, film aesthetic |

### Corner Radius
Shape of the icon background.

| Value | Shape | Platform |
|-------|-------|----------|
| 0.15–0.18 | Squircle | iOS-like |
| 0.20–0.24 | Rounded | Modern default |
| 0.30+ | Very round | Playful, bubble |
| 0.50 | Circle | Circular icons |

---

## Output Structure

### Standard Suite (Default)
```
public/
├── favicon.ico          # Legacy (16+32 combined)
├── favicon.svg          # Modern browsers (scalable)
├── favicon-16x16.png    # Browser tabs
├── favicon-32x32.png    # Browser tabs (retina)
├── favicon-48x48.png    # Windows tiles
├── favicon-64x64.png    # Windows tiles
├── favicon-128x128.png  # Chrome Web Store
├── apple-touch-icon.png # iOS home screen (180x180)
├── favicon-192x192.png  # Android Chrome
└── favicon-512x512.png  # PWA, Android
```

### Framework Integration

#### Next.js (App Router)
```typescript
// app/layout.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  icons: {
    icon: [
      { url: '/favicon.ico', sizes: 'any' },
      { url: '/favicon.svg', type: 'image/svg+xml' },
      { url: '/favicon-16x16.png', sizes: '16x16', type: 'image/png' },
      { url: '/favicon-32x32.png', sizes: '32x32', type: 'image/png' },
    ],
    apple: [
      { url: '/apple-touch-icon.png', sizes: '180x180' },
    ],
  },
}
```

#### Standard HTML
```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
```

#### PWA Manifest
```json
{
  "icons": [
    { "src": "/favicon-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/favicon-512x512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

---

## Workflow Examples

### Example 1: New SaaS Product

```
User: "Create a favicon for my project management app called Flowboard"

Claude:
1. [Discovers existing icons]
   - Searches codebase: rg "from.*lucide-react"
   - Finds: Header.tsx uses PackagePlus icon
   - Checks: No existing favicon, but brand uses PackagePlus
   
2. [Analyzes codebase]
   - tailwind.config.ts: primary = "#6366f1"
   - Package name: "flowboard"
   - Brand icon: PackagePlus (from lucide-react)
   
3. [Selects approach]
   - Option A: Match brand icon (PackagePlus) → Extract paths from lucide-react
   - Option B: Use letter "F" (distinctive, good at small sizes)
   - Decision: Use PackagePlus to match brand identity
   - Style: "Modern" (professional SaaS)
   - Colors: Use brand indigo
   
4. [Extracts icon paths]
   - Reads: node_modules/lucide-react/dist/esm/icons/package-plus.js
   - Extracts SVG paths and converts 24x24 → 32x32
   
5. [Generates with Python script]
   python generate_packageplus_favicon.py --output ./public/
   
6. [Integrates with Next.js]
   Updates app/layout.tsx with metadata.icons
   
7. [Delivers]
   "Created favicon suite matching your PackagePlus brand icon. 
   The favicon now matches your Header logo exactly—check the browser tab preview."
```

### Example 2: Developer Tool

```
User: "Make a favicon for my CLI tool"

Claude:
1. [Discovers existing icons]
   - Searches: rg "Icon|Logo" --type tsx
   - Finds: No existing brand icons, new project
   
2. [Considers personality]
   - Developer audience → technical, minimal
   - CLI context → terminal icon fits well
   
3. [Selects approach]
   - Content: Terminal icon from Lucide (extract actual paths)
   - Style: "Minimal" (dark, understated)
   - Effects: Subtle shadow, slight noise
   
4. [Extracts Terminal icon paths]
   - Reads: node_modules/lucide-react/dist/esm/icons/terminal.js
   - Converts paths to favicon coordinate system
   
5. [Opens HTML generator for preview]
   Shows user the terminal icon in minimal style
   
6. [Adjusts based on feedback]
   User: "Can we make it more techy?"
   → Switches to "Neon" style with cyan glow
   
7. [Generates final suite]
   Downloads all sizes, integrates with project
```

### Example 3: Playful Consumer App

```
User: "I need a fun favicon with a rocket for my startup"

Claude:
1. [Selects approach]
   - Content: Rocket icon (not emoji for consistency)
   - Style: "Vibrant" (pink→orange, energetic)
   - Effects: Strong shadow, highlight, no noise
   
2. [Previews in context]
   Shows browser tab mockup, bookmark bar
   
3. [Generates]
   Full suite with all sizes
   
4. [Delivers with context]
   "Here's your rocket favicon in vibrant colors. The icon 
   stays crisp even at 16px. I've included the apple-touch-icon
   for when users add to their phone home screen."
```

---

## Anti-Patterns

❌ **Flat, shadowless designs**
```
Problem: Icon looks pasted on, no depth
Fix: Add at least 0.3 shadow intensity
```

❌ **Over-complicated at small sizes**
```
Problem: 16px version is unrecognizable mush
Fix: Test at actual 16px—simplify if needed
```

❌ **Generic blue gradient**
```
Problem: Looks like every other AI-generated icon
Fix: Use brand colors, vary the template
```

❌ **Ignoring the effects stack**
```
Problem: Just background + letter, looks amateur
Fix: Apply shadow + highlight at minimum
```

❌ **Wrong template for context**
```
Problem: Neon style for a healthcare app
Fix: Match template to brand personality
```

❌ **Skipping the preview step**
```
Problem: Looks good at 512px, bad at 16px
Fix: Always check size previews before finalizing
```

❌ **Not testing in context**
```
Problem: Colors clash with browser chrome
Fix: Use context preview (tab, bookmarks)
```

---

## Variation Guidance

**CRITICAL**: Each favicon should feel custom, not templated.

**Vary by app type**:
- Dev tools → Terminal icon, Minimal/Neon style, dark colors
- Consumer apps → Vibrant icons, warm colors, playful shapes
- Enterprise → Letter monogram, Modern/Mono style, brand colors
- Creative tools → Abstract shapes, Glass style, unique gradients

**Vary the effects**:
- Don't always use the same shadow intensity
- Try different corner radii
- Experiment with inner glow for certain styles
- Add noise for organic apps, skip for technical ones

**Vary the content**:
- Not every app needs a letter
- Icons can be more memorable than letters
- Consider the app's core action (send, shield, target)

---

## Quick Reference

### Python CLI
```bash
# Basic
python generate_favicon.py --letter A --output ./public/

# With template
python generate_favicon.py --letter T --style vibrant --output ./public/

# Custom colors
python generate_favicon.py --letter N --bg "#0f172a" --bg2 "#1e293b" \
  --fg "#22d3ee" --output ./public/

# Full control
python generate_favicon.py --letter M \
  --bg "#ec4899" --bg2 "#f97316" --fg "#ffffff" \
  --shadow 0.5 --highlight 0.3 --glow 0.2 --noise 0.05 \
  --radius 0.24 --output ./public/
```

### Available Templates
`modern`, `vibrant`, `minimal`, `glass`, `neon`, `warm`, `forest`, `mono`

### Available Icons
`rocket`, `zap`, `star`, `heart`, `code`, `box`, `compass`, `flame`, `globe`, `layers`, `music`, `send`, `shield`, `sparkles`, `sun`, `target`, `terminal`, `wand`

### Effect Ranges
- Shadow: 0.0–1.0 (default: 0.4)
- Highlight: 0.0–1.0 (default: 0.25)
- Inner Glow: 0.0–1.0 (default: 0.0)
- Noise: 0.0–1.0 (default: 0.0)
- Corner Radius: 0.0–0.5 (default: 0.22)

---

## Remember

**Great favicons are felt, not analyzed.** Users don't consciously notice the drop shadow or the highlight gradient—they just sense that the icon feels professional and polished.

The difference between amateur and professional is:
1. **Layered effects** vs. flat rendering
2. **Considered templates** vs. random colors
3. **Size-appropriate detail** vs. complexity that muddies
4. **Tested in context** vs. only viewed at full size

Use the tools to handle the technical complexity. Focus your energy on choosing the right personality, colors, and content for the specific app.
