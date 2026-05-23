---
name: SCIM Provisioning
description: Comprehensive guide to implementing SCIM 2.0 for automated user provisioning and deprovisioning in enterprise applications
---

# SCIM Provisioning

## What is SCIM?

**SCIM (System for Cross-domain Identity Management):** Standard for automating user provisioning.

### Key Characteristics

- **Push-based:** IdP pushes changes to your app (not pull)
- **REST API:** Standard HTTP endpoints for user management
- **Real-time:** Changes happen immediately (not on next login)

### Example Flow
```
1. IT admin creates user in Okta
2. Okta calls your SCIM API: POST /scim/v2/Users
3. Your app creates user in database
4. User can now log in (before first SSO login!)

5. IT admin deactivates user in Okta
6. Okta calls your SCIM API: PATCH /scim/v2/Users/{id} (active=false)
7. Your app deactivates user
8. User can no longer log in
```

---

## Why Enterprises Need SCIM

### 1. Automate Onboarding

**Without SCIM:**
```
New employee joins
→ IT admin manually creates account in 20 apps
→ Takes hours, error-prone
```

**With SCIM:**
```
New employee joins
→ IT admin creates account in IdP (Okta)
→ IdP automatically creates account in all apps via SCIM
→ Takes seconds
```

### 2. Automate Offboarding

**Without SCIM:**
```
Employee leaves
→ IT admin manually deactivates account in 20 apps
→ Often missed, security risk!
```

**With SCIM:**
```
Employee leaves
→ IT admin deactivates account in IdP
→ IdP automatically deactivates in all apps via SCIM
→ Immediate, no orphaned accounts
```

### 3. Keep User Info in Sync

**Example:**
```
User changes name (marriage, etc.)
→ IT admin updates in IdP
→ IdP pushes update to all apps via SCIM
→ Name updated everywhere
```

### 4. IT Admin Control

**Benefits:**
- Centralized user management (one place)
- Audit trail (who created/modified users)
- Compliance (SOC2, ISO 27001)

---

## SCIM vs JIT Provisioning

### JIT (Pull)

**How it works:**
```
1. User doesn't exist in your app
2. User logs in via SSO (first time)
3. Your app creates user from SSO assertion
4. User is logged in
```

**Pros:**
- Simple to implement
- No SCIM API needed

**Cons:**
- User created on first login (not before)
- Can't pre-provision users
- Can't deactivate users who never logged in

### SCIM (Push)

**How it works:**
```
1. IT admin creates user in IdP
2. IdP calls your SCIM API
3. Your app creates user
4. User exists before first login
```

**Pros:**
- User created proactively
- Can deactivate users who never logged in
- Real-time updates

**Cons:**
- More complex to implement
- Requires SCIM API

### When to Use

- **JIT:** Small/medium customers, simple setup
- **SCIM:** Enterprise customers, required for large deployments

---

## SCIM 2.0 Specification

### RFCs

- **RFC 7643:** Core Schema (User, Group resources)
- **RFC 7644:** Protocol (HTTP endpoints, operations)

### Resources

**User:**
```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "id": "123",
  "userName": "john.doe@example.com",
  "name": {
    "givenName": "John",
    "familyName": "Doe"
  },
  "emails": [
    {
      "value": "john.doe@example.com",
      "primary": true
    }
  ],
  "active": true,
  "groups": [
    {
      "value": "group-123",
      "display": "Engineering"
    }
  ]
}
```

**Group:**
```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
  "id": "group-123",
  "displayName": "Engineering",
  "members": [
    {
      "value": "123",
      "display": "John Doe"
    }
  ]
}
```

---

## SCIM Endpoints

### User Endpoints

```
GET    /scim/v2/Users              List users
POST   /scim/v2/Users              Create user
GET    /scim/v2/Users/:id          Get user
PUT    /scim/v2/Users/:id          Replace user (full update)
PATCH  /scim/v2/Users/:id          Update user (partial)
DELETE /scim/v2/Users/:id          Delete user (or deactivate)
```

### Group Endpoints

```
GET    /scim/v2/Groups             List groups
POST   /scim/v2/Groups             Create group
GET    /scim/v2/Groups/:id         Get group
PUT    /scim/v2/Groups/:id         Replace group
PATCH  /scim/v2/Groups/:id         Update group
DELETE /scim/v2/Groups/:id         Delete group
```

