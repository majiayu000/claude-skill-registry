---
name: htmx-development
description: Use when implementing HTMX in Drupal, migrating from AJAX to HTMX, building dynamic forms, dependent dropdowns, infinite scroll, real-time validation, or multi-step wizards. Use when user says "HTMX", "migrate AJAX", "dependent dropdown", "dynamic form", "infinite scroll", "load more", "real-time validation", "multi-step wizard", "hx-get", "hx-post", "Htmx class". Use PROACTIVELY for any Drupal 11.3+ dynamic interaction that could use HTMX instead of AJAX. MUST check HTMX patterns before implementing AJAX callbacks.
version: 1.4.0
allowed-tools: Read, Glob, Grep
user-invocable: true
---

# HTMX Development

Drupal 11.3+ HTMX implementation and AJAX migration guidance.

## When to Use

- Implementing dynamic content updates in Drupal
- Building forms with dependent fields
- Migrating existing AJAX to HTMX
- Adding infinite scroll, load more, real-time validation
- NOT for: Traditional AJAX maintenance (use ajax-reference.md)

## Decision: HTMX vs AJAX

| Choose HTMX | Choose AJAX |
|-------------|-------------|
| New features | Existing AJAX code |
| Declarative HTML preferred | Complex command sequences |
| Returns HTML fragments | Dialog commands needed |
| Progressive enhancement needed | Contrib expects AJAX |

**Hybrid OK**: Both systems coexist. Migrate incrementally.

## Quick Start

### 1. Basic HTMX Element

```php
use Drupal\Core\Htmx\Htmx;
use Drupal\Core\Url;

$build['button'] = [
  '#type' => 'button',
  '#value' => t('Load'),
];

(new Htmx())
  ->get(Url::fromRoute('my.content'))
  ->onlyMainContent()
  ->target('#result')
  ->swap('innerHTML')
  ->applyTo($build['button']);
```

### 2. Controller Returns Render Array

```php
public function content() {
  return ['#markup' => '<p>Content loaded</p>'];
}
```

### 3. Route (Optional HTMX-Only)

```yaml
my.content:
  path: '/my/content'
  options:
    _htmx_route: TRUE  # Always minimal response
```

## Core Patterns

### Pattern Selection

| Use Case | Pattern | Key Methods |
|----------|---------|-------------|
| Dependent dropdown | Form partial update | `select()`, `target()`, `swap('outerHTML')` |
| Load more | Append content | `swap('beforeend')`, `trigger('click')` |
| Infinite scroll | Auto-load | `swap('beforeend')`, `trigger('revealed')` |
| Real-time validation | Blur check | `trigger('focusout')`, field update |
| Multi-step wizard | URL-based steps | `pushUrl()`, route parameters |
| Multiple updates | OOB swap | `swapOob('outerHTML:#selector')` |

### Dependent Dropdown

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['category'] = ['#type' => 'select', '#options' => $this->getCategories()];

  (new Htmx())
    ->post(Url::fromRoute('<current>'))
    ->onlyMainContent()
    ->select('#edit-subcategory--wrapper')
    ->target('#edit-subcategory--wrapper')
    ->swap('outerHTML')
    ->applyTo($form['category']);

  $form['subcategory'] = ['#type' => 'select', '#options' => []];

  // Handle trigger
  if ($this->getHtmxTriggerName() === 'category') {
    $form['subcategory']['#options'] = $this->getSubcategories(
      $form_state->getValue('category')
    );
  }

  return $form;
}
```

Reference: `core/modules/config/src/Form/ConfigSingleExportForm.php`

### Multiple Element Updates

```php
// Primary element updates via target
// Secondary element updates via OOB
(new Htmx())
  ->swapOob('outerHTML:[data-secondary]')
  ->applyTo($form['secondary'], '#wrapper_attributes');
```

### URL History

```php
(new Htmx())
  ->pushUrlHeader(Url::fromRoute('my.route', $params))
  ->applyTo($form);
