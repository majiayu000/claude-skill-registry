---
name: API Pagination Debugging
description: "Systematic methodology for debugging pagination issues in API integrations, especially when switching between API versions or endpoints. Auto-activates when pagination stops early, returns duplicate results, or fails to iterate through complete datasets. Covers cursor-based vs page-based pagination, API response structure verification, and efficiency optimization. Trigger keywords: pagination bug, API not paginating, stuck at one page, cursor pagination, nextPageCursor, page-based pagination. (project)"
---

# API Pagination Debugging

> **Purpose**: Systematically diagnose and fix pagination failures that prevent complete data import from APIs

## Core Principles

### 1. Verify API Response Structure Before Assuming

Never assume pagination fields based on documentation or other endpoints. Always test actual responses:
```bash
curl -s API_ENDPOINT | jq 'keys'
```

Different API versions or endpoints may use different pagination patterns even within the same service.

### 2. Match Pagination Logic to API Design

APIs use distinct pagination patterns that require different implementations:
- **Cursor-based**: `{nextPageCursor, results}` - use cursor param
- **Page-based**: `{page, total_pages, results}` - use page number param
- **Offset-based**: `{offset, limit, total}` - use offset/limit params
- **Link-based**: `{next, previous, results}` - follow next URL

Using the wrong pattern causes pagination to stop after first page.

### 3. Optimize Page Size for Efficiency

Most APIs support configurable page sizes (e.g., 50-1000 items per page). Using maximum page_size:
- Reduces total API calls (20x fewer calls with 1000 vs 50)
- Decreases network overhead
- Minimizes rate limit exposure
- Speeds up bulk imports

### 4. Test Pagination Flow Before Implementation

Before implementing pagination logic:
1. Fetch page 1 and inspect response structure
2. Manually fetch page 2 to confirm field values
3. Verify cursor/page advancement works correctly
4. Check termination condition (null cursor, empty results, etc.)

## Systematic Debugging Workflow

### Step 1: Reproduce the Issue

**Symptoms of pagination failure:**
- Import stops after exactly 1 page
- Returns same results repeatedly
- Status shows "completed_all_pages" but dataset incomplete
- Missing data compared to known totals

**Example:**
```
Expected: 74,386 highlights
Actual: 463 files (< 1% of total)
Status: "completed_all_pages" after 1 page
```

### Step 2: Inspect Actual API Response

**Don't trust assumptions - verify response structure:**

```bash
# Fetch first page and check structure
curl -s -H "Authorization: Token $TOKEN" \
  "https://api.example.com/endpoint?page_size=50" | jq 'keys'

# Expected output reveals actual fields:
# ["count", "nextPageCursor", "results"]
# NOT ["count", "next", "previous", "results"]
```

**Critical checks:**
- [ ] What pagination fields exist?
- [ ] What are field names exactly? (case-sensitive)
- [ ] Are there any cursor/token fields?
- [ ] How does the API signal "no more pages"?

### Step 3: Compare Expected vs Actual Fields

**Common mismatches:**

| Expected (Wrong) | Actual (Correct) | Impact |
|-----------------|------------------|---------|
| `next` | `nextPageCursor` | Stops after page 1 |
| `page` parameter | `pageCursor` parameter | Repeats page 1 |
| Page number increment | Cursor advancement | Never progresses |
| `has_more` boolean | `null` cursor | Wrong termination check |

### Step 4: Test Second Page Manually

**Verify pagination actually works:**

```bash
# Get page 1
PAGE1=$(curl -s -H "Authorization: Token $TOKEN" \
  "https://api.example.com/endpoint?page_size=50")

# Extract cursor
CURSOR=$(echo $PAGE1 | jq -r '.nextPageCursor')

# Get page 2 using cursor
curl -s -H "Authorization: Token $TOKEN" \
  "https://api.example.com/endpoint?page_size=50&pageCursor=$CURSOR" \
  | jq '{count, nextPageCursor, results_count: (.results | length)}'
```

