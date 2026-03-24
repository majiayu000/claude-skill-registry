---
name: opentui-operative
description: OpenTUI terminal UI library reference. Use when working with @opentui/core, terminal UIs, renderables, Yoga layouts, or Zig-native rendering.
user-invocable: false
---

# OpenTUI Operative

> Comprehensive reference for building terminal UIs with OpenTUI (@opentui/core).
> Source: https://opentui.com/docs/ — all 29 documentation pages.

---

## Trigger

Use when: user mentions "OpenTUI", "TUI", "terminal UI", "@opentui/core", renderables, or works on files importing from `@opentui/core`.

## Role

You are an expert in OpenTUI — a TypeScript library for building rich terminal interfaces with Yoga-powered flexbox layouts and Zig-native rendering. You know every API surface, every gotcha, and every pattern. You write correct OpenTUI code on the first attempt.

---

## 1. Quick Start

**Requires Bun.**

```bash
bun add @opentui/core
```

```typescript
import { createCliRenderer, Text } from "@opentui/core"

const renderer = await createCliRenderer({ exitOnCtrlC: true })
renderer.root.add(Text({ content: "Hello, OpenTUI!", fg: "#00FF00" }))
```

Run with `bun index.ts`. Press Ctrl+C to exit.

---

## 2. Renderer

The `CliRenderer` drives everything — terminal output, input events, render loop, and context for renderables.

### Creation

```typescript
import { createCliRenderer } from "@opentui/core"

const renderer = await createCliRenderer({
  exitOnCtrlC: true,   // default: true
  targetFps: 30,       // default: 30
})
```

The factory:
1. Loads the native Zig rendering library
2. Configures terminal (mouse, keyboard protocol, alternate screen)
3. Returns an initialised `CliRenderer`

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `exitOnCtrlC` | `boolean` | `true` | Destroy renderer on Ctrl+C |
| `exitSignals` | `NodeJS.Signals[]` | — | Signals that trigger cleanup |
| `targetFps` | `number` | `30` | Target FPS for render loop |
| `maxFps` | `number` | `60` | Max FPS for immediate re-renders |
| `useMouse` | `boolean` | `true` | Enable mouse input/tracking |
| `autoFocus` | `boolean` | `true` | Focus nearest focusable on left click |
| `enableMouseMovement` | `boolean` | `true` | Track mouse movement (not just clicks) |
| `useAlternateScreen` | `boolean` | `true` | Use terminal alternate screen buffer |
| `consoleOptions` | `ConsoleOptions` | — | Built-in console overlay options |
| `openConsoleOnError` | `boolean` | `true` | Auto-open console on errors (dev only) |
| `onDestroy` | `() => void` | — | Callback on renderer destruction |

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `root` | `RootRenderable` | Root of the component tree (fills terminal) |
| `width` | `number` | Current width in columns |
| `height` | `number` | Current height in rows |
| `console` | `TerminalConsole` | Built-in console overlay |
| `keyInput` | `KeyHandler` | Keyboard input handler |
| `isRunning` | `boolean` | Whether render loop is active |
| `isDestroyed` | `boolean` | Whether renderer is destroyed |
| `currentFocusedRenderable` | `Renderable \| null` | Currently focused component |

### Render Loop Control

**Automatic mode (default)** — re-renders only when the component tree changes:
```typescript
const renderer = await createCliRenderer()
renderer.root.add(Text({ content: "Static content" }))
// No start() needed — renders automatically on tree changes
```

**Continuous mode** — runs at targetFps:
```typescript
renderer.start()   // Begin continuous rendering
renderer.stop()    // Stop continuous rendering
```

**Live rendering** — for animations:
```typescript
renderer.requestLive()   // Request continuous rendering
renderer.dropLive()      // Drop live rendering request
```

**Pause/Suspend:**
```typescript
renderer.pause()
renderer.suspend()
renderer.resume()
```

### Events

```typescript
renderer.on("resize", (width, height) => { /* terminal resized */ })
renderer.on("destroy", () => { /* renderer destroyed */ })
renderer.on("selection", (selection) => { /* text selected */ })
```

### Cursor Control

```typescript
renderer.setCursorPosition(10, 5, true)
renderer.setCursorStyle("block", true)    // block | underline | line
renderer.setCursorColor(RGBA.fromHex("#FF0000"))
```

### Cleanup

```typescript
renderer.destroy()
```

