---
name: defining-typescript-models
description: Defines standard TypeScript interfaces for Appwrite Collections. Use when creating new models for Tours, Users, or Bookings to ensure full type safety.
---

# TypeScript Models and Interfaces

## When to use this skill
- When defining the data structure for a new Appwrite collection.
- When creating props for components that data-fetch.
- To avoid using `any` across the codebase.

## Workflow
- [ ] Export interfaces from a central `types/` directory.
- [ ] Include standard Appwrite fields (`$id`, `$createdAt`, `$updatedAt`, `$permissions`).
- [ ] Use Enums for fields with fixed values (e.g., `BookingStatus`).

## Example Template
```typescript
import { Models } from 'appwrite';

export interface Tour extends Models.Document {
    title: string;
    description: string;
    price: number;
    location: string;
    images: string[];
    rating: number;
    availableDates: string[]; // ISO Strings
}

export type BookingStatus = 'pending' | 'confirmed' | 'cancelled';

export interface Booking extends Models.Document {
    userId: string;
    tourId: string;
    status: BookingStatus;
    totalPrice: number;
}
```

## Instructions
- **Generics**: Use these interfaces with Appwrite SDK methods: `databases.listDocuments<Tour>(...)`.
- **Readonly**: Mark fields as `readonly` if they shouldn't be mutated by the frontend.
