---
name: tailwindcss-interactivity
description: "Interactivity utilities Tailwind CSS v4.1. Cursor (cursor-*), Scroll (scroll-smooth, scroll-snap-*, overscroll-*), User select (select-*), Pointer events (pointer-events-*), Touch action, Resize, Caret color, Accent color."
user-invocable: false
---

# Tailwind CSS Interactivity Utilities

Comprehensive utilities for controlling user interaction behaviors and cursor styles in Tailwind CSS v4.1.

## Categories

### Cursor Utilities
Control the cursor appearance on elements
- `cursor-*` - Standard cursors (auto, default, pointer, wait, text, move, help, not-allowed, none, etc.)
- Support for resize cursors (col-resize, row-resize, n-resize, e-resize, s-resize, w-resize, ne-resize, nw-resize, se-resize, sw-resize, ew-resize, ns-resize, nesw-resize, nwse-resize)
- Zoom cursors (zoom-in, zoom-out)
- Grab cursors (grab, grabbing)
- Special cursors (context-menu, progress, cell, crosshair, vertical-text, alias, copy, no-drop, all-scroll)

### Scroll Behavior & Snap
Manage scrolling and snap behavior
- `scroll-smooth` - Enable smooth scrolling
- `scroll-snap-type` - Define snap container behavior (snap-none, snap-x, snap-y, snap-both)
- `scroll-snap-align` - Position snap points (snap-start, snap-center, snap-end)
- `scroll-snap-stop` - Force snap stops (snap-always, snap-normal)
- `overscroll-behavior` - Control overscroll area (overscroll-auto, overscroll-contain, overscroll-none)
- Support for axis-specific variants (x, y)

### User Selection
Control text selection behavior
- `select-none` - Disable text selection
- `select-text` - Allow text selection
- `select-all` - Select all text when clicked
- `select-auto` - Browser default selection

### Pointer Events
Control element interactivity
- `pointer-events-none` - Element cannot be interacted with
- `pointer-events-auto` - Element is interactive (default)

### Touch Action
Define how touch gestures are handled
- `touch-auto` - Browser default touch handling
- `touch-none` - Disable all touch behaviors
- `touch-pan-x` - Allow horizontal panning only
- `touch-pan-y` - Allow vertical panning only
- `touch-manipulation` - Allow panning and zoom only (no double-tap zoom)
- Support for directional variants (pan-up, pan-down, pan-left, pan-right, pinch-zoom)

### Resize
Control element resize behavior
- `resize-none` - Disable resizing
- `resize` - Allow resizing in both directions
- `resize-y` - Allow vertical resizing only
- `resize-x` - Allow horizontal resizing only

### Caret Color
Set text input cursor color
- `caret-*` - Color utilities for input/textarea cursor
- Supports all Tailwind colors and opacity modifiers
- Full dark mode support

### Accent Color
Define accent color for form controls
- `accent-*` - Color utilities for checkboxes, radios, and range inputs
- Supports all Tailwind colors and opacity modifiers
- Full dark mode support

## Resources
- [Official Tailwind CSS Docs](https://tailwindcss.com/)
- [Cursor Documentation](https://tailwindcss.com/docs/cursor)
- [Scroll Behavior Documentation](https://tailwindcss.com/docs/scroll-behavior)
- [Scroll Snap Documentation](https://tailwindcss.com/docs/scroll-snap)
- [User Select Documentation](https://tailwindcss.com/docs/user-select)
- [Pointer Events Documentation](https://tailwindcss.com/docs/pointer-events)
- [Touch Action Documentation](https://tailwindcss.com/docs/touch-action)
- [Resize Documentation](https://tailwindcss.com/docs/resize)
- [Caret Color Documentation](https://tailwindcss.com/docs/caret-color)
- [Accent Color Documentation](https://tailwindcss.com/docs/accent-color)
