---
name: openscad-workshop-tools
description: |
  Create parametric OpenSCAD 3D models of workshop tools (drill presses, vacuums, saws, etc.)
  for workshop layout planning. Use when asked to "model a tool", "create OpenSCAD for [tool]",
  "add [tool] to workshop", or when planning workshop layouts that need tool representations.
  Supports brand-accurate colors (Bosch, Festool, Makita, DeWalt, Milwaukee) and standardized
  code structure with customizer parameters.
---

# OpenSCAD Workshop Tool Modeling

Create parametric 3D models of workshop tools for layout planning and visualization.

## Workflow

### 1. Gather Specifications

Collect from user, manuals, or product pages:
- **Dimensions**: Overall W x D x H, base plate size
- **Weight**: Helps verify scale is reasonable
- **Key features**: Chuck size, motor power, speeds (for header comment)
- **Reference image**: Essential for component identification

### 2. Identify Components

Decompose tool into logical modules. See [references/code-structure.md](references/code-structure.md) for decomposition patterns by tool type.

Typical components:
- Base/frame (static foundation)
- Main body/motor housing
- Moving parts (quill, blade guard, plunge mechanism)
- Controls (buttons, dials, levers)
- Accessories (vise, fence, dust port)

### 3. Write OpenSCAD File

Follow the standardized structure in [references/code-structure.md](references/code-structure.md):

```openscad
/* [Section] */     // Customizer sections
// Comment         // Parameter description
param = value;     // Actual parameter

module component() { ... }  // One module per component
module tool_name() { ... }  // Assembly module
tool_name();                // Render call
echo("=== ... ===");        // Debug output
```

**Key patterns:**
- Use `$fn = $preview ? 32 : 64` for quality switching
- Apply brand colors from reference table
- Include `show_*` toggles for optional components
- Use `hull()` for rounded shapes
- Add floor reference plane for context

### 4. Render Preview

```bash
openscad -o images/tool-name.png \
  --autocenter --viewall \
  --imgsize=800,1000 \
  /path/to/tool.scad
```

### 5. Iterate

Adjust proportions based on visual comparison to reference image.

## File Location

Save to: `workshop/tools/<brand>-<model>.scad`

Examples:
- `workshop/tools/bosch-pbd40.scad`
- `workshop/tools/festool-ctl-midi.scad`
- `workshop/tools/festool-ts55.scad`

## Quick Reference

| Tool Type | Key Dimensions | Critical Components |
|-----------|---------------|---------------------|
| Drill press | Base, column height, head depth | Column, quill, chuck, handwheel |
| Track saw | Body L x W x H, blade dia | Base plate, blade guard, handle |
| Vacuum | L x W x H, wheel dia | Body, wheels, handle, hose port |
| Bandsaw | Table size, throat depth | Frame, table, blade guides |