```

## Htmx Class Reference

### Request Methods
- `get(Url)` / `post(Url)` / `put(Url)` / `patch(Url)` / `delete(Url)`

### Control Methods
- `target(selector)` - Where to swap
- `select(selector)` - What to extract from response
- `swap(strategy)` - How to swap (outerHTML, innerHTML, beforeend, etc.)
- `swapOob(selector)` - Out-of-band updates
- `trigger(event)` - When to trigger
- `vals(array)` - Additional values
- `onlyMainContent()` - Minimal response

### Response Headers
- `pushUrlHeader(Url)` - Update browser URL
- `redirectHeader(Url)` - Full redirect
- `triggerHeader(event)` - Fire client event
- `reswapHeader(strategy)` - Change swap
- `retargetHeader(selector)` - Change target

See: `references/quick-reference.md` for complete tables

## Detecting HTMX Requests

In forms (trait included automatically):

```php
if ($this->isHtmxRequest()) {
  $trigger = $this->getHtmxTriggerName();
}
```

In controllers (add trait):

```php
use Drupal\Core\Htmx\HtmxRequestInfoTrait;

class MyController extends ControllerBase {
  use HtmxRequestInfoTrait;
  protected function getRequest() { return \Drupal::request(); }
}
```

## Migration from AJAX

### Quick Conversion

| AJAX | HTMX |
|------|------|
| `'#ajax' => ['callback' => '::cb']` | `(new Htmx())->post()->applyTo()` |
| `'wrapper' => 'id'` | `->target('#id')` |
| `return $form['element']` | Logic in `buildForm()` |
| `new AjaxResponse()` | Return render array |
| `ReplaceCommand` | `->swap('outerHTML')` |
| `HtmlCommand` | `->swap('innerHTML')` |
| `AppendCommand` | `->swap('beforeend')` |
| `MessageCommand` | Auto-included |

### Migration Steps

1. Identify `#ajax` properties
2. Replace with `Htmx` class
3. Move callback logic to `buildForm()`
4. Use `getHtmxTriggerName()` for conditional logic
5. Replace `AjaxResponse` with render arrays
6. Test progressive enhancement

See: `references/migration-patterns.md` for detailed examples

## Validation Checklist

When reviewing HTMX implementations:

- [ ] `Htmx` class used (not raw attributes)
- [ ] `onlyMainContent()` for minimal response
- [ ] Proper swap strategy selected
- [ ] OOB used for multiple updates
- [ ] Trigger element detection works
- [ ] Works without JavaScript (progressive)
- [ ] Accessibility: `aria-live` for dynamic regions
- [ ] URL updates for bookmarkable states

## Common Issues

| Problem | Solution |
|---------|----------|
| Content not swapping | Check `target()` selector exists |
| Wrong content extracted | Check `select()` selector |
| JS not running | Verify `htmx:drupal:load` fires |
| Form not submitting | Check `post()` and URL |
| Multiple swaps fail | Add `swapOob('true')` to elements |
| History broken | Use `pushUrlHeader()` |

## References

### Bundled (HTMX-Specific)
- `references/quick-reference.md` - Command equivalents, method tables
- `references/htmx-implementation.md` - Full Htmx class API, detection, JS
- `references/migration-patterns.md` - 7 patterns with before/after code
- `references/ajax-reference.md` - AJAX commands for understanding existing code

### Online Dev-Guides

For deeper Drupal context beyond bundled references, use the dev-guides-navigator plugin:

Invoke `/dev-guides-navigator` with keywords like "Drupal forms", "routing", "JS development", or "render API". The navigator handles caching and disambiguation — never fetch dev-guides URLs directly.

Relevant topics: drupal/forms (FAPI with HTMX), drupal/routing (HTMX routes), drupal/js-development (behaviors + HTMX events), drupal/render-api (render arrays for HTMX responses).

## Key Files in Drupal Core

- `core/lib/Drupal/Core/Htmx/Htmx.php` - Main API
- `core/lib/Drupal/Core/Htmx/HtmxRequestInfoTrait.php` - Request detection
- `core/lib/Drupal/Core/Render/MainContent/HtmxRenderer.php` - Response renderer
- `core/modules/config/src/Form/ConfigSingleExportForm.php` - Production example
- `core/modules/system/tests/modules/test_htmx/` - Test examples
