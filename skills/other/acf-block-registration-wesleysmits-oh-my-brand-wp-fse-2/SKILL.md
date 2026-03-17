---
name: acf-block-registration
description: Guide for creating ACF PRO blocks with field groups in Oh My Brand! FSE theme. Use this when registering ACF blocks, creating field groups, or working with ACF-specific render templates.
metadata:
  author: Wesley Smits
  version: "1.0.0"
---

# ACF Block Registration

Creating ACF PRO blocks with custom field groups for the Oh My Brand! FSE theme.

---

## When to Use

- Creating blocks that use ACF field groups for content entry
- Building blocks with repeater fields, galleries, or complex field layouts
- Leveraging ACF PRO features (repeaters, flexible content, clone fields)
- Rapid block prototyping with ACF's visual field editor

---

## ACF vs Native Blocks

| Aspect | ACF Block | Native Block |
|--------|-----------|--------------|
| **Schema** | `https://advancedcustomfields.com/schemas/json/main/block.json` | `https://schemas.wp.org/trunk/block.json` |
| **Name prefix** | `acf/` | `theme-oh-my-brand/` |
| **API Version** | 2 | 3 |
| **Attributes** | Defined in ACF field groups | Defined in `block.json` |
| **Data access** | `get_field()` | `$attributes` array |
| **Render property** | `acf.renderTemplate` | `render` |
| **Editor experience** | ACF field forms | Custom React components |
| **Best for** | Content-heavy blocks, rapid prototyping | Complex interactivity, custom UI |

---

## Block File Structure

ACF blocks live in `blocks/acf-{block-name}/`:

```
blocks/acf-faq/
├── block.json          # ACF block metadata (ACF schema)
├── render.php          # Render template (referenced in block.json)
├── helpers.php         # Block-specific helper functions
├── style.css           # Frontend styles (auto-enqueued)
└── editor.css          # Editor-only styles (optional)
```

Field groups are stored separately in `acf-json/`.

---

## File Templates

Use templates from [block-scaffolds](../block-scaffolds/SKILL.md):

| File | Template | Purpose |
|------|----------|---------|
| `block.json` | [block-json-acf.json](../block-scaffolds/references/block-json-acf.json) | ACF block metadata |
| `render.php` | [render-acf.php](../block-scaffolds/references/render-acf.php) | Render template |
| `helpers.php` | [helpers-acf.php](../block-scaffolds/references/helpers-acf.php) | Helper functions |
| Field group | [field-group-scaffold.json](../block-scaffolds/references/field-group-scaffold.json) | ACF field group |

### Full Examples

| Example | Purpose |
|---------|---------|
| [render-faq-example.php](../block-scaffolds/references/render-faq-example.php) | Complete FAQ render with JSON-LD |
| [helpers-faq-example.php](../block-scaffolds/references/helpers-faq-example.php) | Complete FAQ helpers |
| [block-registration.php](../block-scaffolds/references/block-registration.php) | PHP registration function |
| [acf-json-sync.php](../block-scaffolds/references/acf-json-sync.php) | ACF local JSON config |

---

## block.json Key Properties (ACF)

| Property | Required | Description |
|----------|----------|-------------|
| `$schema` | Yes | `https://advancedcustomfields.com/schemas/json/main/block.json` |
| `name` | Yes | Format: `acf/{block-name}` |
| `acf.mode` | Yes | `preview`, `edit`, or `auto` |
| `acf.renderTemplate` | Yes | Path to render PHP file |
| `style` | Optional | `file:./style.css` |

### ACF Mode Options

| Mode | Description |
|------|-------------|
| `preview` | Shows rendered block output, click to edit fields |
| `edit` | Shows ACF field form directly |
| `auto` | Switches between preview and edit automatically |

---

## Field Group Structure

Field groups connect to blocks via location rules:

```json
"location": [
    [
        {
            "param": "block",
            "operator": "==",
            "value": "acf/faq"
        }
    ]
]
```

