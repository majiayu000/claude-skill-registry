---
name: Elasticsearch
description: Elasticsearch 5.2 operations using HTTP API - searching, indexing, bulk operations, scroll API, and alias management
---

# Elasticsearch

## Instructions

When helping users work with Elasticsearch 5.2 in C#, follow these guidelines:

1. **Version Constraint**: Always use Elasticsearch 5.2 API patterns. This version will not change.

2. **HTTP Client Approach**: Use `HttpClient` directly with Elasticsearch REST API instead of official client libraries. This provides better control and compatibility with version 5.2.

3. **ServiceLib.Elasticsearch Wrapper**: Use the ServiceLib.Elasticsearch wrapper class for common operations (search, bulk index, scroll download, etc.)

4. **Bulk Operations**: Use the `_bulk` API for batch indexing. Format: action line + document line (newline-delimited JSON)

5. **Scroll API**: For downloading large indices, use scroll API with 5000 document batches and 1-minute timeout. Always clear scroll context in finally block.

6. **Alias Management**: Our exsiting JAVA codebase uses  timestamped index pattern with aliases for zero-downtime updates (e.g., `price_discount_20250116_123456` with alias `price_discount`), it writes the whole index and then does an alias. Going forward we want to do in-place overwrites and deletes instead.

7. **Query Format**: Use JSON string format for queries with `bool`, `filter`, `range`, etc. Use raw string literals (`"""..."""`) for complex queries

8. **Dynamic Results**: Parse search results as `dynamic` and access via property names (e.g., `result.hits.hits[0]._source`)

9. **Error Handling**: Always catch and log exceptions. Return "Error" string for operation failures to allow caller to handle.

10. **Index Creation**: Create indices without explicit mappings - let Elasticsearch auto-detect field types (safer and matches production patterns)

## Examples

### Example 1: Search with Range Filters
```
User: Help me search Elasticsearch for pricing periods active today

Claude: I'll use the ServiceLib.Elasticsearch wrapper with a bool query and range filters:
- Current date for comparison
- Two range filters (start <= today AND end >= today)
- Access results via dynamic object properties

[Provides implementation using the Search pattern from reference material below]
```

### Example 2: Bulk Index with Alias Pattern
```
User: I need to bulk load price data into Elasticsearch with zero downtime

Claude: I'll use the timestamped index + alias pattern:
1. Create new timestamped index (e.g., price_discount_20250116_123456)
2. Bulk index documents in batches
3. Switch alias to new index atomically
4. Delete old index on success, or cleanup new index on failure

[Provides implementation using the Bulk Index and Alias patterns from reference material below]
```

### Example 3: Download Entire Index
```
User: How do I download all documents from an Elasticsearch index?

Claude: I'll use the Scroll API for efficient large dataset download:
- Initial search with scroll=1m and size=5000
- Loop through scroll pages until no more documents
- Clear scroll context in finally block
- Log progress with document counts

[Provides implementation using the DownloadIndex pattern from reference material below]
```

### Example 4: Update Documents by Query
```
User: I need to update multiple documents in Elasticsearch based on a query

Claude: I'll use the _update_by_query API:
- POST to /{index}/_update_by_query
- Query to match documents
- Script to update fields
- Error handling with response logging

[Provides implementation using the UpdateByQuery pattern from reference material below]
```

---

# Reference Implementation Details

The sections below contain proven working code from production systems (JordanPrice) that the examples above reference.

**Reference Files in This Folder**:
- `Elasticsearch.cs` - Core ServiceLib wrapper with all HTTP operations
- `ElasticsearchService.cs` - JordanPrice service implementation showing alias pattern

# Elasticsearch 5.2 Operations

**Primary Library**: `System.Net.Http.HttpClient` with Elasticsearch REST API
**Version**: Elasticsearch 5.2 (fixed, will not change)
**Projects**: JordanPrice, ElastiCompare, CRMPollerFixer

## ServiceLib.Elasticsearch Wrapper

