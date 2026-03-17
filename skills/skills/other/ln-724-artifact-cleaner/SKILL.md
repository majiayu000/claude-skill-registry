---
name: ln-724-artifact-cleaner
description: "Universal platform artifact cleaner: Replit, StackBlitz, CodeSandbox, Glitch"
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-724-artifact-cleaner

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-720-structure-migrator

Removes platform-specific artifacts from projects exported from online platforms, preparing them for production deployment.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project directory, platform (auto-detect or manual) |
| **Output** | Clean project without platform dependencies |
| **Platforms** | Replit, StackBlitz, CodeSandbox, Glitch |
| **Duration** | ~2-5 minutes |
| **Invocation** | Called from ln-720 (TRANSFORM mode, conditional) or user-invocable |

**Invocation conditions:**
- TRANSFORM mode only (SKIP in CREATE mode)
- At least one platform detected
- User confirmation before cleanup

---

## Platform Support Matrix

| Platform | Config Files | Directories | NPM Packages | Build Config | Comments |
|----------|-------------|-------------|--------------|--------------|----------|
| **Replit** | `.replit`, `replit.nix` | `.local/`, `.cache/`, `.upm/` | `@replit/*` | `REPL_ID` checks | `// @replit` |
| **StackBlitz** | `.stackblitzrc` | `.turbo/` | -- | Port overrides | -- |
| **CodeSandbox** | `sandbox.config.json` | `.codesandbox/` | -- | CSB env checks | -- |
| **Glitch** | `glitch.json`, `.glitch-assets` | `.glitch/`, `.data/` | -- | Glitch env vars | -- |

**Reference:** [platform_artifacts.md](references/platform_artifacts.md)

---

## Workflow

```
Phase 1: Detect & Scan
    |
    +---> 1.0 Detect platforms (auto-detect by config files)
    +---> 1.1 Scan platform-specific artifacts
    |
    v
Phase 2: Preview
    |
    v
Phase 3: Confirm
    |
    v
Phase 4: Execute (per detected platform)
    |
    +---> 4.1 Delete files/directories
    +---> 4.2 Modify package.json
    +---> 4.3 Modify build config (vite/webpack)
    +---> 4.4 Remove platform comments
    +---> 4.5 Modify .gitignore
    |
    v
Phase 5: Verify & Report
```

---

## Phase 1: Detect & Scan

### Step 1.0: Platform Detection

| Platform | Primary Indicator | Confidence |
|----------|-------------------|------------|
| Replit | `.replit` file | 100% |
| StackBlitz | `.stackblitzrc` | 100% |
| CodeSandbox | `sandbox.config.json` | 100% |
| Glitch | `glitch.json` | 100% |

**Output:**
```yaml
Detected Platforms:
  - replit (confidence: 100%)
```

### Step 1.1: Scan Artifacts

Per detected platform, scan for artifacts using platform-specific detection rules.

**Replit Detection Rules:**
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

**StackBlitz/CodeSandbox/Glitch:** **MANDATORY READ:** Load [platform_artifacts.md](references/platform_artifacts.md) for detection rules.

### Scan Output Format

```yaml
Scan Results:
  Platform: Replit
  Files Found: 2
    - .replit (729 bytes)
    - vite-plugin-meta-images.ts (2333 bytes)
  Directories Found: 1
    - .local/ (6 files, 589KB)
  Package Dependencies: 3
    - @replit/vite-plugin-cartographer
    - @replit/vite-plugin-dev-banner
    - @replit/vite-plugin-runtime-error-modal
  Build Config Modifications: 4
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

Show detailed preview of changes per platform.

```yaml
Will DELETE files:
  - .replit (729 bytes)
  - vite-plugin-meta-images.ts (2333 bytes)
Will DELETE directories:
  - .local/ (6 files, 589KB)
