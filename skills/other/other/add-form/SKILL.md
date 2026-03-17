---
name: add-form
description: Create a react-hook-form wired to a tRPC mutation with validation
---

# Add Form Skill

Create a form component using react-hook-form wired to a tRPC mutation with Zod validation.

## Arguments

The user describes the form. If unclear, ask for:

- Form purpose (create, edit, settings, etc.)
- Which tRPC mutation to call
- Fields with types
- Whether it's a standalone page or embedded component

## File Location

- **Standalone page**: `apps/web/src/app/(dashboard)/{path}/page.tsx`
- **Reusable component**: `apps/web/src/components/{FormName}.tsx`

## Form Template

Reference: `apps/web/src/app/(dashboard)/projects/new/page.tsx`

```tsx
'use client';

import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { trpc } from '@x4/shared/api-client';
import type { CreateEntity } from '@x4/shared/utils';
import { CreateEntitySchema } from '@x4/shared/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';

export default function CreateEntityPage() {
  const router = useRouter();
  const utils = trpc.useUtils();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<CreateEntity>({
    resolver: zodResolver(CreateEntitySchema),
    defaultValues: {
      name: '',
      description: '',
    },
  });

  const createMutation = trpc.entity.create.useMutation({
    onSuccess: (data) => {
      toast.success('Entity created successfully');
      utils.entity.list.invalidate();
      router.push(`/entities/${data.id}`);
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });

  const onSubmit = (data: CreateEntity) => {
    createMutation.mutate(data);
  };

  return (
    <div className="container mx-auto max-w-2xl py-8">
      <h1 className="text-3xl font-bold mb-6">Create Entity</h1>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <Input id="name" {...register('name')} placeholder="Enter name" />
          {errors.name && <p className="text-sm text-destructive">{errors.name.message}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="description">Description</Label>
          <Textarea id="description" {...register('description')} placeholder="Enter description" />
          {errors.description && (
            <p className="text-sm text-destructive">{errors.description.message}</p>
          )}
        </div>

        <Button type="submit" disabled={isSubmitting || createMutation.isPending}>
          {createMutation.isPending ? 'Creating...' : 'Create Entity'}
        </Button>
      </form>
    </div>
  );
}
```

## Edit Form Variant

For edit forms, pre-populate with existing data:

```tsx
const { data: entity } = trpc.entity.get.useQuery({ id });

const form = useForm<UpdateEntity>({
  resolver: zodResolver(UpdateEntitySchema),
  values: entity
    ? { id: entity.id, name: entity.name, description: entity.description }
    : undefined,
});

const updateMutation = trpc.entity.update.useMutation({
  onSuccess: () => {
    toast.success('Updated successfully');
    utils.entity.get.invalidate({ id });
  },
});
```

## Key Patterns

- **Validation**: Always use `zodResolver` with shared Zod schemas
- **Cache invalidation**: Call `utils.router.procedure.invalidate()` on success
- **Loading state**: Disable submit button with `isSubmitting || mutation.isPending`
- **Error display**: Show field errors inline, toast for server errors
- **Navigation**: Use `router.push()` for redirects after creation
- **Components**: shadcn/ui `Input`, `Textarea`, `Button`, `Label`, `Select`

## Workflow

1. Ensure Zod schemas exist (`/add-schema` if needed)
2. Ensure tRPC mutation exists (`/add-router` if needed)
3. Create the form component or page
4. Wire `useForm` → `zodResolver` → `useMutation`
5. Add field error display and loading states
6. Run `bun turbo type-check` to verify
7. Test the form manually in the browser
