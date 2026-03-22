---
name: figma-guidelines
description: "Figma design knowledge for AI agents operating through MCP tools. Use whenever working in Figma via MCP — creating layouts, building components, managing design tokens/variables, organizing files, or manipulating any design element. Covers component architecture (variants, properties, slots, atomic design), auto layout (direction, spacing, sizing, wrap, absolute positioning), variables and styles (token architecture, modes, scoping, aliasing), collaboration features (comments, annotations, sections, Dev Mode), and critical gotchas (font loading, immutable properties, coordinate systems, instance limitations). Also trigger when the user asks to build a design system, create responsive layouts, set up design tokens, organize a Figma file, or work with component libraries. If the task involves Figma in any way, use this skill."
---

# Figma MCP Agent Skill

You are controlling Figma through MCP tools that bridge to the Figma Plugin API. You don't write Plugin API code directly — you call tools. But you need Figma's mental models to call them correctly.

**Before any Figma task, internalize these five rules:**

1. **Frames are the universal container.** Use frames for everything — layouts, components, wrappers. Groups are almost never what you want. Rectangles cannot have children or auto layout.
2. **Auto layout replaces manual positioning.** Once a frame has auto layout, its children's x/y are controlled by the layout engine. Use sizing properties (`FILL`, `HUG`, `FIXED`) instead of coordinates.
3. **Fonts must be loaded before text changes.** Every text content or style change requires loading the font first. This is the #1 source of errors.
4. **Properties are immutable.** Fills, strokes, and effects cannot be mutated in place. You must replace the entire property value, not modify sub-properties.
5. **Verify before modifying.** Always check a node's type and current state before changing it. An instance behaves differently from a frame. A node may have been deleted.

For deeper coverage on any topic, read the corresponding reference file in `references/`.

**Large sessions:** If the task involves a component set with 8+ variants, an unknown tree depth, or is likely to require 100+ tool calls, use the `/figma-sub-agents` skill to delegate the Discovery phase to a sub-agent. This keeps the orchestrator's context clean and prevents attention drift during high-volume binding passes.

---

## Container Selection: Frame vs Group vs Section

**Use a Frame** for virtually everything — layouts, wrappers, components, anything that needs fills, auto layout, clip content, constraints, or effects. Frames have independent dimensions and children position relative to them.

**Use a Group** only for simple fixed-relationship groupings where you want proportional scaling. Groups auto-resize to fit children, cannot have fills/strokes/auto layout, and their children's coordinates are relative to the nearest ancestor frame (not the group). Avoid groups when possible.

**Use a Section** only for top-level canvas organization. Sections cannot be inside frames or groups. They support fills and dev status but nothing else — no auto layout, constraints, clip content, or effects. Use them to organize pages for handoff (sections define "Ready for dev" status areas in Dev Mode).

---

## Auto Layout Essentials

Auto layout is how you build responsive, well-structured designs. Read `references/auto-layout-guide.md` for the full property mapping and patterns.

### Core Concepts

**Direction**: `HORIZONTAL` (row), `VERTICAL` (column), or `NONE` (no auto layout). Set direction on the parent frame.

**Spacing**: `itemSpacing` controls gap between children. Padding is per-side (`paddingTop/Right/Bottom/Left`). Gap can be set to `Auto` for `space-between` behavior (achieved via `primaryAxisAlignItems = 'SPACE_BETWEEN'`).

**Alignment**: Set on the parent, not on children. 9-position grid (3×3) when using numeric gap. Only counter-axis alignment when using space-between.

**Sizing** (the most important concept):
- **HUG** — frame shrinks to fit its children. Cannot hug if a child fills on the same axis.
- **FILL** — child stretches to fill parent. The parent must have auto layout. This is `layoutSizingHorizontal/Vertical = 'FILL'` on the child.
- **FIXED** — explicit size. Use `resize()` to set dimensions.

