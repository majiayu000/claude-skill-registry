---
name: ux-interaction-patterns
description: DAW-grade precision controls, Emacs-inspired keybindings, hover states, and micro-interactions for TMNL
triggers:
  - interaction
  - modifier keys
  - precision control
  - keybinding
  - hotkey
  - slider
  - hover
---

# UX Interaction Patterns

TMNL implements DAW-grade precision controls with Emacs-inspired keyboard ergonomics. This skill documents interaction patterns for precision inputs, keyboard navigation, and micro-interactions.

## Overview

TMNL's interaction model borrows from:
- **DAW tools** (Ableton, FL Studio) - Modifier keys for precision control
- **Emacs** - Chord sequences, prefix keys, which-key hints
- **Vim** - Modal editing, command palette (M-x)
- **Terminal UIs** - Keyboard-first navigation, focus management

All interactions prioritize keyboard-first workflows while maintaining pointer device support with precision modifiers.

## Canonical Sources

### Primary Files
- `/src/lib/slider/` - DAW-grade slider system with modifier keys
- `/src/lib/hotkeys/` - Emacs-inspired hotkey orchestration
- `/src/lib/minibuffer/` - M-x command execution system
- `/src/lib/overlays/visual/` - Overlay interaction patterns

### Key Type Definitions
- `/src/lib/slider/v1/types.ts` - `ModifierKeys`, `SliderState`, `SliderBehaviorShape`
- `/src/lib/hotkeys/types.ts` - `KeyChord`, `KeySequence`, `Binding`, `WhichKeyState`
- `/src/lib/minibuffer/v2/machine.ts` - Minibuffer state machine

## Patterns

### 1. Modifier Keys for Precision Control

**Pattern**: DAW-style modifier keys adjust sensitivity for fine-grained control.

**Canonical Implementation**: `/src/lib/slider/v1/types.ts`

```typescript
export interface ModifierKeys {
  readonly shift: boolean // Fine control (0.1x sensitivity)
  readonly ctrl: boolean  // Ultra-fine (0.01x sensitivity)
  readonly alt: boolean   // Snap to grid/steps
  readonly meta: boolean  // Reserved for future use
}

export const DEFAULT_MODIFIERS: ModifierKeys = {
  shift: false,
  ctrl: false,
  alt: false,
  meta: false,
}
```

**Sensitivity Multipliers**:
```typescript
export interface SliderConfig {
  readonly baseSensitivity: number      // 1.0x (normal dragging)
  readonly shiftSensitivity: number     // 0.1x (fine adjustment)
  readonly ctrlSensitivity: number      // 0.01x (ultra-fine, sub-dB precision)
  readonly altSnap: boolean             // Force snap to step grid
}
```

**Usage Example** (from slider behaviors):
```typescript
getSensitivity(modifiers: ModifierKeys, config: SliderConfig): number {
  if (modifiers.ctrl) return config.ctrlSensitivity  // 0.01x
  if (modifiers.shift) return config.shiftSensitivity // 0.1x
  return config.baseSensitivity // 1.0x
}
```

**When to Use**:
- Volume/gain controls (decibel precision with Ctrl)
- Frequency sliders (fine-tuning with Shift)
- Time-based parameters (millisecond precision)
- Any continuous value requiring both coarse and fine adjustment

**Modifier Key Table**:
| Modifier | Sensitivity | Use Case | Example |
|----------|------------|----------|---------|
| None | 1.0x | Normal dragging | Volume 0-100 |
| Shift | 0.1x | Fine adjustment | Gain -48.0 to -47.5 dB |
| Ctrl | 0.01x | Ultra-fine | Attack 499.5 to 500.0 ms |
| Alt | Snap mode | Quantize to steps | BPM 120 → 125 → 130 |

### 2. Emacs-Inspired Key Sequences

**Pattern**: Multi-chord sequences with prefix keys and which-key hints.

**Canonical Implementation**: `/src/lib/hotkeys/atoms/index.ts`

```typescript
// Chord sequence tracking
export const sequenceSourceAtom = Atom.make<KeyChord[]>([])

// Example chord sequence: "g g" (go to top)
const goToTopBinding: Binding = {
  id: "go-to-top",
  key: ["g", "g"], // Two separate chords
  commandId: "navigate.goToTop",
  scope: ScopeId.Global,
  source: "user",
  description: "Jump to top of page",
}
```

