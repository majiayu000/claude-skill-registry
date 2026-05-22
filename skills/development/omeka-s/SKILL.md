---
name: omeka-s
description: Expert Omeka S developer assistant for Docker-based installations. Covers theme development (SCSS/CSS, templates), module creation (PHP, events, database), configuration management, and troubleshooting. Use for Omeka S customization from simple CSS tweaks to advanced module development.
license: MIT
category: api-integration
---

# Omeka S Development Skill

Expert guidance for Docker-based Omeka S development - from simple CSS tweaks to advanced module development.

## Quick Start

### Installation Context

**Docker-based installation** - All operations use Docker commands:
- **Container**: `omeka-s-app` (application), `omeka-s-db` (database)
- **Base path**: `/var/www/html/` inside container
- **Version check**: `docker exec omeka-s-app cat /var/www/html/application/Module.php | grep VERSION`

### Essential Docker Patterns

```bash
# Read files
docker exec omeka-s-app cat /var/www/html/path/to/file

# List directories  
docker exec omeka-s-app ls -la /var/www/html/themes/

# Copy files into container
docker cp local-file omeka-s-app:/var/www/html/path/

# Fix permissions after copying
docker exec omeka-s-app chown -R www-data:www-data /var/www/html/themes/

# Database access
docker exec -it omeka-s-db mysql -u omeka -p omeka
```

## When to Use This Skill

- **Theme Development**: Custom layouts, SCSS/CSS styling, template overrides
- **Module Development**: PHP modules, event listeners, forms, database entities
- **Configuration**: Site setup, content visibility, database relationships
- **Troubleshooting**: Media issues, permission problems, build failures

## Development Workflow Decision Tree

```
User Request → What type of work?

├─ Theme Customization
│  ├─ Simple CSS change?
│  │  └─ Edit theme/asset/css/style.css directly
│  │     (see references/theme-development.md → Quick CSS Editing)
│  │
│  ├─ Need SCSS/variables?
│  │  └─ Use SCSS build process
│  │     1. Edit theme/asset/sass/*.scss
│  │     2. Run: docker exec omeka-s-app bash -c "cd /var/www/html/themes/THEME && npm run build"
│  │     (see references/theme-development.md → SCSS Build Process)
│  │
│  └─ Template override?
│      └─ Copy from application/view/ to theme/view/
│         (see references/theme-development.md → Template Structure)
│
├─ Module Development
│  ├─ Creating new module?
│  │  └─ Follow module structure pattern
│  │     (see references/module-development.md → Module Structure)
│  │
│  ├─ Adding event listener?
│  │  └─ Register in Module.php attachListeners()
│  │     (see references/module-development.md → Event System)
│  │
│  └─ Database entities?
│      └─ Create Entity, update module.ini
│         (see references/module-development.md → Database Entities)
│
├─ Content Visibility Issues
│  └─ Items not showing?
│      1. Check database relationships
│      2. Verify is_public flags
│      3. Confirm site assignments
│      (see references/database.md → Content Visibility)
│
└─ Configuration/Setup
    └─ See references/troubleshooting.md
```

## Directory Structure

```
/var/www/html/
├── application/          # Core (DON'T MODIFY)
│   ├── view/            # Default templates (COPY to theme to override)
│   └── src/             # PHP source
├── config/
│   ├── database.ini
│   └── local.config.php
├── modules/             # Custom modules here
│   └── MyModule/
│       ├── Module.php
│       ├── module.ini
│       ├── src/
│       └── view/
├── themes/              # Custom themes here
│   └── MyTheme/
│       ├── theme.ini
│       ├── asset/
│       │   ├── css/
│       │   └── sass/
│       └── view/
└── volume/
    └── files/           # Uploaded media
```

## Quick Reference

### Common File Operations

```bash
# Read theme file
docker exec omeka-s-app cat /var/www/html/themes/THEME/theme.ini

# Copy theme into container
docker cp ./my-theme omeka-s-app:/var/www/html/themes/
docker exec omeka-s-app chown -R www-data:www-data /var/www/html/themes/my-theme

# View logs
docker logs omeka-s-app
docker logs omeka-s-db

# Restart services
docker restart omeka-s-app
```

### Common Database Queries

```sql
-- Make all items public
UPDATE resource SET is_public = 1 WHERE resource_type = 'Omeka\\Entity\\Item';

-- Assign all items to site 1
INSERT INTO item_site (item_id, site_id)
SELECT id, 1 FROM item
ON DUPLICATE KEY UPDATE site_id = VALUES(site_id);

-- Check item visibility
SELECT r.id, r.title, r.is_public, COUNT(is_i.item_id) as in_site
FROM resource r
LEFT JOIN item_site is_i ON r.id = is_i.item_id
WHERE r.resource_type = 'Omeka\\Entity\\Item'
GROUP BY r.id;
```

