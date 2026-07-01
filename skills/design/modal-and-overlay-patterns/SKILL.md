---
name: modal-and-overlay-patterns
description: Overlays — modals, drawers, bottom sheets, popovers — interrupt or augment the main flow. Each type has a different scope, blocking level, and appropriate use case. Use when designing dialogs, confirmation prompts, side panels, action sheets, or any UI element that appears above the main content layer.
metadata:
  priority: 7
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "modal"
      - "dialog"
      - "drawer"
      - "overlay"
      - "popover"
      - "bottom sheet"
      - "sheet"
      - "action sheet"
      - "side panel"
      - "lightbox"
      - "confirm"
      - "confirmation dialog"
retrieval:
  aliases:
    - modal dialog
    - overlay pattern
    - drawer panel
    - bottom sheet
    - popover
    - confirmation dialog
    - side panel
    - action sheet
  intents:
    - design a modal dialog
    - add a confirmation prompt
    - build a side drawer
    - choose between modal and drawer
    - design a bottom sheet for mobile
    - add a popover for contextual info
  examples:
    - add a confirm dialog before deleting
    - should this be a modal or a drawer
    - design a side panel for editing details
    - add a popover to explain this field
---

# Modal and Overlay Patterns

Overlays appear above the main content layer. They range from lightweight popovers (non-blocking, anchored to a trigger) to full blocking modals (require a user response before the app continues). Choosing the right overlay type for the task prevents unnecessary interruption and keeps the user oriented.

---

## The Overlay Hierarchy

Choose the lightest type that satisfies the task. Heavier overlays carry higher cognitive cost.

| Type | Blocks background | Anchored to trigger | Typical content | Dismiss with |
|---|---|---|---|---|
| **Tooltip** | No | Yes | 1–2 lines of explanatory text | Cursor leave / focus out |
| **Popover** | No | Yes | Short interactive content: a form field, a picker, a small list | Click outside, Escape, explicit close |
| **Dropdown / Menu** | No | Yes | List of actions or options | Click outside, Escape, selection |
| **Bottom sheet** (mobile) | Partial (dimmed) | No | Actions or content on small screens | Swipe down, tap scrim, Escape |
| **Drawer / Side panel** | Partial (dimmed) | No | Secondary editing, detail views, long forms | Escape, explicit close; optionally click scrim |
| **Dialog / Modal** | Yes (full scrim) | No | Blocking task: confirm action, fill required form | Escape (non-destructive only), explicit button |
| **Full-screen overlay** | Yes (complete) | No | Immersive task: media viewer, complex configuration | Explicit close only |

**Decision rule:** If the user can continue using the rest of the app while the overlay is open, use a non-blocking type (drawer, popover). If the app must wait for the user's response, use a modal.

---

## Tooltip

A tooltip appears on hover or keyboard focus and disappears when the trigger loses focus. It is purely informational — no interactive elements inside.

- Content: one short sentence, label, or keyboard shortcut. Never put a link or button inside a tooltip.
- Delay: 300–400ms on hover; no delay on keyboard focus.
- Position: prefer above the trigger; auto-flip when viewport edge is near.
- ARIA: `role="tooltip"` on the element; `aria-describedby` on the trigger pointing to the tooltip id.

---

## Popover

A popover is anchored to a trigger but contains interactive content — a colour picker, a date range selector, a small form, a list of filters. Unlike a tooltip, it stays open while the user interacts.

- Max width: 280–360px. For larger content, use a drawer.
- Position: anchored to the trigger; auto-flip to stay in viewport.
- Dismiss: click outside, Escape key, or explicit close button when the content is long.
- Focus: move focus into the popover when it opens; return focus to the trigger on close.
- ARIA: `role="dialog"` (if interactive) or `role="listbox"` (if a list); `aria-haspopup` on the trigger.

---

## Dropdown and Menu

A dropdown lists selectable options or actions anchored to a trigger button. It is the lightest interactive overlay.