**Location**: `Elasticsearch.cs` (in this skills folder)
**Purpose**: Reusable HTTP-based Elasticsearch client with common operations

### Constructor Pattern

```csharp
using ServiceLib;
using Microsoft.Extensions.Logging;

// Create client instance
var elasticsearchClient = new ServiceLib.Elasticsearch(
    baseUrl: "http://localhost:9200",
    logger: _logger
);

// Multiple instances for source/destination pattern
var sourceClient = new ServiceLib.Elasticsearch(_settings.Elasticsearch.Source, _logger);
var destinationClient = new ServiceLib.Elasticsearch(_settings.Elasticsearch.Destination, _logger);
```

**Key Features**:
- HttpClient with proper User-Agent header
- Automatic URL trimming and formatting
- Comprehensive logging at Debug and Info levels
- Dynamic result parsing

## Search Operations

### Basic Search (JordanPrice/Services/ElasticsearchService.cs)

```csharp
public dynamic Search(string index, string query)
{
    var cleanBaseUrl = _baseUrl.TrimEnd('/');
    var url = $"{cleanBaseUrl}/{index}/_search";
    _logger.LogInformation("Search {url}", url);
    _logger.LogInformation("  query {query}", query);
    var content = new StringContent(query, Encoding.UTF8, "application/json");

    var response = _httpClient.PostAsync(url, content).Result;
    try {
        response.EnsureSuccessStatusCode();
        var json = response.Content.ReadAsStringAsync().Result;
        _logger.LogInformation("  response status: {status}", response.StatusCode);

        dynamic result = JsonConvert.DeserializeObject<dynamic>(json)!;
        _logger.LogInformation("  total hits: {total}", (int)result.hits.total);
        if (result.hits.hits.Count > 0)
        {
            _logger.LogInformation("  first document index: {index}", (string)result.hits.hits[0]._index);
            _logger.LogInformation("  first document ID: {id}", (string)result.hits.hits[0]._id);
        }
        _logger.LogDebug("  response {json}", json);
        return result;
    }
    catch (Exception ex)
    {
        _logger.LogError("Error searching {url}: {message}", url, ex.Message);
        throw;
    }
}
```

### Range Query with Date Filters

```csharp
public Task<PricingPeriod?> GetCurrentPricingPeriodAsync()
{
    try
    {
        var today = DateTime.Today.ToString("yyyy-MM-dd");

        // Use raw string literal for complex query
        var query = $$"""
        {
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "keyInStartDate": {
                                    "lte": "{{today}}"
                                }
                            }
                        },
                        {
                            "range": {
                                "keyInEndDate": {
                                    "gte": "{{today}}"
                                }
                            }
                        }
                    ]
                }
            }
        }
        """;

        var elasticsearchClient = new ServiceLib.Elasticsearch(_settings.Elasticsearch.Source, _logger);
        var result = elasticsearchClient.Search("pricing_periods", query);

        if (result?.hits?.hits?.Count > 0)
        {
            var source = result.hits.hits[0]._source;

            // Extract values directly from the dynamic object
            var period = new PricingPeriod
            {
                Id = source.id?.ToString() ?? string.Empty,
                KeyInStartDate = source.keyInStartDate?.ToString() ?? string.Empty,
                KeyInEndDate = source.keyInEndDate?.ToString() ?? string.Empty
            };

            _logger.LogInformation("Found pricing period: Id='{Id}', Start='{Start}', End='{End}'",
                period.Id, period.KeyInStartDate, period.KeyInEndDate);

            return Task.FromResult<PricingPeriod?>(period);
        }

        _logger.LogWarning("No current pricing period found in Elasticsearch");
        return Task.FromResult<PricingPeriod?>(null);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error getting current pricing period from Elasticsearch");
        return Task.FromResult<PricingPeriod?>(null);
    }
}
```

**Key Patterns**:
- Raw string literals (`$$"""..."""`) with interpolation for dates
- Bool query with multiple filter clauses
- Range queries for date filtering
- Dynamic object navigation (`result.hits.hits[0]._source`)
- Null-safe property access with `?.` operator
- ToString() with null-coalescing for safe string conversion

