---
name: hubspot-nango-integration
description: Use when writing HubSpot integration code in Nango - HubSpot-specific guidance on Search API for incremental syncs, property name variations, rate limits, and OAuth introspection
---

# HubSpot Integration Specialist for Nango

Use this skill when writing, reviewing, or troubleshooting **HubSpot-specific** aspects of Nango integrations.

**Focus:** This skill covers HubSpot API quirks, not general Nango patterns.

## Critical HubSpot API Knowledge

### Incremental Syncs: Search API is Required

**IMPORTANT:** HubSpot incremental syncs can ONLY be achieved via the Search API endpoint.

**Why:** Only the Search API supports filtering by `hs_lastmodifieddate` (or `lastmodifieddate` for contacts), which is essential for incremental syncs.

**Trade-off:** The Search API has a lower rate limit than other endpoints:
- **Search API Rate Limit:** 4 requests per second per authentication token
- **Standard API Rate Limit:** 190 calls per 10 seconds (up to 250 with capacity pack)

**Implication:** When designing HubSpot integrations, you must balance:
- Incremental sync efficiency (Search API required)
- Rate limit constraints (Search API is more restrictive)

### Search API Endpoint Pattern

```typescript
// POST /crm/v3/objects/{object_type}/search
// Examples:
// POST /crm/v3/objects/contacts/search
// POST /crm/v3/objects/companies/search
// POST /crm/v3/objects/deals/search
```

### Filtering by Last Modified Date

**Property Name Varies by Object:**
- **Contacts:** Use `lastmodifieddate` (not `hs_lastmodifieddate`)
- **Companies, Deals, Tasks, etc.:** Use `hs_lastmodifieddate`

**Date Format:** UNIX timestamp in milliseconds

**Example Request Body:**

```json
{
  "filterGroups": [{
    "filters": [{
      "propertyName": "hs_lastmodifieddate",
      "operator": "GTE",
      "value": "1579514400000"
    }]
  }],
  "properties": ["id", "name", "hs_lastmodifieddate"],
  "limit": 100,
  "after": "cursor_token_here"
}
```

**Supported Operators:**
- `GTE` (greater than or equal)
- `GT` (greater than)
- `LTE` (less than or equal)
- `LT` (less than)
- `BETWEEN` (requires both `value` and `highValue`)

### Search API Limitations

- **Maximum Results:** 10,000 total results per search
- **Maximum Filter Groups:** 5
- **Maximum Filters Total:** 25 in a single query
- **Maximum Filters per Group:** 10

### OAuth Token Introspection Endpoints

HubSpot provides OAuth token introspection endpoints to validate tokens and retrieve associated user/account information:

**Endpoints:**
- **Access Tokens:** `/oauth/v1/access-tokens/:token`
- **Refresh Tokens:** `/oauth/v1/refresh-tokens/:token`

**Use Cases:**
- Validate OAuth tokens programmatically
- Retrieve user_id associated with a token
- Check token expiration and scopes
- Gather account metadata for debugging

**Example Usage in Nango:**
```typescript
// Validate and inspect refresh token
const response = await nango.get({
  endpoint: `/oauth/v1/refresh-tokens/${refreshToken}`,
  baseUrlOverride: 'https://api.hubapi.com'
});

const { user_id, hub_id, scopes } = response.data;
```

## Schema Introspection Pattern

HubSpot provides powerful schema introspection endpoints that allow you to discover:
- Custom object definitions
- Standard object properties (including custom fields)
- Associations between objects
- Field types and configurations

**This is critical for building flexible integrations that adapt to customer-specific customizations.**

### Schema Introspection Endpoints

**1. List All Schemas (Custom + Standard):**
```typescript
GET /crm-object-schemas/v3/schemas
```
Returns all custom object schemas. Each schema includes properties, associations, and metadata.

**2. Get Specific Object Schema:**
```typescript
GET /crm-object-schemas/v3/schemas/{objectTypeId}
```
Returns detailed schema for a specific object (works for both custom and standard objects).

**Required Scope:** `crm.schemas.custom.read`

### Schema Response Structure

```typescript
interface HubSpotSchemaResult {
  id: string                        // Object type ID (e.g., "0-1" for Contact)
  name: string                      // Object name
  objectTypeId: string              // Same as id
  primaryDisplayProperty: string    // Which property to use as display name
  properties: HubSpotProperty[]     // All properties including custom fields
  associations: HubSpotAssociation[] // All associations
}

interface HubSpotProperty {
  name: string              // Property ID (e.g., "firstname", "custom_field_1")
  label: string             // Display label
  type: string              // HubSpot type (string, number, date, enumeration, etc.)
  fieldType: string         // Field type (text, textarea, select, etc.)
  options?: Array<{         // For enumeration/select fields
    label: string
    value: string
  }>
}

interface HubSpotAssociation {
  id: string                // Association ID
  name: string              // Association name
  fromObjectTypeId: string  // Source object
  toObjectTypeId: string    // Target object
}
```