### Service Provider Config

```
GET    /scim/v2/ServiceProviderConfig    Get SCIM capabilities
GET    /scim/v2/Schemas                  Get supported schemas
GET    /scim/v2/ResourceTypes            Get supported resource types
```

---

## SCIM User Schema

### Core Attributes

```json
{
  "userName": "john.doe@example.com",  // Required, unique
  "name": {
    "givenName": "John",
    "familyName": "Doe",
    "formatted": "John Doe"
  },
  "emails": [
    {
      "value": "john.doe@example.com",
      "primary": true
    }
  ],
  "active": true,                      // Boolean, for soft delete
  "groups": [                          // Array of group IDs
    {
      "value": "group-123",
      "display": "Engineering"
    }
  ]
}
```

### Enterprise Extension (Optional)

```json
{
  "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
    "employeeNumber": "12345",
    "department": "Engineering",
    "manager": {
      "value": "manager-456",
      "displayName": "Jane Smith"
    }
  }
}
```

---

## SCIM Authentication

### OAuth 2.0 Bearer Token (Recommended)

**Request:**
```
POST /scim/v2/Users
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/scim+json
```

**Implementation:**
```javascript
app.use('/scim/v2', (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      status: '401',
      detail: 'Missing authorization token'
    });
  }
  
  // Validate token
  const tenant = await validateSCIMToken(token);
  if (!tenant) {
    return res.status(401).json({
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      status: '401',
      detail: 'Invalid token'
    });
  }
  
  req.tenant = tenant;
  next();
});
```

### Basic Auth (Less Secure)

**Request:**
```
POST /scim/v2/Users
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

### API Key (Custom)

**Request:**
```
POST /scim/v2/Users
X-API-Key: your-api-key
```

---

## Implementing SCIM Server

### Libraries

**Node.js:**
```bash
npm install scim2-server
```

**Python:**
```bash
pip install django-scim2
```

**Java:**
```xml
<dependency>
  <groupId>com.unboundid</groupId>
  <artifactId>scim2-sdk-server</artifactId>
</dependency>
```

### Database Schema

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  user_name VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) NOT NULL,
  given_name VARCHAR(255),
  family_name VARCHAR(255),
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE groups (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  display_name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE group_members (
  group_id UUID REFERENCES groups(id),
  user_id UUID REFERENCES users(id),
  PRIMARY KEY (group_id, user_id)
);
```

### Express SCIM Server Example

```javascript
const express = require('express');
const app = express();

app.use(express.json({ type: 'application/scim+json' }));

// List users
app.get('/scim/v2/Users', async (req, res) => {
  const { startIndex = 1, count = 100, filter } = req.query;
  
  let query = db.users.where({ tenantId: req.tenant.id });
  
  // Apply filter (e.g., userName eq "john@example.com")
  if (filter) {
    const parsed = parseSCIMFilter(filter);
    query = query.where(parsed);
  }
  
  const users = await query
    .offset(startIndex - 1)
    .limit(count)
    .all();
  
  const total = await query.count();
  
  res.json({
    schemas: ['urn:ietf:params:scim:api:messages:2.0:ListResponse'],
    totalResults: total,
    startIndex: parseInt(startIndex),
    itemsPerPage: users.length,
    Resources: users.map(toSCIMUser)
  });
});

// Create user
app.post('/scim/v2/Users', async (req, res) => {
  const { userName, name, emails, active = true } = req.body;
  
  // Check if user already exists
  const existing = await db.users.findOne({
    tenantId: req.tenant.id,
    userName
  });
  
  if (existing) {
    return res.status(409).json({
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      status: '409',
      detail: 'User already exists'
    });
  }
  
  // Create user
  const user = await db.users.create({
    tenantId: req.tenant.id,
    userName,
    email: emails[0].value,
    givenName: name.givenName,
    familyName: name.familyName,
    active
  });
  
  res.status(201).json(toSCIMUser(user));
});

// Get user
app.get('/scim/v2/Users/:id', async (req, res) => {
  const user = await db.users.findOne({
    id: req.params.id,
    tenantId: req.tenant.id
  });
  
  if (!user) {
    return res.status(404).json({
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      status: '404',
      detail: 'User not found'
    });
  }
  
  res.json(toSCIMUser(user));
});

// Update user (PATCH)
app.patch('/scim/v2/Users/:id', async (req, res) => {
  const { Operations } = req.body;
  
  const user = await db.users.findOne({
    id: req.params.id,
    tenantId: req.tenant.id
  });
  
  if (!user) {
    return res.status(404).json({
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      status: '404',
      detail: 'User not found'
    });
  }
  
  // Apply operations
  for (const op of Operations) {
    if (op.op === 'replace') {
      if (op.path === 'active') {
        user.active = op.value;
      } else if (op.path === 'name.givenName') {
        user.givenName = op.value;
      }
      // ... handle other paths
    }
  }
  
  await user.save();
  
  res.json(toSCIMUser(user));
});

// Delete user (deactivate)
app.delete('/scim/v2/Users/:id', async (req, res) => {
  const user = await db.users.findOne({
    id: req.params.id,
    tenantId: req.tenant.id
  });
  
  if (!user) {
    return res.status(404).json({
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      status: '404',
      detail: 'User not found'
    });
  }
  
  // Soft delete (set active=false)
  user.active = false;
  await user.save();
  
  res.status(204).send();
});

function toSCIMUser(user) {
  return {
    schemas: ['urn:ietf:params:scim:schemas:core:2.0:User'],
    id: user.id,
    userName: user.userName,
    name: {
      givenName: user.givenName,
      familyName: user.familyName
    },
    emails: [
      {
        value: user.email,
        primary: true
      }
    ],
    active: user.active,
    meta: {
      resourceType: 'User',
      created: user.createdAt,
      lastModified: user.updatedAt
    }
  };
}
```

