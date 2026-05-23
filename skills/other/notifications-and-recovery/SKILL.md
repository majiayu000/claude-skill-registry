---
name: notifications-and-recovery
description: When something goes wrong, the user must be able to recover or try again. Toasts, inline errors, banners, and notification patterns each have a specific role. Use when designing error states, success confirmations, async feedback, in-place editing, or any system that communicates state changes to the user.
metadata:
  priority: 8
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "toast"
      - "notification"
      - "error message"
      - "success message"
      - "in-place editing"
      - "inline error"
      - "alert"
      - "banner"
      - "recovery"
      - "retry"
retrieval:
  aliases:
    - toast notification
    - error recovery
    - inline error
    - notification pattern
    - in-place editing
    - alert banner
    - retry pattern
  intents:
    - show a success message
    - handle an error gracefully
    - design a toast notification
    - add retry to a failed action
    - design inline editing feedback
  examples:
    - show a toast when the form is saved
    - what happens when the API call fails
    - design the error state for this form
    - add a retry button when network fails
---

# Notifications and Recovery

When something changes — success, failure, or anything in between — the user must know. And when something goes wrong, they must always have a path forward. A notification without a recovery action is just an apology.

---

## Pattern Selection

| Pattern | When to use | Dismissal |
|---|---|---|
| **Toast** | Transient result of a user action (saved, sent, deleted) | Auto-dismiss 4–6s, manual close |
| **Inline error** | Field-level validation, form errors | Clears on correction |
| **Alert banner** | Persistent issue affecting the current context | Manual dismiss or resolved state |
| **Modal / dialog** | Blocking error requiring a decision before continuing | User action required |
| **Empty state** | No data yet — guide the user to the first action | N/A |
| **Skeleton / loading** | Async content pending | Replaced by content |
| **In-place confirmation** | Inline edit saved, row updated, item toggled | Auto-clears after 2–3s |

---

## Toast Notifications

Toasts confirm that a background action completed. They appear without interrupting the user's flow.

**Placement:** bottom-center or bottom-right. Never top-center — it competes with page content and navigation.

**Duration:** 4–6 seconds for information. Errors should persist until dismissed — the user needs time to read and act.

**Anatomy:**
```
[Icon] Message text                    [Action] [×]
```

- Icon: colour-coded (green ✓ success, red ✗ error, orange ⚠ warning, blue ℹ info)
- Message: one sentence, plain language
- Action (optional): "Undo", "Retry", "View" — one action maximum
- Close button: always present on errors; optional on success

```
✓ "Changes saved."
✓ "Message sent.  [Undo]"
✗ "Could not save. Check your connection.  [Retry]"  ← persists until dismissed
```

**Never:** multiple simultaneous toasts. Queue them; show one at a time.

---

## Inline Errors

Inline errors appear adjacent to the element that caused them. They are the most contextual and actionable form of error feedback.

**Form validation:**
- Validate on blur (leaving a field), not on every keystroke — keystroke validation is noisy
- Validate on submit for the complete form
- Show the error message directly below the field, in red, with an icon
- The field border changes to `--color-error`
- Error message is associated via `aria-describedby` for screen readers

```html
<label for="email">Email</label>
<input id="email" aria-describedby="email-error" aria-invalid="true">
<p id="email-error" role="alert">Enter a valid email address.</p>
```

**In-place editing:**
- When a field is edited inline (table cell, card title), show save/cancel controls adjacent to the field
- On save: brief success indicator ("✓ Saved") that fades after 2s — do not navigate away
- On error: inline error message below the field with a retry option
- On cancel: restore the original value immediately

---

## Alert Banners

Banners are persistent — they stay until the condition is resolved or the user dismisses them.

**Use for:**
- Service degradation ("Some features are temporarily unavailable")
- Account issues requiring action ("Your subscription expires in 3 days. [Renew]")
- Ongoing sync errors ("Changes are not saving. [Retry]")
- Important announcements tied to the current page

**Placement:** top of the affected section, not the entire page unless the issue is truly global.

**Anatomy:**
```
[Icon] [Message — describes the issue and its scope] [Action] [×]
```

- One banner at a time per region — multiple simultaneous banners create alarm fatigue
- Dismissible unless the condition is blocking
- Colour follows status colour conventions: red (error), orange (warning), blue (info), green (success/resolved)

---

## Recovery Patterns

Every error state must have a path forward. Design the recovery action at the same time as the error message.

### Retry
For transient failures (network, timeout, rate limit):

```
"Could not load results."
[Try again]
```

- Retry button triggers the same action
- After 3 failed retries, escalate: "Still having trouble? [Contact support]"
- Show a spinner during retry — do not let the user click multiple times

### Undo
For destructive or irreversible actions (delete, archive, send):

```
"Message sent.  [Undo]  ×"
```

- Undo window: 5–10 seconds. Toast persists for this duration.
- After the window closes, the action is final
- Undo is preferable to confirmation dialogs for low-stakes actions — it is faster and less disruptive

### Autosave and Draft Recovery
For long-form inputs (forms, documents, editors):

- Autosave every 30–60 seconds silently
- On save failure: "Autosave failed — your changes are stored locally. [Retry save]"
- On return after crash or close: "You have unsaved changes from [time]. [Restore] [Discard]"

### Graceful Degradation
When a feature fails but the rest of the product still works:

- Show an error state for the failed section only — do not blank the entire page
- Offer a fallback: "Could not load recommendations. [Browse all products →]"
- Log the error silently; surface only what the user needs to know

---

## Loading and Skeleton States

Loading is not an error, but it is a state that needs design.

- **Skeleton screens** for content-heavy pages — show the layout shape while data loads
- **Spinners** for targeted async actions (button loading, inline refresh)
- **Progress bars** for long operations with known duration (file upload, multi-step processing)
- Never show a blank screen while loading — always show something

Skeleton screens reduce perceived wait time compared to spinners. Match the skeleton shape to the actual content layout.

---

## Notification Accessibility

- Errors use `role="alert"` — announced immediately by screen readers
- Status updates use `role="status"` — announced politely (after current speech)
- Toasts must be reachable by keyboard — do not use `pointer-events: none` on the close button
- Auto-dismissing toasts must have sufficient duration (`prefers-reduced-motion` users may need more time to read)

```html
<!-- Error: immediate announcement -->
<div role="alert">Could not save. Check your connection.</div>

<!-- Status: polite announcement -->
<div role="status" aria-live="polite">Changes saved.</div>
```

---

## Review Checklist

- [ ] Does every error have a recovery action (retry, undo, contact support)?
- [ ] Do toasts auto-dismiss for success but persist for errors?
- [ ] Is there never more than one toast visible at a time?
- [ ] Are inline errors placed adjacent to the field, not at the top of the form?
- [ ] Are form errors associated to their inputs via `aria-describedby`?
- [ ] Do alert banners appear at the top of the affected section, not always full-page?
- [ ] Is autosave or draft recovery available for long-form inputs?
- [ ] Do loading states use skeletons for content and spinners for targeted actions?
- [ ] Are errors announced via `role="alert"` and status updates via `role="status"`?
