---
name: accessible-notifications
description: |
  Guidance for accessible user notifications and feedback. AUTO-TRIGGER when implementing: toasts, snackbars, notifications, alerts, flash messages, status messages, success/error feedback, or any transient UI messages. Triggers include: "toast", "snackbar", "notification", "flash message", "notify user", "show success", "show error", "feedback message", "status update", "auto-dismiss", "popup message". Use this skill BEFORE implementing any toast-like patterns to ensure accessibility compliance.
---

# Accessible Notifications

## Critical: Toasts Are Not Recommended

Toasts pose significant accessibility concerns and should be avoided. Use the alternatives below instead.

## Why Toasts Are Problematic

### WCAG Violations
- **2.2.1 Timing Adjustable (A)**: Auto-dismiss prevents users from reading content
- **1.3.2 Meaningful Sequence (A)**: DOM placement disconnects toast from trigger
- **2.1.1 Keyboard (A)**: Focus management is complex and often broken
- **4.1.3 Status Messages (AA)**: Assistive technology announcements are disruptive

### Usability Issues
- Large displays: Toasts appear outside user's field of view
- Screen magnification: Toast may be outside magnified area
- Multitasking: Auto-dismiss causes missed messages
- Blocking UI: Floats over important content like submit buttons

## What to Use Instead

### Successfully-Completed Simple Actions
**Do nothing extra.** Success should be self-evident.

```vue
<!-- User creates issue → Issue appears in list -->
<!-- No toast needed - the result IS the feedback -->
```

### Successfully-Completed Complex Actions
Use **persistent banners** or **progressive content display**:

```vue
<Banner v-if="bulkResult" variant="success">
  Created {{ bulkResult.count }} issues successfully.
  <RouterLink :to="{ name: 'issues' }">View all</RouterLink>
</Banner>
```

### Unsuccessful Actions (Errors)
Use **inline validation** or **banners**:

```vue
<!-- Inline validation for forms -->
<FormField :error="errors.email">
  <Input v-model="email" />
</FormField>

<!-- Banner for system errors -->
<Banner v-if="submitError" variant="destructive">
  {{ submitError.message }}
</Banner>
```

### Form Submission Success
Use **interstitial confirmation** or **redirect with banner**:

```vue
<!-- Option 1: Confirmation page -->
<ConfirmationPage v-if="submitted">
  Your request has been submitted. Reference: #{{ referenceId }}
</ConfirmationPage>

<!-- Option 2: Redirect to result -->
// router.push({ name: 'item-detail', params: { id: newItem.id } })
```

### Long-Running Tasks
Use **persistent banners** + **other channels** (email, push notifications):

```vue
<Banner v-if="taskComplete" variant="success">
  Export complete. <a :href="downloadUrl">Download file</a>
</Banner>
```

## Assistive Technology Announcements

### When to Announce
- **Always**: Location changes, navigation
- **Always**: Failed user actions (validation, errors)
- **Sometimes**: Essential streaming content (logs)
- **Avoid**: Non-essential updates (presence indicators, comments by others)

### Implementation
Use `aria-live` regions for dynamic content that must be announced:

```vue
<div aria-live="polite" aria-atomic="true" class="sr-only">
  {{ statusMessage }}
</div>
```

## Quick Decision Guide

| Scenario | Solution |
|----------|----------|
| Simple action succeeded | No feedback needed |
| Complex action succeeded | Persistent banner |
| Action failed | Inline error or banner |
| Form submitted | Confirmation page or redirect |
| Long task complete | Banner + email/push |
| Need user attention | Dialog (interruptive) |
