---
name: build-standards
description: Build quality standards, validation checkpoints, and compilation requirements
---

# Build and Quality Rules

## 🚨 CRITICAL RULES (Immediate Failure)

### 1. Build Must Pass
- `npm run build` MUST exit with code 0
- Build failures STOP all work immediately
- Fix ALL compilation errors before proceeding
- No implementation with broken build

### 2. Lint Compliance
- `npm run lint` MUST pass without errors
- Lint failures require immediate fix
- No proceeding with lint errors

### 3. Clean Git State for Updates
- NO uncommitted changes before starting updates
- Git status must be clean
- User must commit or stash before proceeding

## 🟡 STANDARD RULES

### Mandatory Build Gate Checkpoints
Build MUST pass with exit code 0 after EACH of these steps:

1. **Pre-Implementation Validation** (MANDATORY)
   - Add `"skipLibCheck": true` to tsconfig.json
   - Run `npm run build` - MUST exit with code 0
   - Fix ALL compilation errors before proceeding

2. **Post-Dependency Install**
   - After `npm install` for new dependencies
   - Verify build still passes

3. **Post-HTTP Client Creation**
   - After creating `src/{ServiceName}Client.ts`
   - Build must pass before continuing

4. **Post-Mappers Creation**
   - After creating `src/Mappers.ts`
   - Build must pass before continuing

5. **Post-Producer Implementation** (Each)
   - After EACH producer implementation
   - Build must pass after every producer

6. **Post-Connector Implementation**
   - After main connector class
   - Build must pass before continuing

7. **Post-Entry Point Update**
   - After updating `src/index.ts`
   - Build must pass before continuing

8. **FINAL BUILD GATE** (Task Completion)
   - **ABSOLUTE REQUIREMENT**: `npm run build` exits with code 0
   - Task CANNOT be completed if build fails
   - Zero TypeScript warnings allowed
   - Zero compilation errors allowed

**CRITICAL**: If `npm run build` fails at ANY checkpoint, STOP all work immediately.

### TypeScript Configuration
```json
{
  "compilerOptions": {
    "skipLibCheck": true,  // MANDATORY - Add before implementation
    "strict": true,         // Maintain strict checking
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

### Package.json Scripts
Required scripts that must exist and work:
- `build`: Compile TypeScript
- `clean`: Remove build artifacts
- `lint`: Check code style
- `test`: Run unit tests
- `test:integration`: Run integration tests

### Dependency Installation
- Install exact versions when specified
- Run `npm install` after adding dependencies
- Verify no peer dependency warnings
- Check for security vulnerabilities

### Code Generation Rules
- NEVER modify files in `generated/` directory
- Generated files are read-only
- Failed generation triggers API spec fix
- Regenerate after any API spec changes

## 🟢 GUIDELINES

### Performance Considerations
- Avoid synchronous file operations
- Use async/await properly
- Implement appropriate timeouts
- Handle large datasets efficiently

### Memory Management
- Clean up resources in disconnect methods
- Avoid memory leaks in long-running operations
- Use streaming for large responses when possible

### Error Recovery
- Implement proper cleanup on errors
- Don't leave partial state
- Log errors appropriately
- Provide meaningful error messages

### Code Quality Metrics
- Maintain consistent code style
- Follow existing patterns
- Keep functions focused and small
- Avoid deep nesting

### Validation Sequence
```bash
# Standard validation sequence
npm run clean
npm run build
npm run lint
npm run test
npm run test:integration  # If credentials available
```

## 📝 EXCEPTIONS LOG

### When Build Can Fail Temporarily
- During iterative development (but must fix before commit)
- When updating dependencies (fix immediately after)
- Never leave build broken between tasks

### Lint Exception Handling
- Use inline disable comments sparingly
- Document reason for disabling:
```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any
// Reason: External API returns untyped response
```

## Type Generation Validation (Gate 2)

### Step 1: Run Generation

```bash
# Clean previous generation
rm -rf generated/

# Run generator
npm run clean && npm run generate

# Capture exit code
EXIT_CODE=$?
echo "Exit code: $EXIT_CODE"

# Exit code MUST be 0
if [ $EXIT_CODE -ne 0 ]; then
  echo "❌ Gate 2 FAILED: Generation failed"
  exit 1
fi
```

### Step 2: Validate Generated Files

```bash
# Check generated directory exists
if [ ! -d "generated" ]; then
  echo "❌ Gate 2 FAILED: No generated directory"
  exit 1
fi

# List generated files
ls -la generated/api/
ls -la generated/model/

# Count generated files
FILE_COUNT=$(find generated -name "*.ts" | wc -l)
echo "Generated $FILE_COUNT TypeScript files"

# Must have at least some files
if [ $FILE_COUNT -eq 0 ]; then
  echo "❌ Gate 2 FAILED: No files generated"
  exit 1
