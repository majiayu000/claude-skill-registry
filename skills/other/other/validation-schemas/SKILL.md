---
name: validation-schemas
description: Enforces project Zod validation schema conventions when creating or modifying validation schemas. This skill ensures consistent patterns for drizzle-zod integration, custom zod utilities, schema composition, type exports, and form/action integration.
---

# Validation Schemas Skill

## Purpose

This skill enforces the project Zod validation schema conventions automatically during schema development. It ensures consistent patterns for:

- Drizzle-zod schema generation from database tables
- Custom zod utility functions for common patterns
- Schema composition and extension for actions
- Type exports for both input and output types
- Form integration with TanStack Form
- Server action validation patterns

## Activation

This skill activates when:

- Creating new validation files in `src/lib/validations/`
- Modifying existing validation schemas
- Working with drizzle-zod schema generation
- Defining input/output types for server actions
- Creating form validators for TanStack Form
- Working with zod utility functions in `src/lib/utils/zod.utils.ts`

## Workflow

1. Detect validation work (file path contains `validations/` or imports from `zod` or `drizzle-zod`)
2. Load `references/Validation-Schemas-Conventions.md`
3. Generate/modify code following all conventions
4. Use custom zod utilities (`zodMinMaxString`, `zodMaxString`, etc.) instead of raw zod chains
5. Export both input types (`z.input`) and output types (`z.infer`) for form schemas
6. Scan for violations of schema patterns
7. Auto-fix all violations (no permission needed)
8. Report fixes applied

## Key Patterns

### Schema Generation

- Use `createSelectSchema` and `createInsertSchema` from drizzle-zod
- Apply custom zod utilities for field validation (not raw zod chains)
- Omit auto-generated fields (id, createdAt, updatedAt, userId)
- Create public schemas by omitting sensitive fields

### Custom Zod Utilities

Use utilities from `@/lib/utils/zod.utils`:

- `zodMinMaxString` - Required strings with min/max length
- `zodMaxString` - Optional/required strings with max length
- `zodMinString` - Required strings with min length
- `zodDateString` - Date string parsing with nullable option
- `zodDecimal` - Decimal number parsing from strings
- `zodYear` - 4-digit year validation
- `zodNullableUUID` - Optional UUID with null default
- `zodInteger` - Integer parsing from strings

### Type Exports

- Export `z.infer<typeof schema>` for output types (after transforms)
- Export `z.input<typeof schema>` for input types (before transforms, for forms)
- Use naming: `Insert{Entity}`, `Select{Entity}`, `Update{Entity}`, `Public{Entity}`
- Use naming: `Insert{Entity}Input`, `Update{Entity}Input` for form input types

### Form Integration

- Schemas work with TanStack Form via `validators: { onSubmit: schema }`
- Input types match form field values before zod transforms
- Output types match validated data after transforms

### Action Integration

- Actions use `schema.parse(ctx.sanitizedInput)` for validation
- Extend base schemas with `.extend()` for action-specific fields
- Use `z.uuid()` for ID parameters in action schemas

## References

- `references/Validation-Schemas-Conventions.md` - Complete validation schema conventions