## Scroll API for Large Downloads

### Complete Index Download (ServiceLib/Elasticsearch.cs)

```csharp
public List<dynamic> DownloadIndex(string index)
{
    var allData = new List<dynamic>();
    const string scrollTimeout = "1m"; // Keep the scroll context open for 1 minute
    string? scrollId = null;

    try
    {
        // Initial search request to get the first batch and a scroll_id
        var initialQuery = JsonConvert.SerializeObject(new
        {
            query = new { match_all = new { } },
            size = 5000 // Initial batch size
        });

        var initialResponse = _httpClient.PostAsync(
            $"{_baseUrl}/{index}/_search?scroll={scrollTimeout}",
            new StringContent(initialQuery, Encoding.UTF8, "application/json")
        ).Result;

        initialResponse.EnsureSuccessStatusCode();
        var initialJson = initialResponse.Content.ReadAsStringAsync().Result;
        dynamic initialResults = JsonConvert.DeserializeObject<dynamic>(initialJson)!;

        scrollId = initialResults._scroll_id;
        allData.AddRange(initialResults.hits.hits);
        _logger.LogInformation("Downloaded {count} documents from {index} (initial scroll), total so far: {total}",
            (int)initialResults.hits.hits.Count, index, (int)allData.Count);

        // Loop to fetch subsequent scroll pages
        while (true)
        {
            if (string.IsNullOrEmpty(scrollId))
            {
                _logger.LogWarning("Scroll ID is null or empty, breaking from scroll loop.");
                break;
            }

            var scrollQuery = JsonConvert.SerializeObject(new
            {
                scroll = scrollTimeout,
                scroll_id = scrollId
            });

            var scrollResponse = _httpClient.PostAsync(
                $"{_baseUrl}/_search/scroll",
                new StringContent(scrollQuery, Encoding.UTF8, "application/json")
            ).Result;

            scrollResponse.EnsureSuccessStatusCode();
            var scrollJson = scrollResponse.Content.ReadAsStringAsync().Result;
            dynamic scrollResults = JsonConvert.DeserializeObject<dynamic>(scrollJson)!;

            if (scrollResults.hits.hits.Count == 0)
            {
                break; // No more documents
            }

            allData.AddRange(scrollResults.hits.hits);
            scrollId = scrollResults._scroll_id; // Update scroll ID for next iteration
            _logger.LogInformation("Downloaded {count} documents from {index} (scrolling), total so far: {total}",
                (int)scrollResults.hits.hits.Count, index, (int)allData.Count);
        }
    }
    catch (Exception ex)
    {
        _logger.LogError("Error downloading index {index} using Scroll API: {message}", index, ex.Message);
        throw;
    }
    finally
    {
        // Always clear the scroll context
        if (!string.IsNullOrEmpty(scrollId))
        {
            try
            {
                var clearScrollRequest = new HttpRequestMessage(HttpMethod.Delete, $"{_baseUrl}/_search/scroll");
                clearScrollRequest.Content = new StringContent(
                    JsonConvert.SerializeObject(new { scroll_id = new[] { scrollId } }),
                    Encoding.UTF8,
                    "application/json"
                );

                var clearResponse = _httpClient.SendAsync(clearScrollRequest).Result;
                clearResponse.EnsureSuccessStatusCode();
                _logger.LogDebug("Cleared scroll context for scroll ID: {scrollId}", scrollId);
            }
            catch (Exception ex)
            {
                _logger.LogError("Error clearing scroll context {scrollId}: {message}", scrollId, ex.Message);
            }
        }
    }

    return allData.Select(hit => hit._source).ToList();
}
```

**Scroll API Best Practices**:
- Use 5000 document batch size (ES 5.2 recommended)
- 1-minute scroll timeout
- Initial search with `?scroll=1m` parameter
- Subsequent scrolls via `/_search/scroll` endpoint
- Update scrollId on each iteration
- **CRITICAL**: Always clear scroll context in finally block
- Log progress with document counts
- Break loop when hit count is 0

