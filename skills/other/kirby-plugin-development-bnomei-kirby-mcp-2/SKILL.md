---
name: kirby-plugin-development
description: Builds or extends Kirby plugins using hooks, extensions, blocks, KirbyTags, and shared templates/controllers. Use when creating reusable features or integrating Panel customizations.
---

# Kirby Plugin Development

## KB entry points

- `kirby://kb/scenarios/04-share-templates-controllers-via-plugin`
- `kirby://kb/scenarios/05-kirbytext-kirbytags-hooks`
- `kirby://kb/scenarios/15-custom-blocks-nested-blocks`
- `kirby://kb/scenarios/17-extend-kirbytags`
- `kirby://kb/scenarios/59-monolithic-plugin-setup`
- `kirby://kb/scenarios/60-plugin-workflow-local-testing`

## Required inputs

- Plugin id (vendor/name) and scope.
- Extension points (hooks/fields/tags/blocks/sections).
- Distribution plan (project-only or composer package).

## Minimal plugin skeleton

```php
Kirby::plugin('vendor/name', [
  'hooks' => [],
  'blueprints' => [],
  'snippets' => [],
]);
```

## Local testing

- Use the local workflow guide to test without publishing.
- Render affected pages and verify plugin registration.

## Common pitfalls

- Using inconsistent plugin ids or folder names.
- Registering hooks that assume Panel or API is always enabled.

## Workflow

1. Define the plugin id (vendor/name), feature scope, and whether it must be reusable across projects.
2. Call `kirby:kirby_init` and read `kirby://roots` to locate plugin roots.
3. Inspect existing plugins to avoid duplication: `kirby:kirby_plugins_index`.
4. Use extension and hook references:
   - `kirby://extensions` and `kirby://extension/{name}`
   - `kirby://hooks` and `kirby://hook/{name}`
5. Search the KB with `kirby:kirby_search` (examples: "kirbytext hooks", "extend kirbytags", "custom blocks", "share templates via plugin", "monolithic plugin setup").
6. Implement the plugin with a minimal `index.php` registration, then add blueprints/snippets/assets as needed.
7. Verify by rendering affected pages with `kirby:kirby_render_page` and confirming the plugin loads without errors.
