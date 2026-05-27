---
name: Deprecation Notices
description: Comprehensive guide to API deprecation processes, sunset timelines, communication strategies, and graceful migration paths
---

# Deprecation Notices

## What is Deprecation?

**Definition:** Announcing end-of-life for an API/feature with time for users to migrate before eventual removal.

### Lifecycle
```
Active → Deprecated → Sunset → Removed

Active: Fully supported
Deprecated: Still works, but discouraged (6-12 months)
Sunset: Stops working
Removed: Code deleted
```

### Example
```
Jan 2024: API v1 active
Jun 2024: API v1 deprecated (announce v2)
Dec 2024: API v1 sunset (stops working)
Jan 2025: API v1 code removed
```

---

## Why Proper Deprecation Matters

### 1. Avoid Breaking Users Without Warning

**Bad:**
```
Deploy new version
→ Old endpoint removed
→ Users break immediately
→ Angry customers
→ Emergency rollback
```

**Good:**
```
Announce deprecation (6 months notice)
→ Users migrate gradually
→ Sunset date arrives
→ No surprises
```

### 2. Maintain Trust

**Trust Built By:**
- Advance notice (6-12 months)
- Clear migration path
- Support during migration
- No surprises

**Trust Broken By:**
- Sudden changes
- No warning
- Unclear migration
- Breaking without notice

### 3. Smooth Migration

**Gradual Migration:**
```
Month 0: Announce deprecation
Month 3: 25% migrated
Month 6: 50% migrated
Month 9: 75% migrated
Month 12: 100% migrated, sunset
```

### 4. Legal Compliance (If Contractual)

**Contracts May Require:**
- Minimum notice period (e.g., 12 months)
- Migration support
- No breaking changes without notice

**Check Contracts Before Deprecating!**

---

## Deprecation Timeline

### Typical: 6-12 Months for APIs

**Timeline:**
```
Month 0: Announce deprecation
Month 3: Reminder + usage stats
Month 6: Final warning
Month 9: Reach out to remaining users
Month 12: Sunset
```

### Critical Systems: 12-24 Months

**Examples:**
- Banking APIs
- Healthcare systems
- Government integrations

**Why Longer:**
- Longer approval processes
- More stakeholders
- Higher risk

### Internal APIs: 3-6 Months

**Why Shorter:**
- Control both sides
- Faster coordination
- Lower risk

### Consider: Contract Terms, User Base Size

**Factors:**
- **Contract terms:** May require 12+ months
- **User base size:** More users = longer timeline
- **Criticality:** Mission-critical = longer timeline
- **Complexity:** Complex migration = longer timeline

---

## Deprecation Process

### Step 1: Mark as Deprecated (Code, Docs)

**Code (JavaScript):**
```javascript
/**
 * @deprecated Use getUser() instead. Will be removed in v2.0.0.
 * @see getUser
 */
function getUserProfile(id) {
  console.warn('getUserProfile is deprecated. Use getUser() instead.');
  return getUser(id);
}
```

**Code (Python):**
```python
import warnings

def get_user_profile(id):
    """
    .. deprecated:: 1.5.0
       Use :func:`get_user` instead.
    """
    warnings.warn(
        "get_user_profile is deprecated. Use get_user() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_user(id)
```

**Docs:**
```markdown
## GET /users/:id/profile

**⚠️ DEPRECATED:** This endpoint is deprecated and will be removed on December 31, 2024.

**Use instead:** `GET /users/:id`

**Migration guide:** https://docs.example.com/migration/profile-to-user
```

### Step 2: Announce (Email, Blog, Changelog)

**Email:**
```
Subject: Deprecation Notice: /users/:id/profile endpoint

Hi developers,

We're deprecating the /users/:id/profile endpoint.

What's changing:
- Endpoint: GET /users/:id/profile
- Sunset date: December 31, 2024
- Replacement: GET /users/:id

Why:
- Consolidating user endpoints for simplicity
- New endpoint provides more data

Action required:
- Update your integration by December 31, 2024
- See migration guide: https://docs.example.com/migration

Need help?
- Reply to this email
- Join office hours: Fridays 2-3pm PT

Thank you,
API Team
```

**Blog Post:**
```markdown
# Deprecation Notice: /users/:id/profile Endpoint

**Date:** June 1, 2024
**Sunset Date:** December 31, 2024

We're deprecating the `/users/:id/profile` endpoint in favor of the consolidated `/users/:id` endpoint.

## What's Changing
The `/users/:id/profile` endpoint will stop working on December 31, 2024.

## Why
We're consolidating user endpoints to simplify our API and provide a better developer experience.

## What to Use Instead
Use `GET /users/:id` instead. It returns the same data plus additional fields.

## Migration Guide
See our [migration guide](https://docs.example.com/migration) for step-by-step instructions.

## Timeline
- **June 1, 2024:** Deprecation announced
- **September 1, 2024:** Reminder email sent
- **December 1, 2024:** Final warning
- **December 31, 2024:** Endpoint stops working

## Need Help?
Contact us at api@example.com or join our office hours.
```