**Which-Key Hints** (shows available continuations):
```typescript
// After pressing "g", show available completions
const whichKeyEntries: WhichKeyEntry[] = [
  { key: "g", description: "Go to top" },
  { key: "G", description: "Go to bottom" },
  { key: "t", description: "Go to tab" },
]
```

**Timeout Behavior**:
```typescript
export const DEFAULT_CONFIG: HotkeyConfig = {
  sequenceTimeout: 1000, // Clear sequence after 1s of inactivity
  repeatDelay: 300,      // Key repeat throttle
  repeatRate: 50,        // Subsequent repeat rate
}
```

**Usage Example**:
```tsx
const { currentSequence, showWhichKey, whichKeyEntries } = useGlobalHotkeys()

// Display which-key popup when sequence is partial
{showWhichKey && whichKeyEntries.length > 0 && (
  <WhichKeyPopup entries={whichKeyEntries} prefix={currentSequence} />
)}
```

**Common Prefix Keys in TMNL**:
| Prefix | Domain | Example Chords |
|--------|--------|----------------|
| `g` | Navigation | `g g` (top), `g G` (bottom), `g t` (tab) |
| `SPC` | Leader key | `SPC f f` (find file), `SPC b b` (buffer) |
| `C-x` | Buffer/window | `C-x k` (kill buffer), `C-x 2` (split) |
| `C-c` | Mode-specific | `C-c C-c` (confirm), `C-c C-k` (cancel) |

### 3. M-x Command Palette

**Pattern**: Emacs-style M-x with fuzzy search and completion.

**Canonical Implementation**: `/src/lib/minibuffer/v2/`

```typescript
// Trigger via hotkey
const binding: Binding = {
  id: "execute-command",
  key: ["alt+x"], // M-x equivalent
  commandId: "minibuffer.execute",
  scope: ScopeId.Global,
}

// Minibuffer machine states
type MinibufferMode =
  | "idle"
  | "prompt"       // Asking for input
  | "completing"   // Showing completions
  | "executing"    // Running command
  | "finished"
```

**Completion Provider Interface**:
```typescript
export interface CompletionProvider {
  id: ProviderId
  priority: number
  match: (input: string) => Completion[]
  execute: (completion: Completion) => Promise<void>
}

// Command provider example
const COMMAND_PROVIDER_ID = "tmnl:commands" as ProviderId

// Register with fuzzy matching
providerRegistry.register({
  id: COMMAND_PROVIDER_ID,
  priority: 100,
  match: (input) => searchCommands(input), // Fuse.js fuzzy search
  execute: async (completion) => {
    const command = getCommand(completion.id)
    await command.execute()
  },
})
```

**Usage Pattern**:
```tsx
const { open, isActive, input, completions, selectedIndex } = useMinibuffer()

// Trigger M-x
const handleExecuteCommand = () => {
  open({
    mode: "completing",
    providerId: COMMAND_PROVIDER_ID,
    prompt: "M-x",
  })
}

// Keyboard navigation in completions
<MinibufferContent
  onKeyDown={(e) => {
    if (e.key === "ArrowDown") ops.selectNext()
    if (e.key === "ArrowUp") ops.selectPrevious()
    if (e.key === "Enter") ops.confirm()
    if (e.key === "Escape") ops.cancel()
  }}
/>
```

### 4. Hover State Micro-Interactions

**Pattern**: Progressive disclosure on hover with CSS transitions.

**Canonical Implementation**: `/src/components/static-ui/Modal/Modal.tsx`, buttons in header

```tsx
// Button hover states
const Button = ({ onClick, variant = "ghost" }: ButtonProps) => {
  const variantClasses = {
    ghost: "text-neutral-500 hover:text-white hover:bg-neutral-900",
    outline: "border border-neutral-700 text-neutral-400 hover:border-neutral-500 hover:text-white hover:bg-neutral-900",
    tmnl: "bg-neutral-800 text-white hover:bg-neutral-700",
  }

  return (
    <button
      className={`transition-colors ${variantClasses[variant]}`}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
```

**Icon Hover Pattern**:
```tsx
// Icon button with hover state change
<button className="p-1 hover:bg-neutral-900 transition-colors">
  <User className="text-neutral-600 hover:text-white" />
</button>
```

**Typography Hover** (navigation tabs):
```tsx
{navTabs.map((tab) => (
  <button
    className={`transition-colors ${
      activeTab === tab
        ? 'text-white'
        : 'text-neutral-600 hover:text-neutral-300'
    }`}
  >
    {tab}
  </button>
))}
```

