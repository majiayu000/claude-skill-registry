---
name: yup
description: >-
  Validate data with Yup schemas. Use when adding form validation, defining
  API request schemas, validating configuration, or building type-safe
  validation pipelines in JavaScript/TypeScript.
license: Apache-2.0
compatibility: 'Any JavaScript runtime'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags: [yup, validation, schema, forms, typescript]
---

# Yup

## Overview

Yup is a schema validation library for JavaScript. Define schemas declaratively, validate data, and get detailed error messages. Works with Formik, react-hook-form, and standalone. TypeScript-first with type inference.

## Instructions

### Step 1: Schemas

```typescript
import * as yup from 'yup'

const userSchema = yup.object({
  name: yup.string().min(2).max(100).required(),
  email: yup.string().email().required(),
  age: yup.number().positive().integer().min(13).max(120),
  role: yup.string().oneOf(['admin', 'member', 'viewer']).default('member'),
  tags: yup.array().of(yup.string()).min(1).max(10),
  address: yup.object({
    street: yup.string().required(),
    city: yup.string().required(),
    zip: yup.string().matches(/^\d{5}$/, 'Must be 5 digits'),
  }),
})

// Validate
const user = await userSchema.validate(data, { abortEarly: false })

// Type inference
type User = yup.InferType<typeof userSchema>
```

### Step 2: Custom Validation

```typescript
const passwordSchema = yup.string()
  .min(8)
  .matches(/[A-Z]/, 'Must contain uppercase')
  .matches(/[0-9]/, 'Must contain number')
  .matches(/[^A-Za-z0-9]/, 'Must contain special character')

const signupSchema = yup.object({
  password: passwordSchema.required(),
  confirmPassword: yup.string()
    .oneOf([yup.ref('password')], 'Passwords must match')
    .required(),
})
```

### Step 3: Conditional Validation

```typescript
const schema = yup.object({
  contactMethod: yup.string().oneOf(['email', 'phone']).required(),
  email: yup.string().when('contactMethod', {
    is: 'email',
    then: (s) => s.email().required('Email required when contact method is email'),
  }),
  phone: yup.string().when('contactMethod', {
    is: 'phone',
    then: (s) => s.matches(/^\+\d{10,15}$/).required('Phone required'),
  }),
})
```

## Guidelines

- `abortEarly: false` returns all errors at once — better UX than one-at-a-time.
- Use `InferType` to derive TypeScript types from schemas — single source of truth.
- For new projects, consider Zod instead — better TypeScript inference and ecosystem.
- Yup is still the standard for Formik integration.
- `.when()` for conditional validation — fields required only in certain contexts.