**CRITICAL:** Always call `destroy()` when finished. This restores terminal state (mouse tracking, raw mode, alternate screen). OpenTUI does NOT automatically clean up on `process.exit` or unhandled errors.

### Debug Overlay

```typescript
renderer.toggleDebugOverlay()

import { DebugOverlayCorner } from "@opentui/core"
renderer.configureDebugOverlay({ enabled: true, corner: DebugOverlayCorner.topRight })
```

---

## 3. Renderables (Imperative API)

Renderables are the building blocks of the UI. Each represents a visual element using Yoga layout engine for positioning.

### Creating Renderables

```typescript
import { TextRenderable, BoxRenderable } from "@opentui/core"

// Constructor: new XxxRenderable(ctx: RenderContext, options)
// ctx IS the renderer itself (or any object implementing RenderContext)
const greeting = new TextRenderable(renderer, {
  id: "greeting",
  content: "Hello!",
  fg: "#00FF00",
})
renderer.root.add(greeting)
```

### Available Renderables

| Class | Description |
|-------|-------------|
| `BoxRenderable` | Container with border, background, and layout |
| `TextRenderable` | Read-only styled text display |
| `InputRenderable` | Single-line text input |
| `TextareaRenderable` | Multi-line editable text |
| `SelectRenderable` | Dropdown/list selection |
| `TabSelectRenderable` | Horizontal tab selection |
| `ScrollBoxRenderable` | Scrollable container |
| `ScrollBarRenderable` | Standalone scroll bar control |
| `CodeRenderable` | Syntax-highlighted code display |
| `LineNumberRenderable` | Line number gutter |
| `DiffRenderable` | Unified or split diff viewer |
| `ASCIIFontRenderable` | ASCII art font display |
| `FrameBufferRenderable` | Raw framebuffer for custom graphics |
| `MarkdownRenderable` | Markdown renderer |
| `SliderRenderable` | Numeric slider control |

### The Renderable Tree

```typescript
const container = new BoxRenderable(renderer, {
  id: "container",
  flexDirection: "column",
  padding: 1,
})

const title = new TextRenderable(renderer, { id: "title", content: "My App" })
const body = new TextRenderable(renderer, { id: "body", content: "Content" })

container.add(title)
container.add(body)
renderer.root.add(container)

// Remove a child — MUST use string ID, not the renderable instance
container.remove("body")
```

### CRITICAL: remove() API

**`remove(id: string): void`** — the ONLY signature. Always pass a string ID.

```typescript
// CORRECT
container.remove("body")
container.remove(child.id)     // .id returns the auto-generated or explicit ID

// WRONG — will fail at runtime
container.remove(child)        // passes object, not string
```

Every renderable gets an auto-generated `.id` from a static counter. If you set `id` in options, that becomes the ID. Otherwise it's auto-generated. Access via `renderable.id`.

### Finding Renderables

```typescript
const title = container.getRenderable("title")              // Direct child by ID
const deep = container.findDescendantById("nested-input")   // Recursive search
const children = container.getChildren()                     // All children
```

### Visibility

```typescript
panel.visible = false   // Hides AND removes from layout (like CSS display: none)
panel.visible = true
```

### Opacity

```typescript
panel.opacity = 0.5   // Affects renderable and all children
```

### Z-Index

```typescript
const overlay = new BoxRenderable(renderer, {
  position: "absolute",
  zIndex: 100,   // Higher values render on top
})
```

### Translation (Visual Offset)

```typescript
renderable.translateX = 10
renderable.translateY = -5
// Moves visually without affecting layout
```

### Destroying Renderables

```typescript
renderable.destroy()              // Remove from parent, free resources
container.destroyRecursively()    // Destroy self and all children
```

### Lifecycle Methods (Custom Renderables)

```typescript
class CustomRenderable extends Renderable {
  onUpdate(deltaTime: number) { /* called each frame before render */ }
  onResize(width: number, height: number) { /* dimensions changed */ }
  onRemove() { /* removed from parent — cleanup here */ }
  renderSelf(buffer: OptimizedBuffer, deltaTime: number) { /* custom drawing */ }
}
```

### Live Rendering

```typescript
const box = new AnimatedBox(renderer, {
  live: true,   // Enable continuous rendering for this renderable
})
```

### Buffered Rendering

```typescript
const complex = new BoxRenderable(renderer, {
  buffered: true,   // Render to offscreen buffer first
  renderAfter: (buffer) => {
    buffer.fillRect(0, 0, 10, 5, RGBA.fromHex("#FF0000"))
  },
})
```

---

