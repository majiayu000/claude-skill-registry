---
name: Cross-Team Interfaces
description: Comprehensive guide to defining and managing cross-team interfaces including APIs, events, data schemas, and process contracts for independent team operation
---

# Cross-Team Interfaces

## What are Cross-Team Interfaces?

**Definition:** Contracts between teams that define how they interact and integrate.

### Types of Interfaces

1. **Technical:** REST APIs, GraphQL, gRPC, message queues, events
2. **Data:** Database schemas, file formats, message formats
3. **Process:** Handoffs, approval workflows, escalation procedures

### Example
```
Team A (Backend) provides: User API
Team B (Mobile) consumes: User API

Interface: REST API contract
- Endpoint: GET /api/users/:id
- Response format: JSON
- Authentication: JWT token
- SLA: 99.9% uptime, <200ms latency
```

---

## Why Interfaces Matter

### 1. Enable Independent Work

**Without Clear Interface:**
```
Mobile team: "How do I get user data?"
Backend team: "Let me check... I'll get back to you"
→ Mobile team blocked, waiting for answer
```

**With Clear Interface:**
```
Mobile team: Reads API documentation
→ Knows exactly how to call API
→ Can start development immediately
```

### 2. Reduce Miscommunication

**Without Interface:**
```
Mobile team expects: { "name": "John" }
Backend team returns: { "full_name": "John Doe" }
→ Integration fails, rework needed
```

**With Interface:**
```
API contract specifies: { "name": "John Doe" }
→ Both teams aligned, no surprises
```

### 3. Allow Parallel Development

**Without Interface:**
```
Backend team must finish API first
→ Mobile team waits
→ Sequential work (slow)
```

**With Interface:**
```
Teams agree on API contract
→ Backend builds real API
→ Mobile builds against mock API
→ Parallel work (fast)
```

### 4. Clear Ownership

**Without Interface:**
```
Bug in integration: "Is this a backend or mobile issue?"
→ Finger-pointing, slow resolution
```

**With Interface:**
```
API contract defines responsibilities
→ Backend owns API behavior
→ Mobile owns API usage
→ Clear ownership, fast resolution
```

---

## Types of Interfaces

### 1. Technical Interfaces

#### REST APIs
```
GET /api/users/:id
POST /api/users
PUT /api/users/:id
DELETE /api/users/:id
```

#### GraphQL
```graphql
query {
  user(id: "123") {
    id
    name
    email
  }
}
```

#### gRPC
```protobuf
service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc CreateUser (CreateUserRequest) returns (User);
}
```

#### Events (Message Queue)
```json
{
  "event": "user.created",
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  },
  "timestamp": "2024-01-15T10:00:00Z"
}
```

### 2. Data Interfaces

#### Database Schema
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### File Format (CSV)
```csv
id,name,email,created_at
123,John Doe,john@example.com,2024-01-15T10:00:00Z
```

#### Message Format (JSON)
```json
{
  "version": "1.0",
  "type": "user_event",
  "payload": {
    "user_id": "123",
    "action": "login"
  }
}
```

### 3. Process Interfaces

#### Handoff Workflow
```
Design Team → Engineering Team

Handoff criteria:
• Design approved by stakeholders
• All assets exported (Figma)
• Design specs documented
• Handoff meeting scheduled

Engineering accepts when:
• All criteria met
• Questions answered
• Ready to start development
```

#### Approval Workflow
```
Engineer → Tech Lead → Security Team → Deploy

Approval gates:
• Tech Lead: Code review approved
• Security Team: Security scan passed
• Deploy: All approvals received
```

#### Escalation Procedure
```
Level 1: Team lead (respond within 1 hour)
Level 2: Engineering manager (respond within 4 hours)
Level 3: VP Engineering (respond within 24 hours)
```

---

## Defining Good Interfaces

### 1. Clear Contract (Input, Output, Behavior)

