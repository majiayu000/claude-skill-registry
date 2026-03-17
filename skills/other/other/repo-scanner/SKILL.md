---
name: repo-scanner
description: Deep scan repository structure to extract metadata, detect frameworks, and identify domain boundaries. Use when starting assimilation, analyzing a new codebase, or gathering project context.
metadata:
  phase: 1
  pipeline: assimilation
  version: 1.0.0
---

# Repo Scanner

## Overview

Scan a repository's structure to produce a comprehensive report without reading all source code. This is phase 1 of the assimilation pipeline—gathering metadata that subsequent phases consume.

---

## When to Use

Use this skill when:
- Starting assimilation of a new repository
- Analyzing an unfamiliar codebase
- Gathering project context before making changes
- Detecting frameworks and tooling

---

## Output

**File:** `.github/temp/scan-report.json`

The scan produces a structured report consumed by pattern-extractor (phase 2).

---

## Execution Steps

### Step 1: Create Temp Directory

```bash
mkdir -p .github/temp
```

### Step 2: Apply Ignore Patterns

**MUST skip these directories entirely:**

```
node_modules/    vendor/         .venv/          __pycache__/
dist/            build/          .next/          target/
coverage/        .git/           out/            .cache/
.turbo/          .parcel-cache/  .nuxt/          .output/
```

**Note existence but don't analyze content:**

```
package-lock.json    yarn.lock       pnpm-lock.yaml
Cargo.lock           poetry.lock     go.sum
```

### Step 3: Prioritize Files

Read files in this order (most important first):

| Priority | File Types | Examples | Why |
|----------|------------|----------|-----|
| 1 | Config files | package.json, tsconfig.json, pyproject.toml, Cargo.toml, go.mod | Define project type |
| 2 | Entry points | main.ts, index.js, app.py, main.go, lib.rs, src/index.* | Core application logic |
| 3 | README | README.md, README.rst, README.txt | Project documentation |
| 4 | Shallow files | Files at depth 1-2 from root | High-level structure |
| 5 | Source files | src/**/*.{ts,js,py,go,rs} (skip *test*, *spec*) | Implementation |

**File size limit:** SHOULD skip files >10KB (likely generated or data files)

### Step 4: Detect Language

Check config files to determine primary language:

| Config File | Language |
|-------------|----------|
| package.json | JavaScript/TypeScript |
| tsconfig.json | TypeScript |
| pyproject.toml, setup.py, requirements.txt | Python |
| Cargo.toml | Rust |
| go.mod | Go |
| pom.xml, build.gradle | Java |
| Gemfile | Ruby |
| composer.json | PHP |

**Rule:** Prefer config-based detection over file extension counting.

### Step 5: Detect Framework

Check dependencies in config files:

#### JavaScript/TypeScript (package.json)

| Check `dependencies` for | Framework |
|--------------------------|-----------|
| `next` | Next.js |
| `react` | React |
| `vue` | Vue.js |
| `@angular/core` | Angular |
| `express` | Express.js |
| `fastify` | Fastify |
| `@nestjs/core` | NestJS |
| `hono` | Hono |
| `koa` | Koa |

#### Python (pyproject.toml / requirements.txt)

| Check for | Framework |
|-----------|-----------|
| `django` | Django |
| `fastapi` | FastAPI |
| `flask` | Flask |
| `starlette` | Starlette |
| `tornado` | Tornado |

#### Rust (Cargo.toml)

| Check `dependencies` for | Framework |
|--------------------------|-----------|
| `actix-web` | Actix |
| `axum` | Axum |
| `rocket` | Rocket |
| `warp` | Warp |

#### Go (go.mod)

| Check for | Framework |
|-----------|-----------|
| `github.com/gin-gonic/gin` | Gin |
| `github.com/labstack/echo` | Echo |
| `github.com/gofiber/fiber` | Fiber |

### Step 6: Detect Project Type

Infer project type from structure and config:

| Indicators | Type |
|------------|------|
| `bin` in package.json, CLI-related deps | `cli` |
| `main` field, no `bin`, library deps | `library` |
| Framework detected (Next, Express, etc.) | `web-app` |
| Only test files, no src | `test-suite` |
| `@types/*` only, `.d.ts` files | `types` |
| Unclear | `application` |

### Step 7: Identify Domain Boundaries

**Known domain patterns:**

```
api, auth, backend, frontend, core, common, shared,
services, handlers, controllers, models, views, routes,
components, hooks, utils, lib, pkg, internal, cmd,
modules, features, domains, entities, repositories
```

**Algorithm:**

1. List all top-level directories
2. For each directory:
   - Count files (excluding test files)
   - Check if name matches known pattern
3. Mark as domain if: `matches_pattern AND file_count > 5`

### Step 8: Detect Tooling

Check package.json scripts or config files:

