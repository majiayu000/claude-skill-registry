---
name: check
description: Voer een volledige kwaliteitscheck uit op de Hugo site. Gebruik wanneer de gebruiker wil controleren of de site correct bouwt of geen broken links heeft.
---

Voer een volledige kwaliteitscheck uit op de Hugo site.

## Technische checks

1. Run: `just build`
2. Run: `just check`
3. Rapporteer eventuele problemen in begrijpelijke taal

## Optionele vervolgchecks

Na de technische checks, vraag of de gebruiker ook wil:
- **Content review**: `/content-review` - controleer content op spelling en leesbaarheid
- **Toegankelijkheid**: `/a11y-review` - controleer templates op WCAG 2.1 compliance
- **SEO**: `/seo-check` - controleer meta descriptions en heading structuur

## Bij fouten

- Leg uit wat het probleem is
- Geef suggesties voor hoe het opgelost kan worden
- Bied aan om te helpen met de fix

Dit is dezelfde check die ook automatisch draait via de pre-commit hook (Lefthook).
