---
name: craftcms
description: "Craft CMS 5 plugin and module development — extending Craft with PHP. Covers the full extend surface: elements, element queries, services, models, records, project config, controllers, CP templates, migrations, queue jobs, console commands, field types, native fields, events, behaviors, Twig extensions, utilities, widgets, filesystems, permissions, debugging, testing, GraphQL, and Craft configuration (config/app.php, config/general.php, Redis, SMTP, database replicas). Triggers on: beforePrepare(), afterSave(), defineSources(), defineTableAttributes(), attributeHtml(), MemoizableArray, getConfig(), handleChanged, $allowAnonymous, $enableCsrfValidation, BaseNativeField, EVENT_DEFINE_NATIVE_FIELDS, FieldLayoutBehavior, EVENT_REGISTER, EVENT_DEFINE, EVENT_BEFORE, EVENT_AFTER, CraftVariable, registerTwigExtension, DefineConsoleActionsEvent, PHPStan, Pest, plugin development, module development, custom element type, custom field type, webhook, API endpoint, queue job, batch processing, data sync, migration, CP section, control panel, Craft plugin, Craft module, extending Craft, element action, element exporter, element condition, dashboard widget, utility page, permissions, registerUserPermissions, requirePermission, GraphQL custom types, GraphQL custom mutations, GraphQL schema building, Rector, Craft 4 to 5, upgrade plugin, CI/CD, GitHub Actions, GitLab CI, custom validator, defineRules, EVENT_AUTHORIZE_VIEW, EVENT_AUTHORIZE_SAVE, canView, canSave, canDelete, element authorization, defense-in-depth, query scoping, EVENT_BEFORE_PREPARE, session invalidation, passwordResetRequired, elevated session, Table::SESSIONS, custom field type build, field type development, normalizeValue, serializeValue, inputHtml, BaseCondition, ElementCondition, condition rule, condition builder, system messages, composeFromKey, email sending, Mailer, deployment, zero-downtime deploy, atomic deploy, craft up, project-config/apply, allowAdminChanges, drafts, revisions, provisional draft, canCreateDrafts, applyDraft, getIsDraft, getIsRevision. Always use when writing, editing, or reviewing any Craft CMS plugin or module PHP code — even when the user asks about plugin architecture, Craft internals, or extending Craft without naming specific APIs. Do NOT trigger for front-end Twig templates, content modeling decisions, site-building without PHP, or consuming GraphQL/headless APIs from front-end frameworks (Next.js, Nuxt, Astro) — those belong in craft-site."
---

# Craft CMS 5 — Extending (Plugins & Modules)

Reference for extending Craft CMS 5 through plugins and modules. Covers everything from elements and services to controllers, migrations, fields, and events.

This skill is scoped to **extending** Craft — building plugins, modules, custom element types, field types, and backend integrations. For site/platform development (content modeling, sections, entry types, Twig templating, plugin selection), see the `craft-site` skill.

## Companion Skills — Always Load Together

When this skill triggers, also load:

- **`craft-php-guidelines`** — PHPDoc standards, section headers, naming conventions, class organization, ECS/PHPStan, verification checklist. Required for any PHP code.
- **`ddev`** — All commands run through DDEV. Required for running ECS, PHPStan, scaffolding, and tests.
- **`craft-garnish`** — When working on CP JavaScript, asset bundles, or interactive CP components. Covers Garnish's class system, UI widgets (Modal, HUD, DisclosureMenu, Select), drag system, and the Craft.* JS class pattern.

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

## Reference Files

Read the relevant reference file(s) for your task. Multiple files often apply together.

**Task examples:**
- "Build a custom element type" → read `elements.md` + `element-index.md` + `fields.md` + `migrations.md` + `cp.md`
- "Add a webhook endpoint" → read `controllers.md` + `events.md`
- "Create a queue job that syncs elements" → read `queue-jobs.md` + `elements.md` + `debugging.md`
- "Add a settings page with form fields" → read `controllers.md` + `cp.md` + `architecture.md`
- "Register a custom field type" → read `fields.md` + `events.md`
- "Fix PHPStan errors" → read `quality.md`
- "Add a dashboard widget" → read `cp.md` (Dashboard Widgets) + `events.md` (Widget Types section)
- "Expose template variables for plugin users" → read `events.md` (Twig Extensions section)
- "Attach custom methods to entries" → read `events.md` (Behaviors section)
- "Build a CP utility page" → read `events.md` (Utilities section) + `cp.md`
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
- "Build a custom condition rule for an element index" → read `cp.md` (Condition Builders section)
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

