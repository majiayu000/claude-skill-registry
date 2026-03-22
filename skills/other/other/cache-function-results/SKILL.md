---
name: cache-function-results
description: Add caching to Datagrok functions (scripts, queries, JS functions) using meta.cache annotations
---

# Cache Function Results

Help the user add caching to Datagrok functions to improve performance by storing results for repeated calls with the same inputs.

## Usage
```
/cache-function-results [function-name] [--mode <client|server|all>]
```

## Instructions

### 1. Choose the cache mode

Add `meta.cache` annotation to the function header:

- `client` — stores results in the browser's IndexedDB
- `server` — stores results on the Datagrok server
- `all` — uses both client and server caches together

### 2. Add caching to a TypeScript/JavaScript function

```typescript
//name: Get Users
//meta.cache: all
//meta.cache.invalidateOn: 0 0 * * *
//output: dataframe result
export async function getUsers(): Promise<DG.DataFrame> {
  // Expensive operation — results will be cached
}
```

### 3. Add caching to a Python/R script

```python
#name: Example
#language: python
#meta.cache: client
#meta.cache.invalidateOn: 0 * * * *
#input: string table [Data table]
#output: int result

...
```

### 4. Add caching to a SQL query

```sql
--name: ActivityDetails
--connection: Chembl
--meta.cache: all
--meta.cache.invalidateOn: 0 0 * * *
--input: string target = "CHEMBL1827"
SELECT * FROM activity_details WHERE target_id = @target
--end
```

### 5. Set cache invalidation

Use `meta.cache.invalidateOn` with a cron expression to control when cached results expire:

| Cron expression | Meaning |
|----------------|---------|
| `0 * * * *` | Every hour |
| `0 0 * * *` | Every day at midnight |
| `0 0 * * 1` | Every Monday at midnight |
| `0 0 1 * *` | First day of each month |

If `meta.cache.invalidateOn` is not specified, the cache never expires automatically.

### 6. Cache all queries under a connection

Instead of annotating each query, enable caching at the connection level:

**Via UI:** Right-click the connection > **Edit...** > check **Cache Results** and optionally fill **Invalidate On**.

**Via connection JSON:**
```json
{
  "name": "Northwind",
  "parameters": {
    "server": "db.example.com",
    "port": 5432,
    "db": "mydb",
    "cacheResults": true,
    "cacheSchema": false
  }
}
```

### 7. Client-side cache limits

- Function output must be scalar (int, float, string) or dataframe, graphics, datetime
- Maximum cache size per function: 100 MB
- Maximum record count: 100,000
- Users enable it in **Settings > Cache > Client-side cache**

### 8. Server-side cache

- No restrictions on size or parameter types
- Users enable it in **Settings > Cache > Server-side cache**
- Works together with client-side cache when mode is `all`

## Behavior

- Default to `meta.cache: all` unless the user specifies a preference.
- Always suggest adding `meta.cache.invalidateOn` with an appropriate schedule — warn that without it the cache never refreshes.
- Only recommend caching for functions that are immutable (same input produces same output).
- Warn against caching database queries when the underlying data changes frequently.
- For connection-level caching, mention that it applies to all queries under that connection.
