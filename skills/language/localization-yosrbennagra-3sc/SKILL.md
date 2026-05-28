---
name: localization
description: Implement localization for the .NET 8 WPF widget host app using resource files, culture switching, and RTL considerations. Use when adding RESX resources, binding localized strings, or supporting multiple cultures.
---

# Localization

## Overview

Deliver localized UI text and culture-aware formatting with runtime culture switching.

## Core areas

- RESX resources and resource dictionaries
- Culture switching at runtime
- RTL layout considerations

## Definition of done (DoD)

- No hardcoded user-visible strings in XAML or code
- All strings in RESX files with stable keys
- Dates/numbers use culture-aware formatting
- Culture switching works without app restart
- UI tested in at least one RTL language if RTL support is claimed

## Workflow

1. Define base resources and culture-specific RESX files.
2. Bind localized strings in XAML or view models.
3. Implement runtime culture switching in the shell.
4. Validate RTL layouts for languages that require it.

## Guidance

- Keep resource keys stable and descriptive.
- Use culture-aware formatting for dates and numbers.
- Avoid hard-coded UI strings.

## References

- `references/resources.md` for RESX patterns.
- `references/culture-switching.md` for runtime switch guidance.
- `references/rtl.md` for RTL layout considerations.