**Changelog:**
```markdown
# Changelog

## v1.5.0 (2024-06-01)

### Deprecated
- **GET /users/:id/profile** - Use GET /users/:id instead. Will be removed on 2024-12-31.

### Added
- **GET /users/:id** - New consolidated user endpoint
```

### Step 3: Monitor Usage

**Track Metrics:**
```javascript
app.get('/users/:id/profile', (req, res) => {
  // Track usage
  metrics.increment('deprecated.users_profile.calls', {
    client: req.headers['user-agent'],
    clientId: req.user?.clientId
  });
  
  // Return response
  res.json(profile);
});
```

**Dashboard:**
```
Deprecated Endpoint: /users/:id/profile
Sunset Date: 2024-12-31 (6 months remaining)

Usage:
- Total calls/day: 1,000 (down from 5,000 last month)
- Unique clients: 50 (down from 200)

Top Clients:
1. mobile-app: 500 calls/day
2. web-app: 300 calls/day
3. partner-api: 200 calls/day

Trend: ↓ Declining (good!)
```

### Step 4: Reach Out to Active Users

**Email Top Users:**
```
Subject: Action Required: Migrate from /users/:id/profile

Hi [Client],

We noticed you're still using the deprecated /users/:id/profile endpoint (500 calls/day).

This endpoint will stop working on December 31, 2024 (3 months remaining).

Action required:
- Migrate to GET /users/:id
- See migration guide: https://docs.example.com/migration

Need help?
- Reply to this email
- Schedule a call: https://calendly.com/api-team

Thank you,
API Team
```

### Step 5: Sunset (Stop Working)

**Return 410 Gone:**
```javascript
app.get('/users/:id/profile', (req, res) => {
  res.status(410).json({
    error: 'This endpoint has been removed',
    message: 'GET /users/:id/profile was removed on 2024-12-31',
    replacement: 'Use GET /users/:id instead',
    migrationGuide: 'https://docs.example.com/migration'
  });
});
```

### Step 6: Remove Code

**After Sunset:**
```
1. Sunset date reached (Dec 31, 2024)
2. Monitor for errors (1 month)
3. If no issues, remove code (Jan 31, 2025)
```

---

## Deprecation Headers (HTTP)

### Deprecation: true (Draft RFC)

**Header:**
```
HTTP/1.1 200 OK
Deprecation: true
```

**Spec:** https://datatracker.ietf.org/doc/html/draft-dalal-deprecation-header

### Sunset: Date (RFC 8594)

**Header:**
```
HTTP/1.1 200 OK
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
```

**Spec:** https://datatracker.ietf.org/doc/html/rfc8594

### Link: Migration Guide

**Header:**
```
HTTP/1.1 200 OK
Link: <https://docs.example.com/migration>; rel="sunset"
```

### Warning: Message (RFC 7234)

**Header:**
```
HTTP/1.1 200 OK
Warning: 299 - "This endpoint is deprecated. Use /v2/users instead. See https://docs.example.com/migration"
```

### All Together

**Example:**
```
HTTP/1.1 200 OK
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: <https://docs.example.com/migration>; rel="sunset"
Warning: 299 - "This endpoint is deprecated and will be removed on 2024-12-31. Use /v2/users instead."
Content-Type: application/json

{
  "id": "123",
  "name": "John Doe"
}
```

**Middleware (Express):**
```javascript
function deprecationHeaders(sunsetDate, migrationUrl, message) {
  return (req, res, next) => {
    res.set('Deprecation', 'true');
    res.set('Sunset', sunsetDate);
    res.set('Link', `<${migrationUrl}>; rel="sunset"`);
    res.set('Warning', `299 - "${message}"`);
    next();
  };
}

app.get('/users/:id/profile',
  deprecationHeaders(
    'Sat, 31 Dec 2024 23:59:59 GMT',
    'https://docs.example.com/migration',
    'This endpoint is deprecated. Use /v2/users instead.'
  ),
  (req, res) => {
    res.json(profile);
  }
);
```

---

## OpenAPI Deprecation

### deprecated: true

**Example:**
```yaml
paths:
  /users/{id}/profile:
    get:
      deprecated: true
      summary: Get user profile (DEPRECATED)
      description: |
        **DEPRECATED:** This endpoint is deprecated and will be removed on 2024-12-31.
        
        **Use instead:** GET /users/{id}
        
        **Migration guide:** https://docs.example.com/migration
      responses:
        '200':
          description: User profile
```

