---
name: b2c-page-designer
description: Create Page Designer pages and components in B2C Commerce. Use when building visual merchandising tools, content slots, or experience API integrations. Covers page types, component types, regions, and attribute definitions.
---

# Page Designer Skill

This skill guides you through creating custom Page Designer page types and component types for Salesforce B2C Commerce.

## Overview

Page Designer allows merchants to create and manage content pages through a visual editor. Developers create:

1. **Page Types** - Define page structures with regions
2. **Component Types** - Reusable content blocks with configurable attributes

## File Structure

Page Designer files are in the cartridge's `experience` directory:

```
/my-cartridge
    /cartridge
        /experience
            /pages
                homepage.json           # Page type meta definition
                homepage.js             # Page type script
            /components
                banner.json             # Component type meta definition
                banner.js               # Component type script
        /templates
            /default
                /experience
                    /pages
                        homepage.isml   # Page template
                    /components
                        banner.isml     # Component template
```

**Naming:** The `.json` and `.js` files must have matching names.

## Page Types

### Meta Definition (pages/homepage.json)

```json
{
    "name": "Home Page",
    "description": "Landing page with hero and content regions",
    "region_definitions": [
        {
            "id": "hero",
            "name": "Hero Section",
            "max_components": 1
        },
        {
            "id": "content",
            "name": "Main Content"
        },
        {
            "id": "footer",
            "name": "Footer Section",
            "component_type_exclusions": [
                { "type_id": "video" }
            ]
        }
    ]
}
```

### Page Script (pages/homepage.js)

```javascript
'use strict';

var Template = require('dw/util/Template');
var HashMap = require('dw/util/HashMap');

module.exports.render = function (context) {
    var model = new HashMap();
    var page = context.page;

    model.put('page', page);

    return new Template('experience/pages/homepage').render(model).text;
};
```

### Page Template (templates/experience/pages/homepage.isml)

```html
<isdecorate template="common/layout/page">
    <isscript>
        var PageRenderHelper = require('*/cartridge/experience/utilities/PageRenderHelper');
    </isscript>

    <div class="homepage">
        <div class="hero-region">
            <isprint value="${PageRenderHelper.renderRegion(pdict.page.getRegion('hero'))}" encoding="off"/>
        </div>

        <div class="content-region">
            <isprint value="${PageRenderHelper.renderRegion(pdict.page.getRegion('content'))}" encoding="off"/>
        </div>

        <div class="footer-region">
            <isprint value="${PageRenderHelper.renderRegion(pdict.page.getRegion('footer'))}" encoding="off"/>
        </div>
    </div>
</isdecorate>
```

## Component Types

### Meta Definition (components/banner.json)

```json
{
    "name": "Banner",
    "description": "Promotional banner with image and CTA",
    "group": "content",
    "attribute_definition_groups": [
        {
            "id": "image",
            "name": "Image Settings",
            "attribute_definitions": [
                {
                    "id": "image",
                    "name": "Banner Image",
                    "type": "image",
                    "required": true
                },
                {
                    "id": "alt",
                    "name": "Alt Text",
                    "type": "string",
                    "required": true
                }
            ]
        },
        {
            "id": "content",
            "name": "Content",
            "attribute_definitions": [
                {
                    "id": "headline",
                    "name": "Headline",
                    "type": "string",
                    "required": true
                },
                {
                    "id": "body",
                    "name": "Body Text",
                    "type": "markup"
                },
                {
                    "id": "ctaUrl",
                    "name": "CTA Link",
                    "type": "url"
                },
                {
                    "id": "ctaText",
                    "name": "CTA Button Text",
                    "type": "string"
                }
            ]
        },
        {
            "id": "layout",
            "name": "Layout Options",
            "attribute_definitions": [
                {
                    "id": "alignment",
                    "name": "Text Alignment",
                    "type": "enum",
                    "values": ["left", "center", "right"],
                    "default_value": "center"
                },
                {
                    "id": "fullWidth",
                    "name": "Full Width",
                    "type": "boolean",
                    "default_value": false
                }
            ]
        }
    ]
}
```

### Component Script (components/banner.js)

