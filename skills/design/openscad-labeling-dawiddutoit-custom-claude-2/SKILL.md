---
name: openscad-labeling
description: |
  Adds text labels to OpenSCAD 3D models using BOSL2's face/anchor system and specialized labeling libraries. Use when you need to label model faces, add part numbers, create dimension annotations, or wrap text on curved surfaces. Triggers on "label this model", "add text to face", "how do I label in OpenSCAD", "text on cylinder", "attach text to TOP face", or "install text libraries". Works with .scad files, BOSL2, text_on_OpenSCAD, attachable_text3d, and Write.scad libraries.

---

# OpenSCAD Labeling

Add text labels to 3D model faces, part numbers, dimension annotations, and curved surface text in OpenSCAD.

## Quick Start

Label a cube's top face using BOSL2's attach system (most common use case):

```openscad
include <BOSL2/std.scad>

cuboid([50, 30, 20])
    attach(TOP, BOT)
        linear_extrude(2)
            text("TOP", size=8, halign="center", valign="center");
```

This creates raised text on the top face without calculating positions manually.

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Instructions
   3.1 Define Faces with BOSL2
   3.2 Add Text to Flat Faces
   3.3 Add Text to Curved Surfaces
   3.4 Install Labeling Libraries
4. Supporting Files
5. Expected Outcomes
6. Requirements
7. Red Flags to Avoid

## When to Use This Skill

**Explicit Triggers:**
- "Label this model"
- "Add text to the TOP face"
- "How do I add part numbers in OpenSCAD?"
- "Text on cylinder"
- "Install text_on_OpenSCAD"

**Implicit Triggers:**
- Creating parts that need identification
- Building labeled storage bins
- Making dimension annotations for debug
- Wrapping text around curved objects
- Engraving text into surfaces

**Debugging Triggers:**
- "Why isn't my text showing on the right face?"
- "Text is backwards/upside down"
- "How do I center text on a face?"

## What This Skill Does

This skill helps you:

1. **Define faces** using BOSL2's semantic anchor system (TOP, BOTTOM, LEFT, etc.)
2. **Attach text** to faces without manual position calculations
3. **Choose libraries** based on surface type (flat vs curved) and requirements
4. **Install libraries** for advanced text features (curved surfaces, font metrics)
5. **Create practical patterns** (part labels, dimension annotations, engraved text)

## Instructions

### 3.1 Define Faces with BOSL2

BOSL2 provides named face constants that eliminate manual coordinate calculations.

**Standard faces:**
```openscad
include <BOSL2/std.scad>

// The six primary faces
TOP, BOTTOM, LEFT, RIGHT, FRONT, BACK
```

**Face reference table:**

| Face | Direction | Normal Vector | Notes |
|------|-----------|---------------|-------|
| TOP | +Z | [0, 0, 1] | Points up |
| BOTTOM | -Z | [0, 0, -1] | Points down |
| FRONT | -Y | [0, -1, 0] | Points toward viewer |
| BACK | +Y | [0, 1, 0] | Points away |
| LEFT | -X | [-1, 0, 0] | Points left |
| RIGHT | +X | [1, 0, 0] | Points right |

**Attach objects to faces:**
```openscad
cuboid([50, 30, 20]) {
    attach(TOP) color("red") cuboid([10, 10, 5]);
    attach(FRONT) color("blue") cyl(d=8, h=3);
    attach(LEFT+BOTTOM) color("green") sphere(d=5);
}
```

**Edges and corners:**
```openscad
// Edges (combine two faces)
TOP+LEFT, BOTTOM+RIGHT, FRONT+TOP

// Corners (combine three faces)
TOP+LEFT+FRONT, BOTTOM+RIGHT+BACK
```

### 3.2 Add Text to Flat Faces

**Pattern 1: Raised text (embossed)**

```openscad
include <BOSL2/std.scad>

cuboid([50, 30, 20])
    attach(TOP, BOT)
        linear_extrude(2)
            text("LABEL", size=8, halign="center", valign="center");
```