## Bulk Indexing

### Bulk API Format (ServiceLib/Elasticsearch.cs)

```csharp
public static string BulkToJson(string index, string type, IEnumerable<object> docs)
{
    var settings = new JsonSerializerSettings { NullValueHandling = NullValueHandling.Ignore };

    var json = new StringBuilder();
    foreach (var doc in docs)
    {
        var meta = new { index = new { _index = index, _type = type } };
        json.AppendLine(SerializeKeepingNulls(meta));
        json.AppendLine(SerializeIgnoringNulls(doc));
    }
    return json.ToString();
}

public string BulkIndex(string index, IEnumerable<object> docs)
{
    var url = DeAliasURL(index, "_bulk");
    var json = BulkToJson(ConcreteIndex(index), index, docs);
    _logger.LogDebug("BulkIndex {json}", json);
    var content = new StringContent(json, Encoding.UTF8, "application/json");
    var response = _httpClient.PostAsync(url, content).Result;
    try {
        response.EnsureSuccessStatusCode();
        return response.Content.ReadAsStringAsync().Result;
    }
    catch (Exception ex)
    {
        var errorResponse = response.Content.ReadAsStringAsync().Result;
        _logger.LogError("Error bulk indexing documents: {message}. Response: {response}", ex.Message, errorResponse);
        return "Error";
    }
}

public static string SerializeKeepingNulls(object obj)
{
    var settings = new JsonSerializerSettings { NullValueHandling = NullValueHandling.Include };
    return JsonConvert.SerializeObject(obj, settings);
}

public static string SerializeIgnoringNulls(object obj)
{
    var settings = new JsonSerializerSettings { NullValueHandling = NullValueHandling.Ignore };
    return JsonConvert.SerializeObject(obj, settings);
}
```

### Bulk Index Usage (JordanPrice/Services/ElasticsearchService.cs)

```csharp
public Task BulkIndexPriceDiscountsAsync(IEnumerable<PriceDiscount> priceDiscounts)
{
    var documents = priceDiscounts.ToList();

    try
    {
        var result = _destinationClient.BulkIndex(_newIndexName, documents);
        if (result == "Error")
        {
            throw new InvalidOperationException("Bulk index operation failed");
        }
        return Task.CompletedTask;
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error during bulk index operation to {IndexName}", _newIndexName);
        throw;
    }
}
```

**Bulk Format Requirements**:
- Newline-delimited JSON (NDJSON)
- Action line: `{"index":{"_index":"myindex","_type":"mytype"}}\n`
- Document line: `{"field1":"value1",...}\n`
- Keep nulls in action metadata, ignore nulls in documents
- StringBuilder for efficient string concatenation
- Check for "Error" return value

## Index Management with Aliases

### Zero-Downtime Index Updates (JordanPrice/Services/ElasticsearchService.cs)

