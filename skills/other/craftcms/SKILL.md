---
name: craftcms
description: "Craft CMS 5 plugin and module development — extending Craft with PHP. Covers elements, element queries, services, models, records, project config, controllers, CP templates, migrations, queue jobs, console commands, field types, native fields, events, behaviors, Twig extensions, utilities, widgets, filesystems, permissions, debugging, testing, GraphQL, and Craft configuration. Triggers on: beforePrepare(), afterSave(), defineSources(), defineTableAttributes(), attributeHtml(), MemoizableArray, BaseNativeField, EVENT_REGISTER_*/DEFINE_*/BEFORE_*/AFTER_*, CraftVariable, registerTwigExtension, custom element type, custom field type (normalizeValue, serializeValue, inputHtml), webhook, API endpoint, queue job, batch processing, CP section, control panel, element action, element exporter, element condition, dashboard widget, utility page, registerUserPermissions, requirePermission, GraphQL custom types/mutations, schema building, defineRules, canView/canSave/canDelete authorization, session invalidation, elevated session, BaseCondition, system messages, Mailer, atomic deploy, craft up, project-config/apply, drafts, revisions, GeneralConfig, $allowAnonymous. Always use when writing, editing, or reviewing Craft CMS plugin or module PHP code, even when no specific API names are mentioned. Do NOT trigger for front-end Twig (craft-site), content modeling (craft-content-modeling), or headless GraphQL consumption from Next.js/Nuxt/Astro."
---

# Craft CMS 5 — Extending (Plugins & Modules)

Reference for extending Craft CMS 5 through plugins and modules. Covers everything from elements and services to controllers, migrations, fields, and events.

This skill is scoped to **extending** Craft — building plugins, modules, custom element types, field types, and backend integrations. For site/platform development (content modeling, sections, entry types, Twig templating, plugin selection), see the `craft-site` skill.

## Companion Skills — Always Load Together

When this skill triggers, also load:

- **`craft-php-guidelines`** — PHPDoc standards, section headers, naming conventions, class organization, ECS/PHPStan, verification checklist. Required for any PHP code.
- **`ddev`** — All commands run through DDEV. Required for running ECS, PHPStan, scaffolding, and tests.
- **`craft-garnish`** — When working on CP JavaScript, asset bundles, or interactive CP components. Covers Garnish's class system, UI widgets (Modal, HUD, DisclosureMenu, Select), drag system, and the Craft.* JS class pattern.
- **`craft-cloud`** — When the project is hosted on Craft Cloud (detect via `craft-cloud.yaml` at the repo root or `craftcms/cloud` in `composer.json`). Required for plugin Cloud-compatibility constraints — `App::isEphemeral()` guards, asset-bundle CDN publishing, 15-minute queue-job cap, `csrfInput()` function over raw token output, and the `cloud/up` deploy lifecycle events.

## Documentation

- Extend guide: https://craftcms.com/docs/5.x/extend/
- Class reference: https://docs.craftcms.com/api/v5/
- Generator: https://craftcms.com/docs/5.x/extend/generator.html

Use `WebFetch` on specific doc pages when a reference file doesn't cover enough detail.

## Common Pitfalls (Cross-Cutting)

- Always use `addSelect()` in `beforePrepare()` — it's the Craft convention and safely additive when multiple extensions contribute columns.
- Queue workers run in primary site context — use `->site('*')` for cross-site queries.
- Including `id` in `getConfig()` — project config uses UIDs, never database IDs.
- Business logic in models or controllers — services are where logic belongs.
- Modules need manual template root, translation, and controllerNamespace registration — nothing is automatic.
- `DateTimeHelper` in elements/queries, `Carbon` in services — never mix in the same class.
- Hardcoding `/admin` in CP URLs — `cpTrigger` is configurable. Use `UrlHelper::cpUrl()` in PHP, `cpUrl()` in Twig.
- Passing `$request->getBodyParams()` directly to `savePluginSettings()` on split-settings pages — only submitted keys persist, other settings are silently dropped. Load the full settings model first, update properties, then save.

## Reference Files

Read the relevant reference file(s) for your task. Multiple files often apply together.

