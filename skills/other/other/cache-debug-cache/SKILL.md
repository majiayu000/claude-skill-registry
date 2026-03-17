---
name: cache__debug_cache
description: Debug HybridCache and Redis caching issues when data isn't being cached or invalidated correctly. Use this when cache hit/miss rates are wrong.
---

Use this guide to troubleshoot **HybridCache** and **Redis** caching issues.

## Quick Path (80% of issues)

// turbo
1. **Check Redis is running**:
   ```bash
   docker ps | grep redis && redis-cli ping
   ```
   Should see: `PONG`

2. **Check cache tags match** between `GetOrCreateAsync` and `RemoveByTagAsync`
3. **Check cache key includes all params** (page, culture, userId)
4. **Check `RemoveByTagAsync`** is called after mutations

If still broken, continue to full debugging below.

---

## Symptoms

- ✗ Data not being cached (always fetching from DB)
- ✗ Stale data after updates (cache not invalidating)
- ✗ Cache misses when should be hits
- ✗ Redis connection errors

## Related Skills

**Prerequisites**:
- `/aspire__start_solution` - Solution must be running to debug cache

**First Steps**:
- `/test__verify_feature` - Run basic checks before caching-specific debugging

**Related Debugging**:
- `/frontend__debug_sse` - If issue seems SSE-related instead of cache
- `/ops__doctor_check` - Verify Docker and Redis are installed

**After Fixing**:
- `/test__verify_feature` - Confirm caching works correctly
- `/test__integration_scaffold` - Add tests for cache scenarios

## Debugging Steps

### 1. Verify Cache Configuration

Check `appsettings.json` for cache settings:

```json
{
  "ConnectionStrings": {
    "cache": "localhost:6379"  // Redis connection string
  }
}
```

**Test Redis connection**:

```bash
# Check if Redis is running
docker ps | grep redis

# Test connection
redis-cli ping
# Expected: PONG
```

**If Redis isn't running**:
- Start via Aspire: `aspire run`
- Or manually: `docker run -p 6379:6379 redis:latest`

### 2. Verify HybridCache Setup

Check `Program.cs` in ApiService:

```csharp
// ✅ Correct - HybridCache configured
builder.Services.AddHybridCache(options =>
{
    options.DefaultEntryOptions = new HybridCacheEntryOptions
    {
        Expiration = TimeSpan.FromMinutes(5),
        LocalCacheExpiration = TimeSpan.FromMinutes(1)
    };
});

// Add Redis (if using distributed cache)
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("cache");
});

// ✗ Wrong - missing configuration
// (no AddHybridCache call)
```

### 3. Verify Cache Usage in Code

Check endpoint is using cache:

```csharp
// ✅ Correct - using cache with tags
public static async Task<IResult> GetBooks(
    IDocumentStore store,
    HybridCache cache,  // ✅ Injected
    CancellationToken cancellationToken = default)
{
    var books = await cache.GetOrCreateAsync(
        "books:list",  // Cache key
        async entry =>
        {
            entry.SetOptions(new HybridCacheEntryOptions
            {
                Expiration = TimeSpan.FromMinutes(5)
            });

            await using var session = store.QuerySession();
            return await session.Query<BookProjection>().ToListAsync();
        },
        tags: [CacheTags.BookList],  // ✅ Tags for invalidation
        cancellationToken: cancellationToken
    );

    return Results.Ok(books);
}

// ✗ Wrong - no caching
public static async Task<IResult> GetBooks(
    IDocumentStore store,
    CancellationToken cancellationToken = default)
{
    await using var session = store.QuerySession();
    var books = await session.Query<BookProjection>().ToListAsync();
    return Results.Ok(books);
}
```

### 4. Verify Cache Invalidation

Check cache is invalidated after mutations:

```csharp
// In Handler or Endpoint
public static async Task<IResult> UpdateBook(
    UpdateBookCommand cmd,
    IDocumentSession session,
    HybridCache cache,
    CancellationToken cancellationToken)
{
    // ... mutation logic ...

    // ✅ Correct - invalidate by tag
    await cache.RemoveByTagAsync(CacheTags.BookList, cancellationToken);

    return Results.Ok();
}

// ✗ Wrong - cache never invalidated
// (no RemoveByTagAsync call)
```

