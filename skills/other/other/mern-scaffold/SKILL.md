---
name: mern-scaffold
description: Scaffold a pnpm + Turborepo MERN monorepo with Next.js, tooling, tests, CI, and optional GitHub repo creation.
argument-hint: "[app-name] [--github] [--public] [--org <org>] [--repo <n>] [--no-push]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Create a fully working MERN repo (Next.js + TypeScript + pnpm workspaces + Turborepo) with tooling configured and runnable immediately.

## Arguments
- `app-name` — Project folder name (default: "app"). Use `.` to scaffold in the current directory (must be empty or near-empty).
- `--github` — Create GitHub repo and push (requires `gh auth`)
- `--public` — Make GitHub repo public (default: private)
- `--org <n>` — Create under org instead of personal account
- `--repo <n>` — Override repo name (default: app-name)
- `--no-push` — Create repo and commit but don't push

## Template-first rule
Copy files from `templates/` into the project. If a template doesn't exist, generate equivalent content.

Templates provide:
- Root configs (eslint, prettier, turbo, .prettierignore)
- Test configs (vitest.config.ts with jsdom + coverage, playwright.config.ts)
- Test setup (src/__tests__/setup.tsx with React mocks for next/image, next/navigation, matchMedia, localStorage)
- Server utilities (env validation, response helpers, rate limiting, sanitization)
- Shared package structure (Zod schemas)
- CLAUDE.md for the new repo
- VS Code workspace settings and extension recommendations

## What gets created

```
<app-name>/
├── apps/web/                 # Next.js app (app router + Tailwind)
│   ├── e2e/                  # Playwright e2e tests
│   │   └── health.spec.ts   # Health check e2e test
│   └── src/
│       ├── app/api/health/   # Health check endpoint (app router)
│       │   └── route.ts
│       ├── __tests__/        # Test setup + smoke tests
│       │   ├── setup.tsx
│       │   └── smoke.test.ts
│       └── server/           # Server utilities from templates
├── packages/shared/          # Zod schemas + types
│   ├── package.json
│   └── src/
├── docs/                     # Documentation
│   └── PRD-TEMPLATE.md       # Product requirements template for Ralph
├── .vscode/                  # VS Code workspace config (from templates)
│   ├── settings.json
│   └── extensions.json
├── .github/                  # GitHub config (from templates)
│   ├── workflows/
│   │   ├── ci.yml            # CI pipeline (lint, format, typecheck, test, build, e2e)
│   │   ├── security.yml      # Dependency review + TruffleHog
│   │   └── pr-check.yml      # PR size labeler, commitlint, WIP check
│   ├── dependabot.yml        # Automated dependency updates
│   ├── CODEOWNERS            # Required reviewers by path
│   ├── SECURITY.md           # Security policy
│   └── pull_request_template.md  # PR template with checklist
├── .env.local                # Local env (gitignored)
├── .env.example              # Env template (committed)
├── CLAUDE.md                 # Repo context for Claude Code
└── (root configs)            # eslint, prettier, turbo, pnpm-workspace
```

## Scaffold steps

### 1. Create root package.json

```json
{
  "name": "<app-name>",
  "private": true,
  "packageManager": "pnpm@10.5.2",
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier --check .",
    "format:write": "prettier --write .",
    "test": "turbo run test",
    "test:e2e": "turbo run test:e2e",
    "typecheck": "turbo run typecheck"
  },
  "pnpm": {
    "onlyBuiltDependencies": ["husky"]
  }
}
```

### 2. Copy root configs from templates
- `pnpm-workspace.yaml`
- `turbo.json`
- `eslint.config.mjs` (uses eslint-plugin-import-x for flat config)
- `prettier.config.cjs`
- `.prettierignore`
- `README.md`
- `CLAUDE.md`

### 2a. Copy VS Code config from templates
- `.vscode/settings.json`
- `.vscode/extensions.json`

### 3. Run create-next-app

```bash
mkdir -p apps
pnpm dlx create-next-app@latest "$(pwd)/apps/web" --ts --tailwind --eslint --app --src-dir --import-alias "@/*" --use-pnpm --yes --disable-git
```

**Important:** Use absolute path for the target directory. CNA will not create parent directories and fails with "not writable" if `apps/` doesn't exist.

**Flags explained:**
- `--yes` skips all interactive prompts (React Compiler, etc.)
- `--disable-git` prevents CNA from running git init (we handle git ourselves)

### 4. Post-CNA cleanup

**Remove CNA artifacts** (root config handles linting; monorepo has its own lockfile):
```bash
rm -f apps/web/eslint.config.mjs apps/web/pnpm-lock.yaml apps/web/pnpm-workspace.yaml
```

**Update `apps/web/package.json` scripts:**
- Replace `"lint": "next lint"` with `"lint": "eslint ."`
  (Next.js 16 removed `next lint`; root eslint handles it anyway)
- Add test scripts:
  ```json
  {
    "scripts": {
      "dev": "next dev",
      "build": "next build",
      "start": "next start",
      "lint": "eslint .",
      "test": "vitest run",
      "test:watch": "vitest",
      "test:e2e": "playwright test",
      "typecheck": "tsc --noEmit"
    }
  }
  ```

