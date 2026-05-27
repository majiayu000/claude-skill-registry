---
name: Backward Compatibility Rules
description: Comprehensive guide to backward compatibility rules for APIs, databases, and data contracts with migration strategies and testing approaches
---

# Backward Compatibility Rules

## What is Backward Compatibility?

**Definition:** New version works with old clients without requiring changes.

### Example
```
API v1: GET /users → { id, name }
API v2: GET /users → { id, name, email }  (added field)

Old client (expects v1) calls v2 API:
→ Receives { id, name, email }
→ Ignores 'email' field
→ Works! ✅ Backward compatible
```

### Evolution Design
```
Version 1.0 → 1.1 → 1.2 → 2.0
         ↓      ↓      ↓      ↓
    Compatible Compatible Breaking
```

---

## Why Backward Compatibility Matters

### 1. Avoid Breaking Existing Integrations

**Without Backward Compatibility:**
```
Deploy new API version
→ All clients break immediately
→ Emergency rollback
→ Coordinate with all clients to update
→ Big bang migration (risky!)
```

**With Backward Compatibility:**
```
Deploy new API version
→ Old clients continue working
→ Clients migrate gradually
→ No coordination needed
```

### 2. Gradual Migration (Not Big Bang)

**Timeline:**
```
Month 0: Deploy v2 (backward compatible)
Month 1: 20% of clients migrated
Month 3: 50% of clients migrated
Month 6: 80% of clients migrated
Month 12: 100% migrated, deprecate v1
```

### 3. Reduce Coordination Overhead

**Without:**
- Coordinate deployment with all clients
- Schedule maintenance window
- Rollback plan if issues

**With:**
- Deploy anytime
- Clients migrate when ready
- No coordination needed

### 4. Customer Trust (Stable APIs)

**Trust:**
- "This API won't break my integration"
- "I can upgrade when I'm ready"
- "No surprises"

---

## Compatibility Levels

### Backward Compatible (New Server, Old Client)

**Definition:** Old client works with new server

**Example:**
```
Old client expects: { id, name }
New server returns: { id, name, email }

Client ignores 'email' → Works ✅
```

### Forward Compatible (Old Server, New Client)

**Definition:** New client works with old server

**Example:**
```
New client expects: { id, name, email? }
Old server returns: { id, name }

Client handles missing 'email' → Works ✅
```

### Full Compatible (Both Directions)

**Definition:** Works both ways

**Example:**
```
v1: { id, name }
v2: { id, name, email? }  (optional)

Old client + new server: Ignores 'email' ✅
New client + old server: Handles missing 'email' ✅
```

### Breaking Change (Incompatible)

**Definition:** Doesn't work

**Example:**
```
Old client expects: { id, name }
New server returns: { id, firstName, lastName }

Client looks for 'name' → Not found → Breaks ❌
```

---

## REST API Backward Compatibility

### Safe Changes

#### Add New Endpoint
```
Before:
GET /users

After:
GET /users
GET /projects  (new)

Compatible: ✅ Old clients don't call new endpoint
```

#### Add Optional Field to Request
```
Before:
POST /users
{ "name": "John" }

After:
POST /users
{ "name": "John", "email": "john@example.com" }  (email optional)

Compatible: ✅ Old clients don't send 'email', server handles missing field
```

#### Add Field to Response
```
Before:
GET /users → { "id": "123", "name": "John" }

After:
GET /users → { "id": "123", "name": "John", "email": "john@example.com" }

Compatible: ✅ Old clients ignore 'email'
```

#### Add Enum Value (at End)
```
Before:
status: "ACTIVE" | "INACTIVE"

After:
status: "ACTIVE" | "INACTIVE" | "PENDING"

Compatible: ✅ Old clients may not handle "PENDING", but schema is valid
```

#### Relax Validation (Accept More)
```
Before:
name: minLength 5

After:
name: minLength 1  (less strict)

Compatible: ✅ Old clients sending 5+ chars still work
```

