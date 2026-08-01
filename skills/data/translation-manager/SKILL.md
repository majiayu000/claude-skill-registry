---
name: translation-manager
description: 'Translation Manager for this repo: Supabase-backed translations, admin
  UI under /admin/translation-manager with Home live preview and click-to-select translation,
  Edge Functions (translations-get/admi'
---

---
name: translation-manager
description: Translation Manager for this repo: Supabase-backed translations, admin UI under /admin/translation-manager with Home live preview and click-to-select translation, Edge Functions (translations-get/admin/suggest), build-time translation pipeline, and security hardening. Use when planning or editing translation manager UI, Supabase schema/migrations, translation scripts (seed/pull), Edge Functions, translation auth, or troubleshooting translation data/AI suggestions.
---

# Translation Manager

## Overview

Maintain the translation system end-to-end (admin UI, Supabase tables/functions, build-time translation pipeline) and keep security tight. The Home page is now wired for a live preview with click-to-select text and AI suggestions in the admin UI, plus markup-aware headings for full-line translation, per-entry Save, and a single Publish action.

## Workflow

1. Identify scope (UI, data/schema, Edge Functions, scripts/build, auth/security).
2. Load the matching reference file(s).
3. Implement changes and keep guardrails intact.
4. Validate with local checks and Supabase steps.
5. Update references if scope or architecture changes.

## Reference Map

- Scope and goals: `references/scope-and-goals.md`
- System architecture and file map: `references/system-architecture.md`
- Current implementation snapshot: `references/current-state.md`
- Supabase setup and Edge Functions: `references/supabase-setup.md`
- Operational workflows: `references/workflows.md`
- Security hardening: `references/security-hardening.md`
- Troubleshooting: `references/troubleshooting.md`

## Guardrails

- Never expose the service role key to the client or browser.
- Require a Supabase user token for `translations-admin`/`translations-suggest`, and keep signups disabled unless you add an allowlist/role check.
- Keep RLS policies intact; assume service role bypasses them.
- Preserve the build-time translation flow unless explicitly changed.

## Quick File Map

- Admin UI: `client/src/components/admin/admin-layout.tsx`, `client/src/pages/admin/index.tsx`, `client/src/pages/admin/translation-manager.tsx`, `client/src/pages/translation-manager.tsx`
- Home sections + data: `client/src/pages/home.tsx`, `client/src/components/sections/home/*`, `client/src/data/home.ts`, `client/src/data/home-faqs.ts`
- Translation markup helper: `client/src/lib/translation-markup.tsx`
- Server proxy: `server/routes.ts`
- Supabase: `supabase/migrations/0001_translations.sql`, `supabase/functions/*`
- Build/seed: `scripts/seed-translations.mjs`, `scripts/pull-translations.mjs`, `client/src/generated/translations.json`
