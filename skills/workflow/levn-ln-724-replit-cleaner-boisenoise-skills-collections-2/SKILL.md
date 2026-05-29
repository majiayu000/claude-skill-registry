---
name: ln-724-replit-cleaner
description: Removes all Replit artifacts from exported projects (configs, packages, code comments)
---

# ln-724-replit-cleaner

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-720-structure-migrator

Completely removes Replit-specific artifacts from projects exported from Replit, preparing them for production deployment elsewhere.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project directory (Replit export) |
| **Output** | Clean project without Replit dependencies |
| **Duration** | ~2-5 minutes |
| **Invocation** | Called from ln-720-structure-migrator or user-invocable |

---

## Artifacts Removed

| Category | Artifacts | Action |
|----------|-----------|--------|
| **Config Files** | `.replit`, `replit.nix`, `.replit.nix` | DELETE |
| **Directories** | `.local/`, `.cache/`, `.upm/`, `.breakpoints` | DELETE |
| **NPM Packages** | `@replit/vite-plugin-*` | REMOVE from package.json |
| **Vite Config** | Imports, plugins, `REPL_ID` checks | MODIFY vite.config.ts |
| **Custom Plugins** | `vite-plugin-meta-images.ts` (Replit-specific) | DELETE |
| **Code Comments** | `// @replit` annotations | REMOVE |
| **.gitignore** | `.replit` entry | REMOVE line |

---

## Workflow

```
Phase 1: Scan
    |
    v
Phase 2: Preview
    |
    v
Phase 3: Confirm
    |
    v
Phase 4: Execute
    |
    +---> 4.1 Delete files/directories
    +---> 4.2 Modify package.json
    +---> 4.3 Modify vite.config.ts
    +---> 4.4 Remove @replit comments
    +---> 4.5 Modify .gitignore
    |
    v
Phase 5: Verify & Report
```

---

## Phase 1: Scan

Detect all Replit artifacts in the project.

### Detection Rules

```yaml
Files:
  - Glob: .replit, replit.nix, .replit.nix
  - Glob: vite-plugin-meta-images.ts (if uses REPLIT_* env vars)

Directories:
  - Glob: .local/, .cache/, .upm/, .breakpoints

Package.json:
  - Grep: "@replit/" in devDependencies

Vite Config:
  - Grep: "@replit/" imports
  - Grep: "REPL_ID" or "REPLIT_" environment checks

Code:
  - Grep: "// @replit" comments in *.tsx, *.ts, *.jsx, *.js

.gitignore:
  - Grep: "^\.replit$" line
```

### Output Format

```yaml
Scan Results:
  Files Found: 2
    - .replit (729 bytes)
    - vite-plugin-meta-images.ts (2333 bytes)

  Directories Found: 1
    - .local/ (6 files, 589KB)

  Package Dependencies: 3
    - @replit/vite-plugin-cartographer
    - @replit/vite-plugin-dev-banner
    - @replit/vite-plugin-runtime-error-modal

  Vite Config Modifications: 4
    - Import: runtimeErrorOverlay
    - Import: metaImagesPlugin
    - Plugin: runtimeErrorOverlay()
    - Block: REPL_ID conditional (lines 14-24)

  Code Comments: 10
    - button.tsx: 5 comments
    - badge.tsx: 5 comments

  Gitignore Entries: 1
    - .replit
```

---

## Phase 2: Preview

Show detailed preview of changes.

```yaml
Will DELETE files:
  - .replit (729 bytes)
  - vite-plugin-meta-images.ts (2333 bytes)

Will DELETE directories:
  - .local/ (6 files, 589KB)

Will MODIFY files:
  - package.json: Remove 3 @replit/* devDependencies
  - vite.config.ts: Remove 4 imports/plugins/blocks
  - client/src/components/ui/button.tsx: Remove 5 @replit comments
  - client/src/components/ui/badge.tsx: Remove 5 @replit comments
  - .gitignore: Remove ".replit" line

Summary: 2 files deleted, 1 directory deleted, 5 files modified
```

---

## Phase 3: Confirm

Request user confirmation before making changes.