**Swagger UI:**
```
GET /users/{id}/profile (DEPRECATED)

⚠️ Deprecated
This endpoint is deprecated and will be removed on 2024-12-31.
Use GET /users/{id} instead.
```

---

## GraphQL Deprecation

### @deprecated Directive

**Example:**
```graphql
type User {
  id: ID!
  name: String! @deprecated(reason: "Use firstName and lastName instead")
  firstName: String!
  lastName: String!
}
```

**Query:**
```graphql
{
  user(id: "123") {
    id
    name  # Warning: Field 'name' is deprecated. Use firstName and lastName instead.
  }
}
```

---

## Code Deprecation

### @deprecated Annotation (Java)

```java
/**
 * @deprecated Use getUser() instead. Will be removed in v2.0.0.
 */
@Deprecated
public User getUserProfile(String id) {
    return getUser(id);
}
```

### @deprecated JSDoc (JavaScript)

```javascript
/**
 * @deprecated Use getUser() instead. Will be removed in v2.0.0.
 * @see getUser
 */
function getUserProfile(id) {
  console.warn('getUserProfile is deprecated');
  return getUser(id);
}
```

### warnings.warn (Python)

```python
import warnings

def get_user_profile(id):
    warnings.warn(
        "get_user_profile is deprecated. Use get_user() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_user(id)
```

---

## Communication Channels

### In-App Notifications (For Logged-In Users)

**Example:**
```
Banner:
⚠️ You're using a deprecated API endpoint (/users/:id/profile).
It will stop working on Dec 31, 2024.
[Migrate Now] [Learn More]
```

### Email Campaigns (To All API Users)

See "Step 2: Announce" above

### Blog Post (Public Announcement)

See "Step 2: Announce" above

### Changelog (Detailed Info)

See "Step 2: Announce" above

### Status Page Updates

**Example:**
```
Status: Scheduled Maintenance

API v1 Sunset
Date: December 31, 2024
Impact: API v1 endpoints will stop working
Action: Migrate to API v2
Guide: https://docs.example.com/migration
```

### Release Notes

**Example:**
```
# Release Notes - v1.5.0

## Deprecations
- GET /users/:id/profile (sunset: 2024-12-31)
  - Use: GET /users/:id
  - Guide: https://docs.example.com/migration
```

---

## Migration Guide

### Why Deprecating (Reason)

**Example:**
```markdown
## Why We're Deprecating /users/:id/profile

We're consolidating user endpoints to:
1. Simplify our API (fewer endpoints to learn)
2. Improve performance (single endpoint, less overhead)
3. Provide more data (new endpoint returns additional fields)
```

### What to Use Instead (Alternative)

**Example:**
```markdown
## What to Use Instead

Use `GET /users/:id` instead of `GET /users/:id/profile`.

The new endpoint returns all profile data plus additional fields.
```

### How to Migrate (Step-by-Step)

**Example:**
```markdown
## How to Migrate

### Step 1: Update API Call

**Before:**
```javascript
const profile = await fetch('/api/users/123/profile');
```

**After:**
```javascript
const user = await fetch('/api/users/123');
```

### Step 2: Update Response Handling

**Before:**
```javascript
const { bio, avatar, location } = profile;
```

**After:**
```javascript
const { bio, avatar, location } = user;
// Same fields, no changes needed
```

### Step 3: Test

Test your integration in staging before deploying to production.

### Step 4: Deploy

Deploy your changes before December 31, 2024.
```

### Code Examples (Before/After)

See above

### Timeline (When It Stops Working)

**Example:**
```markdown
## Timeline

- **June 1, 2024:** Deprecation announced
- **September 1, 2024:** Reminder email
- **December 1, 2024:** Final warning
- **December 31, 2024:** Endpoint stops working (410 Gone)
```

### Support Contact (If Help Needed)

**Example:**
```markdown
## Need Help?

- **Email:** api@example.com
- **Office Hours:** Fridays 2-3pm PT (https://meet.google.com/xxx)
- **Slack:** #api-support
- **Schedule Call:** https://calendly.com/api-team
```

---

## Monitoring Deprecated Usage

### Track API Calls to Deprecated Endpoints

See "Step 3: Monitor Usage" above

### Identify Top Users

**Query:**
```sql
SELECT
  client_id,
  COUNT(*) as call_count
FROM api_logs
WHERE endpoint = '/users/:id/profile'
  AND date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY client_id
ORDER BY call_count DESC
LIMIT 10;
```

### Usage Trends (Is It Declining?)

