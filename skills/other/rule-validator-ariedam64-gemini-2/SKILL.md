---
name: rule-validator
description: Validate code compliance with Gemini mod rules (core, modules, features, UI, WebSocket, state)
aliases: [validate, check-rules, lint-rules]
---

# Gemini Rules Validator Skill

## How to Use
When you want to validate code compliance:

```
/rule-validator src/features/myFeature
/rule-validator <file-or-folder>
/validate  # Validate current selection
```

## Validation Scope

### 1. Core Rules (src/*)
Applies to **all code** in the repo.

#### Rule 1: No Hardcoded Game Data
**Forbidden patterns:**
- Plant names: `'Carrot'`, `'Tomato'`, etc.
- Item IDs: hardcoded numeric item IDs
- Pet/mutation/shop data as strings/numbers
- Sprite frame references as literals

**Check for:**
```typescript
// ❌ BAD
const plantName = 'Carrot';
const itemId = 42;
const spriteName = 'plant_carrot_lvl1';

// ✅ GOOD
const plant = MGData.get('plants')['carrot'];
const item = MGData.get('items')[itemId];
const sprite = await MGSprite.show('plant', plantName);
```

**What to report:**
- File + line number
- The hardcoded value
- Suggested fix: "Use MGData.get(...) instead"

---

#### Rule 2: Boundaries (DOM, WebSocket, State)
**Forbidden:**
- DOM rendering outside `src/ui/`
- Direct WebSocket sends (`websocket.send()` outside `src/websocket/api.ts`)
- Direct state mutations (not via Store API)
- Ad-hoc globals (`window.myGlobal = ...` as second source of truth)

**Check for:**
```typescript
// ❌ BAD - in src/features/myFeature/index.ts
document.createElement('div');  // DOM in features
websocket.send(message);        // Direct WS send
window.myState = value;         // Ad-hoc global
atom.value = newValue;          // Direct mutation

// ✅ GOOD
// In src/ui/components/...
const root = document.createElement('div');

// In src/websocket/api.ts
export function sendAction(...) { websocket.send(...) }

// In src/features/...
const unsub = await Store.subscribe('myAtom', callback);
```

**What to report:**
- File + line number
- Pattern detected
- Suggested fix: "Move DOM to src/ui/" or "Use Store API" etc.

---

#### Rule 3: Side Effects & Cleanup
**Forbidden on import:**
- Event listeners without cleanup
- Intervals/timeouts without cancellation
- WebSocket subscriptions without unsubscribe
- Audio playback on import
- Patches or monkey-patching

**Check for:**
```typescript
// ❌ BAD - at module level
window.addEventListener('click', handler);  // No cleanup
setInterval(() => {...}, 1000);             // Runs forever
const unsub = Store.subscribe(...);         // Unsub lost

// ✅ GOOD
let unsub: (() => void) | null = null;
export function init() {
  window.addEventListener('click', handler);
  unsub = () => window.removeEventListener('click', handler);
}
export function destroy() {
  unsub?.();
  unsub = null;
}
```

**What to report:**
- File + line number
- Effect type (listener, interval, etc.)
- Pattern: "Side effect at module level detected"
- Suggestion: "Wrap in init()/destroy() functions"

---

#### Rule 4: Storage Namespacing
**Forbidden:**
- Direct `GM_getValue`/`GM_setValue` calls
- Non-namespaced keys
- Undefined storage keys

**Check for:**
```typescript
// ❌ BAD
GM_setValue('myKey', value);
const key = 'random-key';

// ✅ GOOD
import { KEYS } from 'src/utils/storage';
GM_setValue(KEYS.MY_FEATURE, value);  // Prefixed with gemini:
```

**What to report:**
- File + line number
- Key used (if visible)
- Suggestion: "Use KEYS from src/utils/storage"

---

#### Rule 5: Code Quality (Files < 500 lines)
**Check for:**
- Files exceeding 500 lines
- Functions exceeding 50 lines (warning threshold)
- Single-letter variable names (a, i, x outside loops)
- Magic numbers/strings without constants

**What to report:**
- File + line count
- Suggestion: "Split by responsibility"
- Magic numbers: "Extract to const CONSTANT_NAME"

---

#### Rule 6: TypeScript Strict (no `any`)
**Forbidden:**
- `any` type usage
- Unconstrained generics

**Check for:**
```typescript
// ❌ BAD
function handle(data: any) {}

// ✅ GOOD
function handle(data: unknown) {
  if (typeof data === 'object' && data !== null) { ... }
}
```

**What to report:**
- File + line number
- The `any` usage
- Suggestion: "Use `unknown` + type narrowing"

---

### 2. Feature Rules (src/features/*)

#### Feature Structure Check
**Expected files:**
```
src/features/myFeature/
├── types.ts           # ✅ Required
├── index.ts           # ✅ Required
├── state.ts           # ⚠️ If persistent state
├── ui.ts              # ⚠️ If visual elements
├── middleware.ts      # ⚠️ If WS outgoing
├── handler.ts         # ⚠️ If WS incoming
└── logic/             # 📁 Recommended
    ├── core.ts
    └── helpers.ts
```

**Check for:**
- Missing `types.ts` or `index.ts`
- Config without `enabled: boolean`
- Storage key not using FEATURE_KEYS prefix