Breakdown:
- `attach(TOP, BOT)` - Attach to TOP face, align text's BOT to surface
- `linear_extrude(2)` - Extrude 2mm tall
- `halign="center", valign="center"` - Center text on face

**Pattern 2: Engraved text (debossed)**

```openscad
include <BOSL2/std.scad>

diff()
cuboid([50, 30, 20])
    attach(TOP, BOT, inside=true)
        tag("remove")
        linear_extrude(1)
            text("CUT", size=8, halign="center", valign="center");
```

Breakdown:
- `diff()` - Enable boolean difference mode
- `inside=true` - Attach inside the surface
- `tag("remove")` - Mark for subtraction

**Pattern 3: Multiple labeled faces**

```openscad
include <BOSL2/std.scad>

module labeled_box(size, labels) {
    faces = [TOP, BOTTOM, FRONT, BACK, LEFT, RIGHT];

    diff()
    cuboid(size)
        for (i = [0:5])
            if (labels[i] != "")
                attach(faces[i], BOT)
                    tag("remove")
                    linear_extrude(1)
                        text(labels[i], size=size.x/8, halign="center", valign="center");
}

labeled_box([50, 30, 20], ["TOP", "BOT", "FRONT", "BACK", "L", "R"]);
```

**Pattern 4: Part number label tag**

```openscad
include <BOSL2/std.scad>

module part_label(txt, size=[40, 15, 2]) {
    diff()
    cuboid(size, rounding=1, edges="Z")
        attach(TOP, BOT, inside=true)
            tag("remove")
            linear_extrude(0.5)
                text(txt, size=size.y*0.5, halign="center", valign="center");
}

part_label("PN-001");
```

### 3.3 Add Text to Curved Surfaces

For curved surfaces (cylinders, spheres), use specialized libraries.

**Check library installation status:**

```bash
ls ~/Documents/OpenSCAD/libraries/text_on_OpenSCAD
ls ~/Documents/OpenSCAD/libraries/openscad_attachable_text3d
```

**Option 1: text_on_OpenSCAD (curved surfaces)**

```openscad
use <text_on_OpenSCAD/text_on.scad>

// Text wrapped around cylinder
text_on_cylinder("LABEL", r=15, h=30, size=4, font="Liberation Sans");

// Text on sphere surface
text_on_sphere("Hello World", r=20, size=5);

// Text on cube face (alternative to BOSL2)
text_on_cube("FRONT", size=8, face="front", cube_size=50);
```

**Option 2: attachable_text3d (BOSL2-compatible)**

```openscad
include <BOSL2/std.scad>
use <openscad_attachable_text3d/attachable_text3d.scad>

// Attachable 3D text with accurate font metrics
cuboid([50, 30, 20])
    attach(TOP)
        attachable_text3d("Label", size=10, h=2);
```

Benefits:
- Works with BOSL2's attach system
- Accurate bounding box for alignment
- Better font metric calculations

**Option 3: Write.scad (classic library)**

```openscad
use <Write.scad>

// Text on cube faces
writecube("TEXT", [50, 30, 20], face="front", t=2, h=8);

// Text on sphere
writesphere("GLOBE", 25, t=2, h=6);

// Text on cylinder
writecylinder("LABEL", r=15, h=30, t=2);
```

### 3.4 Install Labeling Libraries

**text_on_OpenSCAD (curved surfaces + internationalization):**

```bash
cd ~/Documents/OpenSCAD/libraries  # macOS
# cd ~/.local/share/OpenSCAD/libraries  # Linux

git clone https://github.com/brodykenrick/text_on_OpenSCAD.git
```

Verify installation:
```openscad
use <text_on_OpenSCAD/text_on.scad>
text_on_cylinder("TEST", r=10, h=20, size=3);
```

**attachable_text3d (BOSL2-compatible, accurate metrics):**

