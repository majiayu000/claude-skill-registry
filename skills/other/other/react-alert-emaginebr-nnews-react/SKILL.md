---
name: react-alert
description: Display user-facing alerts, notifications, and feedback messages using toast notifications from the sonner library. Use this skill whenever the user asks to show an alert, notification, success message, error message, warning, or any kind of user feedback popup.
---

This skill defines the standard approach for displaying alerts, notifications, and user feedback in this project. All alerts MUST use toast notifications from the `sonner` library — never native browser alerts.

## Setup

The `sonner` package is already installed in this project. The `<Toaster>` provider is already mounted in `src/App.tsx`:

```tsx
import { Toaster } from 'sonner';

// Inside the App component JSX:
<Toaster position="bottom-right" richColors />
```

No additional setup is needed. Just import `toast` from `sonner` and call it.

## Rules

1. **Always use `toast` from `sonner`** for any user-facing alert, notification, or feedback message.
2. **Never use `window.alert()`** — use `toast()` or `toast.error()` instead.
3. **Never use `window.confirm()`** — use the Modal component (see `react-modal` skill) for confirmation dialogs, with toast for the resulting success/error feedback.
4. **Never use `window.prompt()`** — use the Modal component with a form input instead.
5. **Never use `console.log()` as a substitute for user feedback** — if the user should see it, use a toast.
6. **Never create custom alert/notification components** (banners, snackbars, inline alerts) for transient feedback. The toast system already handles this with consistent styling and auto-dismiss behavior.

## Toast Types

Use the appropriate toast variant to match the nature of the message:

```tsx
import { toast } from 'sonner';

// Success — operation completed successfully
toast.success('Profile updated successfully!');

// Error — something went wrong
toast.error('Failed to save changes. Please try again.');

// Warning — caution or important notice
toast.warning('Your session will expire in 5 minutes.');

// Info — neutral informational message
toast.info('New updates are available.');

// Default — generic notification (no icon/color)
toast('Something happened.');

// Loading — for async operations with follow-up
toast.loading('Saving changes...');
```

## Usage Patterns

### Basic feedback after an action

```tsx
import { toast } from 'sonner';

const handleSave = async () => {
  try {
    await saveData();
    toast.success('Changes saved successfully!');
  } catch (error) {
    toast.error(error.message || 'Failed to save changes.');
  }
};
```

### Promise-based toast (loading → success/error)

For async operations where you want to show a loading state that resolves:

```tsx
import { toast } from 'sonner';

const handleDelete = () => {
  toast.promise(deleteItem(id), {
    loading: 'Deleting item...',
    success: 'Item deleted successfully!',
    error: 'Failed to delete item.',
  });
};
```

### Toast with action button

When the user might want to undo or take a follow-up action:

```tsx
import { toast } from 'sonner';

toast('Item archived.', {
  action: {
    label: 'Undo',
    onClick: () => restoreItem(id),
  },
});
```

### Toast with custom duration

Default auto-dismiss is usually fine, but you can customize:

```tsx
import { toast } from 'sonner';

// Stay longer for important messages (duration in ms)
toast.warning('Unsaved changes will be lost.', { duration: 8000 });

// Persistent toast that requires manual dismiss
toast.error('Connection lost. Check your internet.', { duration: Infinity });
```

### Toast with description

For messages that need additional context:

```tsx
import { toast } from 'sonner';

toast.success('User invited', {
  description: 'An invitation email has been sent to john@example.com.',
});
```

## Message Guidelines

- Keep toast messages **short and clear** (one sentence).
- Use **past tense** for completed actions: "Profile updated successfully!" not "Profile has been updated."
- Use **imperative or present tense** for errors and instructions: "Failed to save. Please try again."
- Don't include technical details in user-facing messages — log those to `console.error()` separately.
- Always provide a fallback message when the error object might not have a `.message`:
  ```tsx
  toast.error(error.message || 'An unexpected error occurred.');
  ```

## Existing Conventions

This project already uses `toast` from `sonner` in several pages. Follow the same pattern:

- **Success on completed action:** `toast.success('Login successful! Welcome back.')`
- **Error with message fallback:** `toast.error(error.message || 'Login failed. Please try again.')`
- **Callbacks from `nauth-react` components:** Pass `onSuccess` / `onError` handlers that call `toast.success()` / `toast.error()`.