**Expected results:**
- Different `results` array contents
- New `nextPageCursor` value (or null if last page)
- Progress toward completion

### Step 5: Fix Pagination Logic

**Update implementation to match API design:**

#### For Cursor-Based Pagination

```python
# Initialize
cursor = None
page_num = 0

while True:
    page_num += 1

    # Build params
    params = {"page_size": 1000}  # Use maximum
    if cursor:
        params["pageCursor"] = cursor  # Use correct param name

    # Fetch page
    response = fetch_api(endpoint, params)
    results = response.get("results", [])

    if not results:
        break  # Empty results = done

    # Process results
    for item in results:
        process(item)

    # Get next cursor
    next_cursor = response.get("nextPageCursor")  # Use correct field name
    if not next_cursor:
        break  # No more pages

    cursor = next_cursor  # Advance cursor
```

#### For Page-Based Pagination

```python
# Initialize
page_num = 1

while True:
    # Build params
    params = {"page": page_num, "page_size": 1000}

    # Fetch page
    response = fetch_api(endpoint, params)
    results = response.get("results", [])

    if not results:
        break

    # Process results
    for item in results:
        process(item)

    # Check if more pages exist
    if not response.get("next"):  # Or check page_num < total_pages
        break

    page_num += 1  # Increment page number
```

### Step 6: Verify Fix with Logging

Add debug logging to confirm pagination works:

```python
logger.info(f"Page {page_num}: {len(results)} items, cursor={cursor}, next={next_cursor}")
```

**Expected log output:**
```
Page 1: 1000 items, cursor=None, next=55771679
Page 2: 1000 items, cursor=55771679, next=55114962
Page 3: 1000 items, cursor=55114962, next=54503291
...
Page 75: 386 items, cursor=12847563, next=null
```

### Step 7: Optimize Page Size

**Before optimization:**
```python
params = {"page_size": 50}  # Small pages
# Result: 1,488 pages needed for 74,386 items
```

**After optimization:**
```python
params = {"page_size": 1000}  # Maximum supported
# Result: 75 pages needed for 74,386 items
# Improvement: 20x fewer API calls
```

**Check API documentation for:**
- Maximum page_size allowed
- Rate limits (larger pages = fewer calls)
- Response time vs page size tradeoffs

## ✅ REQUIRED Patterns

**DO: Test actual API responses before implementing**

Never rely on documentation alone. Always curl the endpoint and inspect response structure:
```bash
curl -s API_ENDPOINT | jq '.'
```

**DO: Use maximum page_size supported by API**

Default page sizes are often inefficient (50-100 items). Check API limits and use maximum:
```python
# Efficient
params = {"page_size": 1000}

# Inefficient
params = {"page_size": 50}  # 20x more API calls
```

**DO: Match parameter names exactly**

API field names are case-sensitive and specific:
```python
# CORRECT
params["pageCursor"] = cursor

# WRONG (will not work)
params["page_cursor"] = cursor  # Snake case instead of camelCase
params["cursor"] = cursor        # Missing "page" prefix
```

**DO: Add pagination logging for diagnosis**

Always log pagination progress:
```python
logger.info(f"Page {page}: {len(results)} items, next={next_cursor}")
```

**DO: Verify termination conditions**

Check both conditions to prevent infinite loops:
```python
# Check empty results
if not results:
    break

# AND check next cursor/page
if not next_cursor:  # or not has_more, or page >= total_pages
    break
```

## ❌ FORBIDDEN Patterns

**DON'T: Assume pagination pattern from other endpoints**

Different endpoints in same API may use different pagination:
```python
# WRONG: Assume v2 uses same pagination as v3
# v3 endpoint uses page numbers
# v2 endpoint uses cursors
```

**DON'T: Check wrong field for continuation**

```python
# WRONG
if not data.get("next"):  # Field doesn't exist
    break

# RIGHT
if not data.get("nextPageCursor"):  # Actual field name
    break
```

