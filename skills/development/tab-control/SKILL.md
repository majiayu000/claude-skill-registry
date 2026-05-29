---
name: tab-control
description: Guide for implementing keyboard navigation and focus indicators across macOS native app (WKWebView) and web browser versions. Use when adding focusable elements, fixing Tab key navigation, or debugging focus ring visibility issues.
---

# Tab Control & Focus Management

This skill documents how keyboard navigation and focus indicators work across the macOS native app and standard web browser.

## The Problem

When running as a native Mac app via Swift/WKWebView, keyboard events are intercepted before reaching JavaScript. This means:
- Tab key doesn't navigate focus normally
- `focus-visible` CSS pseudo-class doesn't trigger when focus is set programmatically
- Cmd+Enter and other shortcuts need special handling

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Swift (AppDelegate.swift)                                  │
│  - NSEvent.addLocalMonitorForEvents intercepts keys         │
│  - Calls dispatchKeyToWebView() for handled keys            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼ evaluateJavaScript
┌─────────────────────────────────────────────────────────────┐
│  Global Handlers (useNativeKeyboardBridge.ts)               │
│  - window.__nativeFocusNext() - Tab navigation              │
│  - window.__nativeFocusPrevious() - Shift+Tab navigation    │
│  - Checks context: ProseMirror editor vs regular elements   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│  ProseMirror Editor     │     │  Regular Elements           │
│  - Dispatches synthetic │     │  - Moves focus to next/prev │
│    Tab KeyboardEvent    │     │    focusable element        │
│  - Editor handles       │     └─────────────────────────────┘
│    indent/outdent       │
└─────────────────────────┘
```

## Tab in Rich Text Editors (ProseMirror)

When focus is inside a ProseMirror editor, Tab should trigger editor-specific behavior (like indentation) rather than moving focus to the next element.

### How It Works

The `__nativeFocusNext` and `__nativeFocusPrevious` functions detect ProseMirror context:

```typescript
// Check if focus is in a ProseMirror editor
const isInProseMirrorEditor = (): HTMLElement | null => {
    const activeElement = document.activeElement as HTMLElement | null;
    if (!activeElement) return null;

    // Check if active element or parent is ProseMirror contenteditable
    const proseMirrorEditor = activeElement.closest('.ProseMirror[contenteditable="true"]');
    return proseMirrorEditor as HTMLElement | null;
};

// In focusNext():
const editor = isInProseMirrorEditor();
if (editor) {
    // Dispatch synthetic Tab event - let ProseMirror handle it
    const event = new KeyboardEvent('keydown', {
        key: 'Tab',
        code: 'Tab',
        keyCode: 9,
        shiftKey: false, // or true for Shift-Tab
        bubbles: true,
        cancelable: true,
    });
    editor.dispatchEvent(event);
    return;
}
// Otherwise, move focus normally...
```

### Implementing Tab Indentation in ProseMirror

For text-based lists (paragraphs with `- [ ]` or `- ` markers), add keymap handlers:

```typescript
// In simple-todo.ts or similar
export const handleTodoIndent: Command = (state, dispatch) => {
    // 1. Check if on a todo/bullet line
    // 2. Check if there's a valid parent item above
    // 3. Add indentation (e.g., 2 spaces) to line start
    // 4. Return true to indicate handled
};

export const todoKeymap = keymap({
    "Tab": handleTodoIndent,
    "Shift-Tab": handleTodoOutdent,
});
```

For ProseMirror's native list nodes, use `prosemirror-schema-list`:

```typescript
import { sinkListItem, liftListItem } from "prosemirror-schema-list";

const listKeymap = keymap({
    "Tab": sinkListItem(schema.nodes.list_item),
    "Shift-Tab": liftListItem(schema.nodes.list_item),
});
```

### Key Behavior

| Context | Tab | Shift-Tab |
|---------|-----|-----------|
| ProseMirror on todo/bullet | Indents item | Outdents item |
| ProseMirror on regular text | No action (not handled) | No action |
| Button/input/other element | Moves focus forward | Moves focus backward |

## Critical Rule: Use `focus` Not `focus-visible`

**Problem:** When the native keyboard bridge calls `element.focus()` programmatically, browsers don't trigger the `focus-visible` pseudo-class because they don't detect "keyboard navigation".

**Solution:** Always use `focus:` instead of `focus-visible:` for focus indicators.

```tsx
// BAD - Won't show focus ring in Mac app
className="focus-visible:outline focus-visible:outline-2"

