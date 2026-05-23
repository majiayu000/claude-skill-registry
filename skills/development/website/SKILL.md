---
name: website
description: Build, serve, and test the dart_node documentation website (Eleventy + Playwright)
argument-hint: "[build|dev|test|clean]"
disable-model-invocation: true
allowed-tools: Bash
---

# Website (Eleventy + Playwright)

Build and test the dart_node documentation site at `website/`.

## Commands

Parse `$ARGUMENTS` to determine the action:

**build** — Full production build (copies READMEs, generates API docs, runs Eleventy):
```bash
cd website && npm run build
```

**dev** — Start the dev server with live reload:
```bash
cd website && npm run dev
```
Serves at `http://localhost:8080`.

**test** — Run Playwright E2E tests (builds first if `_site/` doesn't exist):
```bash
cd website && npm test
```

**test:coverage** — Run tests with V8 JS coverage:
```bash
cd website && npm run test:coverage
```

**clean** — Remove generated files:
```bash
cd website && npm run clean
```

**No args** — Default to `build` then `test`.

## Build pipeline

`npm run build` runs `scripts/build.sh` which does:
1. `node scripts/copy-readmes.js` — Copies package READMEs into the site
2. `bash scripts/generate-api-docs.sh` — Generates API reference from Dart source
3. `npx eleventy` — Generates static site into `_site/`

## Test files

9 test specs in `website/tests/`:
- Page content, navigation, language switching
- Theme toggle (dark/light mode)
- Mobile responsiveness
- Code blocks and syntax highlighting

## Prerequisites

Playwright must be installed first. Run `/setup-playwright` if `npx playwright --version` fails.