```
Proceed with Replit cleanup? [Y/n]
```

**Options:**
- **Y (default):** Execute cleanup
- **n:** Cancel operation
- **Custom exclusions:** User can specify files to skip

---

## Phase 4: Execute

### 4.1 Delete Files and Directories

```bash
# Delete config files
rm -f .replit replit.nix .replit.nix

# Delete Replit-specific plugin
rm -f vite-plugin-meta-images.ts

# Delete Replit directories
rm -rf .local/ .cache/ .upm/ .breakpoints
```

### 4.2 Modify package.json

Remove from `devDependencies`:

```json
{
  "devDependencies": {
    "@replit/vite-plugin-cartographer": "^0.4.4",
    "@replit/vite-plugin-dev-banner": "^0.1.1",
    "@replit/vite-plugin-runtime-error-modal": "^0.0.4"
  }
}
```

**Method:** JSON parse, filter keys starting with `@replit/`, serialize.

### 4.3 Modify vite.config.ts

**Remove imports:**
```typescript
// REMOVE
import runtimeErrorOverlay from "@replit/vite-plugin-runtime-error-modal";
import { metaImagesPlugin } from "./vite-plugin-meta-images";
```

**Remove from plugins array:**
```typescript
// REMOVE
runtimeErrorOverlay(),
metaImagesPlugin(),
```

**Remove REPL_ID conditional block:**
```typescript
// REMOVE entire block
...(process.env.NODE_ENV !== "production" &&
process.env.REPL_ID !== undefined
  ? [
      await import("@replit/vite-plugin-cartographer").then((m) =>
        m.cartographer(),
      ),
      await import("@replit/vite-plugin-dev-banner").then((m) =>
        m.devBanner(),
      ),
    ]
  : []),
```

### 4.4 Remove @replit Comments

**Pattern:** `// @replit.*$`

**Files:** `**/*.tsx`, `**/*.ts`, `**/*.jsx`, `**/*.js`

**Method:** Read file, remove lines containing `// @replit`, preserve indentation and structure.

### 4.5 Modify .gitignore

**Remove line:** `.replit`

---

## Phase 5: Verify & Report

### Final Report

```yaml
Cleanup Complete!

Deleted:
  - .replit
  - vite-plugin-meta-images.ts
  - .local/ (6 files)

Modified:
  - package.json (removed 3 dependencies)
  - vite.config.ts (removed 4 imports/plugins)
  - button.tsx (removed 5 comments)
  - badge.tsx (removed 5 comments)
  - .gitignore (removed 1 line)

Next Steps:
  1. Run `npm install` to update package-lock.json
  2. Run `npm run build` to verify build works
  3. Commit: git add . && git commit -m "chore: remove Replit artifacts"
```

---

## Edge Cases

| Case | Handling |
|------|----------|
| No Replit artifacts found | Report "Project is clean" and exit |
| Project uses Webpack (not Vite) | Search `webpack.config.*` instead |
| Project uses other bundlers | Search common config patterns |
| No package.json | Skip NPM cleanup phase |
| Protected files | Ask user before modifying |

---

## Error Handling

| Error | Action |
|-------|--------|
| Permission denied | Log error, suggest `chmod` or admin rights |
| File in use | Retry after delay, then warn user |
| JSON parse error | Log error, suggest manual fix |
| Vite config syntax error | Log error, suggest manual fix |

---

## Integration

### With ln-720-structure-migrator

Called as first step before restructuring:

```yaml
ln-720-structure-migrator:
  Phase 1: Detect project type
  Phase 2: Clean Replit artifacts (ln-724-replit-cleaner)  # THIS SKILL
  Phase 3: Restructure frontend (ln-721)
  Phase 4: Generate backend (ln-722)
  Phase 5: Migrate mock data (ln-723)
```

### Standalone Usage

```
User: Clean my project from Replit
Claude: Invokes ln-724-replit-cleaner
```

---

## References

- [replit_artifacts.md](references/replit_artifacts.md) - Complete artifact list by category

---

**Version:** 1.0.0
**Last Updated:** 2026-01-10
