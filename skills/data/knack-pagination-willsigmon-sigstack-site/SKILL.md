---
name: Knack Pagination
description: Manages full data retrieval while respecting Knack's 1,000-record-per-page limit. Essential for HTI's 3,500+ laptop inventory and compliance report...
allowed-tools: Read
---

# Knack Pagination

## Purpose
Manages full data retrieval while respecting Knack's 1,000-record-per-page limit. Essential for HTI's 3,500+ laptop inventory and compliance reporting.

## Core Constraint
**Knack API Limit**: Maximum 1,000 records per request

## Core Functions

### fetch_all_pages
**Purpose**: Retrieve complete dataset across multiple pages

**Parameters**:
- `object_key` (string, required): Target Knack object
- `rows_per_page` (integer, optional): Records per page (default: 1000)
- `filters` (object, optional): Apply consistent filters across all pages
- `sort` (object, optional): Maintain sort order across pages

**Logic**:
```javascript
async function fetch_all_pages(object_key, rows_per_page = 1000) {
  let all_records = [];
  let current_page = 1;
  let total_pages = null;

  while (total_pages === null || current_page <= total_pages) {
    const response = await get_records({
      object_key,
      params: { rows_per_page, page: current_page }
    });

    all_records = all_records.concat(response.records);
    total_pages = response.total_pages;
    current_page++;

    // Rate limit protection
    await sleep(100); // 10 requests/second max
  }

  return all_records;
}
```

**Example**:
```javascript
// Retrieve all 3,500+ laptops
const all_laptops = await fetch_all_pages("object_1");
console.log(`Retrieved ${all_laptops.length} total laptops`);
```

### paginate_with_progress
**Purpose**: Show progress for large dataset retrieval

**Example**:
```javascript
const laptops = await paginate_with_progress({
  object_key: "object_1",
  on_page: (page, total) => {
    console.log(`Fetching page ${page} of ${total}...`);
  }
});
```

### stream_records
**Purpose**: Memory-efficient processing for very large datasets

**Use Case**: Processing 3,500+ laptops without loading all into memory

**Example**:
```javascript
await stream_records({
  object_key: "object_1",
  process_batch: (batch) => {
    // Process 1,000 records at a time
    const ready_count = batch.filter(l => l.status === "Ready").length;
    console.log(`Batch ready count: ${ready_count}`);
  }
});
```

## Performance Optimization

### 1. Parallel Page Fetching
**Caution**: Respect 10 req/sec rate limit

```javascript
// Fetch pages 1-5 in parallel (with rate limiting)
const pages = await Promise.all([
  get_records({ object_key: "object_1", params: { page: 1 }}),
  get_records({ object_key: "object_1", params: { page: 2 }}),
  get_records({ object_key: "object_1", params: { page: 3 }}),
  get_records({ object_key: "object_1", params: { page: 4 }}),
  get_records({ object_key: "object_1", params: { page: 5 }})
]);
```

### 2. Incremental Pagination
**Use**: Dashboards showing "last 100 records"

```javascript
// Only fetch first page for dashboard preview
const recent = await get_records({
  object_key: "object_1",
  params: { rows_per_page: 100, page: 1 }
});
```

## HTI-Specific Use Cases

### Quarterly Report Generation
```javascript
// All laptops acquired in Q1 2025
const q1_laptops = await fetch_all_pages("object_1", {
  filters: {
    field: "acquisition_date",
    operator: "is during",
    range: { start: "2025-01-01", end: "2025-03-31" }
  }
});
```

### County-Level Breakdown
```javascript
// Paginate through all devices, group by county
const all_devices = await fetch_all_pages("object_1");
const by_county = groupBy(all_devices, "target_county");
```

### Donor Analysis
```javascript
// All donations from last 12 months
const donations = await fetch_all_pages("object_2", {
  filters: {
    field: "donation_date",
    operator: "is after",
    value: "2024-01-01"
  }
});
```

## Rate Limit Handling

```javascript
async function fetch_with_rate_limit(object_key) {
  const delay = 100; // 10 req/sec = 100ms between requests

  for (let page = 1; page <= total_pages; page++) {
    await sleep(delay);
    const data = await get_records({ object_key, params: { page }});
    // Process data...
  }
}
```

## Error Recovery

```javascript
async function fetch_all_with_retry(object_key, max_retries = 3) {
  let retries = 0;

  while (retries < max_retries) {
    try {
      return await fetch_all_pages(object_key);
    } catch (error) {
      if (error.status === 429) {
        // Rate limit - wait and retry
        await sleep(1000 * Math.pow(2, retries));
        retries++;
      } else {
        throw error;
      }
    }
  }
}
```

## Integration Points

- **knack_reader**: Provides base get_records function
- **knack_cache_optimizer**: Cache paginated results to avoid re-fetching
- **knack_filter_sort**: Apply consistent filters across pages
- **knack_reporting_sync**: Full dataset retrieval for quarterly reports

## Best Practices

1. **Always paginate** for production datasets (assume >1000 records)
2. **Cache results** of full pagination runs (10+ API calls)
3. **Show progress** for long-running pagination (UX)
4. **Handle rate limits** with delays between requests
5. **Use streaming** for memory-constrained environments

## Grant Reporting
- Essential for accurate counts (3,500+ laptop goal)
- Ensures all records included in quarterly reports
- Prevents data truncation in NCDIT submissions
