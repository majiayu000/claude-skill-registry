---
name: managing-optimistic-ui
description: Implements "Fast Sync" using the useOptimistic hook. Use when you want to provide instant feedback for user actions like booking or liking while the backend processes.
---

# Optimistic UI Updates

## When to use this skill
- When a user performs a mutation (e.g., "Book Now", "Cancel Booking", "Like Tour").
- To improve perceived performance by updating the UI before the server responds.

## Workflow
- [ ] Use the `useOptimistic` hook in a Client Component.
- [ ] Pass the initial state and an update function to `useOptimistic`.
- [ ] Call the state update function immediately before triggering the Server Action.
- [ ] The UI will automatically revert if the Server Action fails (when the component re-renders with fresh data).

## Code Template
```tsx
'use client'
import { useOptimistic } from 'react';
import { bookTourAction } from '@/actions/bookings';

export function BookingButton({ tourId, initialStatus }: { tourId: string, initialStatus: string }) {
    const [optimisticStatus, setOptimisticStatus] = useOptimistic(
        initialStatus,
        (_, newStatus: string) => newStatus
    );

    const handleAction = async () => {
        setOptimisticStatus('confirmed'); // Optimistic state
        const result = await bookTourAction(tourId);
        if (!result.success) {
            // Reversion happens automatically on re-render if we don't manually handle it
        }
    };

    return (
        <button onClick={handleAction}>
            {optimisticStatus === 'confirmed' ? 'Booked!' : 'Book Now'}
        </button>
    );
}
```

## Instructions
- **Read-Your-Writes**: Use `revalidatePath` in the server action to ensure the official state replaces the optimistic one.
- **Failures**: Ensure the backend mutation returns a failure if it cannot be processed so the UI doesn't remain in a "false" state.