## 4. Constructs (Declarative API)

Factory functions that create VNodes — lightweight descriptions of components. VNodes become actual Renderables when added to the tree.

```typescript
import { Box, Text, Input } from "@opentui/core"

Box(
  { width: 40, height: 10, borderStyle: "rounded", padding: 1 },
  Text({ content: "Welcome!" }),
  Input({ placeholder: "Enter your name..." }),
)
```

### Available Constructs

`ASCIIFont`, `Box`, `Code`, `FrameBuffer`, `Input`, `ScrollBox`, `Select`, `TabSelect`, `Text`, `SyntaxStyle`

**NOT yet available as constructs** (use Renderable API): `Textarea`, `ScrollBar`, `Slider`, `Markdown`, `LineNumber`, `Diff`

### Method Chaining on VNodes

VNodes queue method calls — applied after the component is created:
```typescript
const input = Input({ placeholder: "Name..." })
input.focus()   // Queued, applied when added to tree
```

### Delegation

Routes method/property calls to descendant IDs:
```typescript
import { delegate } from "@opentui/core"

function LabeledInput(props) {
  return delegate(
    { focus: `${props.id}-input` },   // focus() routes to child input
    Box(
      { flexDirection: "row" },
      Text({ content: props.label }),
      Input({ id: `${props.id}-input`, placeholder: props.placeholder }),
    ),
  )
}

const field = LabeledInput({ id: "name", label: "Name:", placeholder: "..." })
field.focus()   // Delegates to the inner input
```

### Mixing Renderables and Constructs

```typescript
const container = new BoxRenderable(renderer, { id: "root", flexDirection: "column" })
container.add(Text({ content: "Title" }), Input({ placeholder: "Type here..." }))
renderer.root.add(container)
```

---

## 5. Layout (Yoga Flexbox)

### Flex Direction

```typescript
{ flexDirection: "column" }       // vertical (default)
{ flexDirection: "row" }          // horizontal
{ flexDirection: "row-reverse" }
{ flexDirection: "column-reverse" }
```

### Justify Content (Main Axis)

`flex-start` | `flex-end` | `center` | `space-between` | `space-around` | `space-evenly`

### Align Items (Cross Axis)

`flex-start` | `flex-end` | `center` | `stretch` (default) | `baseline`

### Sizing

```typescript
{ width: 30, height: 10 }        // Fixed (characters/rows)
{ width: "100%", height: "50%" }  // Percentage
{ flexGrow: 1, flexShrink: 0 }   // Flex behaviour
{ minWidth: 20, maxHeight: 30 }   // Constraints
```

### Positioning

```typescript
{ position: "relative" }   // default — flows in layout
{ position: "absolute", left: 10, top: 5 }   // removed from flow
```

### Spacing

```typescript
{ padding: 2 }                          // All sides
{ paddingTop: 1, paddingX: 4 }          // Specific sides/axes
{ margin: 1 }                           // Same pattern
```

### Gap

```typescript
{ gap: 1 }   // Space between children
```

---

## 6. Component Reference

### BoxRenderable

Container with borders, backgrounds, and layout.

```typescript
new BoxRenderable(renderer, {
  id: "panel",
  width: 30, height: 10,
  backgroundColor: "#333366",
  borderStyle: "rounded",       // single | double | rounded | heavy
  borderColor: "#FFFFFF",
  border: true,                 // must be true for border to show
  title: "Panel Title",
  titleAlignment: "center",    // left | center | right
  padding: 1,
  gap: 1,
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "flex-start",
  flexGrow: 1,
})
```

**Mouse events:** `onMouseDown`, `onMouseOver`, `onMouseOut`, `onMouseUp`, `onMouseMove`, `onMouseDrag`, `onMouseDragEnd`, `onMouseDrop`, `onMouseScroll`, `onMouse` (catch-all).

Mouse events bubble up. Stop with `event.stopPropagation()`.

### TextRenderable

Read-only styled text.

```typescript
new TextRenderable(renderer, {
  content: "Hello!",           // string or StyledText
  fg: "#00FF00",               // string | RGBA
  bg: "#000000",
  attributes: TextAttributes.BOLD | TextAttributes.UNDERLINE,
  selectable: true,
})
```

**Text attributes** (combine with bitwise OR): `BOLD`, `DIM`, `ITALIC`, `UNDERLINE`, `BLINK`, `INVERSE`, `HIDDEN`, `STRIKETHROUGH`

