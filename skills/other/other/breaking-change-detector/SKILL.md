---
name: breaking-change-detector
description: Detect and warn about breaking API/schema changes before implementation. Auto-trigger when modifying API routes, database schemas, or public interfaces. Validates changes against api-strategy.md versioning rules. Suggests migration paths for breaking changes. Prevents removing endpoints, changing request/response formats, dropping database columns, modifying function signatures without deprecation.
---

<objective>
The breaking-change-detector skill prevents breaking changes from reaching production by detecting potentially breaking API, schema, and interface modifications before implementation.

Breaking changes destroy trust and break client applications:
- Removing API endpoints breaks existing integrations
- Changing request/response formats breaks client code
- Dropping database columns causes data loss
- Modifying function signatures breaks dependent code
- Changing authentication schemes locks out users

This skill acts as a safety gate that:
1. **Detects** breaking changes before they're implemented
2. **Warns** developers with severity levels (CRITICAL, HIGH, MEDIUM)
3. **Suggests** safe migration paths (versioning, deprecation, backward compatibility)
4. **Validates** changes against project's API versioning strategy (from api-strategy.md)
5. **Blocks** deployment if critical breaking changes lack migration plan

The result: Zero unintentional breaking changes, smooth API evolution, maintained client trust.
</objective>

<quick_start>
<trigger_pattern>
Auto-trigger when detecting these modification patterns:

**API modifications**:
- "Remove endpoint", "Delete route", "Drop API"
- "Change request/response", "Modify payload", "Update schema"
- "Rename endpoint", "Change HTTP method"

**Database modifications**:
- "Drop column", "Remove field", "Delete table"
- "Change column type", "Modify constraint"
- "Rename column/table"

**Interface modifications**:
- "Change function signature", "Modify parameters"
- "Remove method", "Delete class"
- "Change return type"
</trigger_pattern>

<basic_workflow>
**Step 1**: Detect modification type
- User: "Remove the /api/v1/users endpoint"
- Detected: API endpoint deletion (BREAKING)

**Step 2**: Analyze breaking change risk
- Check: Is endpoint currently in use?
- Check: Are there clients depending on it?
- Check: What's the versioning strategy?

**Step 3**: Determine severity
- CRITICAL: Removing production endpoint with active users
- HIGH: Changing required field in request
- MEDIUM: Adding required parameter to function

**Step 4**: Suggest safe migration path
- **Option A**: Deprecate endpoint (mark for removal in v2.0)
- **Option B**: Version API (keep v1, add v2 without endpoint)
- **Option C**: Redirect to replacement endpoint

**Step 5**: Validate against api-strategy.md
- Check project's versioning policy
- Verify deprecation timeline
- Confirm backward compatibility requirements

**Step 6**: Block or warn
- CRITICAL → BLOCK implementation until migration plan approved
- HIGH → WARN and require justification
- MEDIUM → LOG for review
</basic_workflow>

<immediate_value>
**Without breaking-change-detector**:
```
Developer: "Let me remove this old /api/users endpoint"
*Removes endpoint*
*Deploys*
Result: 15 mobile apps break, support tickets flood in, emergency rollback
```

**With breaking-change-detector**:
```
Developer: "Let me remove this old /api/users endpoint"
Detector: "🚨 BREAKING CHANGE DETECTED

Removing: GET /api/users
Severity: CRITICAL
Impact: 15 active clients (iOS app, Android app, web dashboard)

This will break:
- Mobile app v2.1-2.5 (500K users)
- Partner integrations (3 companies)

Safe migration path:
1. Deprecate endpoint (add X-Deprecated header)
2. Announce removal timeline (90 days)
3. Monitor usage (track who's still calling it)
4. Version API (v2 without endpoint, v1 keeps it)
5. Remove after 90 days when usage drops to 0

Cannot proceed without migration plan. Would you like me to implement the deprecation strategy?"

Developer: "Yes, let's deprecate it properly"
Result: Smooth transition, zero broken clients, maintained trust
```
</immediate_value>
</quick_start>

<workflow>
<step number="1">
**Detect modification intent**

Parse user request to identify change type:

**API endpoint changes**:
- Removal: "remove", "delete", "drop" + "endpoint", "route", "API"
- Modification: "change", "update", "modify" + "request", "response", "payload"
- Renaming: "rename", "move" + "endpoint"

