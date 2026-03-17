---
name: kirby-collections-and-navigation
description: Builds Kirby listings, pagination, search, filtering/sorting/grouping, and navigation menus. Use when implementing collection logic in templates/controllers/snippets.
---

# Kirby Collections and Navigation

## KB entry points

- `kirby://kb/scenarios/07-pagination`
- `kirby://kb/scenarios/08-search-page`
- `kirby://kb/scenarios/09-filtering-with-tags`
- `kirby://kb/scenarios/11-navigation-menus`
- `kirby://kb/scenarios/23-collections-filtering`

## Required inputs

- Collection source (page/section/template or ids).
- Filters, sort order, and pagination size.
- Target templates/snippets and UI expectations.

## Default pattern

- Keep collection building in the controller; return a single `items` collection and `pagination`.
- Render items via a snippet to avoid repeated template logic.
- Provide empty-state and active-navigation UI.
- Default sort: use `date desc` when the field exists; otherwise fall back to `title asc`.

## Example

Controller:

```php
return function ($page) {
  $items = $page->children()->listed()->sortBy('date', 'desc')->paginate(10);
  return [
    'items' => $items,
    'pagination' => $items->pagination(),
  ];
};
```

Snippet:

```php
<?php if ($items->isEmpty()): ?>
  <p>No items yet.</p>
<?php else: ?>
  <?php foreach ($items as $item): ?>
    <!-- render item -->
  <?php endforeach ?>
  <?php snippet('pagination', ['pagination' => $pagination]) ?>
<?php endif ?>
```

## Output checklist

- Ensure pagination URLs preserve filters and tags.
- Render empty states without PHP notices.
- Confirm active navigation matches the current page.

## Common pitfalls

- Dropping query params or tag filters on pagination links.
- Implementing heavy collection logic in templates instead of controllers.

## Workflow

1. Clarify collection scope (site vs section), filters, sort order, and UI (pagination, tag filters, menu style).
2. Call `kirby:kirby_init` and read `kirby://roots`.
3. Inspect existing templates/controllers/snippets to reuse patterns:
   - `kirby:kirby_templates_index`
   - `kirby:kirby_controllers_index`
   - `kirby:kirby_snippets_index`
4. Prefer controllers for collection logic; keep templates thin.
5. Search the KB with `kirby:kirby_search` for task playbooks (examples: "pagination", "search page", "filtering with tags", "navigation menus", "collections filtering").
6. Implement or adjust collection queries; add snippets for repeated UI.
7. Verify rendering and pagination URLs with `kirby:kirby_render_page(noCache=true)`.
