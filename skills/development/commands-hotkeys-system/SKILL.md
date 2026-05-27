---
name: commands-hotkeys-system
description: Emacs-inspired command and hotkey infrastructure for TMNL. Invoke when implementing keybindings, M-x command palette, which-key popups, scope-aware bindings, or Effect-native command orchestration. Provides decorator DSL, Effect.Service patterns, and atom-based reactivity.
model_invoked: true
triggers:
  - "command system"
  - "hotkey"
  - "keybinding"
  - "M-x"
  - "command palette"
  - "which-key"
  - "keyboard shortcut"
  - "defineCommand"
  - "CommandService"
  - "wire commands"
  - "effectiveBindingsAtom"
  - "scope-aware binding"
  - "vim-style sequence"
  - "g i"
  - "multi-chord"
---

# Commands & Hotkeys System for TMNL

## Overview

An Emacs-inspired command infrastructure with:
- **Effect-native commands** via decorator DSL or functional API
- **Scope-aware keybindings** (global, editor, grid, tldraw, modal)
- **Multi-chord sequences** (vim-style `g i`, `g g`)
- **which-key popups** for prefix hints
- **M-x command palette** with FlexSearch fuzzy matching
- **Persistent overrides** via localStorage
- **Wire system** bridging commands to hotkey handlers

## Canonical Sources

### TMNL Implementations

| File | Purpose | Pattern |
|------|---------|---------|
| `src/lib/commands/index.ts` | Barrel export | Public API surface |
| `src/lib/commands/types.ts` | Core types | CommandScope, KeyBinding |
| `src/lib/commands/decorators.ts` | Decorator DSL | @command, defineCommand |
| `src/lib/commands/service.ts` | CommandService | Effect.Service + atoms |
| `src/lib/commands/defaults.ts` | Built-in commands | Default bindings |
| `src/lib/commands/wire.ts` | Command→hotkey bridge | Effect-based wiring |
| `src/lib/commands/persistence.ts` | localStorage sync | useKeybindingPersistence |
| `src/lib/commands/CommandProvider.ts` | M-x completions | FlexSearch integration |
| `src/lib/hotkeys/index.ts` | Hotkey system | Public API |
| `src/lib/hotkeys/types.ts` | KeyChord, KeySequence | Primitives |
| `src/lib/hotkeys/atoms/index.ts` | Reactive state | Source + derived atoms |
| `src/lib/hotkeys/components/WhichKeyPopup.tsx` | Prefix hints | which-key UI |

### Testbeds

- **KeybindingTestbed**: `/testbed/keybinding` — Command execution demo
- **HotkeyTestbed**: `/testbed/hotkey` — Multi-chord sequences

---

## Pattern 1: Command Definition — DECORATOR DSL

**When:** Defining commands with default keybindings.

Commands use **decorator DSL** (class-based) OR **functional API** (preferred).

### Functional API (Preferred)

```typescript
import { defineCommand } from '@/lib/commands'
import { Effect } from 'effect'

export const saveCommand = defineCommand(
  {
    id: 'file.save',
    name: 'Save',
    description: 'Save current file',
    category: 'file',
    scope: 'global',
    keys: 'ctrl+s',  // Default binding
  },
  Effect.gen(function* () {
    yield* Effect.log('Saving...')
    // Your save logic
  })
)
```

### Decorator API (Alternative)

```typescript
import { command } from '@/lib/commands'
import { Effect } from 'effect'

@command({
  id: 'file.save',
  name: 'Save',
  category: 'file',
  scope: 'global',
  keys: 'ctrl+s',
})
class SaveCommand {
  execute = Effect.gen(function* () {
    yield* Effect.log('Saving...')
  })
}
```

### Entity Commands (Require Context)

For commands that need a target entity (delete row, format selection):

```typescript
import { defineEntityCommand } from '@/lib/commands'

export const gridDeleteRowCommand = defineEntityCommand<GridRow>(
  {
    id: 'grid.deleteRow',
    name: 'Delete Row',
    category: 'grid',
    scope: 'grid',
    entityType: 'grid.row',
    keys: 'ctrl+backspace',
  },
  (row, ctx) =>
    Effect.gen(function* () {
      yield* Effect.log(`Deleting row ${row.id}`)
      // Delete logic with entity context
    })
)
```