### Title Conventions

| Type | Title Format | Example |
|------|--------------|---------|
| Block field groups | `Block: {Block Name}` | `Block: FAQ` |
| Options pages | `{Page Name} Settings` | `Theme Settings` |
| Post type fields | `{Post Type} Fields` | `Company Fields` |

---

## Render Template Guidelines

| Guideline | Description |
|-----------|-------------|
| `declare(strict_types=1)` | Always include at top |
| Helper file | Use `require_once __DIR__ . '/helpers.php'` |
| Data retrieval | Use helper functions, not inline `get_field()` |
| Empty state check | Return early if no data (except in editor) |
| `get_block_wrapper_attributes()` | Use for consistent wrapper |
| Editor placeholder | Show message when data is empty in editor |

### Template Variables

| Variable | Type | Description |
|----------|------|-------------|
| `$block` | `array` | Block settings (id, name, className, align) |
| `$content` | `string` | Inner HTML (usually empty for ACF blocks) |
| `$is_preview` | `bool` | True when rendering in editor preview |
| `$post_id` | `int` | Post ID where block is used |
| `$context` | `array` | Block context values |

---

## Helper Function Guidelines

| Guideline | Description |
|-----------|-------------|
| `function_exists()` guard | Wrap functions in existence check |
| Default values | Always provide defaults with `?: []` or `?? ''` |
| Type hints | Use parameter and return type declarations |
| Data transformation | Normalize ACF field names to consistent keys |
| ACF guard | Check `function_exists('get_field')` |

---

## Common Field Types

### Repeater Field

```php
$items = get_field('repeater_field_name') ?: [];

foreach ($items as $item) {
    $sub_value = $item['sub_field_name'] ?? '';
}
```

### Gallery Field

```php
$images = get_field('gallery') ?: [];

foreach ($images as $image) {
    $url = $image['url'] ?? '';
    $alt = $image['alt'] ?? '';
}
```

### Image Field

```php
$image = get_field('image');

if ($image) {
    $url = $image['url'];
    $alt = $image['alt'];
}
```

### Options Page Fields

```php
$logo = get_field('site_logo', 'option');
```

---

## Step-by-Step Creation

1. **Create directory**: `mkdir -p blocks/acf-my-block`
2. **Add block.json**: Copy from [template](../block-scaffolds/references/block-json-acf.json), use ACF schema
3. **Create field group**: In WP Admin > ACF > Field Groups
   - Title: `Block: {Block Name}`
   - Location: Block equals `acf/{block-name}`
4. **Create render.php**: Copy from [template](../block-scaffolds/references/render-acf.php)
5. **Create helpers.php**: Copy from [template](../block-scaffolds/references/helpers-acf.php)
6. **Add style.css**: See [css-standards](../css-standards/SKILL.md)
7. **Register block**: Add to `$acf_blocks` array in `functions.php`
8. **Verify**: Block appears in editor and renders correctly

Or use the scaffolding script:
```bash
.github/skills/block-scaffolds/scripts/create-block.sh acf my-block "My Block Title"
```

---

## Related Skills

- [block-scaffolds](../block-scaffolds/SKILL.md) - Copy-paste templates
- [php-standards](../php-standards/SKILL.md) - PHP conventions
- [css-standards](../css-standards/SKILL.md) - CSS conventions
- [phpunit-testing](../phpunit-testing/SKILL.md) - Testing ACF blocks
- [native-block-development](../native-block-development/SKILL.md) - Native blocks

---

## References

- [ACF Block Registration](https://www.advancedcustomfields.com/resources/blocks/)
- [ACF Block JSON Schema](https://www.advancedcustomfields.com/resources/acf-blocks-with-block-json/)
- [ACF Field Types](https://www.advancedcustomfields.com/resources/#field-types)
- [ACF Local JSON](https://www.advancedcustomfields.com/resources/local-json/)
