---
name: Parquet Files
description: This describes how to create Parquet files in C#, including updating and multi threaded creation
---

# Parquet Files

## Instructions

When helping users work with Parquet files in C#, follow these guidelines:

1. **Library Selection**: Always use `Parquet.Net` (versions 4.23.5 - 4.25.0) for parquet operations.

2. **Schema Creation**: Generate schemas dynamically from data sources using the pattern matching approach shown below. Convert unsupported types to compatible types:
   - **Decimal** → `double`
   - **DateTimeOffset** → `DateTime` (DateTimeOffset support was dropped due to ambiguity issues)

3. **Batch Sizing**:
   - Default to 50,000 records for single-threaded operations
   - Reduce to 10,000 records for multi-threaded scenarios or wide tables
   - Monitor memory usage and adjust accordingly

4. **Memory Management**:
   - Clear collections after each batch
   - Force garbage collection with `GC.Collect()` and `GC.WaitForPendingFinalizers()` for large datasets
   - Log memory before/after batch processing

5. **Multi-Threading**:
   - Use `ParquetUpdateQueue` pattern for queue-based updates (max 1 active + 1 waiting)
   - Use `SemaphoreSlim` for thread-safe file writing
   - Use `ConcurrentBag<T>` for thread-safe data collection

6. **Incremental Updates**:
   - Track max timestamp from existing files
   - Apply safety buffer (e.g., 10 seconds) for lagging writes
   - Deduplicate using HashSet before appending

7. **Large Files**: Write data in batches directly to the target parquet file. Never create temporary batch files that need combining - this is unnecessary complexity.

8. **Streaming from External Sources**: For very large datasets from external sources (Elasticsearch, APIs, databases), use callback-based streaming to write each source batch immediately as it arrives. This prevents loading millions of records into memory.

## Examples

### Example 1: Create Parquet from MySQL Data
```
User: Help me export my MySQL table to Parquet with incremental updates

Claude: I'll help you create a Parquet export with incremental updates. I'll use:
- ParquetUpdateQueue for thread-safe updates
- Timestamp-based tracking for incremental sync
- 50,000 record batches
- HashSet deduplication to avoid duplicates

[Provides implementation using the BPQuery pattern from reference material below]
```

### Example 2: Multi-threaded Download to Parquet
```
User: I need to download large datasets from Elasticsearch and save to Parquet

Claude: For large multi-threaded downloads, I'll use:
- ConcurrentBag<T> for thread-safe data collection across parallel downloads
- SemaphoreSlim to serialize writes to the parquet file
- 10,000 record batches (smaller for multi-threading)
- Aggressive garbage collection after each batch
- Write directly to target file - no temporary files needed

[Provides implementation using the multi-threaded batch pattern from reference material below]
```

### Example 3: Dynamic Schema from DataTable
```
User: How do I create a Parquet schema from my DataTable?

Claude: I'll create a dynamic schema that maps .NET types to Parquet types, converting unsupported types like Decimal to double.

[Provides the CreateSchemaFromDataTable implementation from reference material below]
```

---

# Reference Implementation Details

The sections below contain proven working code from production systems that the examples above reference.

**Reference Files in This Folder**:
- `BPQuery_Parquet.cs` - Single-threaded MySQL to Parquet with incremental updates
- `ParquetUpdateQueue.cs` - Thread-safe queue pattern for coordinating updates
- `ElastiCompare_ParquetService.cs` - Multi-threaded Elasticsearch to Parquet with batching

# Multi-Threaded Parquet File Operations

## Overview

This document covers proven techniques for safely updating parquet files in multi-threaded scenarios, based on working implementations from BPQuery (MySQL sync) and ElastiCompare (Elasticsearch downloads).

**Library Used**: `Parquet.Net` (versions 4.23.5 - 4.25.0)

## Working Implementations

### BPQuery: Thread-Safe Queue Pattern
**Use Case**: MySQL to Parquet incremental sync with 50k record batches

**Implementation**: ParquetUpdateQueue class with lock-based coordination
```csharp
public class ParquetUpdateQueue
{
    private volatile bool _isProcessing = false;
    private volatile bool _hasWaitingRequest = false;
    private readonly object _queueLock = new object();

    public void QueueUpdate(string requestSource)
    {
        lock (_queueLock)
        {
            if (_isProcessing)
            {
                _hasWaitingRequest = true;
                return;
            }
            _isProcessing = true;
        }

        // Fire-and-forget async processing
        _ = ProcessUpdateAsync(requestSource);
    }
}
```

**Key Benefits**: Maximum 1 active + 1 waiting request, prevents queue buildup

### ElastiFetch: Scroll Batch Streaming Pattern (BEST for Large Downloads)
**Use Case**: Very large Elasticsearch downloads (millions of documents, GBs of data) with minimal memory