**For complete database operations, see references/database.md**

### Theme Development Quick Start

1. **Create theme directory:**
```bash
mkdir -p my-theme/{asset/{css,js,sass},view/common}
```

2. **Required theme.ini:**
```ini
[info]
name = "My Theme"
version = "1.0"
author = "Your Name"
theme_link = ""
author_link = ""
description = "Custom theme"
```

3. **Override templates:** Copy from `application/view/` to `theme/view/`

**For complete theme guide, see references/theme-development.md**

### Module Development Quick Start

1. **Basic Module.php:**
```php
<?php
namespace MyModule;

use Omeka\Module\AbstractModule;
use Laminas\EventManager\SharedEventManagerInterface;

class Module extends AbstractModule
{
    public function attachListeners(SharedEventManagerInterface $sharedEventManager)
    {
        // Add event listeners here
    }
}
```

2. **Required module.ini:**
```ini
[info]
name = "My Module"
version = "1.0.0"
author = "Your Name"
description = "Module description"
```

**For complete module guide, see references/module-development.md**

## Common Workflows

### Workflow 1: Change Theme Colors

1. Edit `theme/asset/sass/_base.scss` variables
2. Run build: `docker exec omeka-s-app bash -c "cd /var/www/html/themes/THEME && npm run build"`
3. Clear cache if needed
4. Reload page

### Workflow 2: Override Item Display Template

1. Find template: `application/view/omeka/site/item/show.phtml`
2. Copy to theme: `theme/view/omeka/site/item/show.phtml`
3. Edit theme copy
4. Upload to container if needed
5. Test changes

### Workflow 3: Fix Items Not Showing

1. Check database relationships (see references/database.md)
2. Run visibility queries
3. Verify site assignments
4. Check item set linkage
5. Clear cache

### Workflow 4: Add Custom Module

1. Create module structure
2. Write Module.php and module.ini
3. Copy to `/var/www/html/modules/`
4. Fix permissions
5. Install via admin interface
6. Test functionality

## Best Practices

### ✅ DO

- **Always fix permissions** after copying files: `chown -R www-data:www-data`
- **Use SCSS build process** for maintainable styling
- **Copy templates to theme** - never modify `application/` directly
- **Test database queries** on copies before production
- **Version control** your custom themes and modules
- **Document custom code** - future you will thank you

### ❌ DON'T

- **Don't modify core files** in `application/`
- **Don't skip permission fixes** - causes mysterious errors
- **Don't edit compiled CSS** - changes will be overwritten by SCSS build
- **Don't forget site assignments** - items won't show without them
- **Don't skip backups** before database changes

## Troubleshooting

### Items Not Visible
→ See references/database.md (Content Visibility section)

### CSS Changes Not Appearing
- Check if SCSS is being compiled
- Clear browser cache
- Verify file permissions
- Check theme is active

→ See references/theme-development.md (Troubleshooting Build Issues)

### Module Not Loading
- Check module.ini format
- Verify Module.php namespace
- Check file permissions
- View error logs

→ See references/troubleshooting.md

### Media/Thumbnail Issues
- Check file permissions in `volume/files/`
- Verify Imagemagick is installed
- Check thumbnail generation settings

→ See references/database.md (Media & Thumbnails)

## Reference Files

Detailed documentation for each area:

- **references/database.md** - Site configuration, content visibility, database relationships, media system, SQL queries
- **references/theme-development.md** - Complete theme structure, SCSS build process, template overrides, view helpers
- **references/module-development.md** - Module structure, event system, forms, database entities, API integration
- **references/troubleshooting.md** - Common issues, error messages, debugging techniques
- **examples/workflows.md** - Step-by-step examples for common tasks

## Key Concepts

### Content Visibility (Critical!)

Items need **4 conditions** to be visible:
1. Item is public (`is_public = 1`)
2. Item is assigned to site (`item_site` table)
3. Item set is open (`is_open = 1`)
4. Item set is linked to site (`site_item_set` table)

**See references/database.md for complete details**

### Theme Inheritance

Themes inherit from default theme:
- Your theme only contains **overrides**
- Missing templates fall back to `application/view/`
- CSS builds from SCSS in `asset/sass/`

**See references/theme-development.md for template patterns**

### Module Event System

Modules extend Omeka via events:
- `api.search.query` - Modify search
- `view.show.after` - Add to page display
- `form.add_elements` - Add form fields

**See references/module-development.md for event list**

## Getting Started Checklist

For new Omeka S projects:

1. ☐ Verify Docker containers running
2. ☐ Check Omeka version
3. ☐ Create/activate custom theme
4. ☐ Configure site settings
5. ☐ Set up content visibility (database queries)
6. ☐ Test theme customizations
7. ☐ Install required modules
8. ☐ Configure media handling

## Resources

