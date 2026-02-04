---
name: gitignore-hygiene
description: |
  Automatic gitignore maintenance and cleanup. Use when: (1) after commits,
  (2) new file types appear in project, (3) build artifacts get committed,
  (4) before pushing to remote. Scans for unwanted files and suggests
  gitignore additions.
category: development
user-invocable: true
---

# Gitignore Hygiene

Maintains gitignore patterns and cleans cached files from git tracking.

## Trigger Conditions

Invoke when:
- After making commits
- New file types appear (build artifacts, logs)
- Before pushing to remote
- User says "check gitignore", "clean git"

Also invoke explicitly with:
- `/gitignore-hygiene`
- "clean up gitignore"
- "check for unwanted files"

## Procedure

### Step 1: Scan for Unwanted Files

Check for common patterns that should be ignored:

```bash
# Check for tracked files that should be ignored
git ls-files | grep -E '\.(log|env|pem|key)$'
git ls-files | grep -E '^(node_modules|dist|build|coverage)/'
```

### Step 2: Check Current Gitignore

Read .gitignore and identify missing patterns:

| Category | Patterns to Check |
|----------|-------------------|
| Dependencies | node_modules/, .pnpm-store/, vendor/ |
| Build | dist/, build/, .svelte-kit/, .next/, .nuxt/ |
| Test | coverage/, test-results/, playwright-report/ |
| IDE | .idea/, .vscode/, *.swp |
| OS | .DS_Store, Thumbs.db |
| Environment | .env, .env.local, .env.*.local |
| Logs | *.log, npm-debug.log* |
| Cache | .cache/, .turbo/, .eslintcache |
| Credentials | *.pem, *.key, credentials.json |

### Step 3: Detect Project Type

Adjust patterns based on detected stack:

**Node.js / TypeScript:**
```gitignore
node_modules/
dist/
.turbo/
```

**Svelte / SvelteKit:**
```gitignore
.svelte-kit/
build/
```

**Next.js:**
```gitignore
.next/
out/
```

**Python:**
```gitignore
__pycache__/
*.pyc
.venv/
.pytest_cache/
```

**Rust:**
```gitignore
target/
Cargo.lock  # for libraries
```

### Step 4: Report Findings

**If issues found:**

```
Gitignore hygiene check:

Missing patterns:
  + coverage/          (test artifacts)
  + playwright-report/ (test artifacts)
  + .turbo/            (cache)

Tracked files that should be ignored:
  - coverage/lcov.info
  - test-results/results.xml

Recommended actions:
1. Add missing patterns to .gitignore
2. Remove cached files from tracking

Run: git rm -r --cached coverage/ test-results/
```

**If no issues:**

```
Gitignore hygiene check: All clear

No unwanted files tracked.
All common patterns present.
```

### Step 5: Apply Fixes (With Confirmation)

**Add missing patterns:**
```bash
echo "coverage/" >> .gitignore
echo "test-results/" >> .gitignore
```

**Remove cached files:**
```bash
git rm -r --cached coverage/
git rm -r --cached test-results/
```

**Commit the cleanup:**
```bash
git add .gitignore
git commit -m "chore: update gitignore patterns

Added:
- coverage/
- test-results/
- playwright-report/

Removed from tracking:
- coverage/lcov.info
- test-results/results.xml

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Pattern Categories

### Always Include

These patterns should be in every project:

```gitignore
# OS files
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
```

### Language-Specific

**Node.js:**
```gitignore
node_modules/
.pnpm-store/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

**TypeScript:**
```gitignore
dist/
*.tsbuildinfo
```

**Testing:**
```gitignore
coverage/
.nyc_output/
test-results/
playwright-report/
```

### Framework-Specific

**SvelteKit:**
```gitignore
.svelte-kit/
build/
```

**Next.js:**
```gitignore
.next/
out/
```

**Vite:**
```gitignore
dist/
.vite/
```

## Dangerous Patterns

Never ignore these (warn if present):

| Pattern | Risk |
|---------|------|
| `src/` | Ignoring source code |
| `*.ts` | Ignoring all TypeScript |
| `package.json` | Ignoring manifest |
| `.gitignore` | Recursive ignore |

## Skill Chaining

### After Commits

Run hygiene check after commits to catch:
- Accidentally committed build artifacts
- Missing patterns for new file types

### Before Push

Run hygiene check before pushing:
- Ensure no credentials are tracked
- Verify build artifacts are ignored

### With project-init

project-init creates comprehensive .gitignore. This skill maintains it over time.

### Terminal Chain

After any commit session: **repo-hygiene** (final cleanup)

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Just one file" | One file becomes many | Add pattern |
| "I'll clean later" | Later is never | Clean now |
| "It's not sensitive" | Build artifacts bloat repo | Remove from tracking |
| "Gitignore is fine" | Projects evolve | Verify regularly |

## Example Session

```
/gitignore-hygiene

Scanning project...

Found issues:

1. Missing patterns:
   + .turbo/           (detected turbo usage)
   + playwright-report/ (detected playwright)

2. Tracked files to remove:
   - .turbo/cache/abc123
   - playwright-report/index.html

Actions:
[1] Add patterns to .gitignore
[2] Remove cached files
[3] Skip

> 1

Updated .gitignore with:
  + .turbo/
  + playwright-report/

> 2

Removed from tracking:
  - .turbo/cache/ (42 files)
  - playwright-report/ (15 files)

Ready to commit? [y/n]
```

## Notes

- Never modifies .git directory
- Preserves existing .gitignore structure
- Warns about potentially dangerous patterns
- Creates backup before modifying
- Works with both root and package gitignores in monorepos