**Template literals:**
```typescript
import { t, bold, fg } from "@opentui/core"
text.content = t`${bold("Hello")} ${fg("#FF0000", "world")}!`
```

Helpers: `bold`, `dim`, `italic`, `underline`, `blink`, `reverse`, `strikethrough`, `fg`, `bg`

**GOTCHA:** `TextRenderable.content` returns a `StyledText` object, not a plain string. To read the raw text: `text.content.chunks[0].text`.

### SelectRenderable

Vertical list for choosing options.

```typescript
import { SelectRenderable, SelectRenderableEvents } from "@opentui/core"

const select = new SelectRenderable(renderer, {
  options: [
    { name: "Option 1", description: "First option", value: "one" },
    { name: "Option 2", description: "Second option", value: "two" },
  ],
  backgroundColor: theme.background,       // default is transparent (appears black!)
  selectedBackgroundColor: theme.highlight,
  selectedTextColor: theme.text,
  textColor: theme.text,
  descriptionColor: theme.textMuted,
  showDescription: true,
  showScrollIndicator: true,
  wrapSelection: false,
  fastScrollStep: 5,
  flexGrow: 1,
})
renderer.root.add(select)
select.focus()   // REQUIRED for keyboard input
```

**Keyboard controls:**

| Key | Action |
|-----|--------|
| Up / k | Move selection up |
| Down / j | Move selection down |
| Shift+Up / Shift+Down | Fast scroll (5 items) |
| Enter | Select current item |

**Events:**

```typescript
// ITEM_SELECTED: fires on Enter
select.on(SelectRenderableEvents.ITEM_SELECTED, (index: number, option: SelectOption) => {
  console.log(option.value)
})

// SELECTION_CHANGED: fires when highlighted item changes
select.on(SelectRenderableEvents.SELECTION_CHANGED, (index: number, option: SelectOption) => {
  console.log("Now highlighting:", option.name)
})
```

**SelectOption interface:**
```typescript
interface SelectOption {
  name: string
  description: string
  value?: any
}
```

**Programmatic methods:**
- `getSelectedIndex()` / `getSelectedOption()`
- `setSelectedIndex(n)` / `moveUp()` / `moveDown()` / `selectCurrent()`
- Dynamic updates: set `options`, `showDescription`, `showScrollIndicator`, `wrapSelection` as properties

**GOTCHA:** `backgroundColor` defaults to transparent — set it explicitly or items appear with black backgrounds.

### InputRenderable

Single-line text input.

```typescript
import { InputRenderable, InputRenderableEvents } from "@opentui/core"

const input = new InputRenderable(renderer, {
  width: 25,
  placeholder: "Enter your name...",
  value: "",
  maxLength: 1000,
  backgroundColor: "#1a1a1a",
  focusedBackgroundColor: "#222222",
  textColor: "#FFFFFF",
  cursorColor: "#00FF88",
})
input.focus()

input.on(InputRenderableEvents.INPUT, (value) => { /* every keystroke */ })
input.on(InputRenderableEvents.CHANGE, (value) => { /* on blur or Enter, if changed */ })
input.on(InputRenderableEvents.ENTER, () => { /* Enter key pressed */ })
```

### TextareaRenderable

Multi-line editable text. **No construct API yet.**

```typescript
import { TextareaRenderable } from "@opentui/core"

const textarea = new TextareaRenderable(renderer, {
  width: 50, height: 6,
  placeholder: "Type notes here...",
  wrapMode: "word",           // none | char | word
  backgroundColor: "#1a1a1a",
  focusedBackgroundColor: "#222222",
  textColor: "#FFFFFF",
  cursorColor: "#00FF88",
  onSubmit: () => { console.log(textarea.plainText) },
  onContentChange: () => { /* content changed */ },
  onCursorChange: () => { /* cursor moved */ },
  keyBindings: [{ name: "return", ctrl: true, action: "submit" }],
})
textarea.focus()
```

**Properties:** `plainText` (string), `cursorOffset` (number)

### TabSelectRenderable

Horizontal tab selection.

```typescript
import { TabSelectRenderable, TabSelectRenderableEvents } from "@opentui/core"

const tabs = new TabSelectRenderable(renderer, {
  width: 60,
  options: [
    { name: "Tab 1", description: "First tab" },
    { name: "Tab 2", description: "Second tab" },
  ],
  tabWidth: 20,
  showScrollArrows: true,
  showDescription: true,
  showUnderline: true,
  wrapSelection: false,
})
tabs.focus()

tabs.on(TabSelectRenderableEvents.ITEM_SELECTED, (index, option) => { })
tabs.on(TabSelectRenderableEvents.SELECTION_CHANGED, (index, option) => { })
```