| Task | Read |
|------|------|
| Element core: lifecycle, queries, status, authorization, drafts, revisions, propagation, field layouts, events | `references/elements.md` |
| Element index: sources, table/card attributes, sort, conditions, actions, exporters, sidebar, metadata, extending via events (columns, sources, bulk actions, condition rules, sort) | `references/element-index.md` |
| Services, models, records, project config, MemoizableArray, events, API clients, custom validators | `references/architecture.md` |
| Controllers: CP CRUD, webhooks, API endpoints, action routing, authorization | `references/controllers.md` |
| CP templates, form macros, admin changes, VueAdminTable, asset bundles, CP layout, permissions. For CP JavaScript interactions, also load `craft-garnish` skill. | `references/cp.md` |
| Database migrations, Install.php, foreign keys, indexes, idempotency, deployment | `references/migrations.md` |
| Queue jobs, BaseJob, TTR, retry, progress, batch jobs, site context | `references/queue-jobs.md` |
| Console commands, arguments, options, progress bars, output helpers, resave actions | `references/console-commands.md` |
| Debugging, performance, query strategy, profiling, Xdebug, caching, logging | `references/debugging.md` |
| PHPStan, ECS, code review checklist | `references/quality.md` |
| Testing: Pest setup, element factories, HTTP/queue/DB assertions, mocking, multi-site, console, events | `references/testing.md` |
| Field types, native fields, BaseNativeField, field layout elements, FieldLayoutBehavior | `references/fields.md` |
| Events: registration, lifecycle, naming conventions, custom events, behaviors, Twig extensions, utilities, widgets, filesystems, discovering events | `references/events.md` |
| GraphQL types, queries, mutations, directives, schema components, resolvers | `references/graphql.md` |
| Plugin Vite: VitePluginService, CP asset bundles, HMR, TypeScript, Vue in CP | `references/plugin-vite.md` |
| Headless & hybrid: headlessMode, GraphQL API, CORS, preview tokens, front-end frameworks | craft-site skill `references/headless.md` |
| GeneralConfig (system, routing, security, users, sessions, search, assets, images) | `references/config-general.md` |
| GeneralConfig (content, templates, performance, GC, localization, headless, GraphQL, accessibility, preview, dev, dangerous interactions) | `references/config-general-extended.md` |
| App config: cache, session, queue, mutex, mailer/SMTP, search, logging, CORS, DB replicas, web/console split | `references/config-app.md` |
| Config bootstrap: env vars, aliases, priority order, fluent API, custom.php, db.php, routes.php, htmlpurifier | `references/config-bootstrap.md` |
| Caching: template cache tag, data cache, static caching (Blitz), CDN, layered strategy, invalidation | `references/caching.md` |
| Permissions: built-in handles, user groups, custom registration, Twig/PHP checking, authorization events, strategies | `references/permissions.md` |
| Element authorization: four-layer defense model, authorization events, can*() methods, EVENT_BEFORE_PREPARE query scoping, controller enforcement | `references/element-authorization.md` |
| Sessions & auth internals: dual-layer session model, auth tokens, session invalidation, passwordResetRequired, elevated sessions, plugin patterns | `references/sessions-and-auth.md` |
| Custom field types: build pattern, value lifecycle, settings, input HTML, validation, search, GraphQL, relation fields | `references/field-types-custom.md` |
| Conditions framework: BaseCondition, ElementCondition, custom condition rules, registering rules, condition builder UI | `references/conditions.md` |
| Email system: system messages, custom messages, programmatic sending, templates, events, testing | `references/email.md` |
| Deployment: standard pipeline, project config deploy, zero-downtime, CI/CD, rollback, environment management | `references/deployment.md` |
| Drafts & revisions: draft types, provisional drafts, autosave, applying, merge, revisions, plugin considerations | `references/drafts-revisions.md` |

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