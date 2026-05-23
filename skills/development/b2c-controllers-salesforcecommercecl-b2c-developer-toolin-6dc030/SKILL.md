---
name: b2c-controllers
description: Guide for creating storefront controllers in Salesforce B2C Commerce (SFRA and classic patterns)
---

# Controllers Skill

This skill guides you through creating storefront controllers for Salesforce B2C Commerce. Controllers handle HTTP requests and render responses for the storefront.

## Overview

Controllers are JavaScript modules that handle storefront requests. A controller URL has this structure:

```
https://{domain}/on/demandware.store/Sites-{SiteName}-Site/{locale}/{ControllerName}-{FunctionName}
```

**Example:** `https://example.com/on/demandware.store/Sites-RefArch-Site/en_US/Home-Show`

## Two Controller Patterns

B2C Commerce supports two controller patterns:

| Pattern | When to Use | Module Style |
|---------|-------------|--------------|
| **SFRA** | Storefront Reference Architecture sites | `server` module with middleware |
| **Classic** | Non-SFRA sites, simple APIs | Direct exports with `.public = true` |

**SFRA is recommended** for most storefront development. Classic controllers are useful for simple endpoints or non-SFRA projects.

## File Location

Controllers reside in the cartridge's `controllers` directory:

```
/my-cartridge
    /cartridge
        /controllers
            Home.js           # URL: Home-{function}
            Product.js        # URL: Product-{function}
            Cart.js           # URL: Cart-{function}
```

**Naming:** Controller filename becomes the URL prefix. `Home.js` handles `Home-*` requests.

## SFRA Controllers (Recommended)

SFRA controllers use the `server` module for routing and middleware:

```javascript
'use strict';

var server = require('server');

// Handle GET request
server.get('Show', function (req, res, next) {
    res.render('home/homepage');
    next();
});

// Handle POST request
server.post('Subscribe', function (req, res, next) {
    var email = req.form.email;
    // Process subscription...
    res.json({ success: true });
    next();
});

module.exports = server.exports();
```

### Request Object (req)

```javascript
req.querystring          // Query parameters: ?q=shoes -> req.querystring.q
req.form                 // Form POST data: req.form.email
req.httpMethod           // HTTP method: 'GET', 'POST', etc.
req.httpHeaders          // Request headers
req.currentCustomer      // Current customer object
req.locale               // Current locale
req.session              // Session object
```

### Response Object (res)

```javascript
res.render('template', model)   // Render ISML template with data
res.json(object)                // Return JSON response
res.redirect(url)               // Redirect to URL
res.setViewData(data)           // Add data to view model
res.getViewData()               // Get current view model
res.setStatusCode(code)         // Set HTTP status code
```

### Middleware

Apply middleware to routes for cross-cutting concerns:

```javascript
var server = require('server');
var cache = require('*/cartridge/scripts/middleware/cache');
var consentTracking = require('*/cartridge/scripts/middleware/consentTracking');
var csrfProtection = require('*/cartridge/scripts/middleware/csrf');

// Apply caching
server.get('Show', cache.applyDefaultCache, function (req, res, next) {
    res.render('home/homepage');
    next();
});

// Require HTTPS
server.post('Login', server.middleware.https, function (req, res, next) {
    // Handle login...
    next();
});

// CSRF protection for forms
server.post('Submit', csrfProtection.validateAjaxRequest, function (req, res, next) {
    // Handle form submission...
    next();
});
```

### Common Middleware

| Middleware | Purpose |
|------------|---------|
| `server.middleware.https` | Require HTTPS connection |
| `cache.applyDefaultCache` | Apply default page caching |
| `csrfProtection.validateAjaxRequest` | Validate CSRF token |
| `consentTracking.consent` | Check tracking consent |
| `userLoggedIn.validateLoggedIn` | Require authenticated user |

### Route Events

Execute code at specific points in the request lifecycle:

```javascript
server.post('Submit', function (req, res, next) {
    var form = req.form;
    res.setViewData({ email: form.email });
    next();
}, function (req, res, next) {
    // Additional middleware
    next();
});

// Execute after all middleware, before render
this.on('route:BeforeComplete', function (req, res) {
    var viewData = res.getViewData();
    // Modify view data if needed
});
```

### Extending Controllers

Extend existing controllers to add or modify functionality:

```javascript
'use strict';

var server = require('server');
var page = module.superModule;  // Get parent controller

server.extend(page);

// Add new route
server.get('NewRoute', function (req, res, next) {
    res.render('newtemplate');
    next();
});

// Override existing route
server.replace('Show', function (req, res, next) {
    // Custom implementation
    res.render('custom/homepage');
    next();
});

// Prepend to existing route
server.prepend('Show', function (req, res, next) {
    // Runs before original handler
    next();
});

// Append to existing route
server.append('Show', function (req, res, next) {
    // Runs after original handler
    var viewData = res.getViewData();
    viewData.customData = 'value';
    res.setViewData(viewData);
    next();
});

module.exports = server.exports();
```

## Classic Controllers (Non-SFRA)

For non-SFRA sites or simple endpoints, use direct exports:

```javascript
'use strict';

var ISML = require('dw/template/ISML');

exports.Show = function () {
    var params = request.httpParameterMap;
    var productId = params.pid.stringValue;

    ISML.renderTemplate('product/detail', {
        productId: productId
    });
};
exports.Show.public = true;  // Required: marks function as accessible

exports.GetData = function () {
    var result = { status: 'ok', data: [] };

    response.setContentType('application/json');
    response.writer.print(JSON.stringify(result));
};
exports.GetData.public = true;
```

**Key difference:** Classic controllers use `exports.FunctionName.public = true` instead of the `server` module.

## Module Imports

Import B2C Commerce APIs using `require()`:

```javascript
// B2C Commerce APIs
var ProductMgr = require('dw/catalog/ProductMgr');
var Transaction = require('dw/system/Transaction');
var Logger = require('dw/system/Logger');
var URLUtils = require('dw/web/URLUtils');
var Resource = require('dw/web/Resource');

// Cartridge modules (use */ for cartridge path resolution)
var collections = require('*/cartridge/scripts/util/collections');
var productHelper = require('*/cartridge/scripts/helpers/productHelpers');
```

**Best Practice:** Only require modules when needed, not all at the top of the file.

## Error Handling

Wrap operations in try-catch blocks:

```javascript
server.get('Show', function (req, res, next) {
    try {
        var product = ProductMgr.getProduct(req.querystring.pid);
        if (!product) {
            res.setStatusCode(404);
            res.render('error/notfound');
            return next();
        }
        res.render('product/detail', { product: product });
    } catch (e) {
        Logger.error('Product error: ' + e.message);
        res.setStatusCode(500);
        res.render('error/general');
    }
    next();
});
```

## Generating URLs

Use URLUtils to generate locale-aware URLs:

```javascript
var URLUtils = require('dw/web/URLUtils');

// Controller URL
var productUrl = URLUtils.url('Product-Show', 'pid', 'ABC123');
// Result: /on/demandware.store/Sites-RefArch-Site/en_US/Product-Show?pid=ABC123

// HTTPS URL
var loginUrl = URLUtils.https('Login-Show');

// Static resource URL
var imageUrl = URLUtils.staticURL('/images/logo.png');
```

## Best Practices

1. **Always call `next()`** in SFRA middleware chain
2. **Use ViewModels** to prepare data for templates
3. **Keep controllers thin** - move business logic to scripts/helpers
4. **Use hooks** for functionality that works for both storefront and OCAPI
5. **Handle errors gracefully** - never expose stack traces
6. **Use `*/cartridge/...`** for portable module paths

## Detailed Reference

For comprehensive patterns and examples:
- [SFRA Patterns](references/SFRA-PATTERNS.md) - Full SFRA patterns with middleware
- [Classic Patterns](references/CLASSIC-PATTERNS.md) - Non-SFRA controller patterns