**Chart:**
```
Calls/Day to /users/:id/profile

5000 |     ●
4000 |   ●
3000 | ●
2000 |       ●
1000 |         ●
   0 |___________●___
     Jun Jul Aug Sep Oct Nov

Trend: ↓ Declining (good!)
```

### Alert When Usage Spikes

**Alert:**
```
Alert: Deprecated endpoint usage spike
Endpoint: /users/:id/profile
Current: 5,000 calls/day
Previous: 1,000 calls/day
Change: +400%

Action: Investigate (new client using deprecated endpoint?)
```

---

## Outreach to Users

### Email Top Users (Direct Outreach)

See "Step 4: Reach Out to Active Users" above

### Offer Migration Support

**Email:**
```
Need help migrating?

We offer:
- 1-on-1 migration support calls
- Code review of your migration
- Extended sunset date (if needed)

Schedule a call: https://calendly.com/api-team
```

### Schedule Calls with Major Customers

**Process:**
```
1. Identify major customers (high usage)
2. Email to schedule call
3. Call: Explain deprecation, offer help
4. Follow up: Check migration progress
```

### Provide Early Access to New Version

**Email:**
```
Early Access: API v2

As a valued customer, we're offering early access to API v2.

Benefits:
- Test v2 before v1 sunset
- Provide feedback
- Smooth migration

Sign up: https://example.com/v2-early-access
```

---

## Handling Non-Compliant Users

### Repeated Notices

**Timeline:**
```
Month 0: Initial announcement
Month 3: Reminder email
Month 6: Second reminder
Month 9: Final warning
Month 11: Last chance email
Month 12: Sunset
```

### Escalation (Account Manager)

**Process:**
```
1. Email from API team (no response)
2. Email from account manager
3. Phone call from account manager
4. Executive escalation (if major customer)
```

### Final Warning (1 Month Before)

**Email:**
```
Subject: URGENT: Action Required - API v1 Sunset in 30 Days

Hi [Client],

This is a final warning that API v1 will stop working in 30 days (December 31, 2024).

We noticed you're still using:
- GET /users/:id/profile (500 calls/day)

Action required:
- Migrate to GET /users/:id immediately
- See migration guide: https://docs.example.com/migration

If you don't migrate, your integration will break on December 31.

Need help? Reply to this email ASAP.

Thank you,
API Team
```

### Hard Cutoff (Stop Working)

**Process:**
```
1. Sunset date reached
2. Return 410 Gone
3. Monitor for errors
4. Reach out to affected users
```

---

## Graceful Degradation

### Return 410 Gone (After Sunset)

See "Step 5: Sunset" above

### Helpful Error Message (Link to Guide)

**Example:**
```json
HTTP/1.1 410 Gone
Content-Type: application/json

{
  "error": "Endpoint Removed",
  "message": "GET /users/:id/profile was removed on 2024-12-31",
  "sunsetDate": "2024-12-31",
  "replacement": {
    "endpoint": "GET /users/:id",
    "documentation": "https://docs.example.com/api/users"
  },
  "migrationGuide": "https://docs.example.com/migration/profile-to-user",
  "support": "api@example.com"
}
```

### Optional: Temporary Disable (Test Waters)

**Process:**
```
1. Disable endpoint for 1 hour
2. Monitor errors
3. Identify affected users
4. Reach out
5. Re-enable
6. Give more time to migrate
```

---

## Versioning and Deprecation

### v1 Deprecated → Use v2

**Timeline:**
```
2024-06: Launch v2
2024-06: Deprecate v1 (12 month notice)
2025-06: Sunset v1
```

### Maintain v1 During Transition

**Support:**
```
v2: Active development
v1: Maintenance mode (bug fixes only, no new features)
```

### Eventually Remove v1

**Process:**
```
1. Sunset v1 (stop working)
2. Monitor for 1 month
3. Remove v1 code
4. Celebrate! 🎉
```

---

## Database Schema Deprecation

### Multi-Step Migration

See Backward Compatibility Rules skill

### Stop Writing to Old Column

**Step 1:**
```sql
-- Stop writing to 'name' column
-- Write to 'full_name' instead
```

### Stop Reading (Use New Column)

**Step 2:**
```sql
-- Stop reading from 'name' column
-- Read from 'full_name' instead
```

### Drop Old Column

**Step 3:**
```sql
-- After all code migrated
ALTER TABLE users DROP COLUMN name;
```

---

## Feature Flag Deprecation

### Mark Feature as Deprecated

**Code:**
```javascript
if (featureFlags.isEnabled('old-feature')) {
  console.warn('old-feature flag is deprecated. Will be removed in v2.0.0.');
  // Old feature code
}
```

### Monitor Usage

**Dashboard:**
```
Feature Flag: old-feature
Status: Deprecated
Sunset: 2024-12-31

Usage:
- Enabled for 10 users (down from 100)
- Last enabled: 2024-11-15
```

