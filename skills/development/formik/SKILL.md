---
name: formik
description: Manages React form state with Formik using validation, field arrays, and form context. Use when building complex forms in React, handling form submission, or integrating with Yup validation.
---

# Formik

Form state management library for React with built-in validation, submission handling, and field management.

## Quick Start

```bash
npm install formik yup
```

```tsx
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const schema = Yup.object({
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(8, 'Too short').required('Required'),
});

function LoginForm() {
  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      validationSchema={schema}
      onSubmit={(values, { setSubmitting }) => {
        console.log(values);
        setSubmitting(false);
      }}
    >
      {({ isSubmitting }) => (
        <Form>
          <Field name="email" type="email" />
          <ErrorMessage name="email" component="div" />

          <Field name="password" type="password" />
          <ErrorMessage name="password" component="div" />

          <button type="submit" disabled={isSubmitting}>
            Submit
          </button>
        </Form>
      )}
    </Formik>
  );
}
```

## useFormik Hook

```tsx
import { useFormik } from 'formik';

function Form() {
  const formik = useFormik({
    initialValues: {
      email: '',
      password: '',
    },
    validationSchema: schema,
    onSubmit: (values) => {
      console.log(values);
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <input
        name="email"
        type="email"
        onChange={formik.handleChange}
        onBlur={formik.handleBlur}
        value={formik.values.email}
      />
      {formik.touched.email && formik.errors.email && (
        <div>{formik.errors.email}</div>
      )}

      <input
        name="password"
        type="password"
        {...formik.getFieldProps('password')}
      />
      {formik.touched.password && formik.errors.password && (
        <div>{formik.errors.password}</div>
      )}

      <button type="submit">Submit</button>
    </form>
  );
}
```

## Field Component

### Basic Fields

```tsx
<Field name="firstName" />
<Field name="email" type="email" />
<Field name="message" as="textarea" />
<Field name="color" as="select">
  <option value="">Select</option>
  <option value="red">Red</option>
  <option value="blue">Blue</option>
</Field>
```

### With Custom Component

```tsx
<Field name="phone">
  {({ field, meta }) => (
    <div>
      <input {...field} className={meta.error ? 'error' : ''} />
      {meta.touched && meta.error && <span>{meta.error}</span>}
    </div>
  )}
</Field>
```

### Custom Input Component

```tsx
const TextInput = ({ label, ...props }) => {
  const [field, meta] = useField(props);

  return (
    <div>
      <label htmlFor={props.name}>{label}</label>
      <input {...field} {...props} />
      {meta.touched && meta.error && <div className="error">{meta.error}</div>}
    </div>
  );
};

// Usage
<TextInput label="Email" name="email" type="email" />
```

## Form Component

```tsx
<Formik initialValues={...} onSubmit={...}>
  <Form>
    {/* Form fields */}
  </Form>
</Formik>
```

Or with render prop:

```tsx
<Formik initialValues={...} onSubmit={...}>
  {(formikProps) => (
    <form onSubmit={formikProps.handleSubmit}>
      {/* Access formik state */}
    </form>
  )}
</Formik>
```

## Validation

### With Yup

```tsx
import * as Yup from 'yup';

const validationSchema = Yup.object({
  firstName: Yup.string()
    .max(15, 'Must be 15 characters or less')
    .required('Required'),
  lastName: Yup.string()
    .max(20, 'Must be 20 characters or less')
    .required('Required'),
  email: Yup.string()
    .email('Invalid email')
    .required('Required'),
});

<Formik validationSchema={validationSchema} ... />
```

### Custom Validate Function

```tsx
<Formik
  validate={(values) => {
    const errors = {};

    if (!values.email) {
      errors.email = 'Required';
    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(values.email)) {
      errors.email = 'Invalid email';
    }

    return errors;
  }}
  ...
/>
```

### Field-Level Validation

```tsx
const validateUsername = async (value) => {
  if (!value) return 'Required';
  const taken = await checkUsername(value);
  if (taken) return 'Username taken';
};

<Field name="username" validate={validateUsername} />
```

## Field Arrays

```tsx
import { FieldArray } from 'formik';

<Formik
  initialValues={{
    friends: [''],
  }}
  onSubmit={...}
>
  {({ values }) => (
    <Form>
      <FieldArray name="friends">
        {({ push, remove }) => (
          <div>
            {values.friends.map((friend, index) => (
              <div key={index}>
                <Field name={`friends.${index}`} />
                <button type="button" onClick={() => remove(index)}>
                  Remove
                </button>
              </div>
            ))}
            <button type="button" onClick={() => push('')}>
              Add Friend
            </button>
          </div>
        )}
      </FieldArray>
    </Form>
  )}
</Formik>
```

