---
name: regenerate-types
description: Type regeneration workflow - when and how to run npm run clean description: Type regeneration workflow - when and how to run npm run clean && npm run generatedescription: Type regeneration workflow - when and how to run npm run clean && npm run generate npm run generate
---

# API Specification Regeneration Rule

**CRITICAL**: After ANY changes to api.yml, TypeScript interfaces MUST be regenerated before proceeding to implementation.

## The Rule

**After completing api.yml changes (before moving to code work), ALWAYS run:**

```bash
npm run clean && npm run generate
```

## Why Both Commands?

1. **`npm run clean`** - Removes leftover generated files that might cause conflicts
2. **`npm run generate`** - Generates fresh TypeScript interfaces from api.yml

**WHY**: Without clean, old generated files may remain and cause:
- Type conflicts
- Import errors
- Stale interfaces that don't match current api.yml

## When to Run

### ✅ MUST Run

1. **After api.yml edits** - Before implementing operations
2. **After schema changes** - Before writing mappers
3. **After parameter changes** - Before updating client code
4. **After operation additions** - Before creating producer methods
5. **Before Gate 2 validation** - To validate types generate correctly

### ❌ Don't Need to Run

- During active api.yml editing (only after final change)
- If you're just reading api.yml
- During planning phase (before any code work)

## Multiple api.yml Changes

If making multiple changes to api.yml:

```bash
# Edit api.yml multiple times
# ... change 1 ...
# ... change 2 ...
# ... change 3 ...

# THEN run generation ONCE after all changes complete
npm run clean && npm run generate
```

**Don't regenerate after each individual change - only after the last change before moving to implementation.**

## In Workflows

### Standard Pattern in All Workflows

Whenever a workflow mentions type generation or working with generated types:

```bash
# ✅ CORRECT - Always use clean + generate
npm run clean && npm run generate

# ❌ WRONG - Missing clean
npm run generate
```

### Gate 2: Type Generation

Gate 2 specifically validates that types generate correctly:

```bash
# Gate 2 validation
npm run clean && npm run generate

# Check for errors
echo $?  # Should be 0 (success)
```

If generation fails, api.yml has errors that must be fixed before proceeding.

## Error Handling

If `npm run clean && npm run generate` fails:

1. **Read the error message** - TypeScript/OpenAPI errors point to specific issues
2. **Fix api.yml** - Address the schema/type error indicated
3. **Run again** - `npm run clean && npm run generate`
4. **Repeat** until successful

Common errors:
- Missing required fields
- Invalid $ref references
- Circular dependencies
- Invalid OpenAPI syntax

## Validation After Generation

After successful generation, check:

```bash
# 1. Generation succeeded
npm run clean && npm run generate
echo $?  # Should be 0

# 2. Check generated files exist
ls -la src/gen/

# 3. Look for type errors in project
npm run build  # Should compile without errors
```

## In Agent Instructions

Agents working on api.yml or implementation should:

1. **Complete api.yml changes**
2. **Run**: `npm run clean && npm run generate`
3. **Verify**: Check exit code and generated files
4. **Proceed**: Only if generation successful

## Example Workflow

```bash
# 1. Make api.yml changes
# ... edit api.yml ...

# 2. Regenerate types (with clean)
npm run clean && npm run generate

# 3. Verify successful
if [ $? -eq 0 ]; then
  echo "✅ Types generated successfully"
  # Proceed to implementation
else
  echo "❌ Generation failed - fix api.yml"
  # Fix errors and retry
fi
```

## References

- Gate 2 Validation: @.claude/rules/gate-2-type-generation.md
- API Spec Rules: @.claude/rules/api-specification-critical-12-rules.md
- Build Validation: @.claude/rules/gate-6-build.md

---

**REMEMBER**: `npm run clean && npm run generate` not just `npm run generate` - clean prevents leftover conflicts.
