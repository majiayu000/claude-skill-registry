---
name: kirby-core-development
description: Kirby CMS plugin and template development for Cloodle platform. Use when creating Kirby plugins, blueprints, templates, snippets, or working with Kirby content structure.
---

# Kirby Core Development

Create and modify Kirby CMS plugins, templates, and content for the Cloodle platform.

## When to Use This Skill

- Creating new Kirby plugins
- Defining page blueprints
- Building templates and snippets
- Working with Kirby blocks
- API route development

## Server Paths

- **Kirby root**: `/opt/cloodle/apps/kirby/`
- **Plugins**: `/opt/cloodle/apps/kirby/site/plugins/`
- **Content**: `/opt/cloodle/apps/kirby/content/`

## Quick Start

See [reference.md](reference.md) for complete patterns and examples.

### Plugin Registration

```php
<?php
Kirby::plugin('cloodle/my-plugin', [
    'blueprints' => [
        'pages/custom' => __DIR__ . '/blueprints/pages/custom.yml'
    ],
    'templates' => [
        'custom' => __DIR__ . '/templates/custom.php'
    ]
]);
```

### Blueprint Structure

```yaml
title: Custom Page
fields:
  text:
    type: blocks
    fieldsets:
      - heading
      - text
      - image
```

## Existing Cloodle Plugins

- `cloodle/` - Portal dashboard
- `moodle-export/` - IMSCP export
- `zero-one/` - Theme plugin
- `oauth/` - Authentik integration