**Task examples:**
- "Build a custom element type" → read `elements.md` (Architecture section first) + `element-index.md` + `fields.md` + `migrations.md` + `cp.md`
- "Build a hierarchical/tree element type" → read `elements.md` (Architecture: One Element Class with Native Structure)
- "Add a webhook endpoint" → read `controllers.md` + `events.md`
- "Create a queue job that syncs elements" → read `queue-jobs.md` + `elements.md` + `debugging.md`
- "Add a settings page with form fields" → read `controllers.md` + `cp.md` + `architecture.md`
- "Register a custom field type" → read `fields.md` + `events.md`
- "Fix PHPStan errors" → read `quality.md`
- "Add a dashboard widget" → read `cp-components.md` (Dashboard Widgets) + `events.md` (Widget Types section)
- "Expose template variables for plugin users" → read `events.md` (Twig Extensions section)
- "Attach custom methods to entries" → read `events.md` (Behaviors section)
- "Build a CP utility page" → read `cp-components.md` (Utility Pages) + `events.md` (Utilities section)
- "Set up Vite for a plugin's CP assets" → read `plugin-vite.md` + load `craft-garnish` skill
- "Add drag-to-reorder or interactive JS to a CP page" → load `craft-garnish` skill
- "Write CP JavaScript for a custom field type" → read `fields.md` + load `craft-garnish` skill
- "Build a headless Craft API" → read `graphql.md` + load `craft-site` skill for `headless.md`
- "Configure preview for a Next.js front-end" → load `craft-site` skill for `headless.md`
- "Set up Pest tests for a plugin" → read `testing.md`
- "Write a test for a controller action" → read `testing.md`
- "Configure Redis for caching and sessions" → read `config-app.md`
- "Set up environment variables for production" → read `config-bootstrap.md`
- "Find a GeneralConfig setting" → read `config-general.md`
- "Read a config value in plugin code (App::env, parseEnv, GeneralConfig)" → read `config-bootstrap.md` + `config-general.md`
- "Check if allowAdminChanges is enabled in plugin code" → read `config-general.md` + `cp.md` (Read-Only Mode)
- "Resolve env vars in plugin settings ($MY_API_KEY)" → read `config-bootstrap.md` (App::parseEnv)
- "Understand CRAFT_* env var conventions" → read `config-bootstrap.md`
- "Configure mail transport / SMTP" → read `config-app.md`
- "Set up custom URL routes" → read `config-bootstrap.md`
- "Configure search to find short words" → read `config-app.md`
- "Set up GraphQL tokens and schemas" → read `graphql.md` + `config-general.md`
- "Set up caching for a high-traffic site" → read `caching.md`
- "Register custom permissions for my plugin" → read `permissions.md`
- "Check user permissions in templates" → read `permissions.md`
- "Set up plugin editions / feature gating" → read `architecture.md` (Plugin Editions section)
- "Upgrade a plugin from Craft 4 to 5" → read `quality.md` (Rector section)
- "Set up CI for a Craft plugin" → read `quality.md` (CI/CD Integration section)
- "Create sections or fields in a migration" → read `migrations.md` (Content Migrations section)
- "Set up database read replicas" → read `config-app.md` (Database Replicas section)
- "Register a module in app.php" → read `config-app.md` (Module Registration section)
- "Create a custom validator" → read `architecture.md` (Custom Validators section)
- "Create a custom filesystem type" → read `events.md` (Filesystem Types section)
- "Build a custom condition rule for an element index" → read `cp-ui-patterns.md` (Condition Builders)
- "Build a tri-state on/inherit/off control" → read `cp-ui-patterns.md` (Tri-State Inheritance Controls)
- "Add tabbed settings page to a plugin" → read `cp.md` (Tabbed Settings Pages)
- "Show an 'overrides global' warning on a field" → read `cp-ui-patterns.md` (Field Warning Parameter)
- "What CSS variables does Craft CP use?" → read `cp-ui-patterns.md` (Craft CSS Custom Properties)
- "Set up pre-commit hooks for code quality" → read `quality.md` (Pre-Commit Hooks section)
- "Restrict element access by user group" → read `element-authorization.md` + `permissions.md`
- "Scope CP element index by permission" → read `element-authorization.md` (Layer 3: Query Scoping)
- "Add authorization events to a custom element" → read `element-authorization.md` + `elements.md`
- "Build defense-in-depth for a security plugin" → read `element-authorization.md` (Defense Patterns)
- "Force-logout a user from all devices" → read `sessions-and-auth.md` (Plugin Patterns)
- "Understand how Craft sessions work" → read `sessions-and-auth.md`
- "Implement password reset required" → read `sessions-and-auth.md` (passwordResetRequired Gap)
- "Add a column to the Users element index" → read `element-index.md` (Extending Element Indexes via Events)
- "Add a bulk action to an element index" → read `element-index.md` (Adding a custom bulk action)
- "Add an action to the per-element edit-screen menu" → read `element-index.md` (Per-Element Edit-Screen Action Menu)
- "Render a status pill in a table column" → read `element-index.md` (Status Pills in Table Attributes)
- "Add a custom sidebar source to the element index" → read `element-index.md` (Adding a sidebar source)
- "Build a custom field type" → read `field-types-custom.md` + `fields.md`
- "Build a relation field type" → read `field-types-custom.md` (Relation Fields)
- "Add a condition rule to the entry index" → read `conditions.md` + `element-index.md`
- "Build a custom condition rule" → read `conditions.md`
- "Send email from a plugin" → read `email.md`
- "Register a custom system message" → read `email.md` (Registering Custom System Messages)
- "Configure SMTP transport" → read `config-app.md` + `email.md`
- "Deploy Craft CMS to production" → read `deployment.md`
- "Set up CI/CD for a Craft project" → read `deployment.md` (CI/CD Patterns)
- "Zero-downtime deploy" → read `deployment.md` (Zero-Downtime)
- "Roll back a failed deploy" → read `deployment.md` (Rollback Strategies)
- "Work with drafts and revisions" → read `drafts-revisions.md`
- "Create a draft programmatically" → read `drafts-revisions.md` (Creating Drafts)
- "Skip side effects for drafts in afterSave" → read `drafts-revisions.md` (Plugin Considerations)
- "Add generated fields to a custom element" → read `elements.md` (Generated Fields)
- "Customize how my element appears as a chip or card" → read `element-index.md` (Element Display Modes)
- "Add a screen to the User edit page" → read `elements.md` (Extending User Edit Screens)
- "Make plugin settings read-only when allowAdminChanges is off" → read `cp.md` (Read-Only Mode)
- "Add tabs to a plugin's settings page" → read `cp.md` (Settings Pages → With tabs or custom actions). `settingsHtml()` is single-pane only — tabs require a custom controller and a template extending `_layouts/cp` directly.
- "Make a plugin Cloud-compatible" → load `craft-cloud` skill → `plugin-development.md` (ephemeral filesystem, asset-bundle constraints, queue cap, CSRF function, cookie-free design)
- "Deploy a Craft project to Cloud" → load `craft-cloud` skill → `config-file.md` + `deploy-pipeline.md` + `extension.md`
- "Migrate a self-hosted Craft site to Cloud" → load `craft-cloud` skill → `migration.md`
- "Why does my plugin's file write silently fail on Cloud?" → load `craft-cloud` skill → `plugin-development.md` (Ephemeral filesystem) + `extension.md` (App::isEphemeral)

