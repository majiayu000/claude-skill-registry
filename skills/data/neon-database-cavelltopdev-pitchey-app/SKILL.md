---
name: neon-database
description: Neon PostgreSQL patterns for Pitchey. Raw SQL only, no ORM. Uses Hyperdrive for connection pooling. Activates for database queries, migrations, or schema work.
triggers:
  - database
  - sql
  - query
  - neon
  - postgres
  - migration
  - schema
  - table
  - select
  - insert
  - update
  - delete
---

# Neon Database Patterns for Pitchey

## CRITICAL: Connection Pattern

ALWAYS use Hyperdrive in Workers. NEVER use direct Neon connection string.

```typescript
import postgres from 'postgres';

export default {
  async fetch(request: Request, env: Env) {
    // ✅ CORRECT - Use Hyperdrive binding
    const sql = postgres(env.HYPERDRIVE.connectionString);
    
    // ❌ WRONG - Never use direct URL
    // const sql = postgres(process.env.DATABASE_URL);
    
    // ❌ WRONG - Never use Neon pooler with Hyperdrive
    // const sql = postgres('postgres://...pooler.us-east-2.aws.neon.tech/...');
    
    const result = await sql`SELECT * FROM users LIMIT 10`;
    return Response.json(result);
  }
}
```

## Query Patterns (Raw SQL - No ORM)

### Select with Parameters
```typescript
// Safe parameterized query (prevents SQL injection)
const users = await sql`
  SELECT * FROM users WHERE id = ${userId}
`;

// Multiple parameters
const pitches = await sql`
  SELECT * FROM pitches 
  WHERE creator_id = ${creatorId} 
  AND status = ${status}
  ORDER BY created_at DESC
  LIMIT ${limit}
`;
```

### Insert and Return
```typescript
const [newPitch] = await sql`
  INSERT INTO pitches (title, description, creator_id)
  VALUES (${title}, ${description}, ${creatorId})
  RETURNING *
`;
```

### Update
```typescript
const [updated] = await sql`
  UPDATE pitches 
  SET title = ${title}, updated_at = NOW()
  WHERE id = ${pitchId} AND creator_id = ${userId}
  RETURNING *
`;
```

### Delete
```typescript
await sql`
  DELETE FROM pitches 
  WHERE id = ${pitchId} AND creator_id = ${userId}
`;
```

### Transactions
```typescript
await sql.begin(async (tx) => {
  await tx`UPDATE accounts SET balance = balance - ${amount} WHERE id = ${fromId}`;
  await tx`UPDATE accounts SET balance = balance + ${amount} WHERE id = ${toId}`;
  await tx`INSERT INTO transfers (from_id, to_id, amount) VALUES (${fromId}, ${toId}, ${amount})`;
});
```

## Common Pitchey Queries

### Users
```sql
-- Get user by ID
SELECT * FROM users WHERE id = ${userId};

-- Get user with profile
SELECT u.*, p.bio, p.avatar_url 
FROM users u 
LEFT JOIN profiles p ON u.id = p.user_id 
WHERE u.id = ${userId};

-- Get user by email (for auth)
SELECT * FROM users WHERE email = ${email};
```

### Pitches
```sql
-- Trending pitches (most views in 7 days)
SELECT p.*, u.name as creator_name, u.avatar_url as creator_avatar
FROM pitches p
JOIN users u ON p.creator_id = u.id
WHERE p.status = 'published'
  AND p.created_at > NOW() - INTERVAL '7 days'
ORDER BY p.view_count DESC
LIMIT ${limit};

-- New releases (most recent)
SELECT p.*, u.name as creator_name, u.avatar_url as creator_avatar
FROM pitches p
JOIN users u ON p.creator_id = u.id
WHERE p.status = 'published'
ORDER BY p.created_at DESC
LIMIT ${limit};

-- Single pitch with creator
SELECT p.*, u.name as creator_name, u.email as creator_email
FROM pitches p
JOIN users u ON p.creator_id = u.id
WHERE p.id = ${pitchId};
```

### NDAs
```sql
-- Get NDA with both parties
SELECT n.*, 
  req.name as requester_name, req.email as requester_email,
  own.name as owner_name, own.email as owner_email,
  p.title as pitch_title
FROM ndas n
JOIN users req ON n.requester_id = req.id
JOIN users own ON n.owner_id = own.id
JOIN pitches p ON n.pitch_id = p.id
WHERE n.id = ${ndaId};

-- Pending NDAs for owner
SELECT n.*, u.name as requester_name, p.title as pitch_title
FROM ndas n
JOIN users u ON n.requester_id = u.id
JOIN pitches p ON n.pitch_id = p.id
WHERE n.owner_id = ${ownerId} AND n.status = 'pending'
ORDER BY n.created_at DESC;

-- Update NDA status
UPDATE ndas 
SET status = ${status}, 
    updated_at = NOW(),
    ${status === 'approved' ? sql`approved_at = NOW()` : sql``}
WHERE id = ${ndaId}
RETURNING *;
```

## Migrations

Store in `/migrations/` with timestamp prefix. Run via Neon console or MCP.

```sql
-- migrations/20260102_001_add_nda_fields.sql

-- Add signature tracking
ALTER TABLE ndas ADD COLUMN IF NOT EXISTS signed_at TIMESTAMPTZ;
ALTER TABLE ndas ADD COLUMN IF NOT EXISTS signature_url TEXT;
ALTER TABLE ndas ADD COLUMN IF NOT EXISTS rejection_reason TEXT;

-- Add index for faster queries
CREATE INDEX IF NOT EXISTS idx_ndas_status ON ndas(status);
CREATE INDEX IF NOT EXISTS idx_ndas_owner ON ndas(owner_id, status);
CREATE INDEX IF NOT EXISTS idx_ndas_requester ON ndas(requester_id, status);
```

## Performance Tips

1. Always use LIMIT on list queries
2. Add indexes for columns in WHERE and JOIN clauses
3. Use EXPLAIN ANALYZE to check query plans
4. Avoid SELECT * in production - select only needed columns
5. Use transactions for multi-table updates
6. Connection is managed by Hyperdrive - don't worry about pooling