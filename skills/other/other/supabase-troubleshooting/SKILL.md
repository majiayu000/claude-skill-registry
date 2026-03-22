---
name: supabase-troubleshooting
description: Troubleshoot common Supabase issues including auth errors, RLS policies, connection problems, and performance. Use when debugging Supabase issues, fixing errors, or optimizing performance.
---

# Supabase Troubleshooting Skill

Debug and fix common Supabase issues.

## Quick Diagnosis

| Symptom | Likely Cause |
|---------|--------------|
| Empty data returned | RLS policies blocking access |
| "Not authorized" | Missing or invalid auth token |
| "JWT expired" | Token needs refresh |
| Slow queries | Missing indexes or RLS subqueries |
| Connection refused | Wrong URL or service down |
| "Duplicate key" | Unique constraint violation |
| Function timeout | Cold start or heavy computation |

## Authentication Issues

### "Invalid login credentials"

```javascript
// Check email format
const { data, error } = await supabase.auth.signInWithPassword({
  email: email.toLowerCase().trim(),  // Normalize email
  password
})

// Check if user exists
const { data } = await supabase
  .from('auth.users')  // Admin only
  .select('*')
  .eq('email', email)
```

### "Email not confirmed"

```javascript
// Option 1: Resend confirmation
const { error } = await supabase.auth.resend({
  type: 'signup',
  email: 'user@example.com'
})

// Option 2: Admin confirm (server-side)
await supabaseAdmin.auth.admin.updateUserById(userId, {
  email_confirm: true
})
```

### "JWT expired"

```javascript
// Client auto-refreshes, but you can force it
const { data, error } = await supabase.auth.refreshSession()

// Listen for token refresh
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'TOKEN_REFRESHED') {
    // Update any cached tokens
  }
})
```

### Session Not Persisting

```javascript
// Check storage configuration
const supabase = createClient(url, key, {
  auth: {
    persistSession: true,  // Default is true
    storage: localStorage  // Or custom storage
  }
})

// Check for multiple instances
// Only create one Supabase client per app
```

## Row Level Security (RLS) Issues

### Empty Data Returned

```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- Check existing policies
SELECT * FROM pg_policies
WHERE tablename = 'your_table';

-- Test policy with your user ID
SET request.jwt.claims = '{"sub": "your-user-uuid", "role": "authenticated"}';
SELECT * FROM your_table;
```

### "violates row-level security policy"

```javascript
// Check you're authenticated
const { data: { user } } = await supabase.auth.getUser()
console.log('Current user:', user?.id)

// Check the RLS policy requirements
// Common issue: auth.uid() doesn't match row's user_id
```

### Debug RLS Policies

```sql
-- Enable detailed RLS debugging (temporary)
SET log_statement = 'all';
SET log_min_duration_statement = 0;

-- Test as specific user
SET request.jwt.claims = '{
  "sub": "user-uuid",
  "role": "authenticated",
  "aal": "aal1"
}';

-- Run your query
SELECT * FROM posts;

-- Check auth functions
SELECT auth.uid();
SELECT auth.role();
SELECT auth.jwt();
```

### RLS Performance Issues

```sql
-- Bad: Calls auth.uid() for each row
CREATE POLICY "slow" ON posts
USING (auth.uid() = user_id);

-- Good: Caches auth.uid() result
CREATE POLICY "fast" ON posts
USING ((SELECT auth.uid()) = user_id);

-- Add indexes for RLS columns
CREATE INDEX idx_posts_user_id ON posts(user_id);
```

## Database Issues

### "duplicate key value violates unique constraint"

```javascript
// Use upsert instead of insert
const { data, error } = await supabase
  .from('table')
  .upsert({ id: existingId, ...values }, {
    onConflict: 'id'
  })
  .select()
```

### "foreign key violation"

```javascript
// Ensure referenced row exists
const { data: parent } = await supabase
  .from('parent_table')
  .select('id')
  .eq('id', parentId)
  .single()

if (!parent) {
  // Create parent first or handle error
}
```

### Query Returning Stale Data

```javascript
// Disable cache for specific queries
const { data } = await supabase
  .from('table')
  .select('*')
  .eq('id', id)
  .single()
  .throwOnError()  // Actually throws on error

// Force fresh data
const { data } = await supabase
  .from('table')
  .select('*', { head: false, count: 'exact' })
```

## Connection Issues

### "Failed to fetch" / Network Error

```javascript
// Check Supabase URL
console.log('URL:', process.env.NEXT_PUBLIC_SUPABASE_URL)

// Check API key
console.log('Key prefix:', process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY?.slice(0, 20))

// Test connection
const { data, error } = await supabase.from('_health').select('*')
console.log('Health check:', { data, error })
```

### Local Development Connection

```bash
# Check Docker is running
docker ps

# Check Supabase status
supabase status

# Restart if needed
supabase stop
supabase start
```

### CORS Issues

```javascript
// Edge function must include CORS headers
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type'
}

// Always handle OPTIONS preflight
if (req.method === 'OPTIONS') {
  return new Response('ok', { headers: corsHeaders })
}
```

## Storage Issues

### Upload Failing

