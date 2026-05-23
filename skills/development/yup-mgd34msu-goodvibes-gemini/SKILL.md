---
name: yup
description: Validates data with Yup schema builder using chainable methods, custom rules, and TypeScript inference. Use when validating forms with React Hook Form or Formik, or when needing flexible schema validation.
---

# Yup

Schema validation library with a fluent, chainable API for JavaScript and TypeScript.

## Quick Start

```bash
npm install yup
```

```typescript
import * as yup from 'yup';

const schema = yup.object({
  name: yup.string().required(),
  email: yup.string().email().required(),
  age: yup.number().positive().integer(),
});

// Validate
const data = await schema.validate({ name: 'John', email: 'john@example.com' });

// Check validity
const isValid = await schema.isValid(data);
```

## Schema Types

### String

```typescript
yup.string()
  .required('Name is required')
  .min(2, 'At least 2 characters')
  .max(50, 'At most 50 characters')
  .matches(/^[a-zA-Z]+$/, 'Only letters')
  .email('Invalid email')
  .url('Invalid URL')
  .uuid('Invalid UUID')
  .lowercase()
  .uppercase()
  .trim()
  .default('Anonymous')
```

### Number

```typescript
yup.number()
  .required('Required')
  .min(0, 'Must be positive')
  .max(100, 'Max 100')
  .positive('Must be positive')
  .negative('Must be negative')
  .integer('Must be integer')
  .moreThan(0, 'Greater than 0')
  .lessThan(100, 'Less than 100')
  .truncate()
  .round()
  .default(0)
```

### Boolean

```typescript
yup.boolean()
  .required()
  .isTrue('Must accept terms')
  .isFalse()
  .default(false)
```

### Date

```typescript
yup.date()
  .required()
  .min(new Date(), 'Must be in the future')
  .max(new Date('2030-12-31'), 'Too far ahead')
  .default(() => new Date())
```

### Array

```typescript
yup.array()
  .of(yup.string().required())
  .min(1, 'At least one item')
  .max(5, 'At most 5 items')
  .required()
  .default([])

// Tuple-like array
yup.tuple([
  yup.string().required(),
  yup.number().required(),
])
```

### Object

```typescript
yup.object({
  name: yup.string().required(),
  age: yup.number().positive(),
})
  .noUnknown() // Reject unknown keys
  .strict()    // Don't coerce types
```

### Mixed (Any Type)

```typescript
yup.mixed()
  .oneOf(['option1', 'option2'], 'Must be option1 or option2')
  .notOneOf(['forbidden'])
  .required()
```

## Common Patterns

### User Registration

```typescript
const registrationSchema = yup.object({
  email: yup.string()
    .email('Invalid email')
    .required('Email is required'),

  password: yup.string()
    .min(8, 'At least 8 characters')
    .matches(/[a-z]/, 'Need lowercase letter')
    .matches(/[A-Z]/, 'Need uppercase letter')
    .matches(/[0-9]/, 'Need number')
    .required('Password is required'),

  confirmPassword: yup.string()
    .oneOf([yup.ref('password')], 'Passwords must match')
    .required('Confirm password'),

  age: yup.number()
    .positive()
    .integer()
    .min(18, 'Must be 18+')
    .required('Age is required'),

  terms: yup.boolean()
    .isTrue('Must accept terms'),
});
```

### Address

```typescript
const addressSchema = yup.object({
  street: yup.string().required(),
  city: yup.string().required(),
  state: yup.string().length(2).required(),
  zip: yup.string()
    .matches(/^\d{5}(-\d{4})?$/, 'Invalid ZIP')
    .required(),
  country: yup.string().default('US'),
});
```

### Payment

```typescript
const paymentSchema = yup.object({
  cardNumber: yup.string()
    .matches(/^\d{16}$/, 'Invalid card number')
    .required(),

  expiry: yup.string()
    .matches(/^(0[1-9]|1[0-2])\/\d{2}$/, 'MM/YY format')
    .required(),

  cvv: yup.string()
    .matches(/^\d{3,4}$/, 'Invalid CVV')
    .required(),

  amount: yup.number()
    .positive()
    .required(),
});
```

