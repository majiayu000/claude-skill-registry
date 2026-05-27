---
name: browserslistrc
description: Defines target browser versions for CSS autoprefixing and JavaScript transpilation. Generates .browserslistrc configuration file.
---

# Browserslist Skill

## Purpose
Generate Browserslist configuration to define supported browsers for CSS autoprefixing and JavaScript transpilation.

## 🚨 MANDATORY FILE COUNT
This skill MUST create exactly **1 file**:
- `.browserslistrc` (preferred format)

## 🔍 BEFORE GENERATING
**Research current Browserslist standards** to ensure accuracy:
1. Check Browserslist documentation for latest query syntax
2. Verify recommended browser targets for modern web applications
3. Check if any queries have been deprecated or new ones added
4. Verify file format options (standalone file vs package.json)

## Output
Create the file: `.browserslistrc`

**Supported Formats** (in order of preference):
1. `.browserslistrc` (preferred - standalone file)
2. `browserslist` field in `package.json`
3. `.browserslistrc.json` (JSON format)

## Example Configuration (As of December 2025 - May be outdated)

**⚠️ DEPRECATION WARNING**: This example uses December 2025 standards. Always verify current Browserslist query syntax and recommended targets before using.

**Preferred: `.browserslistrc`**
```
> 1%
last 2 versions
not dead
not ie 11
```

**Alternative: package.json field**
```json
{
  "browserslist": [
    "> 1%",
    "last 2 versions",
    "not dead",
    "not ie 11"
  ]
}
```

**Query Explanations:**
- `> 1%` - Browsers with >1% global usage
- `last 2 versions` - Last 2 versions of all major browsers
- `not dead` - Exclude browsers without official support
- `not ie 11` - Explicitly exclude Internet Explorer 11

## Execution Checklist
- [ ] Research current Browserslist query syntax and standards
- [ ] Check if recommended browser targets have changed
- [ ] Verify query syntax hasn't been deprecated
- [ ] Create `.browserslistrc` file with appropriate queries
- [ ] Verify file format follows current standards

## 🛑 BLOCKING VALIDATION CHECKPOINT

**STOP! Before proceeding to the next skill, verify:**

### Automated Verification
Run this command to verify the file exists:
```bash
if [ -f ".browserslistrc" ] || grep -q "browserslist" package.json 2>/dev/null || [ -f ".browserslistrc.json" ]; then
  echo "✓ Browserslist configuration found"
  if [ -f ".browserslistrc" ]; then
    echo "✓ Using .browserslistrc (preferred format)"
  fi
else
  echo "✗ Browserslist configuration missing"
  exit 1
fi
```

### Manual Verification
1. ✓ `.browserslistrc` exists at project root (or browserslist in package.json)
2. ✓ File contains browser targeting queries
3. ✓ Queries follow current Browserslist syntax standards
4. ✓ Configuration balances modern features with browser support

### If Validation Fails
**DO NOT PROCEED** to the next skill. Create the missing file immediately.

## Notes
- Targets browsers with >1% market share
- Supports last 2 versions of all major browsers
- Excludes browsers without official support or security updates (dead browsers)
- Explicitly excludes Internet Explorer 11
- Used by Autoprefixer, Babel, PostCSS, and other build tools
- Helps optimize bundle size by not supporting outdated browsers
- Ensures modern browser features can be used with appropriate polyfills
- **Query syntax evolves** - New queries may be added, old ones deprecated
- **Always verify current standards** - Browser landscape changes over time
- Can test queries at: https://browsersl.ist/