**Database schema changes**:
- Column removal: "drop", "remove" + "column", "field"
- Type changes: "change type", "alter column"
- Table changes: "drop table", "remove table"

**Interface/contract changes**:
- Function signature: "change signature", "modify parameters", "update return type"
- Method removal: "remove method", "delete function"
- Required fields: "make required", "add required"

See [references/change-detection-patterns.md](references/change-detection-patterns.md) for complete patterns.
</step>

<step number="2">
**Classify breaking change type**

Categorize the detected change:

**Type 1: Hard breaking changes** (always break clients):
- Removing endpoint
- Changing endpoint URL
- Changing HTTP method (GET → POST)
- Removing required field from response
- Adding required field to request
- Dropping database column
- Changing authentication scheme

**Type 2: Soft breaking changes** (may break some clients):
- Changing response field type
- Changing error codes
- Adding required query parameter
- Changing default behavior
- Modifying rate limits

**Type 3: Non-breaking changes** (safe):
- Adding optional field to request
- Adding new field to response
- Adding new endpoint
- Deprecating (but not removing) endpoint
- Making required field optional

See [references/breaking-change-taxonomy.md](references/breaking-change-taxonomy.md) for full classification.
</step>

<step number="3">
**Assess impact scope**

Determine who/what will be affected:

**For API changes**:
1. **Find endpoint usage**:
   - Grep codebase for endpoint URL
   - Check API logs for recent requests
   - Identify client applications (mobile app, web app, partners)

2. **Estimate client count**:
   - Internal clients (known)
   - External clients (unknown, but logged)
   - Partner integrations (contractual obligations)

3. **Determine criticality**:
   - Production traffic volume
   - Business-critical operations
   - SLA commitments

**For database changes**:
1. **Find column usage**:
   - Grep for column references in code
   - Check ORM model usage
   - Identify dependent queries

2. **Assess data impact**:
   - How much data would be lost?
   - Can data be migrated?
   - Are there backups?

**For interface changes**:
1. **Find function usage**:
   - Grep for function calls
   - Check import statements
   - Identify dependent modules

2. **Determine coupling**:
   - How many call sites?
   - Internal vs external API?
   - Published vs private interface?
</step>

<step number="4">
**Determine severity level**

Assign severity based on impact:

**CRITICAL** (blocks deployment):
- Removing production endpoint with >100 requests/day
- Dropping database column with data
- Changing authentication that locks out users
- Breaking partner integration with SLA
- Modifying public API without versioning

**HIGH** (requires approval):
- Removing endpoint with <100 requests/day
- Changing required request fields
- Modifying response format
- Changing function signature in public API
- Altering database constraints

**MEDIUM** (requires documentation):
- Adding required parameter with default
- Changing optional field types
- Modifying error messages
- Updating rate limits
- Changing internal interfaces

**LOW** (informational):
- Adding optional fields
- Deprecating (not removing)
- Adding new endpoints
- Improving error messages
- Internal refactoring
</step>

<step number="5">
**Load versioning strategy**

Read project's API versioning policy from `docs/project/api-strategy.md`:

**Common strategies**:

**URL versioning**: `/api/v1/users`, `/api/v2/users`
- Breaking changes → Bump major version
- Keep old version running for deprecation period
- Client chooses version in URL

**Header versioning**: `Accept: application/vnd.app.v1+json`
- Breaking changes → New version in Accept header
- Server negotiates version
- Client specifies version in header

**No versioning** (deprecation only):
- No breaking changes allowed
- All changes must be backward compatible
- Use deprecation headers for removal

**Example api-strategy.md**:
```markdown
# API Versioning Strategy

**Strategy**: URL versioning (/api/v1, /api/v2)

**Breaking change policy**:
- Major version bump required (v1 → v2)
- Old version supported for 6 months minimum
- Deprecation notice 90 days before removal
- Monitor usage, remove when <1% traffic

**Backward compatibility requirements**:
- New fields are optional
- Removed fields are deprecated first (90 days)
- Response format changes require new version
```

If api-strategy.md doesn't exist, use conservative defaults:
- URL versioning
- 6 month deprecation period
- Backward compatibility required
</step>

<step number="6">
**Suggest safe migration path**

Provide options based on change type and versioning strategy:

**For endpoint removal**:
```
Option A: Deprecation strategy
1. Add X-Deprecated header to endpoint
2. Add warning to API docs
3. Email clients (if known)
4. Monitor usage for 90 days
5. Remove when usage drops to 0

Option B: API versioning
1. Keep endpoint in /api/v1
2. Remove from /api/v2
3. Redirect v1 → v2 replacement (if exists)
4. Sunset v1 after 6 months

Option C: Soft delete
1. Return 410 Gone instead of 404
2. Include migration instructions in response
3. Log attempts for monitoring
```

**For schema changes**:
```
Option A: Additive migration
1. Add new column (don't drop old)
2. Dual-write to both columns
3. Migrate existing data
4. Update code to use new column
5. Drop old column in future version

Option B: Versioned schema
1. Create new table (users_v2)
2. Dual-write to both tables
3. Migrate readers to new table
4. Drop old table after migration

Option C: Nullable transition
1. Make column nullable (don't drop)
2. Update code to handle null
3. Backfill default values
4. Make required again if needed
```

**For interface changes**:
```
Option A: Deprecate + replace
1. Mark function as @deprecated
2. Create new function with new signature
3. Update call sites gradually
4. Remove deprecated function in major version

Option B: Overload
1. Add new overload with new signature
2. Keep old overload functional
3. Route to implementation
4. Remove old overload later

Option C: Default parameters
1. Add new parameters with defaults
2. Backward compatible (old calls still work)
3. No breaking change
```

See [references/migration-strategies.md](references/migration-strategies.md) for complete playbook.
</step>

<step number="7">
**Block or warn**

Based on severity, take action:

**CRITICAL → BLOCK**:
```
🚨 BREAKING CHANGE BLOCKED

Cannot proceed with this change without migration plan.

Change: Remove GET /api/users
Severity: CRITICAL
Impact: 500K users (mobile app), 3 partner integrations

Required before proceeding:
[ ] Migration plan documented
[ ] Stakeholders notified
[ ] Deprecation timeline agreed
[ ] Monitoring in place
[ ] Rollback plan ready

Would you like me to implement the recommended deprecation strategy?
```

**HIGH → WARN**:
```
⚠️ BREAKING CHANGE DETECTED

This change will break existing clients.

Change: Add required field "country" to POST /api/users
Severity: HIGH
Impact: Web app, mobile apps will fail validation

Recommended migration:
1. Make field optional initially
2. Update all clients to send field
3. Make field required in v2.0

Proceed anyway? [y/N]
```

**MEDIUM → LOG**:
```
ℹ️ Breaking change detected (MEDIUM severity)

Change: Change validation error format
Impact: Clients parsing error messages

Document this change in:
- CHANGELOG.md
- API migration guide
- Release notes

Proceeding with implementation...
```
</step>
</workflow>

<detection_rules>
<api_endpoint_changes>
**Removal detection**:
```typescript
// Grep patterns
"router\\.delete.*'[^']*'" → Endpoint removal
"app\\..*\\.delete" → Express route removal
"// TODO: remove|// deprecated" → Marked for removal

// File deletions
routes/*.ts deleted → Endpoint removal
controllers/*.ts deleted → Controller removal
```

**Modification detection**:
```typescript
// Request schema changes
"interface.*Request.*{" (before/after diff)
"@Body.*:" (parameter changes)
"validate.*schema" (validation changes)

// Response schema changes
"interface.*Response.*{" (before/after diff)
"res.json({" (response format changes)

// HTTP method changes
"router.get" → "router.post" (method change)
```

**Examples**:
```typescript
// BREAKING: Endpoint removal
- router.get('/api/users/:id', ...)  // Removed
// Severity: CRITICAL

// BREAKING: Required field added
interface CreateUserRequest {
  name: string;
  email: string;
+ country: string;  // NEW REQUIRED FIELD
}
// Severity: HIGH

// BREAKING: Response field removed
interface UserResponse {
  id: string;
  name: string;
- email: string;  // REMOVED
}
// Severity: HIGH
```
</api_endpoint_changes>

<database_schema_changes>
**Column removal detection**:
```sql
-- Prisma schema
- email String  // Removed
// Severity: CRITICAL (data loss)

-- SQL migration
ALTER TABLE users DROP COLUMN email;
// Severity: CRITICAL (data loss)
```

**Type changes**:
```sql
-- Changing column type
ALTER TABLE users ALTER COLUMN age TYPE varchar;  // was integer
// Severity: HIGH (data conversion required)
```

