---
name: openscad-collision-detection
description: |
  Detects and visualizes geometric intersections in OpenSCAD models using built-in
  techniques (intersection(), debug modifiers), BOSL2 utilities (debug_this, ghost),
  and reusable collision check patterns. Use when checking drawer clearances, door
  swing interference, shelf spacing, hinge collisions, or any geometric overlap in
  woodworking projects. Triggers on "check collision", "detect interference",
  "drawer clearance", "door swing", "check overlap", "assembly interference", or
  "fits in cabinet". Works with .scad files, woodworkers-lib patterns, BOSL2
  attachments, and OpenSCAD 2025 Manifold engine.

---

# OpenSCAD Collision Detection

Detect and visualize geometric intersections in OpenSCAD models for woodworking and assembly validation.

## Quick Start

Add collision checking to any OpenSCAD model in 3 steps:

```openscad
// 1. Create reusable checker module
module check_collision(show_overlap=true) {
    if (show_overlap) {
        color("red", 0.8) intersection() {
            children(0);
            children(1);
        }
    }
    %children(0);  // Ghost first object
    children(1);   // Solid second object
}

// 2. Apply to your objects
check_collision() {
    drawer();              // Moving part
    cabinet_interior();    // Fixed structure
}

// 3. Preview (F5) - red regions show collisions
```

