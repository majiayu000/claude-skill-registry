---
name: stylelintrc
description: Generates .stylelintrc configuration for linting CSS, SCSS, and Vue component styles. Auto-detects stylesheet type and fetches latest package versions for plugins.
---

# Stylelint Configuration Skill

## Purpose
Generate Stylelint configuration for linting CSS, SCSS, and Vue component styles with automatic detection of stylesheet type and latest package versions.

## 🚨 MANDATORY FILE COUNT
**Expected Output**: **1 file**
- `.stylelintrc` (primary format, JSON)

**Alternative formats** (if `.stylelintrc` is deprecated):
- `.stylelintrc.json`
- `.stylelintrc.cjs`
- `.stylelintrc.js`
- `.stylelintrc.yaml` / `.stylelintrc.yml`

## 🔍 BEFORE GENERATING - CRITICAL RESEARCH REQUIRED

Perform these checks in order before generating the configuration:

1. **Stylelint Version**: Fetch latest stable version
   - Run: `npm view stylelint version`
   - Use: `^{latest_version}` in package.json
   - **If version >= 16.0.0**: Use new plugin system (verify breaking changes)

2. **Stylesheet Type Detection**: Determine CSS vs SCSS usage
   - **Check `package.json` dependencies**:
     - If `sass` or `node-sass` found → **Use SCSS config**
     - If neither found → **Use standard CSS config**
   - **Check project files**:
     - Search for `**/*.scss` files in `src/` directory
     - If SCSS files found → **Use SCSS config**
     - If only CSS files → **Use standard CSS config**

3. **Config Package Selection** (based on step 2):
   - **For SCSS projects**:
     - Run: `npm view stylelint-config-standard-scss version`
     - Use: `stylelint-config-standard-scss` at `^{latest_version}`
   - **For CSS projects**:
     - Run: `npm view stylelint-config-standard version`
     - Use: `stylelint-config-standard` at `^{latest_version}`

4. **Vue Configuration**: Always include for Vue projects
   - Run: `npm view stylelint-config-recommended-vue version`
   - Use: `stylelint-config-recommended-vue` at `^{latest_version}`
   - **Note**: Works with both CSS and SCSS in Vue SFCs

5. **Verify Configuration Format**: Check if `.stylelintrc` is still supported
   - Run: `npm view stylelint peerDependencies`
   - **If `.stylelintrc` deprecated**: Use `.stylelintrc.json` or `.stylelintrc.cjs`
   - **Default**: Use `.stylelintrc` (JSON format)

6. **Check Rule Compatibility**: Verify rules haven't been deprecated
   - Check: https://stylelint.io/user-guide/rules/
   - **Common deprecations to watch**:
     - `unit-allowed-list` (verify still exists)
     - `color-function-notation` (check valid values)
     - `alpha-value-notation` (verify syntax)
   - **If rules deprecated**: Remove or replace with current alternatives

7. **Lint-Staged Integration**: Check if stylelint should be added to lint-staged
   - **Check if `.lintstagedrc` or `.lintstagedrc.cjs` exists**:
     - If exists → **CROSS-CHECK**: Verify stylelint is included
     - If missing stylelint → **RECOMMEND**: Add to lint-staged config
   - **Suggested lint-staged pattern**:
     ```javascript
     '**/*.{css,scss,vue}': 'stylelint --fix'
     ```
   - **Action**: If lint-staged exists but missing stylelint, notify user to update

8. **PostCSS Integration** (optional): Check if PostCSS is used
   - If `postcss.config.js` exists → Ensure compatibility
   - If Tailwind CSS detected → Add Tailwind-specific rules

## Execution Checklist

Execute in this order:

- [ ] 1. Fetch latest `stylelint` version from npm
- [ ] 2. Detect stylesheet type (SCSS vs CSS) from package.json and file structure
- [ ] 3. Fetch latest version of appropriate config package:
  - [ ] `stylelint-config-standard-scss` (if SCSS detected)
  - [ ] `stylelint-config-standard` (if only CSS)
- [ ] 4. Fetch latest `stylelint-config-recommended-vue` version
- [ ] 5. Verify `.stylelintrc` format is still supported
- [ ] 6. Verify all rules in template are still valid
- [ ] 7. Check if lint-staged config exists and includes stylelint
- [ ] 8. Generate `.stylelintrc` file with detected configuration
- [ ] 9. Run validation script to confirm file exists and is valid JSON

## Output

### Primary Format: `.stylelintrc` (JSON)

**For SCSS Projects**:
```json
{
  "extends": [
    "stylelint-config-standard-scss",
    "stylelint-config-recommended-vue"
  ],
  "rules": {
    // See examples.md for complete rule configuration
  }
}
```