**Constraint changes**:
```sql
-- Adding NOT NULL to existing column
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
// Severity: HIGH (existing nulls will fail)

-- Removing constraint
ALTER TABLE users DROP CONSTRAINT users_email_unique;
// Severity: MEDIUM (behavior change)
```

**Table changes**:
```sql
DROP TABLE users;
// Severity: CRITICAL (data loss + code breaks)

ALTER TABLE users RENAME TO customers;
// Severity: CRITICAL (all queries break)
```
</database_schema_changes>

<interface_changes>
**Function signature changes**:
```typescript
// Parameter removal
- function getUser(id: string, includeDeleted: boolean)
+ function getUser(id: string)
// Severity: HIGH (callers passing 2 params break)

// Parameter type change
- function processOrder(id: string)
+ function processOrder(id: number)
// Severity: HIGH (type mismatch)

// Return type change
- function getUsers(): User[]
+ function getUsers(): Promise<User[]>  // Now async
// Severity: CRITICAL (breaks all callers)
```

**Method removal**:
```typescript
class UserService {
- async deleteUser(id: string) { }  // Removed
}
// Severity: HIGH (callers break)
```

**Required property addition**:
```typescript
interface Config {
  apiKey: string;
+ environment: string;  // NEW REQUIRED
}
// Severity: HIGH (existing configs invalid)
```
</interface_changes>

<authentication_changes>
**Auth scheme changes**:
```typescript
// Changing auth method
- @UseGuards(JwtAuthGuard)  // Was JWT
+ @UseGuards(OAuth2Guard)    // Now OAuth2
// Severity: CRITICAL (clients locked out)

// Adding auth to public endpoint
- router.get('/api/public')
+ router.get('/api/public', authMiddleware)
// Severity: CRITICAL (public → authenticated)
```

**Permission changes**:
```typescript
// Changing required role
- @RequireRole('user')
+ @RequireRole('admin')
// Severity: HIGH (users lose access)
```
</authentication_changes>
</detection_rules>

<auto_trigger_conditions>
<when_to_trigger>
**File modification triggers**:
- Editing `**/routes/**/*.ts` → Check for endpoint changes
- Editing `**/schema/*.prisma` → Check for schema changes
- Editing `**/*.migration.sql` → Check for database changes
- Editing `**/interfaces/**/*.ts` → Check for contract changes
- Editing `**/controllers/**/*.ts` → Check for API changes

**Code pattern triggers**:
- Deleting routes/endpoints
- Removing database columns
- Changing function signatures
- Modifying request/response types
- Changing authentication

**User intent triggers**:
- "Remove endpoint"
- "Drop column"
- "Change request format"
- "Update API"
- "Modify schema"
</when_to_trigger>

