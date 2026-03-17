---
name: react-modal-patterns
description: Modal and form patterns for Orient dashboard frontend. Use when creating modals, dialogs, forms, notifications, or any UI components in packages/dashboard-frontend. The dashboard uses plain HTML/CSS with Tailwind - NOT shadcn/ui, Radix, or other component libraries. Reference this skill before creating any modal, form, or notification component.
---

# React Modal Patterns for Orient Dashboard

The dashboard-frontend uses plain HTML/CSS with Tailwind CSS. Do NOT use shadcn/ui, Radix UI, sonner, or other component libraries.

## Available Dependencies

```json
{
  "lucide-react": "icons",
  "react": "core",
  "react-dom": "core",
  "react-markdown": "markdown rendering",
  "react-router-dom": "routing",
  "tailwindcss": "styling"
}
```

## Modal Structure

```tsx
// Fixed overlay with centered content
<div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
  <div className="bg-white dark:bg-gray-800 rounded-lg shadow-2xl w-full max-w-[500px] max-h-[90vh] flex flex-col">
    {/* Header */}
    <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Title</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Description</p>
      </div>
      <button onClick={onClose} className="text-gray-400 hover:text-gray-500">
        <X className="h-6 w-6" />
      </button>
    </div>

    {/* Content - scrollable */}
    <div className="flex-1 overflow-y-auto p-6">{/* Form or content here */}</div>

    {/* Footer */}
    <div className="flex items-center justify-end gap-3 p-6 border-t border-gray-200 dark:border-gray-700">
      <button className="btn btn-secondary">Cancel</button>
      <button className="btn btn-primary">Submit</button>
    </div>
  </div>
</div>
```

## Button Classes

```tsx
// Primary action
<button className="btn btn-primary">Save</button>

// Secondary action
<button className="btn btn-secondary">Cancel</button>

// Ghost/minimal button
<button className="btn btn-ghost">Back</button>

// With loading state
<button className="btn btn-primary flex items-center gap-2" disabled={loading}>
  {loading && <Loader2 className="h-4 w-4 animate-spin" />}
  {loading ? 'Saving...' : 'Save'}
</button>
```

## Form Inputs

```tsx
// Text input - use className="input"
<input type="text" className="input" placeholder="Enter value" />

// With label
<div className="space-y-2">
  <label className="block text-sm font-medium text-gray-900 dark:text-white">
    Field Name
  </label>
  <input type="text" className="input w-full" />
  <p className="text-xs text-gray-500 dark:text-gray-400">Help text</p>
</div>

// Password with toggle
<div className="relative">
  <input
    type={showPassword ? 'text' : 'password'}
    className="input w-full pr-10"
  />
  <button
    type="button"
    onClick={() => setShowPassword(!showPassword)}
    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
  >
    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
  </button>
</div>

// Select dropdown
<select className="input w-full">
  <option value="">Select...</option>
</select>

// Textarea
<textarea className="input w-full h-auto resize-none" rows={4} />
```

## Error Display

```tsx
// Inline error (in forms)
{
  error && (
    <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
    </div>
  );
}

// Card-level error
<div className="bg-destructive/10 border border-destructive/20 rounded-lg p-4 text-destructive">
  {error}
</div>;
```

## Notifications (Toast Replacement)

Do NOT use `sonner` or `toast()`. Use state-based notifications:

```tsx
interface Notification {
  type: 'success' | 'error' | 'info';
  message: string;
}

function NotificationBanner({
  notification,
  onDismiss,
}: {
  notification: Notification;
  onDismiss: () => void;
}) {
  useEffect(() => {
    const timer = setTimeout(onDismiss, 5000);
    return () => clearTimeout(timer);
  }, [onDismiss]);

  const colors = {
    success:
      'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-800 dark:text-emerald-200 border-emerald-200',
    error: 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-200 border-red-200',
    info: 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 border-blue-200',
  };

  return (
    <div
      className={`fixed top-4 right-4 z-50 max-w-md rounded-lg border p-4 shadow-lg ${colors[notification.type]}`}
    >
      <div className="flex items-center justify-between gap-4">
        <p className="text-sm font-medium">{notification.message}</p>
        <button onClick={onDismiss} className="text-current opacity-70 hover:opacity-100">
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

// Usage in component
const [notification, setNotification] = useState<Notification | null>(null);

const showNotification = (type: Notification['type'], message: string) => {
  setNotification({ type, message });
};

// In JSX
{
  notification && (
    <NotificationBanner notification={notification} onDismiss={() => setNotification(null)} />
  );
}
```