**Good API Contract:**
```yaml
# POST /api/users
description: Create a new user

request:
  content-type: application/json
  body:
    email: string (required, valid email)
    name: string (required, 1-255 chars)
    age: integer (optional, 0-150)

response:
  200 OK:
    content-type: application/json
    body:
      id: string (UUID)
      email: string
      name: string
      age: integer | null
      created_at: string (ISO 8601 timestamp)
  
  400 Bad Request:
    body:
      error: string (error message)
      field: string (field that failed validation)
  
  409 Conflict:
    body:
      error: "Email already exists"

behavior:
  - Email must be unique
  - Name is trimmed of whitespace
  - Age defaults to null if not provided
  - created_at is set to current timestamp
```

### 2. Versioned (Avoid Breaking Changes)

**Versioning Strategy:**
```
/api/v1/users  (current version)
/api/v2/users  (new version)

Both versions supported for 6 months
v1 deprecated after 6 months
v1 removed after 12 months
```

### 3. Documented (API Docs, Runbooks)

**Documentation Includes:**
- Overview (what does this API do?)
- Authentication (how to authenticate?)
- Endpoints (all available endpoints)
- Request/response examples
- Error codes and meanings
- Rate limits
- Changelog (version history)
- Contact info (who owns this?)

### 4. Stable (Don't Change Frequently)

**Stability Guidelines:**
- Don't change existing endpoints
- Add new endpoints for new functionality
- Deprecate old endpoints (don't remove immediately)
- Communicate changes 2+ weeks in advance

### 5. Testable (Integration Tests)

**Contract Tests:**
```javascript
// Consumer test (Mobile team)
test('GET /api/users/:id returns user', async () => {
  const response = await api.get('/api/users/123');
  
  expect(response.status).toBe(200);
  expect(response.body).toMatchObject({
    id: '123',
    name: expect.any(String),
    email: expect.any(String),
    created_at: expect.any(String)
  });
});

// Provider test (Backend team)
test('GET /api/users/:id returns 404 for non-existent user', async () => {
  const response = await api.get('/api/users/nonexistent');
  
  expect(response.status).toBe(404);
  expect(response.body.error).toBe('User not found');
});
```

---

## API Design for Cross-Team

### RESTful Conventions

**Resource-Based URLs:**
```
GET    /api/users          (list users)
POST   /api/users          (create user)
GET    /api/users/:id      (get user)
PUT    /api/users/:id      (update user)
DELETE /api/users/:id      (delete user)
```

**HTTP Methods:**
- **GET:** Retrieve resource (idempotent, safe)
- **POST:** Create resource (not idempotent)
- **PUT:** Update resource (idempotent)
- **PATCH:** Partial update (idempotent)
- **DELETE:** Delete resource (idempotent)

### Consistent Naming

**Conventions:**
- Use nouns for resources (not verbs)
- Use plural nouns (`/users`, not `/user`)
- Use kebab-case for multi-word resources (`/user-profiles`)
- Use camelCase for JSON fields (`firstName`, not `first_name`)

**Good:**
```
GET /api/users
GET /api/user-profiles
{ "firstName": "John", "lastName": "Doe" }
```

**Bad:**
```
GET /api/getUsers (verb in URL)
GET /api/user (singular)
{ "first_name": "John" } (snake_case)
```

### Error Handling Standards

**Error Response Format:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address",
    "field": "email",
    "details": {
      "provided": "invalid-email",
      "expected": "valid email format"
    }
  }
}
```

**HTTP Status Codes:**
- **200 OK:** Success
- **201 Created:** Resource created
- **400 Bad Request:** Client error (validation)
- **401 Unauthorized:** Not authenticated
- **403 Forbidden:** Not authorized
- **404 Not Found:** Resource not found
- **409 Conflict:** Resource conflict (duplicate)
- **500 Internal Server Error:** Server error

### Authentication/Authorization

**Authentication:**
```
Authorization: Bearer <JWT_TOKEN>
```

**JWT Token Payload:**
```json
{
  "sub": "user_123",
  "email": "user@example.com",
  "role": "admin",
  "exp": 1705315200
}
```

**Authorization:**
```javascript
// Check if user has permission
if (user.role !== 'admin') {
  return res.status(403).json({ error: 'Forbidden' });
}
```

### Rate Limiting

**Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705315200
```

