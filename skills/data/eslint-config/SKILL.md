---
name: eslint-config
description: Generates ESLint 9+ configuration using flat config format. Creates eslint.config.cjs with Vue and TypeScript linting rules for code quality enforcement.
---

# ESLint Config Skill

## Purpose
Generate ESLint configuration file for code linting with Vue and TypeScript support using ESLint 9+ flat config format.

## 🚨 MANDATORY FILE COUNT
This skill MUST create exactly **1 file**:
- `eslint.config.cjs` (preferred format)

## 🔍 BEFORE GENERATING - CRITICAL RESEARCH REQUIRED

**⚠️ HIGH PRIORITY: Verify current ESLint standards to prevent outdated code generation**

### Required Research Steps:
1. **ESLint Version**: Verify current ESLint version supports flat config (9.0+)
2. **Plugin Compatibility**: Check all plugins are compatible with current ESLint version:
   - `eslint-plugin-vue` - Verify latest version and Vue 3 support
   - `@typescript-eslint/eslint-plugin` - Verify compatibility with TypeScript version
   - `eslint-plugin-prettier` - Check if still recommended or if Prettier should run separately
3. **Flat Config Format**: Verify flat config is still the recommended format (not legacy `.eslintrc.*`)
4. **Parser Configuration**: Verify `vue-eslint-parser` and `@typescript-eslint/parser` configuration syntax
5. **Test Framework Detection**: 
   - Check `package.json` for test framework dependencies
   - If `vitest` found: Use `globals.vitest` or `globals.node`
   - If `jest` found: Use `globals.jest`
   - If both or neither: Prompt user which test framework to use
6. **Deprecated Rules**: Check if any rules have been deprecated or renamed
7. **Module Format**: Verify project's module system from `package.json` "type" field for file format selection

## Output
Create the file: `eslint.config.cjs`

**Supported Formats** (in order of preference):
1. `eslint.config.cjs` (preferred - CommonJS format, works with any package.json type)
2. `eslint.config.mjs` (ES Module format, explicit ESM)
3. `eslint.config.js` (follows package.json "type" field)

**Format Selection Logic**:
- Default: Use `eslint.config.cjs` (most compatible)
- If package.json has `"type": "module"` and user prefers ESM: Consider `.mjs`
- `.js` format requires package.json type to match module system

## Example File
See: `examples.md` in this directory for complete examples and detailed explanations.

**⚠️ IMPORTANT**: The examples.md file contains December 2025 configurations. Always verify current standards before using.

## Execution Checklist
- [ ] Research current ESLint version and flat config status (ESLint 9+)
- [ ] Verify all plugin versions and compatibility
- [ ] Check for deprecated rules or configuration options
- [ ] Detect test framework from package.json dependencies
- [ ] If test framework unclear, prompt user
- [ ] Verify parser configuration syntax for Vue and TypeScript
- [ ] Check if legacy `.eslintrc.*` migration notes needed
- [ ] Create `eslint.config.cjs` with current standards
- [ ] Verify file format matches project module system

## 🛑 BLOCKING VALIDATION CHECKPOINT

**STOP! Before proceeding to the next skill, verify:**

### Automated Verification
Run this command to verify the file exists:
```bash
if [ -f "eslint.config.cjs" ] || [ -f "eslint.config.mjs" ] || [ -f "eslint.config.js" ]; then
  echo "✓ ESLint configuration found"
  if [ -f "eslint.config.cjs" ]; then
    echo "✓ Using eslint.config.cjs (preferred format)"
  elif [ -f "eslint.config.mjs" ]; then
    echo "⚠ Using eslint.config.mjs (ESM format)"
  else
    echo "⚠ Using eslint.config.js (verify package.json type field)"
  fi
  
  # Check for legacy format (should not exist)
  if [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ] || [ -f ".eslintrc.yml" ]; then
    echo "✗ Legacy .eslintrc.* file found - remove and use flat config only"
    exit 1
  fi
else
  echo "✗ ESLint configuration missing"
  exit 1
fi
```

### Manual Verification
1. ✓ `eslint.config.cjs` (or `.mjs`/`.js`) exists at project root
2. ✓ File uses ESLint 9+ flat config format (array export, not legacy object)
3. ✓ File includes Vue, TypeScript, and Prettier plugins
4. ✓ Test file configuration uses correct globals for detected test framework
5. ✓ No legacy `.eslintrc.*` files exist in project
6. ✓ All plugin versions are compatible with ESLint version
7. ✓ Configuration follows current ESLint best practices

### If Validation Fails
**DO NOT PROCEED** to the next skill. Create or fix the missing/incorrect file immediately.

## Notes
- **ESLint 9+ Flat Config**: Uses modern flat config format (not legacy `.eslintrc.*`)
- **Migration from Legacy**: If upgrading, remove `.eslintrc.*` files and use flat config only
- **Plugin Compatibility**: Always verify plugin versions match ESLint version
- **Test Framework Globals**: Auto-detected from package.json (Vitest or Jest)
- **Console/Debugger**: Allowed in development, warnings in production
- **Special Rules**: Separate configurations for test files and TypeScript declaration files
- **Prettier Integration**: ESLint runs Prettier as a rule (verify this is current best practice)
- **Module Format**: `.cjs` preferred for maximum compatibility across all project types
- **Parser Chain**: Vue files use `vue-eslint-parser` → `@typescript-eslint/parser` for TypeScript
- **Always verify current standards** - ESLint ecosystem evolves rapidly
- **Breaking Changes**: ESLint major versions may change config format or rule behavior