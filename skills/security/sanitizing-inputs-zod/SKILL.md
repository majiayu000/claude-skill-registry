---
name: sanitizing-inputs-zod
description: Advanced input validation and sanitization using Zod. Use to prevent XSS and ensure data integrity before sending to Appwrite.
---

# Input Sanitization and Zod (Advanced)

## When to use this skill
- Every form that accepts user input (Reviews, Profile updates, Booking special requests).
- Before performing any database mutation in a Server Action.

## Advanced Schema
```typescript
import { z } from 'zod';

export const TourReviewSchema = z.object({
    rating: z.number().min(1).max(5),
    comment: z.string().trim()
        .min(10, "Comment too short")
        .max(500, "Comment too long")
        .refine(s => !s.includes('<script>'), { message: "Invalid characters" }),
});
```

## Instructions
- **Server-Side Only**: Validation MUST happen on the server (Server Action) even if you have client-side validation.
- **Type Inference**: Use `z.infer<typeof Schema>` to generate TypeScript types from your validation logic.
- **Sanitization**: Use `.trim()`, `.toLowerCase()`, and custom transforms to clean data before persistence.