<when_not_to_trigger>
**Safe changes** (don't trigger):
- Adding new endpoints
- Adding optional fields
- Adding database columns
- Adding new functions
- Improving error messages (content, not format)
- Internal refactoring (no public API change)

**Explicitly marked safe**:
- Changes in `**/internal/**` (not public API)
- Changes marked `// SAFE: backward compatible`
- Changes in feature flags (not yet released)
</when_not_to_trigger>

<proactive_detection>
**Before modification**:
When user says "Remove GET /api/users":
1. Parse intent (endpoint removal)
2. Immediately trigger breaking-change-detector
3. Analyze impact BEFORE writing code
4. Present migration options
5. Block if CRITICAL
6. Get approval if HIGH
7. Proceed only after approval

**During code review**:
Before creating PR/commit:
1. Diff current code vs modified code
2. Detect breaking changes in diff
3. Block commit if CRITICAL without migration plan
4. Warn in PR description if HIGH
5. Log in commit message if MEDIUM
</proactive_detection>
</auto_trigger_conditions>

<examples>
<example name="api-endpoint-removal">
**Request**: "Remove the deprecated /api/v1/stats endpoint"

**Detection**:
```
Change type: API endpoint removal
File: routes/stats.ts
Line: router.get('/api/v1/stats', ...)
Action: DELETE
```

**Impact analysis**:
```bash
# Search for endpoint usage
grep -r "/api/v1/stats" --include="*.ts" --include="*.js"

Found:
- Frontend: src/services/api.ts (1 call)
- Mobile app: Documented in integration guide
- API logs: 450 requests/day

Clients:
- Web dashboard (internal, can update)
- Mobile app v2.3 (external, 10K users)
- Unknown clients (logged as "curl/7.0", "Python requests")
```

**Severity determination**:
```
Traffic: 450 requests/day → Moderate usage
Clients: External mobile app → Cannot force update
Unknown clients: Present → Unpredictable impact

Severity: CRITICAL
Reason: External clients depend on endpoint
```

**Migration suggestion**:
```
🚨 BREAKING CHANGE BLOCKED

Cannot remove /api/v1/stats - active external usage detected.

Impact:
- Mobile app v2.3 (10K users)
- Unknown clients (curl, Python scripts)
- 450 requests/day

Safe migration path (RECOMMENDED):

Phase 1: Deprecation (Days 0-90)
1. Add response header: X-Deprecated: "true; sunset=2025-03-01; replacement=/api/v2/analytics"
2. Add deprecation notice to API docs
3. Email known clients (mobile team)
4. Log warnings when endpoint called

Phase 2: Monitoring (Days 0-90)
1. Track usage metrics
2. Identify remaining clients (log User-Agent)
3. Reach out to high-volume clients

Phase 3: Removal (Day 90+)
1. Wait until usage < 10 requests/day
2. Return 410 Gone with migration instructions
3. Monitor for spikes (indicates missed client)
4. Remove code after 30 days at 410

Estimated timeline: 4 months

Would you like me to implement Phase 1 (deprecation)?
```

**Implementation** (if approved):
```typescript
// routes/stats.ts (DEPRECATE, don't remove)
router.get('/api/v1/stats',
  deprecationMiddleware({
    sunset: '2025-03-01',
    replacement: '/api/v2/analytics',
    message: 'This endpoint is deprecated and will be removed on 2025-03-01'
  }),
  statsController.getStats  // Keep working
);

// middleware/deprecation.ts (NEW)
export function deprecationMiddleware(options: DeprecationOptions) {
  return (req, res, next) => {
    res.header('X-Deprecated', 'true');
    res.header('Sunset', options.sunset);
    res.header('Link', `<${options.replacement}>; rel="successor-version"`);

    logger.warn('Deprecated endpoint called', {
      endpoint: req.path,
      client: req.get('User-Agent'),
      ip: req.ip,
      sunset: options.sunset
    });

    next();
  };
}
```

See [examples/api-endpoint-removal-full.md](examples/api-endpoint-removal-full.md) for complete example.
</example>

<example name="database-schema-change">
**Request**: "Drop the 'phone' column from users table, we're using email only now"

**Detection**:
```
Change type: Database column removal
Table: users
Column: phone
Action: DROP COLUMN
```

**Impact analysis**:
```bash
# Search for column usage
grep -r "\.phone\|phone:" --include="*.ts"

Found:
- models/User.ts: phone: string
- services/UserService.ts: user.phone (3 references)
- controllers/UserController.ts: req.body.phone (1 reference)
- Database: 15,000 users have phone numbers (non-null)

Data at risk: 15,000 phone numbers
Code impact: 5 files, 10 references
```

**Severity determination**:
```
Data loss: 15,000 records → CRITICAL
Code breakage: 5 files → HIGH
Rollback difficulty: Cannot recover deleted data → CRITICAL

Severity: CRITICAL
Reason: Irreversible data loss
```

**Migration suggestion**:
```
🚨 BREAKING CHANGE BLOCKED

Cannot drop users.phone column - data loss risk.

Impact:
- 15,000 users have phone numbers (data loss)
- 5 files reference phone column (code breaks)
- No backup of phone data

Safe migration path (RECOMMENDED):

Option A: Soft delete (SAFEST)
1. Rename column: phone → phone_deprecated
2. Make column nullable
3. Update code to not use phone
4. Keep data for 6 months
5. Drop column after verification period

Option B: Archive before delete
1. Export phone data to archive table
2. Create users_phone_archive(user_id, phone, archived_at)
3. Copy data: INSERT INTO users_phone_archive SELECT id, phone FROM users
4. Verify archive: Check row counts match
5. Drop column from users table
6. Keep archive table indefinitely

Option C: Make nullable (don't drop)
1. ALTER TABLE users ALTER COLUMN phone DROP NOT NULL
2. Update code to handle null
3. Set existing phones to null (or keep them)
4. Column exists but unused (no data loss)

Which option do you prefer? I recommend Option B (archive).
```

See [examples/database-column-removal.md](examples/database-column-removal.md) for complete example.
</example>

<example name="function-signature-change">
**Request**: "Change getUserById to return Promise<User | null> instead of Promise<User>"

**Detection**:
```
Change type: Function signature modification
Function: getUserById
Return type change: Promise<User> → Promise<User | null>
```

**Impact analysis**:
```typescript
// Search for function calls
grep -r "getUserById" --include="*.ts"

Found 23 call sites:
- controllers/UserController.ts (3 calls)
- services/OrderService.ts (5 calls)
- services/NotificationService.ts (2 calls)
- ... (13 more files)

None handle null return:
const user = await getUserById(id);
user.name  // Will throw if null
```

**Severity determination**:
```
Call sites: 23 locations
Null handling: 0/23 handle null
Impact: Runtime errors (Cannot read 'name' of null)

Severity: HIGH
Reason: Breaks existing code with runtime errors
```

**Migration suggestion**:
```
⚠️ BREAKING CHANGE DETECTED

Changing getUserById return type to nullable breaks 23 call sites.

Current: Promise<User> (never null)
Proposed: Promise<User | null> (can be null)

Impact:
- 23 call sites assume non-null
- Will throw "Cannot read property of null" at runtime
- Requires updating all callers

Safe migration path:

Option A: Deprecate + replace (RECOMMENDED)
1. Keep getUserById as-is (throws if not found)
2. Create findUserById that returns User | null
3. Update callers gradually to findUserById
4. Mark getUserById as @deprecated
5. Remove getUserById in v2.0

Option B: Update all callers first
1. Find all 23 call sites
2. Add null checks: if (!user) throw new NotFoundError()
3. Then change return type
4. Runtime-safe, but large changeset

Option C: Overload (TypeScript only)
1. Add overload: getUserById(id, options: { throwIfNotFound: false }): Promise<User | null>
2. Keep default: getUserById(id): Promise<User>
3. Backward compatible

Recommended: Option A (new function)
```

**Implementation** (Option A):
```typescript
// services/UserService.ts

/**
 * Get user by ID
 * @deprecated Use findUserById instead. This will be removed in v2.0.
 * @throws NotFoundError if user doesn't exist
 */
async getUserById(id: string): Promise<User> {
  const user = await this.findUserById(id);
  if (!user) {
    throw new NotFoundError(`User ${id} not found`);
  }
  return user;
}

/**
 * Find user by ID
 * @returns User if found, null otherwise
 */
async findUserById(id: string): Promise<User | null> {
  return await prisma.user.findUnique({ where: { id } });
}
```

See [examples/function-signature-change.md](examples/function-signature-change.md).
</example>
</examples>

<anti_patterns>
<anti_pattern name="ignoring-detection">
**Problem**: Ignoring breaking change warnings

**Bad approach**:
```
Detector: "⚠️ This will break clients"
Developer: "It's fine, I'll fix it later" *proceeds anyway*
Result: Production breaks, emergency rollback
```

**Correct approach**:
```
Detector: "⚠️ This will break clients"
Developer: "Let me implement the migration path first"
*Implements deprecation strategy*
*Then makes change safely*
```

**Rule**: NEVER ignore CRITICAL warnings. HIGH warnings require approval. MEDIUM warnings require documentation.
</anti_pattern>

<anti_pattern name="removing-without-deprecation">
**Problem**: Removing endpoints/features directly without deprecation period

**Bad approach**:
```sql
-- Just drop it
DROP TABLE old_users;
```

**Correct approach**:
```sql
-- Deprecate first
ALTER TABLE old_users RENAME TO old_users_deprecated;

-- Add deprecation notice
COMMENT ON TABLE old_users_deprecated IS 'DEPRECATED: Use users table instead. Will be dropped 2025-06-01';

-- Monitor usage (if any queries fail, we know what's still using it)

-- Drop after deprecation period
DROP TABLE old_users_deprecated;  -- 6 months later
```

**Rule**: Deprecate first, remove later (after monitoring period).
</anti_pattern>

<anti_pattern name="changing-without-versioning">
**Problem**: Changing API behavior without version bump

**Bad approach**:
```typescript
// v1 returns array
GET /api/users → [{ id: 1 }, { id: 2 }]

// Changed to pagination (BREAKING)
GET /api/users → { items: [...], total: 2, page: 1 }
```

**Correct approach**:
```typescript
// v1 unchanged
GET /api/v1/users → [{ id: 1 }, { id: 2 }]

// v2 with pagination
GET /api/v2/users → { items: [...], total: 2, page: 1 }
```

**Rule**: Breaking changes require version bump (or deprecation path if not versioned).
</anti_pattern>

<anti_pattern name="data-loss-without-backup">
**Problem**: Dropping columns/tables without archiving data

**Bad approach**:
```sql
ALTER TABLE users DROP COLUMN legacy_id;  -- Data gone forever
```

**Correct approach**:
```sql
-- Archive first
CREATE TABLE users_legacy_data AS
SELECT id, legacy_id FROM users;

-- Then drop
ALTER TABLE users DROP COLUMN legacy_id;

-- Keep archive for 12 months
```

**Rule**: Archive before delete. Data recovery is impossible after DROP.
</anti_pattern>
</anti_patterns>

<validation>
<success_indicators>
Breaking-change-detector successfully applied when:

1. **Detection accuracy**: >95% of breaking changes detected before implementation
2. **False positive rate**: <10% (most warnings are genuine breaking changes)
3. **Blocked changes**: 100% of CRITICAL changes blocked until migration plan exists
4. **Migration paths**: Every blocked change receives 2-3 migration options
5. **Zero incidents**: No production breaking changes from detected issues
6. **Deprecation compliance**: All removals follow project's deprecation timeline
7. **Versioning compliance**: Breaking changes follow api-strategy.md versioning rules
</success_indicators>

<metrics>
Track breaking change prevention:

**Detection metrics**:
- Breaking changes detected (before implementation)
- False positives (warnings for non-breaking changes)
- False negatives (breaking changes missed)

**Prevention metrics**:
- CRITICAL changes blocked
- HIGH changes approved with migration plan
- Breaking changes that reached production (should be 0)

**Migration metrics**:
- Deprecation periods followed
- Safe migration paths implemented
- Client impact (number affected, downtime avoided)
</metrics>

<validation_checklist>
Before allowing breaking change implementation:

**CRITICAL severity**:
- [ ] Impact assessed (number of clients, data at risk)
- [ ] Migration plan documented
- [ ] Stakeholders notified (product, support, clients)
- [ ] Deprecation timeline agreed
- [ ] Monitoring in place (track usage, detect issues)
- [ ] Rollback plan ready
- [ ] Approval obtained from tech lead/architect

**HIGH severity**:
- [ ] Migration path chosen
- [ ] Code changes planned
- [ ] Backward compatibility considered
- [ ] Documentation updated
- [ ] Tests updated
- [ ] Changelog entry added

**MEDIUM severity**:
- [ ] Change documented in CHANGELOG
- [ ] Migration guide updated (if exists)
- [ ] Breaking change noted in commit message
</validation_checklist>
</validation>

<reference_guides>
For deeper topics, see reference files:

**Change detection**: [references/change-detection-patterns.md](references/change-detection-patterns.md)
- Comprehensive detection patterns for all change types
- Grep/Glob patterns for finding modifications
- Before/after diff analysis

**Breaking change taxonomy**: [references/breaking-change-taxonomy.md](references/breaking-change-taxonomy.md)
- Complete classification of breaking vs non-breaking changes
- Examples for API, database, interface changes
- Severity scoring rubric

**Migration strategies**: [references/migration-strategies.md](references/migration-strategies.md)
- Complete playbook for safe migrations
- Deprecation workflows
- Versioning strategies
- Data archival patterns

**Integration with workflow**: [references/workflow-integration.md](references/workflow-integration.md)
- Integration with /plan phase
- Integration with /implement phase
- Integration with /optimize phase
- Git hooks for pre-commit detection
</reference_guides>

<success_criteria>
The breaking-change-detector skill is successfully applied when:

1. **Automatic detection**: Triggers before any API/schema/interface modification
2. **Severity assigned**: Every change classified (CRITICAL/HIGH/MEDIUM/LOW)
3. **Impact assessed**: Scope determined (clients affected, data at risk, code impacted)
4. **Migration suggested**: 2-3 safe migration paths provided
5. **Policy validated**: Changes checked against api-strategy.md versioning rules
6. **Critical blocked**: CRITICAL changes cannot proceed without migration plan
7. **High approved**: HIGH changes require explicit approval
8. **Medium logged**: MEDIUM changes documented in CHANGELOG
9. **Zero production breaks**: No unintentional breaking changes reach production
10. **Smooth evolution**: APIs evolve safely with maintained client trust
</success_criteria>
