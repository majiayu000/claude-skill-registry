---
name: babel-config
description: Generates Babel configuration for JavaScript transpilation in tests. Creates babel.config.js file.
---

# Babel Config Skill

## Purpose
Generate a Babel configuration file for transpilation in tests.

## 🔍 BEFORE GENERATING - RESEARCH CURRENT STANDARDS
**⚠️ CRITICAL: Always verify current standards before generating. This skill may reference outdated conventions.**

1. **Check latest Babel documentation**: https://babeljs.io/docs/configuration
2. **Verify current config file format**: Run `npm view @babel/core version` to check latest Babel version
3. **Verify current preset package names**: Check if `@babel/preset-env`, `@babel/preset-typescript` are still current
4. **Check for deprecation warnings**: Review latest Babel release notes for breaking changes
5. **If standards have changed**: Use NEW standards from official docs, NOT the examples below

## 🚨 MANDATORY FILE COUNT
**Total Required: 1 file**
- Babel config file (1 file) - extension may be `.cjs`, `.mjs`, `.js`, or `.json` depending on current standards

**If this file is not created, test transpilation will FAIL.**

## Requirements (Dynamic - Verify Current Standards)
- Check current Babel best practices before generating
- Use latest recommended presets from official Babel documentation
- Use current standard file extension for Babel configs
- Verify package names exist in npm registry before adding: `npm view <package> version`
- If `@babel/preset-env` is deprecated, use its successor
- If `.cjs` extension is outdated, use current standard

## Output
Create a Babel configuration file with the currently recommended format

## Example Configuration (As of December 2025 - May be outdated)
⚠️ **VERIFY these packages and conventions are still current before using:**

### Example File: `babel.config.cjs`
- **Extension**: `.cjs` (CommonJS format - verify this is still standard)
- **Presets**: 
  - `@babel/preset-env` (for ES6+ transpilation - check if deprecated)
  - `@babel/preset-typescript` (for TypeScript - check if deprecated)
- **Plugins**:
  - `@babel/plugin-transform-runtime` (check if still recommended)

**If any of these are deprecated or outdated:**
- Check: https://babeljs.io/docs/ for current replacements
- Check: `npm view @babel/core@latest` for latest version info
- Check: Babel migration guides for breaking changes

## Execution Checklist
Use this checklist to ensure the file is created:
- [ ] **FIRST**: Research current Babel standards (see "BEFORE GENERATING" section)
- [ ] Create Babel config file at project root (verify correct extension)
- [ ] File includes current standard presets for ES6+ and TypeScript
- [ ] File includes current standard plugins (if any)
- [ ] Verify packages exist in npm: `npm view <package> version`
- [ ] Verify file exists: `ls babel.config.*`

## 🛑 BLOCKING VALIDATION CHECKPOINT
**STOP AND VERIFY before proceeding to the next skill:**

### Automated Verification (Flexible for any extension)
Run this command to verify the file exists:
```bash
# Check for babel config file (any valid extension)
if [ ! -f babel.config.cjs ] && [ ! -f babel.config.mjs ] && [ ! -f babel.config.js ] && [ ! -f babel.config.json ]; then
  echo "❌ MISSING: babel config file (expected: .cjs, .mjs, .js, or .json)"
  exit 1
fi
echo "✅ Babel config file present"
```

### Manual Verification
1. ✓ Babel config file exists at project root (any current standard extension)
2. ✓ File contains current standard presets for ES6+ transpilation and TypeScript
3. ✓ File contains current standard plugins (if required)
4. ✓ All package names verified to exist: `npm view <package> version`
5. ✓ Configuration follows latest Babel documentation standards

### If Validation Fails
**DO NOT PROCEED** to the next skill. Create the missing file immediately.

## Notes
- Babel configuration for test environment transpilation (Jest/Vitest with Babel)
- Transpiles modern JavaScript for Node test environment
- File format depends on current Babel standards (check docs)
- Presets automatically determine necessary transformations
- Enables use of modern syntax in test files
- Required for test frameworks to process ES modules and modern JavaScript features
- **Always verify current standards** - Babel ecosystem evolves over time
