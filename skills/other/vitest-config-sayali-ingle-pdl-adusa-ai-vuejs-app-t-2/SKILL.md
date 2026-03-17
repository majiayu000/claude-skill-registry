---
name: vitest-config
description: Generates vitest.config.ts for unit testing configuration. Configures Vitest with Vue, TypeScript support, coverage thresholds, and test environment settings.
---

# Vitest Config Skill

## Purpose
Generate the `vitest.config.ts` file for unit testing configuration with Vitest.

## ⚠️ CONDITIONAL EXECUTION

**This skill should ONLY be used if the project uses Vitest instead of Jest.**

### Test Framework Detection:
1. Check `package.json` for test framework dependency:
   - If `"jest"` found → **SKIP THIS SKILL** (use jest-config skill instead)
   - If `"vitest"` found → **EXECUTE THIS SKILL**
   - If neither found → **PROMPT USER**: "Which test framework do you want to use: Jest or Vitest?"

## 🚨 PRE-REQUISITE: REQUIRED DEPENDENCIES

**CRITICAL: Before generating vitest.config.ts, verify package.json includes ALL required Vitest dependencies.**

### Required Vitest Packages

The following packages MUST be in `package.json` devDependencies BEFORE creating vitest.config.ts:

1. **`vitest`** - Core test framework
   - **Why**: Main testing runtime
   - **Error if missing**: "Cannot find module 'vitest'"

2. **`@vitest/coverage-v8`** - Coverage provider
   - **Why**: Required by `coverage.provider: 'v8'` in vitest.config.ts
   - **Error if missing**: "Coverage provider 'v8' not found"
   - **Impact**: Coverage reports won't work

3. **`jsdom`** - DOM environment
   - **Why**: Required by `environment: 'jsdom'` in vitest.config.ts for Vue component testing
   - **Error if missing**: "Environment 'jsdom' not found. You need to install jsdom package"
   - **Impact**: Tests cannot run (blocks all testing)
   - **Alternative**: `happy-dom` (but jsdom is more compatible with Vue ecosystem)

4. **`@vitest/ui`** - Optional UI visualization
   - **Why**: Interactive test UI for debugging
   - **Error if missing**: None (optional feature)

### Validation Check

**BEFORE proceeding with file generation, run this validation**:

```bash
# Check if all required Vitest packages are in package.json
required_packages=("vitest" "@vitest/coverage-v8" "jsdom")
missing_packages=()

for pkg in "${required_packages[@]}"; do
  if ! grep -q "\"$pkg\":" package.json 2>/dev/null; then
    missing_packages+=("$pkg")
  fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
  echo "❌ ERROR: Missing required Vitest dependencies in package.json:"
  printf '  - %s\n' "${missing_packages[@]}"
  echo ""
  echo "SOLUTION: Update package-json skill to include these packages"
  echo "Then re-run npm install before generating vitest.config.ts"
  exit 1
else
  echo "✅ All required Vitest dependencies found in package.json"
fi
```

### What To Do If Packages Are Missing

**DO NOT PROCEED** with generating vitest.config.ts. Instead:

1. **Go back to package-json skill**
2. **Add missing packages** to the versions.json configuration:
   ```json
   "devDependencies": {
     "vitest": "latest",
     "@vitest/ui": "latest",
     "@vitest/coverage-v8": "latest",
     "jsdom": "latest"
   }
   ```
3. **Regenerate package.json** with complete dependencies
4. **Run `npm install`** to install packages
5. **THEN return to this skill** to generate vitest.config.ts

**Why this order matters**:
- vitest.config.ts imports from these packages
- Configuration references these packages by name
- Tests will fail immediately without these runtime dependencies
- Better to catch missing deps during setup than during first test run

## 🚨 MANDATORY FILE COUNT
This skill MUST create exactly **1 file**:
- `vitest.config.ts` (TypeScript format - recommended for Vite projects)

## 🔍 BEFORE GENERATING - RESEARCH REQUIRED

**⚠️ Verify current Vitest ecosystem to ensure best practices**

### Required Research Steps:
1. **Vitest Version**: Check current Vitest version and features
   - Verify latest stable version
   - Check for new configuration options
2. **Coverage Provider**: Verify `@vitest/coverage-v8` is still recommended
   - Check if coverage provider packages are maintained
   - Verify v8 vs istanbul performance and accuracy
3. **Vue Plugin**: Verify `@vitejs/plugin-vue` compatibility
   - Ensure plugin version matches Vite version
   - Check for breaking changes in Vue plugin
4. **Test Environment**: Verify `jsdom` or `happy-dom` recommendation
   - `jsdom` - More complete, slower, better compatibility
   - `happy-dom` - Faster, lighter, good for most use cases
5. **TypeScript Support**: Verify Vitest's built-in TypeScript support
   - No additional transformer needed (unlike Jest)
   - Uses Vite's built-in esbuild transformation
6. **Coverage Configuration**: Check current coverage threshold recommendations
   - Verify recommended coverage levels (lines, branches, functions, statements)
7. **File Format**: Verify `.ts` format is still preferred
   - Alternative: `.js`, `.mts` formats

## Output
Create the file: `vitest.config.ts`

**Supported Format**:
- `vitest.config.ts` (TypeScript - strict preferred format, best for Vite projects)