// GOOD - Always shows focus ring when focused
className="focus:outline focus:outline-2 focus:outline-offset-2"
```

The Button component (`src/components/ui/button.tsx`) already uses this pattern.

## Implementing Focus Indicators

### For Custom Buttons/Triggers

```tsx
<button
  className="focus:outline-none focus:ring-2 focus:ring-offset-1"
  style={{
    // Use theme color for the ring
    "--tw-ring-color": currentTheme.styles.contentAccent
  }}
>
  Click me
</button>
```

### For Pill/Badge Buttons (like in dialogs)

```tsx
<button
  className="px-3 py-1.5 rounded-md transition-colors hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-offset-1"
  style={{
    backgroundColor: styles.surfaceTertiary,
    color: styles.contentPrimary,
  }}
>
  Status
</button>
```

## Handling Cmd+Enter in Dialogs

Use the `useNativeSubmit` hook for forms that should submit on Cmd+Enter:

```tsx
import { useNativeSubmit } from "@/hooks/useNativeKeyboardBridge";

function MyDialog({ open, onSubmit }) {
  useNativeSubmit(() => {
    if (open && isValid && !loading) {
      onSubmit();
    }
  });

  return (/* dialog content */);
}
```

## Making Containers Keyboard Navigable

For lists/tables that need arrow key navigation, add `tabIndex={0}` and `onKeyDown`:

```tsx
// Example from ProjectBrowserView.tsx
<Table
  ref={tableRef}
  tabIndex={0}
  onKeyDown={handleKeyDown}
  className="outline-none"
>
```

For Kanban-style views using global shortcuts via `useKeyboardShortcuts`, ensure the `when` conditions don't block navigation:

```tsx
useKeyboardShortcuts([
  {
    id: 'navigate-down',
    combo: { key: 'ArrowDown' },
    handler: navigateDown,
    when: () => items.length > 0 && document.activeElement !== searchInputRef.current,
  },
], { onlyWhenActive: true });
```

## Dialog Focus Management

1. **Remove X button from tab order**: Set `tabIndex={-1}` on close buttons
2. **Auto-focus first action**: Add `autoFocus` to Cancel or first button
3. **Show keyboard hint**: Display Cmd+Enter shortcut under primary buttons

```tsx
<div className="flex items-center gap-2">
  <Button variant="ghost" onClick={handleCancel}>
    Cancel
  </Button>
  <Button onClick={handleSubmit}>
    Save
    <KeyboardIndicator keys={["cmd", "enter"]} />
  </Button>
</div>
```

## Key Files

| File | Purpose |
|------|---------|
| `src/hooks/useNativeKeyboardBridge.ts` | Global focus navigation + ProseMirror detection |
| `src/features/notes/simple-todo.ts` | Todo/bullet Tab indent handlers |
| `src/components/ui/button.tsx` | Button with proper focus styling |
| `docs/mac-app-keyboard-shortcuts.md` | Full keyboard bridge documentation |
| `mac-app/macos-host/Sources/AppDelegate.swift` | Swift keyboard interception |

## Debugging Focus Issues

1. **Focus ring not showing?**
   - Check if using `focus-visible` instead of `focus`
   - Verify element has `tabIndex` if it's not naturally focusable

2. **Tab not moving focus in Mac app?**
   - Ensure `useNativeKeyboardBridge` is initialized at app root
   - Check if element is in the focusable elements list

3. **Tab not indenting in ProseMirror (Mac app)?**
   - Verify `isInProseMirrorEditor()` detects the editor (check for `.ProseMirror[contenteditable="true"]`)
   - Ensure the keymap with Tab handler is added to the editor's plugins
   - Check that the handler returns `true` when it handles the event

4. **Tab indents in browser but not Mac app?**
   - The synthetic KeyboardEvent must be dispatched to the editor element
   - Verify `dispatchTabEvent()` is called with the correct element
   - Check browser console for any errors in the keyboard bridge

5. **Shortcuts not firing?**
   - Check if a dialog is open (shortcuts are disabled when `[role="dialog"]` exists)
   - Verify `when` condition returns true
   - Check `onlyWhenActive` and whether the tab is active

## Browser vs Mac App Behavior

| Feature | Browser | Mac App |
|---------|---------|---------|
| Tab navigation | Native | Via `__nativeFocusNext` |
| Tab in ProseMirror | Native KeyboardEvent | Synthetic KeyboardEvent via bridge |
| focus-visible | Works | Doesn't trigger |
| Cmd+Enter | KeyboardEvent | CustomEvent 'nativeSubmit' |
| Arrow keys | Native | Native (not intercepted) |
