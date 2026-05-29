---
name: add-section
description: Create a new HUD section (tab) with lifecycle, persistent state, and registry registration
aliases: [new-section, create-section]
---

# Add Section Skill

## Usage
```
/add-section <SectionName>
```

---

## Step 1: Ask Questions

### 1. Section Purpose
```
Brief description (1 sentence):
What does this section display/manage?
```

### 2. Persistent State
```
What state needs to persist across sessions?
(Must be JSON-serializable: strings, numbers, booleans, arrays, plain objects)

Examples:
- Selected tab/filter
- Sort order
- Collapsed/expanded states
- User preferences
```

### 3. Game Data
```
Does this section need game data?

A) Static data → MGData (plants, items, pets, etc.)
B) Real-time state → Globals (myInventory, myGarden, etc.)
C) Both
D) None
```

### 4. Sprites
```
Does it display game sprites? → MGSprite.toCanvas()
```

### 5. Child Components
```
Does it need existing UI components?
→ REUSE from src/ui/components/

[ ] ArcadeButton, GeminiIconButton → Buttons
[ ] Modal → Dialogs
[ ] ProgressBar → Progress
[ ] SegmentedControl → Tab-like selection
[ ] Tab → Tabs
[ ] SoundPicker → Audio
[ ] Other: ___
```

### 6. Complexity
```
A) Simple - Single file section
B) Complex - Split into parts/ folder
```

### 7. Tab Info
```
- Label (displayed in tab bar): ___________
- Icon (emoji): ___________
```

---

## Step 2: Create Structure

### Simple Section
```
src/ui/sections/<SectionName>/
├── index.ts          # Public exports
├── section.ts        # build() / destroy() lifecycle
├── state.ts          # Persistent state (createSectionStore)
└── styles.css.ts     # Scoped CSS (optional)
```

### Complex Section (with parts)
```
src/ui/sections/<SectionName>/
├── index.ts
├── section.ts        # Assembles parts
├── state.ts
├── styles.css.ts
└── parts/
    ├── header.ts     # Search, filters
    ├── content.ts    # Main content
    └── footer.ts     # Actions
```

**Read existing sections for templates:** `src/ui/sections/*/`

---

## Step 3: File Responsibilities

| File | Purpose |
|------|---------|
| `index.ts` | Export `<Name>Section` and types only |
| `section.ts` | `build(container)`, `destroy()`, `cleanups[]` |
| `state.ts` | `createSectionStore()` with stable ID `tab-<name>` |
| `styles.css.ts` | CSS string with scoped classes |
| `parts/*.ts` | Sub-components with own `destroy()` |

### Key Patterns

#### state.ts
```typescript
import { createSectionStore } from '../core/state';

export interface <Name>State {
    // JSON-serializable only!
    selectedTab: string;
    sortOrder: 'asc' | 'desc';
}

const DEFAULT_STATE: <Name>State = {
    selectedTab: 'all',
    sortOrder: 'asc',
};

// ID must be stable forever (storage key)
export const state = createSectionStore<<Name>State>('tab-<name>', {
    version: 1,  // Increment when state shape changes
    defaults: DEFAULT_STATE,
});
```

#### section.ts
```typescript
export interface SectionDefinition {
    build(container: HTMLElement): void;
    destroy(): void;
}

let root: HTMLElement | null = null;
const cleanups: (() => void)[] = [];

function build(container: HTMLElement): void {
    if (root) return;  // Prevent double-build

    root = document.createElement('div');
    root.className = '<name>-section';

    // Inject styles
    const style = document.createElement('style');
    style.textContent = <name>Css;
    root.appendChild(style);

    // Subscribe to state
    const unsub = state.subscribe((s) => { /* update UI */ });
    cleanups.push(unsub);

    // Add child components (reuse existing!)
    // const button = createArcadeButton({ ... });
    // cleanups.push(() => button.destroy());

    container.appendChild(root);
}

function destroy(): void {
    cleanups.forEach(fn => fn());
    cleanups.length = 0;
    root?.remove();
    root = null;
}

export const <Name>Section: SectionDefinition = { build, destroy };
```

---

## Step 4: Register

### Registry → `src/ui/sections/registry.ts`
```typescript
import { <Name>Section } from './<SectionName>';

export const sectionRegistry: Record<string, SectionConfig> = {
    // ... existing
    'tab-<name>': {
        id: 'tab-<name>',
        label: '<Label>',
        icon: '<emoji>',
        section: <Name>Section,
    },
};
```

---

## Step 5: Validate

### Structure
- [ ] `index.ts` exports `<Name>Section` only
- [ ] `section.ts` has `build()` and `destroy()`
- [ ] `state.ts` uses `createSectionStore()` with stable ID

### State
- [ ] All fields JSON-serializable (no functions, DOM, classes)
- [ ] Section ID is `tab-<name>` format (stable forever)
- [ ] `version` incremented when state shape changes
- [ ] Default state is complete (no undefined)

### Lifecycle
- [ ] `build()` guards against double-build (`if (root) return`)
- [ ] `destroy()` cleans up ALL resources
- [ ] Subscriptions unsubscribed in `destroy()`
- [ ] Child components' `destroy()` called

### Styling
- [ ] Uses CSS variables (no hardcoded colors)
- [ ] Classes scoped (`.section-name__element`)
- [ ] Styles injected into `root`, not `document.head`

### Game Data (if applicable)
- [ ] Static data → `MGData.get()`
- [ ] Real-time → Globals with `.subscribe()` + cleanup
- [ ] Sprites → `MGSprite.toCanvas()`

### Components (if applicable)
- [ ] Reuses existing components from `src/ui/components/`
- [ ] Child components tracked in `cleanups[]`

### Registration
- [ ] Added to `src/ui/sections/registry.ts`
- [ ] ID matches state ID (`tab-<name>`)

---

## Existing Sections

For reference/templates:
- `Settings` - User preferences
- `AutoFavoriteSettings` - Feature config
- `JournalChecker` - Journal progress
- `Pets` - Pet management
- `Trackers` - Stats tracking
- `Alerts` - Notifications config
- `Dev` - Developer tools
- `Test` - Testing section

---

## References

- Rules: `.claude/rules/ui/sections.md`
- Existing sections: `src/ui/sections/*/`
- Core state: `src/ui/sections/core/state.ts`
- UI Components: `src/ui/components/`
- Split workflow: `.claude/workflows/ui/section/split-section-into-parts.md`
