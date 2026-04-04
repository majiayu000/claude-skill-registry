---
name: changelog-infographic
description: Generate beautiful infographic PNG images from Claude Code changelog summaries. Use this skill after changelog-interpreter has generated a user-friendly summary, to create a visual representation that can be saved and shared.
---

# Changelog Infographic Skill

This skill transforms changelog summaries into visually stunning infographic PNG images. It receives structured changelog information from the `changelog-interpreter` skill and produces museum-quality visual artifacts.

## When to Use

- After `changelog-interpreter` has generated a summary
- When user requests a visual representation of changes
- When user asks "Create an infographic" or "Visualize the changelog"
- When sharing changelog updates externally

## Input

Structured changelog summary from `changelog-interpreter`:

```json
{
  "previousVersion": "2.0.74",
  "latestVersion": "2.0.76",
  "summary": "...",
  "features": [
    {
      "name": "LSP Tool",
      "description": "Jump to definitions and search references",
      "usage": "Show me the definition of this function",
      "useCases": ["Navigating large codebases", "Understanding impact of changes"]
    }
  ],
  "improvements": ["Faster startup", "Memory leak fix"],
  "generatedAt": "2025-12-23T12:00:00Z"
}
```

If receiving the raw markdown summary, extract structured data before visualization.

## Output

1. PNG infographic saved to cache directory
2. Clickable file path link for user to open

---

## DESIGN PHILOSOPHY: "Technical Clarity"

### The Vision

Technical Clarity is a design philosophy that bridges the precision of software engineering with the warmth of visual communication. It treats version updates not as sterile changelogs, but as moments of progress worth celebrating—each feature a small victory, each improvement a step forward.

### Form and Space

The canvas breathes with intentional negative space. Information clusters organically into digestible zones: a prominent header anchoring the version transition, feature cards arranged in a grid or flowing column, and a footer grounding the composition. White space is not emptiness but punctuation—giving the eye permission to rest and the mind permission to absorb.

### Color and Material

A restrained palette speaks of professionalism while accent colors inject energy. The primary scheme draws from Claude's brand identity: warm neutrals, sophisticated blues, and purposeful highlights. Feature types receive distinct but harmonious color coding—new features in vibrant accent, improvements in muted success tones, fixes in subtle neutral. Every color choice appears deliberate, the product of countless refinements.

### Typography and Hierarchy

Typography serves information, never competes with it. Version numbers command attention through scale and weight. Feature names balance prominence with restraint. Descriptions whisper in supporting sizes. The typographic hierarchy guides the eye naturally from most important to supporting details, each level of information clearly differentiated yet cohesively unified.

### Iconography and Visual Language

Simple, geometric icons punctuate each feature category—a spark for new features, a wrench for improvements, a check for fixes. These visual anchors accelerate comprehension while adding personality. Icons are restrained, never decorative clutter, always functional visual shorthand crafted with meticulous attention to detail.

### Craftsmanship

Every pixel placement reflects master-level execution. Alignment is obsessive. Spacing is mathematical. The final artifact should appear as though someone at the absolute top of their field labored over every detail with painstaking care—because that is exactly what happens. This is not a template filled in; this is a designed artifact.

---

## CANVAS CREATION PROCESS

### Step 1: Parse Input Data

Extract from the changelog summary:
- `previousVersion` → `latestVersion` (version transition)
- Feature list with names, descriptions, usage examples
- Improvements and fixes
- Generation timestamp

### Step 2: Establish Layout

Create a canvas with these specifications:

| Property | Value |
|----------|-------|
| Width | 1200px |
| Height | Dynamic (800-1600px based on content) |
| Background | #FAFAFA (light) or #1A1A1A (dark variant) |
| Margins | 60px all sides |
| Grid | 12-column with 24px gutters |

### Step 3: Header Zone

