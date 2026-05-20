---
name: 'Zod Schema Management'
description: 'Create and modify Zod schemas for runtime validation with proper type inference.'
---

1. **Define schemas with specificity**: Prefer concrete schema methods over loose ones.
   - Use `z.string().min(1)` instead of bare `z.string()` for required non-empty strings
   - Use `z.number().int().nonnegative()` instead of bare `z.number()` when appropriate
   - Use `z.enum()` for known string unions
   - Use `z.literal()` for exact values

2. **Derive types from schemas**: Always use `z.infer<typeof Schema>` to derive TypeScript types from Zod schemas. Do not define the type separately and the schema separately — the schema is the source of truth.

   ```typescript
   const MySchema = z.object({
     name: z.string().min(1),
     count: z.number().int().nonnegative(),
   });
   type My = z.infer<typeof MySchema>;
   ```

3. **Choose the right parse method**:
   - `.safeParse()` for external or untrusted input (API payloads, user input, parsed documents) — check `.success` before using `.data`
   - `.parse()` for internal guaranteed data where a thrown error indicates a programming bug

4. **Colocate schema with type**: Place the Zod schema in the same file as the type it defines. Export both the schema and the inferred type.

5. **Test stubs**: Use `zocker` with `createStubFromSchema()` from `@carrot-fndn/shared/testing` to generate test data from schemas. This ensures stubs always match the schema definition.

6. **Schema composition**: Use `.extend()`, `.merge()`, `.pick()`, `.omit()`, and `.partial()` to compose schemas from existing ones rather than duplicating field definitions.

7. **Optional fields**: Use `z.optional()` or `.optional()` for truly optional fields. Remember that `exactOptionalPropertyTypes` is enabled in tsconfig, so optional fields must be explicitly marked.