```javascript
'use strict';

var Template = require('dw/util/Template');
var HashMap = require('dw/util/HashMap');
var URLUtils = require('dw/web/URLUtils');

module.exports.render = function (context) {
    var model = new HashMap();
    var content = context.content;

    // Access merchant-configured attributes
    model.put('image', content.image);        // Image object
    model.put('alt', content.alt);            // String
    model.put('headline', content.headline);  // String
    model.put('body', content.body);          // Markup string
    model.put('ctaUrl', content.ctaUrl);      // URL object
    model.put('ctaText', content.ctaText);    // String
    model.put('alignment', content.alignment || 'center');
    model.put('fullWidth', content.fullWidth);

    return new Template('experience/components/banner').render(model).text;
};
```

### Component Template (templates/experience/components/banner.isml)

```html
<div class="banner ${pdict.fullWidth ? 'banner--full-width' : ''}"
     style="text-align: ${pdict.alignment}">
    <isif condition="${pdict.image}">
        <img src="${pdict.image.file.absURL}"
             alt="${pdict.alt}"
             class="banner__image"/>
    </isif>

    <div class="banner__content">
        <h2 class="banner__headline">${pdict.headline}</h2>

        <isif condition="${pdict.body}">
            <div class="banner__body">
                <isprint value="${pdict.body}" encoding="off"/>
            </div>
        </isif>

        <isif condition="${pdict.ctaUrl && pdict.ctaText}">
            <a href="${pdict.ctaUrl}" class="banner__cta btn btn-primary">
                ${pdict.ctaText}
            </a>
        </isif>
    </div>
</div>
```

## Attribute Types

| Type | Description | Returns |
|------|-------------|---------|
| `string` | Text input | String |
| `text` | Multi-line text | String |
| `markup` | Rich text editor | Markup string (use `encoding="off"`) |
| `boolean` | Checkbox | Boolean |
| `integer` | Number input | Integer |
| `enum` | Single select dropdown | String |
| `image` | Image picker | Image object with `file.absURL` |
| `file` | File picker | File object |
| `url` | URL picker | URL string |
| `category` | Category selector | Category object |
| `product` | Product selector | Product object |
| `page` | Page selector | Page object |
| `custom` | JSON object | Object |

## Region Definitions

```json
{
    "region_definitions": [
        {
            "id": "main",
            "name": "Main Content",
            "max_components": 10,
            "component_type_exclusions": [
                { "type_id": "heavy-component" }
            ],
            "component_type_inclusions": [
                { "type_id": "text-block" },
                { "type_id": "image-block" }
            ]
        }
    ]
}
```

| Property | Description |
|----------|-------------|
| `id` | Unique region identifier |
| `name` | Display name in editor |
| `max_components` | Max number of components (optional) |
| `component_type_exclusions` | Components NOT allowed |
| `component_type_inclusions` | Only these components allowed |

## Rendering Pages

### In Controllers

```javascript
var PageMgr = require('dw/experience/PageMgr');

server.get('Show', function (req, res, next) {
    var page = PageMgr.getPage(req.querystring.cid);

    if (page && page.isVisible()) {
        res.page(page.ID);
    } else {
        res.setStatusCode(404);
        res.render('error/notfound');
    }
    next();
});
```

### In ISML

```html
<isscript>
    var PageMgr = require('dw/experience/PageMgr');
    var page = PageMgr.getPage('homepage-id');
</isscript>

<isif condition="${page && page.isVisible()}">
    <isprint value="${PageMgr.renderPage(page.ID)}" encoding="off"/>
</isif>
```

## Component Groups

Organize components in the editor sidebar:

```json
{
    "name": "Product Card",
    "group": "products"
}
```

Common groups: `content`, `products`, `navigation`, `layout`, `media`

## Best Practices

1. **Use `dw.util.Template`** for rendering (NOT `dw.template.ISML`)
2. **Keep components self-contained** - avoid cross-component dependencies
3. **Provide default values** for optional attributes
4. **Group related attributes** in `attribute_definition_groups`
5. **Use meaningful IDs** - they're used programmatically
6. **Don't change type IDs** after merchants create content

## Detailed Reference

For comprehensive attribute documentation:
- [Meta Definitions Reference](references/META-DEFINITIONS.md) - Full JSON schema
- [Attribute Types Reference](references/ATTRIBUTE-TYPES.md) - All attribute types with examples