**TMNL Location**: `src/lib/commands/decorators.ts:162`

---

## Pattern 2: CommandService — EFFECT.SERVICE WITH ATOMS

**When:** Executing commands, managing bindings, or implementing M-x.

CommandService is an `Effect.Service` (Context.Tag) with **atom-backed state**.

```typescript
import { CommandService } from '@/lib/commands'
import { Effect } from 'effect'

// Execute a global command
const executeProgram = Effect.gen(function* () {
  const service = yield* CommandService
  yield* service.execute('file.save')
})

// Execute an entity command
const deleteRowProgram = Effect.gen(function* () {
  const service = yield* CommandService
  yield* service.executeEntity('grid.deleteRow', selectedRow, {
    scope: 'grid',
  })
})

// Run with default layer
Effect.runPromise(
  executeProgram.pipe(Effect.provide(CommandService.Default))
)
```

### M-x Command Palette (executeInteractive)

```typescript
import { CommandService } from '@/lib/commands'

// Open command palette (minibuffer-based)
const openPaletteProgram = Effect.gen(function* () {
  const service = yield* CommandService
  yield* service.executeInteractive({
    animate: 'slide',  // Optional animation
  })
})
```

**Key Methods:**

| Method | Signature | Purpose |
|--------|-----------|---------|
| `execute` | `(id: string) => Effect<void, CommandError>` | Execute global command |
| `executeEntity` | `<T>(id, entity, ctx?) => Effect<void>` | Execute entity command |
| `executeInteractive` | `(options?) => Effect<void>` | M-x palette |
| `get` | `(id) => Effect<Option<Command>>` | Retrieve command |
| `list` | `() => Effect<Command[]>` | All commands |
| `overrideBinding` | `(registry, id, keys, scope?)` | Override keybinding |
| `resetBinding` | `(registry, id)` | Reset to default |

**TMNL Location**: `src/lib/commands/service.ts:136`

---

## Pattern 3: effectiveBindingsAtom — DERIVED BINDINGS

**When:** Computing final keybindings with user overrides applied.

The `effectiveBindingsAtom` is a **derived atom** that merges defaults + overrides.

```typescript
import { effectiveBindingsAtom, bindingOverridesAtom } from '@/lib/commands'
import { Atom } from '@effect-atom/atom'

// Derived atom (computed)
export const effectiveBindingsAtom = Atom.make((get) => {
  const overrides = get(bindingOverridesAtom)
  const defaults = getDefaultBindings()

  // Build override lookup
  const overrideMap = new Map<string, KeyBindingOverride>()
  for (const override of overrides) {
    overrideMap.set(override.commandId, override)
  }

  // Apply overrides to defaults
  const effective: KeyBinding[] = []
  for (const binding of defaults) {
    const override = overrideMap.get(binding.commandId)
    if (override) {
      // null keys means unbind
      if (override.keys !== null) {
        effective.push({
          ...binding,
          keys: override.keys,
          scope: override.scope ?? binding.scope,
        })
      }
    } else {
      effective.push(binding)
    }
  }

  return effective
})
```

**Usage in React:**

```typescript
import { useAtomValue } from '@effect-atom/atom-react'
import { effectiveBindingsAtom } from '@/lib/commands'

function KeybindingSettings() {
  const bindings = useAtomValue(effectiveBindingsAtom)

  return (
    <table>
      {bindings.map(b => (
        <tr key={b.commandId}>
          <td>{b.keys}</td>
          <td>{b.commandId}</td>
        </tr>
      ))}
    </table>
  )
}
```

**TMNL Location**: `src/lib/commands/service.ts:35`

---

## Pattern 4: Keybinding Override Persistence — LOCALSTORAGE SYNC

**When:** Persisting user-customized keybindings across sessions.

The `useKeybindingPersistence` hook syncs `bindingOverridesAtom` with localStorage.

```typescript
import { useKeybindingPersistence } from '@/lib/commands'

function App() {
  const { isLoaded, loadedCount } = useKeybindingPersistence({
    debug: true,  // Log load/save operations
  })

  if (!isLoaded) return <Loading />

  return <YourApp />
}
```

### Manual Operations

