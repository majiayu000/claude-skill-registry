---
name: add-inject
description: Create a game UI injection that modifies existing game elements with proper cleanup
aliases: [new-inject, create-inject, add-qol]
---

# Add Inject Skill

## Usage
```
/add-inject <featureName>
```

**Note:** This creates a game UI injection (modifies existing game UI). For Gemini HUD UI, use `/add-component` or `/add-section`.

---

## Step 1: Ask Questions

### 1. Injection Purpose
```
What game UI element does this modify?
Brief description:
```

### 2. Target Elements
```
Which game UI elements are targeted?

Examples:
- Inventory panel
- Shop interface
- Player stats display
- Game toolbar
- Chat window
```

### 3. Modification Type
```
What modifications are made?

[ ] Add new elements (buttons, indicators, overlays)
[ ] Modify existing elements (styles, text, attributes)
[ ] Add event listeners (click handlers, observers)
[ ] Inject data displays (stats, timers, counters)
```

### 4. Game Data
```
Does it need game data?

A) Static data → MGData
B) Real-time state → Globals
C) Both
D) None
```

### 5. Sprites
```
Does it display game sprites? → MGSprite.toCanvas()
```

### 6. Persistence
```
Does it need persistent state?

A) Yes - User preferences saved
B) No - Stateless
```

---

## Step 2: Create Structure

```
src/ui/inject/qol/<featureName>/
├── index.ts        # Public API (init, destroy, isEnabled)
├── inject.ts       # DOM injection logic
├── styles.css.ts   # Scoped styles (optional)
└── state.ts        # Persistent state (optional)
```

---

## Step 3: File Templates

### index.ts

```typescript
/**
 * <FeatureName> Game UI Injection
 *
 * <Description of what it modifies>
 */

import { injectElements, removeElements } from './inject';

// ─────────────────────────────────────────────────────────────────────────────
// State
// ─────────────────────────────────────────────────────────────────────────────

let injected = false;
const cleanups: (() => void)[] = [];

// ─────────────────────────────────────────────────────────────────────────────
// Public API
// ─────────────────────────────────────────────────────────────────────────────

export const <FeatureName>Inject = {
    /**
     * Inject into game UI
     * Idempotent - safe to call multiple times
     */
    init(): void {
        if (injected) return;
        injected = true;

        const cleanup = injectElements();
        if (cleanup) cleanups.push(cleanup);

        console.log('[<FeatureName>Inject] Initialized');
    },

    /**
     * Remove all injected elements
     * Idempotent - safe to call multiple times
     */
    destroy(): void {
        if (!injected) return;

        cleanups.forEach(fn => fn());
        cleanups.length = 0;
        removeElements();

        injected = false;
        console.log('[<FeatureName>Inject] Destroyed');
    },

    /**
     * Check if injection is active
     */
    isEnabled(): boolean {
        return injected;
    },
};
```

### inject.ts

```typescript
/**
 * <FeatureName> DOM Injection Logic
 */

import { <featureName>Css } from './styles.css';
// If using sprites:
// import { MGSprite } from '../../../../modules/sprite';
// If using game data:
// import { MGData } from '../../../../modules/data';
// If using globals:
// import { getMyInventory } from '../../../../globals/variables/myInventory';

// ─────────────────────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────────────────────

const CONTAINER_SELECTOR = '.game-ui-container';  // Adjust to target element
const INJECT_CLASS = 'gemini-qol-<featureName>';

// ─────────────────────────────────────────────────────────────────────────────
// Injection
// ─────────────────────────────────────────────────────────────────────────────

export function injectElements(): (() => void) | null {
    const container = document.querySelector(CONTAINER_SELECTOR);
    if (!container) {
        console.warn('[<FeatureName>Inject] Container not found');
        return null;
    }

    const cleanups: (() => void)[] = [];

    // Inject styles
    const style = document.createElement('style');
    style.textContent = <featureName>Css;
    style.setAttribute('data-gemini', '<featureName>');
    document.head.appendChild(style);
    cleanups.push(() => style.remove());

    // Create injected element
    const wrapper = document.createElement('div');
    wrapper.className = INJECT_CLASS;
    // ... build element
    container.appendChild(wrapper);
    cleanups.push(() => wrapper.remove());

    // Add event listeners (track for cleanup!)
    const handleClick = () => { /* ... */ };
    wrapper.addEventListener('click', handleClick);
    cleanups.push(() => wrapper.removeEventListener('click', handleClick));

    // Subscribe to globals (track for cleanup!)
    // const unsub = getMyInventory().subscribe((inv) => { /* update UI */ });
    // cleanups.push(unsub);

    // Return combined cleanup
    return () => {
        cleanups.forEach(fn => fn());
    };
}

export function removeElements(): void {
    // Remove all injected elements by class
    document.querySelectorAll(`.${INJECT_CLASS}`).forEach(el => el.remove());

    // Remove injected styles
    document.querySelectorAll('style[data-gemini="<featureName>"]').forEach(el => el.remove());
}
```