Load only the reference files your task needs — each file costs input tokens on every turn.

| Task | Read | ~Tokens |
|------|------|--------:|
| Element core: lifecycle, queries, status, authorization, drafts, revisions, propagation, field layouts, user edit screens, events | `references/elements.md` | 8.4K |
| Element index: sources, table/card attributes, status pills, sort, conditions, actions (bulk + per-element action menu), exporters, sidebar, metadata, extending via events | `references/element-index.md` | 6.1K |
| Services, models, records, project config, MemoizableArray, events, API clients, custom validators | `references/architecture.md` | 6.0K |
| Controllers: CP CRUD, webhooks, API endpoints, action routing, authorization | `references/controllers.md` | 3.9K |
| CP templates, form macros, settings pages, navigation, permissions, read-only mode | `references/cp.md` | 7.2K |
| CP components: dashboard widgets, utility pages, slideout editors, ajax, alerts | `references/cp-components.md` | 1.8K |
| CP UI patterns: tri-state controls, status indicators, CSS variables, condition builders, asset bundles | `references/cp-ui-patterns.md` | 2.4K |
| Database migrations, Install.php, foreign keys, indexes, idempotency, deployment | `references/migrations.md` | 3.9K |
| Queue jobs, BaseJob, TTR, retry, progress, batch jobs, site context | `references/queue-jobs.md` | 4.2K |
| Console commands, arguments, options, progress bars, output helpers, resave actions | `references/console-commands.md` | 6.0K |
| Debugging, performance, query strategy, profiling, Xdebug, caching, logging | `references/debugging.md` | 4.6K |
| PHPStan, ECS, code review checklist | `references/quality.md` | 3.5K |
| Testing: Pest setup, element factories, HTTP/queue/DB assertions, mocking, multi-site, console, events | `references/testing.md` | 2.9K |
| Field types, native fields, BaseNativeField, field layout elements, FieldLayoutBehavior | `references/fields.md` | 3.6K |
| Events: registration, lifecycle, naming conventions, custom events, behaviors, Twig extensions, utilities, widgets, filesystems | `references/events.md` | 4.4K |
| GraphQL types, queries, mutations, directives, schema components, resolvers | `references/graphql.md` | 4.6K |
| Plugin Vite: VitePluginService, CP asset bundles, HMR, TypeScript, Vue in CP | `references/plugin-vite.md` | 2.7K |
| Headless & hybrid: headlessMode, GraphQL API, CORS, preview tokens, front-end frameworks | craft-site skill `references/headless.md` | 3.4K |
| GeneralConfig (system, routing, security, users, sessions, search, assets, images) | `references/config-general.md` | 8.4K |
| GeneralConfig (content, templates, performance, GC, localization, headless, GraphQL, accessibility) | `references/config-general-extended.md` | 7.2K |
| App config: cache, session, queue, mutex, mailer/SMTP, search, logging, CORS, DB replicas | `references/config-app.md` | 5.5K |
| Config bootstrap: env vars, aliases, priority order, fluent API, custom.php, db.php, routes.php | `references/config-bootstrap.md` | 3.6K |
| Caching: template cache tag, data cache, static caching (Blitz), CDN, layered strategy, invalidation | `references/caching.md` | 5.2K |
| Permissions: built-in handles, user groups, custom registration, Twig/PHP checking, authorization events | `references/permissions.md` | 4.7K |
| Element authorization: four-layer defense model, authorization events, can*() methods, query scoping | `references/element-authorization.md` | 4.6K |
| Sessions & auth internals: dual-layer session model, auth tokens, session invalidation, elevated sessions | `references/sessions-and-auth.md` | 3.0K |
| Custom field types: build pattern, value lifecycle, settings, input HTML, validation, search, GraphQL | `references/field-types-custom.md` | 3.5K |
| Conditions framework: BaseCondition, ElementCondition, custom condition rules, registering rules | `references/conditions.md` | 2.3K |
| Email system: system messages, custom messages, programmatic sending, templates, events, testing | `references/email.md` | 2.4K |
| Deployment: standard pipeline, project config deploy, zero-downtime, CI/CD, rollback | `references/deployment.md` | 2.5K |
| Drafts & revisions: draft types, provisional drafts, autosave, applying, merge, revisions | `references/drafts-revisions.md` | 2.5K |