### Breaking Changes

#### Remove Endpoint
```
Before:
GET /users

After:
(endpoint removed)

Breaking: ❌ Old clients calling endpoint get 404
```

#### Remove Field from Response
```
Before:
GET /users → { "id": "123", "name": "John" }

After:
GET /users → { "id": "123" }  ('name' removed)

Breaking: ❌ Old clients expect 'name' field
```

#### Add Required Field to Request
```
Before:
POST /users
{ "name": "John" }

After:
POST /users
{ "name": "John", "email": "john@example.com" }  (email required)

Breaking: ❌ Old clients don't send 'email', get 400 error
```

#### Change Field Type
```
Before:
age: integer

After:
age: string

Breaking: ❌ Old clients send integer, server expects string
```

#### Rename Field
```
Before:
{ "name": "John" }

After:
{ "fullName": "John" }

Breaking: ❌ Old clients look for 'name', not found
```

#### Change Semantics
```
Before:
amount: 100  (dollars)

After:
amount: 10000  (cents, changed meaning!)

Breaking: ❌ Same field, different meaning
```

---

## Database Schema Compatibility

### Safe Migrations

#### Add Nullable Column
```sql
-- Safe: Existing rows get NULL
ALTER TABLE users ADD COLUMN email VARCHAR(255);
```

#### Add Table
```sql
-- Safe: Doesn't affect existing tables
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  name VARCHAR(255)
);
```

#### Add Index
```sql
-- Safe: Improves performance, doesn't change data
CREATE INDEX idx_users_email ON users(email);
```

### Breaking Migrations

#### Drop Column (Requires Multi-Step Migration)
```sql
-- Breaking: Existing queries fail
ALTER TABLE users DROP COLUMN name;

-- Multi-step migration:
-- Step 1: Stop writing to column
-- Step 2: Deploy code that doesn't read column
-- Step 3: Drop column
```

#### Rename Column (Use Views/Aliases)
```sql
-- Breaking: Existing queries fail
ALTER TABLE users RENAME COLUMN name TO full_name;

-- Multi-step migration:
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN full_name VARCHAR(255);

-- Step 2: Copy data
UPDATE users SET full_name = name;

-- Step 3: Create view with old name
CREATE VIEW users_v1 AS
SELECT id, full_name AS name FROM users;

-- Step 4: Migrate clients to new column
-- Step 5: Drop view and old column
```

#### Change Column Type
```sql
-- Breaking: Data may not fit
ALTER TABLE users ALTER COLUMN age TYPE VARCHAR(10);

-- Multi-step migration:
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN age_str VARCHAR(10);

-- Step 2: Copy and convert data
UPDATE users SET age_str = age::VARCHAR;

-- Step 3: Migrate clients
-- Step 4: Drop old column, rename new column
```

---

## Event/Message Compatibility

### Safe Changes

#### Add Optional Field
```json
Before:
{ "id": "123", "name": "John" }

After:
{ "id": "123", "name": "John", "email": "john@example.com" }

Compatible: ✅ Old consumers ignore 'email'
```

#### Add New Event Type
```
Before:
user.created

After:
user.created
user.deleted  (new)

Compatible: ✅ Old consumers don't subscribe to new event
```

### Breaking Changes

#### Remove Field
```json
Before:
{ "id": "123", "name": "John" }

After:
{ "id": "123" }  ('name' removed)

Breaking: ❌ Old consumers expect 'name'
```

#### Change Field Type
```json
Before:
{ "age": 30 }  (integer)

After:
{ "age": "30" }  (string)

Breaking: ❌ Old consumers expect integer
```

#### Rename Field
```json
Before:
{ "name": "John" }

After:
{ "fullName": "John" }

Breaking: ❌ Old consumers look for 'name'
```

---

## GraphQL Compatibility

### Safe Changes