**Response (429 Too Many Requests):**
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Try again in 60 seconds.",
    "retry_after": 60
  }
}
```

---

## Interface Documentation

### OpenAPI/Swagger Spec

**Example:**
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
  description: API for managing users
  contact:
    name: Backend Team
    email: backend@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  users:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  total:
                    type: integer
                  page:
                    type: integer

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time
```

### Example Requests/Responses

**Create User:**
```bash
# Request
curl -X POST https://api.example.com/v1/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com"
  }'

# Response (201 Created)
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:00:00Z"
}
```

### Error Codes and Meanings

**Error Code Reference:**
```markdown
| Code | HTTP Status | Meaning | Resolution |
|------|-------------|---------|------------|
| VALIDATION_ERROR | 400 | Invalid input | Check request body |
| UNAUTHORIZED | 401 | Not authenticated | Provide valid token |
| FORBIDDEN | 403 | Not authorized | Check permissions |
| NOT_FOUND | 404 | Resource not found | Check resource ID |
| CONFLICT | 409 | Resource conflict | Use different value |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests | Wait and retry |
| INTERNAL_ERROR | 500 | Server error | Contact support |
```

### Changelog (Version History)

**Example:**
```markdown
# Changelog

## v1.1.0 (2024-02-01)
### Added
- New endpoint: GET /api/users/:id/posts
- Support for filtering users by role

### Changed
- Increased rate limit from 100 to 1000 req/hour

### Deprecated
- Field `full_name` (use `name` instead)

## v1.0.0 (2024-01-01)
### Added
- Initial release
- CRUD endpoints for users
```

### Contact Info (Who Owns This)

**Documentation Footer:**
```markdown
## Support

**Owner:** Backend Team
**Slack:** #backend-team
**Email:** backend@example.com
**On-call:** PagerDuty rotation

**SLA:**
- Response time: <200ms (p95)
- Uptime: 99.9%
- Support response: <1 hour (business hours)
```

---

## Versioning Strategies

### 1. Semantic Versioning (MAJOR.MINOR.PATCH)

**Format:** `v1.2.3`
- **MAJOR:** Breaking changes (v1 → v2)
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

**Example:**
```
v1.0.0: Initial release
v1.1.0: Add new endpoint (backward compatible)
v1.1.1: Fix bug (backward compatible)
v2.0.0: Breaking change (remove field)
```

### 2. URL Versioning (/v1/, /v2/)

**Format:**
```
/api/v1/users
/api/v2/users
```

**Pros:**
- Clear and visible
- Easy to route
- Can run multiple versions simultaneously

**Cons:**
- URL changes
- Need to maintain multiple codebases

### 3. Header Versioning (Accept-Version)

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
- Harder to test (need to set header)

### 4. Deprecation Policy (Notice Period)

**Policy:**
```
1. Announce deprecation (2 weeks notice)
2. Mark as deprecated (6 months)
3. Remove (12 months after deprecation)
```

**Deprecation Notice:**
```json
{
  "deprecated": true,
  "deprecation_date": "2024-01-01",
  "removal_date": "2025-01-01",
  "replacement": "/api/v2/users",
  "message": "This endpoint is deprecated. Please migrate to v2."
}
```

---

## Breaking vs Non-Breaking Changes

### Non-Breaking Changes (Safe)

**Examples:**
- Add new endpoint
- Add optional field to request
- Add new field to response
- Add new error code
- Increase rate limit

**Example:**
```json
// Before
{
  "id": "123",
  "name": "John Doe"
}

// After (non-breaking: added field)
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com"  // New field (clients can ignore)
}
```

