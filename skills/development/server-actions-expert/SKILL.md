---
name: server-actions-expert
description: Use this skill for creating safe Next.js server actions with next-safe-action and @kit/action-middleware. Includes authentication, organization context, RBAC permissions, admin actions, proper error handling, revalidation patterns, and form integration.
---

You are an expert in building secure, type-safe server actions using next-safe-action and the @kit/action-middleware package. You create actions that integrate seamlessly with Better Auth, organization multi-tenancy, and RBAC permissions.

## CRITICAL: Always Check Permissions

**Every server action MUST have appropriate permission checks.** Never create an action without considering:

1. **Who can execute this action?** Use the right action client
2. **What role/permission is required?** Add middleware checks
3. **Does the user own this resource?** Verify in service layer

### Permission Check Examples

```typescript
// BAD: No permission check - anyone authenticated can delete ANY post
export const deletePostAction = authenticatedActionClient
  .inputSchema(DeletePostSchema)
  .action(async ({ parsedInput }) => {
    await db.delete(posts).where(eq(posts.id, parsedInput.postId));
  });

// GOOD: Verify ownership in service
export const deletePostAction = authenticatedActionClient
  .inputSchema(DeletePostSchema)
  .action(async ({ parsedInput, ctx }) => {
    await postService.delete({
      postId: parsedInput.postId,
      userId: ctx.user.id, // Service verifies ownership
    });
  });

// GOOD: Role-based permission for org actions
export const removeTeamMemberAction = authenticatedActionClient
  .use(withMinRole('admin')) // Only admins can remove members
  .inputSchema(RemoveMemberSchema)
  .action(async ({ parsedInput, ctx }) => {
    // ctx.organizationId verified by middleware
  });

// GOOD: RBAC permission for specific features
export const updateBillingAction = authenticatedActionClient
  .use(withFeaturePermission({ billing: ['update'] }))
  .inputSchema(BillingSchema)
  .action(async ({ parsedInput, ctx }) => {
    // Only users with billing:update permission
  });
```

### Permission Checklist

Before finalizing any action, verify:

- [ ] Correct action client selected (authenticated/organization/admin)
- [ ] Role middleware added if action requires minimum role
- [ ] Permission middleware added for feature-specific actions
- [ ] Service layer verifies resource ownership with `userId`/`organizationId`
- [ ] Admin actions use `adminActionClient` + `withAdminPermission`

## Action Clients

Choose the right client based on authorization needs:

| Client | Context Provided | Use Case |
|--------|------------------|----------|
| `authenticatedActionClient` | `ctx.user`, `ctx.session` | Any authenticated user action |
| `organizationActionClient` | `ctx.user`, `ctx.organizationId`, `ctx.role` | Actions requiring org context |
| `adminActionClient` | `ctx.user` (admin verified) | Admin-only actions |
| `adminPermissionActionClient` | Same as `adminActionClient` | Admin actions with RBAC |

## Middleware Functions

| Middleware | Purpose |
|------------|---------|
| `withMinRole(role)` | Require minimum role level in org |
| `withFeaturePermission(perms)` | Check RBAC permissions |
| `withAdminPermission(reqs)` | Check admin RBAC permissions |

## File Structure

```
feature/
├── _lib/
│   ├── schemas/
│   │   └── feature.schema.ts      # Zod validation schemas
│   ├── server/
│   │   └── feature-server-actions.ts  # Server actions
│   └── services/
│       └── feature.service.ts     # Business logic
```

## Basic Authenticated Action

```typescript
'use server';

import { revalidatePath } from 'next/cache';

import { authenticatedActionClient } from '@kit/action-middleware';

import { UpdateFeatureSchema } from '../schemas/feature.schema';
import { createFeatureService } from '../services/feature.service';

/**
 * @name updateFeatureAction
 * @description Updates feature for the authenticated user
 */
export const updateFeatureAction = authenticatedActionClient
  .inputSchema(UpdateFeatureSchema)
  .action(async ({ parsedInput: data, ctx }) => {
    const service = createFeatureService();

    const result = await service.update({
      userId: ctx.user.id,
      ...data,
    });

    revalidatePath('/', 'layout');

    return result;
  });
```

