---
name: prettier-config
description: Generates .prettierrc configuration file for code formatting with Prettier. Defines formatting rules for consistent code style across the project.
---

# Prettier Config Skill

## Purpose
Generate Prettier configuration file for code formatting.

## 🚨 MANDATORY FILE COUNT
This skill MUST create exactly **1 file**:
- `.prettierrc` (preferred format - JSON without extension)

## 🔍 BEFORE GENERATING - CRITICAL RESEARCH REQUIRED

**⚠️ HIGH PRIORITY: Verify current Prettier configuration options to prevent outdated settings**

### Required Research Steps:
1. **Prettier Version**: Check current Prettier version and configuration format
   - Verify `.prettierrc` format is still recommended
   - Check if any configuration options have been deprecated
2. **Configuration Options**: Verify the following options are still valid:
   - `singleQuote` - Still accepts boolean values
   - `semi` - Still accepts boolean values
   - `trailingComma` - Still accepts "es5" / "all" / "none" values
3. **Default Values**: Check if Prettier defaults have changed
   - Verify current default for `printWidth` (usually 80)
   - Verify current default for `tabWidth` (usually 2)
   - Check if `endOfLine` default is still "lf"
4. **Optional Settings**: Research if new recommended options have been added:
   - `printWidth` - Line length (default 80)
   - `tabWidth` - Spaces per indentation (default 2)
   - `endOfLine` - Line ending style (lf/crlf/auto)
   - `arrowParens` - Arrow function parentheses
5. **File Format Alternatives**: Check if format is deprecated
   - Verify `.prettierrc` (JSON) is still preferred
   - Check `.prettierrc.json`, `.prettierrc.js`, package.json field

## Output
Create the file: `.prettierrc`

**Supported Formats** (in order of preference):
1. `.prettierrc` (preferred - JSON without extension)
2. `.prettierrc.json` (explicit JSON format)
3. `.prettierrc.js` (JavaScript with dynamic logic)
4. `prettier` field in `package.json`

## Template
See: `examples.md` in this directory for complete template and detailed examples.

**⚠️ IMPORTANT**: The examples.md file contains December 2025 configurations. Always verify current Prettier options before using.

## Execution Checklist
- [ ] Research current Prettier version and recommended config format
- [ ] Verify `singleQuote`, `semi`, `trailingComma` options are still valid
- [ ] Check if option syntax or values have changed
- [ ] Verify default values haven't changed (printWidth, tabWidth, endOfLine)
- [ ] Check for new recommended options
- [ ] Create `.prettierrc` with minimal, verified configuration
- [ ] Verify file format is still recommended (not deprecated)

## 🛑 BLOCKING VALIDATION CHECKPOINT

**STOP! Before proceeding to the next skill, verify:**

### Automated Verification
Run this command to verify the file exists:
```bash
if [ -f ".prettierrc" ] || [ -f ".prettierrc.json" ] || [ -f ".prettierrc.js" ] || grep -q "prettier" package.json 2>/dev/null; then
  echo "✓ Prettier configuration found"
  if [ -f ".prettierrc" ]; then
    echo "✓ Using .prettierrc (preferred format)"
    # Validate JSON syntax
    if command -v jq >/dev/null 2>&1; then
      jq empty .prettierrc && echo "✓ Valid JSON syntax" || echo "✗ Invalid JSON syntax"
    elif command -v node >/dev/null 2>&1; then
      node -e "JSON.parse(require('fs').readFileSync('.prettierrc', 'utf8'))" && echo "✓ Valid JSON" || echo "✗ Invalid JSON"
    fi
  fi
else
  echo "✗ Prettier configuration missing"
  exit 1
fi
```

### Manual Verification
1. ✓ `.prettierrc` exists at project root (or alternative format)
2. ✓ File contains valid JSON syntax
3. ✓ File includes `singleQuote` option (verify current syntax)
4. ✓ File includes `semi` option (verify current syntax)
5. ✓ File includes `trailingComma` option (verify current values)
6. ✓ Configuration options use current Prettier syntax
7. ✓ All option values are valid for current Prettier version

### If Validation Fails
**DO NOT PROCEED** to the next skill. Create or fix the missing/incorrect file immediately.

## Notes
- **Minimal Configuration**: Uses only 3 essential options (singleQuote, semi, trailingComma)
- **Prettier Defaults**: Relies on Prettier's sensible defaults for other options
- **Single Quotes**: `"singleQuote": true` - Uses single quotes for strings
- **Semicolons**: `"semi": true` - Requires semicolons at end of statements
- **Trailing Commas**: `"trailingComma": "es5"` - ES5 compatible trailing commas (objects, arrays)
- **Works with ESLint**: Compatible with eslint-plugin-prettier integration
- **Git-Friendly**: Minimal diffs when configuration changes
- **Optional Settings**: Can add `printWidth`, `tabWidth`, `endOfLine` if needed
- **Format Flexibility**: Supports .prettierrc, .json, .js, package.json field
- **Always verify current options** - Prettier may change configuration schema
- **JSON Preferred**: Simple, declarative, no build step required
- **Team Consistency**: Ensures all developers use same formatting rules
