---
name: Request Validation
description: TypeScript-based input validation for API requests and video data structures. Use this when validating request bodies in Express handlers, implementing type guards, or validating RenderRequest and RecapBook data. Ensures type safety at API boundaries.
---

# Request Validation

This Skill provides Claude Code with specific guidance on how it should handle global validation.

## When to use this skill:

- Validating API request bodies in Express handlers
- Creating TypeScript type guard functions
- Checking RenderRequest fields (month, year, books)
- Validating RecapBook data structure and completeness
- Implementing field-specific validation logic
- Returning structured validation error responses

## Instructions

- **TypeScript Type Guards**: Use TypeScript types and type guards for compile-time and runtime validation
- **Server-Side Validation**: All API endpoints must validate request bodies against defined types
- **Fail Early**: Validate input at API boundary; reject invalid requests before processing
- **Specific Error Messages**: Return clear, field-specific errors: `{ error: 'Invalid month', field: 'month' }`
- **Request Body Validation**: Validate RenderRequest fields (month 1-12, year valid, books array structure)
- **Type Safety**: Define interfaces in `src/lib/types.ts` and enforce at API boundaries
- **Business Rule Validation**: Validate video constraints (frame counts, durations, book data completeness)
- **No Client-Side Validation**: This is a server-to-server API; all validation happens server-side

**Examples:**
```typescript
// Good: Type guards, early validation, specific errors
import { RenderRequest, RecapBook } from '@/lib/types';

function isValidRenderRequest(body: any): body is RenderRequest {
  return (
    typeof body.month === 'number' &&
    body.month >= 1 && body.month <= 12 &&
    typeof body.year === 'number' &&
    body.year >= 2000 && body.year <= 2100 &&
    Array.isArray(body.books)
  );
}

app.post('/render', async (req, res) => {
  if (!isValidRenderRequest(req.body)) {
    return res.status(400).json({
      error: 'Invalid request',
      details: 'month (1-12) and year (2000-2100) required'
    });
  }

  const request: RenderRequest = req.body;
  // Now TypeScript knows the shape is correct
});

// Bad: No validation, assumes input is correct
app.post('/render', async (req, res) => {
  const { month, year } = req.body;
  const result = await renderVideo(month, year);
  res.json(result);
});
```