## Plugin vs Module Differences

Plugins and modules share the same architecture patterns. The differences are in bootstrapping and registration:

| Feature | Plugin | Module |
|---------|--------|--------|
| CP template root | Automatic (by handle) | Manual via `EVENT_REGISTER_CP_TEMPLATE_ROOTS` |
| Site template root | Manual via event | Same — manual for both |
| Translation category | Automatic (by handle) | Manual `PhpMessageSource` in `init()` |
| Settings model | Built-in `createSettingsModel()` | Env vars, config files, or private plugin (`_` prefix) |
| Install migration | `migrations/Install.php` | Content migrations only |
| Console commands | Automatic `controllerNamespace` | Must set before `parent::init()`, must be bootstrapped |
| CP nav section | `$hasCpSection = true` | `EVENT_REGISTER_CP_NAV_ITEMS` |
| Project config | Settings auto-tracked | Manual `ProjectConfig::set()` only |
| Namespace alias | Automatic via Composer | Must call `Craft::setAlias()` |

### Module Template Root Registration

```php
use craft\events\RegisterTemplateRootsEvent;
use craft\web\View;

Event::on(View::class, View::EVENT_REGISTER_CP_TEMPLATE_ROOTS,
    function(RegisterTemplateRootsEvent $event) {
        $event->roots['my-module'] = __DIR__ . '/templates';
    }
);
```

### Module Translation Registration

```php
Craft::$app->i18n->translations['my-module'] = [
    'class' => \craft\i18n\PhpMessageSource::class,
    'sourceLanguage' => 'en',
    'basePath' => __DIR__ . '/translations',
    'allowOverrides' => true,
];
```

### Module Console Command Registration

```php
public function init()
{
    Craft::setAlias('@mymodule', __DIR__);

    if (Craft::$app->getRequest()->getIsConsoleRequest()) {
        $this->controllerNamespace = 'modules\\mymodule\\console\\controllers';
    } else {
        $this->controllerNamespace = 'modules\\mymodule\\controllers';
    }

    parent::init(); // MUST come after setting controllerNamespace
}
```

The module **must** be bootstrapped in `config/app.php` for console commands to be discoverable.