### 5. Check Cache Tags Definition

Verify cache tags are defined in constants:

```csharp
// src/ApiService/BookStore.ApiService/Infrastructure/CacheTags.cs
public static class CacheTags
{
    public const string BookList = "book-list";
    public const string BookDetails = "book-details";
    public const string AuthorList = "author-list";

    // ❌ Missing: Your resource tags
}
```

**If tags are missing**:
1. Add const string for your resource
2. Use consistent naming pattern
3. Use tags in both `GetOrCreateAsync` and `RemoveByTagAsync`

### 6. Verify Cache Keys Include All Parameters

Cache keys must include all query parameters:

```csharp
// ✅ Correct - includes page, pageSize, culture
var cacheKey = $"books:page:{page}:size:{pageSize}:culture:{culture}";

var books = await cache.GetOrCreateAsync(
    cacheKey,
    async entry => { /* fetch data */ },
    tags: [CacheTags.BookList],
    cancellationToken: cancellationToken
);

// ✗ Wrong - missing parameters (same key for different pages)
var cacheKey = "books:list";  // Doesn't include page/size!
```

### 7. Test Cache Behavior

**Test cache hit**:

```bash
# Request 1 - cache miss
curl http://localhost:5000/api/books

# Request 2 - should be cache hit (faster)
curl http://localhost:5000/api/books
```

**Measure response times**:
- First request: ~100-500ms (DB query)
- Second request: ~1-10ms (cache hit)

**If both requests are slow**:
- Cache isn't working
- Check HybridCache configuration
- Verify cache key is consistent

### 8. Check Redis with redis-cli

Connect to Redis and inspect:

```bash
# Connect to Redis
redis-cli

# List all keys
KEYS *

# Get cache entry (if using Redis serialization)
GET "books:list"

# Check TTL (time to live)
TTL "books:list"

# Flush all cache (for testing)
FLUSHALL
```

### 9. Monitor Cache Metrics

Check Aspire Dashboard:
1. Go to Traces
2. Look for cache operations
3. Check hit/miss rates
4. Monitor cache latency

**Add logging to debug**:

```csharp
public static async Task<IResult> GetBooks(
    IDocumentStore store,
    HybridCache cache,
    ILogger<Program> logger,  // Add logger
    CancellationToken cancellationToken = default)
{
    logger.LogInformation("Fetching books from cache");

    var books = await cache.GetOrCreateAsync(
        "books:list",
        async entry =>
        {
            logger.LogInformation("Cache MISS - fetching from DB");
            await using var session = store.QuerySession();
            return await session.Query<BookProjection>().ToListAsync();
        },
        tags: [CacheTags.BookList],
        cancellationToken: cancellationToken
    );

    logger.LogInformation("Returning {Count} books", books.Count);
    return Results.Ok(books);
}
```

## Common Issues & Fixes

### Issue: Cache Always Misses

**Symptom**: Every request fetches from DB

**Diagnosis**:
1. Add logging to cache callback (see above)
2. Check if callback always executes

**Fixes**:
- Verify Redis is running and connected
- Check cache key is consistent across requests
- Ensure HybridCache is registered in DI
- Verify no exceptions in cache retrieval

### Issue: Stale Data After Updates

**Symptom**: Updates don't reflect until cache expires

**Diagnosis**:
1. Check if `RemoveByTagAsync` is called
2. Verify tags match between get and invalidate

**Fixes**:
```csharp
// ✅ Correct - matching tags
await cache.GetOrCreateAsync("key", ..., tags: [CacheTags.BookList]);
await cache.RemoveByTagAsync(CacheTags.BookList);

// ✗ Wrong - mismatched tags
await cache.GetOrCreateAsync("key", ..., tags: [CacheTags.BookList]);
await cache.RemoveByTagAsync(CacheTags.BookDetails);  // Wrong tag!
```

### Issue: Different Users See Same Data (Cache Poisoning)

**Symptom**: User A sees User B's data

**Diagnosis**:
- Cache key doesn't include user ID or culture

