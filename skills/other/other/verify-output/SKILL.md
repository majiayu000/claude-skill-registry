---
name: verify-output
description: Pattern for verifying your output matches required schema before completing. Use before writing final output to ensure validity.
allowed-tools: Read, Bash
---

# Verify Output Skill

Pattern for ensuring outputs match required schemas using automated validation.

## When to Use

- Before writing final output file
- After completing a task
- When producing structured JSON output

## Quick Reference

**Validate before writing:**
```bash
./scripts/validate.sh <schema_name> <file_path>
```

## Available Schemas

| Schema | Used By | Output Path |
|--------|---------|-------------|
| `demand` | PM | `memory/reports/demand.json` |
| `design` | Architect | `memory/reports/designs/*.json` |
| `task-output` | Implementer | `memory/tasks/*/output.json` |
| `verification` | Verifier | `memory/tasks/*/verification.json` |
| `reflection` | Reflector | `memory/reflections/*.json` |
| `evolution-proposal` | Evolver | `memory/evolution/*.json` |
| `contract` | Executor | `memory/contracts/*.json` |

## Validation Process

### Step 1: Determine Your Schema

Based on your agent role:
```
PM agent          → demand.schema.json
Architect agent   → design.schema.json
Implementer agent → task-output.schema.json
Verifier agent    → verification.schema.json
Reflector agent   → reflection.schema.json
Evolver agent     → evolution-proposal.schema.json
```

### Step 2: Write Output to Temp Location

```bash
Write(memory/tasks/{id}/output.json.tmp, content)
```

### Step 3: Validate

```bash
./scripts/validate.sh task-output memory/tasks/{id}/output.json.tmp
```

### Step 4: If Valid, Move to Final Location

```bash
mv memory/tasks/{id}/output.json.tmp memory/tasks/{id}/output.json
```

### Step 5: If Invalid, Fix and Retry

Common validation errors and fixes:

| Error | Fix |
|-------|-----|
| `'X' is a required property` | Add the missing field |
| `'Y' is not one of ['a', 'b']` | Use valid enum value |
| `'Z' is not of type 'array'` | Wrap value in array: `[value]` |
| `Additional properties not allowed` | Remove extra fields |

## Output Format: Compact JSON

All agent outputs MUST be compact JSON (single line, no extra whitespace):

```json
{"task_id":"001","status":"pre_complete","knowledge_updates":[],"reflection":{"what_worked":[],"what_failed":[],"patterns_noticed":[]}}
```

## Mandatory Fields (All Agents)

Every output MUST include:

```json
{"knowledge_updates":[{"category":"codebase","content":"string","confidence":"certain"}],"reflection":{"what_worked":["string"],"what_failed":["string"],"patterns_noticed":["string"]}}
```

Or empty arrays if no updates:
```json
{"knowledge_updates":[],"reflection":{"what_worked":[],"what_failed":[],"patterns_noticed":[]}}
```

Valid values:
- `category`: `"codebase"` | `"convention"` | `"decision"` | `"gotcha"`
- `confidence`: `"certain"` | `"likely"` | `"uncertain"`

## Pre-Write Validation Pattern

Recommended pattern for agents:

```
1. Construct output object in memory
2. Write to {output_path}.tmp
3. Run: ./scripts/validate.sh {schema} {output_path}.tmp
4. IF validation passes:
     → mv {output_path}.tmp {output_path}
     → Log: "Output validated and written"
5. ELSE:
     → Read validation errors
     → Fix output object
     → Retry from step 2
     → Max 3 retries, then report validation failure
```

## Common Mistakes

- Forgetting `knowledge_updates` (even if empty array)
- Forgetting `reflection` fields
- Using invalid enum values (check schema for allowed values)
- Missing required nested fields
- Wrong type (string instead of array, etc.)
- Using YAML instead of JSON
- Pretty-printing JSON (use compact format)

## Principles

1. **Validate before write** - Never output invalid data
2. **Schema is law** - Missing fields = rejection by executor
3. **Empty is valid** - `"knowledge_updates":[]` is okay
4. **Fail fast** - Catch errors before they propagate
5. **Compact JSON** - Single line, no formatting