```javascript
const { data, error } = await supabase.storage
  .from('bucket')
  .upload('path', file)

if (error) {
  // Check error type
  if (error.message.includes('exceeded')) {
    console.log('File too large')
  } else if (error.message.includes('mime type')) {
    console.log('Invalid file type')
  } else if (error.message.includes('row-level security')) {
    console.log('RLS policy blocking upload')
  }
}
```

### Storage RLS Debug

```sql
-- Check storage policies
SELECT * FROM pg_policies
WHERE tablename = 'objects'
AND schemaname = 'storage';

-- Common fix: Allow authenticated uploads to user folder
CREATE POLICY "Upload to own folder"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'uploads'
  AND auth.uid()::text = (storage.foldername(name))[1]
);
```

## Edge Function Issues

### Function Timeout (504)

```typescript
// Check for blocking operations
// Bad: Long synchronous operation
const result = heavyComputation()

// Good: Keep operations async and fast
const result = await heavyComputationAsync()

// Check limits:
// - CPU time: 2 seconds
// - Wall clock: 150s (400s on Pro)
```

### Function Error (500)

```typescript
// Always wrap in try-catch
try {
  const result = await riskyOperation()
  return new Response(JSON.stringify({ data: result }))
} catch (error) {
  console.error('Function error:', error)
  return new Response(
    JSON.stringify({ error: error.message }),
    { status: 500 }
  )
}
```

### Secrets Not Available

```bash
# Check secrets are set
supabase secrets list

# Set missing secrets
supabase secrets set API_KEY=value

# Note: Changes apply immediately, no redeploy needed
```

## Realtime Issues

### Not Receiving Events

```javascript
// 1. Check table has realtime enabled
// SQL: ALTER PUBLICATION supabase_realtime ADD TABLE your_table;

// 2. Check subscription status
const channel = supabase
  .channel('test')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'posts' }, callback)
  .subscribe((status, err) => {
    console.log('Subscription status:', status, err)
  })

// 3. Check RLS allows SELECT
// Realtime respects RLS policies
```

### "Tried to subscribe multiple times"

```javascript
// Don't call subscribe() twice on same channel
const channel = supabase.channel('my-channel')
channel.subscribe()  // OK
channel.subscribe()  // Error!

// Cleanup before resubscribing
await supabase.removeChannel(channel)
const newChannel = supabase.channel('my-channel').subscribe()
```

### Too Many Connections

```javascript
// Clean up channels on unmount
useEffect(() => {
  const channel = supabase.channel('data')
    .on('postgres_changes', {...}, callback)
    .subscribe()

  return () => {
    supabase.removeChannel(channel)  // Important!
  }
}, [])
```

## Performance Optimization

### Slow Queries

```sql
-- Use EXPLAIN ANALYZE to find bottlenecks
EXPLAIN ANALYZE SELECT * FROM posts WHERE user_id = 'uuid';

-- Add missing indexes
CREATE INDEX CONCURRENTLY idx_posts_user_id ON posts(user_id);

-- Check for sequential scans
SELECT relname, seq_scan, idx_scan
FROM pg_stat_user_tables
ORDER BY seq_scan DESC;
```

### High Connection Count

```bash
# Check connections
supabase inspect db role-connections --linked

# Use connection pooling for serverless
# Use transaction mode, not session mode
```

### Optimize RLS Queries

```sql
-- Avoid subqueries in hot path
-- Bad:
USING (user_id IN (SELECT user_id FROM team_members WHERE team_id = ...))

-- Good: Use security definer function
CREATE FUNCTION get_user_teams()
RETURNS SETOF uuid
LANGUAGE sql STABLE SECURITY DEFINER
AS $$ SELECT team_id FROM team_members WHERE user_id = auth.uid() $$;

USING (team_id IN (SELECT get_user_teams()))
```

## Common Error Codes

### PostgREST Errors (PGRST*)

| Code | Description | Solution |
|------|-------------|----------|
| `PGRST116` | No rows found (single expected) | Use `maybeSingle()` instead of `single()` |
| `PGRST205` | Table not found in schema cache | Check table name spelling, verify table exists |
| `PGRST301` | Multiple rows (single expected) | Add unique constraint or better filter |

### PostgreSQL Errors

| Code | Description | Solution |
|------|-------------|----------|
| `22P02` | Invalid input syntax (e.g., bad UUID) | Validate input format before query |
| `23503` | Foreign key violation | Ensure parent row exists first |
| `23505` | Unique constraint violation | Use upsert or check existence |
| `42501` | Insufficient privilege (RLS) | Fix RLS policies or use service role |
| `42703` | Column does not exist | Check column name spelling |
| `42P01` | Relation (table) doesn't exist | Check table name and schema |
| `08P01` | Protocol violation | Check query syntax |

### Auth Errors

| Error | Description | Solution |
|-------|-------------|----------|
| `Invalid API key` | Wrong or missing apikey header | Check SUPABASE_ANON_KEY |
| `JWT expired` | Access token expired | Call `refreshSession()` |
| `Invalid login credentials` | Wrong email/password | Verify credentials |

## References

- [common-errors.md](references/common-errors.md) - Error code reference
