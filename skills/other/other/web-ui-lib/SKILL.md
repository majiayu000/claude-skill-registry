---
name: web-ui-lib
description: (ePost) Use when referencing klara-theme component APIs, props, variants, spacing tokens, or theme provider patterns
user-invocable: false

metadata:
  agent-affinity: [epost-muji, epost-fullstack-developer]
  keywords: [ui-lib, components, design-tokens, integration]
  platforms: [web]
---

# klara-theme Knowledge

## Before Using This Skill — Load Live KB (Mandatory)

klara-theme has a structured knowledge base in `libs/klara-theme/docs/`. Always start here — these docs are authoritative and agent-indexed.

**Step 1 — Read the KB registry:**
```
libs/klara-theme/docs/index.json
```
Parse `entries[]`. Each entry has an `agentHint` field that tells you exactly when to load it.

**Step 2 — Load docs by task type:**

| Task | Load these entries |
|------|--------------------|
| Component lookup / REUSE check | **FEAT-0001** — 76-component catalog |
| Component structure audit | **CONV-0001** — required files, directory rules |
| Props / naming audit | **CONV-0003** — IProps naming, vocab, JSDoc |
| Token / styling audit | **CONV-0006** — semantic tokens, styles file rule |
| Business isolation audit | **CONV-0007** — no domain types, no data fetching |
| A11Y audit | **CONV-0004** — theme-ui-label, useId, Radix, focus ring |
| New component / dev workflow | **CONV-0002** — nx commands, Storybook, test execution |
| Architecture understanding | **ARCH-0001** — atomic design, module structure |
| Adding dependencies / build | **ARCH-0002** — stack, Radix UI, Tailwind, Jest setup |

If `index.json` is missing, fall back to: `Glob libs/klara-theme/docs/**/*.md` then read files directly.

## Aspects (Static Reference — supplement live KB)

| Aspect | File | Purpose |
|--------|------|---------|
| Components | references/components.md | Component API reference, RAG query patterns, Glob fallback |
| Design System | references/design-system.md | Spacing, colors, typography, token system |
| Integration | references/integration.md | Theme provider, composition, state patterns |
| Contributing | references/contributing.md | Proposing components back to MUJI |
| Component Authoring | references/component-authoring.md | Conventions for building klara-theme components |