| Tool Type | How to Detect |
|-----------|---------------|
| Test | `scripts.test`, jest.config, vitest.config, pytest.ini |
| Lint | `scripts.lint`, .eslintrc, .pylintrc, rustfmt.toml |
| Build | `scripts.build`, webpack.config, vite.config, tsconfig.json |
| Format | `scripts.format`, .prettierrc, .editorconfig |

### Step 9: Generate Report

Create `.github/temp/scan-report.json`:

```json
{
  "name": "<repo-name>",
  "type": "<cli|library|web-app|application|types|test-suite>",
  "language": "<JavaScript|TypeScript|Python|Rust|Go|Java|Ruby|PHP>",
  "framework": "<detected-framework-or-null>",
  "structure": {
    "type": "<flat|nested|monorepo>",
    "depth": <max-directory-depth>,
    "mainDirs": ["<top-level-dirs>"],
    "entryPoints": ["<detected-entry-files>"]
  },
  "domains": [
    {
      "name": "<domain-name>",
      "path": "<relative-path>",
      "files": <file-count>
    }
  ],
  "tools": {
    "test": "<test-command-or-null>",
    "lint": "<lint-command-or-null>",
    "build": "<build-command-or-null>",
    "format": "<format-command-or-null>"
  },
  "docs": ["<doc-files-found>"],
  "metadata": {
    "scanned_at": "<ISO-timestamp>",
    "scanner_version": "1.0.0",
    "files_analyzed": <count>,
    "files_skipped": <count>
  }
}
```

### Step 10: Report Completion

After generating the report, output:

```
✅ Scan complete: <repo-name>
   Language: <language>
   Framework: <framework>
   Type: <type>
   Domains: <count>
   Files analyzed: <count>
   
   Report: .github/temp/scan-report.json
```

---

## Error Handling

| Condition | Action |
|-----------|--------|
| No config files found | Set language="Unknown", continue with file extension analysis |
| Directory is empty | FAIL with error: "Empty directory, nothing to scan" |
| Permission denied | Skip file, log warning, continue |
| File too large (>10KB) | Skip file, increment `files_skipped` |

**On failure, produce error report:**

```json
{
  "error": true,
  "message": "<error-description>",
  "phase": "repo-scanner",
  "timestamp": "<ISO-timestamp>"
}
```

---

## Examples

### Example 1: Scanning an Express.js Project

**Input:** Repository with package.json containing express dependency

**Output:**
```json
{
  "name": "my-api",
  "type": "web-app",
  "language": "JavaScript",
  "framework": "Express.js",
  "structure": {
    "type": "nested",
    "depth": 4,
    "mainDirs": ["src", "tests", "docs"],
    "entryPoints": ["src/index.js", "src/app.js"]
  },
  "domains": [
    { "name": "routes", "path": "src/routes", "files": 8 },
    { "name": "controllers", "path": "src/controllers", "files": 6 },
    { "name": "models", "path": "src/models", "files": 4 }
  ],
  "tools": {
    "test": "npm test",
    "lint": "npm run lint",
    "build": null
  },
  "docs": ["README.md", "API.md"],
  "metadata": {
    "scanned_at": "2026-01-25T10:30:00Z",
    "scanner_version": "1.0.0",
    "files_analyzed": 45,
    "files_skipped": 3
  }
}
```

### Example 2: Scanning a Python CLI

**Input:** Repository with pyproject.toml and click dependency

**Output:**
```json
{
  "name": "my-cli",
  "type": "cli",
  "language": "Python",
  "framework": null,
  "structure": {
    "type": "flat",
    "depth": 2,
    "mainDirs": ["src", "tests"],
    "entryPoints": ["src/main.py", "src/cli.py"]
  },
  "domains": [
    { "name": "commands", "path": "src/commands", "files": 5 }
  ],
  "tools": {
    "test": "pytest",
    "lint": "ruff check .",
    "build": "python -m build"
  },
  "docs": ["README.md"],
  "metadata": {
    "scanned_at": "2026-01-25T10:35:00Z",
    "scanner_version": "1.0.0",
    "files_analyzed": 18,
    "files_skipped": 0
  }
}
```

---

## Conventions

✅ **Do:**
- Check config files before inferring from extensions
- Skip large files to avoid wasting context
- Include metadata for debugging
- Report both analyzed and skipped counts

❌ **Don't:**
- Read file contents of all source files (that's pattern-extractor's job)
- Analyze node_modules, vendor, or other dependency directories
- Fail silently—always produce output or error report
- Include absolute paths in report (use relative paths)

---

## Related Skills

- [pattern-extractor](../pattern-extractor/SKILL.md) — Phase 2: Extract patterns from scanned files
- [skill-generator](../skill-generator/SKILL.md) — Phase 3: Generate skills from patterns
- [orchestrator](../orchestrator/SKILL.md) — Coordinates all phases
