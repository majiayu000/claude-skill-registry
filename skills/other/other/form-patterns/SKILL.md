---
name: form-patterns
description: "Use when building forms in React or Next.js. Covers React Hook Form with Zod validation, multi-step wizards, server actions, file uploads, and accessible form UX."
---

# Form Patterns

## Stack Decision

| Need | Use |
|------|-----|
| Client-side React forms | React Hook Form + Zod |
| Next.js server mutations | Server Actions + useActionState |
| Simple 1-2 field forms | Uncontrolled + native validation |
| Complex multi-step | React Hook Form + state machine |

## React Hook Form + Zod

Use `zodResolver(schema)` with `useForm`. Register inputs with `{...register('field')}`. Display `errors.field.message` with `role='alert'` and `aria-describedby`.

## Multi-Step Wizard

Track current step in state. Merge step data on each submit. Each step is its own RHF instance with `defaultValues` from accumulated data.

## Server Actions (Next.js)

Mark action files `'use server'`. Parse FormData with Zod's `safeParse`. Return `{ errors }` on failure. Client uses `useActionState(action, initialState)` returning `[state, formAction, isPending]`.

## File Upload

Use `useRef` for hidden file input. Handle drag-and-drop via `onDrop`/`onDragOver`. Transfer dropped files to input via `new DataTransfer()` + `dt.items.add(file)` for form submission.

## Validation UX

Use `mode: 'onBlur'` for inline validation. Debounce async validators (username availability). Prefer inline-on-blur for most fields, on-submit for short forms.

## Accessibility Checklist

- Every `<input>` has a `<label>` with matching `htmlFor`/`id`
- Error messages use `role="alert"` and link via `aria-describedby`
- Required fields use `aria-required="true"` (not just `required` attribute)
- Focus the first error field on submit failure
- Disabled submit buttons still explain why (tooltip or adjacent text)

## Gotchas

- **Controlled vs uncontrolled**: React Hook Form is uncontrolled by default; `Controller` wraps controlled components (Select, DatePicker). Don't mix `register` with `value` prop
- **FormData with checkboxes**: unchecked checkboxes are absent from FormData, not `false` -- parse with `formData.get('field') === 'on'`
- **File input reset**: setting `input.value = ''` is the only way to clear; React state won't do it
- **Server Action errors**: `useActionState` replaces `useFormState` in React 19; always return structured error objects, not thrown errors
- **Zod `.transform()`**: transforms run after validation; `z.coerce.number()` for FormData string-to-number

## Cross-References

- **frontend:react-state-management** -- managing form state alongside global state
- **frontend:nextjs-app-router-patterns** -- server actions, revalidation, and progressive enhancement
- **languages:pydantic-and-data-validation** -- server-side schema validation mirroring Zod patterns