```typescript
import { loadOverrides, saveOverrides, clearPersistedOverrides } from '@/lib/commands'

// Load from localStorage
const overrides = loadOverrides()

// Save to localStorage
saveOverrides([
  { commandId: 'file.save', keys: 'ctrl+alt+s', scope: 'global' },
])

// Clear all
clearPersistedOverrides()
```

**Storage Format:**

```json
{
  "version": 1,
  "overrides": [
    {
      "commandId": "file.save",
      "keys": "ctrl+alt+s",
      "scope": "global"
    }
  ]
}
```

**TMNL Location**: `src/lib/commands/persistence.ts:115`

---

## Pattern 5: Wire System — COMMAND→HOTKEY BRIDGE

**When:** Registering commands with the hotkey system at app initialization.

The **wire system** bridges commands to hotkeys using Effect for error accumulation.

```typescript
import { wireCommandsEffect } from '@/lib/commands'
import { RegistryContext } from '@effect-atom/atom-react'
import { useContext, useEffect } from 'react'

function App() {
  const registry = useContext(RegistryContext)

  useEffect(() => {
    Effect.runPromise(
      wireCommandsEffect(registry).pipe(
        Effect.tap((result) =>
          Effect.log(
            `Wired ${result.commandsRegistered} commands, ${result.bindingsRegistered} bindings`
          )
        ),
        Effect.catchAll((error) =>
          Effect.log(`Wire failed: ${JSON.stringify(error)}`)
        )
      )
    )
  }, [registry])

  return <YourApp />
}
```

### Wire Result

```typescript
interface WireResult {
  readonly commandsRegistered: number
  readonly bindingsRegistered: number
  readonly errors: readonly (CommandRegistrationError | BindingRegistrationError)[]
}
```

**Error Handling:**

Wiring uses **non-fail-fast** error accumulation. Partial wiring succeeds even if some commands/bindings fail.

```typescript
// Errors are accumulated, not thrown
const result = yield* wireCommandsEffect(registry)

if (result.errors.length > 0) {
  // Some commands failed to register
  console.warn('Wire completed with errors:', result.errors)
}
```

**TMNL Location**: `src/lib/commands/wire.ts:224`

---

## Pattern 6: which-key Integration — PREFIX HINTS

**When:** Showing available key continuations after a multi-chord prefix.

The **which-key popup** appears after timeout when a partial sequence is entered.

### Hotkey Atoms

```typescript
import {
  sequenceSourceAtom,
  whichKeyEntriesAtom,
  hotkeyActions,
} from '@/lib/hotkeys'
import { useAtomValue, useRegistry } from '@effect-atom/atom-react'

function HotkeyListener() {
  const registry = useRegistry()
  const currentSequence = useAtomValue(sequenceSourceAtom)
  const whichKeyEntries = useAtomValue(whichKeyEntriesAtom)

  const handleKeyDown = (e: KeyboardEvent) => {
    // Parse chord from event
    const chord: KeyChord = {
      ctrl: e.ctrlKey,
      alt: e.altKey,
      shift: e.shiftKey,
      meta: e.metaKey,
      key: e.key,
    }

    // Append to sequence
    hotkeyActions.appendToSequence(registry, chord)

    // After timeout, show which-key if partial matches exist
    setTimeout(() => {
      const entries = registry.get(whichKeyEntriesAtom)
      if (entries.length > 0) {
        setShowWhichKey(true)
      }
    }, 500)
  }

  return (
    <>
      <YourApp onKeyDown={handleKeyDown} />
      {showWhichKey && (
        <WhichKeyPopup
          entries={whichKeyEntries}
          prefix={currentSequence}
        />
      )}
    </>
  )
}
```

### WhichKeyPopup Component

```typescript
import { WhichKeyPopup } from '@/lib/hotkeys'

<WhichKeyPopup
  entries={[
    { key: 'i', label: 'Go to Inbox', isPrefix: false },
    { key: 's', label: 'Go to Starred', isPrefix: false },
  ]}
  prefix={[{ ctrl: false, alt: false, shift: false, meta: false, key: 'g' }]}
/>
```

**Display Format:**

```
┌─────────────────────────────┐
│ which-key   [g]             │
│ i    Go to Inbox            │
│ s    Go to Starred          │
│ g    Go to Top              │
└─────────────────────────────┘
```

