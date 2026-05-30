---
name: status-colors-and-errors
description: Keep status and error colours minimal and consistent — too many semantic colours confuse users. Each colour must mean exactly one thing. Errors should be recoverable, large failures must be prevented, and the UI should always give the user a path forward. Use when designing status indicators, error states, form validation, alerts, or any feedback system.
metadata:
  priority: 8
  pathPatterns:
    - "**/*.css"
    - "**/*.scss"
    - "**/tokens/**"
    - "**/theme/**"
    - "tailwind.config.*"
    - "design-system/**"
    - "components/**"
    - "**/*.tsx"
    - "**/*.jsx"
  promptSignals:
    phrases:
      - "error"
      - "warning"
      - "success"
      - "alert"
      - "status"
      - "validation"
      - "feedback"
      - "toast"
      - "notification"
retrieval:
  aliases:
    - error states
    - status colours
    - semantic colours
    - alerts
    - form validation
    - error recovery
    - feedback system
  intents:
    - design error states
    - set up semantic colours
    - handle errors gracefully
    - show validation feedback
    - communicate status to users
  examples:
    - what colours should I use for errors and warnings
    - how should I handle a failed API call
    - design the error state for this form
---

# Status Colours and Error Design

## Keep the Colour Set Small

Every status colour added to a system is a cognitive burden on the user. They must learn what each colour means, remember it, and interpret it correctly under stress — which is exactly when errors occur.

**The minimal set that covers almost everything:**

| Colour | Semantic meaning | Always means |
|---|---|---|
| **Red** | Error / failure / destructive | Something went wrong, or this action cannot be undone |
| **Orange / Amber** | Warning | Something needs attention before proceeding |
| **Green** | Success / positive | Action completed, state is healthy |
| **Blue** | Info / neutral status | Informational, no action required |

**Rule: each colour maps to exactly one meaning across the entire product.** If orange means "warning" in one component and "pending" in another, the system breaks down.

When in doubt, cut the colour — neutral grey communicates status without semantic weight, and neutral is better than a misused semantic colour.

## Orange Is Always a Warning

Orange (amber) carries a specific signal: pay attention, something may go wrong. Do not use it for:
- Neutral states (use grey)
- Progress or pending (use blue or a spinner)
- Informational content (use blue)
- Branding or decorative purposes inside status indicators

If orange appears in the UI, the user should immediately know it requires their attention.

## Errors Should Be Recoverable

**The worst error is one the user cannot recover from.** Design every error state with a path forward.

### Error message anatomy
Every error should answer three questions:
1. **What went wrong?** — plain language, no error codes
2. **Why did it happen?** — if useful and known
3. **What should the user do next?** — specific, actionable

```
❌ "Error 500"
❌ "Something went wrong"
✓  "We couldn't save your changes. Check your connection and try again."
✓  "This email is already in use. Sign in instead, or use a different email."
```

### Recovery actions
- Always provide a retry button for transient failures (network errors, timeouts)
- For validation errors, point directly to the problematic field
- For destructive actions that failed, reassure the user nothing was lost
- For session expiry, redirect to login and return the user to where they were

## Prevent Large Errors Before They Happen

The most damaging errors — data loss, irreversible actions, broken state — should be prevented at the design level, not handled after the fact.

- **Confirm before irreversible actions:** "Delete this project and all 47 tasks? This cannot be undone."
- **Disable unavailable actions** rather than letting users trigger them and hit an error
- **Autosave** where possible so a browser crash or accidental close does not destroy work
- **Optimistic UI** with rollback: show the success state immediately, silently retry on failure, surface an error only if the retry also fails

## Levels of Severity — Use Sparingly

Not every problem is equal. Match the visual weight of the feedback to the severity.

| Severity | Pattern | When to use |
|---|---|---|
| **Blocking error** | Full-page error state or modal | App cannot continue, user must act |
| **Inline error** | Red text below a field | Form field validation failure |
| **Toast / snackbar** | Temporary notification, bottom of screen | Transient failure the user should know about but can dismiss |
| **Alert banner** | Persistent bar at top of section | Ongoing issue affecting the current context |
| **Empty state** | Illustrated or descriptive empty screen | No data yet — use as an opportunity for guidance, not just a blank |

Avoid showing multiple simultaneous error types at once — one clear message is more useful than three overlapping alerts.

## Review Checklist

- [ ] Does the product use four or fewer semantic status colours?
- [ ] Does each colour mean exactly one thing, used consistently everywhere?
- [ ] Is orange/amber reserved exclusively for warnings?
- [ ] Does every error message state what went wrong and what to do next?
- [ ] Do all transient errors (network, timeout) have a retry action?
- [ ] Are irreversible destructive actions protected by a confirmation step?
- [ ] Is autosave or draft recovery available for long-form or complex inputs?
- [ ] Are multiple simultaneous error states avoided?

## Common Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| "Something went wrong" with no action | User is stuck with no path forward | Add specific cause and a retry or contact link |
| Orange used for "pending" and "warning" simultaneously | Colour loses its meaning | Orange = warning only; use blue or spinner for pending |
| Five or more status colours (red, orange, yellow, teal, purple…) | User must learn and remember a complex legend | Cut to the minimum: red, orange, green, blue |
| Inline validation only on submit | User discovers all errors at once | Validate on blur (leaving a field) for immediate feedback |
| No confirmation on delete | Users accidentally delete data | Require explicit confirmation for all irreversible actions |