```csharp
private const string IndexPrefix = "price_discount_";
private const string AliasName = "price_discount";
private string _newIndexName = string.Empty;

// Step 1: Create timestamped index
public async Task InitializeIndexAsync()
{
    // Generate new timestamped index name
    _newIndexName = $"{IndexPrefix}{DateTime.Now:yyyyMMdd_HHmmss}";
    _logger.LogInformation("Creating new index: {IndexName}", _newIndexName);

    try
    {
        // Create new index without explicit mapping - let Elasticsearch auto-detect field types
        using var httpClient = new HttpClient();
        var createUrl = $"{_settings.Elasticsearch.Destination.TrimEnd('/')}/{_newIndexName}";

        var response = await httpClient.PutAsync(createUrl, null);

        if (response.IsSuccessStatusCode)
        {
            _logger.LogInformation("Successfully created new index {IndexName}", _newIndexName);
        }
        else
        {
            var errorContent = await response.Content.ReadAsStringAsync();
            throw new InvalidOperationException($"Failed to create index {_newIndexName}: {response.StatusCode} - {errorContent}");
        }
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error creating new index {IndexName}", _newIndexName);
        throw;
    }
}

// Step 2: Bulk index documents (see Bulk Indexing section above)

// Step 3: Switch alias atomically
public async Task FinalizeIndexAsync()
{
    _logger.LogInformation("Finalizing index - switching alias {AliasName} to point to {NewIndexName}",
        AliasName, _newIndexName);

    try
    {
        // Switch the alias to point to the new index
        var aliasActions = $$"""
        {
            "actions": [
                {
                    "remove": {
                        "index": "{{IndexPrefix}}*",
                        "alias": "{{AliasName}}"
                    }
                },
                {
                    "add": {
                        "index": "{{_newIndexName}}",
                        "alias": "{{AliasName}}"
                    }
                }
            ]
        }
        """;

        using var httpClient = new HttpClient();
        var aliasUrl = $"{_settings.Elasticsearch.Destination.TrimEnd('/')}/_aliases";
        var content = new StringContent(aliasActions, Encoding.UTF8, "application/json");

        var response = await httpClient.PostAsync(aliasUrl, content);

        if (response.IsSuccessStatusCode)
        {
            _logger.LogInformation("Successfully switched alias {AliasName} to {NewIndexName}",
                AliasName, _newIndexName);
        }
        else
        {
            var errorContent = await response.Content.ReadAsStringAsync();
            throw new InvalidOperationException($"Failed to switch alias {AliasName} to {_newIndexName}: {response.StatusCode} - {errorContent}");
        }
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error switching alias {AliasName} to {NewIndexName}", AliasName, _newIndexName);
        throw;
    }
}

// Step 4: Cleanup on failure
public async Task DeleteNewIndexAsync()
{
    if (string.IsNullOrEmpty(_newIndexName))
    {
        _logger.LogInformation("No new index to clean up");
        return;
    }

    _logger.LogInformation("Cleaning up failed index: {IndexName}", _newIndexName);

    try
    {
        using var httpClient = new HttpClient();
        var deleteUrl = $"{_settings.Elasticsearch.Destination.TrimEnd('/')}/{_newIndexName}";

        var response = await httpClient.DeleteAsync(deleteUrl);

        if (response.IsSuccessStatusCode)
        {
            _logger.LogInformation("Successfully deleted failed index {IndexName}", _newIndexName);
        }
        else
        {
            var errorContent = await response.Content.ReadAsStringAsync();
            _logger.LogWarning("Failed to delete index {IndexName}: {StatusCode} - {Error}",
                _newIndexName, response.StatusCode, errorContent);
        }
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error deleting failed index {IndexName}", _newIndexName);
        // Don't re-throw since this is cleanup - log and continue
    }
}
```

**Alias Pattern Benefits**:
- Zero downtime during index updates
- Atomic alias switch (remove old + add new in single request)
- Timestamped indices for audit trail
- Easy rollback (just switch alias back)
- Cleanup of failed indices

## Alias-Aware Operations

### Handle Aliases in Document Operations (ServiceLib/Elasticsearch.cs)

```csharp
public bool IsAlias(string indexName)
{
    try
    {
        var url = $"{_baseUrl}/_alias/{indexName}";
        var response = _httpClient.GetAsync(url).Result;
        return response.IsSuccessStatusCode;
    }
    catch (Exception ex)
    {
        _logger.LogError("Error checking if {indexName} is an alias: {message}", indexName, ex.Message);
        return false;
    }
}

private List<string> GetAliasInfo(string aliasName)
{
    try
    {
        var url = $"{_baseUrl}/_alias/{aliasName}";
        var response = _httpClient.GetAsync(url).Result;

        if (!response.IsSuccessStatusCode)
        {
            return new List<string>();
        }

        var json = response.Content.ReadAsStringAsync().Result;
        var aliasInfo = JsonConvert.DeserializeObject<Dictionary<string, object>>(json);

        if (aliasInfo == null || aliasInfo.Count == 0)
        {
            return new List<string>();
        }

        return aliasInfo.Keys.ToList();
    }
    catch (Exception ex)
    {
        _logger.LogError("Error getting alias info for {aliasName}: {message}", aliasName, ex.Message);
        return new List<string>();
    }
}

public string ConcreteIndex(string index)
{
    if (IsAlias(index))
    {
        return GetAliasInfo(index)[0];
    }
    return index;
}

private string DeAliasURL(string index, string id)
{
    var cleanBaseUrl = _baseUrl.TrimEnd('/');
    if (IsAlias(index))
    {
        var concreteIndex = ConcreteIndex(index);
        return $"{cleanBaseUrl}/{concreteIndex}/{index}/{id}";
    }
    return $"{cleanBaseUrl}/{index}/{id}";
}
```

