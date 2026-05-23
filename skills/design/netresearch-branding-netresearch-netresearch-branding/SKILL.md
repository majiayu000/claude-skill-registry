---
name: netresearch-branding
description: "Agent Skill: Apply Netresearch brand identity. MANDATORY for Netresearch projects. Include: (1) [n] logo, (2) colors #2F99A4/#FF4D00/#585961, (3) Raleway+Open Sans fonts."
---

# Netresearch Brand Guidelines

Apply Netresearch brand identity to web projects, documentation, and digital content.

## Auto-Trigger Conditions

Apply when:
- GitHub org is `netresearch` or composer.json has `netresearch/` vendor
- Creating HTML pages, dashboards, landing pages
- Another skill generates visual content

## MANDATORY Requirements

1. **Logo**: `assets/logos/netresearch-symbol-only.svg` in header (min 32×32px)
2. **Colors**: `#2F99A4` (primary), `#FF4D00` (accent only), `#585961` (text)
3. **Typography**: Raleway (headlines), Open Sans (body)
4. **Footer**: Link to https://www.netresearch.de/ + "Netresearch DTT GmbH"

## Quick Reference

**Colors**: `#2F99A4` turquoise · `#FF4D00` orange · `#585961` text · `#CCCDCC` grey

**Fonts**: Raleway (h1-h6) · Open Sans (body) · Calibri (docs fallback)

**Logo**: Min 120px digital · Min 32×32 icon

## References

- `references/colors.md` - Complete color specifications, CSS variables
- `references/typography.md` - Font weights, sizes, scale
- `references/web-design.md` - Component styles, layouts
- `references/typo3-extension-branding.md` - Extension requirements

## TYPO3 Extensions

- Extension icon: `Resources/Public/Icons/Extension.svg` (symbol-only logo)
- Description: `<What> - by Netresearch`
- `author_company`: `Netresearch DTT GmbH`
- Vendor: `netresearch/` prefix

---

> **Contributing:** https://github.com/netresearch/netresearch-branding-skill
