---
name: implementing-service-layer
description: Defines a pattern for abstracting Appwrite database calls into dedicated service files. Use to keep components clean and reusable.
---

# Appwrite Service Layer Pattern

## When to use this skill
- Before writing database logic in a component.
- When a database query needs to be reused across multiple pages or actions.

## Folder Structure
- `services/tours.ts`
- `services/bookings.ts`
- `services/auth.ts`

## Example Pattern
```typescript
import { databases, DATABASE_ID, COLLECTIONS } from '@/lib/appwrite';
import { Query } from 'appwrite';
import { Tour } from '@/types';

export const TourService = {
    async getAll(limit = 10) {
        return await databases.listDocuments<Tour>(
            DATABASE_ID,
            COLLECTIONS.TOURS,
            [Query.limit(limit), Query.orderDesc('$createdAt')]
        );
    },
    async getById(id: string) {
        return await databases.getDocument<Tour>(DATABASE_ID, COLLECTIONS.TOURS, id);
    }
};
```

## Instructions
- **Abstraction**: Components should call `TourService.getAll()` rather than the Appwrite SDK directly.
- **Error Handling**: Catch errors in the service or re-throw them with descriptive messages.
