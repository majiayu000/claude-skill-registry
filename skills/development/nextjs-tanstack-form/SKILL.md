---
name: nextjs-tanstack-form
description: TanStack Form v1 for Next.js 16 with Server Actions, Zod validation, and shadcn/ui integration. Use when building forms, validation, multi-step wizards, or dynamic field arrays.
versions:
  tanstack-form: 1.0
  nextjs: 16
  react: 19
  zod: 3.24
user-invocable: true
references: references/installation.md, references/basic-usage.md, references/field-api.md, references/form-state.md, references/validation-zod.md, references/server-actions.md, references/array-fields.md, references/async-validation.md, references/shadcn-integration.md, references/typescript.md, references/multi-step-form.md, references/performance.md, references/testing.md, references/migration-rhf.md
related-skills: nextjs-16, nextjs-shadcn, solid-nextjs
---

# TanStack Form for Next.js 16

Type-safe, performant forms with Server Actions and signal-based reactivity.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing forms and validation patterns
2. **fuse-ai-pilot:research-expert** - Verify latest TanStack Form docs via Context7/Exa
3. **mcp__context7__query-docs** - Check form options and field API

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Building forms with complex validation requirements
- Need Server Actions integration for form submission
- Implementing multi-step wizards or dynamic field arrays
- Require real-time async validation (username availability)
- Want type-safe forms with full TypeScript inference

### Why TanStack Form

| Feature | Benefit |
|---------|---------|
| Signal-based state | Minimal re-renders, optimal performance |
| Full TypeScript | DeepKeys, DeepValue inference |
| Server Actions native | Built-in Next.js 16 integration |
| Zod adapter | Schema-first validation |
| Framework agnostic | Same API for React, Vue, Solid |
| Headless | Works with any UI library (shadcn/ui) |

---

## Critical Rules

1. **formOptions shared** - Define once, use in client and server
2. **Server validation** - DB checks in `onServerValidate`, not client
3. **Zod schemas** - Client-side instant feedback
4. **useActionState** - React 19 hook for Server Actions
5. **mergeForm** - Combine server errors with client state
6. **SOLID paths** - Forms in `modules/[feature]/src/components/forms/`

---

## SOLID Architecture

### Module Structure

Forms organized by feature module:

- `modules/auth/src/components/forms/` - Auth forms (login, signup)
- `modules/auth/src/interfaces/` - Form types and schemas
- `modules/auth/src/actions/` - Server Actions for form submission
- `modules/cores/lib/forms/` - Shared form utilities

### File Organization

| File | Purpose | Max Lines |
|------|---------|-----------|
| `form-options.ts` | Shared formOptions + Zod schema | 50 |
| `FormComponent.tsx` | Client form UI with fields | 80 |
| `form.action.ts` | Server Action with validation | 30 |
| `form.interface.ts` | Types for form values | 30 |

---

## Key Concepts

### Form Options Pattern

Define form configuration once, share between client and server. Ensures type safety and consistency.

### Field API

Each field has state (value, errors, touched, validating) and handlers (handleChange, handleBlur).

### Validation Levels

- **onChange** - Real-time as user types
- **onBlur** - When field loses focus
- **onSubmit** - Before form submission
- **onServer** - Server-side in action

### Error Management

Errors exist at field-level and form-level. Use `field.state.meta.errors` for field errors, `form.state.errorMap` for form errors.

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Initial setup | [installation.md](references/installation.md) |
| Basic patterns | [basic-usage.md](references/basic-usage.md), [field-api.md](references/field-api.md) |
| Validation | [validation-zod.md](references/validation-zod.md), [async-validation.md](references/async-validation.md) |
| Server Actions | [server-actions.md](references/server-actions.md) |
| Dynamic forms | [array-fields.md](references/array-fields.md), [multi-step-form.md](references/multi-step-form.md) |
| UI integration | [shadcn-integration.md](references/shadcn-integration.md) |
| TypeScript | [typescript.md](references/typescript.md) |
| Migration | [migration-rhf.md](references/migration-rhf.md) |

---

## Best Practices

1. **Define schemas first** - Zod schemas drive both validation and types
2. **Shared formOptions** - Single source of truth for client/server
3. **Debounce async validation** - Use `asyncDebounceMs` for API calls
4. **form.Subscribe** - Selective re-renders for submit state
5. **Field composition** - Reusable field components with shadcn/ui
6. **Server errors merge** - Use `mergeForm` to show server validation errors

---

## Comparison vs React Hook Form

| Aspect | TanStack Form | React Hook Form |
|--------|---------------|-----------------|
| Type Safety | 100% (DeepKeys) | Manual typing |
| Performance | Signals (minimal) | Refs (good) |
| Server Actions | Native support | Manual integration |
| Bundle Size | ~12KB | ~9KB |
| Learning Curve | Medium | Low |
| Use Case | Complex apps | Standard forms |
