---
name: typescript-configuration
description: TypeScript configuration standards and tsconfig.json patterns
---

# TypeScript Configuration Patterns

## 🚨 CRITICAL RULES

### 1. Use Standard Configuration
Every module MUST use the standard tsconfig.json configuration.

**Standard tsconfig.json:**
```json
{
  "compilerOptions": {
    "module": "commonjs",
    "noImplicitAny": false,
    "target": "ES5",
    "strict": true,
    "moduleResolution": "node",
    "removeComments": true,
    "sourceMap": true,
    "noLib": false,
    "allowJs": true,
    "declaration": true,
    "lib": ["es6", "es5"],
    "outDir": "dist",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "typeRoots": [
      "node_modules/@types"
    ]
  },
  "include": [
    "src/**/*",
    "test/**/*",
    "generated/**/*"
  ],
  "exclude": [
    "dist",
    "node_modules"
  ]
}
```

### 2. NEVER Modify Without Strong Justification
- tsconfig.json is scaffolded by generator
- Only modify if absolutely necessary for build or compatibility
- Document ALL changes with comments explaining why
- Get approval before changing core settings

### 3. Critical Settings (MUST be present)
These settings are REQUIRED and should NOT be changed:

```json
{
  "compilerOptions": {
    "strict": true,              // Enable all strict type checking
    "declaration": true,         // Generate .d.ts files
    "skipLibCheck": true,        // Skip type checking of node_modules
    "esModuleInterop": true,     // Enable CommonJS/ES module interop
    "moduleResolution": "node"   // Use Node.js module resolution
  }
}
```

## 🟡 STANDARD RULES

### Compiler Options Explained

#### Module System
```json
{
  "module": "commonjs",           // Output CommonJS modules (required for Node.js)
  "target": "ES5",                // Compile to ES5 for broad compatibility
  "lib": ["es6", "es5"],          // Include ES5 and ES6 library definitions
  "esModuleInterop": true,        // Enable import/export interop with CommonJS
  "allowSyntheticDefaultImports": true  // Allow default imports from modules with no default export
}
```

**Why:**
- Node.js ecosystem primarily uses CommonJS
- ES5 target ensures compatibility with older Node versions
- esModuleInterop allows clean imports from CommonJS modules

#### Type Checking
```json
{
  "strict": true,                 // Enable all strict type checking options
  "noImplicitAny": false,         // Allow implicit any (relaxed for generated code)
  "skipLibCheck": true            // Skip checking .d.ts files in node_modules
}
```

**Why:**
- `strict: true` catches most type errors
- `noImplicitAny: false` allows flexibility with generated/dynamic code
- `skipLibCheck: true` dramatically improves build performance without sacrificing safety

#### Output Configuration
```json
{
  "outDir": "dist",               // Output compiled files to dist/
  "declaration": true,            // Generate .d.ts type declaration files
  "sourceMap": true,              // Generate .map files for debugging
  "removeComments": true          // Strip comments from output
}
```

**Why:**
- Separate source (`src/`) from output (`dist/`)
- Declaration files enable TypeScript consumers to get type information
- Source maps enable debugging with original TypeScript code
- Removing comments reduces bundle size

#### Module Resolution
```json
{
  "moduleResolution": "node",     // Use Node.js-style module resolution
  "typeRoots": ["node_modules/@types"],  // Where to find type definitions
  "allowJs": true,                // Allow importing .js files
  "noLib": false                  // Include default library (lib.d.ts)
}
```

**Why:**
- Node.js resolution matches runtime behavior
- Allows importing JavaScript files if needed
- typeRoots ensures @types packages are found

### Include/Exclude Patterns

#### Standard Include
```json
{
  "include": [
    "src/**/*",       // All source files
    "test/**/*",      // All test files
    "generated/**/*"  // All generated files (from OpenAPI, etc.)
  ]
}
```

**Why:**
- Explicitly list directories to compile
- Ensures generated code is type-checked
- Test files are included for IDE support

#### Standard Exclude
```json
{
  "exclude": [
    "dist",           // Don't compile output directory
    "node_modules"    // Don't compile dependencies
  ]
}
```

**Why:**
- Prevent circular compilation
- Improve build performance
- Avoid duplicate module errors

### When to Modify tsconfig.json

**Valid Reasons:**
1. **New TypeScript version** - Upgrade requires new compiler options
2. **Special library compatibility** - Third-party library needs specific setting
3. **Build errors** - Compiler option causes build failures that can't be fixed otherwise
4. **Performance issues** - Specific optimization needed