---

## SCIM Operations

### Create User

**Request:**
```
POST /scim/v2/Users
Content-Type: application/scim+json

{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "userName": "john.doe@example.com",
  "name": {
    "givenName": "John",
    "familyName": "Doe"
  },
  "emails": [
    {
      "value": "john.doe@example.com",
      "primary": true
    }
  ],
  "active": true
}
```

**Response (201 Created):**
```json
{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "id": "123",
  "userName": "john.doe@example.com",
  "name": {
    "givenName": "John",
    "familyName": "Doe"
  },
  "emails": [
    {
      "value": "john.doe@example.com",
      "primary": true
    }
  ],
  "active": true,
  "meta": {
    "resourceType": "User",
    "created": "2024-01-15T10:00:00Z",
    "lastModified": "2024-01-15T10:00:00Z"
  }
}
```

### Update User (PATCH)

**Request:**
```
PATCH /scim/v2/Users/123
Content-Type: application/scim+json

{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
  "Operations": [
    {
      "op": "replace",
      "path": "name.givenName",
      "value": "Jonathan"
    },
    {
      "op": "replace",
      "path": "active",
      "value": false
    }
  ]
}
```

### Deactivate User

**Request:**
```
PATCH /scim/v2/Users/123
Content-Type: application/scim+json

{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
  "Operations": [
    {
      "op": "replace",
      "path": "active",
      "value": false
    }
  ]
}
```

**Implementation:**
```javascript
// Set active=false (soft delete)
await db.users.update(userId, { active: false });

// Prevent login
if (!user.active) {
  throw new Error('User account is deactivated');
}
```

### Add to Group

**Request:**
```
PATCH /scim/v2/Users/123
Content-Type: application/scim+json

{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
  "Operations": [
    {
      "op": "add",
      "path": "groups",
      "value": [
        {
          "value": "group-456",
          "display": "Engineering"
        }
      ]
    }
  ]
}
```

---

## Error Handling

### Error Response Format

```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "400",
  "scimType": "invalidValue",
  "detail": "userName is required"
}
```

### Common Errors

**400 Bad Request:**
```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "400",
  "detail": "Invalid request body"
}
```

**401 Unauthorized:**
```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "401",
  "detail": "Invalid bearer token"
}
```

**404 Not Found:**
```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "404",
  "detail": "User not found"
}
```

**409 Conflict:**
```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "409",
  "scimType": "uniqueness",
  "detail": "userName already exists"
}
```

**500 Internal Server Error:**
```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "500",
  "detail": "Internal server error"
}
```

---

## Testing SCIM

### Manual Testing (Postman)