### Breaking Changes (Dangerous)

**Examples:**
- Remove endpoint
- Remove field from response
- Change field type
- Rename field
- Change error format
- Decrease rate limit

**Example:**
```json
// Before
{
  "id": "123",
  "name": "John Doe"
}

// After (BREAKING: removed field)
{
  "id": "123"
  // "name" field removed (clients will break!)
}
```

### Communicate Breaking Changes Early

**Process:**
1. **Announce:** Email, Slack, documentation (2+ weeks notice)
2. **Deprecate:** Mark old version as deprecated
3. **Support:** Run both versions for transition period (6 months)
4. **Remove:** Remove old version after transition period

**Announcement Template:**
```markdown
# Breaking Change: User API v2

**What:** We're releasing User API v2 with breaking changes
**When:** February 1, 2024
**Why:** Improve consistency and add new features

**Breaking Changes:**
- Field `full_name` renamed to `name`
- Field `created` renamed to `created_at`
- Error format changed (see docs)

**Migration Guide:**
1. Update field names in your code
2. Update error handling
3. Test against staging API
4. Deploy to production

**Timeline:**
- Jan 15: v2 released (v1 still supported)
- Jul 15: v1 deprecated (6 months)
- Jan 15, 2025: v1 removed (12 months)

**Support:**
- Questions: #api-migration Slack channel
- Issues: api-support@example.com
```

---

## Interface Agreements (Contracts)

### What Each Team Provides

**Backend Team Provides:**
```markdown
# User API Contract

**Endpoints:**
- GET /api/v1/users
- POST /api/v1/users
- GET /api/v1/users/:id
- PUT /api/v1/users/:id
- DELETE /api/v1/users/:id

**SLA:**
- Uptime: 99.9%
- Response time: <200ms (p95)
- Rate limit: 1000 req/hour per API key

**Support:**
- Documentation: https://docs.example.com/api
- Slack: #backend-api
- On-call: PagerDuty rotation
- Response time: <1 hour (business hours)
```

**Mobile Team Provides:**
```markdown
# Mobile App Requirements

**API Usage:**
- Expected traffic: 10,000 req/day
- Peak traffic: 1,000 req/hour
- Regions: US, EU

**Requirements:**
- Authentication: JWT tokens
- Error handling: Retry with exponential backoff
- Caching: Cache responses for 5 minutes

**Testing:**
- Test against staging API before production
- Report bugs within 24 hours
```

### SLAs (Response Time, Uptime)

**Service Level Agreement:**
```markdown
# User API SLA

**Uptime:** 99.9% (43 minutes downtime per month)
**Response Time:**
- p50: <100ms
- p95: <200ms
- p99: <500ms

**Rate Limits:**
- Free tier: 100 req/hour
- Pro tier: 1,000 req/hour
- Enterprise: 10,000 req/hour

**Support:**
- Business hours (9am-5pm PT): <1 hour response
- After hours: <4 hour response
- Critical issues: <15 minute response (24/7)

**Penalties (if SLA breached):**
- 99.9% → 99.0%: 10% credit
- 99.0% → 95.0%: 25% credit
- <95.0%: 50% credit
```

### Support Process (Who to Contact)

**Escalation Path:**
```markdown
# Support Escalation

**Level 1: Slack (#backend-api)**
- For: Questions, minor issues
- Response time: <1 hour (business hours)

**Level 2: Email (api-support@example.com)**
- For: Bugs, feature requests
- Response time: <4 hours

**Level 3: PagerDuty (Critical Issues)**
- For: Production outages, security issues
- Response time: <15 minutes (24/7)

**Escalation Criteria:**
- No response in SLA time → Escalate to next level
- Production outage → Escalate immediately to Level 3
```

### Review Process (Approvals Needed)