### Reach Out to Enabled Users

**Email:**
```
Subject: Feature Flag Deprecation: old-feature

Hi,

We noticed you have the 'old-feature' flag enabled.

This feature is deprecated and will be removed on 2024-12-31.

Action: Disable 'old-feature' flag and use 'new-feature' instead.

Need help? Reply to this email.
```

### Force Disable

**Process:**
```
1. Sunset date reached
2. Force disable flag for all users
3. Monitor for errors
4. Remove feature code
```

### Remove Code

**After Sunset:**
```javascript
// Remove old feature code
// Remove feature flag
```

---

## Real Deprecation Examples

### Twitter API v1 → v2

**Timeline:**
- 2020: v2 launched
- 2021: v1.1 deprecated
- 2023: v1.1 sunset (3 years notice!)

**Communication:**
- Blog posts
- Email campaigns
- Developer forums
- Migration guides

### GitHub API v3 Deprecations

**Process:**
- Announce deprecation in changelog
- Add deprecation headers
- Provide migration guide
- 12+ months notice
- Sunset

### Heroku Free Tier Sunset

**Timeline:**
- Aug 2022: Announced
- Nov 2022: Sunset (3 months notice)

**Controversy:**
- Short notice (3 months)
- No free alternative
- Many affected users

**Lesson:** Give more notice for major changes

---

## Templates

### Deprecation Announcement (Email)

See "Step 2: Announce" above

### Deprecation Announcement (Blog)

See "Step 2: Announce" above

### Migration Guide

See "Migration Guide" section above

### API Response Headers

See "Deprecation Headers" section above

---

## Summary

### Quick Reference

**Deprecation:** Announcing end-of-life with time to migrate

**Timeline:**
- APIs: 6-12 months
- Critical systems: 12-24 months
- Internal APIs: 3-6 months

**Process:**
1. Mark as deprecated (code, docs)
2. Announce (email, blog, changelog)
3. Monitor usage
4. Reach out to active users
5. Sunset (stop working)
6. Remove code

**Headers:**
- Deprecation: true
- Sunset: Date
- Link: Migration guide
- Warning: Message

**OpenAPI:**
```yaml
deprecated: true
description: Migration guide
```

**GraphQL:**
```graphql
@deprecated(reason: "Use X instead")
```

**Communication:**
- In-app notifications
- Email campaigns
- Blog post
- Changelog
- Status page
- Release notes

**Migration Guide:**
- Why deprecating
- What to use instead
- How to migrate (step-by-step)
- Code examples (before/after)
- Timeline
- Support contact

**Monitoring:**
- Track usage
- Identify top users
- Usage trends
- Alert on spikes

**Outreach:**
- Email top users
- Offer migration support
- Schedule calls
- Early access to new version

**Non-Compliant:**
- Repeated notices
- Escalation
- Final warning
- Hard cutoff

**Graceful Degradation:**
- 410 Gone
- Helpful error message
- Link to migration guide

**Versioning:**
- v1 deprecated → v2
- Maintain v1 during transition
- Eventually remove v1

## Overview

Deprecation Notices is the practice of announcing end-of-life for an API/feature with time for users to migrate before eventual removal.

### Lifecycle

```
Active → Deprecated → Sunset → Removed
Month 0:  Fully supported
Month 3: Deprecated (6-12 months notice)
Month 6: Final warning
Month 12: Sunset (stops working)
```

### Example

```
Jan 2024: API v1 active
Jun 2024: API v1 deprecated (announce v2)
Dec 2024: API v1 sunset (stops working)
Jan 2025: API v1 code removed
```

---

## Why Proper Deprecation Matters

### 1. Avoid Breaking Users Without Warning

**Without Deprecation:**
```
Deploy new version
→ All clients break immediately
→ Emergency rollback
→ Coordinate with all clients to update
→ Big bang migration (risky!)
```

**With Deprecation:**
```
Deploy new version
→ Old clients continue working
→ Clients migrate gradually
→ No coordination needed
```

### 2. Maintain Trust

**Trust Built By:**
- Advance notice (6-12 months)
- Clear migration path
- Support during migration
- No surprises

**Trust Broken By:**
- Sudden changes
- No warning
- Unclear migration
- Breaking without notice
```

### 3. Smooth Migration

**Gradual Migration:**
```
Month 0: Deploy v2 (backward compatible)
Month 1: 20% of clients migrated
Month 3: 50% of clients migrated
Month 6: 80% of clients migrated
Month 12: 100% migrated, deprecate v1
```

### 4. Reduce Coordination Overhead

**Without:**
- Coordinate deployment with all clients
- Schedule maintenance window
- Rollback plan if issues

**With:**
- Deploy anytime
- Clients migrate when ready
- No coordination needed
```

