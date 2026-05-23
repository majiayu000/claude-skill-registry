---
name: form-system
description: Enforces project form system conventions when creating or modifying forms using the custom TanStack Form integration. This skill covers useAppForm hook usage, field components, focus management, validation patterns, and accessibility requirements.
---

# Form System Skill

## Purpose

This skill enforces the project form system conventions automatically during form development. It ensures consistent patterns for form hooks, field components, focus management, validation, server action integration, and accessibility.

## Activation

This skill activates when:

- Creating forms with `useAppForm` hook
- Using field components (`TextField`, `TextareaField`, `SelectField`, `SwitchField`, `CheckboxField`, `ComboboxField`, `TagField`)
- Implementing focus management with `withFocusManagement`
- Setting up form validation with Zod schemas
- Creating custom form dialogs or form-based features
- Using `form.AppField` for field rendering
- Using `form.SubmitButton` or `form.AppForm` wrappers
- Using `useStore` from `@tanstack/react-form` for form value access
- Using `formOptions` from `@tanstack/form-core` for reusable form configurations
- Implementing field listeners or programmatic field operations
- Integrating forms with `useServerAction` hook

## Workflow

1. Detect form work (imports from `@/components/ui/form` or `useAppForm`)
2. Load `references/Form-System-Conventions.md`
3. Generate/modify code following all conventions
4. Scan for violations of form patterns
5. Auto-fix all violations (no permission needed)
6. Report fixes applied

## Key Patterns

### Form Setup

- Use `useAppForm` hook from `@/components/ui/form`
- Wrap form components with `withFocusManagement` HOC
- Configure validation with `validators: { onSubmit: zodSchema }`
- Use `revalidateLogic` for validation timing
- Handle invalid submissions with `onSubmitInvalid` and `focusFirstError`
- Always set `canSubmitWhenInvalid: true`

### Field Rendering

- Use `form.AppField` with field components (`TextField`, etc.)
- Each field supports `label`, `description`, `isRequired`, `focusRef`, and `testId` props
- Use field `listeners` for side effects (onChange, onBlur)

### Form Submission

- Wrap `form.handleSubmit()` in event handler with `e.preventDefault()` and `e.stopPropagation()`
- Integrate with `useServerAction` hook for server actions
- Use `form.SubmitButton` wrapped in `form.AppForm` for automatic loading state

### Accessing Form Values

- Use `useStore` from `@tanstack/react-form` for reactive access
- Access via `useStore(form.store, (state) => state.values.fieldName)`
- Never access form values directly during render

### Programmatic Operations

- Use `form.setFieldValue()` to update field values
- Use `form.validateField()` to trigger validation
- Use field listeners for dependent field updates

### Server Action Options

- `toastMessages` for loading/success/error toasts
- `isDisableToast: true` for background operations
- `onSuccess` callback for post-submission logic

## References

- `references/Form-System-Conventions.md` - Complete form system conventions
