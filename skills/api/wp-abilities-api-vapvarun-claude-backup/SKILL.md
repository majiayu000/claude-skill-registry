---
name: wp-abilities-api
description: "Use when working with the WordPress Abilities API: wp_register_ability, wp_register_ability_category, /wp-json/wp-abilities/v1/*, @wordpress/abilities for defining abilities, categories, REST exposure, and permission checks for clients."
compatibility: "Targets WordPress 6.9+ (PHP 8.0+). Abilities API may require plugin for older versions."
---

# WP Abilities API

## When to use

Use this skill when the task involves:

- Registering abilities or ability categories in PHP
- Exposing abilities to clients via REST (`wp-abilities/v1`)
- Consuming abilities in JS (`@wordpress/abilities`)
- Diagnosing "ability doesn't show up" / "client can't see ability"

## Inputs required

- Repo root and project type
- Target WordPress version(s)
- Where the change should live (plugin vs theme vs mu-plugin)

## Procedure

### 1) Register an ability category (optional)

Categories group related abilities:

```php
add_action('wp_abilities_api_categories_init', function() {
    wp_register_ability_category('my-plugin-features', array(
        'label'       => __('My Plugin Features', 'my-plugin'),
        'description' => __('Feature flags for My Plugin', 'my-plugin'),
    ));
});
```

### 2) Register abilities

```php
add_action('wp_abilities_api_init', function() {
    wp_register_ability('my-plugin/can-export', array(
        'label'       => __('Can Export Data', 'my-plugin'),
        'description' => __('User can export their data', 'my-plugin'),
        'category'    => 'my-plugin-features',
        'meta'        => array(
            'readonly'     => false,
            'show_in_rest' => true,
        ),
    ));
});
```

### 3) Check ability in PHP

```php
if (current_user_has_ability('my-plugin/can-export')) {
    // User has this ability
}
```

### 4) Expose via REST API

Abilities with `show_in_rest: true` are available at:

```
GET /wp-json/wp-abilities/v1/abilities
GET /wp-json/wp-abilities/v1/abilities/my-plugin%2Fcan-export
GET /wp-json/wp-abilities/v1/categories
```

### 5) Consume in JavaScript

```javascript
import { store, useAbility } from '@wordpress/abilities';

// Check if user has ability
const canExport = useAbility('my-plugin/can-export');

if (canExport) {
    // Show export button
}
```

### 6) Meta options

| Option | Purpose |
|--------|---------|
| `readonly` | If true, ability is informational only |
| `show_in_rest` | If true, exposed via REST API |
| `default` | Default value for the ability |

## Verification

- REST check: `wp-abilities/v1/abilities` returns your ability
- PHP check: `current_user_has_ability()` returns expected value
- JS check: `useAbility()` returns expected value

```bash
# Test REST endpoint
curl -X GET "https://example.com/wp-json/wp-abilities/v1/abilities" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Failure modes / debugging

**Ability never appears:**
- Registration code not running (wrong hook / file not loaded)
- Missing `meta.show_in_rest`
- Incorrect category/ID mismatch

**REST shows ability but JS doesn't:**
- Wrong REST base/namespace
- JS dependency not bundled
- Caching (object/page caches) masking changes

**Debug checklist:**

```bash
# Check if ability is registered
wp eval 'print_r(wp_get_abilities());'

# Check REST endpoint directly
wp rest get /wp-abilities/v1/abilities
```

## Escalation

If version support is unclear:
- Confirm target WP core versions
- Check if Abilities API is in core or requires plugin

Consult:
- [Abilities API Core Proposal](https://make.wordpress.org/core/)
- WordPress Developer Resources
