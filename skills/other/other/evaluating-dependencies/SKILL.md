---
name: evaluating-dependencies
description: Evaluates Node.js packages before installation by checking bundle size impact, comparing alternatives, verifying latest stable versions, and assessing maintenance status. Use when adding dependencies, installing packages, choosing between libraries, optimizing bundle size, or when user mentions npm install, yarn add, pnpm add, package selection, or asks about package recommendations.
user-invocable: false
allowed-tools: Bash WebFetch WebSearch Read Grep
metadata:
  author: Saturate
  version: "1.0"
---

# Dependency Evaluation

Evaluate Node.js packages before installation to make informed decisions about bundle size, maintenance status, and alternatives.

## Evaluation Workflow

**For every dependency addition request, follow these steps:**

```
Evaluation Progress:
- [ ] Step 1: Identify need and alternatives
- [ ] Step 2: Check bundle sizes (bundlephobia)
- [ ] Step 3: Verify latest versions (npm registry)
- [ ] Step 4: Assess maintenance status
- [ ] Step 5: Compare and recommend
- [ ] Step 6: Install with latest stable version
```

### Step 1: Identify Need and Alternatives

**If specific package requested** (e.g., "add lodash"):
- Proceed to Step 2 with that package
- Consider mentioning well-known alternatives if relevant

**If generic need** (e.g., "add a date library"):
- Identify 2-4 popular alternatives in that category
- Examples:
  - Date handling: `date-fns`, `dayjs`, `luxon`
  - HTTP client: `axios`, `ky`, `got`
  - State management: `zustand`, `jotai`, `redux`
  - Validation: `zod`, `yup`, `joi`
  - Testing: `vitest`, `jest`, `uvu`

### Step 2: Check Bundle Sizes

**Use bundlephobia to check bundle size impact:**

```bash
# Check bundle size via bundlephobia
curl -s "https://bundlephobia.com/api/size?package=<package>@latest" | jq
```

**Extract key metrics:**
- `size` - Minified size
- `gzip` - Gzipped size (most important for actual impact)
- `dependency_count` - How many dependencies it pulls in

**For multiple alternatives, compare:**
```bash
# Example: Compare date libraries
curl -s "https://bundlephobia.com/api/size?package=dayjs@latest" | jq '.gzip'
curl -s "https://bundlephobia.com/api/size?package=date-fns@latest" | jq '.gzip'
curl -s "https://bundlephobia.com/api/size?package=luxon@latest" | jq '.gzip'
```

### Step 3: Verify Latest Versions

**Check npm registry for latest version:**

```bash
# Get latest version
npm view <package> version

# Get version info with dates
npm view <package> time --json | jq '.modified'

# Check for deprecated status
npm view <package> deprecated
```

**Check multiple versions:**
```bash
# See all versions
npm view <package> versions --json

# Get latest major versions
npm view <package> dist-tags --json
```

### Step 4: Assess Maintenance Status

**Check package health:**

```bash
# Last publish date
npm view <package> time.modified

# Weekly downloads (popularity)
npm view <package> dist.tarball | xargs -I {} curl -s "https://api.npmjs.org/downloads/point/last-week/{}"

# Check repository activity (if GitHub URL available)
npm view <package> repository.url
```

**Red flags:**
- ❌ Last updated >2 years ago
- ❌ Marked as deprecated
- ❌ Security vulnerabilities (check npm audit after install)
- ❌ Very low download count (<1000/week)

**Green flags:**
- ✅ Updated within last 6 months
- ✅ Active maintenance (regular releases)
- ✅ High download count
- ✅ TypeScript support built-in

### Step 5: Compare and Recommend

**Present comparison in this format:**

```
Package Evaluation Results:

Option 1: <package-name> (recommended)
- Bundle size: X KB gzipped
- Latest version: X.X.X
- Last updated: X months ago
- Weekly downloads: XXX,XXX
- TypeScript: ✅ Built-in / ⚠️ @types required / ❌ None
- Why: [Brief reason - smallest/fastest/most maintained/best DX]

Option 2: <alternative>
- Bundle size: X KB gzipped (XX% larger)
- Latest version: X.X.X
- Last updated: X months ago
- Why not: [Brief reason - larger/older/less maintained]

Recommendation: Install <package>@<version>
```

**Decision criteria (in order of importance):**
1. **Maintenance** - Is it actively maintained?
2. **Bundle size** - How much does it add to the bundle?
3. **Popularity** - Is it widely used and trusted?
4. **TypeScript** - Does it have good type support?
5. **Features** - Does it meet the requirements?

### Step 6: Install with Latest Stable Version

**Detect package manager first:**

```bash
if [ -f "bun.lockb" ]; then
    PM="bun"
elif [ -f "pnpm-lock.yaml" ]; then
    PM="pnpm"
elif [ -f "yarn.lock" ]; then
    PM="yarn"
else
    PM="npm"
fi
echo "Using: $PM"
```

