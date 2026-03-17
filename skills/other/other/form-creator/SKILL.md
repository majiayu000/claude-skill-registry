---
name: form-creator
description: Create forms, validation schemas, and CRUD API endpoints. Use when building new data entry features or managing existing forms.
---

# Form Creator

## Instructions

### 1. Validation Schema
- **File**: `src/lib/validations/{feature}.schema.ts`
- **Action**: Define Zod schema and export inferred type.
  ```typescript
  export const featureSchema = z.object({ ... });
  export type FeatureFormValues = z.infer<typeof featureSchema>;
  ```

### 2. Form Component
- **File**: `src/components/forms/{feature}-form.tsx`
- **Directives**: `"use client";` required.
- **Setup**: Use `useForm` with `zodResolver`.
- **Props**: Accept `initialData` and `onSubmit`.
- **UI**: Use Shadcn components (`Form`, `FormField`, `Input`).

### 3. API Routes
- **File**: `src/app/api/{feature}/route.ts`
- **Security**: Wrap with `withAuthRequired` or `withSuperAdminAuthRequired`.
- **Logic**:
  - `GET`: Handle pagination/search.
  - `POST`: Validate body against schema -> Insert to DB.
  - `PATCH`: Validate partial body -> Update DB.

## Reference
For code patterns, best practices, and examples, see [reference.md](reference.md).