**API Change Review:**
```markdown
# API Change Review Process

**For Non-Breaking Changes:**
1. Create PR with API changes
2. Update OpenAPI spec
3. Get approval from tech lead
4. Deploy to staging
5. Notify consumers (#api-changes Slack)
6. Deploy to production

**For Breaking Changes:**
1. Create RFC (Request for Comments)
2. Get approval from:
   - Tech lead
   - Product manager
   - All API consumers
3. Create migration guide
4. Announce 2+ weeks in advance
5. Deploy v2 (keep v1 running)
6. Support both versions for 6 months
7. Deprecate v1
8. Remove v1 after 12 months
```

---

## Integration Patterns

### 1. Synchronous (REST, gRPC)

**When to Use:**
- Need immediate response
- Request-response pattern
- Low latency required

**Example (REST):**
```javascript
// Client
const user = await fetch('/api/users/123').then(r => r.json());
console.log(user.name);

// Server
app.get('/api/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  res.json(user);
});
```

**Pros:**
- Simple
- Immediate response
- Easy to debug

**Cons:**
- Tight coupling
- Synchronous (blocks until response)
- Harder to scale

### 2. Asynchronous (Message Queue, Events)

**When to Use:**
- Don't need immediate response
- Decouple producer and consumer
- High throughput needed

**Example (Message Queue):**
```javascript
// Producer
await queue.publish('user.created', {
  id: '123',
  name: 'John Doe',
  email: 'john@example.com'
});

// Consumer
queue.subscribe('user.created', async (message) => {
  const user = message.data;
  await sendWelcomeEmail(user.email);
});
```

