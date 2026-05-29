---
name: nango-esm-migration
description: Use when fixing CJS/ESM module issues in Nango integrations after zero-yaml migration - covers import path fixes, creating ESM wrappers for CJS vendor modules, and restoring commented-out code
---

# Nango ESM Migration Fixes

This skill documents common issues and fixes when migrating Nango integrations to ESM (zero-yaml migration).

## Common Symptoms

1. **Commented-out imports** with "temporary replacement" functions that hardcode values
2. **Build errors** like `Could not resolve "../../vendor/dinero.js/index.js"`
3. **Type errors** like `Cannot find module '../../../vendor/dinero.js'`

## Investigation Checklist

1. Check git history to see what was changed during migration:
   ```bash
   git log --oneline -10 -- <file>
   git show <commit>:<file> | head -20
   ```

2. Look for commented-out code with "temporary" comments - these are often proper implementations replaced with broken workarounds

3. Verify the vendor module exists and check its structure:
   ```bash
   ls -la vendor/<module>/
   cat vendor/<module>/package.json
   ```

## Fix Pattern: CJS Vendor Module to ESM

When a vendor module only has CJS exports but your project uses ESM:

### Step 1: Create ESM Wrapper

Create `vendor/<module>/index.js`:

```javascript
import Module from './build/cjs/<module>.js';
export default Module;
```

### Step 2: Fix Import Paths

Update imports to use `.js` extensions (required for ESM):

```typescript
// Before (commented out or broken)
// import foo from "../../../vendor/foo";

// After (working ESM)
import foo from "../../vendor/foo/index.js";
```

### Step 3: Restore Proper Implementation

Replace any "temporary" hardcoded workarounds with the original implementation.

**Example - Currency Conversion:**

```typescript
// BAD: Hardcoded workaround (loses currency-specific precision)
function fromMajorToDinero(amount: number | null | undefined, _currencyCode: string | undefined): number | null {
  if (amount == null) return null;
  return Math.round(amount * 100);  // Wrong for JPY, KWD, etc.
}

// GOOD: Proper implementation using currency exponents
import dinero from "../../vendor/dinero.js/index.js";
import { currencies } from "../../vendor/dinero.js/dinero-currencies.js";

function fromMajorToDinero(amount: number | null | undefined, currencyCode: string | undefined): number | null {
  if (amount == null || !currencyCode) return null;
  const currency = currencies[currencyCode.toUpperCase()];
  if (!currency) return null;

  const exponent = currency.exponent;
  const amountInMinor = Math.round(amount * 10 ** exponent);
  return dinero({
    amount: amountInMinor,
    currency: currency as any,
  }).getAmount();
}
```

## Path Calculation

From `nango-integrations/<integration>/mappers/<file>.ts`:
- To `nango-integrations/vendor/`: use `../../vendor/`

From `nango-integrations/<integration>/actions/<file>.ts`:
- To `nango-integrations/vendor/`: use `../../vendor/`

## Verification

```bash
# Type check
npx tsc --noEmit

# Full compile
npx nango compile
```

## Red Flags to Watch For

- `_paramName` (underscore prefix) - indicates intentionally unused parameter, likely a workaround
- Comments like "Temporary replacement until X is available" when X IS available
- Hardcoded values (like `* 100`) replacing dynamic lookups (like `* 10 ** exponent`)
- Commented-out imports at top of file with no replacement
