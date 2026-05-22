---
name: schema-validators
description: Define or validate canonical schemas for Pentatonic entities. Every canonical record must validate against schema at runtime.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Schema Validators Skill

## Core Principle

**Every canonical record must validate against schema at runtime.**

---

## ProductRecord Schema

```javascript
import { z } from "zod";

export const ProductRecordSchema = z.object({
  identity: z.object({
    canonical_id: z.string().startsWith("ptc_prod_"),
    source_ids: z.record(z.string()).optional(),
  }),
  schema_version: z.literal("v1"),
  taxonomy: z.object({
    category_path: z.array(z.string()).min(1),
    vertical: z.enum(["fashion", "electronics", "home", "toys", "beauty", "sports"]),
  }),
  attributes: z.object({
    core: z.object({
      brand: z.string(),
      title: z.string(),
      description: z.string().optional(),
    }),
  }),
  value_profile: z.object({
    msrp: z.number().optional(),
    currency: z.string().default("GBP"),
  }).optional(),
  provenance: z.object({
    created_at: z.string().datetime(),
    confidence: z.number().min(0).max(1).optional(),
  }),
});
```

---

## ItemRecord Schema

```javascript
export const ItemRecordSchema = z.object({
  identity: z.object({
    canonical_id: z.string().startsWith("ptc_item_"),
    product_ref: z.string().startsWith("ptc_prod_"),
  }),
  schema_version: z.literal("v1"),
  owner_ref: z.string().startsWith("ptc_part_"),
  item_state: z.object({
    condition: z.object({
      grade: z.enum(["NEW", "LIKE_NEW", "EXCELLENT", "GOOD", "FAIR", "POOR"]),
      score: z.number().min(1).max(10).optional(),
    }),
  }),
  value_profile: z.object({
    estimated_value: z.number(),
    confidence: z.number().min(0).max(1),
  }),
});
```

---

## Validation Function

```javascript
export function validateRecord(entityType, record) {
  const schemas = { product: ProductRecordSchema, item: ItemRecordSchema };
  const schema = schemas[entityType];

  const result = schema.safeParse(record);

  if (result.success) {
    return { valid: true, data: result.data };
  }

  return {
    valid: false,
    errors: result.error.issues.map(issue => ({
      path: issue.path.join("."),
      message: issue.message,
    })),
  };
}
```

---

## API Usage

```javascript
export async function onRequestPost(context) {
  const body = await context.request.json();
  const validation = validateRecord("product", body);

  if (!validation.valid) {
    return Response.json({
      success: false,
      error: { code: "SCHEMA_VALIDATION_ERROR", errors: validation.errors },
    }, { status: 400 });
  }

  // Use validation.data (typed and validated)
}
```

---

## AI Output Validation

```javascript
async function enrichProduct(imageUrl, env) {
  const aiResponse = await analyzeWithVision(imageUrl);
  const validation = validateRecord("product", aiResponse);

  if (!validation.valid) {
    await emitTESEvent({
      type: "eval.validation_failed",
      payload: { errors: validation.errors, raw: aiResponse },
    }, env);
    return { success: false, errors: validation.errors };
  }

  return { success: true, data: validation.data };
}
```

---

## Anti-Patterns

- No validation on API inputs
- Silent validation failures
- Missing schema_version
- No confidence on AI fields