**For CSS Projects**:
```json
{
  "extends": [
    "stylelint-config-standard",
    "stylelint-config-recommended-vue"
  ],
  "rules": {
    // See examples.md for complete rule configuration
  }
}
```

## 🛑 BLOCKING VALIDATION CHECKPOINT

After generating the file, run this validation:

```bash
#!/bin/bash

# Validate .stylelintrc exists and is valid JSON
STYLELINT_FILES=(".stylelintrc" ".stylelintrc.json" ".stylelintrc.cjs" ".stylelintrc.js")
FOUND=false

for file in "${STYLELINT_FILES[@]}"; do
  if [ -f "$file" ]; then
    FOUND=true
    echo "✓ Found: $file"
    
    # Validate JSON format (if .stylelintrc or .json)
    if [[ "$file" == *.stylelintrc ]] || [[ "$file" == *.json ]]; then
      if ! jq empty "$file" 2>/dev/null; then
        echo "✗ ERROR: $file is not valid JSON"
        exit 1
      fi
    fi
    
    # Validate required extends
    if [[ "$file" == *.stylelintrc ]] || [[ "$file" == *.json ]]; then
      if ! grep -q "stylelint-config-" "$file"; then
        echo "✗ ERROR: Missing stylelint-config-* in extends"
        exit 1
      fi
      
      if ! grep -q "stylelint-config-recommended-vue" "$file"; then
        echo "✗ WARNING: Missing Vue config (expected for Vue projects)"
      fi
    fi
    
    break
  fi
done

if [ "$FOUND" = false ]; then
  echo "✗ ERROR: No stylelint configuration file found"
  echo "Expected one of: ${STYLELINT_FILES[@]}"
  exit 1
fi

# Check if lint-staged exists and includes stylelint
LINTSTAGED_FILES=(".lintstagedrc" ".lintstagedrc.json" ".lintstagedrc.cjs" ".lintstagedrc.js")
for file in "${LINTSTAGED_FILES[@]}"; do
  if [ -f "$file" ]; then
    if ! grep -q "stylelint" "$file"; then
      echo "⚠️ RECOMMENDATION: Add stylelint to $file for pre-commit linting"
      echo "   Suggested pattern: '**/*.{css,scss,vue}': 'stylelint --fix'"
    else
      echo "✓ Stylelint integrated with lint-staged"
    fi
    break
  fi
done

echo "✓ Stylelint configuration validation passed"
```

**Validation Requirements**:
1. ✅ Stylelint config file exists (any supported format)
2. ✅ File is valid JSON/JavaScript syntax
3. ✅ Contains `extends` array with config packages
4. ✅ Includes `stylelint-config-recommended-vue` for Vue projects
5. ⚠️ Check lint-staged integration (warning if missing)

## Template Reference
See: `examples.md` in this directory for:
- Complete `.stylelintrc` examples (SCSS and CSS variants)
- Detailed rule explanations with why each rule is configured
- Package version verification commands
- Lint-staged integration examples
- Common issues and troubleshooting
- Rule migration guide for deprecated options

## Notes

### Key Features
- **Automatic Detection**: SCSS vs CSS based on project dependencies and files
- **Latest Versions**: Always fetch current stable versions from npm
- **Vue Support**: Includes Vue SFC style linting
- **Flexible Rules**: Balanced between strictness and developer experience
- **Lint-Staged Ready**: Integrates with pre-commit hooks
- **Format Flexibility**: Supports multiple config formats with validation

### Rule Philosophy
- **Extends standard configs**: Leverage community best practices
- **Minimal overrides**: Only disable overly restrictive rules
- **Allow common units**: px, rem, em, %, vh, vw, deg, fr, s, in
- **Disable vendor prefix warnings**: Required for browser compatibility
- **Relaxed patterns**: No strict class naming enforcement
- **SCSS-specific**: Space after variable colons for consistency

### Configuration Strategy
- **Standard SCSS/CSS**: Primary configuration source
- **Vue-specific**: Handles `<style>` blocks in `.vue` files
- **Legacy notation**: `color-function-notation: "legacy"` for rgb()/rgba()
- **Import flexibility**: String notation for `@use`/`@import`
- **No descending specificity checks**: Too strict for real-world CSS

### Lint-Staged Integration
- **Pattern**: `**/*.{css,scss,vue}` matches all style files
- **Auto-fix**: Use `stylelint --fix` to auto-fix issues
- **Performance**: Only lint changed files in pre-commit
- **Cross-skill coordination**: Check if lintstagedrc skill added stylelint

### Maintenance Considerations
- **Stylelint 16+**: Major version with breaking changes (verify compatibility)
- **Rule deprecations**: Check release notes for removed/renamed rules
- **Config package updates**: Standard configs may change rule defaults
- **Vue config compatibility**: Ensure works with current Vue version
- **Format migration**: Be ready to switch from `.stylelintrc` to `.stylelintrc.json`

