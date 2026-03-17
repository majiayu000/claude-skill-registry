---
name: chronicle-structure
description: Guide for adding structure information to Chronicle with visual hints
---

# Chronicle Structure Addition Guide

**Purpose**: Guide for adding new structure information to Chronicle with visual hints (images).

**How it works**: This skill is automatically activated when you mention tasks related to:
- Adding new structures to Chronicle
- Converting screenshots to Chronicle images
- Adding image pages to Chronicle entries
- Creating visual hints for structures in Chronicle

Simply describe what you want to do, and Claude will reference the appropriate guidance from this skill.

---

## Adding Structure to Chronicle (2025-12-27)

**Overview**: Adding a new structure to Chronicle involves three main steps:
1. Creating the structure entry JSON
2. Converting screenshots to Chronicle-style images
3. Adding image pages to the entry

### Step 1: Create Structure Entry JSON

**Location**: `common/src/main/resources/assets/chronodawn/chronicle/entries/structures/<structure_name>.json`

**Template**:
```json
{
  "category": "structures",
  "title": {
    "en_us": "Structure Name",
    "ja_jp": "構造物名"
  },
  "icon": "minecraft:block_name",
  "sortnum": 1,
  "pages": [
    {
      "text": {
        "en_us": "Structure description...",
        "ja_jp": "構造物の説明..."
      }
    },
    {
      "image": "chronodawn:textures/gui/chronicle/<structure_name>.png"
    },
    {
      "text": {
        "en_us": "Additional details...",
        "ja_jp": "追加の詳細..."
      }
    }
  ]
}
```

### Step 2: Convert Screenshots to Chronicle Images

**Tool**: `scripts/convert_chronicle_image.sh`

**Requirements**:
- ImageMagick installed (`brew install imagemagick` on macOS)
- Screenshot placed in `assets/screenshots/chronicle/`

**Conversion Process**:

The script applies the following transformations:
1. **Grayscale conversion** (`-colorspace Gray`) - Convert to black and white
2. **Sketch effect** (`-sketch 0x10+80`) - Apply pencil sketch appearance
3. **Auto-level** (`-auto-level`) - Normalize brightness/contrast
4. **Brightness/contrast adjustment** (`-brightness-contrast -5x-10`) - Fine-tune for book aesthetic

**Usage**:

Single file:
```bash
./scripts/convert_chronicle_image.sh phantom_catacombs.png
```

All files in directory:
```bash
./scripts/convert_chronicle_image.sh --all
```

**Input/Output**:
- Input: `assets/screenshots/chronicle/<structure_name>.png`
- Output: `common/src/main/resources/assets/chronodawn/textures/gui/chronicle/<structure_name>.png`

### Step 3: Add to Categories (if new structure type)

**Location**: `common/src/main/resources/assets/chronodawn/chronicle/categories.json`

Only needed if adding a new category. Existing categories: `basics`, `progression`, `items`, `structures`, `bosses`.

---

## Complete Workflow Example

**Scenario**: Adding "Ancient Ruins" structure to Chronicle

1. **Take screenshot**:
   - Capture in-game screenshot of the structure
   - Save as `assets/screenshots/chronicle/ancient_ruins.png`

2. **Convert to Chronicle style**:
   ```bash
   ./scripts/convert_chronicle_image.sh ancient_ruins.png
   ```

3. **Create JSON entry**:
   - Create `common/src/main/resources/assets/chronodawn/chronicle/entries/structures/ancient_ruins.json`
   - Add description text pages
   - Insert image page reference: `"image": "chronodawn:textures/gui/chronicle/ancient_ruins.png"`

4. **Test in-game**:
   - Build mod: `./gradlew :fabric:build`
   - Open Chronicle in-game
   - Navigate to Structures → Ancient Ruins
   - Verify image appears on page 2 with proper styling

---

## Image Rendering Features

Chronicle image pages include:

1. **Automatic scaling**: Images scale to fit page dimensions while maintaining aspect ratio
2. **Sepia tone**: Warm beige/sepia color (0xF0E0D0) matches book background
3. **Vignette effect**: 15px fade on edges and corners for sketch-like appearance
4. **Center alignment**: Images centered on page

**Technical Details**:
- Maximum width: ~140px (page width minus margins)
- Maximum height: ~190px (page height minus margins and page number)
- Aspect ratio: Preserved automatically
- Format: PNG with transparency support

---

## Directory Structure

```
ChronoDawn/
├── assets/screenshots/chronicle/          # Original screenshots
│   ├── phantom_catacombs.png
│   ├── master_clock.png
│   └── ancient_ruins.png                  # New screenshot
├── scripts/
│   └── convert_chronicle_image.sh         # Conversion script
└── common/src/main/resources/assets/chronodawn/
    ├── chronicle/entries/structures/      # Structure JSON entries
    │   ├── phantom_catacombs.json
    │   ├── master_clock.json
    │   └── ancient_ruins.json             # New entry
    └── textures/gui/chronicle/            # Converted Chronicle images
        ├── phantom_catacombs.png
        ├── master_clock.png
        └── ancient_ruins.png              # Converted image
```

---

## Existing Structures with Images

As of 2025-12-27:
- Phantom Catacombs (`phantom_catacombs.png`)
- Master Clock (`master_clock.png`)
- Clockwork Depths (`clockwork_depths.png`)
- Desert Clock Tower (`desert_clock_tower.png`)
- Entropy Crypt (`entropy_crypt.png`)
- Guardian Vault (`guardian_vault.png`)

---

## Troubleshooting

**Image not appearing**:
- Verify file exists: `common/src/main/resources/assets/chronodawn/textures/gui/chronicle/<name>.png`
- Check JSON syntax: Image path must be `chronodawn:textures/gui/chronicle/<name>.png`
- Rebuild mod: `./gradlew :fabric:build`

**Image quality issues**:
- Adjust ImageMagick parameters in `scripts/convert_chronicle_image.sh`
- Sketch intensity: Change `-sketch 0x10+80` (format: `radius x sigma + angle`)
- Brightness: Adjust `-brightness-contrast -5x-10` (format: `brightness x contrast`)

**Image too large/small**:
- Original screenshot size doesn't matter (auto-scaled)
- Ensure aspect ratio is reasonable (avoid extreme wide/tall images)

---

## Best Practices

1. **Screenshot quality**:
   - Use high resolution (e.g., 1920x1080)
   - Clear view of the structure
   - Good lighting (avoid too dark/bright)

2. **Image naming**:
   - Use snake_case (e.g., `ancient_ruins.png`)
   - Match structure entry JSON filename
   - Keep names descriptive but concise

3. **Page ordering**:
   - Page 1: Structure overview and description
   - Page 2: Image (visual hint)
   - Page 3+: Additional details, boss info, tips

4. **Testing**:
   - Always test in-game before committing
   - Verify on both Fabric and NeoForge if applicable
   - Check both English and Japanese text

---

**Last Updated**: 2025-12-27
**Maintained by**: Chrono Dawn Development Team
