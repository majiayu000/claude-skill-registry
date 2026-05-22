---
name: zod-form-validation
description: Zod schema validation and React Hook Form integration for TypeScript frontends. This skill should be used when creating forms, defining API schemas, validating form data, implementing type-safe validation, using ZodResolver with React Hook Form, or migrating legacy forms to the Zod + React Hook Form pattern.
---

# Zod Form Validation Skill

Implements type-safe form validation using Zod schemas with React Hook Form integration in the DTX frontend.

## Quick Reference

### Form Setup Pattern

```typescript
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from '~/components/ui/form';

// 1. Define schema
const MySchema = z.object({
  email: z.string().email('Invalid email'),
  name: z.string().min(2, 'Name too short'),
});

// 2. Create form with zodResolver
const form = useForm<z.infer<typeof MySchema>>({
  resolver: zodResolver(MySchema),
  defaultValues: { email: '', name: '' },
});

// 3. Handle submission
const onSubmit = (data: z.infer<typeof MySchema>) => {
  toast.promise(apiCall(data), {
    loading: 'Saving...',
    success: 'Saved!',
    error: (err) => `Failed: ${err?.response?.data ?? String(err)}`,
  });
};
```

### Form Field Pattern

```typescript
<FormField
  control={form.control}
  name="email"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Email</FormLabel>
      <FormControl>
        <Input {...field} />
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Project Conventions

### Schema Location

Define schemas in `~/components/<feature>/schemas.ts`:
- `UserSchema` in `~/components/user/schemas.ts`
- `TeamSchema` in `~/components/team/schemas.ts`
- `GameSchema` in `~/components/game/schemas.ts`

### Type Extraction

Always use `z.infer<typeof Schema>` for types instead of manual interfaces:

```typescript
export const UserSchema = z.object({ /* ... */ });
export type UserType = z.infer<typeof UserSchema>;
```

### Error Handling

Wrap mutations in `toast.promise()`:

```typescript
import { toast } from 'sonner';
import { getLogger } from '~/lib/logger';

const log = getLogger('FormComponent');

toast.promise(apiCall(data), {
  loading: 'Processing...',
  success: (response) => {
    setData(response);
    return 'Success!';
  },
  error: (err) => {
    log.error('API call failed', err);
    return `Failed: ${err?.response?.data ?? String(err)}`;
  },
});
```

## Detailed References

For comprehensive documentation:
- [Zod Schema Patterns](references/zod-schemas.md) - Schema types, validation, composition
- [React Hook Form Integration](references/react-hook-form.md) - Form setup, field types, error handling
- [Form Field Components](references/form-fields.md) - Input, Select, Checkbox patterns

## Migration Guide

When migrating legacy forms from manual `useState` to React Hook Form + Zod:

1. Create/update schema in `schemas.ts`
2. Replace `useState` with `useForm({ resolver: zodResolver(Schema) })`
3. Replace input handlers with `<FormField>` components
4. Remove manual error state management
5. Wrap form in `<Form {...form}>` provider

Reference implementation: `~/pages/profile/profile.tsx`

## Common Patterns

### Nested Objects

```typescript
const Schema = z.object({
  user: z.object({
    name: z.string(),
    email: z.string().email(),
  }),
});

<FormField control={form.control} name="user.name" ... />
```

### Optional & Nullable

```typescript
const Schema = z.object({
  nickname: z.string().nullable().optional(),
  mmr: z.number().min(0).nullable().optional(),
});
```

### Select Fields (Number Values)

```typescript
<FormField
  control={form.control}
  name="position"
  render={({ field }) => (
    <Select onValueChange={(v) => field.onChange(Number(v))} defaultValue={field.value?.toString()}>
      {/* options */}
    </Select>
  )}
/>
```

## Dependencies

Required packages (already installed in DTX frontend):
- `zod: ^4.1.5`
- `react-hook-form: ^7.62.0`
- `@hookform/resolvers: ^5.2.1`
