---
name: b2c-custom-caches
description: Implement custom caching with CacheMgr in B2C Commerce. Use when adding application-level caching, cache invalidation, or optimizing performance with custom cache regions. Covers cache definition JSON, CacheMgr API, and cache entry lifecycle.
---

# B2C Custom Caches

Custom caches improve code performance by storing data that is expensive to calculate, takes a long time to retrieve, or is accessed frequently. Caches are defined in JSON files within cartridges and accessed via the Script API.

## When to Use Custom Caches

| Use Case | Example |
|----------|---------|
| Expensive calculations | Check if any variation product is on sale for base product display |
| External system responses | Cache in-store availability or prices from external APIs |
| Configuration settings | Store configuration data from JSON files or external sources |
| Frequently accessed data | Product attributes, category data, site preferences |

## Limitations

| Constraint | Value |
|------------|-------|
| Total memory per app server | ~20 MB for all custom caches |
| Max caches per code version | 100 |
| Max entry size | 128 KB |
| Supported value types | Primitives, arrays, plain objects, `null` (not `undefined`) |
| Cross-server sync | None (caches are per-application-server) |

## Defining a Custom Cache

### File Structure

```
my_cartridge/
├── package.json       # References caches.json
└── caches.json        # Cache definitions
```

### package.json

Add a `caches` entry pointing to the cache definition file:

```json
{
  "name": "my_cartridge",
  "caches": "./caches.json"
}
```

### caches.json

Define caches with unique IDs and optional expiration:

```json
{
  "caches": [
    {
      "id": "ProductAttributeCache"
    },
    {
      "id": "ExternalPriceCache",
      "expireAfterSeconds": 300
    },
    {
      "id": "SiteConfigCache",
      "expireAfterSeconds": 60
    }
  ]
}
```

| Property | Required | Description |
|----------|----------|-------------|
| `id` | Yes | Unique ID across all cartridges in code version |
| `expireAfterSeconds` | No | Maximum seconds an entry is retained |

## Using Custom Caches

### Script API Classes

| Class | Description |
|-------|-------------|
| `dw.system.CacheMgr` | Entry point for accessing defined caches |
| `dw.system.Cache` | Cache instance for storing and retrieving entries |

### Basic Usage

```javascript
var CacheMgr = require('dw/system/CacheMgr');

// Get a defined cache
var cache = CacheMgr.getCache('ProductAttributeCache');

// Get value (returns undefined if not found)
var value = cache.get('myKey');

// Store value directly
cache.put('myKey', { data: 'value' });

// Remove entry
cache.invalidate('myKey');
```

### Recommended Pattern: get with Loader

Use `get(key, loader)` to automatically populate the cache on miss:

```javascript
var CacheMgr = require('dw/system/CacheMgr');
var Site = require('dw/system/Site');

var cache = CacheMgr.getCache('SiteConfigCache');

// Loader function called only on cache miss
var config = cache.get(Site.current.ID + '_config', function() {
    // Expensive operation - only runs if not cached
    return loadConfigurationFromFile(Site.current);
});
```

### Scoped Cache Keys

Include scope identifiers in keys to separate entries by context:

```javascript
var CacheMgr = require('dw/system/CacheMgr');
var Site = require('dw/system/Site');

var cache = CacheMgr.getCache('ProductCache');

// Site-scoped key
var siteKey = Site.current.ID + '_' + productID;
var productData = cache.get(siteKey, loadProductData);

// Catalog-scoped key
var catalogKey = 'catalog_' + catalogID + '_' + productID;
var catalogData = cache.get(catalogKey, loadCatalogData);

// Locale-scoped key
var localeKey = request.locale + '_' + contentID;
var content = cache.get(localeKey, loadLocalizedContent);
```

## Cache Methods

| Method | Description |
|--------|-------------|
| `get(key)` | Returns cached value or `undefined` |
| `get(key, loader)` | Returns cached value or calls loader, stores result |
| `put(key, value)` | Stores value directly (overwrites existing) |
| `invalidate(key)` | Removes entry for key |

## Best Practices

### Do

- Use `get(key, loader)` pattern for automatic population
- Include scope (site, catalog, locale) in cache keys
- Set appropriate `expireAfterSeconds` for time-sensitive data
- Handle cache misses gracefully (data may be evicted anytime)
- Use descriptive cache IDs

### Don't

- Include personal user data in cache keys (keys may appear in logs)
- Store Script API objects (only primitives and plain objects)
- Rely on cache entries existing (no persistence guarantee)
- Expect cross-server cache synchronization
- Store `undefined` values (use `null` instead)

## Cache Invalidation

Caches are automatically cleared when:
- Any file in the active code version changes
- A new code version is activated
- Data replication completes
- Code replication completes

Manual invalidation only affects the current application server:

```javascript
var cache = CacheMgr.getCache('MyCache');

// Invalidate single entry (current app server only)
cache.invalidate('myKey');

// Storing undefined has same effect as invalidate
cache.put('myKey', undefined);
```

## Common Patterns

### Caching External API Responses

```javascript
var CacheMgr = require('dw/system/CacheMgr');
var LocalServiceRegistry = require('dw/svc/LocalServiceRegistry');

var priceCache = CacheMgr.getCache('ExternalPriceCache');

function getExternalPrice(productID) {
    return priceCache.get('price_' + productID, function() {
        var service = LocalServiceRegistry.createService('PriceService', {
            createRequest: function(svc, args) {
                svc.setRequestMethod('GET');
                svc.addParam('productId', args.productID);
                return null;
            },
            parseResponse: function(svc, response) {
                return JSON.parse(response.text);
            }
        });

        var result = service.call({ productID: productID });
        return result.ok ? result.object : null;
    });
}
```

### Caching Expensive Calculations

```javascript
var CacheMgr = require('dw/system/CacheMgr');

var saleCache = CacheMgr.getCache('ProductSaleCache');

function isProductOnSale(masterProduct) {
    return saleCache.get('sale_' + masterProduct.ID, function() {
        var variants = masterProduct.variants.iterator();
        while (variants.hasNext()) {
            var variant = variants.next();
            if (isInPromotion(variant)) {
                return true;
            }
        }
        return false;
    });
}
```

### Configuration Cache with Site Scope

```javascript
var CacheMgr = require('dw/system/CacheMgr');
var Site = require('dw/system/Site');
var File = require('dw/io/File');
var FileReader = require('dw/io/FileReader');

var configCache = CacheMgr.getCache('SiteConfigCache');

function getSiteConfig() {
    var siteID = Site.current.ID;

    return configCache.get(siteID + '_config', function() {
        var configFile = new File(File.IMPEX + '/src/config/' + siteID + '.json');
        if (!configFile.exists()) {
            return null;
        }

        var reader = new FileReader(configFile);
        var content = reader.getString();
        reader.close();

        return JSON.parse(content);
    });
}
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Cache not found exception | Cache ID not defined in any caches.json | Add cache definition to caches.json |
| Duplicate cache ID error | Same ID used in multiple cartridges | Use unique IDs across all cartridges |
| Entry not stored | Value exceeds 128 KB limit | Reduce data size or cache subsets |
| Entry not stored | Value contains Script API objects | Use only primitives and plain objects |
| Unexpected cache misses | Different app server or cache cleared | Always handle misses gracefully |

Check the custom error log and custom warn log for cache-related messages.
