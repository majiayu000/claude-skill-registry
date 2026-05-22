---
name: formik
description: "Building and managing forms in React with Formik. Validation, accessibility, error handling, form submission. Trigger: When creating forms in React, implementing form validation, or managing form state with Formik."
skills:
  - conventions
  - a11y
  - react
  - yup
  - humanizer
dependencies:
  formik: ">=2.0.0 <3.0.0"
  yup: ">=1.0.0 <2.0.0"
  react: ">=17.0.0 <19.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Formik Skill

## Overview

This skill provides guidance for building forms with Formik in React applications, including validation with Yup, accessibility patterns, and integration with UI libraries.

## Objective

Enable developers to create robust, accessible forms using Formik with proper validation, error handling, and user feedback.

---

## When to Use

Use this skill when:

- Building forms in React with validation
- Managing form state, submission, and errors
- Integrating Yup validation schemas
- Handling complex forms with nested fields
- Creating accessible forms with proper error announcements

Don't use this skill for:

- Simple forms (use basic React state)
- Non-React forms (use html skill)
- Data tables (use ag-grid skill)

---

## Critical Patterns

### ✅ REQUIRED: Use Yup for Validation

```typescript
// ✅ CORRECT: Yup schema with Formik
import * as Yup from 'yup';

const schema = Yup.object({
  email: Yup.string().email('Invalid email').required('Required'),
});

<Formik validationSchema={schema} /* ... */ />

// ❌ WRONG: Manual validation (error-prone)
<Formik validate={(values) => {
  const errors = {};
  if (!values.email) errors.email = 'Required';
  return errors;
}} />
```

### ✅ REQUIRED: Associate Labels with Inputs

```typescript
// ✅ CORRECT: Label with htmlFor
<label htmlFor="email">Email</label>
<Field id="email" name="email" type="email" />

// ❌ WRONG: No label association (inaccessible)
<div>Email</div>
<Field name="email" type="email" />
```

### ✅ REQUIRED: Show Errors Only After Touch

```typescript
// ✅ CORRECT: Check both errors and touched
{errors.email && touched.email && <div>{errors.email}</div>}

// ❌ WRONG: Show errors immediately (poor UX)
{errors.email && <div>{errors.email}</div>}
```

---

## Conventions

Refer to conventions for:

- Code organization
- Error handling

Refer to a11y for:

- Form labels
- Error announcements
- Keyboard navigation

### Formik Specific

- Use Yup for validation schemas
- Implement proper error messages
- Handle submission states (loading, success, error)
- Use Field components for better performance
- Associate labels with inputs properly

---

## Decision Tree

**Simple form (<5 fields)?** → Use basic Formik with `<Field>` components.

**Complex nested form?** → Use `<FieldArray>` for dynamic fields, dot notation for nested: `name="user.address.street"`.

**Async validation?** → Use `validate` prop with async function or Yup's `test()` method.

**Custom input component?** → Use `<Field>` with custom component: `<Field component={CustomInput} />`.

**Submission handling?** → Use `isSubmitting` state, disable button during submit, show success/error feedback.

**Reset form after submit?** → Call `resetForm()` in `onSubmit` after successful submission.

**File upload?** → Use `setFieldValue` to handle file input changes, store File object in state.

---

## Example

```typescript
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';

const validationSchema = Yup.object({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(8, 'Too short').required('Required')
});

<Formik
  initialValues={{ email: '', password: '' }}
  validationSchema={validationSchema}
  onSubmit={(values) => console.log(values)}
>
  {({ errors, touched }) => (
    <Form>
      <Field name="email" type="email" />
      {errors.email && touched.email && <div>{errors.email}</div>}
      <button type="submit">Submit</button>
    </Form>
  )}
</Formik>
```

## Edge Cases

- Handle async validation
- Manage complex nested forms
- Reset forms after submission
- Handle file uploads

## References

- https://formik.org/docs/overview
- https://github.com/jquense/yup