### Conceptual Pattern: Two-Phase Sync

Advanced HubSpot integrations use a **two-phase sync pattern**:

**Phase 1: Schema Sync** - Discover structure
- Fetch all schemas via introspection endpoints
- Identify custom objects and standard objects
- Map field types and associations
- Cache schema information in metadata

**Phase 2: Records Sync** - Fetch data
- Use cached schema to know which properties exist
- Dynamically build property lists based on schema
- Handle associations discovered in schema phase
- Adapt to customer-specific customizations without code changes

### Why This Matters

**Without Introspection:**
```typescript
// Hardcoded - breaks if customer adds custom fields
const properties = ['firstname', 'lastname', 'email'];
```

**With Introspection:**
```typescript
// Dynamic - adapts to customer's schema
const schema = await getSchema(nango, objectId);
const properties = schema.properties.map(p => p.name);
// Includes all custom fields automatically!
```

### HubSpot Object Type IDs

**Standard Objects** have numeric IDs:
- `0-1` - Contact
- `0-2` - Company
- `0-3` - Deal
- `0-5` - Ticket
- `0-7` - Product
- `0-8` - Line Item
- `0-136` - Lead
- `owner` - Owner (special case)

**Custom Objects** have different ID formats (provided by HubSpot when created).

### Handling Custom Fields

**Key Insight:** HubSpot custom fields are just additional properties in the schema. They appear alongside standard fields.

**Standard Contact Fields:**
- `firstname`, `lastname`, `email` (built-in)

**Custom Contact Fields** (examples):
- `custom_field_name` (user-defined)
- `department`, `employee_id`, etc.

**All appear in the same `properties` array from schema introspection.**

```typescript
// Fetch schema for contacts
const schema = await nango.get({
  endpoint: '/crm-object-schemas/v3/schemas/0-1', // Contact
  retries: 10
});

// Properties include both standard AND custom fields
const allProperties = schema.data.properties.map(p => p.name);
// ['firstname', 'lastname', 'email', 'custom_field_1', 'department', ...]
```

### Handling Associations

HubSpot associations link objects together (e.g., Contact → Company, Deal → Contact).

**Association Types:**
- `HUBSPOT_DEFINED` - Built-in associations (Contact to Company)
- `USER_DEFINED` - Custom associations (Custom Object to Contact)

**Key Pattern:** Associations are discovered via schema introspection, then included in record fetch.

```typescript
// 1. Get associations from schema
const schema = await getSchema(nango, objectId);
const associations = schema.associations
  .filter(a => a.fromObjectTypeId === objectId)
  .map(a => a.toObjectTypeId);

// 2. Fetch records with associations
const response = await nango.get({
  endpoint: `/crm/v3/objects/${objectType}`,
  params: {
    properties: properties.join(','),
    associations: associations.join(',') // Include in request!
  }
});

// 3. Response includes associations in each record
const record = response.data.results[0];
// record.associations.companies.results = [{ id: "123" }, ...]
```

### Property Chunking Pattern

HubSpot has limits on URL length and number of properties per request. For objects with many custom fields:

**Problem:** 100+ properties can exceed URL limits

**Solution:** Chunk properties into groups, fetch multiple times, merge results

```typescript
// Split properties into chunks of 50
const chunks = chunkArray(properties, 50);

const recordMap = new Map();

for (const propertyChunk of chunks) {
  const response = await nango.get({
    endpoint: `/crm/v3/objects/contacts`,
    params: {
      properties: propertyChunk.join(','),
      after: cursor
    }
  });

  // Merge properties from multiple requests
  for (const record of response.data.results) {
    const existing = recordMap.get(record.id);
    if (existing) {
      recordMap.set(record.id, {
        ...existing,
        properties: { ...existing.properties, ...record.properties }
      });
    } else {
      recordMap.set(record.id, record);
    }
  }
}

// All properties now merged in recordMap
```

### Owner Fields Special Case

HubSpot has special "owner" fields that reference the Owner object:
- `hubspot_owner_id`
- `hs_owner_id`

**These should be treated as lookups/foreign keys to the Owner object (`owner`).**