**Fix**:
```csharp
// ✅ Correct - user-specific cache key
var userId = httpContext.User.FindFirst("sub")?.Value;
var cacheKey = $"cart:{userId}";

// ✗ Wrong - shared cache key
var cacheKey = "cart";  // Same for all users!
```

### Issue: Redis Connection Errors

**Symptom**: `StackExchange.Redis.RedisConnectionException`

**Diagnosis**:
1. Check Redis container status: `docker ps | grep redis`
2. Verify connection string in `appsettings.json`
3. Check network between app and Redis

**Fixes**:
- Restart Redis container
- Check firewall rules
- Verify Aspire resource configuration in AppHost

### Issue: Localized Data Not Cached Correctly

**Symptom**: Wrong language data returned

**Diagnosis**:
- Cache key doesn't include culture

**Fix**:
```csharp
// ✅ Correct - culture in cache key
var culture = CultureInfo.CurrentUICulture.Name;
var cacheKey = $"books:list:culture:{culture}";

// ✗ Wrong - missing culture
var cacheKey = "books:list";
```

### Issue: Memory Leak

**Symptom**: Memory grows over time

**Diagnosis**:
- Cache expiration too long
- Too many unique cache keys

**Fixes**:
```csharp
// ✅ Correct - reasonable expiration
entry.SetOptions(new HybridCacheEntryOptions
{
    Expiration = TimeSpan.FromMinutes(5),        // Distributed cache
    LocalCacheExpiration = TimeSpan.FromMinutes(1)  // In-memory cache
});

// ✗ Wrong - cache never expires
entry.SetOptions(new HybridCacheEntryOptions
{
    Expiration = TimeSpan.MaxValue  // Never expires!
});
```

## Verification Checklist

- [ ] Redis container is running (`docker ps`)
- [ ] Connection string configured in `appsettings.json`
- [ ] `AddHybridCache()` called in `Program.cs`
- [ ] Cache injected in endpoint (`HybridCache cache`)
- [ ] Cache key includes all query parameters
- [ ] Cache tags defined and used consistently
- [ ] `RemoveByTagAsync` called after mutations
- [ ] Cache expiration times are reasonable
- [ ] Logging added to debug cache behavior
- [ ] Metrics monitored in Aspire dashboard

## Debugging Tools

**Redis CLI**:
```bash
redis-cli
> KEYS *              # List all keys
> GET "key"           # Get value
> TTL "key"           # Check expiration
> FLUSHALL           # Clear all cache
```

**Aspire Dashboard**:
- Traces → Look for cache operations
- Metrics → Monitor hit/miss rates
- Logs → Search for cache-related errors

**Logging**:
```csharp
logger.LogInformation("Cache key: {Key}", cacheKey);
logger.LogInformation("Cache tags: {Tags}", string.Join(", ", tags));
logger.LogInformation("Cache callback executed (MISS)");
```

## Performance Tips

- ✅ Use short local cache TTL (1-2 minutes)
- ✅ Use longer distributed cache TTL (5-15 minutes)
- ✅ Include culture in cache keys for localized data
- ✅ Use tag-based invalidation for complex scenarios
- ✅ Monitor cache hit rates (target: >80%)
- ❌ Don't cache user-specific data without user ID in key
- ❌ Don't use very long expirations (causes stale data)

## Related Skills

**First Steps**:
- `/test__verify_feature` - Run basic checks before caching-specific debugging

**Related Debugging**:
- `/frontend__debug_sse` - If issue seems SSE-related instead of cache
- `/ops__doctor_check` - Verify Docker and Redis are installed

**After Fixing**:
- `/test__verify_feature` - Confirm caching works correctly
- `/test__integration_scaffold` - Add tests for cache scenarios

**See Also**:
- [marten__list_query](../marten__list_query/SKILL.md) - Cache implementation patterns
- [wolverine__create_operation](../wolverine__create_operation/SKILL.md) - Cache invalidation on mutations
- [caching-guide](../../../docs/guides/caching-guide.md) - HybridCache configuration and patterns
- ApiService AGENTS.md - HybridCache configuration
