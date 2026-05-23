---
name: kirby-routing-and-representations
description: Implements custom Kirby routes and content representations (.json/.xml/.rss), including redirects, sitemap endpoints, and URL pattern filtering. Use when building endpoints, redirects, or representation templates that change how URLs resolve.
---

# Kirby Routing and Representations

## KB entry points

- `kirby://kb/scenarios/13-custom-routes`
- `kirby://kb/scenarios/21-filtering-via-routes`
- `kirby://kb/scenarios/49-sitemap-xml-route`
- `kirby://kb/scenarios/78-trailing-slash-and-canonical-urls`
- `kirby://kb/scenarios/02-json-content-representation-ajax-load-more`

## Required inputs

- URL pattern and HTTP methods.
- Response type and content language behavior.
- Redirect or canonicalization rules.

## Decision guide

- Use content representations for page-backed JSON/XML/RSS.
- Use routes for non-page endpoints, redirects, or custom logic.
- Avoid greedy patterns that shadow representations.

## Pattern hint

- Put specific routes before catch-alls; avoid top-level `(:all)` when using representations.

## Canonical redirect example

```php
[
  'pattern' => '(:any)/',
  'action' => function ($path) {
    return go('/' . trim($path, '/'), 301);
  }
]
```

## Common pitfalls

- Route patterns that shadow `.json` or `.rss` representations.
- Expecting `kirby:kirby_render_page` to execute route logic.

## Workflow

1. Clarify the URL pattern, HTTP methods, response type, and language behavior.
2. Call `kirby:kirby_init` and read `kirby://roots` to locate config and template roots.
3. Read `kirby://config/routes` to understand current route configuration.
4. If runtime is available, call `kirby:kirby_routes_index` to see registered patterns; otherwise run `kirby:kirby_runtime_status` and `kirby:kirby_runtime_install` first.
5. Inspect existing templates/controllers to avoid collisions:
   - `kirby:kirby_templates_index`
   - `kirby:kirby_controllers_index`
6. For content representations, add `site/templates/<template>.<type>.php` and optional `site/controllers/<template>.<type>.php`.
7. For routes, add or adjust `routes` in `site/config/config.php` or a plugin. Avoid greedy patterns that shadow `.json`/`.rss` representations.
8. Validate output:
   - use `kirby:kirby_render_page(contentType: json|xml|rss)` for representations
   - manually hit route URLs for router behavior (render does not execute the router)
9. Search the KB with `kirby:kirby_search` (examples: "custom routes", "json content representation", "filtering via routes", "sitemap.xml", "trailing slash").