**Alias Handling Pattern**:
- Check if name is alias before document operations
- Resolve to concrete index name
- URL format with alias: `/{concrete_index}/{alias}/{id}`
- URL format without alias: `/{index}/{id}`
- Prevents routing errors

## Update By Query

### Batch Document Updates (ServiceLib/Elasticsearch.cs)

```csharp
public string UpdateByQuery(string index, string query)
{
    var url = $"{_baseUrl}/{index}/_update_by_query";
    _logger.LogInformation("UpdateByQuery {url}", url);
    var content = new StringContent(query, Encoding.UTF8, "application/json");

    var response = _httpClient.PostAsync(url, content).Result;
    try {
        response.EnsureSuccessStatusCode();
        return response.Content.ReadAsStringAsync().Result;
    }
    catch (Exception ex)
    {
        _logger.LogError("Error updating document by query {query}: {message}", query, ex.Message);
        return "Error";
    }
}
```

## Individual Document Operations

### Index Single Document

```csharp
public string IndexDocument(string index, string id, object document)
{
    var url = DeAliasURL(index, id);
    _logger.LogDebug("IndexDocumentAsync {url}", url);
    var content = new StringContent(SerializeIgnoringNulls(document), Encoding.UTF8, "application/json");
    var response = _httpClient.PutAsync(url, content).Result;
    try {
        response.EnsureSuccessStatusCode();
        return response.Content.ReadAsStringAsync().Result;
    }
    catch (Exception ex)
    {
        var errorResponse = response.Content.ReadAsStringAsync().Result;
        _logger.LogError("Error indexing document {id} to index {index}: {message}. Response: {response}",
            id, index, ex.Message, errorResponse);
        return "Error";
    }
}
```

### Delete Document

```csharp
public string DeleteDocument(string index, string id)
{
    var url = DeAliasURL(index, id);
    _logger.LogInformation("DeleteDocument {url}", url);
    var response = _httpClient.DeleteAsync(url).Result;
    try {
        response.EnsureSuccessStatusCode();
        return response.Content.ReadAsStringAsync().Result;
    }
    catch (Exception ex)
    {
        _logger.LogError("Error deleting document {id} from index {index}: {message}", id, index, ex.Message);
        return "Error";
    }
}
```

## Utility Functions

### Extract IDs from Search Results

```csharp
public static List<string> ExtractIds(dynamic searchResults)
{
    var ids = new List<string>();
    foreach (var hit in searchResults.hits.hits)
    {
        ids.Add((string)hit._id);
    }
    return ids;
}

public static string GetId(dynamic hit)
{
    return hit._id;
}
```

### Get Indices Information

```csharp
public dynamic GetIndices()
{
    var url = $"{_baseUrl}/_cat/indices?format=json";
    var response = _httpClient.GetAsync(url).Result;
    try {
        response.EnsureSuccessStatusCode();
        var json = response.Content.ReadAsStringAsync().Result;
        return JsonConvert.DeserializeObject<dynamic>(json)!;
    }
    catch (Exception ex)
    {
        _logger.LogError("Error getting indices: {message}", ex.Message);
        return "Error";
    }
}
```

## JSON Canonicalization for Comparison