Will MODIFY files:
  - package.json: Remove 3 @replit/* devDependencies
  - vite.config.ts: Remove 4 imports/plugins/blocks
  - 2 UI files: Remove 10 @replit comments
  - .gitignore: Remove ".replit" line

Summary: 2 files deleted, 1 directory deleted, 5 files modified
```

---

## Phase 3: Confirm

```
Proceed with platform cleanup (Replit)? [Y/n]
```

**Options:**
- **Y (default):** Execute cleanup
- **n:** Cancel operation
- **Custom exclusions:** User can specify files to skip

---

## Phase 4: Execute

### Platform Router

Based on detected platforms, dispatch to platform-specific cleanup. Execute sequentially if multiple platforms detected.

### 4.1 Replit Cleanup (Primary)

**Delete files/directories:**
```bash
rm -f .replit replit.nix .replit.nix
rm -f vite-plugin-meta-images.ts
rm -rf .local/ .cache/ .upm/ .breakpoints
```

**Modify package.json:** Remove keys starting with `@replit/` from devDependencies.

**Modify vite.config.ts:**
- Remove `@replit/*` imports
- Remove Replit plugins from plugins array
- Remove `REPL_ID` conditional blocks

**Remove `// @replit` comments:** Grep `// @replit.*$` in `**/*.tsx`, `**/*.ts`, `**/*.jsx`, `**/*.js`.

**Modify .gitignore:** Remove `.replit` line.

### 4.2 StackBlitz Cleanup

```bash
rm -f .stackblitzrc
rm -rf .turbo/  # Only if not used in production
```

### 4.3 CodeSandbox Cleanup

```bash
rm -f sandbox.config.json
rm -rf .codesandbox/
```
Remove `"sandbox"` field from package.json (if exists).

### 4.4 Glitch Cleanup

```bash
rm -f glitch.json .glitch-assets
rm -rf .glitch/
# .data/ - ASK USER before deleting (may contain important data)
```
Remove Glitch env var checks (`PROJECT_DOMAIN`, `ASSETS_URL`) from server code.

---

## Phase 5: Verify & Report

```yaml
Cleanup Complete!

Platforms Cleaned: Replit

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
  3. Commit: git add . && git commit -m "chore: remove platform artifacts"
```

---

## Edge Cases

| Case | Handling |
|------|----------|
| No platform artifacts found | Report "Project is clean" and exit |
| Multiple platforms detected | Clean each sequentially, separate reports |
| Project uses Webpack (not Vite) | Search `webpack.config.*` instead |
| No package.json | Skip NPM cleanup phase |
| `.data/` directory (Glitch) | Ask user before deleting (may contain data) |

---

## Error Handling

| Error | Action |
|-------|--------|
| Permission denied | Log error, suggest `chmod` or admin rights |
| File in use | Retry after delay, then warn user |
| JSON parse error | Log error, suggest manual fix |
| Build config syntax error | Log error, suggest manual fix |

---

## Integration

### With ln-720-structure-migrator

Called conditionally in TRANSFORM mode:

```yaml
ln-720-structure-migrator:
  Phase 1: Detect project type + platform
  Phase 2: Clean artifacts (ln-724-artifact-cleaner)  # CONDITIONAL
    Condition: Platform detected (Replit/StackBlitz/CodeSandbox/Glitch)
    Skipped if: CREATE mode OR no platform markers
  Phase 3: Restructure frontend (ln-721)
  Phase 4: Generate backend (ln-722)
  Phase 5: Generate seed data (ln-723)
```

### Standalone Usage

```
User: Clean my project from platform artifacts
Claude: Invokes ln-724-artifact-cleaner
```

---

## Critical Rules

- **Conditional Invocation:** Only run when platform artifacts detected, SKIP in CREATE mode
- **User Confirmation:** Always preview and confirm before deleting
- **No Data Loss:** Ask user before deleting directories that may contain user data (.data/)
- **Build Verification:** Recommend `npm run build` after cleanup
- **Idempotent:** Re-running on clean project reports "no artifacts found"

---

## References

- [platform_artifacts.md](references/platform_artifacts.md) - Per-platform artifact catalog

---

## Definition of Done

- At least one platform detected (Replit/StackBlitz/CodeSandbox/Glitch)
- All platform artifacts scanned and previewed to user
- User confirmation received before any deletions
- Platform files, directories, dependencies, build config, and comments cleaned
- .gitignore entries for platform files removed
- Cleanup report generated with deleted/modified file counts

---

**Version:** 2.0.0
**Last Updated:** 2026-02-07
