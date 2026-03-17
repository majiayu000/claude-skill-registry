---
name: web-forms-vee-validate
description: VeeValidate v4 patterns - useForm, useField, defineField, useFieldArray, schema validation with Composition API
---

# VeeValidate Form Validation Patterns

> **Quick Guide:** Use VeeValidate v4 for Vue 3 form validation with Composition API. Use `useForm` for form state, `defineField` for quick field setup, `useField` for custom input components, and `useFieldArray` for dynamic lists.

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
- Integrating schema validation libraries (Zod, Yup, Valibot)
- Building multi-step wizard forms

**Key patterns covered:**

- useForm hook with TypeScript generics
- defineField for quick native input binding
- useField for custom input components
- useFieldArray for dynamic field lists
- Schema validation with toTypedSchema
- Error handling and display
- Form meta state tracking

**When NOT to use:**

- Single input without validation (use native v-model)
- Server-only forms with server actions (use native form submission)
- Read-only data display (not a form scenario)

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [core.md](examples/core.md) - Basic form patterns
  - [validation.md](examples/validation.md) - Schema validation integration
  - [arrays.md](examples/arrays.md) - useFieldArray for dynamic forms
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

VeeValidate v4 embraces Vue 3's Composition API as the primary approach, enabling seamless integration with any UI library. Validation logic is decoupled from presentation, allowing schema-first validation with full TypeScript inference.

**Core Principles:**

1. **Composition API first** - Use `useForm`, `useField`, `defineField` for seamless Vue 3 integration
2. **Schema-first validation** - Prefer declarative schemas (Zod/Yup) over inline rules
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

Use `useForm` with `defineField` for the fastest form setup with native inputs.

```vue
<script setup lang="ts">
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import { z } from "zod";

const MIN_PASSWORD_LENGTH = 8;

// Define schema with type inference
const schema = toTypedSchema(
  z.object({
    email: z.string().min(1, "Email is required").email("Invalid email"),
    password: z
      .string()
      .min(MIN_PASSWORD_LENGTH, `At least ${MIN_PASSWORD_LENGTH} characters`),
  }),
);

// Initialize form with typed schema
const { handleSubmit, errors, defineField } = useForm({
  validationSchema: schema,
});

// defineField returns [model, attrs] tuple
const [email, emailAttrs] = defineField("email");
const [password, passwordAttrs] = defineField("password");

// Type-safe submit handler
const onSubmit = handleSubmit((values) => {
  // values is fully typed: { email: string; password: string }
  console.log("Submitting:", values);
});
</script>

<template>
  <form @submit="onSubmit">
    <div>
      <label for="email">Email</label>
      <input id="email" v-model="email" v-bind="emailAttrs" type="email" />
      <span v-if="errors.email" role="alert">{{ errors.email }}</span>
    </div>

    <div>
      <label for="password">Password</label>
      <input
        id="password"
        v-model="password"
        v-bind="passwordAttrs"
        type="password"
      />
      <span v-if="errors.password" role="alert">{{ errors.password }}</span>
    </div>

    <button type="submit">Submit</button>
  </form>
</template>
```

**Why good:** toTypedSchema enables full type inference from Zod schema, defineField returns reactive model and attributes for v-model binding, errors object provides field-level error messages, named constant for MIN_PASSWORD_LENGTH

---

### Pattern 2: Typed Forms with Generics

For explicit type control without schema libraries.

```vue
<script setup lang="ts">
import { useForm } from "vee-validate";

interface LoginForm {
  email: string;
  password: string;
  rememberMe: boolean;
}

const { handleSubmit, errors, defineField } = useForm<LoginForm>({
  initialValues: {
    email: "",
    password: "",
    rememberMe: false,
  },
});

// Fields are typed based on LoginForm interface
const [email, emailAttrs] = defineField("email");
const [password, passwordAttrs] = defineField("password");
const [rememberMe, rememberMeAttrs] = defineField("rememberMe");

const onSubmit = handleSubmit(async (values) => {
  // values: LoginForm
  await loginUser(values);
});
</script>
```

**Why good:** TypeScript generics provide autocomplete and type checking for field names, initialValues establishes default state, explicit interface documents form shape

---

### Pattern 3: Custom Input Components with useField

Use `useField` when building reusable input components.

```vue
<!-- components/text-input.vue -->
<script setup lang="ts">
import { useField } from "vee-validate";

interface Props {
  name: string;
  label: string;
  type?: string;
  placeholder?: string;
}

const props = withDefaults(defineProps<Props>(), {
  type: "text",
  placeholder: "",
});

// CRITICAL: Use function form to maintain reactivity
const { value, errorMessage, handleBlur, handleChange, meta } =
  useField<string>(
    () => props.name, // Function form maintains reactivity
    undefined,
    {
      validateOnValueUpdate: false, // Lazy validation
    },
  );
</script>

<template>
  <div class="form-field">
    <label :for="name">{{ label }}</label>
    <input
      :id="name"
      :name="name"
      :type="type"
      :value="value"
      :placeholder="placeholder"
      :class="{ 'has-error': meta.touched && errorMessage }"
      :aria-invalid="meta.touched && !!errorMessage"
      @input="handleChange"
      @blur="handleBlur"
    />
    <span v-if="meta.touched && errorMessage" role="alert">
      {{ errorMessage }}
    </span>
  </div>
</template>
```

