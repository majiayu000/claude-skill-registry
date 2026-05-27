---
name: config-hygiene
description: Fixes configuration hygiene issues including gitignore patterns, ESLint config duplication, and hook scripts. Use when encountering backup files in repo, missing gitignore patterns, or config maintenance issues.
---

# Configuration Hygiene Fixes

Fixes for project configuration issues. Clean configs prevent noise, ensure consistency, and improve developer experience.

## Quick Start

1. Identify the config issue (gitignore, ESLint, husky)
2. Apply the recommended fix
3. Verify no unintended side effects
4. Commit config changes

## Priority Matrix

| Issue | Priority | Impact |
|-------|----------|--------|
| Backup files in repo | P2 | Noise, confusion |
| Missing gitignore patterns | P2 | Unwanted files tracked |
| Husky silent failure | P2 | Hidden hook failures |
| ESLint config duplication | P3 | Maintenance burden |
| Permissive lint threshold | P2 | Quality regression |

---

## Workflows

### Backup/Artifact Files in Repository (#35 - 12 occurrences)

**Detection**: Files matching `*.bak`, `*.orig`, `*~` patterns.

**Pattern**: Editor/merge artifacts committed to repo.

**Fix Strategy**: Remove from git, add to gitignore.

```bash
# Remove from git (keep locally)
git rm --cached "*.bak"
git rm --cached "*.orig"
git rm --cached "*~"

# Add to .gitignore
echo "*.bak" >> .gitignore
echo "*.orig" >> .gitignore
echo "*~" >> .gitignore

# Commit
git add .gitignore
git commit -m "chore: ignore backup/artifact files"
```

---

### Missing .gitignore Patterns (#36 - 8 occurrences)

**Detection**: Common patterns not in .gitignore.

**Fix Strategy**: Add comprehensive patterns.

```gitignore
# Editor artifacts
*.swp
*.swo
*~
*.bak
*.orig

# OS files
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.sublime-*

# Build outputs
dist/
build/
*.tsbuildinfo

# Dependencies
node_modules/

# Environment
.env
.env.*
!.env.example

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Test coverage
coverage/
.nyc_output/

# Cache
.cache/
.eslintcache
.parcel-cache/
```

**Template**: See `templates/gitignore-node.txt` for complete Node.js template.

---

### Husky Prepare Script Silent Failure (#37 - 1 occurrence)

**Detection**: `prepare` script uses `|| true` fallback.

**Pattern**: Hook installation fails silently.

```json
// PROBLEM - hides failures
{
  "scripts": {
    "prepare": "husky install || true"
  }
}
```

**Fix Strategy 1**: Conditional execution based on CI.

```json
// SOLUTION - check CI environment
{
  "scripts": {
    "prepare": "node -e \"if (process.env.CI !== 'true') require('husky').install()\""
  }
}
```

**Fix Strategy 2**: Use is-ci package.

```bash
npm install --save-dev is-ci
```

```json
{
  "scripts": {
    "prepare": "is-ci || husky install"
  }
}
```

**Fix Strategy 3**: Husky v9+ auto-setup.

```json
// Husky v9 uses .husky/_/husky.sh automatically
{
  "scripts": {
    "prepare": "husky"
  }
}
```

---

### Permissive lint:strict Threshold (#38 - 1 occurrence)

**Detection**: High `--max-warnings` value in lint script.

**Pattern**: Too many warnings allowed.

```json
// PROBLEM - too permissive
{
  "scripts": {
    "lint:strict": "eslint . --max-warnings 500"
  }
}
```

**Fix Strategy**: Progressive reduction.

```json
// Week 1: Lower to current count + small buffer
{
  "scripts": {
    "lint:strict": "eslint . --max-warnings 350"
  }
}

// Week 2: Lower further
{
  "scripts": {
    "lint:strict": "eslint . --max-warnings 200"
  }
}

// Target: Zero tolerance
{
  "scripts": {
    "lint:strict": "eslint . --max-warnings 0"
  }
}
```

**Tracking Progress**:

```bash
# Get current warning count
npx eslint . 2>&1 | tail -1
# Output: "X warnings" or "X problems (Y errors, Z warnings)"
```

---

### ESLint Config Duplication (#39, #40)

**Issue #39**: Repeated plugin/globals definitions.

```typescript
// PROBLEM - repeated in multiple blocks
export default [
  {
    files: ['**/*.ts'],
    plugins: { '@typescript-eslint': tsPlugin },
  },
  {
    files: ['**/*.tsx'],
    plugins: { '@typescript-eslint': tsPlugin },  // Duplicated
  },
];
```

**Fix Strategy**: Extract shared config.

