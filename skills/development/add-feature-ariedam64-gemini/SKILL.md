---
name: add-feature
description: Scaffold a new toggleable feature with full structure, storage, API exposure, and bootstrap registration
aliases: [new-feature, create-feature, scaffold-feature]
---

# Add Feature Skill

## Usage
```
/add-feature <featureName>
```

---

## Step 1: Ask Questions

Before creating files, gather this information:

### 1. Game Data (CRITICAL)
```
Does this feature need game data?

A) Static data → MGData
B) Real-time state → Globals
C) Both → MGData + Globals
D) None
```

**If A or C (Static data), specify which:**
```
[ ] Plants - definitions, growth stages, harvest data
[ ] Items - definitions, categories, properties
[ ] Pets - definitions, abilities, stats
[ ] Mutations - definitions, effects
[ ] Shops - configurations (not stock)
[ ] Recipes - crafting recipes
[ ] Other: ___________
```

**If B or C (Real-time), specify which:**
```
[ ] currentTile - player's current tile
[ ] myGarden - player's garden state
[ ] myInventory - player's inventory
[ ] myPets - player's pets
[ ] players - other players in room
[ ] shops - current shop stock
[ ] weather - current weather
[ ] gameMap - full map data
[ ] Other: ___________
```

### 2. UI Type
```
A) Gemini HUD only - UI in Gemini overlay
B) Game UI injection - Modifies existing game UI (src/ui/inject/qol/<name>/)
C) Both - Feature logic + game UI injection
D) No UI - Backend/logic only
```

### 3. Sprites (if UI selected)
```
Does the UI need game sprites?

A) Yes → MGSprite.show() / MGSprite.toCanvas()
B) No - Text/icons only

If A, which types?
[ ] Plant sprites  [ ] Item sprites  [ ] Pet sprites
[ ] Cosmetic sprites  [ ] Tile sprites  [ ] Other: ___
```

### 4. UI Components (if UI selected)
```
Does the UI need existing components?
→ REUSE, never recreate!

[ ] ArcadeButton, GeminiIconButton → Buttons
[ ] Modal → Dialogs/popups
[ ] ProgressBar → Progress indicators
[ ] SegmentedControl → Tab-like selection
[ ] Tab → Tabs
[ ] SoundPicker → Audio selection
[ ] Other from src/ui/components/
```

### 5. Module Dependencies
```
[ ] MGCalculators - XP, prices, growth time calculations
[ ] MGCosmetic - Player cosmetic data
[ ] MGTile - Map/tile utilities
[ ] MGAudio - Sound effects, notifications
[ ] MGShopActions - Buy/sell operations
[ ] MGEnvironment - World/environment data
[ ] None
```

### 6. WebSocket
```
A) Outgoing actions - Sends messages (api.ts)
B) Incoming handlers - Reacts to server messages
C) Middleware - Intercept/block/modify outgoing messages
D) Multiple (specify which)
E) None
```

**If C (Middleware), specify:**
```
[ ] Intercept specific message types
[ ] Modify payload before sending
[ ] Block messages based on conditions
[ ] Log/track outgoing messages
Which message types? ___________
```

### 7. Brief Description
```
One sentence for documentation:
```

---

## Step 2: Create Structure

```
src/features/<featureName>/
├── types.ts        # Config, constants, types
├── state.ts        # Storage operations
├── index.ts        # Public API (MG<FeatureName>)
├── logic/
│   └── core.ts     # Business logic
├── ui.ts           # (if HUD UI)
├── handler.ts      # (if incoming WS)
└── middleware.ts   # (if WS middleware)
```

### Naming Conventions
- Folder: `camelCase` → `src/features/autoHarvest/`
- Public API: `MG<PascalCase>` → `MGAutoHarvest`
- Storage key: `SCREAMING_SNAKE` → `AUTO_HARVEST`
- Storage value: `feature:<camelCase>:config` → `feature:autoHarvest:config`

### File Responsibilities

| File | Purpose |
|------|---------|
| `types.ts` | Config interface with `enabled: boolean`, `STORAGE_KEY`, `DEFAULT_CONFIG` |
| `state.ts` | `loadConfig()`, `saveConfig()`, `updateConfig()` |
| `index.ts` | `MG<Name>` with `init`, `destroy`, `isEnabled`, `setEnabled` |
| `logic/core.ts` | `start()`, `stop()`, `cleanups[]` array |
| `ui.ts` | HUD components (reuse existing!) |
| `handler.ts` | `registerHandlers()` for incoming WS |
| `middleware.ts` | `registerFeatureMiddleware()`, `unregisterFeatureMiddleware()` |

**Read existing features for templates:** `src/features/*/`

---

