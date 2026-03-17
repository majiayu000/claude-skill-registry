---
name: kirby-ide-support
description: Improves IDE autocomplete and static analysis in Kirby projects with PHPDoc hints and Kirby IDE helper generation. Use when types are missing or IDE support is degraded.
---

# Kirby IDE Support

## Quick start

- Follow the workflow below for a minimal, types-only IDE pass.

## KB entry points

- `kirby://kb/scenarios/18-ide-support`
- `kirby://kb/glossary/page-model`
- `kirby://kb/glossary/template`

## Required inputs

- Target files and scope (templates/snippets/controllers/models).
- Whether to generate helpers or only add PHPDoc hints.

## Minimal PHPDoc hints

```php
/** @var Kirby\Cms\Site $site */
/** @var Kirby\Cms\Page $page */
```

- Place hints at the top of templates/snippets; keep them types-only.

## Generation rule

- Add PHPDoc hints for a few files or local fixes.
- Generate IDE helpers when multiple templates/models lack types or for project-wide refresh.

## Common pitfalls

- Generating helpers for a single missing type.
- Leaving stale helpers after blueprint or model changes.

## Workflow

1. Call `kirby:kirby_init`, then check status with `kirby:kirby_ide_helpers_status`.
2. Inspect templates/snippets/controllers/models for missing hints:
   - `kirby:kirby_templates_index`
   - `kirby:kirby_snippets_index`
   - `kirby:kirby_controllers_index`
   - `kirby:kirby_models_index`
3. Add minimal, types-only improvements:
   - `@var` hints in templates/snippets
   - typed controller closures
   - ensure page models extend the correct base class
4. If generating helpers, run `kirby:kirby_generate_ide_helpers(dryRun=true)` first; ask before writing, then run with `dryRun=false`.
5. Re-run `kirby:kirby_ide_helpers_status` and summarize changes.
6. Search the KB with `kirby:kirby_search` (example: "ide support").