#### Add New Field to Type
```graphql
Before:
type User {
  id: ID!
  name: String!
}

After:
type User {
  id: ID!
  name: String!
  email: String  # New field
}

Compatible: ✅ Old queries don't request 'email'
```

#### Add New Type
```graphql
After:
type Project {
  id: ID!
  name: String!
}

Compatible: ✅ Old queries don't use new type
```

#### Add New Query/Mutation
```graphql
After:
type Query {
  users: [User!]!
  projects: [Project!]!  # New query
}

Compatible: ✅ Old clients don't call new query
```

### Breaking Changes

#### Remove Field
```graphql
Before:
type User {
  id: ID!
  name: String!
}

After:
type User {
  id: ID!
  # 'name' removed
}

Breaking: ❌ Old queries requesting 'name' fail
```

#### Change Field Type
```graphql
Before:
type User {
  age: Int!
}

After:
type User {
  age: String!  # Changed type
}

Breaking: ❌ Old queries expect Int
```

#### Change Field Arguments
```graphql
Before:
users(limit: Int): [User!]!

After:
users(limit: Int!, offset: Int!): [User!]!  # 'offset' required

Breaking: ❌ Old queries don't provide 'offset'
```

---

## Deprecation Strategy

### Mark as Deprecated

**In Docs:**
```markdown
## GET /users/:id/profile

**Deprecated:** Use GET /users/:id instead.
**Sunset Date:** 2024-12-31
```

**In Code:**
```javascript
/**
 * @deprecated Use getUser() instead. Will be removed in v2.0.0.
 */
function getUserProfile(id) {
  // ...
}
```

**In Headers:**
```
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: <https://docs.example.com/migration>; rel="deprecation"
```

### Provide Migration Guide

**Example:**
```markdown
# Migration Guide: /users/:id/profile → /users/:id

## What's Changing
The `/users/:id/profile` endpoint is deprecated. Use `/users/:id` instead.

## Why
Consolidating user endpoints for simplicity.

## How to Migrate

### Before
```javascript
const profile = await fetch('/api/users/123/profile');
```

### After
```javascript
const user = await fetch('/api/users/123');
```

## Timeline
- **2024-06-01:** Deprecation announced
- **2024-12-31:** Endpoint will stop working
```

### Set Sunset Date (6-12 Months)

**Timeline:**
```
Month 0: Announce deprecation
Month 3: Warn users (emails, headers)
Month 6: Final warning
Month 12: Sunset (stop working)
```

### Warn Clients (in Response Headers)

```
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Warning: 299 - "This endpoint is deprecated. Use /v2/users instead. See https://docs.example.com/migration"
```

### Monitor Usage

**Track Deprecated Endpoint Usage:**
```javascript
app.get('/users/:id/profile', (req, res) => {
  // Log usage
  metrics.increment('deprecated.users_profile.calls');
  
  // Return response with deprecation headers
  res.set('Deprecation', 'true');
  res.set('Sunset', 'Sat, 31 Dec 2024 23:59:59 GMT');
  res.json(profile);
});
```

**Dashboard:**
```
Deprecated Endpoint Usage:
/users/:id/profile
- Calls/day: 1,000 (down from 5,000 last month)
- Top clients: mobile-app (500), web-app (300), partner-api (200)
- Sunset date: 2024-12-31 (6 months remaining)
```

### Remove After Sunset

**Process:**
```
1. Sunset date reached
2. Return 410 Gone
3. Monitor for errors
4. After 1 month, remove code
```

**410 Gone Response:**
```
HTTP/1.1 410 Gone
Content-Type: application/json

{
  "error": "This endpoint has been removed. Use /v2/users instead.",
  "migrationGuide": "https://docs.example.com/migration"
}
```

---

## Multi-Step Migrations

### Example: Rename Field