**Why good:** Function form `() => props.name` maintains reactivity when prop changes, validateOnValueUpdate: false enables lazy validation, meta.touched shows errors only after interaction, aria-invalid improves accessibility

---

### Pattern 4: Form Meta and State

Access aggregated form state for UX features.

```vue
<script setup lang="ts">
import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import { z } from "zod";

const schema = toTypedSchema(
  z.object({
    email: z.string().email(),
  }),
);

const { handleSubmit, meta, isSubmitting, resetForm, defineField } = useForm({
  validationSchema: schema,
  initialValues: {
    email: "",
  },
});

const [email, emailAttrs] = defineField("email");

const onSubmit = handleSubmit(async (values) => {
  await submitForm(values);
});
</script>

<template>
  <form @submit="onSubmit">
    <input v-model="email" v-bind="emailAttrs" type="email" />

    <button type="submit" :disabled="!meta.valid || isSubmitting">
      {{ isSubmitting ? "Submitting..." : "Submit" }}
    </button>

    <button type="button" @click="resetForm()">Reset</button>

    <p v-if="meta.dirty">You have unsaved changes</p>
  </form>
</template>
```

**Why good:** meta.valid enables submit button state, meta.dirty tracks unsaved changes, isSubmitting provides loading state, resetForm clears form to initialValues

---

### Pattern 5: Lazy Validation Control

Control when validation triggers per field.

```vue
<script setup lang="ts">
import { useForm } from "vee-validate";

const { defineField } = useForm({
  initialValues: { email: "", username: "" },
});

// Aggressive validation (default) - validates on every change
const [email, emailAttrs] = defineField("email");

// Lazy validation - validates on blur only
const [username, usernameAttrs] = defineField("username", {
  validateOnModelUpdate: false, // Don't validate on input
});
</script>
```

**Why good:** validateOnModelUpdate: false reduces validation noise during typing, per-field control enables different UX patterns

---

### Pattern 6: Server-Side Error Handling

Set errors from API responses.

```vue
<script setup lang="ts">
import { useForm } from "vee-validate";

interface ApiError {
  field: string;
  message: string;
}

const { handleSubmit, setErrors, setFieldError, errors, defineField } = useForm(
  {
    initialValues: { email: "", username: "" },
  },
);

const [email] = defineField("email");
const [username] = defineField("username");

const onSubmit = handleSubmit(async (values) => {
  try {
    await api.createUser(values);
  } catch (error) {
    if (error.response?.data?.errors) {
      // Set multiple field errors from API
      const apiErrors = error.response.data.errors as ApiError[];
      const errorMap = apiErrors.reduce(
        (acc, err) => {
          acc[err.field] = err.message;
          return acc;
        },
        {} as Record<string, string>,
      );
      setErrors(errorMap);
    } else {
      // Set single field error
      setFieldError("apiError", "Something went wrong");
    }
  }
});
</script>

<template>
  <form @submit="onSubmit">
    <input v-model="email" type="email" />
    <span v-if="errors.email">{{ errors.email }}</span>

    <input v-model="username" />
    <span v-if="errors.username">{{ errors.username }}</span>

    <span v-if="errors.apiError">{{ errors.apiError }}</span>

    <button type="submit">Register</button>
  </form>
</template>
```

**Why good:** setErrors handles multiple API validation errors at once, setFieldError sets individual field errors, error state integrates seamlessly with form display

</patterns>

---

<decision_framework>

## Decision Framework

### When to Use defineField vs useField

```
Are you building the form directly in your component?
├─ YES → Are you using native HTML inputs?
│   ├─ YES → Use defineField ✓
│   └─ NO → Does your component accept v-model?
│       ├─ YES → Use defineField with v-model ✓
│       └─ NO → Use useField with manual binding
└─ NO → Are you building a reusable input component?
    ├─ YES → Use useField ✓
    └─ NO → Use defineField for application forms
```

### Validation Mode Selection

```
What validation UX do you need?
├─ Validate after first error then aggressively → default behavior ✓
├─ Validate only on blur → defineField with validateOnModelUpdate: false
├─ Validate only on submit → useForm with validateOnMount: false
└─ Eager validation (lazy first, aggressive after error) → custom listeners
```

### Schema Library Selection

```
Which schema library should you use?
├─ Need smallest bundle size? → Valibot
├─ Already using Zod elsewhere? → Zod ✓ (recommended)
├─ Legacy codebase with Yup? → Yup
└─ Functional validation style? → Valibot
```

</decision_framework>

---

<integration>

## Integration Guide

**Styling Integration:**
Components accept class bindings for styling flexibility.
Use `:class="{ 'has-error': errorMessage }"` for error states.
Validation state is exposed via `meta` object.

**State Integration:**
Form values are managed internally by VeeValidate.
Use `values` from useForm for reading current state.
Server state synchronization handled via `resetForm(newValues)`.

**Testing Integration:**
Forms can be tested by triggering input events and submit.
Mock validation schemas for isolated component tests.
Use `flushPromises()` for async validation timing.

</integration>

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