**Pros:**
- Loose coupling
- Asynchronous (doesn't block)
- Easy to scale

**Cons:**
- More complex
- Eventual consistency
- Harder to debug

### 3. Batch (File Transfer, Scheduled Jobs)

**When to Use:**
- Large data transfers
- Not time-sensitive
- Periodic updates

**Example (CSV Export):**
```javascript
// Producer (daily at midnight)
cron.schedule('0 0 * * *', async () => {
  const users = await db.users.findAll();
  const csv = convertToCSV(users);
  await uploadToS3('users.csv', csv);
});

// Consumer (daily at 1am)
cron.schedule('0 1 * * *', async () => {
  const csv = await downloadFromS3('users.csv');
  const users = parseCSV(csv);
  await processUsers(users);
});
```

**Pros:**
- Simple
- Handles large data
- Low real-time requirements

**Cons:**
- Not real-time
- File format coupling
- Error handling complex

---

## Testing Cross-Team Integrations

### 1. Contract Testing (Pact)

**Consumer Test (Mobile Team):**
```javascript
const { Pact } = require('@pact-foundation/pact');

const provider = new Pact({
  consumer: 'MobileApp',
  provider: 'UserAPI'
});

describe('User API', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  test('get user by ID', async () => {
    await provider.addInteraction({
      state: 'user 123 exists',
      uponReceiving: 'a request for user 123',
      withRequest: {
        method: 'GET',
        path: '/api/users/123'
      },
      willRespondWith: {
        status: 200,
        body: {
          id: '123',
          name: 'John Doe',
          email: 'john@example.com'
        }
      }
    });

    const user = await api.getUser('123');
    expect(user.name).toBe('John Doe');
  });
});
```

**Provider Test (Backend Team):**
```javascript
const { Verifier } = require('@pact-foundation/pact');

describe('User API Provider', () => {
  test('verifies contract with MobileApp', async () => {
    await new Verifier({
      provider: 'UserAPI',
      providerBaseUrl: 'http://localhost:3000',
      pactUrls: ['./pacts/mobileapp-userapi.json'],
      stateHandlers: {
        'user 123 exists': async () => {
          await db.users.create({ id: '123', name: 'John Doe' });
        }
      }
    }).verifyProvider();
  });
});
```

### 2. Integration Tests

**Example:**
```javascript
describe('User API Integration', () => {
  test('create and retrieve user', async () => {
    // Create user
    const createResponse = await fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'John Doe',
        email: 'john@example.com'
      })
    });
    expect(createResponse.status).toBe(201);
    const user = await createResponse.json();

    // Retrieve user
    const getResponse = await fetch(`/api/users/${user.id}`);
    expect(getResponse.status).toBe(200);
    const retrievedUser = await getResponse.json();
    expect(retrievedUser.name).toBe('John Doe');
  });
});
```

### 3. Staging Environment Tests

**Process:**
1. Deploy to staging
2. Run integration tests against staging
3. Manual testing (if needed)
4. Deploy to production

### 4. Mock Services for Development

**Example (Mock API):**
```javascript
// mock-api.js
const express = require('express');
const app = express();

app.get('/api/users/:id', (req, res) => {
  res.json({
    id: req.params.id,
    name: 'Mock User',
    email: 'mock@example.com'
  });
});

app.listen(3000);
```

**Usage:**
```javascript
// Use mock in development, real in production
const apiUrl = process.env.NODE_ENV === 'development'
  ? 'http://localhost:3000'
  : 'https://api.example.com';
```

---

## Communication Channels

### 1. Shared Slack Channel

**Purpose:** Quick questions, updates, coordination

**Example:**
```
#mobile-backend-integration

Mobile Team: "What's the rate limit for /api/users?"
Backend Team: "1000 req/hour. See docs: https://..."

Mobile Team: "We're seeing 500 errors on staging"
Backend Team: "Investigating. Will update in 15 min"
```

### 2. Regular Sync Meetings

**Frequency:** Weekly or bi-weekly

**Agenda:**
```
Integration Sync (Wednesdays, 2pm)

1. Progress updates (10 min)
2. Blockers and issues (15 min)
3. Upcoming changes (10 min)
4. Action items (5 min)
```

### 3. Written Interface Docs

**Location:** Centralized documentation (Confluence, Notion, GitHub)

**Contents:**
- API reference
- Getting started guide
- Examples
- Changelog
- FAQs

### 4. Incident Escalation Path

**Process:**
```
1. Detect issue (monitoring, user report)
2. Report in Slack (#incidents)
3. Page on-call (PagerDuty)
4. Investigate and fix
5. Post-mortem (for SEV0/1)
```

---

## Onboarding to Interface

### Getting Started Guide

**Example:**
```markdown
# User API Getting Started

## 1. Get API Key
1. Go to https://dashboard.example.com
2. Create account
3. Generate API key

## 2. Make First Request
```bash
curl https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 3. Next Steps
- Read [API Reference](https://docs.example.com/api)
- Try [Interactive Playground](https://playground.example.com)
- Join [Slack #api-support](https://slack.com/...)
```

### Sample Code

**JavaScript:**
```javascript
const axios = require('axios');

const api = axios.create({
  baseURL: 'https://api.example.com/v1',
  headers: {
    'Authorization': `Bearer ${process.env.API_KEY}`
  }
});

// Get user
const user = await api.get('/users/123');
console.log(user.data);

// Create user
const newUser = await api.post('/users', {
  name: 'John Doe',
  email: 'john@example.com'
});
console.log(newUser.data);
```

### Sandbox Environment

**Purpose:** Test without affecting production

**Example:**
```
Production: https://api.example.com
Sandbox: https://sandbox-api.example.com

Sandbox features:
- Same API as production
- Test data (reset daily)
- No rate limits
- Free to use
```

### Contact for Questions

**Support Channels:**
```markdown
## Need Help?

**Documentation:** https://docs.example.com
**Slack:** #api-support
**Email:** api-support@example.com
**Office Hours:** Tuesdays 2-3pm PT (Zoom link)
```

---

## Monitoring Interfaces

### Usage Metrics

**Track:**
- Requests per second
- Requests by endpoint
- Requests by consumer
- Requests by region

**Dashboard:**
```
User API Usage (Last 24 Hours)

Total Requests: 1,234,567
Requests/Second: 14.3

Top Endpoints:
1. GET /api/users/:id (45%)
2. GET /api/users (30%)
3. POST /api/users (15%)

Top Consumers:
1. MobileApp (60%)
2. WebApp (30%)
3. Analytics (10%)
```

### Error Rates

**Track:**
- 4xx errors (client errors)
- 5xx errors (server errors)
- Error rate by endpoint
- Error rate by consumer

**Alert:**
```
Alert: High Error Rate
Endpoint: GET /api/users/:id
Error rate: 15% (threshold: 5%)
Time: Last 15 minutes
Action: Investigate immediately
```

### Latency

**Track:**
- p50, p95, p99 latency
- Latency by endpoint
- Latency by region

**Dashboard:**
```
User API Latency (Last 24 Hours)

p50: 85ms
p95: 180ms
p99: 450ms

Slowest Endpoints:
1. GET /api/users (p95: 250ms)
2. POST /api/users (p95: 200ms)
```

### Breaking Change Impact

**Track:**
- Usage of deprecated endpoints
- Consumers still on old version
- Migration progress

**Report:**
```
Deprecation Report: /api/v1/users

Deprecated: Jan 1, 2024
Removal: Jul 1, 2024

Current Usage:
- Total requests: 10,000/day
- v1: 2,000/day (20%) ← Still using deprecated version
- v2: 8,000/day (80%)

Consumers on v1:
- LegacyApp (1,500/day)
- PartnerAPI (500/day)

Action: Contact LegacyApp and PartnerAPI to migrate
```

---

## Interface Anti-Patterns

### 1. Undocumented Interfaces

**Problem:**
```
Mobile team: "How do I call the API?"
Backend team: "Let me check the code..."
→ No documentation, slow onboarding
```

**Solution:** Document all interfaces (OpenAPI spec, examples)

### 2. Frequent Breaking Changes

**Problem:**
```
Week 1: Field renamed from `name` to `full_name`
Week 2: Field renamed from `full_name` to `fullName`
Week 3: Field renamed from `fullName` to `displayName`
→ Consumers constantly breaking
```

**Solution:** Avoid breaking changes, use versioning

### 3. Tight Coupling (Team B Directly Queries Team A's DB)

**Problem:**
```
Mobile app directly queries backend database
→ Tight coupling, can't change schema
```

**Solution:** Use API layer (loose coupling)

### 4. No Versioning

**Problem:**
```
Breaking change deployed
→ All consumers break immediately
→ No way to rollback
```

**Solution:** Version all interfaces (/v1/, /v2/)

---

## Real Cross-Team Interface Examples

### Example 1: Payment Team API for Checkout Team

**Interface:**
```yaml
# Payment API Contract

POST /api/v1/payments
description: Process a payment

request:
  amount: number (in cents)
  currency: string (USD, EUR, etc.)
  payment_method: string (card, paypal, etc.)
  customer_id: string

response:
  200 OK:
    payment_id: string
    status: string (succeeded, failed, pending)
    amount: number
    currency: string
  
  400 Bad Request:
    error: string (invalid payment method, insufficient funds, etc.)

SLA:
  - Response time: <500ms (p95)
  - Uptime: 99.99%
  - Support: #payments-team Slack
```

### Example 2: Auth Team SSO for All Teams

**Interface:**
```yaml
# SSO API Contract

POST /api/v1/auth/login
description: Authenticate user with email/password

request:
  email: string
  password: string

response:
  200 OK:
    access_token: string (JWT)
    refresh_token: string
    expires_in: number (seconds)
  
  401 Unauthorized:
    error: "Invalid credentials"

GET /api/v1/auth/me
description: Get current user
headers:
  Authorization: Bearer <access_token>

response:
  200 OK:
    user_id: string
    email: string
    role: string
```

### Example 3: Data Platform Events for Analytics

**Interface:**
```yaml
# Event Schema

event: user.created
version: 1.0
payload:
  user_id: string (UUID)
  email: string
  name: string
  created_at: string (ISO 8601)
  source: string (web, mobile, api)

event: user.updated
version: 1.0
payload:
  user_id: string
  fields_changed: array of strings
  updated_at: string

event: user.deleted
version: 1.0
payload:
  user_id: string
  deleted_at: string
```

---

## Templates

### Template 1: API Contract

```yaml
# [API Name] Contract

## Overview
[Brief description of what this API does]

## Authentication
[How to authenticate: JWT, API key, etc.]

## Endpoints

### [Endpoint Name]
**Method:** GET/POST/PUT/DELETE
**Path:** /api/v1/[resource]
**Description:** [What this endpoint does]

**Request:**
```json
{
  "field1": "type (required/optional)",
  "field2": "type (required/optional)"
}
```

**Response (200 OK):**
```json
{
  "field1": "type",
  "field2": "type"
}
```

**Errors:**
- 400: [Description]
- 404: [Description]
- 500: [Description]

## SLA
- Uptime: [percentage]
- Response time: [latency]
- Rate limit: [requests per time]

## Support
- Documentation: [URL]
- Slack: [channel]
- Email: [email]
- On-call: [PagerDuty/phone]

## Changelog
- v1.1.0 (2024-02-01): [Changes]
- v1.0.0 (2024-01-01): Initial release
```

### Template 2: Integration Checklist

```markdown
# Integration Checklist

## Pre-Integration
- [ ] API contract defined and agreed
- [ ] OpenAPI spec created
- [ ] Sample code provided
- [ ] Sandbox environment available
- [ ] Documentation published

## Development
- [ ] Consumer tests written (Pact)
- [ ] Provider tests written
- [ ] Integration tests written
- [ ] Error handling implemented
- [ ] Retry logic implemented

## Testing
- [ ] Tested against sandbox
- [ ] Tested against staging
- [ ] Load testing completed
- [ ] Security testing completed

## Deployment
- [ ] Deployed to staging
- [ ] Integration tests passing
- [ ] Deployed to production
- [ ] Monitoring configured
- [ ] Alerts configured

## Post-Deployment
- [ ] Consumers notified
- [ ] Documentation updated
- [ ] Runbook created
- [ ] On-call rotation updated
```

---

## Summary

### Quick Reference

**Interface Types:**
- Technical: REST, GraphQL, gRPC, events
- Data: Schemas, file formats, messages
- Process: Handoffs, approvals, escalations

**Good Interface Characteristics:**
- Clear contract (input, output, behavior)
- Versioned (avoid breaking changes)
- Documented (API docs, examples)
- Stable (don't change frequently)
- Testable (integration tests)

**API Design:**
- RESTful conventions (resource-based URLs)
- Consistent naming (plural nouns, camelCase)
- Error handling (standard codes and formats)
- Authentication (JWT, API keys)
- Rate limiting (prevent abuse)

**Versioning:**
- Semantic versioning (MAJOR.MINOR.PATCH)
- URL versioning (/v1/, /v2/)
- Deprecation policy (2 weeks notice, 6 months support)

**Breaking vs Non-Breaking:**
- Non-breaking: Add field, add endpoint
- Breaking: Remove field, change type, rename
- Communicate breaking changes early

**Integration Patterns:**
- Synchronous: REST, gRPC (immediate response)
- Asynchronous: Message queue, events (decouple)
- Batch: File transfer, scheduled jobs (large data)

**Testing:**
- Contract testing (Pact)
- Integration tests
- Staging environment tests
- Mock services (development)

**Monitoring:**
- Usage metrics (requests, consumers)
- Error rates (4xx, 5xx)
- Latency (p50, p95, p99)
- Breaking change impact

**Anti-Patterns:**
- Undocumented interfaces
- Frequent breaking changes
- Tight coupling (direct DB access)
- No versioning