```typescript
// When mapping fields, detect owner fields
if (['hubspot_owner_id', 'hs_owner_id'].includes(property.name)) {
  // This is a reference to Owner object, not a simple field
  field.type = 'lookup';
  field.externalLinkTargetTable = 'owner';
}
```

## HubSpot-Specific Implementation Examples

### Full Sync: Use Standard CRM Endpoints

**HubSpot Endpoint:** `/crm/v3/objects/{object}` (GET with query params)
**Rate Limit:** 190 calls per 10 seconds (up to 250 with capacity pack)

```typescript
// HubSpot-specific considerations:
const properties = [
    'firstname',      // HubSpot uses lowercase, no camelCase
    'lastname',
    'email',
    'jobtitle',
    'createdate',     // Note: 'createdate' not 'createdDate'
    'hubspot_owner_id' // HubSpot prefix for system properties
];

const config: ProxyConfiguration = {
    endpoint: '/crm/v3/objects/contacts', // Standard CRM endpoint
    params: {
        properties: properties.join(',') // HubSpot requires comma-separated string
    },
    // ... pagination config
};
```

### Incremental Sync: Must Use Search API

**HubSpot Endpoint:** `/crm/v3/objects/{object}/search` (POST with filter body)
**Rate Limit:** 4 requests per second (much lower!)
**Why Required:** Only endpoint supporting `hs_lastmodifieddate` filtering

```typescript
// HubSpot-specific: Convert lastSyncDate to UNIX timestamp in milliseconds
const lastSyncDate = nango.lastSyncDate?.toISOString().slice(0, -8).replace('T', ' ');
const queryDate = lastSyncDate ? Date.parse(lastSyncDate) : Date.now() - 86400000;

const payload = {
    endpoint: '/crm/v3/objects/tickets/search', // POST, not GET
    data: {
        sorts: [{
            propertyName: 'hs_lastmodifieddate', // HubSpot-specific property
            direction: 'DESCENDING'
        }],
        properties: TICKET_PROPERTIES, // Array, not comma-separated string
        filterGroups: [{
            filters: [{
                propertyName: 'hs_lastmodifieddate', // Key for incremental
                operator: 'GT',                       // Greater than last sync
                value: queryDate                      // UNIX ms timestamp
            }]
        }],
        limit: `${MAX_PAGE}`,
        after: afterLink // Cursor for pagination
    },
    retries: 10
};

const response = await nango.post(payload);
```

**HubSpot Pagination:** Response includes `paging.next.after` cursor token.

### Actions: Use Standard CRM Endpoints (Not Search)

**HubSpot Endpoint:** `/crm/v3/objects/{object}` (POST for create)
**Rate Limit:** 190 calls per 10 seconds (higher than Search API)

```typescript
// HubSpot requires properties wrapped in 'properties' object
const hubSpotContact = {
    properties: {
        firstname: input.firstName,
        lastname: input.lastName,
        email: input.email,
        jobtitle: input.jobTitle
    }
};

const config: ProxyConfiguration = {
    endpoint: 'crm/v3/objects/contacts', // Standard endpoint, NOT /search
    data: hubSpotContact,
    retries: 3
};

const response = await nango.post(config);
// HubSpot returns: { id, properties: {...}, createdAt, updatedAt, archived }
```

## HubSpot-Specific Considerations

### Object Type Variations

Different HubSpot objects may have different property names:
- Always check HubSpot's API documentation for the specific object
- Use the Search API with a test filter to verify property names
- Common objects: `contacts`, `companies`, `deals`, `tickets`, `products`, `line_items`

### Pagination Strategy

**Search API Pagination:**
- Uses cursor-based pagination via `after` parameter
- Returns `paging.next.after` for the next page
- Limited to 10,000 total results

**If you hit the 10,000 limit:**
- Add additional filters to narrow results
- Consider splitting by date ranges
- Process in smaller time windows

### HubSpot Rate Limits

**Standard Endpoints:** 190 calls per 10 seconds (250 with capacity pack)
**Search API:** 4 requests per second per token

**Implication:** Search API can make ~24 requests per 10 seconds vs 190 for standard endpoints.

### HubSpot Error Codes

- **400:** Invalid property name or filter syntax
- **429:** Rate limit exceeded
- **403:** Missing OAuth scopes

## HubSpot-Specific Checklist

When implementing HubSpot integrations, verify these **HubSpot-specific** requirements:

### API Endpoint Selection
- [ ] Using Search API (`/crm/v3/objects/{object}/search`) for incremental syncs ONLY
- [ ] Using standard CRM endpoints (`/crm/v3/objects/{object}`) for full syncs and actions
- [ ] Correct HTTP method: POST for Search API, GET for standard list endpoints