**INVALID Reasons:**
1. ❌ "I prefer different settings"
2. ❌ "It works on my machine"
3. ❌ "Other projects do it differently"
4. ❌ Trying to bypass type errors (fix the errors instead!)

### Modification Process

If you MUST modify tsconfig.json:

1. **Document the change:**
```json
{
  "compilerOptions": {
    // CUSTOM: Added resolveJsonModule to import JSON files
    // Reason: api-metadata.json needs to be imported at build time
    // Date: 2024-10-15
    // Approved by: Team Lead
    "resolveJsonModule": true
  }
}
```

2. **Test thoroughly:**
```bash
# Clean build
rm -rf dist
npm run build

# Run tests
npm test

# Check generated types
ls dist/*.d.ts
```

3. **Update documentation:**
- Add comment in tsconfig.json
- Document in module README if significant
- Note in PR description

## 🟢 GUIDELINES

### Path Mapping (Generally Avoid)

**Only use path mapping if absolutely necessary:**

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@generated/*": ["generated/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

**Why to avoid:**
- Adds complexity
- Relative imports are clearer
- Path mapping can cause issues with bundlers
- Makes code less portable

**When it's acceptable:**
- Large codebase with deep nesting
- Shared utilities across many modules
- Generated code in separate directory

**If you use paths, also configure:**
- jest.config.js (moduleNameMapper)
- package.json (for tools that don't respect tsconfig paths)

### Advanced Compiler Options

**Options you might add (with justification):**

```json
{
  "compilerOptions": {
    // Import JSON files directly
    "resolveJsonModule": true,  // Only if you need to import .json as modules

    // Decorator support
    "experimentalDecorators": true,  // Only if using decorators
    "emitDecoratorMetadata": true,   // Only with decorators + reflection

    // Incremental builds
    "incremental": true,  // Faster rebuilds (creates .tsbuildinfo)
    "tsBuildInfoFile": ".tsbuildinfo",  // Location of build cache

    // Strict null checks (already in strict: true, but can be disabled)
    "strictNullChecks": false,  // ONLY if absolutely necessary (not recommended)

    // Import helpers
    "importHelpers": true,  // Import tslib helpers (reduces bundle size)

    // Force consistent casing
    "forceConsistentCasingInFileNames": true  // Catch casing errors early
  }
}
```

### CommonJS vs ES Modules

**Current standard: CommonJS**
```json
{
  "compilerOptions": {
    "module": "commonjs"
  }
}
```

**If moving to ES Modules (future):**
```json
{
  "compilerOptions": {
    "module": "ES2020",
    "target": "ES2020"
  }
}
```

**Also update package.json:**
```json
{
  "type": "module"
}
```

**Note:** ES modules migration is a breaking change requiring updates to:
- All imports/exports
- Jest configuration
- File extensions (.mjs)
- Runtime environment

### Multiple tsconfig Files

For complex projects, you might have multiple configs:

**tsconfig.json** (main)
```json
{
  "extends": "./tsconfig.base.json",
  "compilerOptions": {
    "outDir": "dist"
  },
  "include": ["src/**/*"]
}
```

**tsconfig.test.json** (tests)
```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "outDir": "dist-test"
  },
  "include": ["test/**/*", "src/**/*"]
}
```

**tsconfig.base.json** (shared)
```json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    // ... common options
  }
}
```

**When to use:**
- Different build outputs for src vs test
- Multiple entry points
- Monorepo with shared configuration

## Validation

### Check tsconfig Exists and is Valid JSON
```bash
# Check file exists
if [ -f tsconfig.json ]; then
  echo "✅ PASS: tsconfig.json exists"
else
  echo "❌ FAIL: tsconfig.json missing"
  exit 1
fi

# Validate JSON syntax
if cat tsconfig.json | jq . > /dev/null 2>&1; then
  echo "✅ PASS: Valid JSON"
else
  echo "❌ FAIL: Invalid JSON syntax"
  exit 1
fi
```

### Check Critical Settings
```bash
# Check strict mode
STRICT=$(cat tsconfig.json | jq -r '.compilerOptions.strict')
if [ "$STRICT" = "true" ]; then
  echo "✅ PASS: strict mode enabled"
else
  echo "❌ FAIL: strict mode must be true"
fi

