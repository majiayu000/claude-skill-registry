---
name: web-forms-vee-validate
description: VeeValidate v4 patterns - useForm, useField, defineField, useFieldArray, schema validation with Composition API
---

# VeeValidate Form Validation Patterns

> **Quick Guide:** Use VeeValidate v4 for Vue 3 form validation with Composition API. Use `useForm` for form state, `defineField` for quick field setup, `useField` for custom input components, and `useFieldArray` for dynamic lists. Always wrap schema libraries with `toTypedSchema()`. Always use `field.key` (not index) as iteration key in field arrays.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `toTypedSchema()` wrapper when using schema libraries in v4 - raw schemas won't work)**

**(You MUST use `field.key` as iteration key in useFieldArray - NEVER use array index)**

**(You MUST use function form `() => props.name` or `toRef()` in useField for prop reactivity)**

**(You MUST initialize field array values in `initialValues` - undefined arrays cause errors)**

</critical_requirements>

---

**Auto-detection:** VeeValidate, vee-validate, useForm, useField, defineField, useFieldArray, toTypedSchema, ErrorMessage, Form component

**When to use:**

- Building Vue 3 forms with validation requirements
- Managing complex form state with multiple fields
- Creating dynamic forms with add/remove field capabilities
- Integrating schema validation libraries with `toTypedSchema()`
- Building multi-step wizard forms

**When NOT to use:**

- Single input without validation (use native v-model)
- Server-only forms with server actions (use native form submission)
- Read-only data display (not a form scenario)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - defineField, useField, form meta, eager validation
- [examples/validation.md](examples/validation.md) - Zod/Yup/Valibot schema integration, conditional validation
- [examples/arrays.md](examples/arrays.md) - useFieldArray, nested arrays, reordering
- [reference.md](reference.md) - Decision frameworks, API reference tables, anti-patterns

---

<philosophy>

## Philosophy

VeeValidate v4 embraces Vue 3's Composition API as the primary approach, enabling seamless integration with any UI library. Validation logic is decoupled from presentation, allowing schema-first validation with full TypeScript inference.

**Core Principles:**

1. **Composition API first** - Use `useForm`, `useField`, `defineField` for seamless Vue 3 integration
2. **Schema-first validation** - Prefer declarative schemas over inline rules
3. **Full type safety** - TypeScript inference from schemas and generics
4. **UI agnostic** - Works with any component library or native inputs
5. **Minimal re-renders** - Efficient reactivity through Vue's reactive system

**defineField vs useField:**

| Feature          | `defineField`                       | `useField`                                |
| ---------------- | ----------------------------------- | ----------------------------------------- |
| **Use case**     | Quick form setup with native inputs | Building reusable custom input components |
| **Form context** | Always requires form context        | Optional form integration                 |
| **Best for**     | Application-level forms             | Component library development             |

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Form with defineField

Use `useForm` with `defineField` for the fastest form setup. `defineField` returns a `[model, attrs]` tuple for v-model binding. See [examples/core.md](examples/core.md) for full examples.

```vue
<script setup lang="ts">
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import { z } from "zod";

const schema = toTypedSchema(
  z.object({
    email: z.string().email("Invalid email"),
    password: z.string().min(8, "At least 8 characters"),
  }),
);

const { handleSubmit, errors, defineField } = useForm({
  validationSchema: schema,
});

const [email, emailAttrs] = defineField("email");

const onSubmit = handleSubmit((values) => {
  // values is fully typed from schema
});
</script>
```

---

### Pattern 2: Custom Input Components with useField

Use `useField` when building reusable input components. **Critical:** use function form `() => props.name` to maintain reactivity. See [examples/core.md](examples/core.md) for full component example.

```vue
<script setup lang="ts">
import { useField } from "vee-validate";

const props = defineProps<{ name: string }>();

// CRITICAL: Function form maintains reactivity
const { value, errorMessage, handleBlur, meta } = useField<string>(
  () => props.name,
  undefined,
  { validateOnValueUpdate: false },
);
</script>
```

---

### Pattern 3: Schema Validation with toTypedSchema