### HubSpot Property Names
- [ ] Correct property for last modified: `lastmodifieddate` (contacts) or `hs_lastmodifieddate` (other objects)
- [ ] Using lowercase property names (`firstname`, not `firstName`)
- [ ] Using `hubspot_owner_id` (with prefix) for owner references
- [ ] Properties as comma-separated string for standard endpoints, array for Search API

### HubSpot Data Formats
- [ ] Timestamp in milliseconds (via `Date.parse()`)
- [ ] Request body wraps properties in `properties` object for create/update
- [ ] Response includes `properties` object, not flat structure

### HubSpot Rate Limits & Pagination
- [ ] Aware of 4 req/sec limit for Search API (vs 190 per 10 sec for standard)
- [ ] Pagination via `paging.next.after` cursor (not offset-based)
- [ ] Search API limited to 10,000 results max

### Schema Introspection & Custom Fields
- [ ] Using schema introspection endpoints for flexible integrations
- [ ] Fetching schemas first to discover custom fields dynamically
- [ ] Caching schema information in metadata
- [ ] Building property lists from schema (not hardcoding)
- [ ] Property chunking for objects with many custom fields (50 properties per request)
- [ ] Merging chunked responses by record ID
- [ ] Handling associations discovered via schema
- [ ] Special treatment of owner fields (`hubspot_owner_id`, `hs_owner_id`)
- [ ] Distinguishing custom objects from standard objects via ID format
- [ ] Using `crm.schemas.custom.read` scope for schema access

## Common HubSpot-Specific Mistakes

### API Endpoint & Protocol
1. **Using standard CRM endpoints for incremental syncs** - They don't support `hs_lastmodifieddate` filtering; must use Search API
2. **Using Search API for actions** - Use standard endpoints for better rate limits
3. **Wrong HTTP method** - Search API is POST, not GET

### Property & Field Handling
4. **Hardcoding property lists** - Use schema introspection to discover custom fields dynamically
5. **Wrong property name for last modified** - Using `hs_lastmodifieddate` for contacts (should be `lastmodifieddate`)
6. **CamelCase property names** - HubSpot uses lowercase (`firstname`, not `firstName`)
7. **Missing `properties` wrapper** - Create/update requests need `{ properties: {...} }`
8. **Wrong properties format** - Comma-separated string for GET, array for Search API POST
9. **Exceeding URL length limits** - Chunk properties into groups of 50 for objects with many custom fields
10. **Not merging chunked responses** - When fetching properties in chunks, merge by record ID

### Data Format & Timestamps
11. **Date format errors** - HubSpot requires UNIX timestamp in milliseconds, not seconds

### Rate Limits & Performance
12. **Ignoring Search API rate limits** - 4 req/sec is much lower than standard 190 per 10 sec
13. **Exceeding 10,000 result limit** - Search API caps at 10k results per query

### Schema & Custom Objects
14. **Not fetching schemas before records** - Schema provides critical info about custom fields and associations
15. **Treating owner fields as simple properties** - `hubspot_owner_id` should be treated as lookup to Owner object
16. **Not handling custom object IDs** - Custom objects have different ID formats than standard objects

## When to Use This Skill

Use this skill for **HubSpot-specific** questions:
- Choosing between Search API and standard CRM endpoints
- HubSpot property name variations (`lastmodifieddate` vs `hs_lastmodifieddate`)
- HubSpot data format requirements (timestamps, property wrappers)
- HubSpot rate limits and pagination quirks
- Schema introspection for custom fields and associations
- Two-phase sync pattern (schema → records)
- Handling custom objects vs standard objects
- Property chunking for objects with many fields
- OAuth introspection endpoints
- Troubleshooting HubSpot API errors

**Do NOT use for generic Nango patterns** - focus on HubSpot API specifics only.

## HubSpot API Resources

- Schema Introspection: `https://developers.hubspot.com/docs/api/crm/properties`
- Object Schemas: `https://developers.hubspot.com/docs/guides/api/crm/using-object-apis`
- Search API: `https://developers.hubspot.com/docs/api/crm/search`
- OAuth: `https://developers.hubspot.com/docs/api/working-with-oauth`
- Rate Limits: `https://developers.hubspot.com/docs/api/usage-details`
- CRM Objects: `https://developers.hubspot.com/docs/api/crm/understanding-the-crm`
- Scopes: `https://developers.hubspot.com/docs/apps/legacy-apps/authentication/scopes`