- **Official Docs:** https://omeka.org/s/docs/
- **Developer Docs:** https://omeka.org/s/docs/developer/
- **Docker Hub:** https://hub.docker.com/r/dodeeric/omeka-s
- **Forums:** https://forum.omeka.org/

For detailed guidance on any topic, see the appropriate reference file above.

## Critical Lessons Learned

### Modern MariaDB Commands (2024+)

Newer MariaDB Docker images use different command names:

```bash
# OLD (deprecated)
docker exec omeka-s-db mysqladmin ping
docker exec omeka-s-db mysql -u user -p database

# NEW (current)
docker exec omeka-s-db mariadb-admin ping  
docker exec omeka-s-db mariadb -u user -p database
```

**Always use `mariadb` and `mariadb-admin` commands for compatibility.**

### Block Layouts: Two Types

Omeka S has two distinct types of block layouts that are registered differently:

#### 1. Site Page Blocks (`block_layouts`)
Used for **site pages** (like Time Periods, About, etc.)

```php
// In module.config.php
'block_layouts' => [
    'invokables' => [
        'timePeriodsGrid' => MyModule\Site\BlockLayout\TimePeriodsGrid::class,
    ],
],
```

#### 2. Resource Page Blocks (`resource_page_block_layouts`)  
Used for **item/media/item-set display pages**

```php
// In module.config.php
'resource_page_block_layouts' => [
    'invokables' => [
        'relatedItems' => MyModule\Site\ResourcePageBlockLayout\RelatedItems::class,
    ],
],
```

**Key Difference:** Site page blocks go in regular pages; resource page blocks appear when viewing an item.

### Using the API in Block Layouts

**NEVER use direct database connections in blocks.** Use the API instead:

```php
// ❌ WRONG - Will fail
$connection = $view->getHelperPluginManager()->get('api')->getManager()->getConnection();

// ✅ CORRECT - Use the API
$view->api()->search('items', [
    'site_id' => $site->id(),
    'property' => [[
        'joiner' => 'and',
        'property' => 'dcterms:coverage',
        'type' => 'eq',
        'text' => 'some value',
    ]],
]);
```

**Getting unique property values dynamically:**

```php
// Get property first
$coverageProperty = $view->api()->searchOne('properties', [
    'term' => 'dcterms:coverage',
])->getContent();

// Get all items with that property
$allItems = $view->api()->search('items', [
    'site_id' => $site->id(),
    'has_property' => [$coverageProperty->id()],
])->getContent();

// Extract unique values
$uniqueValues = [];
foreach ($allItems as $item) {
    $values = $item->value('dcterms:coverage', ['all' => true]);
    foreach ($values as $val) {
        $textValue = (string)$val;
        if (!in_array($textValue, $uniqueValues)) {
            $uniqueValues[] = $textValue;
        }
    }
}
```

### Module Version Mismatches

**Symptoms:**
- Blocks render empty
- "Unknown block layout" errors
- Features not working despite module being active

**Diagnosis:**

```bash
# Check file version
docker exec omeka-s-app cat /var/www/html/modules/ModuleName/config/module.ini | grep version

# Check database version
docker exec omeka-s-db mariadb -u omekas -pomekas omekas -e "SELECT id, version FROM module WHERE id = 'ModuleName';"
```

**Solution:** Download the correct version from GitHub releases to match database expectations.

### Custom Block Layout Template

**Full working example of a site page block:**

```php
<?php
namespace MyModule\Site\BlockLayout;

use Omeka\Api\Representation\SiteRepresentation;
use Omeka\Api\Representation\SitePageRepresentation;
use Omeka\Api\Representation\SitePageBlockRepresentation;
use Omeka\Site\BlockLayout\AbstractBlockLayout;
use Laminas\View\Renderer\PhpRenderer;

class MyCustomBlock extends AbstractBlockLayout
{
    public function getLabel()
    {
        return 'My Custom Block'; // @translate
    }

    public function form(
        PhpRenderer $view,
        SiteRepresentation $site,
        SitePageRepresentation $page = null,
        SitePageBlockRepresentation $block = null
    ) {
        // Get saved data
        $data = $block ? $block->data() : [];
        $myValue = $data['myValue'] ?? '';

        // Return HTML form for admin
        return sprintf(
            '<div class="field"><label>My Setting</label><input type="text" name="o:block[__blockIndex__][o:data][myValue]" value="%s"></div>',
            htmlspecialchars($myValue, ENT_QUOTES)
        );
    }

    public function render(PhpRenderer $view, SitePageBlockRepresentation $block)
    {
        $site = $view->currentSite();
        $data = $block->data();
        
        // Query items dynamically
        $items = $view->api()->search('items', [
            'site_id' => $site->id(),
            'limit' => 10,
        ])->getContent();

        // Render template
        return $view->partial('common/block-layout/my-custom-block', [
            'items' => $items,
            'data' => $data,
        ]);
    }
}
```