---

#### Feature API Exposure
**Check in `src/features/index.ts`:**
```typescript
// ✅ GOOD
export { MGMyFeature } from './myFeature';
export type { MyFeatureConfig } from './myFeature';
```

**Check in `src/api/index.ts`:**
```typescript
// ✅ GOOD
Features: {
  MyFeature: MGMyFeature,
}
```

**Check in `src/ui/loader/bootstrap.ts`:**
```typescript
// ✅ GOOD
{ name: "MyFeature", init: MGMyFeature.init.bind(MGMyFeature) }
```

**What to report:**
- Feature not exported from index.ts
- Feature not in GeminiAPI
- Feature not initialized in bootstrap

---

### 3. Module Rules (src/modules/*)

#### Module Structure
**Modules MUST:**
- Always be active (no toggle)
- Export named exports (not default)
- Have proper initialization if needed
- Be listed in core module list

**Check for:**
- Modules with `enabled` config (should be modules, not features)
- Toggles in module structure

---

### 4. UI Rules (src/ui/*)

#### Component Factory Pattern
**Check for factory violations:**
```typescript
// ❌ BAD
export function MyButton() { return <JSX>... }

// ✅ GOOD
export interface Options { label: string; onClick?: () => void }
export interface Handle { root: HTMLElement; destroy(): void }
export function create(options: Options): Handle { ... }
```

**What to report:**
- Missing Options/Handle interfaces
- No destroy() method
- Direct JSX exports

---

#### Shadow DOM Isolation
**Check for:**
- Direct DOM queries outside Shadow DOM boundary
- CSS not using CSS variables
- Hardcoded colors (should be theme tokens)

---

### 5. WebSocket Rules (src/websocket/*)

#### File Responsibilities
**Check locations:**
- Type definitions ONLY in `protocol.ts`
- Transport logic ONLY in `connection.ts`
- Public API ONLY in `api.ts`
- Handlers ONLY in `handlers/`
- Middlewares ONLY in `middlewares/`

**What to report:**
- Message type defined outside protocol.ts
- Logic mixed into wrong file

---

#### No Hardcoded Message Types
**Check for:**
```typescript
// ❌ BAD
if (type === 'plant_action') { ... }

// ✅ GOOD
import { WS_TYPES } from './protocol';
if (type === WS_TYPES.PLANT_ACTION) { ... }
```

---

## Validation Report Format

When violations are found, report as:

```
🚨 RULE VIOLATIONS FOUND (Gemini Mod)

[File: src/features/myFeature/index.ts]
├─ ❌ Rule 1: Hardcoded Game Data (line 42)
│  └─ Found: const plantName = 'Carrot'
│  └─ Fix: Use MGData.get('plants')['carrot']
│
├─ ⚠️  Rule 5: Code Quality (lines: 312)
│  └─ File exceeds 500 lines (actual: 612)
│  └─ Suggestion: Split by responsibility
│
└─ ❌ Rule 2: Boundaries (line 89)
   └─ Found: Direct WebSocket send
   └─ Fix: Use websocket/api.ts actions instead

✅ PASSED CHECKS:
├─ Feature structure (types.ts, index.ts present)
├─ Storage keys namespaced correctly
├─ TypeScript strict (no `any` found)
└─ Side effect cleanup present

📋 SUMMARY: 3 violations, 4 checks passed
💡 Next steps: Review suggested fixes above
```

---

## Usage in Review Workflows

### Before Commit
```
/rule-validator src/        # Validate entire src/
/rule-validator dist/       # Skip dist builds
```

### Before PR
```
/rule-validator src/features/newFeature
/rule-validator src/ui/components/NewComponent
```

### Full Repo Audit
```
/rule-validator .           # Entire project
```

---

## Configuration

### Ignore Patterns (Optional)
Can skip certain paths:
- `dist/` — Build output
- `node_modules/` — Dependencies
- `GameSourceFiles/` — Reference only
- `GameFilesExample/` — Examples only

### Severity Levels
- 🚨 **Error** — Must fix before commit
- ⚠️ **Warning** — Consider fixing
- ℹ️ **Info** — Best practice suggestion

---

## Common False Positives & How to Handle

| Detection | Reality | Action |
|-----------|---------|--------|
| `'Carrot'` in comment | Actually just documentation | Ignore |
| `any` in test file | Test-only, acceptable | Allow |
| 600-line file | Truly complex, can't split | Document why |
| WS send in tests | Mock data, OK | Allow |

**When reporting:** Flag but don't block if edge case is justified.

---

## Rules Priority (Strict → Lenient)

### 🔴 Strict (Never compromise)
1. No hardcoded game data (MGData required)
2. No direct WebSocket sends
3. No side effects on import
4. TypeScript strict (no `any`)

### 🟠 Medium (Be thoughtful)
5. Storage namespacing
6. File size (< 500 lines)
7. Cleanup discipline

### 🟡 Low (Guidance only)
8. Code organization
9. Naming conventions
10. Documentation

---

## Integration with /clear Workflow

When you `/clear` before starting a new task:
```
/rule-validator src/       # Run full validation
→ Fix any violations
→ Commit with pre-commit-gate skill
→ Proceed with clean slate
```

This ensures you never accumulate debt across task boundaries.
