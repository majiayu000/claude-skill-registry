---
name: verification-validator
description: Minimal verification based on change type. Backend=pytest, Frontend=webpack, CSS=webpack, Full flow=Playwright.
---

# Verification Validator

**Principle**: Minimum necessary verification only. No overkill.

## Decision Tree

```
git diff --name-only HEAD~1
         │
         ├─ apps/api/** only ──────────► pytest only (~500 tokens)
         │
         ├─ *.tsx only ────────────────► webpack check (~500 tokens)
         │
         ├─ *.scss only ───────────────► webpack check (~500 tokens)
         │
         ├─ API + Frontend together ───► Full Playwright (~10,000 tokens)
         │
         └─ en.json only ──────────────► webpack check (~500 tokens)
```

## Verification Commands

### Backend Only (apps/api/**)
```bash
cd /Users/beomsu/Documents/My\ Awesome\ RA/apps/api
source .venv/bin/activate && pytest -v --tb=short
```
**Done.** No frontend checks needed.

### Frontend Only (*.tsx, *.scss, en.json)
```bash
cd /Users/beomsu/Documents/My\ Awesome\ RA/overleaf/develop
docker compose logs webpack --tail 20 | grep -E "compiled|error"
```
**Done.** If "compiled successfully" appears, verification complete.

### Full Flow (API + Frontend Integration)
Only when BOTH conditions:
1. Backend API changed (apps/api/**)
2. Frontend calls that API (evidence-panel components)

Then use Playwright:
```
1. browser_navigate → http://localhost/login
2. browser_snapshot → find form refs
3. browser_fill_form → login
4. browser_click → login button
5. browser_wait_for → {time: 2}
6. browser_snapshot → verify feature works
7. browser_close
```

## What NOT to Do

| Change Type | DO NOT |
|-------------|--------|
| Backend only | Run webpack, Playwright |
| Frontend only | Run pytest, Playwright |
| CSS only | Run pytest, Playwright, browser tests |
| i18n only | Run pytest, Playwright |

## Quick Reference

| Change | Command | Done? |
|--------|---------|-------|
| `apps/api/**` | `pytest -v --tb=short` | Yes |
| `*.tsx` | `docker compose logs webpack` | Yes |
| `*.scss` | `docker compose logs webpack` | Yes |
| `en.json` | `docker compose logs webpack` | Yes |
| API + Frontend | Playwright sequence | Yes |

## When to Use Playwright

**ONLY** when testing user-facing integration:
- Login flow changes
- Evidence search API + UI together
- PDF toolbar + backend API

**NEVER** for:
- Backend-only changes
- Component logic changes
- Styling changes
- Translation changes
