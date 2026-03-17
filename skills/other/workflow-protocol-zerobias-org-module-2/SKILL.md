---
name: workflow-protocol
description: Workflow execution protocol and phase transition rules
---

# 🚨 MANDATORY EXECUTION PROTOCOL

## THE MISSING PIECE - READ FIRST!

When a user requests ANY module work, follow this exact protocol.

## Step 1: UNDERSTAND THE REQUEST

```
User says: "Add operation X to module Y"
           ↓
You MUST:
1. Identify: What module? What operation?
2. Choose workflow: add-operation.md
3. START EXECUTING - Don't just explore!
```

## Step 1.5: CHECK FOR CREDENTIALS (MANDATORY FIRST ACTION)

**🚨 BEFORE doing ANY work, ALWAYS check for credentials:**

**Check multiple common locations:**

```bash
# 1. Check module .env file
ls .env 2>/dev/null && echo "Found .env" || echo "No .env"

# 2. Check module .connectionProfile.json
ls .connectionProfile.json 2>/dev/null && echo "Found .connectionProfile.json" || echo "No .connectionProfile.json"

# 3. Check repository root .env (go up to find it)
ls ../../.env 2>/dev/null && echo "Found root .env" || echo "No root .env"

# 4. Check for credentials in any found files
if [ -f .env ]; then
  cat .env | grep -iE "(MODULE|SERVICE|VENDOR)_(API_?KEY|TOKEN|PASSWORD|SECRET|EMAIL)"
fi

if [ -f .connectionProfile.json ]; then
  cat .connectionProfile.json | jq '.' 2>/dev/null
fi
```

**Credential location flexibility:**
- Credentials can be in **module/.env**, **module/.connectionProfile.json**, **root .env**, or other locations
- Try common locations first: `.env`, `.connectionProfile.json`, `../.env`, `../../.env`
- Look for patterns: `*_API_KEY`, `*_TOKEN`, `*_PASSWORD`, `*_SECRET`, `*_EMAIL`
- **If unsure where credentials are**, ASK the user:
  ```
  🔍 Checking for credentials...

  I found these files but I'm not sure which contains credentials:
  - [list of found files]

  Where should I look for credentials for [Module Name]?
  Or provide the credential location/values.
  ```

**Note on credential naming:**
- Credential names may vary (e.g., `GITHUB_TOKEN` vs `GITHUB_API_KEY` vs `GITHUB_ACCESS_TOKEN`)
- Try to identify credentials intelligently by looking for common patterns
- Check for vendor/service name + credential type variations
- If multiple similar names exist, ask user which one to use

**IF credentials are NOT available:**
1. **STOP immediately** - Do not proceed with ANY work
2. **ASK the user** what to do:
   ```
   ⚠️ Credentials not found in .env file.

   Required credentials for [Module Name]:
   - CREDENTIAL_VAR_1: [description]
   - CREDENTIAL_VAR_2: [description]

   What would you like to do?
   1. Provide credentials now (I'll wait)
   2. Continue without credentials (integration tests will be skipped)
   ```
3. **WAIT for explicit user response** - Do NOT assume or proceed automatically
4. **ONLY continue** if user explicitly says to proceed without credentials

**IF credentials ARE available:**
- Note them for later use in integration tests
- Proceed to Step 2

**Rationale**: Many tasks require credentials for testing. Checking early prevents wasted work and ensures user controls the execution approach.

## Step 2: LOAD REQUIRED RULES

**🚨 CRITICAL: Re-read rules at the start of EVERY new step/task!**

**BEFORE starting work, load these files:**

### For API Specification Work:
- `api-spec-core-rules.md` - Core API rules (Rules 1-10)
- `api-spec-operations.md` - Operation patterns (Rules 11-13)
- `api-spec-schemas.md` - Schema design (Rules 14-24)
- `api-spec-standards.md` - Standards & guidelines
- `gate-1-api-spec.md` - Gate 1 validation

### For Implementation Work:
- `implementation.md` - Implementation patterns
- `error-handling.md` - Error types
- `type-mapping.md` - Type conversions
- `gate-3-implementation.md` - Gate 3 validation

### For Testing Work:
- `testing.md` - Test requirements
- `gate-4-test-creation.md` - Gate 4 validation
- `gate-5-test-execution.md` - Gate 5 validation

### Always Read:
- `prerequisites.md` - Before any work

## Step 3: CRITICAL EXECUTION SEQUENCE

