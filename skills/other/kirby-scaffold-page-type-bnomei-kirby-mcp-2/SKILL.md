---
name: kirby-scaffold-page-type
description: Scaffolds a new Kirby page type (blueprint + template, optional controller/model) using project roots, index tools, and Panel field/section references. Use when creating a new page type or extending an existing blueprint/template.
---

# Kirby Scaffold Page Type

## Quick start

- Follow the workflow below to scaffold a new page type safely.

## KB entry points

- `kirby://kb/scenarios/01-scaffold-page-type`
- `kirby://kb/scenarios/22-custom-post-types`
- `kirby://kb/scenarios/30-create-a-blog-section`
- `kirby://kb/scenarios/31-one-pager-site-sections`
- `kirby://kb/scenarios/06-blueprints-reuse-extends`

## Required inputs

- Page type name and required fields.
- Panel UX expectations and any reuse/extends needs.
- Template/controller/model naming preferences.

## Minimal scaffold

Blueprint:

```yaml
title: Example
fields:
  title:
    type: text
```

Template:

```php
<?php snippet('header') ?>
<?php snippet('footer') ?>
```

## Default controller/model

Controller:

```php
return function ($page) {
  return ['page' => $page];
};
```

Model:

```php
class ExamplePage extends Page
{
}
```

## Naming checklist

- Template filename matches blueprint id.
- Controller filename matches template name.
- Model class name matches template name in StudlyCase.

## Common pitfalls

- Mismatched template, blueprint, and controller names.
- Creating a Panel type without a matching blueprint.

## Workflow

1. Ask for page type name, required fields, Panel UX expectations, and whether to extend an existing type.
2. Call `kirby:kirby_init` and read `kirby://roots` to locate templates, blueprints, controllers, models, and snippets.
3. Check for name collisions and existing patterns:
   - `kirby:kirby_templates_index`
   - `kirby:kirby_blueprints_index`
   - `kirby:kirby_controllers_index`
   - `kirby:kirby_models_index`
4. If extending an existing type, read it with `kirby:kirby_blueprint_read` before generating new files.
5. Use Panel reference resources for field and section choices:
   - `kirby://fields`
   - `kirby://sections`
6. Search the KB with `kirby:kirby_search` (examples: "scaffold page type", "blueprints reuse extends", "custom post types", "create a blog section", "one pager site sections").
7. Create minimal, convention-aligned files; prefer snippets for reusable view logic.
8. Verify with `kirby:kirby_render_page(noCache=true)` when runtime is available; otherwise run `kirby:kirby_runtime_status` and `kirby:kirby_runtime_install` first.
9. Optionally run `kirby:kirby_ide_helpers_status` and `kirby:kirby_generate_ide_helpers` (dry-run first) to keep IDE types in sync.