**Keys:** Left/`[` = prev, Right/`]` = next, Enter = select

**Methods:** `getSelectedIndex()`, `setSelectedIndex(n)`, `setOptions(array)`

### ScrollBoxRenderable

Scrollable container.

```typescript
const scrollbox = new ScrollBoxRenderable(renderer, {
  width: 60, height: 20,
  scrollX: false,
  scrollY: true,            // default
  stickyScroll: false,      // "bottom" | "top" | "left" | "right" when truthy
  viewportCulling: true,    // Render only visible children (default)
})
```

**Keyboard (when focused):** Arrow keys, Page Up/Down, Home, End.

**Methods:**
- `scrollBy()` — relative scrolling by lines, pixels, or viewport
- `scrollTo()` — absolute positioning

**Internal structure:** `wrapper`, `viewport`, `content`, `horizontalScrollBar`, `verticalScrollBar`

**Sub-component options:** `rootOptions`, `wrapperOptions`, `viewportOptions`, `contentOptions`, `scrollbarOptions`

### ScrollBarRenderable

Standalone scrollbar. **No construct API yet.**

```typescript
const scrollbar = new ScrollBarRenderable(renderer, {
  orientation: "vertical",   // vertical | horizontal
  height: 10,
  showArrows: true,
  trackOptions: { backgroundColor: "#222222", foregroundColor: "#888888" },
  onChange: (position) => { console.log(position) },
})
scrollbar.scrollSize = 200
scrollbar.viewportSize = 20
scrollbar.scrollPosition = 0
scrollbar.focus()
```

**Keys:** Up/Down or k/j (vertical), Left/Right or h/l (horizontal), PageUp/Down, Home/End

### SliderRenderable

Draggable slider. **No construct API yet.**

```typescript
const slider = new SliderRenderable(renderer, {
  orientation: "horizontal",   // horizontal | vertical
  width: 30, height: 1,
  min: 0, max: 100, value: 25,
  backgroundColor: "#333",
  foregroundColor: "#0f0",
  onChange: (value) => { console.log(value) },
})
```

### ASCIIFontRenderable

ASCII art font display.

```typescript
new ASCIIFontRenderable(renderer, {
  text: "Iris",
  font: "block",            // tiny | block | shade | slick | huge | grid | pallet
  color: "#FFFFFF",          // or array for gradient: ["#FF0000", "#0000FF"]
  backgroundColor: "transparent",
  selectable: false,
})
```

Both Renderable (`ASCIIFontRenderable`) and Construct (`ASCIIFont`) APIs available.

### CodeRenderable

Syntax-highlighted code with Tree-sitter.

```typescript
import { CodeRenderable, SyntaxStyle, RGBA } from "@opentui/core"

const syntaxStyle = SyntaxStyle.fromStyles({
  default: { fg: RGBA.fromHex("#E6EDF3") },
  keyword: { fg: RGBA.fromHex("#FF7B72") },
  string: { fg: RGBA.fromHex("#A5D6FF") },
  comment: { fg: RGBA.fromHex("#8B949E"), italic: true },
  function: { fg: RGBA.fromHex("#D2A8FF") },
})

const code = new CodeRenderable(renderer, {
  content: "const x = 1;",
  filetype: "typescript",
  syntaxStyle,
  streaming: false,
  conceal: true,
  selectable: true,
  wrapMode: "none",
})
```

**Token names:** `keyword`, `string`, `comment`, `function`, `operator`, `variable`, `type`, `number`, `constant`, plus `markup.*` for markdown.

### MarkdownRenderable

Markdown renderer. **No construct API yet.**

```typescript
new MarkdownRenderable(renderer, {
  content: "# Hello\n\nSome **bold** text.",
  syntaxStyle,
  conceal: true,       // Hide markdown markers
  streaming: false,    // Incremental update optimisation
  renderNode: (node) => { /* custom rendering per block */ },
})
```

### LineNumberRenderable

Line number gutter. **No construct API yet.**

```typescript
const lineNumbers = new LineNumberRenderable(renderer, {
  target: codeRenderable,   // Must implement LineInfoProvider
  minWidth: 3,
  paddingRight: 1,
  fg: "#6b7280",
  bg: "#161b22",
})

lineNumbers.setLineColor(3, "#2b6cb0")
lineNumbers.setLineSign(3, { before: ">", beforeColor: "#2b6cb0" })
```