```bash
cd ~/Documents/OpenSCAD/libraries
git clone https://github.com/jon-gilbert/openscad_attachable_text3d.git
```

Verify installation (requires BOSL2):
```openscad
include <BOSL2/std.scad>
use <openscad_attachable_text3d/attachable_text3d.scad>
attachable_text3d("TEST", size=10, h=2);
```

**Check what's already installed:**

```bash
ls -la ~/Documents/OpenSCAD/libraries/
```

Common pre-installed libraries:
- BOSL2 (always available in this project)
- NopSCADlib
- MCAD

## Supporting Files

**References:**
- `references/library-comparison.md` - Detailed comparison of text_on_OpenSCAD, attachable_text3d, Write.scad
- `references/font-reference.md` - Cross-platform fonts, font parameters, system font usage

**Examples:**
- `examples/practical-labels.scad` - Part labels, dimension annotations, debug labels
- `examples/curved-text.scad` - Cylinder/sphere text wrapping examples
- `examples/engraved-embossed.scad` - Raised vs cut text patterns

**Scripts:**
- `scripts/check-text-libraries.sh` - Verify text library installations
- `scripts/list-system-fonts.sh` - List available fonts for OpenSCAD

## Expected Outcomes

**Success:** Text appears on correct face, properly centered

```openscad
include <BOSL2/std.scad>

cuboid([50, 30, 20])
    attach(TOP, BOT)
        linear_extrude(2)
            text("SUCCESS", size=6, halign="center", valign="center");
```

Output: Text centered on top face, raised 2mm, easily readable.

**Failure:** Text backwards, wrong face, or positioning errors

```openscad
// ❌ WRONG: Manual positioning without BOSL2
cube([50, 30, 20]);
translate([25, 15, 20])  // Easy to miscalculate
    linear_extrude(2)
        text("WRONG", size=6, halign="center");
```

Problem: Manual calculations prone to errors, text may be backwards or misaligned.

## Requirements

**Required:**
- OpenSCAD 2021.01+ (text() function)
- BOSL2 library (for attach system)

**Optional:**
- text_on_OpenSCAD (curved surfaces)
- attachable_text3d (better font metrics)
- Write.scad (classic curved text)

**Knowledge:**
- Basic BOSL2 attach syntax
- Understanding of face normals
- OpenSCAD text() parameters

## Red Flags to Avoid

1. **Manual text positioning** - Use attach() instead of translate/rotate calculations
2. **Forgetting halign/valign** - Text won't center without these parameters
3. **Wrong face attachment point** - Use `attach(TOP, BOT)` not `attach(TOP, TOP)`
4. **Missing libraries** - Check installation before using specialized text functions
5. **Text too large for surface** - Scale text size relative to face dimensions
6. **Backwards text on faces** - BOSL2's attach handles orientation automatically
7. **Using inside=true for raised text** - Only use for engraved/cut text
8. **Forgetting tag("remove") in diff()** - Text won't be cut without tag
9. **Assuming Write.scad is installed** - It's not bundled with OpenSCAD
10. **Not centering text** - Default text origin is bottom-left corner

## Notes

**Library decision tree:**

```
Need text on model?
├─ Flat surface?
│  ├─ Using BOSL2? → attach() + text()
│  └─ Not using BOSL2? → text_on_OpenSCAD or Write.scad
└─ Curved surface (cylinder/sphere)?
   ├─ BOSL2 workflow? → attachable_text3d (if installed)
   └─ Classic approach? → text_on_OpenSCAD or Write.scad
```

**Performance tip:** Use `$fn=$preview ? 32 : 64` to speed up text rendering in preview mode.

**Font availability:** Use "Liberation Sans", "Liberation Mono", or "Liberation Serif" for cross-platform compatibility.

**Text depth guidelines:**
- Raised text: 1-2mm for labels, 0.5mm for fine detail
- Engraved text: 0.5-1mm depth (too deep weakens part)

**See references/ for detailed library comparisons and advanced examples.**