**Result:** Transparent reference geometry + solid moving part + red overlap visualization.

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Core Techniques](#3-core-techniques)
4. [Reusable Patterns](#4-reusable-patterns)
5. [Woodworking Scenarios](#5-woodworking-scenarios)
6. [Debugging Workflow](#6-debugging-workflow)
7. [Supporting Files](#7-supporting-files)
8. [Expected Outcomes](#8-expected-outcomes)
9. [Integration Points](#9-integration-points)
10. [Requirements](#10-requirements)
11. [Red Flags to Avoid](#11-red-flags-to-avoid)

## When to Use This Skill

### Explicit Triggers
- "Check collision between drawer and cabinet"
- "Detect interference in door swing"
- "Verify clearance for shelf spacing"
- "Show overlaps in assembly"
- "Check if drawer fits in cabinet"
- "Door hinge collision check"
- "Workbench against wall clearance"

### Implicit Triggers
- Designing cabinets with drawers
- Creating furniture assemblies
- Planning room layouts with furniture placement
- Validating mechanical clearances
- Debugging "won't fit" issues
- Testing parametric designs with varying dimensions

### Debugging Scenarios
- Drawer won't close (hits back panel)
- Door hits adjacent object when opening
- Shelf spacing too tight for items
- Hinge cup interferes with door panel
- Workbench depth exceeds available space
- Parametric model generates invalid dimensions

## What This Skill Does

Provides systematic approach to collision detection:

1. **Visualize intersections** using `intersection()` to reveal overlap volumes
2. **Ghost reference geometry** using `%` modifier for transparent context
3. **Highlight collisions** with color coding (red = problem, yellow = clearance)
4. **Measure clearances** with echo statements and visual indicators
5. **Create reusable patterns** for common woodworking scenarios
6. **Integrate with project libraries** (woodworkers-lib, BOSL2, labels.scad)
7. **Validate assemblies** before fabrication or room layout

## Core Techniques

### intersection() - Reveal Overlaps

Returns geometry only where objects overlap:

```openscad
// Show collision volume
color("red") intersection() {
    drawer();
    cabinet_interior();
}
// If result has volume → collision exists
```

### Debug Modifiers

| Modifier | Effect | Use Case |
|----------|--------|----------|
| `%` | Transparent (ghost) | Show reference geometry |
| `#` | Highlight (red) | Emphasize specific object |
| `!` | Show only | Isolate object for testing |
| `*` | Disable | Temporarily hide geometry |

```openscad
%cabinet_interior();  // Ghost
#drawer();           // Highlight
```

### BOSL2 Utilities

```openscad
include <BOSL2/std.scad>

debug_this() drawer();  // Shows bounding box + transparent object
ghost() cabinet();      // Semantic equivalent to %
```

## Reusable Patterns

### Pattern 1: Basic Collision Checker

```openscad
module check_collision(show_overlap=true, overlap_color="red") {
    if (show_overlap) {
        color(overlap_color, 0.8) intersection() {
            children(0);
            children(1);
        }
    }
    %children(0);  // Ghost first object
    children(1);   // Solid second object
}
```

**Usage:**
```openscad
check_collision() {
    drawer_extended();
    cabinet_side_panel();
}
```

### Pattern 2: Clearance Visualization

```openscad
module show_clearance(clearance=2, zones=true) {
    // Original objects
    %children(0);
    children(1);

    // Clearance zones
    if (zones) {
        color("yellow", 0.2)
            offset(r=clearance)
            projection(cut=false)
            children(0);
    }

    // Collision check
    color("red") intersection() {
        children(0);
        children(1);
    }
}
```

### Pattern 3: Conditional Debug Mode

```openscad
DEBUG_COLLISION = true;  // Toggle at file top

module conditional_check() {
    if (DEBUG_COLLISION) {
        color("red") intersection() {
            children(0);
            children(1);
        }
        %children(0);
        children(1);
    } else {
        children(0);
        children(1);
    }
}
```

### Pattern 4: Assembly Interference Check

```openscad
module assembly_check(explode=false) {
    spacing = explode ? 50 : 0;

    // Check overlaps when assembled (explode=false)
    if (!explode) {
        color("red", 0.8) intersection() {
            children(0);
            children(1);
        }
    }

    children(0);
    translate([spacing, 0, 0]) children(1);
}

// Usage
assembly_check(explode=$preview) {
    cabinet_shell();
    drawer_assembly();
}
```

## Woodworking Scenarios

### Drawer Clearance Check

```openscad
include <woodworkers-lib/std.scad>

module drawer_clearance_check(cabinet_dim, drawer_dim, panel=18) {
    interior_w = cabinet_dim[0] - 2 * panel;
    interior_d = cabinet_dim[1] - panel;
    interior_h = cabinet_dim[2] - 2 * panel;

    // Ghost cabinet interior
    %color("blue", 0.2)
        translate([panel, 0, panel])
        cube([interior_w, interior_d, interior_h]);

    // Show drawer
    color("green", 0.5) cube(drawer_dim);

    // Highlight collision
    color("red") intersection() {
        translate([panel, 0, panel]) cube([interior_w, interior_d, interior_h]);
        cube(drawer_dim);
    }

    // Echo clearances
    side_clearance = (interior_w - drawer_dim[0]) / 2;
    echo(str("Side clearance: ", side_clearance, "mm per side"));
}
```

### Door Swing Interference

```openscad
module door_swing_check(door_width, swing_angle=90, adjacent_pos=500) {
    // Door sweep volume
    color("yellow", 0.3)
        rotate([0, 0, swing_angle])
        cube([door_width, 5, 720]);

    // Adjacent object
    translate([adjacent_pos, 0, 0])
        color("green", 0.5)
        cube([200, 400, 720]);

    // Check interference
    color("red") intersection() {
        rotate([0, 0, swing_angle]) cube([door_width, 5, 720]);
        translate([adjacent_pos, 0, 0]) cube([200, 400, 720]);
    }
}
```

### Shelf Spacing Validation

```openscad
module shelf_spacing_check(cabinet_dim, shelf_positions, item_height, panel=18) {
    // Draw shelves
    for (z = shelf_positions) {
        translate([0, 0, z])
            %planeBottom([cabinet_dim[0], cabinet_dim[1], panel]);
    }

    // Check spacing
    for (i = [0:len(shelf_positions)-2]) {
        spacing = shelf_positions[i+1] - shelf_positions[i] - panel;
        if (spacing < item_height) {
            echo(str("WARNING: Shelf ", i, " spacing (", spacing,
                     "mm) < item height (", item_height, "mm)"));

            // Highlight insufficient spacing
            translate([0, 0, shelf_positions[i] + panel])
                color("red", 0.5)
                cube([cabinet_dim[0], cabinet_dim[1], spacing]);
        }
    }
}
```

## Debugging Workflow

Follow this systematic 5-step process:

### Step 1: Isolate Components

```openscad
!drawer();  // Show only drawer (use ! modifier)
```

### Step 2: Ghost Reference Geometry

```openscad
%cabinet_interior();
drawer();
```

### Step 3: Check Intersection

```openscad
color("red") intersection() {
    cabinet_interior();
    drawer();
}
// No volume = no collision
```

### Step 4: Measure Clearance

```openscad
drawer_width = 764;
interior_width = 782;
clearance = interior_width - drawer_width;
echo(str("Total clearance: ", clearance, "mm (", clearance/2, "mm per side)"));

if (clearance < 4) {
    echo("ERROR: Insufficient clearance!");
}
```

### Step 5: Iterate with Parameters

```openscad
DRAWER_CLEARANCE = 2;  // mm per side

module drawer_with_clearance(interior_width) {
    width = interior_width - 2*DRAWER_CLEARANCE;
    cube([width, 400, 100]);
}
```

## Supporting Files

### examples/examples.md
Comprehensive collision detection examples:
- Drawer clearance checks (side, top, depth)
- Door swing interference (hinges, adjacent objects)
- Shelf spacing validation (item heights, bin clearance)
- Hinge collision detection (cup-to-door, door-to-frame)
- Room layout validation (workbench against wall)
- Assembly interference (multi-part checking)

### references/reference.md
Technical reference:
- OpenSCAD boolean operations (intersection, difference, union)
- Manifold vs CGAL engine comparison
- Performance optimization techniques
- Color coding standards for collision detection
- Mathematical clearance calculations
- Integration with BOSL2 and woodworkers-lib

## Expected Outcomes

### Successful Collision Detection

**No collision:**
```
ECHO: "Side clearance: 2.0mm per side"
ECHO: "Top clearance: 5.0mm"
ECHO: "Depth clearance: 10.0mm"
```
Preview shows no red regions.

**Collision detected:**
```
ECHO: "WARNING: Drawer collision detected!"
ECHO: "Overlap volume: 15mm × 18mm × 100mm"
ECHO: "Reduce drawer width by 15mm"
```
Preview shows red overlap region.

### Visual Feedback

| Color | Meaning |
|-------|---------|
| Red | Collision/interference |
| Yellow | Clearance zone |
| Green | Moving parts |
| Blue | Fixed structure |
| Transparent | Reference geometry |

## Integration Points

### With woodworkers-lib

```openscad
include <woodworkers-lib/std.scad>

module ww_collision_check(outer_dim, inner_dim) {
    // Outer box (cabinet)
    %color("blue", 0.2) {
        planeBottom(outer_dim);
        planeTop(outer_dim);
        planeLeft(outer_dim, t=-1, b=-1);
        planeRight(outer_dim, t=-1, b=-1);
    }

    // Inner box (drawer)
    color("green", 0.5) {
        planeBottom(inner_dim);
        // ... other planes
    }
}
```

### With labels.scad

```openscad
include <lib/labels.scad>

module labeled_collision_check() {
    labeled_cuboid([800, 400, 100],
        name="DRAWER",
        box_color="green"
    );

    translate([0, 0, 100])
    labeled_cuboid([800, 400, 18],
        name="SHELF",
        box_color="brown"
    );

    // Collision check
    color("red") intersection() {
        cube([800, 400, 100]);
        translate([0, 0, 100]) cube([800, 400, 18]);
    }
}
```

### With BOSL2 Attachments

```openscad
include <BOSL2/std.scad>

diff()
cuboid([100, 100, 50])
    attach(TOP) tag("remove")
        cyl(d=20, h=30);  // Check if penetrates too deep
```

## Requirements

### Tools
- OpenSCAD 2025.x (Manifold engine for fast intersections)
- BOSL2 library (optional, for debug_this/ghost utilities)
- woodworkers-lib (optional, for cabinet/furniture patterns)

### Knowledge
- Basic OpenSCAD syntax (modules, translate, cube)
- CSG operations (union, difference, intersection)
- Debug modifiers (%, #, !, *)
- Color syntax with alpha channel

### Environment
- Preview mode (F5) for fast iteration
- Console output visible for echo statements

## Red Flags to Avoid

- [ ] **Not checking clearances before fabrication** - Always validate fits
- [ ] **Ignoring echo warnings** - Console output reveals dimension problems
- [ ] **Using render (F6) for collision checks** - Preview (F5) is 10-100x faster
- [ ] **Forgetting alpha channel in colors** - `color("red", 0.5)` not `color("red")`
- [ ] **Testing only best-case scenarios** - Check extreme parameter values
- [ ] **Nesting intersection() unnecessarily** - Slows down renders significantly
- [ ] **Not parameterizing clearances** - Hardcoded values make iteration difficult
- [ ] **Skipping validation in parametric designs** - Add `assert()` statements
- [ ] **Assuming preview accuracy** - Render (F6) for final validation if critical
- [ ] **Not documenting clearance requirements** - Add comments explaining minimums

## Notes

**Manifold Engine:** OpenSCAD 2025+ uses Manifold by default for 10-100x faster boolean operations. If intersection results look wrong, try `--backend CGAL` as fallback.

**Preview vs Render:** Collision detection is usually sufficient in preview mode (F5). Only use render (F6) for final validation of critical clearances.

**Color Consistency:** Use red for collisions, yellow for clearances, green for moving parts, blue for fixed structure throughout all models.

**Documentation:** Add echo statements for all clearance calculations. Future you will thank present you.

**Parametric Validation:** Use `assert()` to enforce clearance minimums:
```openscad
assert(clearance >= 4, "Drawer clearance must be >= 4mm");
```
