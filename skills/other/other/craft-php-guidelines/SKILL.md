---
name: craft-php-guidelines
description: "Craft CMS 5 PHP coding standards and conventions. Triggers: writing PHP classes, PHPDoc blocks, @author, @since, @throws, section headers (=========), defineRules(), beforePrepare(), addSelect(), MemoizableArray, DateTimeHelper, Carbon, ECS check-cs, PHPStan, ddev craft make, Twig templates, form macros, translations Craft::t(), enum definitions, commit messages. Always load when writing, editing, or reviewing any PHP or Twig code in a Craft CMS plugin or module."
---

# Craft CMS 5 PHP Guidelines

Complete PHP coding standards and conventions for active coding sessions.

## Common Pitfalls

- `addSelect()` is the convention in `beforePrepare()` — safely additive when multiple extensions contribute columns. Craft's `**` placeholder merges defaults regardless, but `addSelect()` prevents conflicts.
- `$_instances` is not a Craft convention — private properties use underscore prefix but meaningful names like `$_items`, `$_sections`.
- Records use the **same class name** as models (namespace distinguishes). Alias when importing both: `use ...\records\MyEntity as MyEntityRecord;`.
- Queue jobs have **no "Job" suffix** — `ResaveElements`, not `ResaveElementsJob`.
- `declare(strict_types=1)` is NOT used in plugin source files. Only in standalone config files like `ecs.php`.
- `@author` goes on classes and methods only — never on properties.
- Don't use `string|null` — use `?string` (short nullable notation).
- Forget `parent::defineRules()` and you lose all inherited validation.
- `DateTimeHelper` in elements/queries, `Carbon` in services — never mix in the same class.
- Missing `@throws` chains — document exceptions from called methods too, not just your own throws.

## Documentation

- Official coding guidelines: https://craftcms.com/docs/5.x/extend/coding-guidelines.html
- Class reference: https://docs.craftcms.com/api/v5/
- Generator reference: https://craftcms.com/docs/5.x/extend/generator.html

When unsure about a convention, `web_fetch` the coding guidelines page for the authoritative answer.

## Critical Rules

1. PHPDocs on everything: classes, methods, properties. No exceptions.
2. `@throws` chains: document every exception including uncaught from called methods.
3. `@author` and `@since` at the bottom of class/method docblocks, after a blank line.
4. Section headers with `// =========================================================================` on every class.
5. `declare(strict_types=1)` is NOT used in plugin source files.
6. Private methods/properties prefixed with underscore: `_registerCpUrlRules()`, `$_items`.
7. `addSelect()` convention in `beforePrepare()` (additive across extensions).
8. `DateTimeHelper` in elements/queries, `Carbon` in services.
9. Always scaffold with `ddev craft make <type> --with-docblocks`, then customize.
10. `ddev composer check-cs` and `ddev composer phpstan` must pass before every commit.

## Section Header Order

```
// Traits
// Const Properties
// Static Properties
// Public Properties
// Protected Properties
// Private Properties
// Public Methods
// Protected Methods
// Private Methods
```

Only include sections that have content. Blank line after the separator, before the first item.

## Naming Quick-Reference

- **Services (resource):** Plural — `Entries`, `Volumes`, `Users`
- **Services (utility):** Domain noun — `Auth`, `Search`, `Gc`
- **Queue jobs:** Action verb, no suffix — `ResaveElements`, `UpdateSearchIndex`
- **Records:** Same name as model — namespace distinguishes
- **Events:** Three patterns — `SectionEvent`, `RegisterUrlRulesEvent`, `DefineHtmlEvent`
- **Element actions:** Action verb, no suffix — `Delete`, `Duplicate`, `SetStatus`
- **Enums:** PascalCase cases, string/int backed — `PropagationMethod`, `CmsEdition`

## Verification Checklist

Before every commit:

1. `ddev composer check-cs` passes
2. `ddev composer phpstan` passes
3. Tests green
4. PHPDocs complete on all new/modified code
5. `@throws` chains verified
6. Section headers present and correct
7. Imports alphabetical and grouped
