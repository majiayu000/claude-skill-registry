---
name: TypeScript Type Definitions
description: TypeScript interface and type definitions for video data structures. Use this when defining types in src/lib/types.ts, creating new interfaces for request/response payloads, or defining prop types for components. Ensures strong typing across the video generation pipeline.
---

# TypeScript Type Definitions

This Skill provides Claude Code with specific guidance on how it should handle TypeScript types and interfaces.

## When to use this skill:

- Defining new types or interfaces in src/lib/types.ts
- Creating request/response payload types for API endpoints
- Defining component prop interfaces
- Adding fields to existing interfaces (RenderRequest, RecapBook)
- Creating enum or const objects for fixed value sets
- Refactoring types for better type safety

## Instructions

- **Centralized Types**: Define all shared types in `src/lib/types.ts` for consistency
- **Interface Naming**: Use descriptive names that indicate purpose (RenderRequest, RecapBook, MonthlyRecapExport)
- **Strong Typing**: Avoid `any`; use specific types for all function parameters and return values
- **Required vs Optional**: Use `?` for optional fields; avoid excessive optionality
- **Type Exports**: Export all public-facing types for use across the codebase
- **Enum for Constants**: Use enums or const objects for fixed sets of values (e.g., AnimationType)
- **Readonly Where Appropriate**: Use `readonly` for immutable properties in interfaces

**Examples:**
```typescript
// Good: Clear types, required fields explicit, exported
export interface RenderRequest {
  month: number; // 1-12
  year: number;
  books: RecapBook[];
  templateId?: string;
}

export interface RecapBook {
  title: string;
  author: string;
  coverUrl: string;
  rating: number;
  cawpileScores: {
    characters: number;
    atmosphere: number;
    writing: number;
    plot: number;
    intrigue: number;
    logic: number;
    enjoyment: number;
  };
}

// Bad: Vague types, everything optional, not exported
interface Request {
  month?: any;
  year?: any;
  data?: any[];
}
```
