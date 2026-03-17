---
name: jest-config
description: Generates jest.config.cjs for unit testing configuration. Configures Jest with Vue, TypeScript support, coverage thresholds, and test environment settings.
---

# Jest Config Skill

## Purpose
Generate the `jest.config.cjs` file for unit testing configuration with Jest.

## ⚠️ CONDITIONAL EXECUTION

**This skill should ONLY be used if the project uses Jest instead of Vitest.**

### Test Framework Detection:
1. Check `package.json` for test framework dependency:
   - If `"vitest"` found → **SKIP THIS SKILL** (use vitest-config skill instead)
   - If `"jest"` found → **EXECUTE THIS SKILL**
   - If neither found → **PROMPT USER**: "Which test framework do you want to use: Jest or Vitest?"

**Note**: Vitest is the officially recommended test framework for Vue 3 projects as of 2024+. Jest is considered legacy but still widely used.

## 🚨 MANDATORY FILE COUNT
This skill MUST create exactly **1 file**:
- `jest.config.cjs` (preferred format - CommonJS)

## 🔍 BEFORE GENERATING - CRITICAL RESEARCH REQUIRED

**⚠️ HIGH PRIORITY: Verify current Jest ecosystem to prevent outdated configuration**

### Required Research Steps:
1. **Jest Version**: Check current Jest version and configuration format
   - Verify Jest is still maintained and supported
   - Check if `jest.config.cjs` format is still recommended
2. **Vue 3 Jest Transformer**: **CRITICAL - Check if `@vue/vue3-jest` is still maintained**
   - Run: `npm view @vue/vue3-jest time`
   - Check last publish date and maintenance status
   - **If deprecated or unmaintained**:
     - **STOP and PROMPT USER**: "@vue/vue3-jest appears unmaintained. Vitest is now recommended for Vue 3. Should we continue with Jest or switch to Vitest?"
     - Wait for user decision before proceeding
   - If maintained: Verify current version and compatibility with Jest 29+
3. **Coverage Provider**: Verify `v8` vs `babel` coverage provider
   - Check if `v8` is still recommended over `babel`
   - Verify compatibility with current Jest version
   - Check performance and accuracy differences
4. **TypeScript Support**: Verify `ts-jest` transformer
   - Check if `ts-jest` is still maintained
   - Verify compatibility with TypeScript and Jest versions
5. **ESM Package Detection**: Identify packages requiring transformation
   - Check `package.json` for ESM-only packages (axios, date-fns, etc.)
   - Research which packages need to be in `transformIgnorePatterns`
   - Common ESM packages: axios, lodash-es, uuid (verify current list)
6. **Test Environment**: Verify `jsdom` is still recommended
   - Check if `jsdom` or `node` environment is appropriate
   - Verify `jsdom` version compatibility
7. **File Format Options**: Check if format is deprecated
   - Verify `.cjs` format is still preferred
   - Check `.js`, `.mjs`, `.json`, package.json field alternatives

## Output
Create the file: `jest.config.cjs`

**Supported Format**:
- `jest.config.cjs` (strict preferred format - CommonJS, most compatible)

**Alternative Formats** (only if .cjs deprecated):
- `jest.config.js` (JavaScript, follows package.json type)
- `jest.config.mjs` (ES Module format)
- `jest.config.json` (JSON format, limited functionality)

## Example File
See: `examples.md` in this directory for complete examples and detailed explanations.

**⚠️ IMPORTANT**: The examples.md file contains December 2025 configurations. Always verify current Jest ecosystem before using.

## Execution Checklist
- [ ] **Detect test framework** from package.json (Jest vs Vitest)
- [ ] If Vitest detected, skip this skill entirely
- [ ] If Jest detected, proceed with research
- [ ] Research current Jest version and configuration format
- [ ] **CRITICAL**: Verify `@vue/vue3-jest` maintenance status
- [ ] If `@vue/vue3-jest` unmaintained, prompt user for decision
- [ ] Verify `ts-jest` transformer compatibility
- [ ] Research coverage provider (`v8` vs `babel`)
- [ ] Detect ESM packages in package.json needing transformation
- [ ] Verify `jsdom` test environment compatibility
- [ ] Create `jest.config.cjs` with current standards
- [ ] Verify file format is still recommended (not deprecated)

## 🛑 BLOCKING VALIDATION CHECKPOINT

**STOP! Before proceeding to the next skill, verify:**

### Automated Verification
Run this command to verify the file exists:
```bash
if [ -f "jest.config.cjs" ] || [ -f "jest.config.js" ] || [ -f "jest.config.mjs" ] || grep -q "\"jest\":" package.json 2>/dev/null; then
  echo "✓ Jest configuration found"
  if [ -f "jest.config.cjs" ]; then
    echo "✓ Using jest.config.cjs (preferred format)"
  fi
  
  # Check for Vitest conflict
  if grep -q "\"vitest\"" package.json 2>/dev/null; then
    echo "⚠ WARNING: Both Jest and Vitest detected in package.json"
    echo "  Consider using only one test framework"
  fi
else
  echo "✗ Jest configuration missing"
  exit 1
fi
```

### Manual Verification
1. ✓ `jest.config.cjs` exists at project root
2. ✓ File uses CommonJS format (`module.exports`)
3. ✓ File includes `preset: 'ts-jest'` for TypeScript support
4. ✓ File includes `testEnvironment: 'jsdom'` for DOM testing
5. ✓ File includes Vue transformer (`@vue/vue3-jest` - if maintained)
6. ✓ `transformIgnorePatterns` includes detected ESM packages
7. ✓ Coverage provider is set (verify `v8` or `babel`)
8. ✓ Module name mapper includes path aliases (`@/` → `src/`)
9. ✓ No Vitest configuration conflict in package.json

### If Validation Fails
**DO NOT PROCEED** to the next skill. Create or fix the missing/incorrect file immediately.

## Notes
- **Conditional Execution**: Only use if project uses Jest (not Vitest)
- **Vitest Preferred**: For new Vue 3 projects, Vitest is officially recommended
- **Coverage Provider**: `v8` is faster and more accurate than `babel` (verify current recommendation)
- **Vue Transformer**: `@vue/vue3-jest` transforms Vue SFC files (check maintenance status)
- **TypeScript Support**: `ts-jest` transforms TypeScript files
- **ESM Handling**: `transformIgnorePatterns` allows testing ESM packages
- **Coverage Exclusions**: Excludes infrastructure files (main.ts, router, services, etc.)
- **Module Name Mapper**: Handles `@/` path aliases and asset imports
- **Test Environment**: `jsdom` provides DOM APIs for component testing
- **Setup Files**: Can configure test environment and globals
- **Always verify current ecosystem** - Jest/Vue testing landscape evolves
- **CommonJS Format**: `.cjs` ensures compatibility with all module systems
- **Legacy Status**: Jest is legacy for Vue 3; consider migrating to Vitest