**Step 1: Add New Field, Both Fields Populated**
```javascript
// API returns both fields
{
  "name": "John Doe",      // Old field (deprecated)
  "fullName": "John Doe"   // New field
}
```

**Step 2: Clients Migrate to New Field**
```
Month 1-3: Clients update to use 'fullName'
```

**Step 3: Stop Populating Old Field (Still Present)**
```javascript
// API returns both fields, but old field is null
{
  "name": null,            // Old field (deprecated, not populated)
  "fullName": "John Doe"   // New field
}
```

**Step 4: Remove Old Field**
```javascript
// API returns only new field
{
  "fullName": "John Doe"   // New field
}
```

---

## API Versioning Strategies

### URL Versioning (/v1/, /v2/)

**Format:**
```
/api/v1/users
/api/v2/users
```

**Pros:**
- Clear and visible
- Easy to route
- Can run multiple versions

**Cons:**
- URL changes
- Maintain multiple codebases

### Header Versioning (Accept-Version: v1)

**Format:**
```
GET /api/users
Accept-Version: v1
```

**Pros:**
- URL doesn't change
- More RESTful

**Cons:**
- Less visible
- Harder to test

### No Versioning (Only Non-Breaking Changes)

**Strategy:**
- Never make breaking changes
- Always backward compatible

**Pros:**
- Simple
- No migration

**Cons:**
- Technical debt accumulates

---

## Testing Backward Compatibility

### Contract Tests (Pact)

See Contract Testing skill for details

### Integration Tests with Old Clients

**Example:**
```javascript
describe('Backward compatibility', () => {
  test('v1 client works with v2 API', async () => {
    // v1 client expects { id, name }
    const response = await v1Client.get('/users/123');
    
    expect(response).toHaveProperty('id');
    expect(response).toHaveProperty('name');
    // v2 API may return additional fields (email), but v1 client ignores them
  });
});
```

### Schema Compatibility Checks (Automated)

**OpenAPI:**
```bash
oasdiff breaking old.yaml new.yaml
```

**JSON Schema:**
```javascript
const isCompatible = checkBackwardCompatibility(oldSchema, newSchema);
if (!isCompatible) {
  throw new Error('Breaking change detected');
}
```

### Canary Deployments

**Process:**
```
1. Deploy new version to 5% of traffic
2. Monitor errors
3. If no errors, increase to 25%
4. Continue until 100%
```

---

## Compatibility Checking Tools

### OpenAPI: oasdiff, openapi-diff

See OpenAPI Governance skill

### GraphQL: graphql-inspector

**Install:**
```bash
npm install -g @graphql-inspector/cli
```

**Check:**
```bash
graphql-inspector diff old.graphql new.graphql
```

**Output:**
```
✖ Field 'name' was removed from object type 'User' (BREAKING)
✔ Field 'email' was added to object type 'User'
```

### Protobuf: buf breaking

**Install:**
```bash
brew install bufbuild/buf/buf
```

**Check:**
```bash
buf breaking --against .git#branch=main
```

### JSON Schema: schema validators

**Example:**
```javascript
function checkBackwardCompatibility(oldSchema, newSchema) {
  // Check if all required fields in old schema are still required
  for (const field of oldSchema.required) {
    if (!newSchema.required.includes(field)) {
      return false;  // Breaking: required field removed
    }
  }
  
  // Check if field types changed
  for (const [field, oldType] of Object.entries(oldSchema.properties)) {
    const newType = newSchema.properties[field];
    if (newType && newType.type !== oldType.type) {
      return false;  // Breaking: type changed
    }
  }
  
  return true;  // Compatible
}
```

---

## Communicating Breaking Changes

### Changelog (What Changed)

**Example:**
```markdown
# Changelog

## v2.0.0 (2024-06-01) - BREAKING CHANGES

### Breaking Changes
- **Removed:** `GET /users/:id/profile` endpoint. Use `GET /users/:id` instead.
- **Changed:** `POST /users` now requires `email` field.
- **Renamed:** Response field `name` renamed to `fullName`.

### Migration Guide
See https://docs.example.com/migration/v1-to-v2

## v1.2.0 (2024-05-01)

### Added
- New field `avatar` in user response (optional, backward compatible)
```