**TMNL Location**: `src/lib/hotkeys/components/WhichKeyPopup.tsx`

---

## Pattern 7: Multi-Chord Sequences — VIM-STYLE BINDINGS

**When:** Implementing vim/Emacs-style multi-key sequences (`g i`, `g g`, `ctrl+k ctrl+s`).

### Sequence Definition

```typescript
import { defineCommand, defineBinding } from '@/lib/commands'

// Two-chord sequence (g i)
export const goToInboxCommand = defineCommand(
  {
    id: 'nav.goToInbox',
    name: 'Go to Inbox',
    category: 'navigation',
    scope: 'global',
    keys: 'g i',  // ← Space-separated chords
  },
  Effect.log('Navigating to inbox...')
)

// Alternative: Add binding separately
defineBinding('g s', 'nav.goToStarred', 'global')
```

### Sequence Processing

The `processKeyboardEvent` pure function handles sequence matching:

```typescript
import { processKeyboardEvent } from '@/lib/hotkeys'

const { result, newSequence } = processKeyboardEvent(
  chord,           // Current key press
  currentSequence, // Accumulated sequence
  scopedBindings,  // Filtered to active scope
  commands         // Command registry
)

switch (result.type) {
  case 'exact':
    // Full match - execute command
    executeCommand(result.binding.commandId)
    break

  case 'partial':
    // Prefix match - show which-key
    showWhichKey(result.entries)
    break

  case 'none':
    // No match - reset sequence
    resetSequence()
    break
}
```

**TMNL Location**: `src/lib/hotkeys/atoms/index.ts:373`

---

## Pattern 8: Scope-Aware Bindings — CONTEXT SWITCHING

**When:** Commands should only be active in specific contexts (editor, grid, modal).

### Scope Hierarchy

```typescript
export const ScopeId = Schema.Literal(
  'global',      // Always active
  'editor',      // Text editor context
  'grid',        // AG-Grid context
  'tldraw',      // Canvas context
  'modal',       // Modal overlay
  'palette',     // Command palette
  'minibuffer'   // Minibuffer prompt
)
```

### Scope Inheritance

```typescript
const DEFAULT_CONFIG: HotkeyConfig = {
  scopeInheritance: {
    editor: 'global',    // editor inherits global
    grid: 'global',      // grid inherits global
    tldraw: 'global',
    modal: 'global',
    palette: 'modal',    // palette inherits modal
    minibuffer: 'global',
  },
}
```

### Scoped Command Example

```typescript
// Only active in grid scope
export const gridDeleteRowCommand = defineEntityCommand<GridRow>(
  {
    id: 'grid.deleteRow',
    name: 'Delete Row',
    scope: 'grid',  // ← Scope restriction
    keys: 'ctrl+backspace',
  },
  (row) => Effect.log(`Deleting row ${row.id}`)
)

// Active globally
export const commandPaletteCommand = defineCommand(
  {
    id: 'system.commandPalette',
    name: 'Command Palette',
    scope: 'global',  // ← Available everywhere
    keys: 'ctrl+shift+p',
  },
  Effect.log('Opening palette...')
)
```

### Scope Management

```typescript
import { hotkeyActions } from '@/lib/hotkeys'

// Set active scope
hotkeyActions.setScope(registry, 'grid')

// Push scope (stack-based)
hotkeyActions.pushScope(registry, 'modal')

// Pop scope
hotkeyActions.popScope(registry)

// Current scope chain (derived atom)
const scopeChain = useAtomValue(scopeChainAtom)
// ['grid', 'global'] - grid scope inherits global
```

**TMNL Location**: `src/lib/hotkeys/types.ts:126`, `src/lib/hotkeys/atoms/index.ts:62`

---

## Pattern 9: CommandProvider — M-X FUZZY SEARCH

**When:** Implementing M-x style command completion with FlexSearch.

CommandProvider bridges commands to the minibuffer system with fuzzy search.

```typescript
import { CommandProvider, registerCommandProvider } from '@/lib/commands'

// Register once at app init
registerCommandProvider()

// Provider automatically handles:
// - Fuzzy search via FlexSearch
// - QueryDSL (regex, dorking operators)
// - Command execution via CommandService
```

### Search Features