- Separate **select dropdowns** (the user picks one value that persists) from **action menus** (the user triggers an action that doesn't persist as a value).
- Width: at least as wide as the trigger; cap at 280px.
- Long lists: add a search input at the top when there are more than 8–10 items.
- Keyboard: `↑`/`↓` to move between items, `Enter` to select, `Escape` to close.

---

## Bottom Sheet (Mobile)

On small screens, a bottom sheet replaces modals and popovers. It slides up from the bottom edge and feels native to touch devices.

- **Peek height:** Show a small portion of the sheet first (a handle + title), let the user drag to expand.
- **Full-height:** For longer content or forms that need the full viewport.
- Dismiss: swipe down, tap the scrim, or press Escape.
- Do not centre dialogs on mobile — use a bottom sheet instead (centred modals are too small and hard to reach).
- ARIA: treat as `role="dialog"` with the same focus management as a modal.

---

## Drawer / Side Panel

A drawer slides in from the left or right and partially covers the main content. Use it for secondary editing tasks, detail views, or settings that the user might refer back to while using the main content.

- **Right drawer:** Detail view, editing form, filter/sort panel. Most common.
- **Left drawer:** Navigation on mobile (hamburger menu pattern).
- Width: 320–480px on desktop. Full-width on mobile (effectively a bottom sheet or full-screen overlay instead).
- Scrim: a semi-transparent backdrop (`rgba(0,0,0,0.4)`) behind the drawer dims the main content.
- Dismiss: Escape key, explicit close button. Clicking the scrim is optional — avoid it when the drawer contains an unsaved form.
- Do not use a drawer when the task is blocking (e.g. a required decision). Use a modal instead.
- ARIA: `role="dialog"`, `aria-modal="true"`, `aria-labelledby` pointing to the drawer title.

---

## Modal / Dialog

A modal blocks the entire UI with a full scrim. Use it only when the app genuinely cannot continue without the user's response.

### When to use a modal

- Confirming a destructive or irreversible action
- A required form that must be submitted before continuing
- An error or warning that requires the user's acknowledgement

### When not to use a modal

- Displaying information the user can read at their leisure → use an inline notice or notification
- A task the user might want to do alongside the main content → use a drawer
- A large form with many fields → use a dedicated page or a drawer

### Anatomy

```
┌──────────────────────────────────┐
│  Title                      [✕]  │  ← Header: title + close button
├──────────────────────────────────┤
│                                  │
│  Body content                    │  ← Content: scrolls if needed
│  (description, form, media)      │
│                                  │
├──────────────────────────────────┤
│               [Cancel]  [Confirm]│  ← Footer: actions, right-aligned
└──────────────────────────────────┘
```

### Sizing

| Size | Width | Use for |
|---|---|---|
| Small | 360px | Short confirmations, single-field prompts |
| Medium | 480px | Standard dialogs, short forms |
| Large | 640px | Multi-field forms, richer content |
| Full-screen | 100% viewport | Immersive tasks; use sparingly |

Content that overflows the modal height should scroll within the **body area only** — the header and footer must remain visible.

### Dismiss behaviour

| Trigger | Allowed for non-destructive? | Allowed for destructive? |
|---|---|---|
| `Escape` key | Yes | No — require explicit Cancel |
| Click outside scrim | Yes (optional) | No — too easy to dismiss accidentally |
| Close button (✕) | Yes | Yes |
| Cancel button | Yes | Yes |

For destructive or irreversible actions: disable Escape and click-outside dismissal. The user must explicitly press Cancel or Confirm.

### Stacking modals

Avoid opening a modal from inside a modal. It signals an information architecture problem — the task is likely too complex for a single dialog.

If a secondary overlay is unavoidable, use a popover anchored inside the modal rather than another full modal. Never stack two blocking scrim overlays.

---

## Focus Management

Every overlay must manage focus correctly. Broken focus management is one of the most common accessibility failures.

### On open
1. Move focus to the first interactive element inside the overlay (usually the first field, or the confirm button for confirmations).
2. Trap focus: `Tab` and `Shift+Tab` cycle within the overlay only; focus cannot escape to the content behind the scrim.

### On close
Return focus to the element that triggered the overlay. If the trigger no longer exists (the element was deleted), move focus to a logical nearby element.

### Implementation note
Use a focus trap library or the native `<dialog>` element, which handles trapping natively in modern browsers. Rolling a manual focus trap is error-prone.

---

## ARIA for Modals and Drawers

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
>
  <h2 id="modal-title">Delete project?</h2>
  <p id="modal-description">
    This will permanently delete "Apollo" and all its data. This cannot be undone.
  </p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

- `role="dialog"` on the container
- `aria-modal="true"` tells screen readers to ignore content behind the overlay
- `aria-labelledby` points to the dialog title's id
- `aria-describedby` points to the description's id (optional but helpful for confirmations)
- The scrim backdrop should have `aria-hidden="true"` — screen readers must not read it

---

## Destructive Confirmation Pattern

Confirmation dialogs for destructive actions must name the item and consequence. Generic "Are you sure?" dialogs don't give enough context.

**Do:**
> Delete "Apollo Project"?
> This will permanently remove all tasks, files, and history. This cannot be undone.
> [Cancel] [Delete project]

**Don't:**
> Are you sure you want to do this?
> [No] [Yes]

- The primary destructive action button uses `--color-error` / `--color-danger`, not `--color-primary`.
- Label the destructive button explicitly: "Delete project", "Remove member", "Cancel order" — not just "OK" or "Confirm".
- Cancel is always on the left (or secondary position); destructive action on the right.

---

## Review Checklist

- [ ] Is the correct overlay type chosen for the task (tooltip / popover / menu / bottom sheet / drawer / modal)?
- [ ] Is a modal avoided when a drawer or inline pattern would suffice?
- [ ] Does the modal/drawer have a visible title, body, and clear action buttons?
- [ ] Does overflow content scroll within the body — with the header and footer fixed?
- [ ] Is Escape disabled for destructive actions (click-outside too)?
- [ ] Does focus move into the overlay on open, and return to the trigger on close?
- [ ] Is focus trapped within the overlay while it's open?
- [ ] Is `role="dialog"`, `aria-modal="true"`, `aria-labelledby` set correctly?
- [ ] Does the destructive confirm dialog name the item and describe the consequence?
- [ ] Is the destructive button labelled explicitly (not "OK" or "Confirm")?
- [ ] Are stacked modals avoided?
- [ ] On mobile, are modals replaced with bottom sheets?