**Install with explicit version:**

```bash
# npm
npm install <package>@<version>

# pnpm
pnpm add <package>@<version>

# yarn
yarn add <package>@<version>

# bun
bun add <package>@<version>
```

**For dev dependencies, add -D flag:**
```bash
npm install -D <package>@<version>
pnpm add -D <package>@<version>
yarn add -D <package>@<version>
bun add -d <package>@<version>
```

## Quick Reference Tables

### Common Package Categories

| Need | Top Alternatives | Recommendation |
|------|-----------------|----------------|
| Date handling | dayjs, date-fns, luxon | dayjs (smallest) or date-fns (most features) |
| HTTP client | axios, ky, got, undici | ky (modern) or axios (most popular) |
| Validation | zod, yup, joi | zod (TypeScript-first) |
| Testing | vitest, jest, uvu | vitest (fastest) |
| State (React) | zustand, jotai, redux | zustand (simplest) |
| CSS-in-JS | styled-components, emotion | Check project conventions |
| Icons | lucide-react, react-icons | lucide-react (smaller, tree-shakeable) |
| Forms (React) | react-hook-form, formik | react-hook-form (better performance) |
| UUID | uuid, nanoid | nanoid (smaller, faster) |
| Lodash | lodash-es, radash, remeda | lodash-es (tree-shakeable) or avoid if possible |

### Bundle Size Thresholds

| Size (gzipped) | Impact | Action |
|---------------|--------|--------|
| < 5 KB | Negligible | ✅ Safe to add |
| 5-20 KB | Small | ✅ Usually fine |
| 20-50 KB | Medium | ⚠️ Consider alternatives |
| 50-100 KB | Large | ⚠️ Justify the need |
| > 100 KB | Very large | ❌ Look for lighter alternatives |

## Special Cases

### TypeScript Projects

**Prefer packages with built-in types:**
- ✅ `zod` - Types built-in
- ⚠️ `joi` - Needs `@types/joi`

**Check for types:**
```bash
npm view <package> types
# or check for @types package
npm view @types/<package> version
```

### Monorepo/Workspaces

**For workspace dependencies:**
```bash
# npm
npm install <package> --workspace=packages/web

# pnpm
pnpm add <package> --filter packages/web

# yarn
yarn workspace packages/web add <package>
```

### Alternative: Tree-shakeable Imports

**Some large libraries support tree-shaking:**
```javascript
// ❌ Bad - imports entire library
import _ from 'lodash'

// ✅ Good - tree-shakeable
import debounce from 'lodash-es/debounce'
```

## Anti-Patterns

### ❌ Installing Without Version Check

```bash
# Bad - might get old cached version
npm install lodash

# Good - explicit latest version
npm install lodash@4.17.21
```

### ❌ Not Considering Bundle Size

Don't install `moment.js` (289 KB) when `dayjs` (2.9 KB) would work.

### ❌ Not Checking Maintenance

Avoid deprecated or unmaintained packages:
- `request` (deprecated, use `got` or `ky`)
- `moment` (maintenance mode, use `dayjs` or `date-fns`)

### ❌ Adding Unnecessary Dependencies

Before adding a package, check if:
- Native JavaScript can do it (e.g., `Date` API instead of date library for simple cases)
- It's already in dependencies (check `package.json`)
- A lighter alternative exists

## Examples

### Example 1: Generic Request

**User:** "Add a date library"

**Evaluation:**
1. Alternatives: dayjs, date-fns, luxon
2. Bundle sizes: dayjs (2.9 KB), date-fns (13 KB), luxon (25 KB)
3. Latest: dayjs@1.11.10, date-fns@3.3.1, luxon@3.4.4
4. All actively maintained
5. Recommend: dayjs (smallest, good DX)
6. Install: `npm install dayjs@1.11.10`

### Example 2: Specific Package

**User:** "Add axios"

**Evaluation:**
1. Package: axios (requested), alternatives: ky, got
2. Bundle: axios (13 KB), ky (4.8 KB), got (Node.js only)
3. Latest: axios@1.6.7
4. Very active, 50M+ downloads/week
5. Recommend: axios (as requested, widely used)
6. Install: `npm install axios@1.6.7`

### Example 3: Optimization Request

**User:** "Our bundle is too large, what can we optimize?"

**Evaluation:**
1. Check package.json for heavy dependencies
2. Run bundlephobia on top packages
3. Identify candidates: moment (289 KB) → dayjs (2.9 KB)
4. Suggest: "Replace moment with dayjs, saves 286 KB"
5. Migration guide if needed

## References

**External tools:**
- [Bundlephobia](https://bundlephobia.com) - Bundle size checker
- [npm trends](https://npmtrends.com) - Compare package popularity
- [Snyk Advisor](https://snyk.io/advisor) - Package health scores

**For package manager commands:** See [node-package-management skill](../node-package-management/SKILL.md)
