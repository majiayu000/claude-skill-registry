---
name: formatting-api-responses
description: Standardizes the structure of internal function results. Use when writing Services or Server Actions.
---

# API Response Formatting

## When to use this skill
- Writing any function that fetches or mutates data and is called by the frontend.
- Ensuring the UI knows exactly how to read a "Success" or "Failure".

## Standard Structure
```typescript
{
    success: boolean;
    data?: T;       // The resulting object(s)
    error?: string; // User-friendly error message
    code?: number;  // Optional status code (404, 401, etc.)
}
```

## Example Usage
```typescript
export async function deleteBooking(id: string) {
    try {
        await BookingService.delete(id);
        return { success: true };
    } catch (e) {
        return { success: false, error: "Could not delete booking. Please try again." };
    }
}
```

## Instructions
- **Consistency**: Never return raw error objects to the component; always parse them into a `success: false` structure.
