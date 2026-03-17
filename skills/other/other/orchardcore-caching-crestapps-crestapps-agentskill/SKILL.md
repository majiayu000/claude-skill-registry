---
name: orchardcore-caching
description: Skill for configuring and managing caching in Orchard Core. Covers response compression, dynamic cache, shape caching, cache tag helpers, ISignal-based invalidation, distributed cache with Redis, cache profiles, and CacheContext dependencies.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Caching - Prompt Templates

## Configure and Manage Caching

You are an Orchard Core expert. Generate code and configuration for caching strategies including response compression, dynamic cache, shape-level caching, cache invalidation, and distributed cache.

### Guidelines

- Enable `OrchardCore.ResponseCompression` to compress HTTP responses with gzip or Brotli.
- Enable `OrchardCore.DynamicCache` for shape-level output caching with dependency tracking.
- Use `ISignal` to invalidate cached entries when underlying data changes.
- Use `IDistributedCache` for storing serialized data across multiple servers.
- Use `IDynamicCacheService` to programmatically manage dynamic cache entries.
- Use `CacheContext` to declare cache dependencies, vary-by keys, and expiration policies.
- Cache tag helpers in Razor and `{% cache %}` blocks in Liquid provide declarative shape caching.
- All recipe JSON must be wrapped in `{ "steps": [...] }`.
- All C# classes must use the `sealed` modifier.

### Enabling Caching Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.ResponseCompression",
        "OrchardCore.DynamicCache"
      ],
      "disable": []
    }
  ]
}
```

### Response Compression

Enable `OrchardCore.ResponseCompression` to add gzip and Brotli compression to HTTP responses. This module registers `ResponseCompressionMiddleware` and does not require additional code. Configure compression providers in `Startup` if custom settings are needed:

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.Configure<BrotliCompressionProviderOptions>(options =>
        {
            options.Level = System.IO.Compression.CompressionLevel.Fastest;
        });

        services.Configure<GzipCompressionProviderOptions>(options =>
        {
            options.Level = System.IO.Compression.CompressionLevel.SmallestSize;
        });
    }
}
```

### Dynamic Cache (Shape-Level Caching)

`OrchardCore.DynamicCache` caches the rendered HTML output of shapes. Each cached shape tracks dependencies so it can be evicted when related content changes. Dependencies use the format `contentitemid:{id}` or custom signal names.

### Shape Cache Tag Helper (Razor)

Use the `<cache>` tag helper in Razor views to cache rendered shape output with vary-by attributes:

```html
<cache expires-after="TimeSpan.FromMinutes(10)"
       vary-by-route="area,controller,action"
       vary-by-query="page">
    @await DisplayAsync(Model.Content)
</cache>
```

Supported vary-by attributes:
- `vary-by-route` - Vary by route values.
- `vary-by-query` - Vary by query string parameters.
- `vary-by-user` - Vary by authenticated user.
- `vary-by-cookie` - Vary by cookie values.
- `vary-by-header` - Vary by request headers.
- `vary-by` - Vary by a custom string key.
- `expires-after` - Absolute expiration as `TimeSpan`.
- `expires-sliding` - Sliding expiration as `TimeSpan`.
- `expires-on` - Absolute expiration as `DateTimeOffset`.

### Liquid Cache Block

In Liquid templates, use the `{% cache %}` tag for shape-level caching:

```liquid
{% cache "my-cache-key", after: "00:10:00", vary_by: Request.QueryString["page"] %}
    {{ Model.Content | shape_render }}
{% endcache %}
```

### Using CacheContext for Shape Dependencies

Shapes can declare caching behavior through `CacheContext`. In a shape display driver, configure cache parameters:

```csharp
using OrchardCore.DisplayManagement.Handlers;
using OrchardCore.DisplayManagement.Views;
using OrchardCore.Environment.Cache;

public sealed class RecentPostsDisplayDriver : DisplayDriver<RecentPostsViewModel>
{
    public override IDisplayResult Display(RecentPostsViewModel model, BuildDisplayContext context)
    {
        return View("RecentPosts", model)
            .Location("Detail", "Content:5")
            .Cache("recentposts", cache => cache
                .AddDependency("contenttype:BlogPost")
                .AddContext("user")
                .WithExpiryAfter(TimeSpan.FromMinutes(15))
            );
    }
}
```

Common `CacheContext` methods:
- `AddDependency(string)` - Evict when the named dependency signals.
- `AddContext(string)` - Vary by the named context (e.g., `"user"`, `"route"`).
- `WithExpiryAfter(TimeSpan)` - Set absolute expiration.
- `WithExpirySliding(TimeSpan)` - Set sliding expiration.

### Cache Invalidation with ISignal

`ISignal` triggers cache eviction by signaling a named dependency. Any dynamic cache entry tracking that dependency is purged:

```csharp
using OrchardCore.Environment.Cache;

public sealed class ProductService
{
    private readonly ISignal _signal;

    public ProductService(ISignal signal)
    {
        _signal = signal;
    }

    public async Task InvalidateProductCacheAsync()
    {
        await _signal.SignalTokenAsync("productcatalog");
    }
}
```

