---
name: kirby-panel-and-blueprints
description: Designs Kirby blueprints and Panel UI, including blueprint reuse/extends, programmable blueprints, and custom Panel fields/sections/areas. Use when changing the Panel experience or schema.
---

# Kirby Panel and Blueprints

## KB entry points

- `kirby://kb/scenarios/06-blueprints-reuse-extends`
- `kirby://kb/scenarios/19-programmable-blueprints`
- `kirby://kb/scenarios/53-panel-first-custom-field`
- `kirby://kb/scenarios/54-panel-first-custom-section`
- `kirby://kb/panel/reference-fields`
- `kirby://kb/panel/panel-bundling-decisions`

## Required inputs

- Content model and required fields.
- Panel UX (tabs/sections/layout) and validation rules.
- Whether to extend an existing blueprint.

## Minimal blueprint skeleton

```yaml
title: Example
status:
  draft: true
  listed: true
fields:
  title:
    type: text
  text:
    type: textarea
```

## Extends example

```yaml
extends: pages/default
```

## Common pitfalls

- Duplicating fields instead of using `extends`.
- Implementing Panel UI logic in templates instead of blueprints or plugins.

## Workflow

1. Clarify the content model, required fields, and Panel UX expectations.
2. Call `kirby:kirby_init` and read `kirby://roots`.
3. Inspect existing blueprints and patterns:
   - `kirby:kirby_blueprints_index`
   - `kirby:kirby_blueprint_read`
4. Use Panel reference resources for field/section choices:
   - `kirby://fields`
   - `kirby://sections`
5. Check plugin surface when custom Panel UI is needed:
   - `kirby:kirby_plugins_index`
   - `kirby://extensions`
6. Search the KB with `kirby:kirby_search` (examples: "blueprints reuse extends", "programmable blueprints", "custom panel field", "custom panel section", "panel branding").
7. Implement minimal, convention-aligned YAML/PHP; prefer `extends` and shared sections over duplication.
8. Validate by re-reading the blueprint (`kirby:kirby_blueprint_read`) and verifying frontend output with `kirby:kirby_render_page` when relevant.