# Check skipLibCheck
SKIP=$(cat tsconfig.json | jq -r '.compilerOptions.skipLibCheck')
if [ "$SKIP" = "true" ]; then
  echo "✅ PASS: skipLibCheck enabled"
else
  echo "⚠️ WARN: skipLibCheck should be true for performance"
fi

# Check declaration files
DECL=$(cat tsconfig.json | jq -r '.compilerOptions.declaration')
if [ "$DECL" = "true" ]; then
  echo "✅ PASS: declaration files enabled"
else
  echo "❌ FAIL: declaration must be true"
fi

# Check module type
MODULE=$(cat tsconfig.json | jq -r '.compilerOptions.module')
if [ "$MODULE" = "commonjs" ]; then
  echo "✅ PASS: module is commonjs"
else
  echo "⚠️ WARN: module is $MODULE (expected commonjs)"
fi
```

### Check Include/Exclude Patterns
```bash
# Check src is included
if cat tsconfig.json | jq -r '.include[]' | grep -q 'src'; then
  echo "✅ PASS: src directory included"
else
  echo "❌ FAIL: src directory must be included"
fi

# Check node_modules is excluded
if cat tsconfig.json | jq -r '.exclude[]' | grep -q 'node_modules'; then
  echo "✅ PASS: node_modules excluded"
else
  echo "⚠️ WARN: Should exclude node_modules"
fi

# Check dist is excluded
if cat tsconfig.json | jq -r '.exclude[]' | grep -q 'dist'; then
  echo "✅ PASS: dist excluded"
else
  echo "⚠️ WARN: Should exclude dist directory"
fi
```

### Test Build with tsconfig
```bash
# Clean build test
echo "Testing build with current tsconfig..."
rm -rf dist
npm run build

if [ $? -eq 0 ]; then
  echo "✅ PASS: Build successful"
else
  echo "❌ FAIL: Build failed"
  exit 1
fi

# Check output files generated
if [ -d dist ]; then
  echo "✅ PASS: dist directory created"
else
  echo "❌ FAIL: No dist directory"
  exit 1
fi

