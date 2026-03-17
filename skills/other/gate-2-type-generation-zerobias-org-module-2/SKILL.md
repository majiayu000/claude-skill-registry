---
name: gate-2-type-generation
description: Gate 2 validation: TypeScript type generation from OpenAPI spec
---

### Gate 2: Type Generation

**STOP AND CHECK:**
```bash
# Generation must succeed
npm run clean && npm run generate
echo "Exit code: $?"
# Must be 0

# New types must exist
ls generated/api/*.ts | wc -l
# Must show new files

# No inline types
grep "InlineResponse" generated/
# Must return nothing
```

**PROCEED ONLY IF:**
- ✅ Generation command succeeded (exit code 0)
- ✅ New types exist in generated/ directory
- ✅ No InlineResponse or InlineRequestBody types
- ✅ No TypeScript compilation errors

**IF FAILED:** Fix API spec issues before implementing.