Always wrap schema libraries with `toTypedSchema()`. Initialize ALL fields used in `refine/superRefine` - Zod skips refinements when keys are undefined. See [examples/validation.md](examples/validation.md) for Zod, Yup, and Valibot examples.

```typescript
import { toTypedSchema } from "@vee-validate/zod";

// CORRECT: Wrapped schema
const schema = toTypedSchema(z.object({ email: z.string().email() }));

// WRONG: Raw schema won't work with VeeValidate
const schema = z.object({ email: z.string().email() });
```

---

### Pattern 4: Dynamic Arrays with useFieldArray

Use `useFieldArray` for add/remove/reorder patterns. **Always** use `field.key` as `:key`, never array index. Initialize arrays in `initialValues`. See [examples/arrays.md](examples/arrays.md) for full patterns.

```vue
<script setup lang="ts">
import { useForm, useFieldArray } from "vee-validate";

const { handleSubmit } = useForm({
  initialValues: { users: [{ name: "", email: "" }] },
});

const { fields, push, remove } = useFieldArray("users");
</script>

<template>
  <!-- CORRECT: field.key as key -->
  <div v-for="(field, index) in fields" :key="field.key">
    <input v-model="field.value.name" />
  </div>
</template>
```

---

### Pattern 5: Server-Side Error Handling

Set errors from API responses using `setErrors` (multiple) or `setFieldError` (single).

```typescript
const { handleSubmit, setErrors, setFieldError } = useForm({ ... });

const onSubmit = handleSubmit(async (values) => {
  try {
    await api.createUser(values);
  } catch (error) {
    if (error.response?.data?.errors) {
      // Set multiple field errors from API
      setErrors(mapApiErrors(error.response.data.errors));
    } else {
      setFieldError("apiError", "Something went wrong");
    }
  }
});
```

---

### Pattern 6: Form Meta and State

Access aggregated form state for UX features like dirty tracking, submit button state, and reset. See [examples/core.md](examples/core.md) for full example.

```vue
<script setup lang="ts">
const { handleSubmit, meta, isSubmitting, resetForm } = useForm({ ... });
</script>

<template>
  <button :disabled="!meta.valid || !meta.dirty || isSubmitting">
    {{ isSubmitting ? "Saving..." : "Save" }}
  </button>
  <p v-if="meta.dirty">You have unsaved changes</p>
</template>
```

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `toTypedSchema()` wrapper - raw schemas silently fail to validate
- Using array index as `:key` in `useFieldArray` - causes form state corruption on add/remove
- Direct `props.name` in `useField` - loses reactivity when prop changes
- Undefined `initialValues` for field arrays - causes runtime errors

**Medium Priority Issues:**

- `validateOnValueUpdate` enabled everywhere - validates on every keystroke (noisy UX)
- Not handling async validation errors - API failures need `setErrors()` or `setFieldError()`
- Forgetting `resetForm()` after submission - form stays dirty after success
- Multiple `useForm` calls in same component - creates conflicting form contexts
- Not using `meta.touched` for error display - shows errors before user interaction

**Gotchas & Edge Cases:**

- `errors` has first error per field; `errorBag` has ALL errors per field as arrays
- `meta.valid` may be false during initial render before validation runs
- Nested fields use dot notation: `defineField('user.profile.name')`
- Array field errors use bracket notation: `errors['items[0].name']`
- `resetForm({ values: data })` not `resetForm(data)` - wrong structure silently fails
- `keepValuesOnUnmount: false` (default) drops values of unmounted fields - set `true` for multi-step forms
- Mixing `<Form>` component with `useForm()` creates conflicting contexts - pick one approach
- Zod `refine/superRefine` do NOT execute when object keys are missing - always initialize all fields

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `toTypedSchema()` wrapper when using schema libraries in v4 - raw schemas won't work)**

**(You MUST use `field.key` as iteration key in useFieldArray - NEVER use array index)**

**(You MUST use function form `() => props.name` or `toRef()` in useField for prop reactivity)**

**(You MUST initialize field array values in `initialValues` - undefined arrays cause errors)**

**Failure to follow these rules will break form validation, cause reactivity issues, and corrupt form state.**

</critical_reminders>