### 5. Install root dependencies

```bash
pnpm add -D eslint @eslint/js@^9 globals typescript-eslint @next/eslint-plugin-next eslint-plugin-react-hooks eslint-plugin-react-refresh eslint-plugin-import-x eslint-plugin-unused-imports vitest @vitest/coverage-v8 turbo prettier -w
```

### 6. Copy test configs to apps/web from templates
- `apps/web/vitest.config.ts`
- `apps/web/src/__tests__/setup.tsx`
- `apps/web/playwright.config.ts`

### 7. Install web app testing dependencies

```bash
pnpm --filter web add -D @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @playwright/test vitest @vitest/coverage-v8
```

### 8. Install Playwright browsers

```bash
pnpm --filter web exec playwright install chromium
```

**Note:** Playwright is installed in the web workspace, not root. Use `--filter web` to run from the correct scope.

### 9. Copy server utilities from templates to apps/web/src/server/
- `env.ts`
- `http/response.ts`
- `http/rateLimit.ts`
- `http/validate.ts`
- `http/securityHeaders.ts`
- `db/sanitize.ts`
- `db/mongoose.ts`

### 10. Install web app server dependencies

```bash
pnpm --filter web add zod mongoose
```

### 11. Create packages/shared

Create `packages/shared/package.json`:
```json
{
  "name": "@repo/shared",
  "version": "0.0.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": {
    "lint": "eslint .",
    "test": "vitest run --passWithNoTests",
    "typecheck": "tsc --noEmit"
  }
}
```

Create `packages/shared/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "declaration": true,
    "declarationMap": true
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules"]
}
```

Copy shared source files from templates:
- `packages/shared/src/index.ts`
- `packages/shared/src/schemas/example.ts`

Install shared dependencies:
```bash
pnpm --filter @repo/shared add zod
pnpm --filter @repo/shared add -D typescript vitest
```

Add workspace reference in web app:
```bash
pnpm --filter web add '@repo/shared@workspace:*'
```

**Note:** Single quotes required — zsh expands unquoted `*` as a glob.

### 12. Create docs/
Copy `docs/PRD-TEMPLATE.md` from templates.

### 13. Create health check endpoint

Create `apps/web/src/app/api/health/route.ts`:
```typescript
import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({ ok: true, data: { status: "ok" } });
}
```

### 14. Create smoke test

Create `apps/web/src/__tests__/smoke.test.ts`:
```typescript
import { describe, it, expect } from "vitest";

describe("smoke test", () => {
  it("should pass a basic assertion", () => {
    expect(1 + 1).toBe(2);
  });
});
```

### 15. Create e2e test

Create `apps/web/e2e/health.spec.ts`:
```typescript
import { test, expect } from "@playwright/test";

test("health endpoint returns ok", async ({ request }) => {
  const response = await request.get("/api/health");
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  expect(body).toEqual({ ok: true, data: { status: "ok" } });
});
```

### 16. Create environment files

`.env.local` (gitignored):
```
MONGODB_URI=mongodb://localhost:27017/hello-mern
```

`.env.example` (committed):
```
MONGODB_URI=mongodb://localhost:27017/myapp
```

### 17. Create .gitignore

```
node_modules
.next
dist
build
out
coverage
.turbo
.env.local
.env.test
*.tsbuildinfo
playwright-report
test-results
```

### 18. Create GitHub config files

Copy all `.github/` files from templates. Replace `__GITHUB_USER__` in
`dependabot.yml` and `CODEOWNERS` with the GitHub username (from `gh api user`
or the `--org` argument). Replace `__APP_NAME__` in `ci.yml` with the project name.

### 19. Run pnpm install

```bash
pnpm install
```

### 20. Run quality gates (must all pass before done)

```bash
pnpm lint
pnpm format
pnpm typecheck
pnpm test
pnpm build
pnpm test:e2e
```

Fix any failures and re-run until all pass.

### 21. git init

```bash
git init
```

This prepares the repo for the github-hooks step.

## GitHub setup (if --github)
- Requires `gh auth status` to succeed
- Creates repo: `gh repo create <owner>/<repo> --<visibility> --source . --remote origin`
- Commits and pushes unless `--no-push`

## Post-scaffold: GitHub security (recommended)

After scaffolding, run these skills to complete GitHub security setup:

1. **`/github-hooks --platform mern`** — Install local Git hooks
   - Husky + lint-staged for pre-commit validation
   - Commit message enforcement (conventional commits)
   - Secret scanning (gitleaks)
   - Pre-push test runs

2. **`/github-secure`** (if `--github` was used) — Configure repo security via GitHub API
   - Branch protection rules
   - Dependabot alerts + security updates
   - Auto-merge enablement
   - (Files already created by scaffold — github-secure skips existing files)

These are invoked automatically by `/mern-kit`.

## Output
Summarize: structure created, commands available, what tooling is included, GitHub status if applicable, **and remind to run github-hooks/github-secure if not using mern-kit**.
