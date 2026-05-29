---
name: focus-management
description: Keyboard focus management patterns for accessibility. Covers focus traps, roving tabindex, focus restore, skip links, and FocusScope components for WCAG-compliant interactive widgets. Use when implementing focus traps or keyboard navigation.
context: fork
agent: accessibility-specialist
version: 1.0.0
tags: [accessibility, focus, keyboard, a11y, trap]
allowed-tools: [Read, Write, Edit, Grep, Glob]
author: SkillForge
user-invocable: false
---

# Focus Management

Essential patterns for managing keyboard focus in accessible web applications, ensuring keyboard-only users can navigate complex interactive components.

## Overview

- Building modals, dialogs, or drawers that require focus trapping
- Implementing tab panels, menus, or toolbars with roving tabindex
- Restoring focus after closing overlays or completing actions
- Creating skip links for keyboard navigation
- Ensuring focus visibility meets WCAG 2.4.7 requirements

## Quick Reference

### FocusScope Trap (React Aria)

```tsx
import { FocusTrap } from '@react-aria/focus';

function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;
  return (
    <div role="dialog" aria-modal="true">
      <FocusTrap>
        <div className="modal-content">
          {children}
          <button onClick={onClose}>Close</button>
        </div>
      </FocusTrap>
    </div>
  );
}
```

### Roving Tabindex

```tsx
function TabList({ tabs, onSelect }) {
  const [activeIndex, setActiveIndex] = useState(0);
  const tabRefs = useRef<HTMLButtonElement[]>([]);

  const handleKeyDown = (e: KeyboardEvent, index: number) => {
    const keyMap: Record<string, number> = {
      ArrowRight: (index + 1) % tabs.length,
      ArrowLeft: (index - 1 + tabs.length) % tabs.length,
      Home: 0, End: tabs.length - 1,
    };
    if (e.key in keyMap) {
      e.preventDefault();
      setActiveIndex(keyMap[e.key]);
      tabRefs.current[keyMap[e.key]]?.focus();
    }
  };

  return (
    <div role="tablist">
      {tabs.map((tab, i) => (
        <button key={tab.id} ref={(el) => (tabRefs.current[i] = el!)}
          role="tab" tabIndex={i === activeIndex ? 0 : -1}
          aria-selected={i === activeIndex}
          onKeyDown={(e) => handleKeyDown(e, i)}
          onClick={() => { setActiveIndex(i); onSelect(tab); }}>
          {tab.label}
        </button>
      ))}
    </div>
  );
}
```

### Focus Restore

```tsx
function useRestoreFocus(isOpen: boolean) {
  const triggerRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      triggerRef.current = document.activeElement as HTMLElement;
    } else if (triggerRef.current) {
      triggerRef.current.focus();
      triggerRef.current = null;
    }
  }, [isOpen]);
}
```

## Key Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Trap vs Contain | `FocusTrap` (strict) | `FocusScope` (soft) | Trap for modals, Scope for popovers |
| Restore strategy | Trigger element | Last focused | Always restore to trigger |
| Skip links | Single main skip | Multiple landmarks | Multiple for complex layouts |
| Initial focus | First focusable | Auto-focus input | Context-dependent, prefer inputs |
| Focus visible | Browser default | Custom outline | Custom `:focus-visible` for consistency |

## Anti-Patterns (FORBIDDEN)

```tsx
// NEVER use positive tabindex - breaks natural tab order
<button tabIndex={5}>Bad</button>

// NEVER remove focus outline without replacement (WCAG 2.4.7)
button:focus { outline: none; }

// NEVER trap focus without Escape key handler
<FocusTrap><div>No way out!</div></FocusTrap>

// NEVER auto-focus without user expectation
useEffect(() => inputRef.current?.focus(), []);

// NEVER hide skip links permanently - must be visible on focus
.skip-link { display: none; }
```

## Related Skills

- `a11y-testing` - Test focus management with Playwright and axe
- `design-system-starter` - Focus indicators in design tokens
- `motion-animation-patterns` - Animate focus transitions accessibly

## Capability Details

### focus-trap
**Keywords:** focus trap, modal focus, dialog focus, FocusTrap, aria-modal
**Solves:**
- Trap focus within modals and dialogs
- Prevent focus escaping to background content
- Handle Escape key to close and release trap

### roving-tabindex
**Keywords:** roving tabindex, arrow navigation, tablist, menu keyboard
**Solves:**
- Navigate widget items with arrow keys
- Maintain single tab stop for composite widgets
- Support Home/End for quick navigation

### focus-restore
**Keywords:** focus restore, return focus, trigger focus, focus memory
**Solves:**
- Return focus to trigger after closing overlay
- Preserve focus context across interactions
- Handle focus when elements are removed from DOM