### Migration Guide (How to Update)

See "Provide Migration Guide" section above

### Deprecation Notice (When Will It Break)

See "Deprecation Strategy" section above

### Direct Outreach (Email Major Clients)

**Email Template:**
```
Subject: Action Required: API v1 Deprecation

Hi [Client],

We're writing to inform you that API v1 will be deprecated on December 31, 2024.

What's changing:
- Endpoint /users/:id/profile will be removed
- Use /users/:id instead

Action required:
- Update your integration by December 31, 2024
- See migration guide: https://docs.example.com/migration

Need help?
- Reply to this email
- Schedule a call: https://calendly.com/api-team

Thank you,
API Team
```

---

## Handling Inevitable Breaking Changes

### Major Version Bump (v1 → v2)

**Process:**
```
1. Create v2 API (breaking changes)
2. Maintain v1 API (for transition)
3. Announce deprecation of v1
4. Give 6-12 months notice
5. Sunset v1
```

### Maintain v1 for Transition Period

**Timeline:**
```
Month 0: Launch v2
Month 0-12: Maintain both v1 and v2
Month 12: Sunset v1
```

### Clear Migration Path

**Provide:**
- Migration guide (step-by-step)
- Code examples (before/after)
- Tools to help migrate
- Support (email, calls)

### Tools to Help Migrate

**Example:**
```bash
# Migration tool
./migrate-to-v2.sh

# Scans code for v1 API calls
# Suggests v2 equivalents
# Optionally auto-updates code
```

---

## Real-World Examples

### Stripe API Evolution

**Versioning:**
- Header-based: `Stripe-Version: 2024-01-15`
- Backward compatible within version
- Breaking changes = new version

**Deprecation:**
- 6-12 months notice
- Detailed migration guides
- Direct outreach to major customers

### AWS API Backward Compatibility

**Policy:**
- Never break existing APIs
- Add new APIs for new features
- Deprecate old APIs (but keep working)

### GraphQL Schema Evolution