**Create User:**
```
POST https://yourapp.com/scim/v2/Users
Authorization: Bearer your-token
Content-Type: application/scim+json

{
  "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
  "userName": "test@example.com",
  "name": {
    "givenName": "Test",
    "familyName": "User"
  },
  "emails": [{"value": "test@example.com", "primary": true}],
  "active": true
}
```

### SCIM Test Suite

**Runscope SCIM Validator:**
- Tests all SCIM endpoints
- Validates responses
- Checks compliance

**Example:**
```bash
# Run SCIM validator
curl -X POST https://www.runscope.com/radar/scim \
  -d "base_url=https://yourapp.com/scim/v2" \
  -d "token=your-bearer-token"
```

### Integration Testing with Actual IdP

**Process:**
1. Configure SCIM in IdP (Okta, Azure AD)
2. Create test user in IdP
3. Verify user created in your app via SCIM
4. Update user in IdP
5. Verify user updated in your app
6. Deactivate user in IdP
7. Verify user deactivated in your app

---

## SCIM IdP Configuration

### Okta Configuration

**Steps:**
1. Go to Okta Admin → Applications → Your App
2. Click "Provisioning" tab
3. Enable "SCIM"
4. Enter SCIM endpoint: `https://yourapp.com/scim/v2`
5. Enter bearer token
6. Map attributes:
   - Okta `email` → SCIM `userName`
   - Okta `firstName` → SCIM `name.givenName`
   - Okta `lastName` → SCIM `name.familyName`
7. Test connection
8. Enable provisioning (Create, Update, Deactivate)

### Azure AD Configuration

**Steps:**
1. Go to Azure AD → Enterprise Applications → Your App
2. Click "Provisioning"
3. Set provisioning mode to "Automatic"
4. Enter SCIM endpoint: `https://yourapp.com/scim/v2`
5. Enter bearer token
6. Test connection
7. Map attributes (similar to Okta)
8. Start provisioning

---

## Handling SCIM Edge Cases

### User Already Exists (409 Conflict)

**Scenario:** IdP tries to create user that already exists

**Response:**
```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "409",
  "scimType": "uniqueness",
  "detail": "User with userName 'john@example.com' already exists"
}
```

**IdP Behavior:** Usually updates existing user instead

### Email Change (Unique Constraint)

**Scenario:** User email changes, but new email already exists

**Solution:**
```javascript
// Check if new email is already used
const existing = await db.users.findOne({
  email: newEmail,
  tenantId: req.tenant.id,
  id: { $ne: userId }  // Exclude current user
});

if (existing) {
  return res.status(409).json({
    schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
    status: '409',
    detail: 'Email already in use'
  });
}
```

### Group Doesn't Exist

**Scenario:** IdP adds user to group that doesn't exist in your app

**Option 1: Create group automatically**
```javascript
let group = await db.groups.findOne({ id: groupId });
if (!group) {
  group = await db.groups.create({
    id: groupId,
    displayName: groupDisplay,
    tenantId: req.tenant.id
  });
}
```

**Option 2: Return error**
```json
{
  "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
  "status": "404",
  "detail": "Group not found"
}
```

### Partial Updates (PATCH)

**Scenario:** IdP sends PATCH with only changed fields

**Implementation:**
```javascript
// Only update fields that are present in the request
const updates = {};
for (const op of Operations) {
  if (op.op === 'replace') {
    if (op.path === 'active') updates.active = op.value;
    if (op.path === 'name.givenName') updates.givenName = op.value;
    // ... etc
  }
}

await db.users.update(userId, updates);
```

---

## SCIM for Multi-Tenancy

### Tenant-Specific SCIM Endpoints

**Option 1: Tenant in URL**
```
https://yourapp.com/scim/v2/tenants/{tenantId}/Users
```

**Option 2: Tenant in bearer token**
```
https://yourapp.com/scim/v2/Users
Authorization: Bearer {token-with-tenant-id}
```

**Recommended:** Option 2 (cleaner URLs)

### Isolate Users by Tenant

**Database Query:**
```javascript
// Always filter by tenant
const users = await db.users.where({
  tenantId: req.tenant.id  // From bearer token
});
```

**Security:** Never return users from other tenants!

---

## Monitoring SCIM

### Provisioning Success Rate

**Metric:**
```
Success Rate = Successful SCIM Requests / Total SCIM Requests
```