### Block Data Storage

Block configuration is stored as JSON in `site_page_block.data`:

```sql
-- View block data
SELECT id, layout, data FROM site_page_block WHERE page_id = 10;

-- Update block data (be careful with escaping!)
UPDATE site_page_block 
SET data = '{"key": "value"}' 
WHERE id = 54;
```

**Important:** Data must be valid JSON. Use proper escaping when updating via SQL.

### Querying with Property Filters

```php
// Search items by property value
$response = $view->api()->search('items', [
    'site_id' => $site->id(),
    'property' => [[
        'joiner' => 'and',           // 'and' or 'or'
        'property' => 'dcterms:title', // property term
        'type' => 'eq',               // 'eq', 'neq', 'in', 'nin', 'ex', 'nex'
        'text' => 'search term',
    ]],
]);

$count = $response->getTotalResults();
$items = $response->getContent();
```

### CSS Loading System (CSSEditor Module)

**Omeka S uses the CSSEditor module for custom CSS.** It provides two methods:

1. **Inline CSS** (`css_editor_css`) - Written directly in admin interface
2. **External CSS** (`css_editor_external_css`) - URLs to external CSS files

**Database Storage:**

```sql
-- Check current CSS configuration
SELECT id, value FROM site_setting WHERE id LIKE '%css%';

-- Example output:
css_editor_css                 (empty or contains CSS code)
css_editor_external_css        ["/themes/foundation/asset/css/cdha-custom.css"]
```

**CSS Loading Order (Cascade):**

```
1. Core CSS (iconfonts.css, resource-page-blocks.css)
2. Module CSS (from installed modules)
3. Theme base CSS (default.css, inkwell.css, etc.)
4. Inline CSS from css_editor_css (via /s/SITE/css-editor endpoint)
5. External CSS from css_editor_external_css
6. Additional module CSS
```

**Key Points:**

- **Inline CSS loads BEFORE external CSS** - External files can override inline styles
- Both are added by CSSEditor module, accessible via Admin → Sites → [Site] → Theme
- External CSS URLs can be theme-relative paths or full CDN URLs
- Inline CSS is stored directly in database; external CSS is just a reference

**Common Issue: CSS Conflicts**

If CSS changes don't appear:

```sql
-- Clear conflicting inline CSS
UPDATE site_setting SET value = '' WHERE id = 'css_editor_css';

-- Check what external files are referenced
SELECT value FROM site_setting WHERE id = 'css_editor_external_css';
```

**Best Practice:**

- Use **external CSS files** for maintainable, version-controlled styles
- Use **inline CSS** only for quick tweaks or site-specific overrides
- Reference external files via CSSEditor rather than hardcoding in templates

**Real-World Example:**

```json
css_editor_external_css: ["/themes/foundation/asset/css/cdha-custom.css"]
```

This tells Omeka to load `cdha-custom.css` after the base theme CSS but load it as a separate file (not copied into the inline editor).

### Template Precedence Order (CRITICAL!)

**Omeka S loads templates in this order (highest to lowest priority):**

1. **Theme templates** (`themes/THEME/view/`) - **HIGHEST PRIORITY**
2. **Module templates** (`modules/MODULE/view/`)
3. **Core templates** (`application/view/`) - LOWEST PRIORITY

⚠️ **This means theme templates override EVERYTHING, including module templates.**

**Real-World Example:**

```bash
# You edit this module template:
modules/CdhaBlocks/view/common/resource-page-block-layout/filtered-values-main.phtml

# But Omeka actually uses this theme template (if it exists):
themes/foundation/view/common/resource-page-block-layout/filtered-values-main.phtml

# Result: Your module changes don't appear, causing confusion!
```

**Debugging Template Issues:**

When template changes don't appear:

```bash
# 1. Check if theme has override
find themes/ACTIVE_THEME -name "template-name.phtml"

# 2. If found, edit the THEME template, not the module template

# 3. Use error logging to confirm which file loads:
# Add to top of both templates:
<?php error_log('TEMPLATE: ' . __FILE__); ?>
```

**Best Practice:**

- Always check theme directory first before editing module templates
- Use `grep -r` to find ALL instances of a template name
- Remember: even resource page block templates can be overridden by themes

**Common Symptoms:**

- "I changed the module template but nothing happens"
- "My debug logs in the module template don't appear"
- "The module is being called but using old code"

### Common Pitfalls

1. **Don't hardcode values** - Query database dynamically
2. **Don't use direct SQL** - Use API methods
3. **Don't forget permissions** - `chown -R www-data:www-data` after file changes
4. **Don't skip version checks** - Module version mismatches cause silent failures
5. **Don't forget to restart** - `docker-compose restart omeka-s` after code changes
6. **Don't edit module templates without checking for theme overrides** - Theme templates take precedence