### DiffRenderable

Unified or split diffs. **No construct API yet.**

```typescript
new DiffRenderable(renderer, {
  diff: unifiedDiffString,
  view: "unified",          // unified | split
  filetype: "typescript",
  syntaxStyle,
  showLineNumbers: true,
  addedBg: "#1a4d1a",
  removedBg: "#4d1a1a",
  addedSignColor: "#22c55e",
  removedSignColor: "#ef4444",
})
```

### FrameBufferRenderable

Low-level rendering surface.

```typescript
new FrameBufferRenderable(renderer, {
  width: 40, height: 20,
  respectAlpha: false,
})
```

**Drawing methods:** `setCell`, `setCellWithAlphaBlending`, `drawText`, `fillRect`, `drawFrameBuffer`

---

## 7. Keyboard Input

### Global Key Handler

```typescript
renderer.keyInput.on("keypress", (key: KeyEvent) => {
  console.log(key.name, key.ctrl, key.shift, key.meta)
})

renderer.keyInput.on("paste", (event: PasteEvent) => {
  console.log(event.text)
})
```

### KeyEvent Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | `string` | Key identifier (e.g. "a", "escape", "f1", "return") |
| `sequence` | `string` | Raw escape sequence |
| `ctrl` | `boolean` | Ctrl modifier |
| `shift` | `boolean` | Shift modifier |
| `meta` | `boolean` | Alt/Meta modifier |
| `option` | `boolean` | macOS Option key |

**Event methods:** `preventDefault()`, `stopPropagation()`

### Per-Renderable Key Handling

```typescript
new InputRenderable(renderer, {
  onKeyDown: (key) => {
    if (key.name === "escape") input.blur()
  },
  onPaste: (event) => { console.log(event.text) },
})
```

### Raw Input Handler

```typescript
renderer.addInputHandler((sequence) => {
  if (sequence === "\x1b[A") return true   // consumed
  return false                              // pass through
})
```

---

## 8. Focus Management

```typescript
input.focus()           // Give focus
input.blur()            // Remove focus
console.log(input.focused)   // Check state
```

**Auto-focus:** Left-clicking a renderable auto-focuses nearest focusable ancestor. Disable globally with `{ autoFocus: false }` or per-interaction with `event.preventDefault()` in `onMouseDown`.

**Events:**
```typescript
import { RenderableEvents } from "@opentui/core"
input.on(RenderableEvents.FOCUSED, () => { })
input.on(RenderableEvents.BLURRED, () => { })
```

**Internal key routing:** `focus()` uses `_internalKeyInput.onInternal()` — the renderer's internal key handler that ensures global handlers can `preventDefault` before renderable handlers process events.

---

## 9. Colours

### RGBA Class

```typescript
import { RGBA } from "@opentui/core"

RGBA.fromInts(255, 0, 0, 255)        // From integers (0-255)
RGBA.fromValues(0.0, 1.0, 0.0, 1.0)  // From normalised floats (0.0-1.0)
RGBA.fromHex("#800080")               // From hex string
RGBA.fromHex("#FF000080")             // With alpha
```

### String Colour Support

Components accept: hex strings (`"#FF0000"`), CSS colour names (`"red"`), RGBA objects, `"transparent"`.

### parseColor() Utility

```typescript
import { parseColor } from "@opentui/core"
const rgba = parseColor("#FF0000")   // Converts various formats to RGBA
```

### Common Constants

`RGBA.white`, `RGBA.black`, `RGBA.red`, `RGBA.green`, `RGBA.blue`, `RGBA.transparent`