## Step 3: Register

### A) Storage key → `src/utils/storage.ts`
```typescript
export const FEATURE_KEYS = {
    // ... existing
    <FEATURE_NAME>: 'feature:<featureName>:config',
} as const;
```

### B) Export → `src/features/index.ts`
```typescript
export { MG<FeatureName> } from './<featureName>';
export type { <FeatureName>Config } from './<featureName>';
```

### C) API → `src/api/index.ts`
```typescript
import { MG<FeatureName> } from "../features/<featureName>";

Features: {
    <FeatureName>: MG<FeatureName>,
}
```

### D) Bootstrap → `src/ui/loader/bootstrap.ts`
```typescript
import { MG<FeatureName> } from "../../features/<featureName>";

{ name: "<FeatureName>", init: () => MG<FeatureName>.init() }
```

### E) Game UI injection (if applicable)
Create structure in `src/ui/inject/qol/<featureName>/`:
```
├── index.ts       # init(), destroy(), isEnabled()
├── inject.ts      # DOM injection logic
├── styles.css.ts  # Scoped styles
└── state.ts       # (optional)
```

---

## Step 4: Key Patterns

### Using Globals (reactive state)
```typescript
import { getMyInventory } from '../../../globals/variables/myInventory';

const cleanups: (() => void)[] = [];

function start(): void {
    const unsub = getMyInventory().subscribe((inventory) => {
        // React to changes
        onInventoryChange(inventory);
    });
    cleanups.push(unsub);
}

function stop(): void {
    cleanups.forEach(fn => fn());
    cleanups.length = 0;
}
```

### Using Middleware
```typescript
import { registerMiddleware } from '../../websocket/middlewares/registry';

let unregister: (() => void) | null = null;

export function registerFeatureMiddleware(): void {
    if (unregister) return;
    unregister = registerMiddleware((message) => {
        // Return message (pass), modified message, or null (block)
        return message;
    });
}

export function unregisterFeatureMiddleware(): void {
    unregister?.();
    unregister = null;
}
```

### UI with existing components
```typescript
import { createArcadeButton, createProgressBar } from '../../ui/components';

function buildUI(container: HTMLElement): void {
    const button = createArcadeButton({ label: 'Action', onClick: handleClick });
    const progress = createProgressBar({ value: 0, max: 100 });

    container.appendChild(button.root);
    container.appendChild(progress.root);

    // Track for cleanup
    cleanups.push(() => {
        button.destroy();
        progress.destroy();
    });
}
```

---

## Step 5: Validate

### Structure
- [ ] `types.ts` with `enabled: boolean` in config
- [ ] `index.ts` exports `MG<FeatureName>`
- [ ] Public API: `init`, `destroy`, `isEnabled`, `setEnabled`
- [ ] `logic/` folder for business logic

### Lifecycle
- [ ] `init()` is idempotent (safe to call multiple times)
- [ ] `destroy()` cleans up ALL resources
- [ ] No side effects on import
- [ ] Uses `FEATURE_KEYS` (not `MODULE_KEYS`)

### Game Data (NEVER hardcode!)
- [ ] Static data → `MGData.get('plants'/'items'/'pets'/...)`
- [ ] Sprites → `MGSprite.show()` / `MGSprite.toCanvas()`
- [ ] Calculations → `MGCalculators`
- [ ] Real-time → Globals with `.subscribe()` + unsubscribe in cleanup

### UI (if applicable)
- [ ] Reuses existing components (never recreate Button, Modal, etc.)
- [ ] Child components' `destroy()` called in cleanup
- [ ] Uses CSS variables (no hardcoded colors)
- [ ] If injection: fully removes DOM on destroy

### WebSocket (if applicable)
- [ ] Actions via `websocket/api.ts` only
- [ ] Handlers via `registerHandler()`
- [ ] Middleware returns `message` or `null`, never throws
- [ ] Middleware unregisters on `destroy()`
- [ ] Message types from `protocol.ts` enums

### Registration
- [ ] Storage key in `src/utils/storage.ts`
- [ ] Export in `src/features/index.ts`
- [ ] Exposed in `src/api/index.ts`
- [ ] Initialized in `src/ui/loader/bootstrap.ts`

---

## References

- Rules: `.claude/rules/features.md`, `.claude/rules/core.md`
- Existing features: `src/features/*/`
- Modules: `src/modules/*/` (MGData, MGSprite, MGCalculators, etc.)
- Globals: `src/globals/variables/`
- WebSocket: `src/websocket/` (api.ts, middlewares/, handlers/)
- UI Components: `src/ui/components/`
- UI Injection: `src/ui/inject/qol/`, `.claude/rules/ui/ui.inject.md`
