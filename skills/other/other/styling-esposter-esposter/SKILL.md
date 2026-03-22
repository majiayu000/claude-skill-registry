---
name: styling
description: Esposter UnoCSS Attributify Mode styling conventions — prop-based attributes for all static styles, flex not d-flex, class only for dynamic or Vuetify-specific utilities. Apply when writing .vue or .scss files.
---

# Styling — UnoCSS Attributify Mode (MANDATORY)

- Use prop-based styling: `<div text-red p-4>` for ALL static styles.
- Use `flex` not `d-flex`.
- Use `size` attribute (or `width`/`height` props) instead of `w-<n>` / `h-<n>` where possible.
- Only use `class="..."` when technically required (dynamic `:class` bindings, Vuetify-specific typography/colour classes like `text-overline`, `text-medium-emphasis`, `text-wrap`). UnoCSS utilities (spacing, flex, sizing) must always be attributes even when mixed with Vuetify classes: `<div class="text-overline" mb-2>`.
