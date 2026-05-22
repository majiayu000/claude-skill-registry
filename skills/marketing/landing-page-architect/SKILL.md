---
name: landing-page-architect
description: >
  Product marketing and landing page architect for Raamattu Nyt. Generates landing page copy,
  feature page copy, and CTA suggestions based on the canonical user model. Translates user
  paths into benefit narratives and core tasks into user value propositions.
  Use when (1) creating or updating the main landing page, (2) writing feature page copy,
  (3) generating marketing messaging for app features, (4) crafting CTAs,
  (5) translating technical features into user benefits, (6) planning marketing page structure.
  Triggers: "landing page", "marketing copy", "feature page", "CTA", "value proposition",
  "markkinointi", "laskeutumissivu", "ominaisuussivu", "benefits copy", "marketing messaging".
---

# Landing Page Architect

Generate marketing copy and landing pages for Raamattu Nyt by translating the canonical user
model into benefits and value.

## Authority

- Consumes `Docs/ai/core-user-model.json` as the single source of truth
- NEVER redefines tasks or paths — translates them into benefits and value
- The `core-ux-detective` skill owns definitions; this skill owns marketing presentation

## Workflow

### 1. Read the User Model

```
Read Docs/ai/core-user-model.json
```

If file doesn't exist, inform the user to run `core-ux-detective` first.

### 2. Determine Scope

From user request, determine what to generate:
- **Full landing page**: Hero + feature sections + CTAs
- **Feature page**: Single feature deep-dive
- **CTA copy**: Call-to-action suggestions
- **Messaging framework**: Benefit mapping for all tasks/paths

### 3. Transform Paths → Narratives

For each `user_path`, generate a benefit narrative:

| Model Field | Marketing Use |
|-------------|---------------|
| `user_paths[].intent` | Problem statement / user need |
| `user_paths[].label` | Section heading (Finnish) |
| `user_paths[].steps` | Implied complexity → simplicity promise |
| `user_paths[].primary` | Hero section (true) vs. feature section (false) |

**Primary paths** → hero section and main value proposition.
**Secondary paths** → feature cards / supporting sections.

### 4. Transform Tasks → Benefits

For each `core_task`, map to a user benefit:

```
Task intent (English)  →  What problem it solves
Task label (Finnish)   →  Feature name in copy
Task appears_in        →  Context for where to show it
```

Focus on **outcomes**, not mechanics:
- "Löydä jakeet hetkessä" (Find verses instantly) — not "Hakutoiminto käyttää tekstihakua"
- "Kuuntele Raamattu matkalla" (Listen to the Bible on the go) — not "TTS-toisto ElevenLabs APIlla"

### 5. Generate Copy

See [references/copy-patterns.md](references/copy-patterns.md) for page structure templates and
Finnish copywriting patterns.

### 6. Output

| Output | Format | Location |
|--------|--------|----------|
| Landing page | React component or HTML | `apps/raamattu-nyt/src/pages/LandingPage.tsx` |
| Feature sections | Component per section | `apps/raamattu-nyt/src/components/landing/` |
| Copy data | JSON | `apps/raamattu-nyt/src/data/marketing-copy.json` |
| Static landing | HTML (if standalone) | `apps/raamattu-nyt/public/landing/` |

## Messaging Rules

1. **Never rename** tasks or paths from the canonical model
2. **Never invent** features that don't exist in `core-user-model.json`
3. **User intent language** — describe what the user wants, not what the app does
4. **Finnish first** — all user-facing copy in Finnish, English for dev comments only
5. **No superlatives** — avoid "paras", "vallankumouksellinen", "uskomaton"
6. **Trustworthy tone** — clear, honest, non-pushy
7. **No step-by-step** — marketing explains why, not how (help-system-architect owns how)

## Tone

- **Trustworthy**: Honest about what the app does, no exaggeration
- **Clear**: Short sentences, concrete benefits, no jargon
- **Non-pushy**: Invite, don't pressure — "Kokeile" over "Osta nyt"
- **Warm**: The Bible is personal; copy should feel respectful and inviting
