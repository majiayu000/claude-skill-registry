---
name: add-component
description: Create a reusable UI component with factory pattern, theme compatibility, and proper cleanup
aliases: [new-component, create-component]
---

# Add Component Skill

## Usage
```
/add-component <ComponentName>
```

## Step 1: Ask Questions

### 1. Check Existing Components First
```
Does an existing component cover ~80% of the need?
→ Check src/ui/components/ before creating new
```

Existing: `ArcadeButton`, `BasePetCard`, `GeminiIconButton`, `Modal`, `ProgressBar`, `SegmentedControl`, `SeeMore`, `SoundPicker`, `Tab`, `TeamListItem`

### 2. Component Purpose
```
Brief description (1 sentence):
```

### 3. Configuration Options
```
What options does it need?
- Required: ___________
- Optional with defaults: ___________
- Event handlers: ___________
```

### 4. Sprites
```
Does it display game sprites? → MGSprite.toCanvas()
```

### 5. Dynamic State
```
Does it need reactive updates?

A) Manual setters only (setLabel, setDisabled, setValue, etc.)
B) Reactive to Globals (subscribe to myInventory, currentTile, weather, etc.)
C) Both

If B/C: Component subscribes to Globals and auto-updates UI
→ Remember to unsubscribe in destroy()!
```

### 6. Child Components (IMPORTANT)
```
Does this component need sub-components?
→ REUSE existing components, never recreate!

Available:
- ArcadeButton, GeminiIconButton → Buttons
- Modal → Dialogs/popups
- ProgressBar → Progress indicators
- SegmentedControl → Tab-like selection
- Tab → Tabs
- SoundPicker → Audio selection
- BasePetCard, TeamListItem → List items
- SeeMore → Expandable content

Example: A "SettingsPanel" component might use:
- SegmentedControl for sections
- Toggle for on/off settings
- ArcadeButton for actions
```

---

## Step 2: Create Structure

```
src/ui/components/<ComponentName>/
├── <ComponentName>.ts      # Logic + factory function
├── <componentName>.css.ts  # Styles (CSS string)
└── index.ts                # Re-exports
```

**Read existing components for templates:** `src/ui/components/*/`

---

## Step 3: Required API

### Options Interface
```typescript
export interface <ComponentName>Options {
    // Required (no default)
    label: string;

    // Optional (have defaults)
    variant?: 'primary' | 'secondary';
    disabled?: boolean;

    // Event handlers
    onClick?: () => void;
}
```

### Handle Interface
```typescript
export interface <ComponentName>Handle {
    root: HTMLElement;           // REQUIRED
    set<Property>(value): void;  // Public setters (minimal)
    destroy(): void;             // REQUIRED - cleanup
}
```

### Factory Function
```typescript
export function create<ComponentName>(options: <ComponentName>Options): <ComponentName>Handle
```

---

## Step 4: Style Rules

### Theme Tokens (REQUIRED)
```css
/* NO hardcoded colors */
background: var(--color-bg);
color: var(--color-text);
border: 1px solid var(--color-border);
```

### Responsive (REQUIRED)
```css
min-height: 44px;        /* Touch-friendly */
width: 100%;             /* Flexible, not fixed */
max-width: 300px;        /* Constraint if needed */
```

### Scoped Styles
```css
/* Prefix all classes with component name */
.component-name { }
.component-name__label { }
.component-name--variant { }
```

---

## Step 5: Register

### Export → `src/ui/components/index.ts`
```typescript
export { create<ComponentName> } from './<ComponentName>/<ComponentName>';
export type { <ComponentName>Options, <ComponentName>Handle } from './<ComponentName>/<ComponentName>';
```

---

## Step 6: Validate

### Required
- [ ] `root: HTMLElement` in Handle
- [ ] `destroy()` removes ALL listeners/observers/intervals
- [ ] Factory function returns Handle

### Styling
- [ ] Uses CSS variables (no hardcoded colors)
- [ ] Touch-friendly (min 44px targets)
- [ ] Flexible widths (not fixed px)
- [ ] Focus states visible (`:focus-visible`)

### Composability
- [ ] Safe to nest inside other components
- [ ] No global CSS (scoped classes only)
- [ ] Styles injected into `root`, not `document.head`
- [ ] **Reuses existing components** (never recreate Button, Modal, ProgressBar, etc.)
- [ ] Child components' `destroy()` called in parent's `destroy()`

### If using Sprites
- [ ] Uses `MGSprite.toCanvas()` (never hardcoded paths)

### If using Globals (reactive)
- [ ] Subscribes in factory function
- [ ] **Unsubscribes in `destroy()`** (memory leak otherwise!)
- [ ] Updates UI elements on subscription callback

### If using Child Components
```typescript
import { createProgressBar, createArcadeButton } from '../index';

// In factory:
const progressBar = createProgressBar({ ... });
root.appendChild(progressBar.root);

// In destroy:
destroy() {
    progressBar.destroy();
    root.remove();
}
```

### If using Globals (reactive UI)
```typescript
import { getMyInventory } from '../../../globals/variables/myInventory';

// In factory:
const unsub = getMyInventory().subscribe((inventory) => {
    // Update UI when inventory changes
    updateItemCount(inventory.items.length);
});

// In destroy - CRITICAL!
destroy() {
    unsub();  // Unsubscribe from Global
    root.remove();
}
```

---

## References

- Rules: `.claude/rules/ui/components.md`
- Existing components: `src/ui/components/*/`
- Theme tokens: `src/ui/theme/`
- Reuse workflow: `.claude/workflows/ui/component/reuse-existing-component.md`