**Key rule**: A parent cannot HUG on an axis where a child is set to FILL. One of them must be FIXED.

### Absolute Positioning Within Auto Layout

To make a child ignore the flow (like CSS `position: absolute`), set `layoutPositioning = 'ABSOLUTE'` on the child. It stays nested in the frame but uses constraints instead of auto layout rules. Useful for overlapping badges, floating elements, or decorative layers.

### Wrap Mode

Only works on horizontal auto layout. Items that overflow wrap to the next line. Separate horizontal and vertical gap values apply. Set `layoutWrap = 'WRAP'` on the parent frame.

### Common Auto Layout Mistakes

- Setting `x`/`y` on a child inside auto layout — the layout engine controls position. Use alignment and spacing instead.
- Trying to FILL a child inside a HUG parent on the same axis — contradiction.
- Setting child sizing properties before the parent has auto layout enabled — causes errors.
- Forgetting that removing auto layout (`layoutMode = 'NONE'`) does NOT restore children to their original positions.

---

## Component Architecture

Components are Figma's reusability system. Read `references/components-and-variants.md` for the full guide.

### Hierarchy

- **Main component** (◆) — the source of truth. Edit it and all instances update.
- **Instance** (◇) — a linked copy. Can override certain properties.
- **Component set** — a dashed-border container holding multiple variants of one component.

### Variant Properties

Variants define axes of variation within a component set. Common axes: Size (S/M/L), State (Default/Hover/Pressed/Disabled), Type (Primary/Secondary/Outline). Variant names follow `Property=Value, Property=Value` format.

### Component Properties (Non-Variant)

Three property types are available via the plugin API:
- **Boolean** — toggles layer visibility only (nothing else). Example: show/hide an icon.
- **Text** — exposes editable text content. Example: button label.
- **Instance swap** — allows swapping nested component instances. Example: changing an icon.

A fourth type, **Slot** (open content areas where users can freely add/remove/reorder any content), exists in the Figma UI but has no plugin API support — it cannot be created or managed programmatically. Do not confuse slots with `isExposedInstance` (which only surfaces nested instance properties at the parent level) or with INSTANCE_SWAP properties (which restrict swapping to a picker of components).

**Critical gotcha**: Boolean, Text, and Instance Swap property names include a `#uniqueId` suffix (e.g., `'Label#12:0'`). Variant properties do not have this suffix. Always use the full suffixed name in API calls.

### Atomic Design in Figma

Build design systems bottom-up:
1. **Tokens** (variables/styles) — colors, spacing, typography
2. **Atoms** (primitive components) — icons, buttons, badges, inputs
3. **Molecules** (compound components) — search bars (input + button + icon), card headers
4. **Organisms** (complex components) — navigation bars, card grids, modals

Every sub-element should be a component for cascading updates. Prefix internal-only components with `_` or `.` to hide them from the library Assets panel.

### Naming Convention

Use slash `/` separators for hierarchy: `Button/Primary/Large`. This creates nested groups in the Assets panel. Use consistent naming across the file.

### Working With Instances

- Instances cannot have children added, removed, or reordered.
- Overrides transfer between instance swaps when **layer names match**.
- Check `node.type` before modifying — instance behavior differs from frame behavior.
- Detaching an instance converts it to a frame and loses all component linkage.
- Swapping `mainComponent` clears all overrides on nested instances.

---

## Text Operations

**Font loading is mandatory.** This is the single most common error source.

### The Correct Sequence

1. Load the font: `loadFontAsync({ family: 'Inter', style: 'Regular' })`
2. Set the font on the node (if changing from default)
3. Set the text content (`.characters`)

If you skip step 1, you get `"Cannot write to node with unloaded font"`. If you load a different font than what's currently on the node and try to set `.characters` without changing `.fontName` first, the error references the old font — confusing but logical.

### Mixed-Style Text

