---
name: managing-server-actions
description: Defines the standard pattern for Next.js 15 Server Actions to handle mutations securely. Use for form submissions and data updates.
---

# Server Actions and Mutations

## When to use this skill
- When handling form submissions (`'use server'`).
- When mutating data in Appwrite from the frontend.
- When you need to revalidate the cache after an update.

## Workflow
- [ ] Create actions in `app/actions/` or directly in the component file.
- [ ] Use `'use server'` at the top of the function or file.
- [ ] Implement `try-catch` for error handling.
- [ ] Call `revalidatePath()` to refresh the UI.

## Code Template (Next.js 15)
```typescript
'use server'

import { revalidatePath } from 'next/cache';
import { BookingService } from '@/services/bookings';

export async function createBookingAction(formData: FormData) {
    try {
        const tourId = formData.get('tourId') as string;
        // Logic to create booking...
        await BookingService.create({ ... });
        
        revalidatePath('/dashboard/bookings');
        return { success: true };
    } catch (error) {
        return { success: false, error: 'Failed to create booking' };
    }
}
```

## Instructions
- **Security**: Always validate user session/permissions inside the Server Action.
- **Data Refresh**: Use `revalidatePath` for the specific route or `revalidateTag` for broader invalidation.