**Timing Guidelines**:
- **Fast hover response**: 150ms (buttons, tabs)
- **Delayed tooltips**: 500ms (progressive disclosure)
- **Exit transitions**: 100ms (slightly faster than enter)

### 5. Double-Click Reset

**Pattern**: Double-click to reset slider to default value.

**Canonical Implementation**: `/src/lib/slider/v1/hooks/useSlider.ts`

```typescript
const handleDoubleClick = useCallback(() => {
  if (!config.doubleClickReset) return

  dispatch({
    type: 'RESET' // Resets to config.defaultValue
  })

  onChange(config.defaultValue)
}, [config, onChange])

// In JSX
<div
  ref={containerRef}
  onDoubleClick={handleDoubleClick}
  // ... other handlers
/>
```

**When to Use**:
- All sliders/faders with default values
- Numeric inputs with reset behavior
- Color pickers (reset to theme default)

### 6. Pointer Events Passthrough

**Pattern**: Container blocks events but children capture them.

**Canonical Implementation**: `/src/App.tsx`, overlay containers

```tsx
// Container is non-interactive
<div style={{ pointerEvents: 'none' }}>
  {/* Children opt-in to interactions */}
  <div style={{ pointerEvents: 'auto' }}>
    <MyInteractiveContent />
  </div>
</div>
```

**Three-Tier Model**:
```typescript
type PointerEventsBehavior = 'auto' | 'none' | 'pass-through'

// auto: Layer captures all clicks
<div style={{ pointerEvents: 'auto' }} />

// none: Layer ignores all clicks (transparent overlay)
<div style={{ pointerEvents: 'none' }} />

// pass-through: Container is 'none', children are 'auto'
<div className="pointer-events-none">
  <button className="pointer-events-auto">Click me</button>
</div>
```

**Usage**: See `/src/lib/overlays/schemas/visual.ts` for drawer/modal backdrop patterns.

## Examples

### Example 1: DAW-Grade Volume Fader

```tsx
import { Slider, DecibelBehavior } from '@/lib/slider'

function VolumeFader() {
  const [gain, setGain] = useState(0) // 0 dB reference

  return (
    <Slider
      value={gain}
      onChange={setGain}
      behavior={DecibelBehavior.shape}
      config={{
        min: -48,
        max: 12,
        defaultValue: 0,
        step: 0.5,
        unit: 'dB',
        baseSensitivity: 1,
        shiftSensitivity: 0.1,  // Fine: -12.0 → -11.5 dB
        ctrlSensitivity: 0.01,   // Ultra: -12.00 → -11.95 dB
        altSnap: true,           // Alt: snap to 0.5 dB steps
        doubleClickReset: true,  // Dbl-click → 0 dB
      }}
    />
  )
}
```

### Example 2: Custom Hotkey with Which-Key

```tsx
import { useGlobalHotkeys } from '@/lib/hotkeys'

function MyComponent() {
  const { showWhichKey, whichKeyEntries, currentSequence } = useGlobalHotkeys({
    debug: false,
    onSettings: () => console.log('Open settings'),
  })

  // After user presses "g", show available completions
  return (
    <>
      {showWhichKey && whichKeyEntries.length > 0 && (
        <WhichKeyPopup
          entries={whichKeyEntries}
          prefix={currentSequence}
        />
      )}
    </>
  )
}
```

### Example 3: M-x Command Registration

```tsx
import { providerRegistry, COMMAND_PROVIDER_ID } from '@/lib/minibuffer'
import { hotkeyActions } from '@/lib/hotkeys'

// Register command
hotkeyActions.registerCommand(registry, {
  id: 'navigate.goToTop',
  name: 'Go to Top',
  category: 'navigation',
  execute: () => Effect.sync(() => window.scrollTo(0, 0)),
})

// Bind to hotkey
hotkeyActions.addBinding(registry, {
  id: 'go-to-top',
  key: ['g', 'g'],
  commandId: 'navigate.goToTop',
  scope: ScopeId.Global,
  source: 'user',
})

// Now "g g" or "M-x go to top" both work
```

## Anti-Patterns

### DON'T: Hardcode Sensitivity Values

```tsx
// WRONG - Hardcoded sensitivity, no modifier support
const handleDrag = (deltaY: number) => {
  const newValue = value + deltaY * 0.5 // What if user wants precision?
  setValue(newValue)
}

// CORRECT - Use slider system with modifier keys
<Slider
  value={value}
  onChange={setValue}
  config={{ shiftSensitivity: 0.1, ctrlSensitivity: 0.01 }}
/>
```

