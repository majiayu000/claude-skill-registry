---
name: local-env
description: Local environment management - run SQL queries, set up fake payments, reset test data. Use when the user needs help with local database operations or test data setup.
---

# Local Environment Management

Help with local development environment tasks for daily-api.

## Database Access

PostgreSQL runs locally via Docker in a k8s container.

### Finding the Container

```bash
docker ps --format "table {{.Names}}" | grep "k8s_app_postgres"
```

### Running Queries

```bash
docker exec <CONTAINER_NAME> psql -U postgres -d api -c "YOUR SQL QUERY"
```

For multi-line queries:

```bash
docker exec <CONTAINER_NAME> psql -U postgres -d api <<'EOF'
SELECT * FROM users LIMIT 1;
EOF
```

## Fake Payment Setup

Payment status for opportunities is tracked on the **Organization** level via `recruiterSubscriptionFlags`. Opportunities also store subscription info in their `flags` column.

### Organization Subscription Fields

| Field | Description |
|-------|-------------|
| `status` | Must be `'active'` for payment validation to pass |
| `provider` | Use `'paddle'` |
| `items[].quantity` | Number of opportunity "seats" available |
| `items[].priceId` | Price ID that opportunities reference |

### Opportunity Flags Fields

| Field | Description |
|-------|-------------|
| `plan` | Must match a `priceId` from the org's subscription items |
| `batchSize` | Number of candidates per batch |

### Fake Payment for Organization

```sql
UPDATE organization
SET "recruiterSubscriptionFlags" = jsonb_build_object(
  'status', 'active',
  'provider', 'paddle',
  'subscriptionId', 'fake_sub_123',
  'createdAt', now(),
  'updatedAt', now(),
  'items', jsonb_build_array(
    jsonb_build_object('priceId', 'pri_fake_123', 'quantity', 5)
  )
)
WHERE id = 'ORGANIZATION_ID';
```

Reset: `UPDATE organization SET "recruiterSubscriptionFlags" = '{}' WHERE id = 'ORGANIZATION_ID';`

### Fake Payment for Opportunity

Requires updating both the organization AND the opportunity:

```sql
-- Step 1: Update organization subscription
UPDATE organization
SET "recruiterSubscriptionFlags" = jsonb_build_object(
  'status', 'active',
  'provider', 'paddle',
  'subscriptionId', 'fake_sub_123',
  'createdAt', now(),
  'updatedAt', now(),
  'items', jsonb_build_array(
    jsonb_build_object('priceId', 'pri_fake_123', 'quantity', 5)
  )
)
WHERE id = (SELECT "organizationId" FROM opportunity WHERE id = 'OPPORTUNITY_ID');

-- Step 2: Update opportunity flags
UPDATE opportunity
SET flags = flags || jsonb_build_object(
  'plan', 'pri_fake_123',
  'batchSize', 50
)
WHERE id = 'OPPORTUNITY_ID';
```

Reset:
```sql
UPDATE organization SET "recruiterSubscriptionFlags" = '{}'
WHERE id = (SELECT "organizationId" FROM opportunity WHERE id = 'OPPORTUNITY_ID');

UPDATE opportunity SET flags = flags - 'plan' - 'batchSize'
WHERE id = 'OPPORTUNITY_ID';
```

## Opportunity State Management

The `opportunity` table uses a `state` column (integer) to track lifecycle status. Values come from `OpportunityState` enum in `@dailydotdev/schema`.

### OpportunityState Values

| Value | Name | Description |
|-------|------|-------------|
| 0 | UNSPECIFIED | Default/unset |
| 1 | DRAFT | Not yet published |
| 2 | LIVE | Active and visible |
| 3 | CLOSED | No longer active |
| 4 | IN_REVIEW | Pending review |

### Update Opportunity State

```sql
-- Set to LIVE
UPDATE opportunity SET state = 2 WHERE id = 'OPPORTUNITY_ID' RETURNING id, state, title;

-- Set to DRAFT
UPDATE opportunity SET state = 1 WHERE id = 'OPPORTUNITY_ID' RETURNING id, state, title;

-- Set to CLOSED
UPDATE opportunity SET state = 3 WHERE id = 'OPPORTUNITY_ID' RETURNING id, state, title;

-- Set to IN_REVIEW
UPDATE opportunity SET state = 4 WHERE id = 'OPPORTUNITY_ID' RETURNING id, state, title;
```

## Instructions

When the user asks for local environment help:

1. **For SQL queries**: First find the postgres container, then execute via docker exec
2. **For fake payments**: Determine if they're providing an opportunity ID or organization ID, run the appropriate SQL
3. **Always verify**: After changes, run a SELECT to confirm
4. **Ask if unclear**: If the request is ambiguous, ask clarifying questions

Common requests:
- "Set up fake payment for opportunity X" → Run both org and opportunity updates
- "Set up fake payment for org X" → Run only org update
- "Run SQL: ..." → Execute via docker
- "Reset payment for X" → Run reset queries
- "Check subscription for X" → Query and display current state
- "Update opp X to live/draft/closed" → Update opportunity state

## Discovering Schema Information

When handling requests not covered in this skill, use these techniques to discover the correct schema:

### 1. Check Entity Definitions

Entity files define column names and types:
```bash
# Find the entity file
grep -r "TableName" src/entity/ --include="*.ts"
# Read the entity to see column definitions
```

Key location: `src/entity/` - TypeORM entities with `@Column` decorators show actual DB column names.

### 2. Find Enum Values

Many columns use integer enums from `@dailydotdev/schema`. To find enum values:

```bash
# Search for enum usage in codebase
grep -r "EnumName\." src/ --include="*.ts" | head -20

# Find enum definition in schema package
grep -r "EnumName" node_modules/@dailydotdev/schema/dist/ --include="*.d.ts"
```

Common enum locations: `node_modules/@dailydotdev/schema/dist/daily-api/*_pb.d.ts`

### 3. Query Existing Data

When unsure about column names or values:
```sql
-- Check table structure
\d tablename

-- See existing values
SELECT DISTINCT column_name FROM tablename LIMIT 10;

-- Inspect a specific row
SELECT * FROM tablename WHERE id = 'xxx' LIMIT 1;
```

### 4. Common Gotchas

- **Column naming**: Entity property names may differ from DB columns (e.g., `state` not `status`)
- **Integer enums**: Many "status" fields are integers, not strings - find the enum definition
- **JSONB fields**: Use `jsonb_build_object()` for updates, `->` or `->>` for queries
- **Quoted columns**: PostgreSQL requires double quotes for camelCase columns (e.g., `"organizationId"`)

## Continuous Improvement

This skill should evolve over time. When you discover new local environment operations, common testing patterns, or useful queries:

1. **Add them to this file** - Update the SKILL.md with new sections or examples
2. **Keep it practical** - Focus on operations that are frequently needed
3. **Document the why** - Explain what fields mean and why certain values are used

If a user asks for something not covered here, help them and then offer to add it to this skill for future use.
