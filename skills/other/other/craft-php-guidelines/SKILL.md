---
name: craft-php-guidelines
description: "Craft CMS 5 PHP coding standards and conventions. ALWAYS load this skill when writing, editing, reviewing, or discussing any PHP file in a Craft CMS plugin or module — even for small edits. Also load when running ECS, PHPStan, or scaffolding with ddev craft make. Covers: PHPDoc blocks (@author, @since, @throws chains, documenting exceptions), section headers (=========), class organization, naming conventions (services, queue jobs, records, events, enums), defineRules() and validation, beforePrepare() and addSelect(), MemoizableArray, DateTimeHelper vs Carbon, strict_types and declare(strict_types=1) usage, short nullable notation (?string), typed properties, void return types, control flow patterns (early returns, match over switch), CP Twig template conventions, form macros, translations (Craft::t), ECS/PHPStan configuration, scaffolding commands, and the verification checklist. Triggers on: writing service classes, models, controllers, elements, element queries, records, queue jobs, migrations, or any PHP class in a Craft CMS context. Also triggers on PHP code review, refactoring, or style questions for Craft plugins and modules. NOT for front-end Twig templates (use craft-twig-guidelines), template architecture (use craft-site), or CP JavaScript/Garnish (use craft-garnish). If you are touching PHP code in a Craft CMS context, you need this skill."
---

# Craft CMS 5 PHP Guidelines

Complete PHP coding standards and conventions for Craft CMS 5 plugin and module development. These extend Craft's official coding guidelines with project-specific conventions.

**Core principles:** PHPDocs on everything — classes, methods, and properties — regardless of type hints. No `declare(strict_types=1)` in plugin source files (matching Craft core convention).

## Companion Skills — Always Load Together

- **`craftcms`** — Architecture patterns, element lifecycle, controllers, events, migrations. Required for any Craft plugin or module development.
- **`ddev`** — All commands run through DDEV. Required for running ECS, PHPStan, scaffolding, and tests.

## Documentation

- Official coding guidelines: https://craftcms.com/docs/5.x/extend/coding-guidelines.html
- Class reference: https://docs.craftcms.com/api/v5/
- Generator reference: https://craftcms.com/docs/5.x/extend/generator.html

When unsure about a convention, `WebFetch` the coding guidelines page for the authoritative answer.

## Common Pitfalls

- `addSelect()` is the convention in `beforePrepare()` — safely additive when multiple extensions contribute columns.
- `$_instances` is not a Craft convention — private properties use underscore prefix but meaningful names like `$_items`, `$_sections`.
- Records use the **same class name** as models (namespace distinguishes). Alias when importing both: `use ...\records\MyEntity as MyEntityRecord;`.
- Queue jobs have **no "Job" suffix** — `ResaveElements`, not `ResaveElementsJob`.
- `declare(strict_types=1)` is NOT used in plugin source files. Only in standalone config files like `ecs.php`.
- `@author` goes on classes and methods only — never on properties.
- Don't use `string|null` — use `?string` (short nullable notation).
- Forget `parent::defineRules()` and you lose all inherited validation.
- `DateTimeHelper` in elements/queries, `Carbon` in services — never mix in the same class.
- Missing `@throws` chains — document exceptions from called methods too, not just your own throws.
- Using magic property access (`$plugin->settings`, `$app->view`) instead of explicit getters (`$plugin->getSettings()`, `$app->getView()`) — PHPStan can't resolve `__get()` calls, so magic access passes at runtime but fails static analysis. Always use explicit getters for Yii2 components and Craft plugin properties.

## Reference Files

Read the relevant reference file(s) for your task:

| Task | Read |
|------|------|
| Writing PHPDocs, `@author`, `@since`, `@throws`, `@var`, `@param`, type references | `references/phpdoc-standards.md` |
| Class structure, section headers, ordering, enums, control flow, comments, whitespace | `references/class-organization.md` |
| Naming classes, methods, properties, files, services, events, migrations | `references/naming-conventions.md` |
| CP Twig templates, form macros, translations, file headers, validation | `references/templates-and-patterns.md` |
| ECS, PHPStan, scaffolding commands, commit messages | `references/tooling.md` |

## Critical Rules

1. PHPDocs on everything: classes, methods, properties. No exceptions.
2. `@throws` chains: document every exception including uncaught from called methods.
3. `@author` and `@since` at the bottom of class/method docblocks, after a blank line.
4. Section headers with `// =========================================================================` on every class.
5. `declare(strict_types=1)` is NOT used in plugin source files — Craft's internal type coercion depends on PHP's default weak typing mode.
6. Private methods/properties prefixed with underscore: `_registerCpUrlRules()`, `$_items`.
7. `addSelect()` convention in `beforePrepare()` — additive across extensions, prevents column conflicts.
8. `DateTimeHelper` in elements/queries, `Carbon` in services — separate concerns prevent mixing date APIs in the same class.
9. Always scaffold with `ddev craft make <type> --with-docblocks`, then customize.
10. `ddev composer check-cs` and `ddev composer phpstan` must pass before every commit.

## PHP Standards

- Minimum PHP 8.2 (Craft CMS 5 requirement).
- PSR-12 baseline with Craft modifications (trailing commas, constant visibility).
- `craftcms/ecs` with `SetList::CRAFT_CMS_4` preset (covers both Craft 4 and 5).
- Short nullable notation: `?string` not `string|null`.
- Always specify `void` return types.
- Typed properties everywhere. No untyped public properties.
- Strict comparison always: `$foo === null`, `in_array($x, $y, true)`.
- Casts over functions: `(int)$foo` not `intval($foo)`.

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

## Control Flow

- **Happy path last.** Handle error conditions first with early returns.
- **Avoid `else`** — use early returns instead.
- **`match` over `switch`** — always.
- **Always use curly brackets** even for single statements.
- **Separate compound conditions** into nested `if` statements for readability.
- **Named arguments** when calling methods with 3+ parameters.

## Date Handling

- **Elements and element queries**: `craft\helpers\DateTimeHelper`.
- **Services** (date arithmetic): `Carbon\Carbon`.
- Never mix both in the same class.

## Database Conventions

- `[[column]]` quoting in Yii2 join conditions.
- `addSelect()` in `beforePrepare()` — safely additive.
- `postDate` and `expiryDate` in `addSelect()` and indexed on element tables.
- `Db::parseParam()` for query parameters. `Db::parseDateParam()` for dates.
- Foreign keys with explicit `CASCADE` / `SET NULL` behavior.

## Naming Quick-Reference

| Thing | Convention | Example |
|-------|-----------|---------|
| Services (resource) | Plural | `Entries`, `Volumes`, `Users` |
| Services (utility) | Domain noun | `Auth`, `Search`, `Gc` |
| Queue jobs | Action verb, no suffix | `ResaveElements`, `UpdateSearchIndex` |
| Records | Same name as model | Namespace distinguishes |
| Events | Three patterns | `SectionEvent`, `RegisterUrlRulesEvent`, `DefineHtmlEvent` |
| Element actions | Action verb, no suffix | `Delete`, `Duplicate`, `SetStatus` |
| Enums | PascalCase cases, string/int backed | `PropagationMethod`, `CmsEdition` |

For the complete naming reference including file structure conventions, read `references/naming-conventions.md`.

## Verification Checklist

Before every commit:

1. `ddev composer check-cs` passes
2. `ddev composer phpstan` passes
3. Tests green
4. PHPDocs complete on all new/modified code
5. `@throws` chains verified
6. Section headers present and correct
7. Imports alphabetical and grouped
