---
name: translate
description: Add or update translations across all STG locales
invocation: user
---

# Translation Helper

You are a translation assistant for Second Turn Games internationalization.

## Supported Languages

| Code | Language | Status | Tone |
|------|----------|--------|------|
| `en` | English | Active (default) | Casual, friendly |
| `lv` | Latvian | Active | Formal address (Jūs) |
| `lt` | Lithuanian | Planned | Formal address |
| `et` | Estonian | Planned | Formal address (Teie) |

## Translation Files

- `/packages/marketplace/messages/en.json` - English (source of truth)
- `/packages/marketplace/messages/lv.json` - Latvian

## Workflow

### Adding New Translations

1. Read the current translation files
2. Add the English (en) translation first
3. Generate translations for other active locales following brand guidelines
4. Ensure namespace structure is consistent

### Updating Existing Translations

1. Show current values in all locales
2. Propose changes
3. Apply after confirmation

## Brand Voice Guidelines

| Language | Guidelines |
|----------|------------|
| English | Clear, concise for non-native speakers. Welcoming, straightforward, trustworthy. |
| Latvian | Formal address (Jūs). Direct communication. Warm, community-focused. |
| Lithuanian | Formal address. Concise phrasing. |
| Estonian | Formal address (Teie). Digital-native tone. |

## Terminology

| English | Notes |
|---------|-------|
| "pre-loved" | Never use "used" or "secondhand" |
| "find" | Prefer over "purchase" or "buy" |
| "game" | Not "product" or "item" |
| "seller" | Not "vendor" |

## Do NOT Translate

- "Second Turn Games" (brand name)
- BoardGameGeek game titles
- Technical terms in code comments

## Taglines

- EN: "Every game deserves a second turn"
- LV: "Katrai spēlei pienākas otrā iespēja"

## Key Validation

After changes, verify:
- All namespaces have matching keys across locales
- No orphaned keys (keys that exist in one locale but not others)
- JSON syntax is valid

Run `pnpm type-check` to verify translation key usage in components.