For ANY operation addition:

```bash
# 1. Update API specification
edit api.yml
→ VALIDATE: No errors, correct naming, descriptions added

# 2. IMMEDIATELY generate types (NEVER SKIP!)
npm run clean && npm run generate
→ VALIDATE: Types generated successfully

# 3. Check what was generated
ls generated/api/
cat generated/model/NewType.ts

# 4. ONLY THEN implement using generated types
edit src/SomeProducer.ts  # Use the generated types!
→ VALIDATE: No 'any' types, using generated types

# 5. WRITE TESTS (MANDATORY!)
edit test/SomeProducerTest.ts  # Unit tests
edit test/integration/SomeIntegrationTest.ts  # Integration tests
→ VALIDATE: Tests complete for operation

# 6. RUN TESTS (MANDATORY!)
npm test
→ VALIDATE: All tests pass

# 7. Build and validate
npm run build
→ VALIDATE: Build successful
```

**DO NOT STOP UNTIL ALL 7 STEPS COMPLETE!**

## Step 4: VALIDATION GATES

**See `gate-1-api-spec.md` through `gate-6-build.md` for complete gate definitions.**

All operations must pass through 6 validation gates sequentially:
1. API Specification ✓
2. Type Generation ✓
3. Implementation ✓
4. Test Creation ✓
5. Test Execution ✓
6. Build ✓

**Task is ONLY complete when ALL gates pass.**

## Step 5: COMMON FAILURES AND FIXES

### Failure: "I added 401, 403, 500 responses"
**Fix**: Remove them! Only 200/201 allowed

### Failure: "I used `any` type in method signature"
**Fix**: Run `npm run clean && npm run generate` first, use generated types

### Failure: "I implemented before generating"
**Fix**: ALWAYS: api.yml → generate → implement

### Failure: "Rules were ignored"
**Fix**: Check rules DURING execution, not after

## THE EXECUTION MANTRA

```
1. Read request
2. CHECK FOR CREDENTIALS - Ask user if missing
3. Load required rules (see Step 2)
4. Open workflow task
5. Execute step by step with validation gates
6. RE-READ RULES before each new step
7. Generate before implement
8. Write tests WITHOUT being asked
9. Run tests and build
```

## EXAMPLE EXECUTION

User: "Add getAccessToken operation"

```typescript
// ❌ WRONG - Jumping straight to implementation
async getAccessToken(): Promise<any> { // NO!

// ✅ CORRECT - Follow protocol
// 1. Update api.yml with operation
// 2. Run npm run clean && npm run generate
// 3. Import AccessToken from generated
// 4. Implement with proper type
async getAccessToken(): Promise<AccessToken> { // YES!
// 5. Write tests (unit + integration)
// 6. Run tests - verify all pass
// 7. Build - verify success
```

## WORKFLOW TASK MAPPING

| User Says | Use This Task |
|-----------|--------------|
| "Analyze X API" or "Create API diagram" | `workflow/tasks/analyze-api.md` |
| "Create X module" | `workflow/tasks/create-module.md` |
| "Add X operation" | `workflow/tasks/add-operation.md` |
| "Add X operations" (multiple) | `workflow/tasks/update-module.md` |
| "Fix X issue" | `workflow/tasks/fix-module.md` |

## FINAL CHECKLIST

Before ANY implementation:
- [ ] **Checked for credentials first** - Asked user if not found
- [ ] **Got explicit user permission** to proceed (if no credentials)
- [ ] Identified the correct workflow task
- [ ] Loaded required rule files (Step 2)
- [ ] Re-reading rules before EACH new step
- [ ] Created TodoWrite with ALL steps
- [ ] Updated api.yml first
- [ ] Ran npm run clean && npm run generate
- [ ] Using generated types (not any)
- [ ] Checking rules during execution
- [ ] Not adding error responses
- [ ] Writing tests WITHOUT being asked
- [ ] All validation gates passed

## Remember

**The workflow and rules only work if you EXECUTE them, not just READ them!**

When user says "add operation":
1. **Check for credentials FIRST** - Ask user if missing
2. Load rules: `api-specification.md`, `implementation.md`, `testing.md`, `ENFORCEMENT.md`
3. Create TodoWrite with 7 steps
4. Execute sequentially with validation at each gate
5. Write tests automatically
6. Complete only when all gates pass

**STOP EXPLORING - START EXECUTING!**

For complete enforcement details, see `completion-checklist.md`.