### styles.css.ts

```typescript
/**
 * <FeatureName> Injection Styles
 *
 * Scoped to .gemini-qol-<featureName>
 */

export const <featureName>Css = `
    .gemini-qol-<featureName> {
        /* Use CSS variables when possible */
        position: absolute;
        z-index: 100;
    }

    .gemini-qol-<featureName>__button {
        background: var(--color-primary, #4a9eff);
        color: var(--color-text, #fff);
        border: none;
        border-radius: 4px;
        padding: 8px 12px;
        cursor: pointer;
        min-height: 44px;  /* Touch-friendly */
    }

    .gemini-qol-<featureName>__button:hover {
        opacity: 0.9;
    }
`;
```

### state.ts (if persistent)

```typescript
/**
 * <FeatureName> Injection State
 */

import { storageGet, storageSet } from '../../../../utils/storage';

const STORAGE_KEY = 'inject:<featureName>:config';

export interface <FeatureName>Config {
    enabled: boolean;
    // ... other settings
}

const DEFAULT_CONFIG: <FeatureName>Config = {
    enabled: true,
};

export function loadConfig(): <FeatureName>Config {
    return storageGet(STORAGE_KEY, DEFAULT_CONFIG);
}

export function saveConfig(config: <FeatureName>Config): void {
    storageSet(STORAGE_KEY, config);
}
```

---

## Step 4: Register (if standalone)

If this injection is standalone (not part of a feature):

### Export → `src/ui/inject/qol/index.ts`

```typescript
export { <FeatureName>Inject } from './<featureName>';
```

### Initialize in bootstrap or feature

```typescript
import { <FeatureName>Inject } from '../../ui/inject/qol/<featureName>';

// Initialize
<FeatureName>Inject.init();

// Cleanup
<FeatureName>Inject.destroy();
```

---

## Step 5: Validate

### Structure
- [ ] `index.ts` with `init()`, `destroy()`, `isEnabled()`
- [ ] `inject.ts` with `injectElements()`, `removeElements()`
- [ ] `styles.css.ts` with scoped classes
- [ ] `state.ts` (if persistent)

### Lifecycle
- [ ] `init()` is idempotent (guard against double-inject)
- [ ] `destroy()` removes ALL injected elements
- [ ] All event listeners tracked and removed
- [ ] All MutationObservers disconnected
- [ ] All intervals/timeouts cleared
- [ ] All Global subscriptions unsubscribed

### Styling
- [ ] Classes prefixed with `gemini-qol-<name>`
- [ ] Uses CSS variables where possible
- [ ] Touch-friendly (44px min targets)
- [ ] Styles removed on destroy

### Game Data (if applicable)
- [ ] Uses `MGData.get()` (no hardcoded data)
- [ ] Uses `MGSprite.toCanvas()` (no hardcoded sprite paths)
- [ ] Globals subscribed with cleanup

### Boundaries
- [ ] Only modifies game UI (never Gemini HUD)
- [ ] No imports from `src/ui/components/` or `src/ui/hud/`
- [ ] No Shadow DOM

---

## Integration with Features

If the injection is part of a feature:

```typescript
// In src/features/<featureName>/index.ts
import { <FeatureName>Inject } from '../../ui/inject/qol/<featureName>';

function init(): void {
    // ... feature init
    <FeatureName>Inject.init();
}

function destroy(): void {
    <FeatureName>Inject.destroy();
    // ... feature cleanup
}
```

---

## References

- Rules: `.claude/rules/ui/ui.inject.md`
- Existing injections: `src/ui/inject/qol/*/`
- Storage: `src/utils/storage.ts`
