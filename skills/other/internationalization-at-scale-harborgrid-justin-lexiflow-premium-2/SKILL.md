---
name: internationalization-at-scale
description: Implement performant i18n pipelines with code-splitting and ICU message support.
---

# Internationalization (i18n) at Scale

## Summary
Implement performant i18n pipelines with code-splitting and ICU message support.

## Key Capabilities
- Dynamically load locale chunks based on user preference.
- Implement ICU message parsing and interpolation.
- Manage bidirectional layout changes for RTL languages.

## PhD-Level Challenges
- Prevent waterfall loading of translation strings.
- Handle layout shifts during locale switching.
- Automate string extraction and synchronization with translation services.

## Acceptance Criteria
- Show sub-second locale switching mechanism.
- Provide valid ICU message usage examples.
- Demonstrate RTL layout mirror correctness.
