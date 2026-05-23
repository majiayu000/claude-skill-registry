---
name: lintstagedrc
description: Generates .lintstagedrc configuration to automatically fix and format staged files before commit. Runs ESLint, Stylelint, and Prettier on staged files.
---

# Lint-Staged Configuration Skill

## Purpose
Generate lint-staged configuration to automatically fix and format staged files before commit.

## 🚨 MANDATORY FILE COUNT
This skill MUST create exactly **1 file**:
- `.lintstagedrc.json` (preferred format)

## 🔍 BEFORE GENERATING - CRITICAL RESEARCH REQUIRED

**⚠️ HIGH PRIORITY: Verify current tool CLI flags to prevent outdated commands**

### Required Research Steps:
1. **ESLint CLI Flags**: Verify `eslint --fix` is still the correct flag
   - Check if ESLint CLI has deprecated or changed flags
   - Verify `--fix` flag still works with current ESLint version
2. **Prettier CLI Flags**: Verify `prettier --write` is still correct
   - Check if Prettier CLI has changed flags
   - Verify `--write` flag syntax hasn't changed
3. **Stylelint CLI** (if project uses Stylelint):
   - Check `package.json` for `stylelint` dependency
   - If found: Verify `stylelint --fix` is correct flag
   - Include style file patterns in configuration
4. **File Patterns**: Verify glob patterns work with lint-staged version
   - Check if pattern syntax has changed
   - Verify file extension support (jsx, tsx, css, scss)
5. **Command Chaining**: Verify array of commands still executes sequentially
6. **Alternative Formats**: Check if `.lintstagedrc.json` is still recommended format
   - Verify not deprecated in favor of `.lintstagedrc.js` or package.json field

## Output
Create the file: `.lintstagedrc.json`

**Supported Format**:
- `.lintstagedrc.json` (strict preferred format - simple JSON configuration)

**Alternative Formats** (only if JSON deprecated):
- `.lintstagedrc.js` (JavaScript with dynamic logic)
- `lint-staged` field in `package.json`
- `.lintstagedrc.cjs` (CommonJS format)

## Example File
See: `examples.md` in this directory for complete examples and detailed explanations.

**⚠️ IMPORTANT**: The examples.md file contains December 2025 configurations. Always verify current CLI flags before using.

## Execution Checklist
- [ ] Research current ESLint CLI flags (verify `--fix`)
- [ ] Research current Prettier CLI flags (verify `--write`)
- [ ] Check if project has Stylelint in package.json
- [ ] If Stylelint found, verify `stylelint --fix` flag
- [ ] Determine file patterns based on project needs (jsx/tsx/css/scss)
- [ ] Verify lint-staged glob pattern syntax hasn't changed
- [ ] Create `.lintstagedrc.json` with appropriate commands and patterns
- [ ] Verify JSON format is still recommended (not deprecated)

## 🛑 BLOCKING VALIDATION CHECKPOINT

**STOP! Before proceeding to the next skill, verify:**

### Automated Verification
Run this command to verify the file exists:
```bash
if [ -f ".lintstagedrc.json" ] || [ -f ".lintstagedrc.js" ] || [ -f ".lintstagedrc.cjs" ] || grep -q "lint-staged" package.json 2>/dev/null; then
  echo "✓ Lint-staged configuration found"
  if [ -f ".lintstagedrc.json" ]; then
    echo "✓ Using .lintstagedrc.json (preferred format)"
    # Validate JSON syntax
    if command -v jq >/dev/null 2>&1; then
      jq empty .lintstagedrc.json && echo "✓ Valid JSON syntax" || echo "✗ Invalid JSON syntax"
    fi
  fi
else
  echo "✗ Lint-staged configuration missing"
  exit 1
fi
```

### Manual Verification
1. ✓ `.lintstagedrc.json` exists at project root
2. ✓ File contains valid JSON syntax
3. ✓ File includes ESLint command with current flags
4. ✓ File includes Prettier command with current flags
5. ✓ File patterns match project file types (js/ts/vue, optionally jsx/tsx/css/scss)
6. ✓ Commands use current CLI flags (not deprecated)
7. ✓ If Stylelint in project, style files have stylelint command

### If Validation Fails
**DO NOT PROCEED** to the next skill. Create or fix the missing/incorrect file immediately.

## Notes
- **ESLint Auto-Fix**: Runs `eslint --fix` on JS/TS/Vue files (verify flag current)
- **Prettier Formatting**: Runs `prettier --write` on code and config files (verify flag current)
- **Fast and Efficient**: Only processes staged files, not entire codebase
- **Husky Integration**: Works with pre-commit hook for automated quality checks
- **Prevents Bad Commits**: Blocks commits that don't meet linting standards
- **Sequential Execution**: Commands in array run sequentially for each file
- **File Patterns**: Supports glob patterns (`*.{js,ts,vue}`, `*.{css,scss}`)
- **Extended Patterns**: Include jsx/tsx if React, css/scss if using style files
- **Stylelint Optional**: Only include if project has `stylelint` in package.json
- **Always verify current CLI flags** - Tools may change flag syntax
- **JSON Format Preferred**: Simple, declarative, works without build step
- **Command Arrays**: Multiple commands per pattern run sequentially on same files
