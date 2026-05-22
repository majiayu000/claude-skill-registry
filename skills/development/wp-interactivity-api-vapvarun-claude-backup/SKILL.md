---
name: wp-interactivity-api
description: "Use when building or debugging WordPress Interactivity API features: data-wp-* directives, @wordpress/interactivity store/state/actions, block viewScriptModule integration, performance, hydration, and directive behavior."
compatibility: "Targets WordPress 6.9+ (PHP 8.0+). Requires @wordpress/scripts for building."
---

# WP Interactivity API

## When to use

Use this skill when the user mentions:

- Interactivity API, `@wordpress/interactivity`
- `data-wp-interactive`, `data-wp-on--*`, `data-wp-bind--*`, `data-wp-context`
- Block `viewScriptModule` / module-based view scripts
- Hydration issues or "directives don't fire"

## Inputs required

- Repo root + project type (plugin, theme, block)
- Which surfaces are affected (frontend, editor, both)
- WordPress version constraints

## Procedure

### 1) Set up interactivity in a block

**block.json:**

```json
{
  "name": "my-plugin/interactive-block",
  "title": "Interactive Block",
  "viewScriptModule": "file:./view.js",
  "supports": {
    "interactivity": true
  }
}
```

**view.js (ES module):**

```javascript
import { store, getContext } from '@wordpress/interactivity';

store('my-plugin', {
  state: {
    get isOpen() {
      return getContext().isOpen;
    }
  },
  actions: {
    toggle() {
      const context = getContext();
      context.isOpen = !context.isOpen;
    }
  }
});
```

### 2) Core directives reference

| Directive | Purpose | Example |
|-----------|---------|---------|
| `data-wp-interactive` | Activate interactivity on element | `data-wp-interactive="my-plugin"` |
| `data-wp-context` | Provide local state | `data-wp-context='{"isOpen": false}'` |
| `data-wp-bind--attr` | Bind attribute to state | `data-wp-bind--aria-expanded="state.isOpen"` |
| `data-wp-on--event` | Handle events | `data-wp-on--click="actions.toggle"` |
| `data-wp-class--name` | Toggle CSS class | `data-wp-class--is-open="state.isOpen"` |
| `data-wp-text` | Set text content | `data-wp-text="state.count"` |
| `data-wp-watch` | Run side effects | `data-wp-watch="callbacks.logChanges"` |

### 3) PHP render with directives

```php
<?php
$context = array( 'isOpen' => false );
?>
<div
  <?php echo get_block_wrapper_attributes(); ?>
  data-wp-interactive="my-plugin"
  <?php echo wp_interactivity_data_wp_context( $context ); ?>
>
  <button data-wp-on--click="actions.toggle">
    Toggle
  </button>
  <div data-wp-bind--hidden="!state.isOpen">
    Content here
  </div>
</div>
```

### 4) WordPress 6.9 changes

**Deprecated:**
- `data-wp-ignore` is deprecated - avoid using it

**New features:**
- Unique directive IDs with `---` separator:
  ```html
  data-wp-on--click---plugin-a="actions.handleA"
  data-wp-on--click---plugin-b="actions.handleB"
  ```
- New TypeScript types: `AsyncAction<ReturnType>`, `TypeYield<T>`
- `getServerState()` and `getServerContext()` reset between page transitions

### 5) Create interactive block from scratch

```bash
npx @wordpress/create-block@latest my-interactive-block --template @wordpress/create-block-interactive-template
```

This scaffolds:
- block.json with `viewScriptModule`
- view.js with store setup
- render.php with directives

## Verification

- Manual smoke test: directive triggers and state updates as expected
- View script loads in browser Network tab
- No JS console errors before hydration
- If tests exist: add/extend Playwright E2E

## Failure modes / debugging

**Directives not firing:**
- View script not loading - check `viewScriptModule` path
- Missing `data-wp-interactive` on parent element
- Store namespace mismatch
- JS errors before hydration

**Hydration mismatch / flicker:**
- Server markup differs from client expectations
- Simplify or align initial state

**Performance issues:**
- Overly broad interactive roots
- Scope interactivity to smaller subtrees

**Debug checklist:**

```bash
# Check view script is registered
wp eval 'print_r(wp_scripts()->registered);' | grep "view"

# Check for interactivity usage
grep -r "data-wp-interactive" .
grep -r "@wordpress/interactivity" .
```

## Escalation

If build constraints are unclear, ask:
> "Is this using @wordpress/scripts or a custom bundler (webpack/vite)?"

Consult:
- [Interactivity API Reference](https://developer.wordpress.org/block-editor/reference-guides/interactivity-api/)
- [Interactivity API Docs](https://make.wordpress.org/core/tag/interactivity-api/)