## Tabs (Auth Method Selector)

```tsx
// Tab container
<div className="flex rounded-lg bg-gray-100 dark:bg-gray-700 p-1">
  {options.map((option) => (
    <button
      key={option.value}
      type="button"
      onClick={() => setSelected(option.value)}
      className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
        selected === option.value
          ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow'
          : 'text-gray-600 dark:text-gray-400 hover:text-gray-900'
      }`}
    >
      {option.icon}
      {option.label}
    </button>
  ))}
</div>
```

## Loading Spinner

```tsx
// Inline spinner
<svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
  <circle
    className="opacity-25"
    cx="12"
    cy="12"
    r="10"
    stroke="currentColor"
    strokeWidth="4"
    fill="none"
  />
  <path
    className="opacity-75"
    fill="currentColor"
    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
  />
</svg>;

// Or use lucide-react
import { Loader2 } from 'lucide-react';
<Loader2 className="h-4 w-4 animate-spin" />;
```

## Icons

Always use lucide-react for icons:

```tsx
import { X, Eye, EyeOff, Loader2, Check, AlertCircle } from 'lucide-react';
```

## Form Validation Patterns

### Required Fields Tracking

Track form completion state using derived values:

```tsx
// Track whether all required fields are filled
const isFormComplete = useMemo(() => {
  return requiredFields.every((field) => {
    const value = formValues[field.name];
    return value && value.trim().length > 0;
  });
}, [formValues, requiredFields]);
```

### Disabled Submit Button

Disable submit when form is incomplete or submitting:

```tsx
<button
  type="submit"
  disabled={!isFormComplete || isSubmitting}
  className="btn btn-primary flex items-center gap-2"
>
  {isSubmitting && <Loader2 className="h-4 w-4 animate-spin" />}
  {isSubmitting ? 'Saving...' : 'Save & Connect'}
</button>
```

### Field-Level Error Display

Show errors inline below inputs:

```tsx
<div className="space-y-2">
  <label className="block text-sm font-medium text-gray-900 dark:text-white">
    Email <span className="text-red-500">*</span>
  </label>
  <input
    type="email"
    className={`input w-full ${errors.email ? 'border-red-500' : ''}`}
    value={email}
    onChange={(e) => setEmail(e.target.value)}
  />
  {errors.email && <p className="text-xs text-red-500">{errors.email}</p>}
</div>
```

### Password Field Visibility Toggle

Pattern for toggling password visibility with state per field:

```tsx
const [showPasswords, setShowPasswords] = useState<Record<string, boolean>>({});

const togglePasswordVisibility = (fieldName: string) => {
  setShowPasswords((prev) => ({ ...prev, [fieldName]: !prev[fieldName] }));
};

// In render
<div className="relative">
  <input
    type={showPasswords[field.name] ? 'text' : 'password'}
    className="input w-full pr-10"
    value={formValues[field.name] || ''}
    onChange={(e) => handleChange(field.name, e.target.value)}
  />
  <button
    type="button"
    onClick={() => togglePasswordVisibility(field.name)}
    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
  >
    {showPasswords[field.name] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
  </button>
</div>;
```

### Auto-Dismiss Notifications

Notifications auto-dismiss after 5 seconds with cleanup on unmount:

```tsx
function NotificationBanner({
  notification,
  onDismiss,
}: {
  notification: Notification;
  onDismiss: () => void;
}) {
  useEffect(() => {
    const timer = setTimeout(onDismiss, 5000); // Auto-dismiss after 5s
    return () => clearTimeout(timer); // Cleanup on unmount
  }, [onDismiss]);

  // ... render
}

// Usage with optional callbacks
const handleSave = async () => {
  try {
    await saveData();
    onSuccess?.('Changes saved successfully'); // Optional callback
    setNotification({ type: 'success', message: 'Saved!' });
    onOpenChange(false); // Close modal
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Save failed';
    onError?.(message); // Optional callback
    setError(message); // Show inline error
  }
};
```

## Reference Components

See these files for complete examples:

- `packages/dashboard-frontend/src/components/MiniAppEditor/MiniAppEditorModal.tsx` - Full modal with form
- `packages/dashboard-frontend/src/components/ScheduleForm.tsx` - Complex form with validation
- `packages/dashboard-frontend/src/components/IntegrationCredentialModal.tsx` - Modal with tabs, password fields, and form validation