A text node can have different fonts/sizes/colors on different character ranges. When modifying such text, you must load ALL fonts present in the node, not just the one you're changing to. Use `getStyledTextSegments` to discover which fonts are in use.

### Text Sizing Modes

- `NONE` — fixed size box, text overflows
- `WIDTH_AND_HEIGHT` — frame resizes to fit all text
- `HEIGHT` — width is fixed, height adjusts (most common for paragraphs)
- `TRUNCATE` — fixed size with ellipsis via `textTruncation: 'ENDING'` and `maxLines`

### Properties That DON'T Require Font Loading

Fills, strokes, stroke weight, stroke alignment, and opacity can be changed without loading fonts.

---

## Variables and Design Tokens

Variables are Figma's implementation of design tokens. Read `references/variables-and-styles.md` for the full token architecture guide.

### Four Variable Types

| Type | Applies to |
|------|-----------|
| COLOR | Fills, strokes, shadow/effect colors |
| FLOAT (number) | Corner radius, dimensions, spacing, padding, font size, line height, opacity, stroke weight |
| STRING | Text content, font family, font style |
| BOOLEAN | Layer visibility |

### Three-Tier Token Architecture

1. **Primitives** — raw values (`blue/500 = #2196F3`, `space/4 = 16`). Hidden from library consumers.
2. **Semantic tokens** — purpose-based names aliasing primitives (`color/surface/primary → neutral/100`). Modes (light/dark) defined here.
3. **Component tokens** (optional) — scoped to specific components.

### Modes

Modes let one variable resolve to different values based on context — light/dark themes, responsive breakpoints, locale variants. Mode resolution walks up the node tree: check node → parent → grandparent → page → collection default.

### Variables vs Styles

**Variables** = single values with modes and aliasing. Use for colors, spacing, sizing, radii.
**Styles** = composite values (gradient fills, shadow stacks, full typography definitions). Use for text styles, complex effects, multi-fill layers.

Variables cannot represent gradients, multiple fills, image fills, or blend modes. Use styles for those.

---

## File Organization Best Practices

### Page Structure

- **Cover page** — thumbnail with file name, status, last updated
- **Design pages** — organized by feature or flow
- **Component pages** — all components with documentation
- **Playground/Sandbox** — experimentation area

### Within Pages

Use **sections** (`SectionNode`) to group related designs. Sections define scope for Dev Mode and can be marked "Ready for dev". Space designs consistently with a grid approach (e.g., 100px between frames).

### Naming Layers

Name every layer meaningfully. Unnamed `Frame 47` layers are unusable for developers. Good layer names match what the element represents: `Header`, `SearchInput`, `NavItem`, `ProfileAvatar`. This also matters for override preservation during instance swaps — names must match.

---

## Collaboration Features

### Comments

Comments pin to top-level frames/components/groups and move with them. They cannot attach to nested layers. Anyone with view access can comment. Comments support threading and resolution. Resolved comments hide from canvas but aren't deleted.

### Annotations

Created on design elements to communicate specs. Support plain text and auto-updating property references (e.g., "Corner radius: 8px" updates if you change it). Annotations are color-coded by category and appear as green dots in Dev Mode.

### Dev Mode

Surfaces component info, generated CSS/iOS/Android code, layout specs, and variable bindings. Key concepts:
- **Sections** organize what developers see — content outside sections collapses.
- **Dev statuses**: Ready for dev, Completed, Changed.
- **Compare Changes** shows before/after property diffs on a timeline.
- **Component Playground** lets devs experiment with properties without modifying the file.

### Sections for Organization

Sections are top-level only (cannot nest inside frames). Use them for: feature groupings, handoff areas, flow organization, and status tracking. They're the primary organizing unit for Dev Mode.

---

## Critical Gotchas Quick Reference

Read `references/gotchas-and-edge-cases.md` for the full list. The most impactful ones:

### Immutable Properties