> **Palette advisory:** When choosing hex values for OpenTUI components, prefer colours from [Reasonable Colors](https://www.reasonable.work/colors/) (`library/docs/reasonable-colors-reference.md`). The LCH-based palette is designed for consistent rendering across display types, which matters more in terminal contexts than web. Use `RGBA.fromHex()` with RC hex values directly.

---

## 10. Console Overlay

OpenTUI captures all `console.log/info/warn/error/debug` calls to prevent interference with the UI.

```typescript
const renderer = await createCliRenderer({
  consoleOptions: {
    position: ConsolePosition.BOTTOM,   // TOP | BOTTOM | LEFT | RIGHT
    sizePercent: 30,
  },
})

renderer.console.toggle()
```

**Keyboard (when focused):** Arrow keys to scroll, `+`/`-` to resize.

**Env vars:**
- `OTUI_USE_CONSOLE=false` — disable capture
- `SHOW_CONSOLE=true` — start visible
- `OTUI_DUMP_CAPTURES=true` — output on exit

---

## 11. Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OTUI_USE_ALTERNATE_SCREEN` | `true` | Alternate screen buffer |
| `OTUI_SHOW_STATS` | `false` | Debug overlay at startup |
| `OTUI_DEBUG` | `false` | Debug input capture |
| `OTUI_NO_NATIVE_RENDER` | `false` | Disable native rendering |
| `OTUI_DUMP_CAPTURES` | `false` | Dump captured output on exit |
| `OTUI_OVERRIDE_STDOUT` | `true` | Override stdout (debug) |
| `OTUI_USE_CONSOLE` | `true` | Enable console capture |
| `SHOW_CONSOLE` | `false` | Show console at startup |
| `OTUI_TS_STYLE_WARN` | `false` | Warn on missing syntax styles |
| `OTUI_TREE_SITTER_WORKER_PATH` | `""` | Tree-sitter worker path |
| `OTUI_DEBUG_FFI` | `false` | Debug logging for FFI |
| `OTUI_TRACE_FFI` | `false` | Tracing for FFI |
| `OPENTUI_FORCE_WCWIDTH` | `false` | Use wcwidth for char widths |
| `OPENTUI_FORCE_UNICODE` | `false` | Force Mode 2026 Unicode |
| `OPENTUI_NO_GRAPHICS` | `false` | Disable Kitty graphics detection |
| `OPENTUI_FORCE_NOZWJ` | `false` | No ZWJ width method |
| `OPENTUI_FORCE_EXPLICIT_WIDTH` | — | Force explicit width detection |

---

## 12. Tree-sitter Integration

### Global Registration

```typescript
import { addDefaultParsers } from "@opentui/core"

addDefaultParsers([{
  filetype: "python",
  wasm: "https://github.com/tree-sitter/tree-sitter-python/releases/download/v0.23.6/tree-sitter-python.wasm",
  queries: {
    highlights: ["https://raw.githubusercontent.com/.../highlights.scm"],
  },
}])
```

### Per-Client

```typescript
const client = new TreeSitterClient({ dataPath: "./parsers" })
client.addFiletypeParser({ filetype, wasm, queries })
```

### Utilities

```typescript
pathToFiletype("/foo/bar.ts")   // "typescript"
extToFiletype(".py")            // "python"
```

---

## 13. Framework Bindings

### Solid.js (`@opentui/solid`)

```bash
bun install solid-js @opentui/solid
```

JSX components (snake_case): `text`, `box`, `scrollbox`, `input`, `textarea`, `select`, `tab_select`, `code`, `diff`, `markdown`, `ascii_font`, `line_number`

Hooks: `useRenderer()`, `useKeyboard()`, `useTerminalDimensions()`, `onResize()`, `usePaste()`, `useSelectionHandler()`, `useTimeline()`

Entry: `render(<App />)` or `testRender(<App />)` for testing.

### React (`@opentui/react`)

```bash
bun add @opentui/react @opentui/core react
```

JSX components (kebab-case): `<text>`, `<box>`, `<scrollbox>`, `<input>`, `<textarea>`, `<select>`, `<tab-select>`, `<code>`, `<diff>`, `<markdown>`, `<ascii-font>`, `<line-number>`

Hooks: `useRenderer()`, `useKeyboard()`, `useOnResize()`, `useTerminalDimensions()`, `useTimeline()`

Entry: `createRoot(renderer).render(<App />)`

---

## 14. Common Patterns

### Screen Pattern (Full-screen Views)

```typescript
const CONTAINER_ID = "my-screen-root"

class MyScreen {
  private renderer: Renderer
  private keyHandler?: (key: KeyEvent) => void

  constructor(renderer: Renderer) {
    this.renderer = renderer
  }

  async render(): Promise<Result> {
    return new Promise((resolve) => {
      const container = new BoxRenderable(this.renderer, {
        id: CONTAINER_ID,
        flexDirection: "column",
        width: "100%",
        height: "100%",
        backgroundColor: "#1a1a2e",
      })

      // ... build UI tree ...

      this.renderer.root.add(container)
      select.focus()

      this.keyHandler = (key) => {
        if (key.name === "escape") resolve({ action: "back" })
      }
      this.renderer.keyInput.on("keypress", this.keyHandler)
    })
  }

  cleanup(): void {
    if (this.keyHandler) {
      this.renderer.keyInput.off("keypress", this.keyHandler)
    }
    this.renderer.root.remove(CONTAINER_ID)
  }
}
```

### Application Lifecycle

```typescript
const renderer = await createCliRenderer({ exitOnCtrlC: true })

// Build UI...
renderer.root.add(container)

// When done:
renderer.destroy()   // ALWAYS call this
```

### Dynamic Content Updates

```typescript
// Update text content
text.content = "New content"          // Triggers re-render automatically

// Update select options
select.options = newOptions
select.setSelectedIndex(0)

// Update colours
text.fg = "#FF0000"
box.backgroundColor = "#333"
```

### Swapping Child Renderables

```typescript
// Remove old child by ID, add new one
if (oldChild) {
  parent.remove(oldChild.id)
}
const newChild = new TextRenderable(renderer, { content: "New" })
parent.add(newChild)
```

---

## 15. Testing with Mock Renderer

When unit testing screens/components that use OpenTUI, mock the renderer:

```typescript
import { vi } from "vitest"

function createMockRenderer() {
  const mockRoot = { add: vi.fn(), remove: vi.fn() }
  const mockKeyInput = {
    on: vi.fn(), off: vi.fn(), once: vi.fn(),
    emit: vi.fn(), removeAllListeners: vi.fn(),
  }
  const mockInternalKeyInput = {
    on: vi.fn(), off: vi.fn(), once: vi.fn(), emit: vi.fn(),
    onInternal: vi.fn(), offInternal: vi.fn(), removeAllListeners: vi.fn(),
  }

  return {
    root: mockRoot,
    keyInput: mockKeyInput,
    _internalKeyInput: mockInternalKeyInput,
    start: vi.fn(), stop: vi.fn(),
    requestRender: vi.fn(),
    width: 80, height: 24,
    addToHitGrid: vi.fn(),
    pushHitGridScissorRect: vi.fn(),
    popHitGridScissorRect: vi.fn(),
    clearHitGridScissorRects: vi.fn(),
    setCursorPosition: vi.fn(),
    setCursorStyle: vi.fn(),
    setCursorColor: vi.fn(),
    widthMethod: "wcwidth" as const,
    capabilities: null,
    requestLive: vi.fn(), dropLive: vi.fn(),
    hasSelection: false,
    getSelection: vi.fn().mockReturnValue(null),
    requestSelectionUpdate: vi.fn(),
    currentFocusedRenderable: null,
    focusRenderable: vi.fn(),
    registerLifecyclePass: vi.fn(),
    unregisterLifecyclePass: vi.fn(),
    getLifecyclePasses: vi.fn().mockReturnValue(new Set()),
    clearSelection: vi.fn(),
    startSelection: vi.fn(),
    updateSelection: vi.fn(),
    on: vi.fn(), off: vi.fn(), once: vi.fn(),
    emit: vi.fn(), removeAllListeners: vi.fn(),
  }
}
```

**Key testing patterns:**
- `SelectRenderable.focus()` requires `_internalKeyInput` with `onInternal`/`offInternal`
- Screen `render()` returns a Promise that waits for user input — don't `await` in tests
- `TextRenderable.content` returns `StyledText`, not string — access via `.content.chunks[0].text`
- Call `buildUI()` before testing event handlers that depend on the renderable tree

---

## 16. Gotchas & Pitfalls

1. **`remove()` takes a string ID, not a renderable instance** — `parent.remove(child.id)` not `parent.remove(child)`
2. **`renderer.destroy()` not `stop()`** — `destroy()` restores terminal state. `stop()` only stops the render loop.
3. **`exitOnCtrlC: true` is default** — no manual Ctrl+C handler needed
4. **Automatic rendering** — no `renderer.start()` call needed; re-renders on tree changes
5. **`SelectRenderable.focus()` is required** — keyboard input won't work without it
6. **`backgroundColor` defaults to transparent** — set explicitly on SelectRenderable or items appear black
7. **`TextRenderable.content` returns `StyledText`** — not a plain string. Read via `.chunks[0].text`
8. **`_internalKeyInput` needed for `focus()`** — mock renderers must include this with `onInternal`/`offInternal`
9. **OpenTUI does NOT auto-cleanup** — `process.exit` or unhandled errors won't restore terminal. Always call `destroy()`.
10. **Mouse events bubble** — stop with `event.stopPropagation()`
11. **`visible = false` removes from layout** — equivalent to CSS `display: none`, not `visibility: hidden`