fi
```

### Step 3: Check for InlineResponse Types

```bash
# InlineResponse indicates inline schemas (bad)
if grep -r "InlineResponse\|InlineRequestBody" generated/; then
  echo "❌ Gate 2 FAILED: Inline types found"
  echo "Fix: Move inline schemas to components/schemas in api.yml"
  exit 1
fi
```

**Why this matters:** InlineResponse types indicate inline schemas in api.yml. All schemas must be named and in components/schemas.

### Step 4: Validate TypeScript Compilation After Generation

```bash
# Try to compile generated code
npm run build

# Check exit code
if [ $? -ne 0 ]; then
  echo "❌ Gate 2 FAILED: TypeScript compilation errors"
  echo "Check generated types for issues"
  exit 1
fi
```

## Build Validation (Gate 6)

### Step 1: Clean Build

```bash
# Clean previous build
rm -rf dist/

# Run build
npm run build

# Capture exit code
EXIT_CODE=$?
echo "Build exit code: $EXIT_CODE"

# MUST be 0
if [ $EXIT_CODE -ne 0 ]; then
  echo "❌ Gate 6 FAILED: Build failed"
  exit 1
fi
```

### Step 2: Validate Artifacts

```bash
# Distribution directory must exist
if [ ! -d "dist" ]; then
  echo "❌ Gate 6 FAILED: No dist directory"
  exit 1
fi

# Count artifacts
FILE_COUNT=$(find dist -name "*.js" | wc -l)
echo "Generated $FILE_COUNT JavaScript files"

# Must have files
if [ $FILE_COUNT -eq 0 ]; then
  echo "❌ Gate 6 FAILED: No compiled files"
  exit 1
fi

# Check for index files
if [ ! -f "dist/index.js" ]; then
  echo "❌ Gate 6 FAILED: No dist/index.js"
  exit 1
fi
```

### Step 3: Dependency Locking

```bash
# Run shrinkwrap
npm run shrinkwrap

# Capture exit code
EXIT_CODE=$?
echo "Shrinkwrap exit code: $EXIT_CODE"

# MUST be 0
if [ $EXIT_CODE -ne 0 ]; then
  echo "❌ Gate 6 FAILED: Shrinkwrap failed"
  exit 1
fi

# Verify shrinkwrap file exists
if [ ! -f "npm-shrinkwrap.json" ]; then
  echo "❌ Gate 6 FAILED: npm-shrinkwrap.json not created"
  exit 1
fi
```

### Step 4: Type Check (if separate)

```bash
# Run type check separately if configured
npm run type-check 2>&1

# Should show no errors
if [ $? -ne 0 ]; then
  echo "⚠️  Type check failed"
fi
```

## Common Build Failures & Fixes

### Failure: TypeScript Errors

**Error:** Property 'x' does not exist on type 'Y'

**Fix:** Check type definitions
1. Ensure using generated types
2. Verify mapper returns correct type
3. Check method signatures

### Failure: Missing Imports

**Error:** Cannot find module 'X'

**Fix:** Check imports
1. Verify relative paths correct
2. Ensure generated types imported
3. Check package dependencies

### Failure: Shrinkwrap Failed

**Error:** npm ERR! shrinkwrap failed

**Fix:** Check npm state
1. Ensure node_modules clean
2. Run npm install
3. Retry shrinkwrap

### Failure: InlineResponse Types

**Error:** Found InlineResponse200, InlineResponse201

**Cause:** Inline schema in api.yml

```yaml
# ❌ WRONG - Inline schema
responses:
  '200':
    content:
      application/json:
        schema:
          type: object  # Inline schema
          properties: ...
```

**Fix:** Move to components/schemas

```yaml
# ✅ CORRECT - Reference named schema
responses:
  '200':
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/Webhook'
```

### Failure: Generation Error

**Error:** "Could not resolve reference"

**Cause:** Invalid $ref in api.yml

```yaml
# ❌ WRONG
$ref: '#/components/schemas/NonExistent'
```

**Fix:** Ensure referenced schema exists

```yaml
# ✅ CORRECT
components:
  schemas:
    NonExistent:
      type: object
```

## Gate Validation Criteria

### Gate 2 Criteria (Type Generation) - MUST ALL PASS

- [ ] `npm run clean && npm run generate` exit code is 0
- [ ] Generated directory exists with TypeScript files
- [ ] No InlineResponse or InlineRequestBody types
- [ ] At least one API interface generated
- [ ] At least one model type generated
- [ ] `npm run build` succeeds with no errors
- [ ] Generated types match API specification

### Gate 6 Criteria (Final Build) - MUST ALL PASS

- [ ] `npm run build` exit code is 0
- [ ] No TypeScript compilation errors
- [ ] No linting errors
- [ ] dist/ directory created
- [ ] JavaScript files in dist/
- [ ] Type declaration files (.d.ts) in dist/
- [ ] `npm run shrinkwrap` exit code is 0
- [ ] npm-shrinkwrap.json file exists
- [ ] All imports resolve correctly

**All criteria MUST pass to proceed/complete task**