### Array of Objects

```tsx
<Formik
  initialValues={{
    contacts: [{ name: '', email: '' }],
  }}
  ...
>
  {({ values }) => (
    <FieldArray name="contacts">
      {({ push, remove }) => (
        <>
          {values.contacts.map((contact, index) => (
            <div key={index}>
              <Field name={`contacts.${index}.name`} placeholder="Name" />
              <Field name={`contacts.${index}.email`} placeholder="Email" />
              <button onClick={() => remove(index)}>Remove</button>
            </div>
          ))}
          <button onClick={() => push({ name: '', email: '' })}>
            Add Contact
          </button>
        </>
      )}
    </FieldArray>
  )}
</Formik>
```

## Formik Context

### useFormikContext

```tsx
import { useFormikContext } from 'formik';

function SubmitButton() {
  const { isSubmitting, isValid } = useFormikContext();

  return (
    <button type="submit" disabled={isSubmitting || !isValid}>
      {isSubmitting ? 'Submitting...' : 'Submit'}
    </button>
  );
}
```

### Accessing Form State

```tsx
function FormDebug() {
  const { values, errors, touched, isValid, dirty } = useFormikContext();

  return (
    <pre>
      {JSON.stringify({ values, errors, touched, isValid, dirty }, null, 2)}
    </pre>
  );
}
```

## Form State

### Formik Props

```tsx
<Formik ...>
  {({
    // Values
    values,           // Form values
    initialValues,    // Initial values
    errors,           // Validation errors
    touched,          // Touched fields

    // Status
    isSubmitting,     // Submit in progress
    isValid,          // No validation errors
    isValidating,     // Validation in progress
    dirty,            // Values changed from initial

    // Handlers
    handleSubmit,     // Form submit handler
    handleChange,     // Input change handler
    handleBlur,       // Input blur handler
    handleReset,      // Reset form

    // Helpers
    setFieldValue,    // Set specific field
    setFieldTouched,  // Mark field as touched
    setFieldError,    // Set field error
    setValues,        // Set all values
    setErrors,        // Set all errors
    setTouched,       // Set all touched
    setStatus,        // Set form status
    setSubmitting,    // Set submitting state
    resetForm,        // Reset to initial
    validateForm,     // Trigger validation
    validateField,    // Validate specific field

    // Getters
    getFieldProps,    // Get field props helper
    getFieldMeta,     // Get field meta (error, touched)
    getFieldHelpers,  // Get field helpers
  }) => (
    <Form>...</Form>
  )}
</Formik>
```

## Submission

### Basic Submit

```tsx
<Formik
  onSubmit={(values, { setSubmitting }) => {
    submitToServer(values).then(() => {
      setSubmitting(false);
    });
  }}
  ...
/>
```

### Async Submit

```tsx
<Formik
  onSubmit={async (values, { setSubmitting, setStatus, resetForm }) => {
    try {
      await api.submit(values);
      resetForm();
      setStatus({ success: true });
    } catch (error) {
      setStatus({ error: error.message });
    } finally {
      setSubmitting(false);
    }
  }}
  ...
/>
```

### With Server Errors

```tsx
<Formik
  onSubmit={async (values, { setErrors }) => {
    try {
      await api.submit(values);
    } catch (error) {
      if (error.validationErrors) {
        setErrors(error.validationErrors);
      }
    }
  }}
  ...
/>
```

## Enable/Disable Reinitialize

```tsx
<Formik
  initialValues={userData}
  enableReinitialize={true}  // Update when initialValues change
  ...
/>
```

## TypeScript

```tsx
interface FormValues {
  email: string;
  password: string;
}

const initialValues: FormValues = {
  email: '',
  password: '',
};

<Formik<FormValues>
  initialValues={initialValues}
  onSubmit={(values: FormValues) => {
    console.log(values.email);
  }}
  ...
/>
```

### Typed Custom Field

```tsx
import { useField, FieldHookConfig } from 'formik';

interface TextInputProps extends FieldHookConfig<string> {
  label: string;
}

const TextInput: React.FC<TextInputProps> = ({ label, ...props }) => {
  const [field, meta] = useField(props);

  return (
    <div>
      <label>{label}</label>
      <input {...field} {...props} />
      {meta.touched && meta.error && <div>{meta.error}</div>}
    </div>
  );
};
```

See [references/patterns.md](references/patterns.md) for advanced patterns and recipes.
