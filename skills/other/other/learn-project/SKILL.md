---
name: learn-project
description: Scan project code to detect patterns, dependencies, and conventions. Propose domain rules based on what the code actually does.
context: fork
---

# Learn Project

Scan the current project's source code to detect patterns, classify tooling, and propose domain rules. Unlike `/forge domain extract` (which reads dotforge's internal memory), this skill reads the CODE directly.

## Step 1: Detect dependency files

Read whichever exist (skip missing):

- `package.json` — extract `dependencies` + `devDependencies` keys
- `pyproject.toml` — extract `[project.dependencies]` and `[tool.*]` sections
- `requirements.txt` — read all lines
- `go.mod` — extract `require` block
- `Podfile` — read all lines
- `Gemfile` — read all lines
- `pom.xml` / `build.gradle` / `build.gradle.kts` — extract dependency declarations

Collect a flat list of dependency names.

## Step 2: Scan imports

Find the top 20 most-imported libraries across the codebase:

```bash
# Python
grep -rh "^import \|^from " --include="*.py" . 2>/dev/null | sed 's/import //;s/from //;s/ .*//' | sort | uniq -c | sort -rn | head -20

# TypeScript/JavaScript
grep -rh "from ['\"]" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" . 2>/dev/null | sed "s/.*from ['\"]//;s/['\"].*//" | grep -v '^\.' | sort | uniq -c | sort -rn | head -20

# Go
grep -rh "\"" --include="*.go" . 2>/dev/null | grep -E '^\s+"' | sed 's/.*"//;s/".*//' | sort | uniq -c | sort -rn | head -20

# Swift
grep -rh "^import " --include="*.swift" . 2>/dev/null | sed 's/import //' | sort | uniq -c | sort -rn | head -20
```

## Step 3: Scan project structure

```bash
# Directory structure (2 levels deep, ignore hidden/vendor)
find . -maxdepth 2 -type d ! -path '*/\.*' ! -path '*/node_modules*' ! -path '*/.venv*' ! -path '*/vendor*' ! -path '*/__pycache__*' | sort

# Config files present
ls -1 .eslintrc* .prettierrc* ruff.toml pyproject.toml tsconfig.json biome.json jest.config* vitest.config* vite.config* webpack.config* Makefile Dockerfile docker-compose* .env.example 2>/dev/null
```

## Step 4: Classify patterns

From Steps 1-3, classify into categories. Only report categories with HIGH CONFIDENCE (direct evidence in code):

**ORM/Database:**
- SQLAlchemy (import sqlalchemy, from sqlalchemy)
- Prisma (@prisma/client)
- TypeORM (import { Entity } from "typeorm")
- GORM (gorm.io/gorm)
- Supabase (@supabase/supabase-js, supabase-py)
- Raw SQL (psycopg2, pg, mysql2)

**Auth:**
- JWT (python-jose, jsonwebtoken, @auth/core)
- OAuth (authlib, passport, next-auth)
- Session-based (express-session, flask-session)
- Supabase Auth (@supabase/auth-helpers)

**Test framework:**
- pytest, vitest, jest, mocha, go test, XCTest
- Detect test directory: tests/, __tests__/, spec/, test/

**Build system:**
- Vite, webpack, esbuild, rollup, turbopack
- setuptools, poetry, hatch
- Make (Makefile targets)

**API framework:**
- FastAPI, Express, Koa, Fastify, Gin, Echo, Fiber
- REST vs GraphQL (detect graphql imports/schema files)

**State management:**
- Zustand, Redux, MobX, Recoil, Jotai
- SwiftUI @Observable, @State, @Binding

**Deployment:**
- Docker (Dockerfile, docker-compose)
- Serverless (serverless.yml, sam template)
- Cloud Run (app.yaml, cloudbuild.yaml)
- Vercel (vercel.json)

**Naming conventions:**
```bash
# Function naming: snake_case vs camelCase
grep -rh "def [a-z]" --include="*.py" . 2>/dev/null | head -5  # snake_case
grep -rh "function [a-z]" --include="*.ts" --include="*.js" . 2>/dev/null | head -5  # camelCase
```

## Step 5: Present proposals

Show detected patterns grouped by category. For each, propose a domain rule:

```
═══ /forge learn — [project-name] ═══

Detected patterns (high confidence only):

1. ORM: SQLAlchemy 2.x (async sessions detected in 8 files)
   Proposed rule: .claude/rules/domain/orm-patterns.md
   Content: async session lifecycle, model conventions, migration patterns
   → Create? [approve/skip/edit]

2. Auth: Supabase Auth (auth-helpers in 4 files)
   Proposed rule: .claude/rules/domain/auth-flow.md
   Content: session management, RLS policies, token refresh
   → Create? [approve/skip/edit]

3. Testing: vitest (vitest.config.ts found, 23 test files)
   Proposed rule: .claude/rules/domain/testing.md
   Content: test patterns, mock conventions, coverage targets
   → Create? [approve/skip/edit]

4. Naming: snake_case (Python), camelCase (TypeScript)
   Proposed rule: .claude/rules/domain/naming.md
   Content: per-language conventions detected
   → Create? [approve/skip/edit]
```

Wait for user approval on each before creating files.

## Step 6: Generate approved rules

For each approved proposal, create a rule file in `.claude/rules/domain/`:

```markdown
---
globs: "<relevant file patterns>"
description: "<what this rule covers>"
domain: "<project-name>"
last_verified: "<today YYYY-MM-DD>"
source: "/forge learn"
---

# <Title>

<Factual observations from the scan — imperative mood, concise>
```

Rules must be:
- Under 40 lines
- Factual (observed in code, not assumed)
- Actionable (tell Claude what to do, not what exists)
- English only

## Step 7: Report summary

```
═══ Learn complete ═══
Scanned: <N> dependency files, <N> imports, <N> config files
Detected: <N> patterns across <N> categories
Created: <N> domain rules in .claude/rules/domain/
Skipped: <N> proposals

Tip: run /forge domain extract to capture session-learned knowledge too.
```

## What this skill does NOT do

- Does not read dotforge memory, errors, or agent memory (use `/forge domain extract` for that)
- Does not modify existing rules (only creates new ones in domain/)
- Does not run any code or install dependencies
- Does not guess — only reports patterns with direct evidence in the codebase