## Action Without Input

```typescript
export const noInputAction = authenticatedActionClient.action(
  async ({ ctx }) => {
    // No schema needed when action takes no input
    return { userId: ctx.user.id };
  },
);
```

## Organization-Scoped Action

```typescript
'use server';

import { revalidatePath } from 'next/cache';

import { authenticatedActionClient } from '@kit/action-middleware';
import { requireActiveOrganizationId } from '@kit/better-auth/context';

import { InviteMemberSchema } from '../schemas/members.schema';
import { createInvitationsService } from '../services/invitations.service';

export const inviteMemberAction = authenticatedActionClient
  .inputSchema(InviteMemberSchema)
  .action(async ({ parsedInput: data, ctx }) => {
    const organizationId = await requireActiveOrganizationId();
    const service = createInvitationsService();

    const result = await service.inviteMember({
      userId: ctx.user.id,
      organizationId,
      invitation: data,
    });

    revalidatePath('/', 'layout');

    return result;
  });
```

## Role-Protected Action

```typescript
import { authenticatedActionClient, withMinRole } from '@kit/action-middleware';

export const ownerOnlyAction = authenticatedActionClient
  .use(withMinRole('owner'))
  .inputSchema(Schema)
  .action(async ({ parsedInput, ctx }) => {
    // Only org owners reach here
    // ctx.organizationId and ctx.role available
  });
```

## Permission-Protected Action

```typescript
import {
  authenticatedActionClient,
  withFeaturePermission,
} from '@kit/action-middleware';

export const billingAction = authenticatedActionClient
  .use(withFeaturePermission({ billing: ['update'] }))
  .inputSchema(Schema)
  .action(async ({ ctx }) => {
    // Only users with billing:update permission
  });
```

## Admin Action with Permission

```typescript
'use server';

import { revalidatePath } from 'next/cache';

import { adminActionClient, withAdminPermission } from '@kit/action-middleware';

import { banUserSchema } from '../schemas';
import { createUserAdminService } from '../services/user-admin.service';

export const banUserAction = adminActionClient
  .use(withAdminPermission({ user: ['ban'] }))
  .inputSchema(banUserSchema)
  .action(async ({ parsedInput, ctx }) => {
    const service = createUserAdminService();

    const result = await service.banUser({
      adminId: ctx.user.id,
      ...parsedInput,
    });

    revalidatePath('/admin', 'layout');

    return result;
  });
```

## Schema Patterns

Schemas go in `_lib/schemas/` and are shared between client forms and server actions:

```typescript
// feature.schema.ts
import * as z from 'zod';

export const UpdateFeatureSchema = z.object({
  name: z
    .string()
    .min(2, 'feature.errors.nameMinLength')
    .max(100, 'feature.errors.nameMaxLength'),
  description: z.string().optional(),
});

export type UpdateFeatureInput = z.output<typeof UpdateFeatureSchema>;
```

Use i18n keys in error messages for localization support.

## Consuming Actions in Forms

Use `useAction` from `next-safe-action/hooks`:

```typescript
'use client';

import { useAction } from 'next-safe-action/hooks';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { toast } from '@kit/ui/sonner';

import { updateFeatureAction } from '../server/feature-server-actions';
import { UpdateFeatureSchema } from '../schemas/feature.schema';

export function UpdateFeatureForm() {
  const { executeAsync, status } = useAction(updateFeatureAction);
  const isPending = status === 'executing';

  const form = useForm({
    resolver: zodResolver(UpdateFeatureSchema),
    defaultValues: { name: '' },
  });

  return (
    <form
      onSubmit={form.handleSubmit((data) => {
        toast.promise(
          executeAsync(data).then((response) => {
            if (response.serverError || response.validationErrors) {
              throw new Error(response.serverError || 'An error occurred');
            }
          }),
          {
            loading: 'Saving...',
            success: 'Saved successfully',
            error: 'Failed to save',
          },
        );
      })}
    >
      {/* Form fields */}
    </form>
  );
}
```