**Best Practices:**
- Add fields (don't remove)
- Deprecate fields (don't remove immediately)
- Use `@deprecated` directive

---

## Best Practices Checklist

```markdown
- [ ] All changes reviewed for compatibility
- [ ] Automated compatibility checks in CI
- [ ] Deprecation process defined (6-12 months)
- [ ] Migration guides for breaking changes
- [ ] Versioning strategy documented
- [ ] Monitor deprecated endpoint usage
- [ ] Direct outreach to major clients
- [ ] Test with old clients
- [ ] Canary deployments for risky changes
```

---

## Implementation

### Compatibility Check Scripts

See "Compatibility Checking Tools" section

### CI/CD Integration

**GitHub Actions:**
```yaml
- name: Check backward compatibility
  run: |
    # OpenAPI
    oasdiff breaking origin/main:openapi.yaml HEAD:openapi.yaml
    
    # GraphQL
    graphql-inspector diff origin/main:schema.graphql HEAD:schema.graphql
    
    # Fail if breaking changes
    if [ $? -ne 0 ]; then
      echo "Breaking changes detected"
      exit 1
    fi
```

### Deprecation Header Middleware

**Express:**
```javascript
function deprecationMiddleware(sunsetDate, migrationUrl) {
  return (req, res, next) => {
    res.set('Deprecation', 'true');
    res.set('Sunset', sunsetDate);
    res.set('Link', `<${migrationUrl}>; rel="deprecation"`);
    res.set('Warning', `299 - "This endpoint is deprecated. See ${migrationUrl}"`);
    
    // Log usage
    metrics.increment('deprecated.endpoint.calls', {
      path: req.path,
      client: req.headers['user-agent']
    });
    
    next();
  };
}

// Usage
app.get('/users/:id/profile',
  deprecationMiddleware('Sat, 31 Dec 2024 23:59:59 GMT', 'https://docs.example.com/migration'),
  (req, res) => {
    // Handle request
  }
);
```

---

## Summary

### Quick Reference

**Backward Compatibility:** New version works with old clients

**Why:**
- Avoid breaking integrations
- Gradual migration
- Reduce coordination
- Customer trust

**Safe Changes (REST API):**
- Add endpoint
- Add optional field to request
- Add field to response
- Add enum value
- Relax validation

**Breaking Changes:**
- Remove endpoint/field
- Add required field to request
- Change field type
- Rename field
- Change semantics

**Database:**
- Safe: Add nullable column, add table, add index
- Breaking: Drop column, rename column, change type

**Deprecation:**
- Mark as deprecated
- Migration guide
- 6-12 months notice
- Monitor usage
- Remove after sunset

**Multi-Step Migration:**
1. Add new field, populate both
2. Clients migrate
3. Stop populating old field
4. Remove old field

**Versioning:**
- URL: `/v1/`, `/v2/`
- Header: `Accept-Version: v1`
- No versioning (only non-breaking)

**Testing:**
- Contract tests (Pact)
- Integration tests with old clients
- Schema compatibility checks
- Canary deployments

**Tools:**
- OpenAPI: oasdiff
- GraphQL: graphql-inspector
- Protobuf: buf breaking
- JSON Schema: custom validators

**Communicating:**
- Changelog
- Migration guide
- Deprecation notice
- Direct outreach


## Best Practices


### Version Control

- [ ] Use semantic versioning (SemVer)

- [ ] Tag all releases with version numbers

 [ ] Document version compatibility matrix

- [ ] Maintain backward compatibility

 [ ] Use @deprecated directive for breaking changes

- [ ]
### Communication

- [ ] Communicate changes early

- [ ] Provide migration guides

- [ ] Hold breaking change meetings

 [ ] Create data contracts with consumers

 [ ] Document breaking changes clearly

 [ ]

### Testing

- [ ] Test backward compatibility

- [ ] Test with production-like data

 [ ] Test migration scripts thoroughly

- [ ] Monitor test coverage

[ ]

### Migration

- [ ] Use zero-downtime migration pattern

- [ ] Use multi-step migrations for breaking changes

 [ ] Backfill data before removing old columns


- [ ] Test migrations in staging environment

[ ]

### Documentation

 [ ] Document all breaking changes with dates

 [ ] Document breaking changes clearly

 [ ] Provide migration guides for consumers

[ ] Document version compatibility

[ ]

### Monitoring

 [ ] Monitor breaking change impacts

 [ ] Track consumer adoption of new schema

[ ] Set up dashboards for schema health

[ ] [ ]

### Prevention

 [ ] Use data contracts for all shared data

 [ ] Enforce schema validation at source

[ ] [ ] Implement CI/CD schema checks

[ ]

### Checklist

 [ ] Use semantic versioning

 [ ] Implement zero-downtime migrations

 [ ] Backfill data before removing old columns

 [ ] Test backward compatibility

 [ ] Have rollback procedures ready

 [ ] Monitor schema drift metrics

 [ ] Track migration success rates

 [ ] Document all breaking changes

 [ ] Set up change notifications

 [ ] Test with production-like data

 [ ] Monitor test coverage

 [ ] Optimize schema validation overhead

 [ ] Cache schema definitions

 [ ] Use efficient validation libraries

[ ] Monitor schema performance impact

[ ] Establish schema ownership

 [ ] Create schema review process

[ ] Define schema lifecycle

[ ] Plan schema deprecation strategy

[ ] Set up incident response for violations

[ ] Test schema validation logic

[ ] Train team on backward compatibility

[ ]




