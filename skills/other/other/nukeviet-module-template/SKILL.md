---
   name: nukeviet-module-template
   description: Secure, production-ready template for NukeViet 5.x modules using Smarty Template Engine
---

# NukeViet 5.x Module Template

Secure, production-ready template for NukeViet 5.x modules using **Smarty Template Engine**.

## Features

✅ Full CSRF protection
✅ Prepared statements for all queries
✅ XSS prevention with auto-escaping
✅ Input validation
✅ Error handling
✅ Caching support
✅ **Smarty template engine**
✅ **$nv_Lang object for language**
✅ Bootstrap 5 UI
✅ Multi-language support

## NukeViet 5.x Standards

### Language System
- Use `$nv_Lang->getModule('key')` instead of `$lang_module['key']`
- Language files: `language/data_vi.php` (admin), `language/vi.php` (frontend)
- In templates: `{$LANG->getModule('title')}`

### Template Engine
- **Smarty** instead of XTemplate
- `$tpl = new \NukeViet\Template\NVSmarty();`
- `$tpl->fetch('template.tpl')`
- Smarty syntax: `{$var}`, `{if}`, `{foreach}`, etc.

## Structure

```
example/
├── action_mysql.php          # Database schema
├── version.php                # Module metadata
├── admin.menu.php            # Admin menu
├── admin.functions.php       # Helper functions
├── admin/
│   ├── main.php             # List items (Smarty)
│   ├── content.php          # Add/Edit item (Smarty)
│   └── del.php              # Delete item
├── language/
│   ├── vi.php               # Frontend Vietnamese
│   ├── data_vi.php          # Admin Vietnamese
│   ├── en.php               # Frontend English
│   └── data_en.php          # Admin English
└── templates/
    ├── main.tpl             # Smarty list template
    └── content.tpl          # Smarty form template
```

## Quick Start

```bash
# Copy template
cp -r .claude/skills/templates/nukeviet-module-template modules/mymodule

# Replace module name
cd modules/mymodule
find . -type f -exec sed -i 's/example/mymodule/g' {} +

# Customize schema
# Edit action_mysql.php

# Install via admin panel
# Admin -> Extensions -> Modules -> Install
```

## Key Differences from NukeViet 4.x

| Feature | NV 4.x | NV 5.x |
|---------|--------|--------|
| Template | XTemplate | **Smarty** |
| Language | `$lang_module['key']` | **`$nv_Lang->getModule('key')`** |
| Lang Files | `language/vi/admin_module.php` | **`language/data_vi.php`** |
| Syntax | `{LANG.key}` | **`{$LANG->getModule('key')}`** |
| Constants | `<!-- BEGIN: main -->` | **`{* BEGIN: main *}`** |

## Security Features

- All database queries use PDO prepared statements
- CSRF tokens on all forms
- Input validation on all fields
- XSS prevention with Smarty auto-escaping
- Transaction support for data integrity
- Proper error logging

## Smarty Template Examples

### Variables
```smarty
{$DATA.title}
{$smarty.const.NV_BASE_ADMINURL}
{$LANG->getModule('item_list')}
{$LANG->getGlobal('save')}
```

### Control Structures
```smarty
{if not empty($ERROR)}
    <div class="alert alert-danger">{$ERROR|@join:"<br />"}</div>
{/if}

{foreach from=$ITEMS item=item}
    <tr>
        <td>{$item.title}</td>
    </tr>
{/foreach}
```

### Escaping
```smarty
{* Auto-escaped *}
{$user_input}

{* JavaScript escape *}
onclick="alert('{$item.title|escape:'javascript'}')"

{* No escape (use carefully) *}
{$html_content nofilter}
```

## License

Same as NukeViet CMS