## Revalidation Patterns

```typescript
import { revalidatePath, revalidateTag } from 'next/cache';

// Revalidate entire layout (most common)
revalidatePath('/', 'layout');

// Revalidate specific page
revalidatePath('/settings', 'page');

// Revalidate admin area
revalidatePath('/admin', 'layout');

// Revalidate by tag (for fetch caching)
revalidateTag('user-data');
```

## Error Handling

Errors are handled automatically by the middleware:

- **Auth errors**: Preserve message from Better Auth
- **Production**: Generic "Something went wrong" message
- **Development**: Actual error message shown

Standard error types:
- `"Unauthorized"` - no session or permission denied
- `"No active organization"` - org required but not set
- `"Unauthorized: {role} role required"` - insufficient role
- `forbidden()` from `next/navigation` - admin permission denied

For custom errors, throw with meaningful messages:

```typescript
export const deleteAccountAction = authenticatedActionClient
  .inputSchema(DeleteAccountSchema)
  .action(async ({ parsedInput, ctx }) => {
    const eligibility = await checkDeletionEligibility(ctx.user.id);

    if (!eligibility.canDelete) {
      throw new Error(
        'Account cannot be deleted. Please check eligibility requirements.',
      );
    }

    // Proceed with deletion
  });
```

## Context Properties

### authenticatedActionClient
```typescript
ctx: {
  user: { id, email, name, role, ... };
  session: { id, userId, expiresAt, ... };
}
```

### organizationActionClient
```typescript
ctx: {
  user: { ... };
  organizationId: string;
  role: string; // User's role in org
}
```

### adminActionClient
```typescript
ctx: {
  user: { ... }; // Verified admin user
}
```

## Decision Tree

1. **User-only action** → `authenticatedActionClient`
2. **Need org context** → use `requireActiveOrganizationId()` or `organizationActionClient`
3. **Role check needed** → `authenticatedActionClient` + `withMinRole()`
4. **Permission check** → `authenticatedActionClient` + `withFeaturePermission()`
5. **Admin area** → `adminActionClient`
6. **Admin with RBAC** → `adminActionClient` + `withAdminPermission()`

## Best Practices

1. **ALWAYS check permissions** - Use middleware and verify ownership in services
2. **NEVER trust client input for authorization** - Always use `ctx.user.id`, never `parsedInput.userId`
3. Always add `'use server'` directive at top of file
4. Add JSDoc comment with `@name` and `@description` for each action
5. Use services for business logic, keep actions thin
6. Always call `revalidatePath` after mutations
7. Return meaningful results, not just `{ success: true }`
8. Pass `ctx.user.id` and `ctx.organizationId` to services for ownership verification
9. Name files: `{feature}-server-actions.ts`
10. Share schemas between client forms and server actions
11. Use i18n keys in schema error messages

## Security Anti-Patterns to Avoid

```typescript
// NEVER: Trust user-provided IDs for authorization
export const badAction = authenticatedActionClient
  .inputSchema(z.object({ userId: z.string() }))
  .action(async ({ parsedInput }) => {
    // Attacker can pass any userId!
    await service.doSomething(parsedInput.userId);
  });

// NEVER: Skip permission checks for "simple" actions
export const badDeleteAction = authenticatedActionClient
  .action(async ({ parsedInput }) => {
    // No ownership check = anyone can delete anything
    await db.delete(items).where(eq(items.id, parsedInput.id));
  });

// NEVER: Check permissions client-side only
// Client-side checks are for UX, server-side checks are for security
```
