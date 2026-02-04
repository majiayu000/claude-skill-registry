---
name: setup-knip
description: Install and configure Knip for dead code detection. Use before running dead-code-hunter or dependency-auditor to ensure Knip is available. Handles installation, configuration creation, and validation.
allowed-tools: Bash, Read, Write, Glob
---

# Setup Knip

Install and configure Knip - the tool for finding unused files, dependencies, and exports in JavaScript/TypeScript projects.

## When to Use

- Before running dead-code-hunter agent
- Before running dependency-auditor agent
- When project doesn't have Knip configured
- When upgrading Knip configuration
- In pre-flight validation of health workflows

## Instructions

### Step 1: Check if Knip is Installed

Check package.json for knip in devDependencies.

**Tools Used**: Read

```bash
# Read package.json and check for knip
```

**Check Logic**:

- If `devDependencies.knip` exists → Knip is installed
- If not found → Need to install

### Step 2: Install Knip if Missing

If Knip is not installed, add it as devDependency.

**Tools Used**: Bash

```bash
# Detect package manager
if [ -f "pnpm-lock.yaml" ]; then
  pnpm add -D knip
elif [ -f "yarn.lock" ]; then
  yarn add -D knip
elif [ -f "bun.lockb" ]; then
  bun add -D knip
else
  npm install -D knip
fi
```

**Expected Output**:

```
+ knip@5.x.x
```

### Step 3: Check for Knip Configuration

Look for existing Knip configuration files.

**Tools Used**: Glob

**Configuration Files** (in priority order):

1. `knip.json`
2. `knip.jsonc`
3. `knip.ts`
4. `knip.config.ts`
5. `knip.config.js`
6. `package.json` (knip field)

### Step 4: Create Default Configuration if Missing

If no configuration found, create `knip.json` with sensible defaults.

**Tools Used**: Write

**Default Configuration for Standard Project**:

```json
{
  "$schema": "https://unpkg.com/knip@5/schema.json",
  "entry": ["src/index.{ts,tsx,js,jsx}", "src/main.{ts,tsx,js,jsx}"],
  "project": ["src/**/*.{ts,tsx,js,jsx}"],
  "ignore": [
    "**/*.d.ts",
    "**/*.test.{ts,tsx}",
    "**/*.spec.{ts,tsx}",
    "**/test/**",
    "**/tests/**",
    "**/__tests__/**",
    "**/node_modules/**"
  ],
  "ignoreDependencies": ["@types/*"]
}
```

**Default Configuration for Next.js Project** (detected by next in dependencies):

```json
{
  "$schema": "https://unpkg.com/knip@5/schema.json",
  "entry": [
    "src/app/**/*.{ts,tsx}",
    "src/pages/**/*.{ts,tsx}",
    "app/**/*.{ts,tsx}",
    "pages/**/*.{ts,tsx}"
  ],
  "project": ["src/**/*.{ts,tsx}", "app/**/*.{ts,tsx}", "pages/**/*.{ts,tsx}"],
  "ignore": ["**/*.d.ts", "**/*.test.{ts,tsx}", "**/*.spec.{ts,tsx}", "**/node_modules/**"],
  "next": {
    "entry": ["next.config.{js,ts,mjs}", "middleware.{js,ts}"]
  }
}
```

**Default Configuration for Monorepo** (detected by workspaces in package.json):

```json
{
  "$schema": "https://unpkg.com/knip@5/schema.json",
  "workspaces": {
    "packages/*": {
      "entry": ["src/index.{ts,tsx,js,jsx}"],
      "project": ["src/**/*.{ts,tsx,js,jsx}"]
    },
    "apps/*": {
      "entry": ["src/index.{ts,tsx,js,jsx}", "src/main.{ts,tsx,js,jsx}"],
      "project": ["src/**/*.{ts,tsx,js,jsx}"]
    }
  },
  "ignore": ["**/*.d.ts", "**/*.test.{ts,tsx}", "**/*.spec.{ts,tsx}", "**/node_modules/**"]
}
```

### Step 5: Add npm Scripts if Missing

Check if package.json has knip scripts, add if missing.

**Tools Used**: Read, Bash

**Scripts to Add**:

```json
{
  "scripts": {
    "knip": "knip",
    "knip:fix": "knip --fix",
    "knip:deps": "knip --dependencies",
    "knip:exports": "knip --exports",
    "knip:files": "knip --files"
  }
}
```

**Add via npm pkg**:

```bash
npm pkg set scripts.knip="knip"
npm pkg set scripts.knip:fix="knip --fix"
npm pkg set scripts.knip:deps="knip --dependencies"
npm pkg set scripts.knip:exports="knip --exports"
npm pkg set scripts.knip:files="knip --files"
```

### Step 6: Validate Installation

Run Knip to verify installation works.

**Tools Used**: Bash

```bash
npx knip --help
```

**Expected**: Help output displayed without errors

### Step 7: Return Result

Return structured result indicating setup status.

**Expected Output**:

