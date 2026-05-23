---
name: b2c-isml
description: Guide for working with ISML templates in Salesforce B2C Commerce
---

# ISML Skill

This skill guides you through creating and working with ISML (Isomorphic Markup Language) templates in Salesforce B2C Commerce. ISML templates combine HTML with dynamic server-side tags.

## Overview

ISML templates are server-side templates that generate HTML. They use special tags prefixed with `is` and expressions in `${...}` syntax to embed dynamic content.

## File Location

Templates reside in the cartridge's `templates` directory:

```
/my-cartridge
    /cartridge
        /templates
            /default                    # Default locale
                /product
                    detail.isml
                    tile.isml
                /home
                    homepage.isml
                /util
                    modules.isml        # Custom tag definitions
            /fr_FR                      # French-specific templates
                /product
                    detail.isml
```

## Essential Tags

### Conditional Logic

```html
<isif condition="${product.available}">
    <span class="in-stock">In Stock</span>
<iselseif condition="${product.preorderable}">
    <span class="preorder">Pre-order</span>
<iselse>
    <span class="out-of-stock">Out of Stock</span>
</isif>
```

### Loops

```html
<isloop items="${products}" var="product" status="loopstate">
    <div class="product ${loopstate.odd ? 'odd' : 'even'}">
        <span>${loopstate.count}. ${product.name}</span>
        <isif condition="${loopstate.first}">
            <span class="badge">Featured</span>
        </isif>
    </div>
</isloop>
```

**Loop status properties:**
- `count` - Iteration number (1-based)
- `index` - Current index (0-based)
- `first` - Boolean, true on first iteration
- `last` - Boolean, true on last iteration
- `odd` - Boolean, true on odd iterations
- `even` - Boolean, true on even iterations

### Variables

```html
<!-- Set a variable (scope is required) -->
<isset name="productName" value="${product.name}" scope="page"/>

<!-- Use the variable -->
<span>${productName}</span>

<!-- Remove a variable -->
<isremove name="productName" scope="page"/>
```

**Scopes (required):** `page`, `request`, `session`, `pdict`

### Output

```html
<!-- Basic output (HTML encoded by default) -->
<isprint value="${product.name}"/>

<!-- Unencoded output (use carefully) -->
<isprint value="${htmlContent}" encoding="off"/>

<!-- Formatted number -->
<isprint value="${price}" style="CURRENCY"/>

<!-- Formatted date -->
<isprint value="${order.creationDate}" style="DATE_SHORT"/>
```

### Include Templates

```html
<!-- Include local template -->
<isinclude template="product/components/price"/>

<!-- Include with URL (remote include) -->
<isinclude url="${URLUtils.url('Product-GetPrice', 'pid', product.ID)}"/>
```

### Decorator Pattern

**Base decorator (layouts/pagelayout.isml):**
```html
<!DOCTYPE html>
<html>
<head>
    <title>${pdict.pageTitle}</title>
</head>
<body>
    <header>
        <isinclude template="components/header"/>
    </header>
    <main>
        <isreplace/>  <!-- Content inserted here -->
    </main>
    <footer>
        <isinclude template="components/footer"/>
    </footer>
</body>
</html>
```

**Page using decorator:**
```html
<isdecorate template="layouts/pagelayout">
    <isslot id="home-banner" context="global"/>
    <div class="homepage-content">
        <h1>${pdict.welcomeMessage}</h1>
    </div>
</isdecorate>
```

## Expressions

Expressions use `${...}` syntax to embed dynamic values:

```html
<!-- Property access -->
${product.name}
${product.price.sales.value}

<!-- Method calls -->
${product.getAvailabilityModel().isInStock()}

<!-- Built-in objects -->
${pdict.myVariable}           <!-- Controller data -->
${session.customer.firstName} <!-- Session data -->
${request.httpParameterMap.pid.stringValue}

<!-- Operators -->
${price > 100 ? 'expensive' : 'affordable'}
${firstName + ' ' + lastName}
${quantity * unitPrice}
```

## Built-in Utilities

### URLUtils

```html
<!-- Controller URL -->
<a href="${URLUtils.url('Product-Show', 'pid', product.ID)}">View</a>

<!-- HTTPS URL -->
<a href="${URLUtils.https('Account-Show')}">My Account</a>

<!-- Static resource -->
<img src="${URLUtils.staticURL('/images/logo.png')}" alt="Logo"/>

<!-- Absolute URL -->
<a href="${URLUtils.abs('Home-Show')}">Home</a>
```