| Query | Result |
|-------|--------|
| `save` | Fuzzy match "Save", "Save As", etc. |
| `scope:grid` | Filter to grid-scoped commands |
| `/delete.*row/` | Regex match |
| `scope:grid category:edit` | Combined filters |

### Provider Interface

```typescript
export const CommandProvider: CompletionProvider<string> = {
  id: COMMAND_PROVIDER_ID,
  label: "Commands",
  icon: Terminal,
  placeholder: "M-x ",

  complete: (query: string) => Effect<Completion[]>,
  onSelect: (item: Completion) => Effect<void>,
  transformInput: (input: string) => string,
}
```

**TMNL Location**: `src/lib/commands/CommandProvider.ts:114`

---

## Decision Tree: Command vs Hotkey

```
Need to define an action?
│
├─ Should it appear in M-x palette?
│  YES → Define as Command (commands/)
│     └─ Use defineCommand() or @command
│
└─ Is it only triggered by keybinding?
   NO → Define as Command anyway (discoverability)
   YES → Use hotkey system directly (hotkeys/)
       └─ hotkeyActions.addBinding()
```

---

## Anti-Patterns

### Don't: Register commands without wiring

```typescript
// BANNED - commands exist but aren't executable
defineCommand({ id: 'my.command', ... }, handler)

// App renders - commands not wired to hotkeys
// Pressing keybinding does nothing!

// CORRECT - wire at app init
useEffect(() => {
  Effect.runPromise(wireCommandsEffect(registry))
}, [])
```

### Don't: Override bindings directly in defaults

```typescript
// BANNED - modifies shared defaults
const defaults = getDefaultBindings()
defaults.push({ keys: 'ctrl+s', commandId: 'my.save' })

// CORRECT - use bindingOverridesAtom
registry.set(bindingOverridesAtom, [
  { commandId: 'file.save', keys: 'ctrl+alt+s' }
])
```

### Don't: Execute commands without Effect runtime

```typescript
// BANNED - CommandService.execute returns Effect
const service = CommandService.of(...)
service.execute('file.save')  // Does nothing!

// CORRECT - run the Effect
Effect.runPromise(
  service.execute('file.save')
    .pipe(Effect.provide(CommandService.Default))
)
```

### Don't: Use raw KeyboardEvent for sequences

```typescript
// BANNED - loses sequence context
document.addEventListener('keydown', (e) => {
  if (e.key === 'g') {
    // How do you detect 'g i' sequence?
  }
})

// CORRECT - use hotkeyActions + processKeyboardEvent
hotkeyActions.appendToSequence(registry, chord)
const { result } = processKeyboardEvent(...)
```

---

## Integration Points

**Depends on:**
- `effect-patterns` — Effect.Service, Context.Tag
- `effect-atom-integration` — Atom.make, derived atoms
- `effect-schema-mastery` — Schema.Literal for ScopeId

**Used by:**
- `tmnl-testbed-patterns` — Keybinding testbeds
- `ux-interaction-patterns` — Keyboard navigation
- Minibuffer system — M-x command palette

**Bridges:**
- Commands (high-level intent) → Hotkeys (low-level key handling)

---

## Quick Reference

| Task | Pattern | File |
|------|---------|------|
| Define global command | `defineCommand()` | commands/decorators.ts:162 |
| Define entity command | `defineEntityCommand()` | commands/decorators.ts:216 |
| Execute command | `CommandService.execute()` | commands/service.ts:149 |
| Open M-x palette | `CommandService.executeInteractive()` | commands/service.ts:193 |
| Get effective bindings | `useAtomValue(effectiveBindingsAtom)` | commands/service.ts:35 |
| Override keybinding | `CommandService.overrideBinding()` | commands/service.ts:211 |
| Wire commands to hotkeys | `wireCommandsEffect(registry)` | commands/wire.ts:224 |
| Persist overrides | `useKeybindingPersistence()` | commands/persistence.ts:115 |
| Multi-chord sequence | `keys: 'g i'` | commands/defaults.ts:211 |
| Show which-key popup | `<WhichKeyPopup />` | hotkeys/components/WhichKeyPopup.tsx |
| Process keyboard event | `processKeyboardEvent()` | hotkeys/atoms/index.ts:373 |
| Set active scope | `hotkeyActions.setScope()` | hotkeys/atoms/index.ts:327 |