### DON'T: Ignore Keyboard Users

```tsx
// WRONG - Pointer-only interaction
<div onClick={handleClick}>
  Click me
</div>

// CORRECT - Keyboard accessible
<button
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') handleClick()
  }}
  tabIndex={0}
>
  Click me
</button>
```

### DON'T: Single-Key Bindings in Global Scope

```tsx
// WRONG - Captures "s" key globally, breaks typing in inputs
hotkeyActions.addBinding(registry, {
  key: ['s'],
  commandId: 'save',
  scope: ScopeId.Global, // BAD!
})

// CORRECT - Use chord or scoped binding
hotkeyActions.addBinding(registry, {
  key: ['ctrl+s'], // Modifier required
  commandId: 'save',
  scope: ScopeId.Global,
})

// OR scope to non-input contexts
hotkeyActions.addBinding(registry, {
  key: ['s'],
  commandId: 'save',
  scope: ScopeId.Canvas, // Only active when canvas focused
})
```

### DON'T: Suppress Native Browser Shortcuts

```tsx
// WRONG - Breaks user expectations
e.preventDefault() // on Ctrl+T (new tab), Ctrl+W (close tab)

// CORRECT - Let native shortcuts through
const NATIVE_SHORTCUTS = [
  'ctrl+t', 'ctrl+n', 'ctrl+w', 'ctrl+shift+t',
  'ctrl+tab', 'ctrl+shift+tab',
  'F5', 'ctrl+r', 'ctrl+shift+r',
]

// Only preventDefault if NOT a native shortcut
if (!NATIVE_SHORTCUTS.includes(keyString)) {
  e.preventDefault()
}
```

See `/src/lib/hotkeys/types.ts` for `getNativeSuppression()` helper.

### DON'T: Use `pointer-events: none` on Interactive Elements

```tsx
// WRONG - Buttons won't receive clicks
<div className="pointer-events-none">
  <button>Click me</button> {/* Doesn't work! */}
</div>

// CORRECT - Pass-through pattern
<div className="pointer-events-none">
  <button className="pointer-events-auto">Click me</button>
</div>
```

## Testing Interaction Patterns

### Manual Testing Checklist

When implementing interactive components:

1. **Modifier Keys**:
   - [ ] Normal drag/click works
   - [ ] Shift reduces sensitivity to ~0.1x
   - [ ] Ctrl reduces sensitivity to ~0.01x
   - [ ] Alt snaps to grid/steps
   - [ ] Modifiers combine correctly (Ctrl+Shift = 0.001x)

2. **Keyboard Navigation**:
   - [ ] Tab moves focus correctly
   - [ ] Enter/Space activates buttons
   - [ ] Escape cancels/closes overlays
   - [ ] Arrow keys navigate lists/menus
   - [ ] Home/End jump to boundaries

3. **Hover States**:
   - [ ] Hover transitions are smooth (150ms)
   - [ ] Hover persists during rapid mouse movement
   - [ ] No hover flicker on touch devices

4. **Double-Click Reset**:
   - [ ] Double-click resets to default value
   - [ ] Single clicks don't trigger reset
   - [ ] Works on both desktop and trackpad

### Debug Mode

Enable debug overlays to inspect interaction state:

```tsx
import { Slider, withSliderDebug } from '@/lib/slider'

const DebugSlider = withSliderDebug(Slider, { defaultExpanded: true })

<DebugSlider
  value={value}
  onChange={setValue}
  config={{ debugMode: true }}
/>
```

This shows:
- Active modifiers (Shift/Ctrl/Alt)
- Current sensitivity multiplier
- Raw vs normalized values
- Drag state tracking

## Related Skills

- `ux-feedback-patterns` - Loading states, progress indicators, toasts
- `ux-accessibility-patterns` - ARIA, focus management, screen readers
- `ux-overlay-patterns` - Modal/drawer stacking, z-index management

## References

- DAW UI Research: [Ableton Push](https://www.ableton.com/en/push/), [FL Studio](https://www.image-line.com/)
- Emacs Keybindings: [GNU Emacs Manual](https://www.gnu.org/software/emacs/manual/html_node/emacs/Key-Bindings.html)
- Which-Key: [which-key.el](https://github.com/justbur/emacs-which-key)
- Slider Implementation: `/src/lib/slider/v1/` (canonical)
- Hotkey System: `/src/lib/hotkeys/` (canonical)