**Alternative Formats** (only if .ts not preferred):
- `vitest.config.js` (JavaScript)
- `vitest.config.mts` (ES Module TypeScript)

## Example File
See: `examples.md` in this directory for complete examples and detailed explanations.

**⚠️ IMPORTANT**: The examples.md file contains January 2026 configurations. Always verify current Vitest ecosystem before using.

## Configuration Decisions

### Globals: Disabled (`globals: false`)
**Decision**: Explicit imports recommended for modern projects
```typescript
// Requires explicit imports (recommended)
import { describe, it, expect } from 'vitest';
```

**Why**:
- ✅ Better IDE support and auto-completion
- ✅ Explicit dependencies (easier to understand)
- ✅ No global namespace pollution
- ✅ More modern TypeScript pattern

**Alternative** (`globals: true`):
- No imports needed (like Jest)
- Good for migrating from Jest
- May hide dependencies

### Coverage Provider: v8
**Decision**: Use `@vitest/coverage-v8` (recommended)

**Why**:
- ✅ Faster (native V8 instrumentation)
- ✅ More accurate (actual code execution)
- ✅ Better source map support
- ✅ Default for Vitest

**Alternative**: `@vitest/coverage-istanbul` (for Jest compatibility)

### Test Environment: jsdom
**Decision**: Use `jsdom` for maximum compatibility

**Why**:
- ✅ Complete DOM API implementation
- ✅ Better compatibility with third-party libraries
- ✅ Industry standard for Vue testing

**Alternative**: `happy-dom` (faster, lighter, but may have compatibility issues)

## Execution Checklist
- [ ] **Detect test framework** from package.json (Vitest vs Jest)
- [ ] If Jest detected, skip this skill entirely
- [ ] If Vitest detected, proceed with research
- [ ] **CRITICAL: Verify package.json has required Vitest dependencies**:
  - [ ] `vitest` (test framework)
  - [ ] `@vitest/coverage-v8` (coverage provider - REQUIRED for coverage)
  - [ ] `jsdom` (DOM environment - REQUIRED for Vue component testing)
  - [ ] `@vitest/ui` (optional UI visualization)
  - [ ] **If any are missing, STOP and update package.json first**
- [ ] Research current Vitest version and features
- [ ] Verify `@vitest/coverage-v8` is still recommended
- [ ] Verify `@vitejs/plugin-vue` compatibility with Vite version
- [ ] Verify `jsdom` vs `happy-dom` recommendation
- [ ] Check coverage threshold best practices
- [ ] Verify path alias resolution (should inherit from vite.config.ts)
- [ ] Create `vitest.config.ts` with current standards
- [ ] Include coverage thresholds (minimum 80% recommended)
- [ ] Configure globals: false (explicit imports)
- [ ] Verify file format is still recommended (not deprecated)

## 🛑 BLOCKING VALIDATION CHECKPOINT

**STOP! Before proceeding to the next skill, verify:**

### Automated Verification
Run this command to verify the file exists:
```bash
if [ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ] || [ -f "vitest.config.mts" ] || grep -q "\"vitest\":" package.json 2>/dev/null; then
  echo "✓ Vitest configuration found"
  if [ -f "vitest.config.ts" ]; then
    echo "✓ Using vitest.config.ts (preferred format)"
  fi
  
  # Check for Jest conflict
  if grep -q "\"jest\"" package.json 2>/dev/null; then
    echo "⚠ WARNING: Both Vitest and Jest detected in package.json"
    echo "  Consider using only one test framework"
  fi
else
  echo "✗ Vitest configuration missing"
  exit 1
fi
```

### Manual Verification
1. ✓ `vitest.config.ts` exists at project root
2. ✓ File uses TypeScript format (exports `defineConfig`)
3. ✓ File includes `@vitejs/plugin-vue` plugin
4. ✓ File includes `test.globals: false` (explicit imports)
5. ✓ File includes `test.environment: 'jsdom'` for DOM testing
6. ✓ File includes coverage configuration with v8 provider
7. ✓ File includes coverage thresholds (80%+ recommended)
8. ✓ Path aliases are resolved (via Vite config inheritance)
9. ✓ No Jest configuration conflict in package.json
10. ✓ Coverage provider packages in package.json devDependencies

### If Validation Fails
**DO NOT PROCEED** to the next skill. Create or fix the missing/incorrect file immediately.

## Notes
- **Conditional Execution**: Only use if project uses Vitest (not Jest)
- **Recommended**: Vitest is officially recommended for Vue 3 + Vite projects
- **Performance**: Faster than Jest due to Vite's native ESM and esbuild
- **No Transformers**: Vitest uses Vite's built-in transformation (no ts-jest needed)
- **ESM Native**: No `transformIgnorePatterns` needed (handles ESM automatically)
- **Coverage Provider**: v8 is default and recommended for accuracy and performance
- **Test Environment**: jsdom provides complete DOM APIs for Vue component testing
- **Globals Disabled**: Explicit imports improve IDE support and code clarity
- **Hot Module Reload**: Vitest supports HMR for faster development
- **TypeScript Format**: `.ts` format integrates seamlessly with Vite ecosystem
- **Coverage Thresholds**: Include minimum coverage requirements (80%+ recommended)
- **Path Aliases**: Automatically resolved from vite.config.ts (no duplication needed)
- **Always verify current ecosystem** - Vitest evolves with Vite releases
