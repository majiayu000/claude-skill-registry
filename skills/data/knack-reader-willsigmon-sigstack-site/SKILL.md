---
name: Knack Reader
description: REST-based access to Knack Objects and Views for data extraction and transformation. Primary skill for reading HTI operational data from Knack data...
allowed-tools: Read
---

# Knack Reader

## Purpose
REST-based access to Knack Objects and Views for data extraction and transformation. Primary skill for reading HTI operational data from Knack database.

## Core Functions

### get_records
**Endpoint**: `GET /v1/objects/{object_key}/records`

**Parameters**:
- `object_key` (string, required): Knack object identifier (e.g., "object_1", "object_5")
- `rows_per_page` (integer, optional): Number of records per page (default: 1000, max: 1000)
- `page` (integer, optional): Page number to retrieve (default: 1)
- `filters` (object, optional): Filter criteria (see knack_filter_sort skill)
- `sort` (object, optional): Sort configuration (see knack_filter_sort skill)

**Headers Required**:
- `X-Knack-Application-Id`: HTI Knack application ID
- `X-Knack-REST-API-Key`: API key for authentication

**Example Usage**:
```javascript
const laptops = await get_records({
  object_key: "object_1",
  params: {
    rows_per_page: 1000,
    page: 1
  }
});
```

**Response Format**:
```json
{
  "records": [...],
  "total_pages": 5,
  "current_page": 1,
  "total_records": 4327
}
```

### get_view_records
**Endpoint**: `GET /v1/pages/{scene_id}/views/{view_id}/records`

**Parameters**:
- `scene_id` (string, required): Knack scene/page identifier
- `view_id` (string, required): Knack view identifier
- `user_token` (string, optional): For user-specific data

**Use Case**: Retrieve data formatted according to view-level rules (calculated fields, display rules, permissions).

**Example Usage**:
```javascript
const dashboardData = await get_view_records({
  scene_id: "scene_12",
  view_id: "view_45"
});
```

## HTI-Specific Objects

### Common Object Keys
- **Laptop Inventory**: Primary device tracking
- **Donations**: Donor organization records
- **Training Sessions**: Digital literacy event tracking
- **Counties**: Geographic distribution data

## Best Practices

1. **Always use pagination** for datasets >1000 records (see knack_pagination skill)
2. **Cache results** for frequently accessed data (see knack_cache_optimizer skill)
3. **Use filters** to reduce payload size when possible
4. **Respect rate limits**: 10 requests/second maximum

## Integration Points

- **knack_pagination**: For retrieving full datasets
- **knack_filter_sort**: For query optimization
- **knack_cache_optimizer**: For performance
- **knack_data_cleaner**: For post-retrieval validation

## Error Handling

Common errors:
- `401 Unauthorized`: Check API credentials
- `404 Not Found`: Verify object_key/view_id
- `429 Too Many Requests`: Rate limit exceeded (use cache_optimizer)
- `500 Internal Server Error`: Retry with exponential backoff

## Grant Reporting Use
Essential for quarterly reports:
- Acquired laptops count
- Converted/ready devices
- Discarded/recycled units
- Training session attendance