**Target:** >99%

### Failed Operations

**Log and Alert:**
```javascript
app.post('/scim/v2/Users', async (req, res) => {
  try {
    // ... create user
  } catch (err) {
    console.error('SCIM create user failed', {
      tenantId: req.tenant.id,
      userName: req.body.userName,
      error: err.message
    });
    
    // Alert if error rate > 5%
    if (errorRate > 0.05) {
      sendAlert('High SCIM error rate', { errorRate });
    }
    
    res.status(500).json({
      schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'],
      status: '500',
      detail: 'Internal server error'
    });
  }
});
```

### Sync Status

**Check:** Are users in sync with IdP?

**Implementation:**
```javascript
// Periodic sync check (daily)
cron.schedule('0 2 * * *', async () => {
  for (const tenant of tenants) {
    const ourUsers = await db.users.where({ tenantId: tenant.id });
    const idpUsers = await fetchUsersFromIdP(tenant);
    
    const missing = idpUsers.filter(idpUser =>
      !ourUsers.find(u => u.userName === idpUser.userName)
    );
    
    if (missing.length > 0) {
      console.warn('Users out of sync', {
        tenantId: tenant.id,
        missing: missing.length
      });
    }
  }
});
```

---

## Common SCIM Providers

### Okta (SCIM 2.0)

**Features:**
- Full SCIM 2.0 support
- Create, update, deactivate users
- Group provisioning
- Attribute mapping

**Setup:** Easy (built-in SCIM support)

### Azure AD (SCIM 2.0)

**Features:**
- Full SCIM 2.0 support
- Create, update, deactivate users
- Group provisioning
- Custom attributes

**Setup:** Easy (built-in SCIM support)

### OneLogin (SCIM 2.0)

**Features:**
- Full SCIM 2.0 support
- Similar to Okta/Azure AD

**Setup:** Easy

### Google Workspace (Custom, Not Full SCIM)

**Limitation:** Google Workspace doesn't support standard SCIM 2.0

**Alternative:** Use Google Directory API (custom integration)

---

## Summary

### Quick Reference

**SCIM:**
- Standard for automated user provisioning
- Push-based (IdP → Your App)
- REST API (HTTP endpoints)

**Why:**
- Automate onboarding/offboarding
- Keep user info in sync
- IT admin control

**Endpoints:**
- GET /scim/v2/Users (list)
- POST /scim/v2/Users (create)
- GET /scim/v2/Users/:id (get)
- PATCH /scim/v2/Users/:id (update)
- DELETE /scim/v2/Users/:id (deactivate)

**Authentication:**
- OAuth 2.0 Bearer token (recommended)
- Basic auth (less secure)
- API key (custom)

**User Schema:**
- userName (unique, required)
- name (givenName, familyName)
- emails (array)
- active (boolean)
- groups (array)

**Operations:**
- Create user → Create in database
- Update user → Update attributes
- Deactivate user → Set active=false
- Add to group → Update groups array

**Testing:**
- Manual (Postman, curl)
- SCIM test suite (Runscope)
- Integration with actual IdP

**Multi-Tenancy:**
- Tenant-specific endpoints or token
- Isolate users by tenant
- Never return users from other tenants

**Monitoring:**
- Success rate (>99%)
- Failed operations (log and alert)
- Sync status (periodic check)

## Best Practices

### SCIM Implementation Best Practices
- **Use Established Libraries**: Leverage existing SCIM libraries (scim2-server for Node.js, django-scim2 for Python) instead of implementing from scratch. This reduces bugs and speeds up development.
- **Support All Required Endpoints**: Implement all mandatory SCIM 2.0 endpoints (GET/POST/PATCH/DELETE for Users and Groups, ServiceProviderConfig, Schemas, ResourceTypes).
- **Return Proper Error Responses**: Always return SCIM-compliant error responses with correct `schemas`, `status`, and `detail` fields.
- **Handle Pagination**: Implement pagination for list endpoints using `startIndex` and `count` parameters. Return `totalResults` in response.
- **Support Filtering**: Implement SCIM filter syntax for querying users and groups. This is required by many IdPs.