### 5. Customer Trust (Stable APIs)

**Trust:**
- "This API won't break my integration"
- "I can upgrade when I'm ready"
- "No surprises"

---

## Deprecation Timeline

### Typical: 6-12 Months for APIs

**Timeline:**
```
Month 0: Announce deprecation
Month 3: Reminder + usage stats
Month 6: Final warning
Month 12: Sunset
```

### Critical Systems: 12-24 Months

**Examples:**
- Banking APIs
- Healthcare systems
- Government integrations

**Why Longer:**
- Longer approval processes
- More stakeholders
- Higher risk

### Internal APIs: 3-6 Months

**Why Shorter:**
- Control both sides
- Faster coordination
- Lower risk

**Factors:**
- **Contract terms:** May require 12+ months
- **User base size:** More users = longer timeline
- **Criticality:** Mission-critical = longer timeline
- **Complexity:** Complex migration = longer timeline

---

## Deprecation Process

### Step 1: Mark as Deprecated (Code, Docs)

**Code (JavaScript):**
```javascript
/**
 * @deprecated Use getUser() instead. Will be removed in v2.0.0.
 * @see getUser
 */
function getUserProfile(id) {
  console.warn('getUserProfile is deprecated. Use getUser() instead.');
  return getUser(id);
}
```

**Code (Python):**
```python
import warnings

def get_user_profile(id):
    """
    .. deprecated:: 1.5.0
       Use :func:`get_user` instead.
    """
    warnings.warn(
        "get_user_profile is deprecated. Use get_user() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_user(id)
```

**Docs:**
```markdown
## GET /users/:id/profile

**⚠️ DEPRECATED:** This endpoint is deprecated and will be removed on December 31, 2024.

**Use instead:** `GET /users/:id`

**Migration guide:** https://docs.example.com/migration
```

### Step 2: Announce (Email, Blog, Changelog)

**Email:**
```
Subject: Deprecation Notice: /users/:id/profile endpoint

Hi developers,

We're deprecating the `/users/:id/profile` endpoint.

What's changing:
- Endpoint: GET /users/:id/profile
- Sunset date: December 31, 2024

Why:
- Consolidating user endpoints for simplicity
- New endpoint provides more data

Action required:
- Update your integration by December 31, 2024
- See migration guide: https://docs.example.com/migration

Need help?
- Reply to this email
- Schedule a call: https://calendly.com/api-team

Thank you,
API Team
```

**Blog Post:**
```markdown
# Deprecation Notice: /users/:id/profile Endpoint

**Date:** June 1, 2024

**Sunset Date:** December 31, 2024

We're deprecating the `/users/:id/profile` endpoint in favor of the consolidated `/users/:id` endpoint.

What's Changing
The `/users/:id/profile` endpoint will stop working on December 31, 2024.

Why
Consolidating user endpoints to simplify our API and provide a better developer experience.
The new endpoint returns all profile data plus additional fields.

Migration Guide
See our [migration guide](https://docs.example.com/migration) for step-by-step instructions.
```

### Step 3: Monitor Usage

**Track Deprecated Endpoint Usage:**
```javascript
app.get('/users/:id/profile', (req, res) => {
  // Track usage
  metrics.increment('deprecated.users_profile.calls', {
    client: req.headers['user-agent'],
    clientId: req.user?.clientId
  });

  // Return response with deprecation headers
  res.set('Deprecation', 'true');
  res.set('Sunset', 'Sat, 31 Dec 2024 23:59:59 GMT');
  res.set('Link', '<https://docs.example.com/migration>; rel="deprecation"');
  res.set('Warning', '299 - "This endpoint is deprecated. Use /users/:id instead. See https://docs.example.com/migration"');
  res.json(profile);
});
```

**Dashboard:**
```
Deprecated Endpoint: /users/:id/profile
Sunset Date: 2024-12-31 (6 months remaining)
Usage:
- Total calls/day: 1,000 (down from 5,000 last month)
- Top clients: mobile-app (500), web-app (300), partner-api (200)
```

---

## Deprecation Headers

**Sunset Header (RFC 8594):**
```
HTTP/1.1 200 OK
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: <https://docs.example.com/migration>; rel="sunset"
```

**Deprecation Header:**
```
HTTP/1.1 200 OK
Deprecation: true
Link: <https://docs.example.com/migration>; rel="deprecation"
```

**Warning Header:**
```
HTTP/1.1 200 OK
Warning: 299 - "This endpoint is deprecated. Use /v2/users instead. See https://docs.example.com/migration"
```

---

## Deprecation Policy (6-12 Months Notice)