```typescript
// SOLUTION - shared base config
const baseTypescriptConfig = {
  plugins: {
    '@typescript-eslint': tsPlugin,
  },
  languageOptions: {
    parser: tsParser,
    parserOptions: {
      project: './tsconfig.json',
    },
  },
};

export default [
  {
    files: ['**/*.ts'],
    ...baseTypescriptConfig,
    rules: { /* ts-specific rules */ },
  },
  {
    files: ['**/*.tsx'],
    ...baseTypescriptConfig,
    rules: { /* tsx-specific rules */ },
  },
];
```

**Issue #40**: Disabled rules duplicated across blocks.

```typescript
// PROBLEM - duplicated disabled rules
{
  rules: {
    '@typescript-eslint/no-explicit-any': 'off',
    '@typescript-eslint/no-unsafe-assignment': 'off',
  },
},
```

**Fix Strategy**: Extract to named constant with documentation.

```typescript
// SOLUTION - extracted with docs
/**
 * Rules disabled during migration to strict TypeScript.
 * TODO: Re-enable progressively - see issue #456
 */
const migrationDisabledRules = {
  '@typescript-eslint/no-explicit-any': 'off',
  '@typescript-eslint/no-unsafe-assignment': 'off',
  '@typescript-eslint/no-unsafe-member-access': 'off',
} as const;

export default [
  {
    files: ['**/*.ts'],
    rules: {
      ...migrationDisabledRules,
      // ts-specific rules
    },
  },
];
```

---

### Recursive Directory Walking Without Limits (#23 - 1 occurrence)

**Pattern**: Unbounded recursion in file walking.

```typescript
// PROBLEM - no limits
async function walkDir(dir: string): Promise<string[]> {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    if (entry.isDirectory()) {
      files.push(...await walkDir(path.join(dir, entry.name))); // No limit!
    }
  }
  return files;
}
```

**Fix Strategy**: Add depth limit and visited tracking.

```typescript
// SOLUTION - with limits
interface WalkOptions {
  maxDepth?: number;
  maxFiles?: number;
}

async function walkDir(
  dir: string,
  options: WalkOptions = {},
  depth = 0,
  visited = new Set<string>()
): Promise<string[]> {
  const { maxDepth = 10, maxFiles = 10000 } = options;

  if (depth > maxDepth) {
    return [];
  }

  const realPath = await fs.realpath(dir);
  if (visited.has(realPath)) {
    return []; // Circular symlink
  }
  visited.add(realPath);

  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files: string[] = [];

  for (const entry of entries) {
    if (files.length >= maxFiles) break;

    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...await walkDir(fullPath, options, depth + 1, visited));
    } else {
      files.push(fullPath);
    }
  }

  return files;
}
```

---

### Regex Created Per-Match (#24 - 1 occurrence)

**Pattern**: Regex compiled on every function call.

```typescript
// PROBLEM - regex created every call
function containsKeyword(text: string, keyword: string): boolean {
  const regex = new RegExp(`\\b${keyword}\\b`, 'i');
  return regex.test(text);
}
```

**Fix Strategy**: Pre-compile and cache.

```typescript
// SOLUTION - cached regex
const keywordRegexCache = new Map<string, RegExp>();

function getKeywordRegex(keyword: string): RegExp {
  let regex = keywordRegexCache.get(keyword);
  if (!regex) {
    regex = new RegExp(`\\b${escapeRegex(keyword)}\\b`, 'i');
    keywordRegexCache.set(keyword, regex);
  }
  return regex;
}

function escapeRegex(str: string): string {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function containsKeyword(text: string, keyword: string): boolean {
  return getKeywordRegex(keyword).test(text);
}
```

---

## Scripts

### Check Config Hygiene

```bash
node scripts/check-config.js
```

### Fix Gitignore

```bash
node scripts/fix-gitignore.js
```

---

## Templates

### Node.js .gitignore

See `templates/gitignore-node.txt`

### ESLint Base Config

See `templates/eslint-base.js`

---

## CI/CD Considerations

### Ensuring Hooks Run

```yaml
# GitHub Actions
- name: Install dependencies
  run: npm ci

# This runs "prepare" script which installs husky
# Make sure CI=true is set to skip if needed
```

### Lint in CI

```yaml
- name: Lint
  run: npm run lint:strict
  # Fails if warnings exceed threshold
```

### Progressive Strictness

```yaml
# Allow gradual improvement
- name: Check lint progress
  run: |
    WARNINGS=$(npx eslint . 2>&1 | grep -oP '\d+ warning' | grep -oP '\d+' || echo "0")
    THRESHOLD=200
    if [ "$WARNINGS" -gt "$THRESHOLD" ]; then
      echo "Too many warnings: $WARNINGS (max: $THRESHOLD)"
      exit 1
    fi
```