The header establishes context and celebrates the update:

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│   [Claude Logo/Icon]                                   │
│                                                        │
│   v2.0.74  ────────────────►  v2.0.76                 │
│                                                        │
│   Claude Code Update                                   │
│                                                        │
└────────────────────────────────────────────────────────┘
```

- Version transition: Large, bold typography with arrow indicating progression
- Subtle gradient or accent line separating header from content
- Date stamp in small, muted text

### Step 4: Feature Cards

Each feature becomes a self-contained card:

```
┌─────────────────────────────────────┐
│ ✨ [Feature Name]                   │
│                                     │
│ [2-3 line description]              │
│                                     │
│ 💡 [Usage example in code block]    │
│                                     │
│ 📋 Use cases:                       │
│    • [Case 1]                       │
│    • [Case 2]                       │
└─────────────────────────────────────┘
```

Card specifications:
- Background: White (#FFFFFF) with subtle shadow
- Border-radius: 12px
- Padding: 24px
- Icon/emoji for category identification
- Clear typographic hierarchy within card

### Step 5: Improvements & Fixes Section

A compact, list-style section:

```
┌────────────────────────────────────────────────────────┐
│ 🔧 Improvements & Fixes                                │
│                                                        │
│ • Improved startup performance                         │
│ • Fixed memory leak in long sessions                   │
│ • Enhanced error messages                              │
└────────────────────────────────────────────────────────┘
```

### Step 6: Footer

Ground the composition with metadata:

```
┌────────────────────────────────────────────────────────┐
│ Generated by cc-version-updater    │    Dec 2025      │
└────────────────────────────────────────────────────────┘
```

---

## IMPLEMENTATION

**CRITICAL**: Use Python + Pillow (PIL) to programmatically draw the infographic. This is NOT AI image generation - it's code-based drawing.

### Prerequisites

Ensure Pillow is installed:

```bash
pip install pillow
```

### Font Requirements

**IMPORTANT**: Use Unicode-compatible fonts to avoid garbled characters (文字化け).

| OS | Recommended Font | Path |
|----|------------------|------|
| macOS | Hiragino Sans | `/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc` |
| macOS (fallback) | Arial Unicode | `/System/Library/Fonts/Supplemental/Arial Unicode.ttf` |
| Linux | Noto Sans CJK | `/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc` |
| Windows | Yu Gothic | `C:/Windows/Fonts/yugothic.ttf` |

**Avoid emoji**: Most fonts don't render emoji. Use text symbols instead:
- Instead of ✨ → use `[NEW]` or `*`
- Instead of 💡 → use `TIP:` or `>`
- Instead of 🔧 → use `[FIX]` or `-`
- Instead of 📦 → use `[1]`, `[2]`, etc.

### Drawing with Pillow

Create a Python script that draws the infographic:

```python
from PIL import Image, ImageDraw, ImageFont
import os
import platform