Shapes or code that depend on `"productcatalog"` are evicted when the signal fires. Content item changes automatically signal `contentitemid:{ContentItemId}` dependencies.

### Using IDistributedCache

`IDistributedCache` stores serialized data in a shared cache backend (memory, SQL Server, or Redis). Inject and use it directly:

```csharp
using Microsoft.Extensions.Caching.Distributed;

public sealed class CatalogCacheService
{
    private readonly IDistributedCache _distributedCache;

    public CatalogCacheService(IDistributedCache distributedCache)
    {
        _distributedCache = distributedCache;
    }

    public async Task<string?> GetCachedCatalogAsync(string key)
    {
        return await _distributedCache.GetStringAsync(key);
    }

    public async Task SetCachedCatalogAsync(string key, string value)
    {
        var options = new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(30),
            SlidingExpiration = TimeSpan.FromMinutes(10),
        };

        await _distributedCache.SetStringAsync(key, value, options);
    }

    public async Task RemoveCachedCatalogAsync(string key)
    {
        await _distributedCache.RemoveAsync(key);
    }
}
```

### Using IDynamicCacheService

`IDynamicCacheService` provides programmatic access to the dynamic cache for storing and evicting pre-rendered HTML:

```csharp
using OrchardCore.DynamicCache;

public sealed class WidgetCacheManager
{
    private readonly IDynamicCacheService _dynamicCacheService;
    private readonly ISignal _signal;

    public WidgetCacheManager(
        IDynamicCacheService dynamicCacheService,
        ISignal signal)
    {
        _dynamicCacheService = dynamicCacheService;
        _signal = signal;
    }

    public async Task<string?> GetCachedWidgetAsync(CacheContext context)
    {
        return await _dynamicCacheService.GetCachedValueAsync(context);
    }

    public async Task SetCachedWidgetAsync(CacheContext context, string htmlContent)
    {
        await _dynamicCacheService.SetCachedValueAsync(context, htmlContent);
    }

    public async Task InvalidateWidgetAsync()
    {
        await _signal.SignalTokenAsync("widget-sidebar");
    }
}
```

### Redis Distributed Cache Configuration

To use Redis as the distributed cache backend, add the `Microsoft.Extensions.Caching.StackExchangeRedis` package to the web project and configure it:

```csharp
public sealed class Startup : StartupBase
{
    private readonly IConfiguration _configuration;

    public Startup(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddStackExchangeRedisCache(options =>
        {
            options.Configuration = _configuration["Redis:ConnectionString"];
            options.InstanceName = "orchardcore-";
        });
    }
}
```

Corresponding `appsettings.json`:

```json
{
  "Redis": {
    "ConnectionString": "localhost:6379,abortConnect=false,connectTimeout=5000"
  }
}
```

### Cache Profiles and Cache-Control Headers

Configure response cache profiles to set `Cache-Control` headers for HTTP responses:

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddResponseCaching();

        services.AddMvc(options =>
        {
            options.CacheProfiles.Add("Default", new CacheProfile
            {
                Duration = 300,
                Location = ResponseCacheLocation.Any,
                VaryByHeader = "Accept-Encoding",
            });

            options.CacheProfiles.Add("NoCache", new CacheProfile
            {
                Duration = 0,
                Location = ResponseCacheLocation.None,
                NoStore = true,
            });
        });
    }
}
```

Apply a cache profile to a controller or action:

```csharp
[ResponseCache(CacheProfileName = "Default")]
public sealed class CatalogController : Controller
{
    public IActionResult Index()
    {
        return View();
    }

    [ResponseCache(CacheProfileName = "NoCache")]
    public IActionResult Checkout()
    {
        return View();
    }
}
```

### Caching Content Queries

Combine `IDistributedCache` with content queries to avoid repeated database calls:

```csharp
using System.Text.Json;
using Microsoft.Extensions.Caching.Distributed;
using OrchardCore.ContentManagement;
using OrchardCore.Environment.Cache;

public sealed class CachedArticleService
{
    private readonly IContentManager _contentManager;
    private readonly IDistributedCache _distributedCache;
    private readonly ISignal _signal;

    public CachedArticleService(
        IContentManager contentManager,
        IDistributedCache distributedCache,
        ISignal signal)
    {
        _contentManager = contentManager;
        _distributedCache = distributedCache;
        _signal = signal;
    }

    public async Task<IEnumerable<ContentItem>> GetPublishedArticlesAsync()
    {
        var cacheKey = "published-articles";
        var cached = await _distributedCache.GetStringAsync(cacheKey);

        if (cached is not null)
        {
            return JsonSerializer.Deserialize<IEnumerable<ContentItem>>(cached)
                ?? [];
        }

        var articles = await _contentManager
            .GetAsync(VersionOptions.Published);

        var options = new DistributedCacheEntryOptions
        {
            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10),
        };

        await _distributedCache.SetStringAsync(
            cacheKey,
            JsonSerializer.Serialize(articles),
            options);

        return articles;
    }

    public async Task InvalidateArticleCacheAsync()
    {
        await _distributedCache.RemoveAsync("published-articles");
        await _signal.SignalTokenAsync("contenttype:Article");
    }
}
```
