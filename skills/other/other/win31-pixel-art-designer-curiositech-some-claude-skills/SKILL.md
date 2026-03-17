---
name: win31-pixel-art-designer
description: Expert in Windows 3.1 era pixel art and graphics. Creates icons, banners, splash screens, and UI assets with authentic 16/256-color palettes, dithering patterns, and Program Manager styling. Activate on 'win31 icons', 'pixel art 90s', 'retro icons', '16-color', 'dithering', 'program manager icons', 'VGA palette'. NOT for modern flat icons, vaporwave art, or high-res illustrations.
allowed-tools: Read,Write,Edit,Bash(convert:*,magick:*),mcp__ideogram__generate_image,mcp__stability-ai__*
category: Design & Creative
tags:
  - pixel-art
  - icons
  - retro
  - windows
  - 90s
  - dithering
pairs-with:
  - skill: windows-3-1-web-designer
    reason: Visual + CSS Win31 experience
  - skill: win31-audio-design
    reason: Complete retro multimedia
  - skill: pixel-art-infographic-creator
    reason: Diagrams and educational graphics
---

# Win31 Pixel Art Designer

Expert in creating authentic Windows 3.1 era pixel art, icons, splash screens, and program banners. Masters 16-color and 256-color VGA palettes, dithering techniques, and the visual vocabulary of early 90s computing.

## When to Use

**Use for:**
- Program Manager-style application icons (32x32, 16x16)
- Splash screens and "About" dialog graphics
- Banner art for Win31-themed applications
- Custom cursor and toolbar graphics
- Converting modern art to authentic retro style
- Understanding color limitations and dithering

**Do NOT use for:**
- CSS/web styling → **windows-3-1-web-designer**
- Modern flat icons → **web-design-expert**
- Vaporwave aesthetic → **vaporwave-glassomorphic-ui-designer**
- High-resolution illustrations → **native-app-designer**

## The Win31 Visual Vocabulary

### Icon Specifications

| Icon Type | Size | Colors | Purpose |
|-----------|------|--------|---------|
| **Large Icon** | 32×32 | 16 colors | Desktop, file manager |
| **Small Icon** | 16×16 | 16 colors | Title bar, taskbar |
| **Shell Icon** | 48×48 | 256 colors | Win3.11/early Win95 |
| **Cursor** | 32×32 | 2 colors (B/W) | Mouse pointers |

### The 16-Color Windows Palette

This is the EXACT palette Windows 3.1 used. Deviation breaks authenticity.

```
┌──────────────────────────────────────────────────────┐
│  Standard 16-Color VGA Palette (Win31)               │
├──────────────────────────────────────────────────────┤
│  #000000  Black         #808080  Dark Gray           │
│  #800000  Dark Red      #FF0000  Red                 │
│  #008000  Dark Green    #00FF00  Green               │
│  #808000  Dark Yellow   #FFFF00  Yellow              │
│  #000080  Dark Blue     #0000FF  Blue                │
│  #800080  Dark Magenta  #FF00FF  Magenta             │
│  #008080  Dark Cyan     #00FFFF  Cyan                │
│  #C0C0C0  Light Gray    #FFFFFF  White               │
└──────────────────────────────────────────────────────┘
```

**Key insight:** #C0C0C0 (Light Gray) is THE system color. It appears everywhere.

### The 256-Color VGA Palette

For richer graphics (splash screens, About dialogs), Win31 supported 256-color mode:

| Range | Purpose |
|-------|---------|
| 0-15 | Standard 16 colors (above) |
| 16-31 | System reserved |
| 32-247 | Application colors (color cube) |
| 248-255 | System reserved |

**The 6×6×6 Color Cube:** For indexes 32-247, colors follow:
- R: 0, 51, 102, 153, 204, 255 (6 levels)
- G: 0, 51, 102, 153, 204, 255 (6 levels)
- B: 0, 51, 102, 153, 204, 255 (6 levels)

## Dithering Patterns

Dithering creates the illusion of more colors using patterns. Win31 used these heavily.

### Common Dithering Patterns

```
50% Checkerboard:     25% Sparse:          75% Dense:
■ □ ■ □               □ □ □ □              ■ ■ ■ □
□ ■ □ ■               □ ■ □ □              ■ ■ □ ■
■ □ ■ □               □ □ □ □              ■ □ ■ ■
□ ■ □ ■               □ □ □ ■              □ ■ ■ ■

Diagonal:             Horizontal Lines:    Vertical Lines:
■ □ □ □               ■ ■ ■ ■              ■ □ ■ □
□ ■ □ □               □ □ □ □              ■ □ ■ □
□ □ ■ □               ■ ■ ■ ■              ■ □ ■ □
□ □ □ ■               □ □ □ □              ■ □ ■ □
```