def get_font(size):
    """Get a Unicode-compatible font for the current platform."""
    font_paths = []

    if platform.system() == "Darwin":  # macOS
        font_paths = [
            "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    elif platform.system() == "Linux":
        font_paths = [
            "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    elif platform.system() == "Windows":
        font_paths = [
            "C:/Windows/Fonts/yugothic.ttf",
            "C:/Windows/Fonts/meiryo.ttc",
            "C:/Windows/Fonts/arial.ttf",
        ]

    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue

    return ImageFont.load_default()


def create_changelog_infographic(data, output_path):
    """
    Generate changelog infographic PNG using Pillow.

    Args:
        data: dict with previousVersion, latestVersion, features, improvements
        output_path: where to save the PNG
    """
    # Canvas setup
    width = 1200
    height = 900  # Adjust based on content
    bg_color = "#FAFAFA"

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Colors
    primary = "#1a1a2e"      # Dark text
    accent = "#4a90d9"       # Claude blue
    success = "#10b981"      # Green for improvements
    card_bg = "#ffffff"      # White cards

    # Load Unicode-compatible fonts
    font_large = get_font(48)
    font_medium = get_font(24)
    font_small = get_font(16)

    margin = 60
    y_cursor = margin

    # === Header ===
    draw.rectangle([margin, y_cursor, width - margin, y_cursor + 4], fill=accent)
    y_cursor += 30

    # Version transition (use ASCII arrow for compatibility)
    version_text = f"v{data['previousVersion']}  -->  v{data['latestVersion']}"
    draw.text((margin, y_cursor), version_text, font=font_large, fill=primary)
    y_cursor += 70

    # Title
    draw.text((margin, y_cursor), "Claude Code Update", font=font_medium, fill=accent)
    y_cursor += 60

    # === Feature Cards ===
    for i, feature in enumerate(data.get('features', []), 1):
        # Card background
        card_rect = [margin, y_cursor, width - margin, y_cursor + 150]
        draw.rounded_rectangle(card_rect, radius=12, fill=card_bg)

        # Feature name (use text marker instead of emoji)
        draw.text((margin + 24, y_cursor + 20),
                  f"[{i}] {feature['name']}", font=font_medium, fill=primary)

        # Description
        draw.text((margin + 24, y_cursor + 60),
                  feature['description'][:80], font=font_small, fill=primary)

        # Usage (use text marker instead of emoji)
        draw.text((margin + 24, y_cursor + 100),
                  f"> {feature.get('usage', '')[:60]}", font=font_small, fill="#666666")

        y_cursor += 170

    # === Improvements Section ===
    draw.text((margin, y_cursor), "[FIX] Improvements & Fixes", font=font_medium, fill=success)
    y_cursor += 40

    for improvement in data.get('improvements', []):
        draw.text((margin + 20, y_cursor), f"- {improvement}", font=font_small, fill=primary)
        y_cursor += 30

    # === Footer ===
    y_cursor = height - 50
    draw.text((margin, y_cursor), "Generated by cc-version-updater", font=font_small, fill="#999999")

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG")
    return output_path
```

### Execution Steps

1. **Parse changelog data** from the interpreter output
2. **Write Python script** with the drawing code above
3. **Execute the script**:
   ```bash
   python3 generate_infographic.py
   ```
4. **Verify output** exists at the expected path

### Cache Directory

Save generated infographics to:

```
plugins/cc-version-updater/.cache/infographics/
├── changelog-2.0.74-to-2.0.76.png
├── changelog-2.0.76-to-2.0.77.png
└── ...
```

Filename pattern: `changelog-{prevVersion}-to-{newVersion}.png`

### Output Format

After generating the infographic, output:

```markdown
## Infographic Generated

Your changelog infographic has been created:

📁 **File**: `~/.claude-plugins/cc-version-updater/.cache/infographics/changelog-2.0.74-to-2.0.76.png`

👆 Click to open, or run:
```bash
open ~/.claude-plugins/cc-version-updater/.cache/infographics/changelog-2.0.74-to-2.0.76.png
```
```

---

## QUALITY STANDARDS

### Visual Checklist

Before finalizing, verify:

- [ ] All text is legible and properly sized
- [ ] No elements overlap or clip
- [ ] Consistent spacing throughout
- [ ] Color contrast meets accessibility standards
- [ ] Icons are crisp and aligned
- [ ] Version numbers are prominently displayed
- [ ] Feature cards are evenly spaced
- [ ] Footer is properly positioned

### Refinement Pass

After initial generation, review and refine:

1. **Spacing**: Ensure mathematical consistency
2. **Alignment**: Verify all elements align to grid
3. **Typography**: Check hierarchy is clear
4. **Color**: Confirm palette cohesion
5. **Balance**: Assess overall visual weight distribution

The goal: An artifact that could be displayed in a design portfolio, shared on social media, or printed as documentation. Museum quality, every time.

---

## EXAMPLE OUTPUT

For input:
```json
{
  "previousVersion": "2.0.74",
  "latestVersion": "2.0.76",
  "features": [
    {
      "name": "LSP Tool",
      "description": "Jump to definitions and search for references within your code.",
      "usage": "Show me the definition of this function",
      "useCases": ["Navigating large codebases", "Understanding impact before refactoring"]
    }
  ],
  "improvements": ["Faster startup", "Memory leak fix"]
}
```

Generate a 1200x900px PNG with:
- Header showing "v2.0.74 → v2.0.76"
- One feature card for "LSP Tool"
- Compact improvements section
- Footer with generation info

Save to: `.cache/infographics/changelog-2.0.74-to-2.0.76.png`

Output clickable path for user.