**DON'T: Use inefficient page sizes**

```python
# WRONG: Causes 20x more API calls
params = {"page_size": 50}

# RIGHT: Minimizes API calls
params = {"page_size": 1000}
```

**DON'T: Increment page numbers for cursor-based APIs**

```python
# WRONG: Page number ignored for cursor-based pagination
page_num = 1
while True:
    params = {"page": page_num}  # Repeats page 1 forever
    page_num += 1

# RIGHT: Use cursor advancement
cursor = None
while True:
    params = {"pageCursor": cursor} if cursor else {}
    cursor = response.get("nextPageCursor")
```

**DON'T: Skip manual testing before implementation**

```python
# WRONG: Implement without verifying
# Assume API uses page numbers, implement pagination
# Deploy and discover it uses cursors

# RIGHT: Test first
# curl endpoint | jq 'keys'
# Verify field names
# Test page 2 manually
# Then implement
```

## Quick Decision Tree

### Is pagination working?

**NO - stops after 1 page:**
1. Check actual API response structure (curl + jq)
2. Compare field names (case-sensitive)
3. Verify parameter names match API expectations
4. Test page 2 manually

**NO - returns duplicates:**
1. Check if using page number instead of cursor
2. Verify cursor is advancing
3. Check if parameter name is correct

**YES - but slow:**
1. Check page_size value
2. Increase to maximum supported
3. Balance with rate limits

### Which pagination pattern to use?

**API returns `nextPageCursor` field:**
→ Use cursor-based pagination with `pageCursor` parameter

**API returns `next` URL:**
→ Follow link-based pagination (use next URL directly)

**API returns `page` and `total_pages`:**
→ Use page-based pagination with `page` parameter

**API returns `offset` and `total`:**
→ Use offset-based pagination with `offset` and `limit` parameters

## Common Mistakes

### Mistake 1: Checking Non-Existent Field

**Problem:**
```python
if not data.get("next"):  # Field doesn't exist in response
    break
```

**Solution:**
```bash
# First, check actual response
curl API | jq 'keys'
# Output: ["count", "nextPageCursor", "results"]

# Then use correct field
if not data.get("nextPageCursor"):
    break
```

### Mistake 2: Using Wrong Parameter Name

**Problem:**
```python
params["page"] = page_num  # API doesn't use page numbers
```

**Solution:**
```python
# Cursor-based APIs require cursor parameter
params["pageCursor"] = cursor  # Not "page"
```

### Mistake 3: Small Page Size

**Problem:**
```python
params = {"page_size": 50}
# 74,386 items ÷ 50 = 1,488 API calls
```

**Solution:**
```python
params = {"page_size": 1000}  # Use maximum
# 74,386 items ÷ 1000 = 75 API calls
# 20x improvement
```

## Examples

### Example 1: Readwise API Pagination Bug (January 2026)

**Context:**
- Readwise MCP server stuck importing 463 highlights instead of 74,386
- Status: "completed_all_pages" after 1 page
- Using v2 export API endpoint

**❌ WRONG - Assumed page-based pagination**

```python
# Incorrect implementation
page_num = 1
while page_num < 1000:
    params = {"page": page_num, "page_size": 50}
    data = fetch_api("/export/", params, api_version="v2")

    # Wrong field check
    if not data.get("next"):  # This field doesn't exist
        break

    page_num += 1  # Never executed because break on page 1
```

**Problem:** API uses cursor-based pagination, not page numbers. Field is `nextPageCursor` not `next`.

**✅ RIGHT - Cursor-based pagination with correct fields**

```python
# Correct implementation
cursor = None
page_num = 0

while page_num < 1000:
    page_num += 1

    # Use cursor parameter
    params = {"page_size": 1000}  # Increased from 50
    if cursor:
        params["pageCursor"] = cursor  # Correct parameter name

    data = fetch_api("/export/", params, api_version="v2")
    results = data.get("results", [])

    if not results:
        break

    # Process results...

    # Use correct field name
    next_cursor = data.get("nextPageCursor")  # Not "next"
    if not next_cursor:
        break

    cursor = next_cursor  # Advance cursor
```