**Problem**: Downloading all documents into a List first causes massive memory usage (8GB+ for large indexes!)

**Solution**: Write each scroll batch (5000 docs) immediately as it arrives - never accumulate in memory

```csharp
// Elasticsearch: Callback-based streaming (optimal memory usage)
public async Task DownloadIndexStreamingWithCallbackAsync(
    string index,
    Func<List<(string id, JObject source)>, Task> scrollBatchProcessor)
{
    string? scrollId = null;

    // Initial scroll request (5000 docs)
    var initialResponse = await _httpClient.PostAsync(
        $"{_baseUrl}/{index}/_search?scroll=5m&size=5000",
        new StringContent(JsonConvert.SerializeObject(new {
            query = new { match_all = new { } },
            sort = new[] { "_doc" }
        }), Encoding.UTF8, "application/json"));

    var initialResults = JObject.Parse(await initialResponse.Content.ReadAsStringAsync());
    scrollId = initialResults["_scroll_id"]?.ToString();
    var hits = initialResults["hits"]?["hits"] as JArray;

    // Process first batch immediately
    if (hits != null && hits.Count > 0)
    {
        var scrollBatch = hits.Select(hit => (
            id: hit["_id"]?.ToString() ?? "",
            source: hit["_source"] as JObject
        )).Where(x => x.source != null).ToList();

        await scrollBatchProcessor(scrollBatch);
    }

    // Continue scrolling - write each batch immediately
    while (!string.IsNullOrEmpty(scrollId))
    {
        var scrollResponse = await _httpClient.PostAsync(
            $"{_baseUrl}/_search/scroll",
            new StringContent(JsonConvert.SerializeObject(new {
                scroll = "5m",
                scroll_id = scrollId
            }), Encoding.UTF8, "application/json"));

        var scrollResults = JObject.Parse(await scrollResponse.Content.ReadAsStringAsync());
        hits = scrollResults["hits"]?["hits"] as JArray;

        if (hits == null || hits.Count == 0) break;

        var scrollBatch = hits.Select(hit => (
            id: hit["_id"]?.ToString() ?? "",
            source: hit["_source"] as JObject
        )).Where(x => x.source != null).ToList();

        // Write THIS batch to parquet, then clear and GC
        await scrollBatchProcessor(scrollBatch);

        scrollId = scrollResults["_scroll_id"]?.ToString();
    }
}

// Usage: Write each scroll batch to parquet immediately
await elasticsearch.DownloadIndexStreamingWithCallbackAsync(index, async (scrollBatch) =>
{
    var processedBatch = ProcessBatch(scrollBatch, columns, hashService);
    await AppendBatchToParquetAsync(processedBatch, parquetPath, columns, isFirstBatch);
    isFirstBatch = false;

    processedBatch.Clear();
    GC.Collect();
    GC.WaitForPendingFinalizers();
});
```

**Key Benefits**:
- Memory stays **constant** (~50-100MB) regardless of index size
- No accumulation of millions of documents in RAM
- Write happens immediately as data arrives
- Handles multi-GB indexes easily

**When to Use**: Always prefer this for large external data sources (Elasticsearch, APIs, large DB queries)

## Schema Handling (Working Code)

### BPQuery: Dynamic Schema Creation
```csharp
private static ParquetSchema CreateSchemaFromDataTable(DataTable dataTable)
{
    var fields = new List<DataField>();

    foreach (DataColumn column in dataTable.Columns)
    {
        var field = column.DataType.Name switch
        {
            "String" => new DataField(column.ColumnName, typeof(string)),
            "Int32" => new DataField(column.ColumnName, typeof(int)),
            "Int64" => new DataField(column.ColumnName, typeof(long)),
            "Double" => new DataField(column.ColumnName, typeof(double)),
            "Decimal" => new DataField(column.ColumnName, typeof(double)), // Convert to double
            "Boolean" => new DataField(column.ColumnName, typeof(bool)),
            "DateTime" => new DataField(column.ColumnName, typeof(DateTimeOffset)),
            _ => new DataField(column.ColumnName, typeof(string)) // Fallback
        };
        fields.Add(field);
    }

    return new ParquetSchema(fields);
}
```

### ElastiCompare: Dynamic Primary Key Schema
```csharp
var fields = new List<DataField>
{
    new("primary_key_hash", typeof(string)),
    new("document_hash", typeof(string)),
    new("has_valid_primary_keys", typeof(bool))
};

// Add primary key fields dynamically
foreach (var key in primaryKeys)
{
    fields.Add(new DataField($"pk_{key}", typeof(string)));
}
fields.Add(new DataField("raw_document", typeof(string)));

var schema = new ParquetSchema(fields);
```

## Memory Management (Proven Techniques)