**Timeline:**
```
Month 0: Announce deprecation
Month 3: Reminder + usage stats
Month 6: Final warning
Month 12: Sunset
```

---

## OpenAPI Deprecation

**deprecated: true**
```yaml
paths:
  /users/{id}/profile:
    get:
      deprecated: true
      summary: Get user profile (DEPRECATED)
      description: |
        **DEPRECATED:** This endpoint is deprecated and will be removed on 2024-12-31.
        
        **Use instead:** GET /users/{id}
```
```

---

## GraphQL Deprecation

**@deprecated Directive:**
```graphql
type User {
  id: ID!
  name: String! @deprecated(reason: "Use firstName and lastName instead")
  firstName: String!
  lastName: String!
}
```

---

## Code Deprecation

**@deprecated Annotation (Java):**
```java
/**
 * @deprecated Use getUser() instead. Will be removed in v2.0.0.
 * @see getUser
 */
@Deprecated
public User getUserProfile(String id) {
    return getUser(id);
}
```

**@deprecated JSDoc (JavaScript):**
```javascript
/**
 * @deprecated Use getUser() instead. Will be removed in v2.0.0.
 * @see getUser
 */
/**
 * @deprecated Use getUser() instead. Will be removed in v2.0.0.
 */
function getUserProfile(id) {
  console.warn('getUserProfile is deprecated. Use getUser() instead.');
  return getUser(id);
}
```

**warnings.warn (Python):**
```python
import warnings