```json
{
  "installed": true,
  "version": "5.x.x",
  "config_file": "knip.json",
  "config_created": true,
  "scripts_added": ["knip", "knip:fix", "knip:deps", "knip:exports", "knip:files"],
  "project_type": "nextjs|monorepo|standard",
  "ready": true
}
```

## Error Handling

- **Installation fails**: Return error with package manager output
- **Configuration invalid**: Return error with validation details
- **Permission denied**: Return error suggesting sudo or permission fix
- **Network error**: Return error suggesting offline installation

## Examples

### Example 1: Fresh Project (No Knip)

**Initial State**:

- package.json exists
- No knip in devDependencies
- No knip.json

**Actions**:

1. Install knip via detected package manager
2. Detect project type (standard)
3. Create knip.json with defaults
4. Add npm scripts
5. Validate installation

**Output**:

```json
{
  "installed": true,
  "version": "5.73.3",
  "config_file": "knip.json",
  "config_created": true,
  "scripts_added": ["knip", "knip:fix", "knip:deps", "knip:exports", "knip:files"],
  "project_type": "standard",
  "ready": true
}
```

### Example 2: Next.js Project with Existing Knip

**Initial State**:

- package.json with next dependency
- knip already in devDependencies
- knip.json exists

**Actions**:

1. Detect knip installed (skip installation)
2. Detect existing config (skip creation)
3. Check scripts (add missing)
4. Validate installation

**Output**:

```json
{
  "installed": true,
  "version": "5.73.3",
  "config_file": "knip.json",
  "config_created": false,
  "scripts_added": ["knip:deps"],
  "project_type": "nextjs",
  "ready": true
}
```

### Example 3: Monorepo Project

**Initial State**:

- package.json with workspaces field
- No knip

**Actions**:

1. Detect monorepo (workspaces in package.json)
2. Install knip
3. Create monorepo-specific knip.json
4. Add npm scripts
5. Validate installation

**Output**:

```json
{
  "installed": true,
  "version": "5.73.3",
  "config_file": "knip.json",
  "config_created": true,
  "scripts_added": ["knip", "knip:fix", "knip:deps", "knip:exports", "knip:files"],
  "project_type": "monorepo",
  "ready": true
}
```

## Knip Command Reference

For agents using Knip after setup:

| Command                                   | Purpose                | Use Case                 |
| ----------------------------------------- | ---------------------- | ------------------------ |
| `npx knip`                                | Full analysis          | Complete dead code scan  |
| `npx knip --dependencies`                 | Dependencies only      | dependency-auditor       |
| `npx knip --exports`                      | Exports only           | Unused export detection  |
| `npx knip --files`                        | Files only             | Unused file detection    |
| `npx knip --fix --fix-type exports,types` | Auto-fix exports/types | Safe automated cleanup   |
| `npx knip --fix --fix-type dependencies`  | Auto-fix deps          | Remove from package.json |
| `npx knip --reporter json`                | JSON output            | Machine parsing          |
| `npx knip --reporter compact`             | Compact output         | Quick review             |

## CRITICAL SAFETY WARNING

### NEVER Use `--allow-remove-files`

**`npx knip --fix --allow-remove-files` is FORBIDDEN!**

Knip has a critical limitation: **it cannot detect dynamic imports**.

```typescript
// Knip CANNOT see these relationships:
const module = await import(`./plugins/${name}.ts`);
const Component = lazy(() => import('./components/Dashboard'));
require(`./locales/${lang}.json`);
```

Files loaded via dynamic imports will appear "unused" to Knip but are actually critical!

### Safe Knip Usage

**ALLOWED**:

- `npx knip --fix --fix-type exports` - Safe: removes unused exports from files
- `npx knip --fix --fix-type types` - Safe: removes unused type exports
- `npx knip --fix --fix-type dependencies` - Safe: removes from package.json only

**FORBIDDEN**:

- `npx knip --fix --allow-remove-files` - DANGEROUS: may delete files with dynamic imports
- `npx knip --fix` (without --fix-type) - May include file removal

### Manual Verification Required

Before removing ANY file flagged by Knip:

1. Search for dynamic imports: `import(`, `require(`, `lazy(`, `loadable(`
2. Check for string interpolation in imports
3. Verify no config files reference the file
4. Run build and tests after removal

## Integration with Agents

### dead-code-hunter Pre-Check

```markdown
## Phase 0: Pre-Flight

1. Use setup-knip Skill to ensure Knip is available
2. If result.ready === false, halt with setup instructions
3. If result.ready === true, proceed with detection
```

### dependency-auditor Pre-Check

```markdown
## Phase 1: Environment Analysis

1. Use setup-knip Skill before dependency analysis
2. Knip will detect unused dependencies more accurately than manual grep
```

## Notes

- Knip version 5.x is required (major improvements over v4)
- Configuration is auto-detected for 100+ frameworks
- Monorepo support is first-class
- Use `--reporter json` for machine-readable output
- The `--fix` flag can auto-remove unused exports and dependencies