Fills, strokes, effects, and layout grids are **readonly frozen objects**. You cannot do `node.fills[0].color.r = 1`. You must clone the entire array, modify the clone, and reassign: `node.fills = modifiedClone`. This applies universally.

### Rectangles Are Not Frames

Rectangles (`RectangleNode`) cannot have children, auto layout, or clip content. If you need any container behavior, use a frame. A common mistake: creating a rectangle as a "card background" then trying to add children — use a frame with a fill instead.

### Colors Are 0–1 Floats

Figma colors use `{r, g, b, a}` with values from 0 to 1, not 0 to 255. `#FF0000` = `{r: 1, g: 0, b: 0, a: 1}`.

### Instance Limitations

- Cannot add/remove/reorder children
- `mainComponent` swap clears nested instance overrides
- Remote library components are read-only
- `detachInstance()` detaches all ancestor instances, not just the target

### Auto Layout Parent Required

Setting `layoutSizingHorizontal`, `layoutSizingVertical`, `layoutGrow`, or `layoutAlign` on a node that isn't inside an auto layout frame throws an error. Enable auto layout on the parent first.

### Min/Max Constraints

`minWidth`, `maxWidth`, `minHeight`, `maxHeight` only work on auto layout frames and their direct children. Setting them on other nodes throws `"Can only set maxHeight on auto layout nodes."`.

### Coordinate Systems

- `x`/`y` = relative to parent
- `absoluteBoundingBox` = canvas coordinates
- Inside groups, coordinates are relative to the nearest ancestor **frame**, not the group
- Inside auto layout, `x`/`y` are managed by the engine — don't set them manually

### SectionNode Restrictions

Sections cannot be inside frames. They cannot have auto layout, constraints, clip content, corner radius, or effects. Only fills and dev status.

### Image Handling

Images in Figma are **fills on frames/rectangles**, not standalone nodes. To add an image: create a frame or rectangle, then set its fill to `{ type: 'IMAGE', imageHash: hash, scaleMode: 'FILL' }`. Max image size is 4096×4096.

---

## Agent Workflow Patterns

### Prototype One, Then Batch

When creating multiple similar elements, build one correctly first. Verify it looks right. Then replicate the pattern for the rest. This avoids cascading errors across many elements.

### Verify Type Before Modify

Always check `node.type` before operating on a node. An InstanceNode has different capabilities than a FrameNode. A TextNode requires font loading. A GroupNode can't have fills.

### Fail Fast

If an operation fails twice, stop and explain the blocker to the user. Don't retry the same failing approach — investigate why it's failing (wrong node type? missing font? auto layout conflict?).

### Prefer Cloning Over Building From Scratch

If a similar element exists, clone it and modify rather than creating from scratch. This preserves structure, styling, and component linkage.

### Use Composite Operations When Available

If the MCP provides batch or composite tools (e.g., creating a frame with auto layout in one call), prefer those over sequential single-property calls. This reduces round-trips and errors.

### Ask For Reference Material

When the user asks for a complex design, ask for screenshots, design specs, or reference components if the context is unclear. Don't guess at spacing, colors, or typography — ask.

---

## Reference Files

Read these for detailed coverage on specific topics:

| File | When to read |
|------|-------------|
| `references/auto-layout-guide.md` | Building any responsive layout, nesting auto layout frames, using wrap or absolute positioning |
| `references/components-and-variants.md` | Creating components, variant structures, component properties, atomic design patterns |
| `references/variables-and-styles.md` | Setting up design tokens, creating variable collections/modes, choosing variables vs styles |
| `references/gotchas-and-edge-cases.md` | Debugging errors, understanding why something failed, edge cases with fills/text/instances |
| `references/collaboration-and-organization.md` | Adding comments/annotations, organizing files with sections, Dev Mode preparation, branching |

**Post-session**: After completing a large Figma session (50+ tool calls), run `/analyze-session` to capture efficiency metrics, error patterns, and improvement recommendations.