### When to Use Dithering

| Scenario | Pattern | Colors |
|----------|---------|--------|
| Smooth gradients | Ordered dithering | 16 colors |
| Shadow areas | 50% checkerboard | Black + Dark Gray |
| Highlights | 25% sparse | White + Light Gray |
| Sky/backgrounds | Horizontal bands | Blue tones |
| Metal surfaces | Diagonal | Gray tones |

### CSS Dithering Pattern

```css
/* Classic Win31 checkerboard dither in CSS */
.win31-dither {
  background-image: url("data:image/svg+xml,%3Csvg width='4' height='4' viewBox='0 0 4 4' xmlns='http://www.w3.org/2000/svg'%3E%3Crect x='0' y='0' width='2' height='2' fill='%23808080'/%3E%3Crect x='2' y='2' width='2' height='2' fill='%23808080'/%3E%3C/svg%3E");
  background-size: 4px 4px;
}
```

## Icon Design Guidelines

### Anatomy of a Win31 Icon

```
┌──────────────────────────────────────────┐
│          32×32 Icon Anatomy              │
├──────────────────────────────────────────┤
│                                          │
│  ┌─ Light source from top-left           │
│  │                                       │
│  │   ████████████████                    │
│  │   █ Highlight edge █░                 │
│  │   █                █░                 │
│  │   █   SUBJECT      █░ ← Shadow edge   │
│  │   █                █░                 │
│  │   █████████████████░                  │
│  │    ░░░░░░░░░░░░░░░░░                  │
│  │        ↑                              │
│  │    Drop shadow (optional)             │
│                                          │
└──────────────────────────────────────────┘
```

### Icon Design Rules

1. **Light source**: Always top-left (45°)
2. **Outline**: 1px black outline on all edges
3. **Highlight**: 1px white/light edge on top and left
4. **Shadow**: 1px dark edge on bottom and right
5. **Drop shadow**: Optional 1px offset shadow (50% gray)
6. **Hotspot**: Center the visual mass (not geometric center)

### Subject Matter Guidelines

| Category | Style Notes |
|----------|-------------|
| **Documents** | Folded corner, lined interior |
| **Folders** | Tab on top, open or closed |
| **Applications** | Tool/object representing function |
| **Settings** | Gears, sliders, checkmarks |
| **Hardware** | Simplified silhouette |
| **People** | Bust view, simplified features |

## Splash Screens & Banners

### Typical Win31 Splash Screen

```
┌──────────────────────────────────────────────────────┐
│ ┌──────────────────────────────────────────────────┐ │
│ │ ███████████████████████████████████████████████ │ │
│ │ █                                             █ │ │
│ │ █    ╔═══════════════════════════════╗       █ │ │
│ │ █    ║    PROGRAM NAME v1.0          ║       █ │ │
│ │ █    ╚═══════════════════════════════╝       █ │ │
│ │ █                                             █ │ │
│ │ █         [   Large Icon 64×64   ]           █ │ │
│ │ █                                             █ │ │
│ │ █         Copyright © 1993                   █ │ │
│ │ █         Your Company Name                  █ │ │
│ │ █                                             █ │ │
│ │ ███████████████████████████████████████████████ │ │
│ └──────────────────────────────────────────────────┘ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
└──────────────────────────────────────────────────────┘
```

### Banner Dimensions

| Type | Size | Usage |
|------|------|-------|
| **Splash** | 400×300 or 320×240 | Startup screen |
| **About Box** | 300×200 | Help > About |
| **Setup Banner** | 480×60 | Installer wizard |
| **Toolbar Strip** | 16×(16×N) | Button strip |

### Banner Color Guidelines

| Zone | Colors | Notes |
|------|--------|-------|
| **Background** | #C0C0C0 or Navy gradient | System gray or branded |
| **Text** | Black on gray, White on navy | High contrast |
| **Border** | Beveled (white TL, black BR) | 3D effect |
| **Logo area** | 256 colors max | Central focus |

## Prompt Engineering for AI Image Generation

### For Ideogram/Stability AI

**Icon generation prompt template:**
```
32x32 pixel art icon, Windows 3.1 style, [SUBJECT],
16-color VGA palette, 1px black outline,
beveled 3D effect with highlight top-left and shadow bottom-right,
#C0C0C0 system gray background, clean pixel edges,
no anti-aliasing, no gradients, retro 1990s computer aesthetic
```

**Splash screen prompt template:**
```
Windows 3.1 splash screen, 256-color VGA, [PROGRAM NAME],
centered composition, beveled 3D frame border,
navy blue title bar, system gray #C0C0C0 background,
pixel art style, corporate 1990s software aesthetic,
clean typography, no modern effects, authentic retro feel
```

