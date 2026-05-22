---
name: token-injector
description: Automated CSS variable injection from tokens.json. Parses design tokens → generates CSS custom properties → injects into stylesheets → replaces hardcoded values.
---

# Token-Injector Skill

## Function

Input: `tokens.json` + target CSS files
Output: Updated stylesheets with CSS variables

## Process

1. Parse `tokens.json` from asset packages
2. Generate CSS custom properties
3. Inject into `:root` or component scope
4. Replace hardcoded values with `var()` references
5. Validate no broken references

## Token Mapping

**tokens.json:**
```json
{
  "background": "#1A1714",
  "palette": {
    "waratah_crimson": "#C45C4B",
    "wattle_gold": "#D4A84B",
    "eucalyptus_sage": "#7A9E82"
  }
}
```

**Generated CSS:**
```css
:root {
  --color-specimen-night: #1A1714;
  --color-waratah-crimson: #C45C4B;
  --color-wattle-gold: #D4A84B;
  --color-eucalyptus-sage: #7A9E82;
}
```

## Replacement Logic

**Before:**
```css
.card {
  background: #1A1714;
  border: 1px solid #C45C4B;
}
```

**After:**
```css
.card {
  background: var(--color-specimen-night);
  border: 1px solid var(--color-waratah-crimson);
}
```

## Batch Mode

Process all asset `tokens.json` files:
```bash
token-injector --input /assets/*/tokens.json --output /frontend/src/styles/northcote-tokens.css
```

## Integration

**Asset-Packager:** Generates source `tokens.json`
**Claude Code:** Executes injection on target files
**Stylelint:** Validates output

## Efficiency

**Before:** 30 min manual find-replace per component
**After:** 2 min automated injection
**Savings:** 93% reduction

---

*Tokens → CSS variables → automatic injection. Manual replacement eliminated.*