### Authentication Best Practices
- **Use OAuth 2.0 Bearer Tokens**: Require OAuth 2.0 bearer tokens for authentication. This is the most secure and widely supported method.
- **Token Per Tenant**: Generate unique bearer tokens for each tenant. This prevents cross-tenant access and improves security.
- **Token Rotation**: Implement token rotation policies (e.g., rotate tokens every 90 days) to reduce security risks.
- **Secure Token Storage**: Store tokens securely using encryption at rest. Never log tokens or include them in error messages.
- **Token Validation**: Validate tokens on every request and check for expiration, revocation, and proper scope.

### User Management Best Practices
- **Soft Delete for Deactivation**: Set `active=false` instead of hard deleting users. This preserves audit history and allows for reactivation.
- **Prevent Duplicate Users**: Return 409 Conflict error when attempting to create a user with a `userName` that already exists.
- **Handle Email Changes**: Validate that new email addresses are not already in use before updating. Return 409 Conflict if email is taken.
- **Maintain User Attributes**: Keep user attributes in sync with IdP on every update. Update name, email, and other fields from SCIM request.
- **Log All Changes**: Audit log all user creation, update, and deactivation operations with timestamps and actor information.

### Group Management Best Practices
- **Auto-Create Groups**: Create groups automatically when referenced in user updates if they don't exist. This prevents sync failures.
- **Handle Group Membership**: Support adding and removing users from groups via PATCH operations on both users and groups.
- **Group Display Names**: Use `displayName` field from IdP when creating groups. Maintain consistency with IdP's group naming.
- **Nested Groups**: If your application supports nested groups, ensure SCIM operations properly handle group hierarchies.
- **Group Synchronization**: Sync group memberships from IdP on every user update to ensure consistency.

### Multi-Tenancy Best Practices
- **Tenant Isolation**: Always filter queries by tenant ID. Never return users or groups from other tenants.
- **Tenant-Specific Tokens**: Use bearer tokens that include tenant information to identify the tenant making the request.
- **Tenant Configuration**: Store SCIM configuration per tenant (endpoint URLs, certificates, attribute mappings).
- **Separate Databases**: Use separate database schemas or tables for each tenant's users and groups.
- **Audit by Tenant**: Maintain separate audit logs per tenant for compliance and troubleshooting.

### Error Handling Best Practices
- **SCIM-Compliant Errors**: Return errors in SCIM format with `schemas: ['urn:ietf:params:scim:api:messages:2.0:Error']`.
- **Descriptive Error Messages**: Provide clear, actionable error messages that help IdP administrators understand and fix issues.
- **Appropriate HTTP Status Codes**: Use correct HTTP status codes (400 for bad request, 401 for unauthorized, 404 for not found, 409 for conflict, 500 for server errors).
- **Log All Errors**: Log all SCIM errors with request details, error messages, and timestamps. This is crucial for debugging.
- **Monitor Error Rates**: Track error rates and set up alerts when error rates exceed thresholds (e.g., >5%).

### Performance Best Practices
- **Database Indexing**: Index frequently queried fields like `userName`, `tenantId`, and `active` to improve query performance.
- **Response Time Targets**: Aim for sub-second response times for SCIM operations. IdPs may timeout on slow responses.
- **Pagination Limits**: Limit maximum number of results per request (e.g., 100-1000) to prevent large queries from impacting performance.
- **Async Operations**: Consider async processing for bulk operations like group membership updates to prevent blocking.
- **Caching**: Cache frequently accessed data like tenant configurations and role mappings to reduce database load.

### Testing Best Practices
- **Test with Real IdPs**: Test your SCIM implementation with actual IdPs (Okta, Azure AD, OneLogin) to ensure compatibility.
- **Test Edge Cases**: Test scenarios like duplicate users, non-existent groups, invalid tokens, and malformed requests.
- **Use SCIM Validators**: Use SCIM validation tools like Runscope SCIM Validator to verify compliance.
- **Automated Testing**: Create automated tests for all SCIM endpoints and run them in CI/CD pipeline.
- **Load Testing**: Perform load testing to ensure your SCIM endpoints can handle high volumes of requests from large enterprises.

### Monitoring Best Practices
- **Track Success Rate**: Monitor percentage of successful SCIM requests. Target >99% success rate.
- **Monitor Sync Status**: Periodically compare your user database with IdP's user list to identify sync discrepancies.
- **Alert on Failures**: Set up alerts for SCIM failures, especially for critical operations like user creation and deactivation.
- **Log Response Times**: Track response times for all SCIM operations and investigate slow endpoints.
- **Monitor Token Usage**: Track token usage patterns and detect unusual activity that may indicate compromised tokens.

