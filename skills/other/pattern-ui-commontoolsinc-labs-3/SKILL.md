---
name: pattern-ui
description: Add UI polish with layout and styling
user-invocable: false
---

# UI Polish Phase

Only do this AFTER all logic is verified and tests pass.

## Read First
- `docs/common/components/COMPONENTS.md` - Full component reference
- `docs/common/patterns/style.md` - Styling patterns
- `docs/common/patterns/two-way-binding.md` - $value, $checked bindings

## Available Components

Layout: `ct-screen`, `ct-vstack`, `ct-hstack`, `ct-box`
Input: `ct-input`, `ct-textarea`, `ct-checkbox`, `ct-select`
Action: `ct-button`
Display: `ct-text`, `ct-status-pill`

## Key Patterns

**Two-way binding:**
```tsx
<ct-input $value={field} />
<ct-checkbox $checked={done} />
```

**Layout structure:**
```tsx
<ct-screen title="My Pattern">
  <ct-vstack gap="md">
    <ct-hstack gap="sm">
      {/* horizontal items */}
    </ct-hstack>
  </ct-vstack>
</ct-screen>
```

## Reference Existing Patterns
Search `packages/patterns/` for UI layout examples ONLY (not data/action patterns).

## Done When
- UI renders correctly
- Bindings work (typing updates state)
- No regression in data behavior