### Batch Sizes That Work
- **BPQuery**: 50,000 records (MySQL sync)
- **ElastiCompare**: 10,000 records (Elasticsearch downloads)
- **Rule**: Reduce batch size for wider records (more columns)

### Aggressive Memory Management (ElastiCompare)
```csharp
// After each batch
processedBatch.Clear();
GC.Collect();
GC.WaitForPendingFinalizers();

// Monitor memory during processing
var beforeMemory = GC.GetTotalMemory(false);
// ... process batch ...
var afterMemory = GC.GetTotalMemory(false);
logger.LogInformation($"Memory: {beforeMemory / 1024 / 1024} MB -> {afterMemory / 1024 / 1024} MB");
```

## Incremental Updates (BPQuery Pattern)

### Timestamp-Based Sync with Deduplication
```csharp
public async Task UpdateSingleParquetWithNewEventsAsync(string parquetPath)
{
    // Get max timestamp from existing parquet file
    var maxEventTime = await GetMaxEventTimeFromParquet(parquetPath);

    // 10-second safety buffer for lagging writes
    var safeMaxTime = maxEventTime?.Value - 10000;

    // Get new events from MySQL
    var newEvents = await GetKeycloakEventsAfterEventTimeAsync(safeMaxTime, 50000);

    if (newEvents.Rows.Count == 0) return;

    // Get existing IDs for deduplication
    var existingIds = await GetExistingIdsFromParquet(parquetPath);
    var existingIdSet = new HashSet<string>(existingIds);

    // Filter out duplicates
    var filteredRows = newEvents.AsEnumerable()
        .Where(row => !existingIdSet.Contains(row["ID"].ToString()))
        .CopyToDataTable();

    if (filteredRows.Rows.Count > 0)
    {
        await AppendDataTableToParquet(filteredRows, parquetPath);
    }
}
```

### Safe Parquet Append
```csharp
public static async Task AppendDataTableToParquet(DataTable dataTable, string filePath)
{
    var schema = CreateSchemaFromDataTable(dataTable);

    // IMPORTANT: Use FileAccess.ReadWrite when appending because ParquetWriter needs to
    // read existing file metadata to validate schema compatibility
    using var fileStream = new FileStream(filePath, FileMode.Open, FileAccess.ReadWrite);

    using var parquetWriter = await ParquetWriter.CreateAsync(schema, fileStream, append: true);
    using var groupWriter = parquetWriter.CreateRowGroup();

    // Convert DataTable columns to Parquet columns
    foreach (DataColumn column in dataTable.Columns)
    {
        var values = ConvertToTypedArray(dataTable, column);
        var dataColumn = new ParquetDataColumn(schema[column.ColumnName], values);
        await groupWriter.WriteColumnAsync(dataColumn);
    }
}
```

## Multi-Threading Patterns (ElastiCompare)

### Parallel Download with ConcurrentBag
```csharp
private readonly ConcurrentBag<string> _primaryKeyHashes = new();
private readonly ConcurrentBag<string> _documentHashes = new();
private readonly ConcurrentBag<bool> _hasValidPrimaryKeys = new();

// N-way parallel downloads (CPU core count)
var tasks = new List<Task>();
for (int slice = 0; slice < Environment.ProcessorCount; slice++)
{
    tasks.Add(DownloadSliceAsync(slice, Environment.ProcessorCount));
}

await Task.WhenAll(tasks);
```

### Thread-Safe File Writing with SemaphoreSlim
```csharp
private readonly SemaphoreSlim _writeLock = new(1, 1);

public async Task WriteToParquetAsync(List<DocumentData> documents)
{
    await _writeLock.WaitAsync();
    try
    {
        using var fileStream = new FileStream(filePath, FileMode.Append);
        // ... write operations
    }
    finally
    {
        _writeLock.Release();
    }
}
```

## What Actually Works

### Proven Batch Sizes
- **BPQuery**: 50,000 records (MySQL, single thread)
- **ElastiCompare**: 10,000 records (Elasticsearch, multi-thread)
- **Memory consideration**: Monitor actual MB usage, not just row count

### Libraries Actually Used
- **Parquet.Net 4.23.5 - 4.25.0**: Primary parquet operations
- **Microsoft.Data.Analysis**: Data manipulation in BPQuery
- **MySql.Data**: MySQL connectivity

### What to Avoid
1. **Temporary batch files**: Unnecessary complexity - write directly to target file with proper locking
2. **Parallel MySQL queries**: Connection pool issues
3. **Large batch sizes**: >50k records can cause OOM
4. **Ignoring GC**: Must force garbage collection with large datasets

### Connection Patterns That Work
```csharp
// BPQuery: Simple using pattern
using var connection = new MySqlConnection(connectionString);
using var command = new MySqlCommand(sql, connection);
using var reader = command.ExecuteReader();

// ElastiCompare: HTTP client reuse
private static readonly HttpClient _httpClient = new();
```