## Conditional Validation

### when() - Field Dependencies

```typescript
const schema = yup.object({
  hasCompany: yup.boolean(),

  companyName: yup.string().when('hasCompany', {
    is: true,
    then: (schema) => schema.required('Company name required'),
    otherwise: (schema) => schema.notRequired(),
  }),
});
```

### Multiple Conditions

```typescript
const schema = yup.object({
  type: yup.string().oneOf(['personal', 'business']),
  taxId: yup.string(),
  ssn: yup.string(),
}).test('tax-info', 'Tax info required', function(value) {
  if (value.type === 'business') {
    return !!value.taxId;
  }
  return !!value.ssn;
});
```

## Custom Validation

### test() Method

```typescript
const schema = yup.string().test(
  'is-valid-username',
  'Username already taken',
  async (value) => {
    if (!value) return true;
    const available = await checkUsername(value);
    return available;
  }
);
```

### With Context

```typescript
const schema = yup.object({
  password: yup.string().required(),
  confirmPassword: yup.string()
    .test('passwords-match', 'Passwords must match', function(value) {
      return value === this.parent.password;
    }),
});
```

### addMethod() - Reusable Validators

```typescript
yup.addMethod(yup.string, 'phone', function(message) {
  return this.test('phone', message || 'Invalid phone', (value) => {
    if (!value) return true;
    return /^\+?[\d\s-()]+$/.test(value);
  });
});

// Usage
const schema = yup.object({
  phone: yup.string().phone('Invalid phone number'),
});
```

## Type Inference

### InferType

```typescript
const userSchema = yup.object({
  name: yup.string().required(),
  email: yup.string().email().required(),
  age: yup.number().positive(),
});

type User = yup.InferType<typeof userSchema>;
// { name: string; email: string; age: number | undefined }
```

### With Defaults

```typescript
const schema = yup.object({
  role: yup.string().default('user'),
  active: yup.boolean().default(true),
});

type Config = yup.InferType<typeof schema>;
// { role: string; active: boolean }
```

## Transformation

### cast() - Transform Values

```typescript
const schema = yup.string().trim().lowercase();
const result = schema.cast('  HELLO  '); // 'hello'
```

### transform() - Custom Transforms

```typescript
const schema = yup.string().transform((value) => {
  return value?.replace(/\s+/g, ' ').trim();
});
```

### Object Transform

```typescript
const schema = yup.object({
  firstName: yup.string(),
  lastName: yup.string(),
}).transform((value) => ({
  ...value,
  fullName: `${value.firstName} ${value.lastName}`,
}));
```

## Validation Options

### validate()

```typescript
try {
  const result = await schema.validate(data, {
    abortEarly: false,      // Collect all errors
    stripUnknown: true,     // Remove unknown keys
    strict: false,          // Allow coercion
    context: { user: currentUser },
  });
} catch (err) {
  if (err instanceof yup.ValidationError) {
    console.log(err.errors);  // All error messages
    console.log(err.inner);   // Detailed errors
  }
}
```

### validateSync()

```typescript
try {
  const result = schema.validateSync(data);
} catch (err) {
  // Handle error
}
```

### isValid()

```typescript
const valid = await schema.isValid(data);
```

## React Hook Form Integration

```typescript
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';

const schema = yup.object({
  email: yup.string().email().required(),
  password: yup.string().min(8).required(),
});

type FormData = yup.InferType<typeof schema>;

function Form() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: yupResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}

      <input {...register('password')} type="password" />
      {errors.password && <span>{errors.password.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
```

## Formik Integration

```typescript
import { Formik, Form, Field, ErrorMessage } from 'formik';

const schema = yup.object({
  email: yup.string().email().required(),
});

function MyForm() {
  return (
    <Formik
      initialValues={{ email: '' }}
      validationSchema={schema}
      onSubmit={handleSubmit}
    >
      <Form>
        <Field name="email" type="email" />
        <ErrorMessage name="email" />
        <button type="submit">Submit</button>
      </Form>
    </Formik>
  );
}
```

See [references/methods.md](references/methods.md) for complete method reference.