## Checklist

### SCIM Implementation Checklist
- [ ] Choose and install SCIM library for your platform
- [ ] Implement GET /scim/v2/Users (list users with pagination)
- [ ] Implement POST /scim/v2/Users (create user)
- [ ] Implement GET /scim/v2/Users/:id (get user)
- [ ] Implement PUT /scim/v2/Users/:id (replace user)
- [ ] Implement PATCH /scim/v2/Users/:id (update user)
- [ ] Implement DELETE /scim/v2/Users/:id (deactivate user)
- [ ] Implement GET /scim/v2/Groups (list groups with pagination)
- [ ] Implement POST /scim/v2/Groups (create group)
- [ ] Implement GET /scim/v2/Groups/:id (get group)
- [ ] Implement PATCH /scim/v2/Groups/:id (update group)
- [ ] Implement DELETE /scim/v2/Groups/:id (delete group)
- [ ] Implement GET /scim/v2/ServiceProviderConfig
- [ ] Implement GET /scim/v2/Schemas
- [ ] Implement GET /scim/v2/ResourceTypes
- [ ] Implement SCIM filter support
- [ ] Return SCIM-compliant error responses

### Authentication Checklist
- [ ] Implement OAuth 2.0 bearer token authentication
- [ ] Generate unique tokens per tenant
- [ ] Implement token validation middleware
- [ ] Store tokens securely (encrypted at rest)
- [ ] Set up token rotation policy
- [ ] Return 401 for invalid or expired tokens
- [ ] Never log tokens in plain text

### User Management Checklist
- [ ] Implement soft delete (active=false instead of hard delete)
- [ ] Return 409 Conflict for duplicate userName
- [ ] Validate email uniqueness before updates
- [ ] Sync user attributes from SCIM requests
- [ ] Handle PATCH operations correctly (add, replace, remove)
- [ ] Log all user creation, update, deactivation
- [ ] Test user creation with IdP

### Group Management Checklist
- [ ] Auto-create groups when referenced
- [ ] Support adding users to groups via PATCH
- [ ] Support removing users from groups via PATCH
- [ ] Use displayName from IdP for group names
- [ ] Handle nested groups if applicable
- [ ] Sync group memberships from user updates
- [ ] Test group operations with IdP

### Multi-Tenancy Checklist
- [ ] Filter all queries by tenant ID
- [ ] Store tenant information in bearer tokens
- [ ] Store SCIM configuration per tenant
- [ ] Use separate database tables/schemas per tenant
- [ ] Maintain separate audit logs per tenant
- [ ] Test tenant isolation (verify no cross-tenant data access)

### Error Handling Checklist
- [ ] Return SCIM-compliant error responses
- [ ] Use appropriate HTTP status codes
- [ ] Provide descriptive error messages
- [ ] Log all errors with request details
- [ ] Monitor error rates and set up alerts
- [ ] Test error handling with invalid requests

### Performance Checklist
- [ ] Index userName, tenantId, active fields
- [ ] Measure response times for all endpoints
- [ ] Implement pagination limits
- [ ] Consider async processing for bulk operations
- [ ] Cache frequently accessed data
- [ ] Perform load testing

### Testing Checklist
- [ ] Test with Okta
- [ ] Test with Azure AD
- [ ] Test with OneLogin
- [ ] Use SCIM validator tool
- [ ] Create automated tests for all endpoints
- [ ] Test edge cases (duplicates, non-existent resources)
- [ ] Perform load testing

### Monitoring Checklist
- [ ] Track success rate (>99% target)
- [ ] Monitor response times
- [ ] Set up alerts for failures
- [ ] Implement periodic sync checks
- [ ] Monitor token usage patterns
- [ ] Create dashboards for SCIM metrics

### Deployment Checklist
- [ ] Document SCIM API endpoints
- [ ] Create IdP configuration guide
- [ ] Set up monitoring dashboards
- [ ] Configure error alerts
- [ ] Train support team on SCIM issues
- [ ] Create incident response process for SCIM failures
- [ ] Test with production IdP before go-live