**Result:**
- Before: 1 page, 463 highlights (< 1%)
- After: 75 pages, 74,386 highlights (100%)
- Efficiency: 20x fewer API calls (1000 vs 50 page_size)

### Example 2: Debugging Unknown API Pagination

**Context:**
- New API integration
- Documentation unclear about pagination
- Need to import complete dataset

**Step-by-step debugging:**

```bash
# Step 1: Test API response structure
curl -s -H "Authorization: Token $TOKEN" \
  "https://api.example.com/data?limit=10" | jq 'keys'

# Output: ["data", "pagination"]

# Step 2: Inspect pagination object
curl -s -H "Authorization: Token $TOKEN" \
  "https://api.example.com/data?limit=10" | jq '.pagination'

# Output:
# {
#   "total": 5000,
#   "offset": 0,
#   "limit": 10,
#   "has_more": true
# }

# Step 3: Test offset advancement
curl -s -H "Authorization: Token $TOKEN" \
  "https://api.example.com/data?limit=10&offset=10" | jq '.pagination'

# Output:
# {
#   "total": 5000,
#   "offset": 10,
#   "limit": 10,
#   "has_more": true
# }
```

**Implementation:**

```python
# Offset-based pagination identified
offset = 0
limit = 100  # Use larger limit

while True:
    params = {"limit": limit, "offset": offset}
    response = fetch_api("/data", params)

    items = response.get("data", [])
    if not items:
        break

    # Process items...

    pagination = response.get("pagination", {})
    if not pagination.get("has_more"):
        break

    offset += limit  # Advance offset
```

## When to Use This Skill

This skill auto-activates when:
- Pagination stops after exactly 1 page despite more data existing
- Import status shows "completed_all_pages" but dataset incomplete
- API integration returns duplicate results repeatedly
- Implementing pagination for new API endpoint
- User mentions "pagination bug", "stuck at one page", or "not paginating"
- Debugging issues with cursor-based, page-based, or offset-based pagination
- Converting between pagination patterns (e.g., page numbers to cursors)
- Optimizing API call efficiency with page_size tuning

**Don't use when:**
- Pagination works correctly (complete dataset imported)
- API returns proper error messages (different debugging needed)
- Rate limiting is the issue (needs rate limit handling, not pagination fixes)
- Authentication problems (verify auth before debugging pagination)

## Integration

**Related Skills:**
- [Python Filename Sanitization Fallback](/.claude/skills/python-filename-sanitization-fallback/SKILL.md) - Related Readwise MCP pattern from same project
- [API Endpoint Metadata Verification](/.claude/skills/api-endpoint-metadata-verification/SKILL.md) - Systematic debugging for missing API metadata

**Related Commands:**
- `/readwise-import` - Primary user of this debugging methodology

**Related Vault Documents:**
- [[0 Projects/2026 Draft Articles/Readwise Highlights Import Draft]] - Documented implementation of highlights import with pagination
- [[Readwise MCP Server Implementation]] (if exists) - Technical documentation

**Technical Context:**
- MCP server: `/Users/ngpestelos/src/readwise-mcp-server/server.py`
- State file: `.claude/state/readwise-import.json`
- Readwise API docs: https://readwise.io/api_deets

## Key Takeaway

API pagination failures usually stem from field name mismatches or wrong pagination pattern assumptions. Always verify actual API response structure with curl/jq before implementing pagination logic, use maximum page_size for efficiency, and test page 2 manually to confirm advancement works. The pattern is: inspect response → identify pagination type → match implementation → optimize page size → verify with logging.

---

*Discovered January 30, 2026 during Readwise highlights backfill debugging*
*Bug fix reduced 74,386 highlights import from theoretical 1,488 pages to actual 75 pages*
*Pattern applies to any cursor-based, page-based, or offset-based pagination implementation*
