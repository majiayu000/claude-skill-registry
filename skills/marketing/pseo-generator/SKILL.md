---
name: pseo-generator
description: Generate programmatic SEO pages from JSON data using Next.js/React templates, plus sitemap + validation tooling. Use when creating comparison pages, alternatives lists, or “best for [persona]” pages at scale, or when asked to scaffold pSEO data schemas, generate pages, build sitemaps, or check for duplicate/thin content.
---

# pSEO Generator

Create pSEO pages from JSON data and template files. This skill ships a Click CLI plus three Next.js/React templates.

## Quick Start

```bash
./scripts/generate.py init --pattern comparison
./scripts/generate.py generate --data ./data.json --template comparison --output ./pages/
./scripts/generate.py sitemap --output ./public/sitemap.xml
./scripts/generate.py validate
```

## Templates

- `templates/comparison.tsx` → X vs Y (features, pricing, verdict)
- `templates/alternative.tsx` → “[X] alternatives” list page
- `templates/best-for.tsx` → “Best [category] for [persona]”

## Playbooks Reference

Use the 12 programmatic SEO playbooks in `../programmatic-seo/SKILL.md` to pick the right pattern. Relevant playbooks: Templates, Curation, Conversions, Comparisons, Examples, Locations, Personas, Integrations, Glossary, Translations, Directory, Profiles.

## Notes

- `init` writes a starter `data.json` schema for the chosen pattern.
- `generate` replaces placeholders in the template with per-page JSON data.
- `sitemap` scans the pages dir and emits a sitemap XML.
- `validate` flags duplicate or thin generated pages.