### Resource (Localization)

```html
<!-- Get localized string -->
${Resource.msg('button.addtocart', 'product', null)}

<!-- With parameters -->
${Resource.msgf('cart.items', 'cart', null, cartCount)}
```

### StringUtils

```html
<!-- Truncate text -->
${StringUtils.truncate(description, 100, '...')}

<!-- Format number -->
${StringUtils.formatNumber(quantity, '###,###')}
```

## Custom Modules

Define reusable custom tags in `util/modules.isml`:

```html
<!-- Definition in util/modules.isml -->
<ismodule template="components/productcard"
          name="productcard"
          attribute="product"
          attribute="showPrice"
          attribute="showRating"/>

<!-- Usage in any template -->
<isinclude template="util/modules"/>
<isproductcard product="${product}" showPrice="${true}" showRating="${true}"/>
```

**Component template (components/productcard.isml):**
```html
<div class="product-card">
    <img src="${product.image.url}" alt="${product.name}"/>
    <h3>${product.name}</h3>
    <isif condition="${pdict.showPrice}">
        <span class="price">${product.price.sales.formatted}</span>
    </isif>
    <isif condition="${pdict.showRating && product.rating}">
        <span class="rating">${product.rating} stars</span>
    </isif>
</div>
```

## Caching

```html
<!-- Cache for 24 hours -->
<iscache type="relative" hour="24"/>

<!-- Daily cache (expires at midnight) -->
<iscache type="daily" hour="0" minute="0"/>

<!-- Vary cache by parameter -->
<iscache type="relative" hour="1" varyby="price_promotion"/>
```

**Place `<iscache>` at the beginning of the template.**

## Content Type

```html
<!-- Set content type (must be first in template) -->
<iscontent type="text/html" charset="UTF-8"/>

<!-- For JSON responses -->
<iscontent type="application/json" charset="UTF-8"/>

<!-- For XML -->
<iscontent type="application/xml" charset="UTF-8"/>
```

## Embedded Scripts

```html
<isscript>
    var ProductMgr = require('dw/catalog/ProductMgr');
    var product = ProductMgr.getProduct(pdict.pid);
    var price = product.priceModel.price;
</isscript>

<span>${price.toFormattedString()}</span>
```

**Best Practice:** Keep `<isscript>` blocks minimal. Move complex logic to controllers or helper scripts.

## Comments

```html
<!-- HTML comment (visible in source) -->

<iscomment>
    ISML comment - stripped from output.
    Use for documentation and hiding sensitive info.
</iscomment>
```

## Tag Location Constraints

Not all ISML tags can be used anywhere. Important constraints:

| Tag | Allowed Location |
|-----|------------------|
| `<iscontent>` | Must be before DOCTYPE declaration |
| `<isredirect>` | Must be before DOCTYPE declaration |
| `<isprint>` | Only in `<body>` |
| `<isbreak>` | Only in `<body>`, inside `<isloop>` |
| `<iscontinue>` | Only in `<body>`, inside `<isloop>` |
| `<isnext>` | Inside `<isloop>` |
| `<isreplace>` | Must be within `<isdecorate>` tags |
| `<isactivedatahead>` | Only in `<head>` |

Tags that can be used **anywhere**: `<isif>`, `<isloop>`, `<isinclude>`, `<isset>`, `<isremove>`, `<iscache>`, `<iscomment>`, `<ismodule>`, `<iscookie>`, `<isstatus>`.

## Best Practices

1. **Use `<iscomment>`** instead of HTML comments for sensitive info
2. **Place `<iscontent>` first** in templates that need it
3. **Define modules** in `util/modules.isml` for consistency
4. **Keep templates simple** - move logic to controllers/helpers
5. **Use decorators** for consistent page layouts
6. **Enable caching** on cacheable pages with `<iscache>`
7. **Encode output** - default encoding prevents XSS

## Detailed Reference

For comprehensive tag documentation:
- [Tags Reference](references/TAGS.md) - All ISML tags with examples
- [Expressions Reference](references/EXPRESSIONS.md) - Expression syntax and built-in functions