### Clean and Sort JSON for Hashing (ServiceLib/Elasticsearch.cs)

```csharp
public string? GetCanonicalJsonString(dynamic obj)
{
    if (obj == null)
    {
        return null;
    }

    JObject jObject = JObject.FromObject(obj);

    // Remove properties that are null or empty strings
    var propertiesToRemove = jObject.Properties()
                                    .Where(p => p.Value.Type == JTokenType.Null ||
                                                (p.Value.Type == JTokenType.String && string.IsNullOrEmpty(p.Value.ToString())))
                                    .ToList();

    foreach (var prop in propertiesToRemove)
    {
        prop.Remove();
    }

    var orderedProperties = jObject.Properties().OrderBy(p => p.Name, StringComparer.Ordinal);
    var orderedJObject = new JObject(orderedProperties);

    CleanJToken(orderedJObject); // Apply cleaning for hidden characters and trimming

    var settings = new JsonSerializerSettings
    {
        NullValueHandling = NullValueHandling.Ignore,
        Formatting = Formatting.None
    };
    return JsonConvert.SerializeObject(orderedJObject, settings);
}

public JToken CleanJToken(JToken token)
{
    if (token.Type == JTokenType.String)
    {
        var jValue = (JValue)token;
        if (jValue.Value is string s)
        {
            // Remove null characters and trim whitespace
            jValue.Value = s.Replace("\u0000", "").Trim();
        }
        return token;
    }
    else if (token.Type == JTokenType.Null)
    {
        return new JValue(string.Empty); // Convert null to empty string
    }
    else if (token.Type == JTokenType.Object)
    {
        JObject obj = (JObject)token;
        foreach (var property in obj.Properties().ToList())
        {
            JToken cleanedValue = CleanJToken(property.Value);
            if (cleanedValue != property.Value)
            {
                property.Value = cleanedValue;
            }
        }
        return token;
    }
    else if (token.Type == JTokenType.Array)
    {
        JArray arr = (JArray)token;
        for (int i = 0; i < arr.Count; i++)
        {
            JToken cleanedItem = CleanJToken(arr[i]);
            if (cleanedItem != arr[i])
            {
                arr[i] = cleanedItem;
            }
        }
        return token;
    }
    return token;
}
```

**Use Cases**:
- Document comparison/diffing
- Detecting changes between source and destination
- Consistent hashing for deduplication
- Removes null characters, trims whitespace, removes null/empty properties

## Complete Workflow Example

### Zero-Downtime Index Rebuild (JordanPrice Pattern)

```csharp
try
{
    // 1. Create timestamped index
    await InitializeIndexAsync();  // Creates price_discount_20250116_123456

    // 2. Bulk load data in batches
    foreach (var batch in priceDiscounts.Chunk(1000))
    {
        await BulkIndexPriceDiscountsAsync(batch);
    }

    // 3. Switch alias atomically
    await FinalizeIndexAsync();  // Points price_discount alias to new index

    // 4. Success notification
    await SendMailAsync(totalCount);
}
catch (Exception ex)
{
    // Cleanup on failure
    await DeleteNewIndexAsync();
    await SendMailAsync(ex);
    throw;
}
```

## Best Practices Summary

1. **Version Compatibility**: Always use ES 5.2 API patterns (no async/await in old NEST clients)
2. **HTTP Client**: Direct HttpClient provides better control than official client libraries
3. **Scroll API**: Use for large downloads, always clear context in finally block
4. **Bulk Operations**: Use NDJSON format, batch size ~1000-5000 documents
5. **Aliases**: Use timestamped indices with aliases for zero-downtime updates
6. **Error Handling**: Return "Error" string allows caller to decide handling strategy
7. **Dynamic Results**: ES 5.2 works well with dynamic objects, no need for typed models
8. **Logging**: Comprehensive logging at Debug (details) and Info (progress) levels
9. **URL Handling**: Always trim base URLs, handle aliases in document operations
10. **Index Creation**: Let Elasticsearch auto-detect mappings unless specific types needed