# Check declaration files generated
if ls dist/*.d.ts 1> /dev/null 2>&1; then
  echo "✅ PASS: Type declaration files generated"
else
  echo "❌ FAIL: No .d.ts files generated"
fi
```

### Complete Validation Script
```bash
#!/bin/bash
# validate-tsconfig.sh - Complete tsconfig.json validation

echo "=== TypeScript Configuration Validation ==="
echo ""

# 1. File exists
if [ ! -f tsconfig.json ]; then
  echo "❌ FAIL: tsconfig.json not found"
  exit 1
fi
echo "✅ Found tsconfig.json"
echo ""

# 2. Valid JSON
if ! cat tsconfig.json | jq . > /dev/null 2>&1; then
  echo "❌ FAIL: Invalid JSON"
  exit 1
fi
echo "✅ Valid JSON syntax"
echo ""

# 3. Critical settings
echo "Checking critical settings:"
ERRORS=0

# strict
STRICT=$(jq -r '.compilerOptions.strict' tsconfig.json)
if [ "$STRICT" = "true" ]; then
  echo "  ✅ strict: true"
else
  echo "  ❌ strict: $STRICT (must be true)"
  ERRORS=$((ERRORS + 1))
fi

# declaration
DECL=$(jq -r '.compilerOptions.declaration' tsconfig.json)
if [ "$DECL" = "true" ]; then
  echo "  ✅ declaration: true"
else
  echo "  ❌ declaration: $DECL (must be true)"
  ERRORS=$((ERRORS + 1))
fi

# skipLibCheck
SKIP=$(jq -r '.compilerOptions.skipLibCheck' tsconfig.json)
if [ "$SKIP" = "true" ]; then
  echo "  ✅ skipLibCheck: true"
else
  echo "  ⚠️  skipLibCheck: $SKIP (should be true)"
fi

# esModuleInterop
INTEROP=$(jq -r '.compilerOptions.esModuleInterop' tsconfig.json)
if [ "$INTEROP" = "true" ]; then
  echo "  ✅ esModuleInterop: true"
else
  echo "  ⚠️  esModuleInterop: $INTEROP (should be true)"
fi

# moduleResolution
RESOLUTION=$(jq -r '.compilerOptions.moduleResolution' tsconfig.json)
if [ "$RESOLUTION" = "node" ]; then
  echo "  ✅ moduleResolution: node"
else
  echo "  ⚠️  moduleResolution: $RESOLUTION (should be node)"
fi

echo ""

# 4. Include patterns
echo "Checking include patterns:"
if jq -r '.include[]' tsconfig.json | grep -q 'src'; then
  echo "  ✅ Includes src/"
else
  echo "  ❌ Must include src/"
  ERRORS=$((ERRORS + 1))
fi

if jq -r '.include[]' tsconfig.json | grep -q 'generated'; then
  echo "  ✅ Includes generated/"
else
  echo "  ⚠️  Should include generated/ if present"
fi

echo ""

# 5. Exclude patterns
echo "Checking exclude patterns:"
if jq -r '.exclude[]' tsconfig.json | grep -q 'node_modules'; then
  echo "  ✅ Excludes node_modules"
else
  echo "  ⚠️  Should exclude node_modules"
fi

if jq -r '.exclude[]' tsconfig.json | grep -q 'dist'; then
  echo "  ✅ Excludes dist"
else
  echo "  ⚠️  Should exclude dist"
fi

echo ""

# 6. Build test
echo "Testing build:"
rm -rf dist
if npm run build > /dev/null 2>&1; then
  echo "  ✅ Build successful"
else
  echo "  ❌ Build failed"
  ERRORS=$((ERRORS + 1))
fi

# Check output
if [ -d dist ]; then
  echo "  ✅ dist/ created"

  # Check for .d.ts files
  if ls dist/*.d.ts 1> /dev/null 2>&1; then
    echo "  ✅ Type declarations generated"
  else
    echo "  ❌ No .d.ts files generated"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "  ❌ No dist/ directory"
  ERRORS=$((ERRORS + 1))
fi

echo ""

# Summary
if [ $ERRORS -eq 0 ]; then
  echo "=== ✅ VALIDATION PASSED ==="
  exit 0
else
  echo "=== ❌ VALIDATION FAILED ($ERRORS errors) ==="
  exit 1
fi
```

## Common Issues

### Issue: Build is slow
**Cause:** Not using `skipLibCheck: true`
**Solution:**
```json
{
  "compilerOptions": {
    "skipLibCheck": true  // Add this
  }
}
```

### Issue: Can't import from CommonJS modules
**Cause:** Missing `esModuleInterop`
**Solution:**
```json
{
  "compilerOptions": {
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true
  }
}
```

### Issue: Type errors in node_modules
**Cause:** Missing `skipLibCheck`
**Solution:**
```json
{
  "compilerOptions": {
    "skipLibCheck": true
  }
}
```

### Issue: Generated code has implicit any errors
**Cause:** `noImplicitAny: true` with generated code
**Solution:**
```json
{
  "compilerOptions": {
    "noImplicitAny": false  // Relax for generated code
  }
}
```

### Issue: Can't find types for @types packages
**Cause:** Missing or incorrect `typeRoots`
**Solution:**
```json
{
  "compilerOptions": {
    "typeRoots": ["node_modules/@types"]
  }
}
```

### Issue: Module resolution errors
**Cause:** Wrong `moduleResolution` setting
**Solution:**
```json
{
  "compilerOptions": {
    "moduleResolution": "node"  // Use node resolution
  }
}
```

## Anti-Patterns

### ❌ BAD: Disabling strict mode
```json
{
  "compilerOptions": {
    "strict": false  // NEVER do this
  }
}
```

### ✅ GOOD: Keep strict mode, fix errors
```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

### ❌ BAD: Not generating declarations
```json
{
  "compilerOptions": {
    "declaration": false  // Breaks TypeScript consumers
  }
}
```

### ✅ GOOD: Always generate declarations
```json
{
  "compilerOptions": {
    "declaration": true
  }
}
```

### ❌ BAD: Complex path mapping
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@utils/*": ["src/utils/*"],
      "@models/*": ["src/models/*"],
      "@services/*": ["src/services/*"]
    }
  }
}
```

### ✅ GOOD: Use relative imports
```typescript
// Just use relative imports
import { User } from './models/User';
import { UserService } from './services/UserService';
```

### ❌ BAD: Undocumented changes
```json
{
  "compilerOptions": {
    "resolveJsonModule": true  // Why? When? Who added this?
  }
}
```

### ✅ GOOD: Documented changes
```json
{
  "compilerOptions": {
    // CUSTOM: Added 2024-10-15
    // Reason: Need to import api-metadata.json
    // Approved by: team-lead
    "resolveJsonModule": true
  }
}
```