**Banner graphic prompt template:**
```
Windows 3.1 program banner, 480x60 pixels, [PROGRAM NAME],
horizontal layout, beveled border frame,
16-color palette dominant with 256-color logo area,
retro pixel art typography, 1990s software aesthetic,
sharp pixel edges, no blur, no anti-aliasing
```

### Negative prompts (what to AVOID)

```
modern, flat design, gradients, blur, glow effects,
rounded corners, anti-aliasing, smooth edges,
vaporwave, neon, photorealistic, 3D render,
high resolution, 4K, detailed, complex shading
```

## Tool Recommendations

### Image Generation

| Tool | Best For | Notes |
|------|----------|-------|
| **Ideogram** | Icons, logos | Good at pixel art style |
| **Stability AI** | Larger scenes | Needs more prompting for retro |
| **DALL-E** | Concepts | May need post-processing |

### Post-Processing

| Tool | Purpose |
|------|---------|
| **ImageMagick** | Color reduction, dithering |
| **Aseprite** | Pixel art editing (paid) |
| **Piskel** | Free browser pixel editor |
| **GIMP** | Index color conversion |

### ImageMagick Commands

```bash
# Convert to 16-color palette with dithering
convert input.png -colors 16 -dither FloydSteinberg output.png

# Convert to exact Win31 palette
convert input.png -remap win31-palette.png -dither FloydSteinberg output.png

# Scale up pixel art (nearest neighbor)
convert input.png -filter point -resize 200% output.png

# Add 1px black outline
convert input.png -bordercolor black -border 1 output.png
```

## Anti-Patterns

### Anti-Pattern: Smooth Gradients
**What it looks like**: CSS `linear-gradient()` or airbrushed shading
**Why wrong**: Win31 has NO smooth gradients—only dithered patterns
**Instead**: Use ordered dithering between two solid colors

### Anti-Pattern: Anti-Aliasing
**What it looks like**: Smooth diagonal edges, blended pixels
**Why wrong**: Win31 icons have SHARP stair-stepped edges
**Instead**: Hard pixel edges, visible steps on diagonals

### Anti-Pattern: Too Many Colors
**What it looks like**: Full RGB spectrum, subtle color variations
**Why wrong**: 16-color limit means bold, distinct colors
**Instead**: Stick to the VGA palette, use dithering for in-between

### Anti-Pattern: High Resolution
**What it looks like**: 128×128 or larger "pixel art"
**Why wrong**: Real Win31 icons are 32×32 max
**Instead**: Work at native size, scale up with nearest-neighbor

### Anti-Pattern: Drop Shadows with Blur
**What it looks like**: `box-shadow: 4px 4px 8px rgba(0,0,0,0.3)`
**Why wrong**: Win31 shadows are HARD edge, 1-2px offset
**Instead**: 1px solid #808080 offset by 1px right and down

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│           Win31 Pixel Art Quick Reference           │
├─────────────────────────────────────────────────────┤
│                                                     │
│  COLORS                                             │
│  ├─ System Gray: #C0C0C0 (THE background)          │
│  ├─ Navy: #000080 (title bars, accents)            │
│  ├─ Teal: #008080 (links, highlights)              │
│  └─ 16-color VGA palette ONLY                      │
│                                                     │
│  ICONS                                              │
│  ├─ Large: 32×32, 16 colors                        │
│  ├─ Small: 16×16, 16 colors                        │
│  ├─ Light from top-left                            │
│  └─ 1px black outline required                     │
│                                                     │
│  TECHNIQUE                                          │
│  ├─ NO anti-aliasing                               │
│  ├─ NO gradients (use dithering)                   │
│  ├─ NO blur effects                                │
│  └─ Beveled borders for 3D depth                   │
│                                                     │
│  GENERATION                                         │
│  ├─ AI: "16-color, pixel art, no anti-aliasing"   │
│  ├─ Post: ImageMagick -colors 16 -dither Floyd    │
│  └─ Scale: nearest-neighbor only                   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Integrates With

- **windows-3-1-web-designer** - CSS implementation of Win31 aesthetic
- **win31-audio-design** - Audio to match visual style
- **pixel-art-infographic-creator** - Educational diagrams
- **native-app-designer** - When Win31 styling meets modern apps

---

**Core insight**: Win31 pixel art is about CONSTRAINTS creating character. The 16-color limit, hard edges, and dithering patterns define the aesthetic. Embrace these limits—don't fight them.

**Remember**: Every pixel counts at 32×32. Plan your composition carefully, and let dithering do the work of creating depth and gradients.