def get_user_profile(id):
    """
    .. deprecated:: 1.5.0
       Use :func:`get_user` instead.
    """
    warnings.warn(
        "get_user_profile is deprecated. Use get_user() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return get_user(id)
```

---

## Monitoring Deprecated Usage

**Track Metrics:**
- Total calls/day
- Unique clients
- Top clients
- Trend (declining = good!)

---

## Reach Out to Active Users

**Email Top Users:**
```
Subject: Action Required: Migrate from /users/:id/profile

Hi [Client],

We noticed you're still using the deprecated /users/:id/profile endpoint (500 calls/day).

This endpoint will stop working on December 31, 2024 (3 months remaining).

Action required:
- Migrate to GET /users/:id immediately
- See migration guide: https://docs.example.com/migration

Need help?
- Reply to this email
- Schedule a call: https://calendly.com/api-team
- Schedule a call: https://calendly.com/api-team

Thank you,
API Team
```

---

## Graceful Degradation

### Optional: Temporary Disable

**Process:**
```
1. Disable endpoint for 1 hour
2. Monitor errors
3. Identify affected users
4. Reach out
5. Re-enable
6. Give more time to migrate
```

### Helpful Error Message

**410 Gone Response:**
```
HTTP/1.1 410 Gone
Content-Type: application/json

{
  "error": "This endpoint has been removed. Use /v2/users instead.",
  "migrationGuide": "https://docs.example.com/migration",
  "support": "api@example.com"
}
```

---

## Feature Flag Deprecation

### Mark Feature as Deprecated

**Code:**
```javascript
if (featureFlags.isEnabled('old-feature')) {
  console.warn('old-feature flag is deprecated. Will be removed in v2.0.0.');
}
```

---

## Database Schema Deprecation

### Multi-Step Migration

**Step 1: Stop Writing to Old Column**
```sql
-- Stop writing to 'name' column
-- Write to 'full_name' instead
```

**Step 2: Stop Reading (Use New Column)**
```sql
-- Stop reading from 'name' column
-- Read from 'full_name' instead
```

**Step 3: Drop Old Column**
```sql
-- After all code migrated
ALTER TABLE users DROP COLUMN name;
```

---

## Real Deprecation Examples

### Stripe API Evolution

**Characteristics:**
- Excellent consistency
- Comprehensive docs
- Versioning via headers
- Extensive examples
- Idempotency keys
- Webhooks (event-driven)

**Learn From:**
- Error format (detailed, helpful)
- Pagination (cursor-based)
- Deprecation notices
- Comprehensive SDKs

### GitHub API

**Characteristics:**
- RESTful design
- GraphQL alternative
- Deprecation notices
- Rate limiting

**Learn From:**
- Deprecation headers
- Preview features (opt-in)
- Comprehensive documentation

### Internal API Gateway Patterns

**Pattern:**
- All APIs go through API gateway
→ Gateway enforces governance
→ Rate limiting, auth, logging
→ Consistent experience

---

## Implementation

### Migration Guide

**Example:**
```markdown
## How to Migrate

### What's Changing
The `/users/:id/profile` endpoint is deprecated. Use `/users/:id` instead.

### Why
We're consolidating user endpoints to simplify our API and provide a better developer experience.

### How to Migrate

### Before
```javascript
const profile = await fetch('/api/users/123/profile');
```

### After
```javascript
const user = await fetch('/api/users/123');
```

### Timeline
- **June 1, 2024:** Deprecation announced
- **September 1, 2024:** Reminder email
- **December 1, 2024:** Final warning
- **December 31, 2024:** Endpoint stops working (410 Gone)
```

---

## Templates

### Deprecation Announcement (Email)

See "Step 2: Announce" section above

### Deprecation Announcement (Blog)

See "Step 2: Announce" section above

---

## Best Practices

### Communication
- [ ] Communicate changes early
- [ ] Provide migration guides
- [ ] Hold breaking change meetings
- [ ] Create data contracts with consumers
- [ ] Document breaking changes clearly
- [ ] Document breaking changes with dates
- [ ] Set appropriate notice period (6-12 months minimum)
- [ ] Monitor deprecated endpoint usage
- [ ] Track consumer adoption
- [ ] Reach out to active users
- [ ] Provide support during migration
- [ ] Send reminders at key milestones
- [ ]

### Documentation
- [ ] Document all breaking changes with dates
- [ ] Document breaking changes clearly
- [ ] Provide migration guides for consumers
- [ ] Document version compatibility
- [ ] Document migration timeline
- [ ] Document sunset dates
- [ ] Keep documentation in sync with code
- [ ] Use consistent deprecation headers
- [ ] Use appropriate deprecation headers
- [ ] Include migration guide links
- [ ] Document breaking changes in changelog
- [ ] Document examples in documentation
- [ ] Document breaking changes in API docs
- [ ] Document breaking changes in README
- [ ] Document breaking changes in Swagger UI
- [ ] Document breaking changes in ReDoc
- [ ]

### Migration
- [ ] Use zero-downtime migration pattern
- [ ] Use multi-step migrations for breaking changes
- [ ] Backfill data before removing old columns
- [ ] Test migrations in staging environment
- [ ] Provide rollback procedures
- [ ] Monitor migration progress
- [ ] Support consumers during migration
- [ ] Use feature flags for gradual rollout
- [ ] Maintain backward compatibility during migration
- [ ] Use canary deployments for testing
- [ ]

### Monitoring
- [ ] Track deprecated endpoint usage
- [ ] Monitor breaking change impacts
- [ ] Track consumer adoption of new schema
- [ ] Set up dashboards for API health
- [ ] Alert on high usage of deprecated endpoints
- [ ] Monitor migration success rates
- [ ] Track time to sunset
- [ ]

### Testing
- [ ] Test backward compatibility
- [ ] Test with production-like data
- [ ] Test migration scripts thoroughly
- [ ] Test graceful degradation scenarios
- [ ] Monitor test coverage
- [ ]

### Prevention
- [ ] Use data contracts for all shared data
- [ ] Enforce schema validation at source
- [ ] [ ] Implement CI/CD schema checks
- [ ]

### Version Control
- [ ] Use semantic versioning
- [ ] Tag all releases with version numbers
- [ ] Document version compatibility matrix
- [ ] Maintain backward compatibility
- [ ] Use @deprecated directive for breaking changes
- [ ]

### Legal Compliance
- [ ] Follow contract terms if applicable
- [ ] Provide minimum notice period
- [ ] Ensure migration support
- [ ] Document breaking changes clearly
- [ ] Provide migration guides
- [ ] Maintain deprecation records

### Checklist
- [ ] Define deprecation process
- [ ] Set appropriate notice period
- [ ] Document breaking changes clearly
- [ ] Provide migration guides
- [ ] Monitor deprecated endpoint usage
- [ ] Track consumer adoption
- [ ] Set up dashboards for API health
- [ ] Track migration success rates
- [ ] Test backward compatibility
- [ ] Test with production-like data
- [ ] Monitor test coverage
- [ ] Optimize deprecation headers
- [ ] Use feature flags for gradual rollout
- [ ] Use zero-downtime migrations
- [ ] Backfill data before removing old columns
- [ ] Test migrations in staging environment
- [ ] Have rollback procedures ready
- [ ] Monitor schema drift metrics
- [ ] Track breaking change impacts
- [ ] Track consumer adoption of new schema
- [ ] Set up change notifications
- [ ] Test with production-like data
- [ ] Monitor test coverage
- [ ] Optimize schema validation overhead
- [ ] Cache schema definitions
- [ ] Use efficient validation libraries
- [ ] Monitor schema performance impact
- [ ] Establish schema ownership
- [ ] Create schema review process
- [ ] Define schema lifecycle
- [ ] Plan schema deprecation strategy
- [ ] Set up incident response for violations
- [ ] Test schema validation logic
- [ ] Train team on deprecation best practices
